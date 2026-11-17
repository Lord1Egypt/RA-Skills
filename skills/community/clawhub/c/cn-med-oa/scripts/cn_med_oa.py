#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cn_med_oa v2 — 中文医学文献 OA 聚合下载连接器。

架构镜像 paper-to-story/scripts/fulltext_connector.py（多源优先级 + 透明降级 +
disclosure 来源标注 + manifest 落盘）；验证哲学移植 pubmed-verifier v2.1.5
（五态判定、双重模糊匹配、SQLite 缓存、重试退避——模糊匹配已做中文自适应改造）。

数据源：维普OA平台 oa.cqvip.com（免登录、免费、OA 全文）。
API 契约见 references/weipu-oa-api-contract.md。

v2 关键改进（针对评审 P0/P1/P2）：
  P0-1 卷期权威化   : objectInfo.vol/num 为主源，PDF文本交叉验证，DOI正则仅兜底并标记
  P0-2 相关性守门   : 每条结果计算 relevance(ok/low/irrelevant)，多词查询降级提示
  P1-1 页码提取     : PDF 全页页脚模式扫描
  P1-3 SQLite 缓存  : 元数据 30 天 TTL；PDF 按 id 去重，不重复下载
  P2   重试退避     : 3 次指数退避(1s/2s/4s)；日下载配额(默认50)；SSL 校验开关

用法：
  python cn_med_oa.py --query 类风湿关节炎 --field title --max 5 --out-dir ./cn_refs
  python cn_med_oa.py --query 系统性红斑狼疮 --field subject --max 10 --no-pdf
"""
import os, sys, json, re, time, argparse, hashlib, sqlite3, unicodedata, urllib.request, urllib.parse, ssl
from difflib import SequenceMatcher

# ===== 配置（环境变量可覆盖）=====
WEIPU_BASE = os.environ.get("WEIPU_OA_BASE", "https://oa.cqvip.com/dajia-oa-app")
DOWNLOAD_MIN_INTERVAL = float(os.environ.get("CN_MED_OA_INTERVAL", "3.0"))
DAILY_MAX = int(os.environ.get("CN_MED_OA_DAILY_MAX", "50"))
META_TTL_DAYS = int(os.environ.get("CN_MED_OA_META_TTL", "30"))
CACHE_DIR = os.environ.get("CN_MED_OA_CACHE", os.path.join(os.path.expanduser("~"), ".cache", "cn-med-oa"))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
SKILL_VER = "2.4.0"

# ===== 检索词助手（v2.4.0，纯本地零网络）：口语→规范术语，高置信人工 curated，宁缺毋滥 =====
TERM_MAP = [
    # (口语词, 规范检索词, 说明；规范词为空=歧义词只给提示)
    ("类风湿", "类风湿关节炎", ""),
    ("尿酸高", "高尿酸血症", "有痛风发作史直接查「痛风」"),
    ("心梗", "心肌梗死", ""),
    ("脑梗", "脑梗死", "缺血性脑卒中可另查一次"),
    ("中风", "脑卒中", ""),
    ("老慢支", "慢性阻塞性肺疾病", "简称 COPD"),
    ("甲亢", "甲状腺功能亢进", ""),
    ("甲减", "甲状腺功能减退", ""),
    ("血压高", "高血压", ""),
    ("血脂高", "血脂异常", "指南标题多用「血脂异常」"),
    ("小孩发烧", "儿童发热", ""),
    ("小儿发烧", "儿童发热", ""),
    ("孩子咳嗽", "儿童咳嗽", ""),
    ("过敏性咳嗽", "咳嗽变异性哮喘", ""),
    ("幽门螺旋杆菌", "幽门螺杆菌", "规范名（螺旋→螺）"),
    ("肾衰", "慢性肾衰竭", "急性起病查「急性肾损伤」"),
    ("骨刺", "骨质增生", ""),
    ("诺如", "诺如病毒感染", ""),
    ("手足口", "手足口病", ""),
    ("糖甲", "", "歧义简称——请写全称"),
    ("紫癜", "", "歧义词：儿童常见为「过敏性紫癜」；血小板减少为「免疫性血小板减少症」，请先确认是哪种"),
    ("糖尿病", "", "歧义词：建议加分型词（1 型/2 型/妊娠期）再查，否则结果过宽"),
]


def suggest_terms(query):
    """口语→规范检索词建议。返回行列表（纯本地，零网络）。"""
    out = []
    s = (query or "").strip()
    if not s:
        return ["（空查询）"]
    parts = [p for p in re.split(r"\s+", s) if p]
    if len(parts) >= 2:
        out.append("⚠️ 检索平台是 OR 匹配：%d 个词会互相污染结果。建议拆成多次检索，每次只用一个短语：" % len(parts))
        for p in parts:
            out.append('    python scripts/cn_med_oa.py --query "%s"' % p)
    hit = False
    for collo, canon, note in TERM_MAP:
        if collo in s:
            hit = True
            if canon:
                extra = ("（%s）" % note) if note else ""
                out.append("💡 「%s」建议改用规范术语：「%s」%s" % (collo, canon, extra))
                out.append('    python scripts/cn_med_oa.py --query "%s"' % canon)
            else:
                out.append("⚠️ 「%s」%s" % (collo, note))
    if not hit and len(parts) == 1:
        out.append("✅ 「%s」看起来已是规范术语，可直接检索。" % s)
    if not out:
        out.append("✅ 未发现需要转换的口语词。")
    out.append("提示：平台没有「无结果」信号，所有结果都会经过相关性守门过滤；一次一个短语命中率最高。")
    return out


def humanize_neterr(att_txt):
    """网络失败白话层：从 attempts 摘要给「发生了什么/能做什么」。"""
    low = (att_txt or "").lower()
    if "timed out" in low or "timeout" in low:
        return ("💬 网络层：连接文献平台超时（平台偶尔慢）。可以：①等 1 分钟重试 ②加 --timeout 30 "
                "③避开晚间高峰。（技术详情见上方 attempts）")
    if "http 429" in low or "429" in low:
        return ("💬 网络层：被平台限流（请求过频）。本工具已自带每日 50 篇配额与 3 秒间隔；等几分钟再试即可。")
    if re.search(r"http 5\d\d", low) or "500" in low or "502" in low or "503" in low:
        return ("💬 网络层：平台服务器暂时故障（已自动重试 3 次）。稍后重试即可。")
    return ("💬 网络层：连接失败（可能网络中断或 DNS 异常）。检查网络后重试；机构内网请确认放行 oa.cqvip.com。")


# ===== HTTP（禁代理 + SSL 恒校验 + 重试退避，移植 pubmed-verifier _api_get 思路）=====
_ctx = ssl.create_default_context()
_opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({}),
    urllib.request.HTTPSHandler(context=_ctx))

RETRY_MAX, RETRY_BACKOFF = 3, (1, 2, 4)


def _sleep_backoff(attempt):
    if attempt < RETRY_MAX - 1:
        time.sleep(RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)])


def _jpost(path, data, timeout=30):
    """POST JSON，3 次指数退避。返回 (status, parsed|None, raw_text)。"""
    h = {"User-Agent": UA, "Origin": "https://oa.cqvip.com",
         "Referer": "https://oa.cqvip.com/paper", "Content-Type": "application/json"}
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    last = ""
    for attempt in range(RETRY_MAX):
        try:
            r = _opener.open(urllib.request.Request(WEIPU_BASE + path, data=body, headers=h), timeout=timeout)
            raw = r.read().decode("utf-8", "ignore")
            try:
                return r.status, json.loads(raw), raw
            except Exception:
                return r.status, None, raw
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", "ignore")
            if e.code >= 500:
                last = raw
                _sleep_backoff(attempt)
                continue
            return e.code, None, raw
        except (urllib.error.URLError, OSError) as e:
            last = str(e)
            _sleep_backoff(attempt)
    return None, None, "retry_exhausted: " + last[:120]


def _get_bytes(url, timeout=90):
    """GET 二进制，3 次指数退避。返回 (status, bytes)。"""
    h = {"User-Agent": UA, "Referer": "https://oa.cqvip.com/"}
    last = b""
    for attempt in range(RETRY_MAX):
        try:
            r = _opener.open(urllib.request.Request(url, headers=h), timeout=timeout)
            return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code >= 500:
                last = ("HTTP %d" % e.code).encode()
                _sleep_backoff(attempt)
                continue
            return e.code, e.read()
        except (urllib.error.URLError, OSError) as e:
            last = str(e).encode()
            _sleep_backoff(attempt)
    return None, last

# ===== SQLite 缓存 + 日配额（移植 pubmed-verifier 缓存模式，键改维普id）=====
def _cache_db():
    os.makedirs(CACHE_DIR, exist_ok=True)
    db = sqlite3.connect(os.path.join(CACHE_DIR, "cache.db"))
    db.execute("CREATE TABLE IF NOT EXISTS meta (id TEXT PRIMARY KEY, json TEXT, ts REAL)")
    db.execute("CREATE TABLE IF NOT EXISTS pdf (id TEXT PRIMARY KEY, path TEXT, sha256 TEXT, ts REAL)")
    db.execute("CREATE TABLE IF NOT EXISTS quota (day TEXT PRIMARY KEY, downloads INTEGER)")
    return db


def _cache_get_meta(pid):
    try:
        db = _cache_db()
        row = db.execute("SELECT json, ts FROM meta WHERE id=?", (pid,)).fetchone()
        db.close()
        if row and (time.time() - row[1]) < META_TTL_DAYS * 86400:
            return json.loads(row[1])
    except Exception:
        pass
    return None


def _cache_set_meta(pid, det):
    try:
        db = _cache_db()
        db.execute("INSERT OR REPLACE INTO meta VALUES (?,?,?)", (pid, json.dumps(det, ensure_ascii=False), time.time()))
        db.commit()
        db.close()
    except Exception:
        pass


def _cache_get_pdf(pid):
    try:
        db = _cache_db()
        row = db.execute("SELECT path, sha256 FROM pdf WHERE id=?", (pid,)).fetchone()
        db.close()
        if row and os.path.exists(row[0]):
            return {"path": row[0], "sha256": row[1]}
    except Exception:
        pass
    return None


def _cache_set_pdf(pid, path, sha256):
    try:
        db = _cache_db()
        db.execute("INSERT OR REPLACE INTO pdf VALUES (?,?,?,?)", (pid, path, sha256, time.time()))
        db.commit()
        db.close()
    except Exception:
        pass


def _quota_left():
    """当日剩余下载配额（跨进程，sqlite 计数）。"""
    today = time.strftime("%Y-%m-%d")
    try:
        db = _cache_db()
        row = db.execute("SELECT downloads FROM quota WHERE day=?", (today,)).fetchone()
        db.close()
        used = row[0] if row else 0
    except Exception:
        used = 0
    return DAILY_MAX - used


def _quota_consume():
    today = time.strftime("%Y-%m-%d")
    try:
        db = _cache_db()
        db.execute("INSERT INTO quota(day,downloads) VALUES(?,1) "
                   "ON CONFLICT(day) DO UPDATE SET downloads=downloads+1", (today,))
        db.commit()
        db.close()
    except Exception:
        pass

# ===== 中文自适应模糊匹配（移植 pubmed-verifier 双重匹配，改造点：中文 bigram）=====
_EN_STOP = {"a", "an", "the", "of", "in", "on", "for", "and", "to", "with", "by",
            "from", "is", "are", "was", "were", "at", "as", "or", "its", "it",
            "this", "that", "which", "be", "has", "have", "had", "not", "but",
            "also", "into", "than", "through", "during", "between", "their",
            "we", "they", "can", "may", "via", "no", "all", "such", "vs"}
_CJK_RE = re.compile(r"[\u4e00-\u9fff]")
_FULLWIDTH_PUNCT = "　，。、；：？！（）《》「」『』【】·—～…“”‘’"

# ── 核心期刊参考表（内置静态表，仅供快速参考，非官方目录）──
# 依据公开目录（北大核心2023版/CSCD2023-2024/科技核心2023）整理的高置信医学期刊。
# 合规说明：①未收录期刊一律不标注（宁缺毋滥，避免误导）；②可能滞后于最新官方目录，
# 权威判定请以官方目录为准。如需扩充可在此追加 "刊名": "级别"。
_CORE_JOURNALS = {
    # ── 中华医学会系列（高置信，北大核心+CSCD 双收录）──
    "中华内科杂志": "北大核心/CSCD",
    "中华医学杂志": "北大核心/CSCD",
    "中华外科杂志": "北大核心/CSCD",
    "中华妇产科杂志": "北大核心/CSCD",
    "中华儿科杂志": "北大核心/CSCD",
    "中华心血管病杂志": "北大核心/CSCD",
    "中华结核和呼吸杂志": "北大核心/CSCD",
    "中华消化杂志": "北大核心/CSCD",
    "中华血液学杂志": "北大核心/CSCD",
    "中华内分泌代谢杂志": "北大核心/CSCD",
    "中华肾脏病杂志": "北大核心/CSCD",
    "中华神经科杂志": "北大核心/CSCD",
    "中华精神科杂志": "北大核心/CSCD",
    "中华流行病学杂志": "北大核心/CSCD",
    "中华预防医学杂志": "北大核心/CSCD",
    "中华医院感染学杂志": "北大核心/CSCD",
    "中华护理杂志": "北大核心/CSCD",
    "中华病理学杂志": "北大核心/CSCD",
    "中华放射学杂志": "北大核心/CSCD",
    "中华肿瘤杂志": "北大核心/CSCD",
    "中华风湿病学杂志": "北大核心/CSCD",
    "中华检验医学杂志": "北大核心/CSCD",
    "中华老年医学杂志": "北大核心/CSCD",
    "中华急诊医学杂志": "北大核心/CSCD",
    "中华创伤杂志": "北大核心/CSCD",
    "中华麻醉学杂志": "北大核心/CSCD",
    "中华泌尿外科杂志": "北大核心/CSCD",
    "中华骨科杂志": "北大核心/CSCD",
    "中华口腔医学杂志": "北大核心/CSCD",
    "中华耳鼻咽喉头颈外科杂志": "北大核心/CSCD",
    "中华眼科杂志": "北大核心/CSCD",
    "中华皮肤科杂志": "北大核心/CSCD",
    "中华男科学杂志": "北大核心/CSCD",
    "中华中医药杂志": "北大核心/CSCD",
    "中华实验外科杂志": "北大核心/CSCD",
    "中华普通外科杂志": "北大核心/CSCD",
    "中华胃肠外科杂志": "北大核心/CSCD",
    "中华神经外科杂志": "北大核心/CSCD",
    "中华医学遗传学杂志": "北大核心/CSCD",
    "中华围产医学杂志": "北大核心/CSCD",
    "中华消化外科杂志": "北大核心/CSCD",
    "中华肝胆外科杂志": "北大核心/CSCD",
    "中华手外科杂志": "北大核心/CSCD",
    "中华显微外科杂志": "北大核心/CSCD",
    "中华整形外科杂志": "北大核心/CSCD",
    "中华烧伤杂志": "北大核心/CSCD",
    "中华器官移植杂志": "北大核心/CSCD",
    "中华行为医学与脑科学杂志": "北大核心/CSCD",
    "中华糖尿病杂志": "北大核心/CSCD",
    "中华老年心脑血管病杂志": "北大核心/CSCD",
    "中华全科医师杂志": "北大核心",
    "中华医院管理杂志": "北大核心/CSCD",
    "中华劳动卫生职业病杂志": "北大核心/CSCD",
    "中华放射医学与防护杂志": "北大核心/CSCD",
    # ── 中国实用/常见医学核心（高置信）──
    "中国实用内科杂志": "北大核心/CSCD",
    "中国实用外科杂志": "北大核心/CSCD",
    "中国实用儿科杂志": "北大核心",
    "中国实用妇科与产科杂志": "北大核心/CSCD",
    "中国中西医结合杂志": "北大核心/CSCD",
    "中国中药杂志": "北大核心/CSCD",
    "中国药理学通报": "北大核心/CSCD",
    "中国药学杂志": "北大核心/CSCD",
    "中国医院药学杂志": "北大核心",
    "中国临床药理学杂志": "北大核心",
    "中国医学科学院学报": "北大核心/CSCD",
    "中国循证医学杂志": "北大核心/CSCD",
    "中国全科医学": "北大核心",
    "中国卫生统计": "北大核心/CSCD",
    "中国公共卫生": "北大核心/CSCD",
    "中国学校卫生": "北大核心",
    "中国慢性病预防与控制": "北大核心",
    "中国康复医学杂志": "北大核心",
    "中国康复理论与实践": "北大核心",
    "中国运动医学杂志": "北大核心/CSCD",
    "中国疼痛医学杂志": "北大核心",
    "中国糖尿病杂志": "北大核心",
    "中国脊柱脊髓杂志": "北大核心",
    "中国矫形外科杂志": "北大核心",
    "中国修复重建外科杂志": "北大核心",
    "中国微创外科杂志": "北大核心",
    "中国内镜杂志": "北大核心",
    "中国普通外科杂志": "北大核心",
    "中国动脉硬化杂志": "北大核心",
    "中国循环杂志": "北大核心",
    "中国医学影像技术": "北大核心",
    "中国医学影像学杂志": "北大核心",
    "中国超声医学杂志": "北大核心",
    "中国介入影像与治疗学": "北大核心",
    "中国实验血液学杂志": "北大核心",
    "中国免疫学杂志": "北大核心",
    "中国病原生物学杂志": "北大核心",
    "中国疫苗和免疫": "北大核心",
    "中国医院管理": "北大核心",
    "中国卫生事业管理": "北大核心",
    "中国卫生经济": "北大核心",
    "中国护理管理": "北大核心",
    "中国急救医学": "北大核心",
    "中国现代神经疾病杂志": "北大核心",
    "中国微侵袭神经外科杂志": "北大核心",
    "中国脑血管病杂志": "北大核心",
    "中国神经精神疾病杂志": "北大核心/CSCD",
    "中国心理卫生杂志": "北大核心/CSCD",
    "中国临床心理学杂志": "北大核心/CSCD",
    "中国卫生政策研究": "北大核心",
    "中国医学伦理学": "北大核心",
    "中国健康教育": "北大核心",
    "中国妇幼保健": "北大核心",
    "中国儿童保健杂志": "北大核心",
    "中国当代儿科杂志": "北大核心",
    "中国组织工程研究": "北大核心",
    "中国生物医学工程学报": "北大核心/CSCD",
    "中国医学物理学杂志": "北大核心",
    "中国数字医学": "北大核心",
    "中国医疗器械杂志": "北大核心",
    "中国医学装备": "北大核心",
    "中国艾滋病性病": "北大核心",
    "中国皮肤性病学杂志": "北大核心",
    "中国男科学杂志": "北大核心",
    # ── 中西医药/药学（高置信）──
    "中国针灸": "北大核心/CSCD",
    "针刺研究": "北大核心/CSCD",
    "中医杂志": "北大核心/CSCD",
    "中草药": "北大核心/CSCD",
    "中成药": "北大核心",
    "中药材": "北大核心",
    "中药新药与临床药理": "北大核心",
    "中国实验方剂学杂志": "北大核心/CSCD",
    "中华中医药学刊": "北大核心",
    "时珍国医国药": "北大核心",
    "世界科学技术-中医药现代化": "北大核心",
    "中国中西医结合急救杂志": "北大核心",
    "中国中西医结合消化杂志": "北大核心",
    "中国中西医结合肾病杂志": "北大核心",
    "中国中西医结合外科杂志": "北大核心",
    "中国中西医结合皮肤性病学杂志": "北大核心",
    "中西医结合心脑血管病杂志": "北大核心",
    "药学学报": "北大核心/CSCD",
    "药物分析杂志": "北大核心",
    "中国药理学与毒理学杂志": "北大核心",
    "中国现代应用药学": "北大核心",
    "中国医药工业杂志": "北大核心",
    "中国抗生素杂志": "北大核心",
    "中国新药杂志": "北大核心",
    "中国临床药理学与治疗学": "北大核心",
    "中国药房": "北大核心",
    "中国药事": "北大核心",
    "中国医药生物技术": "北大核心",
    "中国生物制品学杂志": "北大核心",
    "中国病毒病杂志": "北大核心",
    "中国寄生虫学与寄生虫病杂志": "北大核心",
    # ── 高校学报（医学）──
    "北京大学学报(医学版)": "北大核心/CSCD",
    "复旦大学学报(医学版)": "北大核心/CSCD",
    "上海交通大学学报(医学版)": "北大核心/CSCD",
    "中山大学学报(医学科学版)": "北大核心/CSCD",
    "浙江大学学报(医学版)": "北大核心/CSCD",
    "华中科技大学学报(医学版)": "北大核心",
    "中南大学学报(医学版)": "北大核心/CSCD",
    "四川大学学报(医学版)": "北大核心/CSCD",
    "西安交通大学学报(医学版)": "北大核心/CSCD",
    "吉林大学学报(医学版)": "北大核心",
    "南方医科大学学报": "北大核心/CSCD",
    # ── 基础医学（高置信）──
    "基础医学与临床": "北大核心",
    "解剖学报": "北大核心",
    "解剖学杂志": "北大核心",
    "生理学报": "北大核心/CSCD",
    "中国病理生理杂志": "北大核心/CSCD",
    "生物化学与生物物理进展": "北大核心/CSCD",
}


def rank_journal(name):
    """核心期刊标注：内置参考表精确匹配（全角括号归一化后比较）。

    未收录返回 ""（不标注，宁缺毋滥）。电子版/子刊为独立刊名，不继承母刊级别。
    仅供快速参考，非官方权威判定。
    """
    if not name:
        return ""
    n = str(name).strip().replace("（", "(").replace("）", ")")
    if n in _CORE_JOURNALS:
        return _CORE_JOURNALS[n]
    return ""


def zh_clean(s):
    """清洗为可比对字符串：NFKC规范化(全角→半角,实测期刊PDF标题是'ｐｎｉ'全角)、
    全角标点→空格、压缩空白、小写。兼容中英文。"""
    s = unicodedata.normalize("NFKC", (s or "")).lower()
    for ch in _FULLWIDTH_PUNCT:
        s = s.replace(ch, " ")
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def zh_tokens(s):
    """token 集合 = 英文词(去停用词) + 中文相邻二元组(bigram)。

    pubmed-verifier 原版按空格分词，对无空格的中文失效——此为移植的核心兼容改造。
    """
    s = zh_clean(s)
    toks = set()
    for w in re.findall(r"[a-z0-9]+", s):
        if w not in _EN_STOP:
            toks.add(w)
    for run in re.findall(r"[\u4e00-\u9fff]+", s):
        if len(run) == 1:
            toks.add(run)
        else:
            for i in range(len(run) - 1):
                toks.add(run[i:i + 2])
    return toks


def zh_similarity(a, b):
    """双重相似度(移植 pubmed-verifier)：词级 Jaccard + 字级 SequenceMatcher。

    返回 (word_ratio, seq_ratio, score=max(两者))。中文场景两者均有效。
    """
    ta, tb = zh_tokens(a), zh_tokens(b)
    if ta and tb:
        overlap = ta & tb
        union = ta | tb
        word_ratio = len(overlap) / len(union) if union else 0.0
    else:
        word_ratio = 0.0
    seq_ratio = SequenceMatcher(None, zh_clean(a), zh_clean(b)).ratio()
    return round(word_ratio, 3), round(seq_ratio, 3), round(max(word_ratio, seq_ratio), 3)


def zh_title_match(a, b, word_th=0.5, seq_th=0.90):
    """标题匹配判定（阈值同 pubmed-verifier）。"""
    w, s, _ = zh_similarity(a, b)
    return (w >= word_th or s >= seq_th), w, s

# ===== 相关性守门（P0-2）=====
# 注：阈值体系与 pubmed-verifier 不同——那边是"标题vs标题"等长比对(Jaccard≥0.5)，
# 这边是"短查询vs长标题"相关性，必须用覆盖率制（查询token被覆盖比例），否则分母爆炸。
REL_OK, REL_LOW = 0.80, 0.50
_TITLE_FIELDS = ("title", "keyword", "subject")


def zh_coverage(query, text):
    """查询覆盖率：query 的 token(英文词+中文bigram) 被文本覆盖的比例。

    "类风湿关节炎" vs "类风湿性关节炎滑膜细胞..." = 4/5 = 0.80（ok）；
    "量子纠缠炒股" vs "量子纠缠源实验研究" = 3/5 = 0.60（low）。
    """
    tq, tt = zh_tokens(query), zh_tokens(text)
    if not tq or not tt:
        return 0.0
    return round(len(tq & tt) / len(tq), 3)


def _jpost_yiigle(path, data, timeout=30):
    """POST JSON 到中华医学期刊全文数据库（yiigle）API。返回 (status, parsed|None, raw)。"""
    h = {"User-Agent": UA, "Origin": "https://www.yiigle.com",
         "Referer": "https://www.yiigle.com/", "Content-Type": "application/json"}
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    last = ""
    for attempt in range(RETRY_MAX):
        try:
            r = _opener.open(urllib.request.Request("https://www.yiigle.com/apiVue" + path,
                                                    data=body, headers=h), timeout=timeout)
            raw = r.read().decode("utf-8", "ignore")
            try:
                return r.status, json.loads(raw), raw
            except Exception:
                return r.status, None, raw
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", "ignore")
            if e.code >= 500:
                last = raw
                _sleep_backoff(attempt)
                continue
            return e.code, None, raw
        except Exception as e:
            last = str(e)
            _sleep_backoff(attempt)
    return 0, None, last


YIIGLE_FIELDS = ("title", "keyword", "subject", "author", "journal", "fund")


def yiigle_search(keyword, field="title", page=1, size=20):
    """检索中华医学期刊全文数据库（CMA 系期刊 + 指南，维普OA不覆盖）。

    返回 (rows, err)。rows 元素为 dict，字段对齐 cn_med_oa 内部 schema
    （title/artId/artDoi/journalCn/year/vol/issue/pages/docType/artUrl）。
    """
    field_map = {"title": "pt", "keyword": "kw", "subject": "sb", "author": "au",
                 "journal": "jn", "fund": "ft"}
    q = keyword.strip()
    if not q:
        return [], "空检索词"
    query_string = q
    if field == "journal":
        query_string = f'JN:("{q}")'
    payload = {
        "type": "all", "sortField": "", "page": page, "searchType": field_map.get(field, "pt"),
        "pageSize": int(size), "queryString": query_string, "query": q,
        "searchText": q, "searchLog": "", "isAggregations": "N", "logintoken": "",
    }
    status, parsed, raw = _jpost_yiigle("/search/searchList", payload)
    if status != 200 or not parsed or parsed.get("code") != 200:
        return [], (raw[:150] if raw else f"HTTP {status}")
    result = parsed.get("data", {}).get("result", {})
    rows = []
    for info in result.get("infos", []):
        rows.append({
            "title": info.get("artTitle") or "",
            "id": str(info.get("artId") or ""),
            "artDoi": info.get("artDoi") or "",
            "journal": info.get("journalCn") or "",
            "year": str(info.get("artPubYear") or ""),
            "vol": str(info.get("vol") or ""),
            "issue": str(info.get("issue") or ""),
            "pages": (str(info.get("startPage") or "") + "-" + str(info.get("endPage") or "")),
            "docType": info.get("docType") or "",
            "artUrl": info.get("artUrl") or "",
            "abstract": info.get("artAbstract") or "",
            "authors": info.get("authorNames") or [],
            "source": "Yiigle",
        })
    return rows, None


def yiigle_try_download(art_id, save_dir, title):
    """yiigle PDF best-effort 下载：三步链路（token→auth→download）。

    resource/auth 必须带 reduceTimes=true（与官网前端一致）：false 时接口只返回
    hasPerm 不签发 token，OA 商品也会被误判为登录墙。OA 商品（如开放获取指南）
    匿名即可下载；真正付费文献 hasPerm=False 或无 token，此时返回 (None, None)
    —— 调用方把 artUrl 记为 download_url 供浏览器下载，不硬闯登录墙。
    返回 (path, sha256) 或 (None, None)。
    """
    try:
        h = {"User-Agent": UA, "Origin": "https://rs.yiigle.com",
             "Referer": f"https://rs.yiigle.com/cmaid/{art_id}",
             "Content-Type": "application/json"}
        body = json.dumps({"resourceId": str(art_id), "captchaCode": "", "captchaId": ""}).encode()
        r = _opener.open(urllib.request.Request(
            "https://rs.yiigle.com/api/file/downloadPdfToken", data=body, headers=h), timeout=20)
        d1 = json.loads(r.read().decode())
        dtoken = (d1.get("data") or {}).get("downloadToken")
        if not dtoken:
            return None, None
        req2 = urllib.request.Request(
            f"https://rs.yiigle.com/api/resource/auth?resourceId={art_id}&resPermType=d&reduceTimes=true",
            headers={"User-Agent": UA, "Referer": f"https://rs.yiigle.com/cmaid/{art_id}"})
        d2 = json.loads(_opener.open(req2, timeout=20).read().decode())
        data2 = d2.get("data") or {}
        if not (data2.get("hasPerm") and data2.get("token")):
            return None, None
        pdf_url = (f"https://rs.yiigle.com/api/file/downloadPdf?resourceId={art_id}"
                   f"&token={data2['token']}&downloadToken={dtoken}")
        r3 = _opener.open(urllib.request.Request(pdf_url, headers={"User-Agent": UA}), timeout=90)
        pdf = r3.read()
        if pdf[:5] != b"%PDF-":
            return None, None
        os.makedirs(save_dir, exist_ok=True)
        safe = re.sub(r'[\\/:*?"<>|·\s]+', "_", title)[:80].strip("_") or art_id
        path = os.path.join(save_dir, f"yiigle_{art_id}_{safe}.pdf")
        open(path, "wb").write(pdf)
        return path, hashlib.sha256(pdf).hexdigest()
    except Exception:
        return None, None


def yiigle_to_entry(row, rel, save_dir=None, want_pdf=False):
    """将 yiigle 检索行转为 manifest entry（对齐 to_vancouver 输出）。"""
    entry = {
        "title": row["title"],
        "authors": row["authors"],
        "journal": row["journal"],
        "year": row["year"],
        "volume": row["vol"],
        "issue": row["issue"],
        "pages": row["pages"],
        "doi": row["artDoi"],
        "docType": row["docType"],
        "artUrl": row["artUrl"],
        "abstract": row["abstract"],
        "relevance": rel,
        "source": "Yiigle",
        "license": "开放阅读",
        "needs_human_check": False,
    }
    entry["journal_rank"] = rank_journal(row["journal"])
    art_id = str(row.get("id") or "")
    if art_id:
        det = yiigle_detail(art_id)
        entry["issn"] = det.get("issn", "")
        entry["cnno"] = det.get("cnno", "")
        if det.get("journal_en"):
            entry["journal_en"] = det["journal_en"]
        if save_dir and want_pdf:
            _throttle()
            path, sha = yiigle_try_download(art_id, save_dir, row["title"])
            if path:
                entry["path"] = path
                entry["sha256"] = sha
            else:
                entry["download_url"] = row["artUrl"]
    return entry


_SSR_ESC_RE = re.compile(r'\\u([0-9a-fA-F]{4})|\\"|\\\\')


def _decode_ssr_escapes(s):
    """解码 SSR 内嵌 JSON 字符串转义：\\uXXXX → 字符、\\" → "、\\\\ → \\。

    只处理 JSON 字符串出现的三种转义，避免整体 unicode_escape
    （Python 3.12 起对无效转义序列发出 DeprecationWarning）。
    代理对（高代理\\uD800-\\uDBFF 后随低代理\\uDC00-\\uDFFF）组合为单码位。
    """
    out = []
    i, n = 0, len(s)
    while i < n:
        m = _SSR_ESC_RE.match(s, i)
        if not m:
            out.append(s[i])
            i += 1
            continue
        if m.group(1):
            cp = int(m.group(1), 16)
            i = m.end()
            if 0xD800 <= cp <= 0xDBFF and i + 1 < n:
                m2 = _SSR_ESC_RE.match(s, i)
                if m2 and m2.group(1):
                    lo = int(m2.group(1), 16)
                    if 0xDC00 <= lo <= 0xDFFF:
                        out.append(chr(0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00)))
                        i = m2.end()
                        continue
            out.append(chr(cp))
        elif m.group(0) == '\\"':
            out.append('"')
            i = m.end()
        else:
            out.append("\\")
            i = m.end()
    return "".join(out)


def yiigle_detail(art_id):
    """抓取 rs.yiigle.com 详情页，解析 JATS 元数据补全 ISSN/CN刊号/英文刊名。

    详情页是 Nuxt SSR，完整 JATS XML 以 Unicode 转义内嵌在 HTML 中。
    返回 {"issn":..., "cnno":..., "journal_en":..., "journal":...}（缺失字段为空串）。
    """
    det = _cache_get_meta("yiigle_" + str(art_id))
    if det:
        return det
    out = {"issn": "", "cnno": "", "journal_en": "", "journal": ""}
    try:
        r = _opener.open(urllib.request.Request(
            f"https://rs.yiigle.com/cmaid/{art_id}",
            headers={"User-Agent": UA, "Referer": "https://www.yiigle.com/"}), timeout=25)
        raw = r.read().decode("utf-8", "ignore")
        decoded = _decode_ssr_escapes(raw)
        m = re.search(r"<journal-meta>(.*?)</journal-meta>", decoded, re.S)
        if m:
            seg = m.group(1)
            issns = re.findall(r"<issn[^>]*>([^<]+)</issn>", seg)
            nums = [x.strip() for x in issns if x.strip()]
            if nums:
                out["issn"] = nums[0]
                # JATS 里 CN 刊号常作为第二个 issn（形如 11-2138/R）
                for x in nums[1:]:
                    if re.match(r"^\d{2}-\d{4}/", x):
                        out["cnno"] = x
                        break
            titles = re.findall(r"<journal-title[^>]*>([^<]+)</journal-title>", seg)
            if len(titles) >= 2:
                out["journal_en"] = titles[1].strip()
            elif titles:
                # 单标题时按是否含 CJK 判定
                t = titles[0].strip()
                if has_cjk(t):
                    out["journal"] = t
                else:
                    out["journal_en"] = t
    except Exception:
        pass
    _cache_set_meta("yiigle_" + str(art_id), out)
    return out


def has_cjk(s):
    """True if string contains CJK ideographs."""
    return any('\u4e00' <= ch <= '\u9fff' for ch in str(s or ""))


def relevance_gate(query, row, field):
    """计算单条结果与查询的相关性。返回 {score, state, coverage, note}。

    多词查询按词取最小覆盖率（"专家共识 风湿"若"风湿"未覆盖则整体降级），
    并在 note 中指出缺失词。不删除低相关结果——只标记（透明降级原则）。
    """
    title = row.get("title") or row.get("name") or ""
    if field in _TITLE_FIELDS:
        kw = " ".join((x.get("name") or "") for x in (row.get("keywordInfo") or []))
        blob = title if zh_coverage(query, title) >= REL_OK else (title + " " + kw)
        terms = [t for t in query.split() if t.strip()]
        if len(terms) > 1:
            covs = [zh_coverage(t, blob) for t in terms]
            score = min(covs)
            missing = [t for t, c in zip(terms, covs) if c < REL_LOW]
            note = ("缺失词: " + ",".join(missing) + "；建议拆分为单短语分别检索") if missing else ""
        else:
            score = zh_coverage(query, blob)
            note = ""
        state = "ok" if score >= REL_OK else ("low" if score >= REL_LOW else "irrelevant")
        return {"score": score, "state": state, "coverage": score, "note": note}
    # 字段型检索（作者/刊名/机构/基金）：用字段包含性判定
    keymap = {"author": ("firstAuthor",), "journal": ("name",),
              "inst": (), "fund": ()}
    blob = ""
    fa = row.get("firstAuthor") or {}
    if field == "author":
        blob = (fa.get("name") or "") + " " + " ".join(
            (x.get("name") or "") for x in (row.get("authorInfo") or []))
    elif field == "journal":
        blob = title
    hit = zh_clean(query) in zh_clean(blob) if blob else False
    score = 1.0 if hit else 0.0
    return {"score": score, "state": "ok" if hit else "low", "word": 0, "seq": 0, "note": ""}

# ===== 维普 OA 适配器 =====
WEIPU_FIELDS = {"title": "T", "keyword": "K", "subject": "M",
                "author": "A", "journal": "J", "inst": "S", "fund": "F"}


def weipu_search(keyword, field="title", page=1, size=20):
    f = WEIPU_FIELDS.get(field, "T")
    body = {"advancedSearchList": [{"field": f, "content": keyword, "logicalOperator": "AND"}],
            "aggsParams": {"C": [], "I": []}, "page": page, "size": size}
    st, j, raw = _jpost("/api/paperSearchApi/search", body)
    if not j or not j.get("success"):
        return [], (raw or "")[:200]
    return j.get("rows") or (j.get("data") or {}).get("rows") or [], None


def weipu_detail(pid):
    """详情（带缓存）。返回完整 detail dict 或 None。"""
    cached = _cache_get_meta(pid)
    if cached is not None:
        return cached
    st, j, raw = _jpost("/api/paperSearchApi/literatureBaseDetails", {"id": pid})
    if not j or not j.get("success"):
        return None
    data = j.get("data") or []
    det = data[0] if data else None
    if det:
        _cache_set_meta(pid, det)
    return det

# ===== 卷期页三级策略（P0-1 + P1-1）=====
_DOI_VOL_RE = re.compile(r"\.(\d{4})\.(\d{1,3})\.(\d{1,3})")


def extract_vol_issue(det, pdf_text=""):
    """卷期提取三级策略。

    1. objectInfo.vol/num（维普详情 API 权威字段，主源）
    2. PDF 首页 "第N卷第M期" 文本（交叉验证，标记一致性）
    3. DOI 正则 年.卷.期（最后手段，source=doi_guess 需人工核对——10.3969 等
       前缀实为 年.期.文章号，正则会误析，故仅当 1/2 均缺失时使用）
    """
    obj = (det or {}).get("objectInfo") or {}
    vol = str(obj.get("vol") or "")
    issue = str(obj.get("num") or "")
    source = "api" if vol else ""
    pdf_vol = pdf_iss = ""
    if pdf_text:
        # ⚠️ 只在页眉区(首页前220字)找"第N卷第M期"——正文/参考文献里也有其他文献的卷期，
        # 全文匹配会误判不一致（实测踩坑：医学临床研究正文含引用文献的卷号）
        masthead = pdf_text[:220]
        mv = re.search(r"第\s*(\d{1,3})\s*卷", masthead)
        mi = re.search(r"第\s*(\d{1,3})\s*期", masthead)
        pdf_vol, pdf_iss = (mv.group(1) if mv else ""), (mi.group(1) if mi else "")
    if not vol and pdf_vol:
        vol, issue, source = pdf_vol, pdf_iss or issue, "pdf"
    if not vol:
        doi = (det or {}).get("doi") or ""
        m = _DOI_VOL_RE.search(doi)
        if m:
            vol, issue, source = m.group(2), m.group(3), "doi_guess"
    consistent = True
    if vol and pdf_vol and pdf_vol != vol:
        consistent = False
    if issue and pdf_iss and pdf_iss != issue:
        consistent = False
    return {"volume": vol, "issue": issue, "vol_source": source or "missing",
            "vol_consistent": consistent,
            "needs_human_check": source == "doi_guess" or not consistent}


def extract_pages(pdf_path):
    """页码提取：扫描每页页脚(尾部60字)的 "· 770" 模式。返回 (pages_str, source)。

    实测中文期刊页脚形如 "·\\n· 770"（点+数字，无尾点），且逐页递增。
    要求：≥2页命中、严格递增、跨度≤30 → "770-774"。
    """
    try:
        import fitz
        doc = fitz.open(pdf_path)
        texts = [p.get_text() for p in doc]
        doc.close()
    except Exception:
        return "", "no_extractor"
    seq = []
    for t in texts:
        m = re.search(r"[·•]\s*(\d{3,4})\s*$", t[-60:].rstrip()[-40:] + "\n", re.M) or \
            re.search(r"[·•]\s*(\d{3,4})", t[-60:])
        if m:
            try:
                seq.append(int(m.group(1)))
            except ValueError:
                pass
    seq = [x for x in seq if 1 <= x <= 9999]
    if len(seq) >= 2:
        inc = all(seq[i] < seq[i + 1] for i in range(len(seq) - 1))
        if inc and (seq[-1] - seq[0]) <= 30:
            return "%d-%d" % (seq[0], seq[-1]), "pdf_footer"
    head = texts[0][:900] if texts else ""
    mp = re.search(r"[:：]\s*(\d{1,4})\s*[-–—~]\s*(\d{1,4})", head)
    if mp and abs(int(mp.group(1)) - int(mp.group(2))) < 50:
        return "%s-%s" % (mp.group(1), mp.group(2)), "pdf_head"
    # v2.2 增强：DOI 行页码（中文期刊 PDF 首页常含 "doi:...j.issn.xxxx.yyyy.nn.nnn"，
    # 末段 nnn 即起始页）；页眉"第N卷第M期·NNN"模式；独立"·NNN·"中缀模式
    mdoi = re.search(r"doi:\s*10\.\d{4,5}/[^\s]*?[.\-](\d{3,4})\s*$", head, re.M | re.I) or \
        re.search(r"10\.\d{4,5}/[^\s]*?[.\-](\d{3,4})\b", head)
    if mdoi:
        pg = int(mdoi.group(1))
        if 1 <= pg <= 9999:
            if seq:
                return "%d-%d" % (min(pg, min(seq)), max(pg + len(texts) - 1, max(seq))), "doi_seq"
            return str(pg), "doi_guess"
    for t in texts[:3]:
        mh = re.search(r"第\d+卷\s*第\d+期[·\s]*(\d{3,4})", t[:400])
        if mh:
            pg = int(mh.group(1))
            return "%d-%d" % (pg, pg + len(texts) - 1), "pdf_header"
    if seq:
        return str(min(seq)), "pdf_footer_single"
    return "", "missing"


def pdf_first_pages_text(pdf_path, n=2):
    try:
        import fitz
        doc = fitz.open(pdf_path)
        txt = "".join(doc[i].get_text() for i in range(min(n, doc.page_count)))
        doc.close()
        return txt
    except Exception:
        return ""

# ===== PDF 下载（三步链路 + 节流 + 配额 + 缓存去重）=====
_last_dl_ts = 0.0


def _throttle():
    global _last_dl_ts
    now = time.time()
    wait = DOWNLOAD_MIN_INTERVAL - (now - _last_dl_ts)
    if wait > 0:
        time.sleep(wait)
    _last_dl_ts = time.time()


def weipu_download(pid, lngid, year, title, save_dir, name_hint=None):
    """previewPath → fileBrowsing 三步链路下载。返回 (pdf_path|None, sha256|None, error|None)。"""
    cached = _cache_get_pdf(pid)
    if cached:
        return cached["path"], cached["sha256"], None
    if _quota_left() <= 0:
        return None, None, "日下载配额已用尽(CN_MED_OA_DAILY_MAX=%d)" % DAILY_MAX
    _throttle()
    st, j, raw = _jpost("/api/paperSearchApi/previewPath",
                        {"lngId": lngid, "paperYear": str(year), "weiPuPaperId": pid, "name": title})
    if not j or not j.get("success") or not j.get("entity"):
        return None, None, "previewPath失败: %s" % (raw or "")[:120]
    url = WEIPU_BASE + "/api/attachmentApi/fileBrowsing?hash=" + urllib.parse.quote(j["entity"])
    st, raw = _get_bytes(url)
    if not isinstance(raw, bytes) or raw[:4] != b"%PDF":
        return None, None, "fileBrowsing非PDF: head=%r" % (raw[:16] if isinstance(raw, bytes) else raw)
    os.makedirs(save_dir, exist_ok=True)
    safe = re.sub(r'[\\/:*?"<>|\s]+', "_", name_hint or title or pid)[:80].strip("_")
    path = os.path.join(save_dir, "%s_%s.pdf" % (safe, pid))
    with open(path, "wb") as f:
        f.write(raw)
    sha = hashlib.sha256(raw).hexdigest()
    _quota_consume()
    _cache_set_pdf(pid, path, sha)
    return path, sha, None

# ===== Vancouver 组装 =====
def _names(info):
    return [x.get("name", "") for x in (info or []) if isinstance(x, dict) and x.get("name")]


def to_vancouver(det, row, pdf_text=""):
    det = det or {}
    obj = det.get("objectInfo") or {}
    van = {
        "title": det.get("title") or row.get("title") or row.get("name", ""),
        "authors": _names(det.get("authorInfo")) or _names(row.get("authorInfo")),
        "journal": obj.get("name", "") if isinstance(obj, dict) else "",
        "year": str(det.get("year") or row.get("year") or ""),
        "doi": det.get("doi") or row.get("doi") or "",
        "abstract": det.get("abstr") or row.get("abstr") or "",
        "keywords": _names(det.get("keywordInfo")),
        "fund": [x.get("name", "") for x in (det.get("fundInfo") or []) if isinstance(x, dict)],
        "classno": ((det.get("classInfo") or {}).get("clc") or {}).get("codes", []),
        "isOa": det.get("isOa") if det.get("isOa") is not None else row.get("cqvipIsOa"),
        "isPdf": det.get("isPdf", row.get("isPdf")),
        "id": str(det.get("id") or row.get("id") or row.get("lngid") or ""),
        "lngid": str(det.get("lngid") or row.get("lngid") or ""),
    }
    van["journal_rank"] = rank_journal(van.get("journal") or "")
    vi = extract_vol_issue(det, pdf_text)
    van.update(vi)
    if isinstance(obj, dict):
        van["issn"] = obj.get("issn", "")
        van["cnno"] = obj.get("cnno", "")
        van["publisher"] = obj.get("publisher", "")
        van["journal_en"] = ""
        for alt in (obj.get("nameAlt") or []):
            if isinstance(alt, dict) and alt.get("_v"):
                van["journal_en"] = " ".join(alt["_v"]) if isinstance(alt["_v"], list) else str(alt["_v"])
                break
    # 知网落地页指引（providerSource 里的 CNKI uri，仅作指引不抓取）
    for p in (det.get("providerSource") or []):
        uri = ((p.get("_v") or {}).get("uri") or "")
        if "cnki.net" in uri:
            van["cnki_uri"] = uri
            break
    return van

# ===== 主入口 =====
def fetch_cn_oa(query=None, field="title", max_results=5, save_dir=None, want_pdf=True,
                min_relevance="low", sources=("WeipuOA", "Yiigle"),
                year_from=None, year_to=None, doc_type=None):
    """检索 + 下载。返回 {query, field, attempts, final_status, files, disclosure, stats}。

    final_status:
      full            有相关(ok)结果且至少下载 1 篇
      metadata_only   有相关结果，未下载/无PDF
      low_relevance   有结果但全部相关性不足(被守门标记)
      not_found       检索无结果
    min_relevance: "ok" 只保留相关 / "low" 保留 low 及以上 / "irrelevant" 全保留
    sources: 数据源优先级，默认先维普OA（期刊文献）再 Yiigle（CMA指南/核心刊），
             前一源无结果时自动降级下一源；两源结果按相关性合并去重。
    """
    result = {"query": query, "field": field, "attempts": [], "final_status": "not_found",
              "files": [], "disclosure": "", "stats": {}}
    if not query:
        result["disclosure"] = "❌ 未提供检索词"
        return result

    # 指南/共识类查询：yiigle（CMA 官方刊 + 指南专区）是权威源，优先于维普OA
    if sources == ("WeipuOA", "Yiigle") and any(k in query for k in ("指南", "共识", "规范", "专家建议")):
        sources = ("Yiigle", "WeipuOA")

    all_rows = []
    for src in sources:
        if src == "WeipuOA":
            rows, err = weipu_search(query, field=field, size=max_results + 3)
        elif src == "Yiigle":
            rows, err = yiigle_search(query, field=field, size=max_results + 3)
        else:
            continue
        result["attempts"].append({"source": src, "op": "search", "count": len(rows), "error": err})
        if rows:
            all_rows.extend(rows)
            break  # 前一源命中即停（优先级设计）

    if not all_rows:
        errs = "; ".join(a.get("error") or "" for a in result["attempts"] if a.get("error"))
        result["disclosure"] = "❌ 检索无结果" + (("：" + errs) if errs else "")
        return result

    # 按源做相关性守门（字段结构一致，relevance_gate 兼容）
    state_order = {"ok": 0, "low": 1, "irrelevant": 2}
    scored = []
    n_irrel = 0
    seen_dedup = set()

    def _dedup_key(row):
        doi = (row.get("artDoi") or row.get("doi") or "").strip().lower()
        if doi:
            return "doi:" + doi
        t = zh_clean(row.get("title") or "")
        return "title:" + t[:40]

    for idx, r in enumerate(all_rows):
        year = str(r.get("year") or "")
        if year_from and year and (not year.isdigit() or int(year) < year_from):
            continue
        if year_to and year and (not year.isdigit() or int(year) > year_to):
            continue
        if doc_type and doc_type not in (r.get("docType") or ""):
            continue
        k = _dedup_key(r)
        if k in seen_dedup:
            continue
        seen_dedup.add(k)
        rel = relevance_gate(query, r, field)
        if state_order[rel["state"]] > state_order[min_relevance]:
            n_irrel += 1
            continue
        scored.append((state_order[rel["state"]], idx, r, rel))
    scored.sort(key=lambda x: (x[0], x[1]))
    kept = [(r, rel) for _, _, r, rel in scored[:max_results]]
    result["stats"] = {"returned": len(all_rows), "kept": len(kept),
                       "filtered": n_irrel, "deduped": len(seen_dedup)}

    if not kept:
        result["final_status"] = "low_relevance"
        result["disclosure"] = ("⚠️ 检索返回 %d 条但相关性均不足（或被年份/类型筛选过滤）。"
                                "建议改用规范医学单短语，或换字段 subject/keyword 重试。" % len(all_rows))
        return result

    got_full = got_meta = n_ok = 0
    for r, rel in kept:
        if r.get("source") == "Yiigle":
            entry = yiigle_to_entry(r, rel, save_dir=save_dir, want_pdf=want_pdf)
            entry["source"] = "Yiigle"
            if rel["state"] == "ok":
                n_ok += 1
            if entry.get("path"):
                got_full += 1  # OA 商品匿名直下成功
            else:
                got_meta += 1  # 无 PDF（真登录墙/非OA），记 download_url 走浏览器兜底
            result["files"].append(entry)
            continue
        pid = str(r.get("id") or r.get("lngid") or "")
        if not pid:
            continue
        det = None
        try:
            det = weipu_detail(pid)
        except Exception as e:
            result["attempts"].append({"source": "WeipuOA", "op": "detail", "id": pid, "error": str(e)})
        if rel["state"] == "ok":
            n_ok += 1
        entry = to_vancouver(det, r)
        entry["relevance"] = rel
        entry["source"] = "WeipuOA"
        entry["license"] = "OA"
        if want_pdf and save_dir and entry.get("isPdf") in (1, "1", True):
            path, sha, derr = weipu_download(pid, entry["lngid"] or pid,
                                             entry["year"] or str(r.get("year") or ""),
                                             entry["title"], save_dir, entry["title"])
            if path:
                entry["path"] = path
                entry["sha256"] = sha
                ptxt = pdf_first_pages_text(path)
                vi = extract_vol_issue(det, ptxt)
                entry.update({k: vi[k] for k in ("volume", "issue", "vol_source", "vol_consistent", "needs_human_check")})
                pages, psrc = extract_pages(path)
                entry["pages"], entry["pages_source"] = pages, psrc
                got_full += 1
            else:
                entry["download_error"] = derr
                got_meta += 1
        else:
            got_meta += 1
        result["files"].append(entry)

    if n_ok == 0:
        result["final_status"] = "low_relevance"
    elif got_full:
        result["final_status"] = "full"
    else:
        result["final_status"] = "metadata_only"

    ok_n = sum(1 for e in result["files"] if e["relevance"]["state"] == "ok")
    parts = []
    srcs = sorted(set(e["source"] for e in result["files"]))
    if got_full:
        parts.append("✅ 下载 %d 篇全文" % got_full)
    if got_meta:
        parts.append("%d 篇仅元数据" % got_meta)
    if ok_n < len(result["files"]):
        parts.append("⚠️ %d 条相关性存疑(已标记)" % (len(result["files"]) - ok_n))
    result["disclosure"] = ("来源 %s：" % "+".join(srcs)) + "，".join(parts)
    return result


def health_check():
    """探测两个数据源可用性。返回 {source: {"ok": bool, "detail": str}}。"""
    out = {}
    try:
        rows, err = weipu_search("痛风", field="title", size=1)
        out["WeipuOA"] = {"ok": bool(rows), "detail": ("search ok" if rows else (err or "no result"))}
    except Exception as e:
        out["WeipuOA"] = {"ok": False, "detail": str(e)[:120]}
    try:
        rows, err = yiigle_search("痛风", field="title", size=1)
        out["Yiigle"] = {"ok": bool(rows), "detail": ("search ok" if rows else (err or "no result"))}
    except Exception as e:
        out["Yiigle"] = {"ok": False, "detail": str(e)[:120]}
    return out


def save_manifest(result, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, "cn_refs.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return path


def _ris_clean(v):
    """RIS 字段防御性清洗：去除换行/回车，防止注入伪造字段行。"""
    return str(v).replace("\r", " ").replace("\n", " ").strip()


def _ris_pages(entry):
    """RIS SP/EP 拆分：'1059-1077' → ('1059','1077')；'1059' → ('1059','')。"""
    p = (entry.get("pages") or "").strip()
    if not p:
        return "", ""
    if "-" in p:
        a, _, b = p.partition("-")
        return a.strip(), b.strip()
    return p, ""


def export_ris(result, save_dir):
    """manifest → RIS 文件（EndNote/NoteExpress/Zotero 可直接导入）。

    返回 (路径, 条数)。
    """
    lines = []
    n = 0
    for e in result["files"]:
        n += 1
        lines += ["TY  - JOUR", "TI  - " + _ris_clean(e.get("title") or "")]
        for au in e.get("authors") or []:
            lines.append("AU  - " + _ris_clean(au))
        lines.append("PY  - " + str(e.get("year") or ""))
        if e.get("journal"):
            lines.append("JO  - " + _ris_clean(e["journal"]))
        if e.get("volume"):
            lines.append("VL  - " + str(e["volume"]))
        if e.get("issue"):
            lines.append("IS  - " + str(e["issue"]))
        sp, ep = _ris_pages(e)
        if sp:
            lines.append("SP  - " + sp)
        if ep:
            lines.append("EP  - " + ep)
        if e.get("doi"):
            lines.append("DO  - " + e["doi"])
        if e.get("download_url"):
            lines.append("UR  - " + e["download_url"])
        elif e.get("path"):
            lines.append("L1  - " + e["path"])
        lines.append("ER  - ")
        lines.append("")
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, "cn_refs.ris")
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    return path, n


def citation(entry):
    """拼 GB/T 7714 风格引用行（页码缺失时留待核对）。"""
    aus = "、".join(entry.get("authors", [])[:3]) + ("等" if len(entry.get("authors", [])) > 3 else "")
    vi = "%s(%s)" % (entry.get("volume"), entry.get("issue")) if entry.get("volume") else ""
    seg = "%s. %s[%s]. %s, %s" % (
        aus or "佚名", entry.get("title", ""), "J", entry.get("journal", ""), entry.get("year", ""))
    if vi:
        seg += ", " + vi
    if entry.get("pages"):
        seg += ": " + entry["pages"]
    elif vi:
        seg += ": [页码待核对]"
    if entry.get("doi"):
        seg += ". DOI: " + entry["doi"]
    return seg + "."


def write_pending_downloads(result, save_dir):
    """把未能自动下载的条目写成人工下载清单（markdown）。"""
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, "pending_downloads.md")
    lines = ["# 待人工下载清单（浏览器打开链接下载 PDF 后放入本目录，再跑 --complete-downloads 入库）", ""]
    n = 0
    for e in result["files"]:
        if not e.get("path") and e.get("download_url"):
            n += 1
            lines.append(f"{n}. **{e['title']}**")
            lines.append(f"   - 链接: {e['download_url']}")
            lines.append(f"   - 期刊: {e.get('journal','')} {e.get('year','')};{e.get('volume','')}({e.get('issue','')})")
            # 建议文件名必须含标题：complete_downloads 按文件名与标题做模糊匹配，
            # 序号类文件名（如 yiigle_Yiigle_1）ratio≈0 永远匹配不上
            safe_title = re.sub(r'[\\/:*?"<>|·\s]+', "_", e["title"])[:80].strip("_") or f"yiigle_{e.get('source','')}_{n}"
            lines.append(f"   - 建议文件名: {safe_title}.pdf")
            lines.append("")
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    return path, n


def complete_downloads(save_dir):
    """扫描目录中用户手动下载的 PDF，按标题模糊匹配 manifest 并补 sha256/path。

    返回 (matched, unmatched_count)。
    """
    mf = os.path.join(save_dir, "cn_refs.json")
    if not os.path.exists(mf):
        return [], 0
    result = json.load(open(mf, encoding="utf-8"))
    import difflib
    matched = []
    pdfs = [f for f in os.listdir(save_dir) if f.lower().endswith(".pdf")]
    for e in result.get("files", []):
        if e.get("path"):
            continue
        et = zh_clean(e["title"])
        best, best_r = None, 0.0
        for f in pdfs:
            ft = zh_clean(f.replace(".pdf", "").replace("yiigle", "").replace("_", " "))
            r = difflib.SequenceMatcher(None, et[:40], ft[:40]).ratio()
            if r > best_r:
                best, best_r = f, r
        if best and best_r >= 0.45:
            p = os.path.join(save_dir, best)
            data = open(p, "rb").read()
            e["path"] = p
            e["sha256"] = hashlib.sha256(data).hexdigest()
            e["download_source"] = "manual"
            matched.append((best, e["title"][:40]))
            pdfs.remove(best)
    json.dump(result, open(mf, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return matched, len(pdfs)


def run_batch(batch_file, field, max_results, save_dir, want_pdf, min_relevance,
              sources, year_from=None, year_to=None, doc_type=None):
    """批量模式：每行一个检索词，逐条 fetch_cn_oa 并汇总。

    行格式：纯标题行；支持 # 开头的注释行与空行。返回 (汇总结果, 报告行列表)。
    汇总结果与单条 fetch_cn_oa 同构（files 合并、stats 累计），可直接 save_manifest/export_ris。
    """
    lines = []
    if not os.path.isfile(batch_file):
        print(f"❌ 批处理文件不存在: {batch_file}", file=sys.stderr)
        sys.exit(2)
    with open(batch_file, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    if not lines:
        print("❌ 批处理文件无有效检索词（每行一个，支持 # 注释）", file=sys.stderr)
        sys.exit(2)
    combined = {"query": f"batch:{batch_file}", "field": field, "attempts": [],
                "final_status": "metadata_only", "files": [], "disclosure": "", "stats": {},
                "batch": {"total": len(lines), "full": 0, "metadata_only": 0,
                          "low_relevance": 0, "not_found": 0}}
    report = [f"批量检索 {len(lines)} 条:"]
    for i, q in enumerate(lines, 1):
        r = fetch_cn_oa(q, field, max_results, save_dir, want_pdf, min_relevance,
                        sources=sources, year_from=year_from, year_to=year_to, doc_type=doc_type)
        st = r["final_status"]
        combined["batch"][st if st in combined["batch"] else "not_found"] += 1
        combined["attempts"] += r["attempts"]
        combined["files"] += r["files"]
        n = len(r["files"])
        report.append(f"  {i}/{len(lines)} [{st}] {q[:38]} → {n} 条")
        if r.get("disclosure") and not r["files"]:
            report.append("      " + r["disclosure"])
        _throttle()  # 批量模式每条检索后固定控频，无论是否下载（合规铁律）
    combined["stats"] = {"returned": len(combined["files"]),
                         "kept": len(combined["files"]), "batches": len(lines)}
    return combined, report


def main():
    ap = argparse.ArgumentParser(description="中文医学文献OA聚合下载器(维普OA+yiigle双源) v" + SKILL_VER)
    ap.add_argument("--query", default=None, help="检索词(建议规范医学单短语)")
    ap.add_argument("--batch", default=None, help="批量模式: 每行一个检索词的清单文件(支持#注释行)")
    ap.add_argument("--field", default="title", choices=list(WEIPU_FIELDS.keys()), help="检索字段")
    ap.add_argument("--max", type=int, default=5, help="最大结果数")
    ap.add_argument("--out-dir", default=None, help="下载目录(不填则只检索元数据)")
    ap.add_argument("--no-pdf", action="store_true", help="仅元数据,不下载PDF")
    ap.add_argument("--min-relevance", default="low", choices=["ok", "low", "irrelevant"],
                    help="相关性过滤阈值: ok=只留相关 low=保留存疑 irrelevant=全保留")
    ap.add_argument("--citation", action="store_true", help="输出 GB/T 7714 引用行")
    ap.add_argument("--year-from", type=int, default=None, help="发表年份下限(含)")
    ap.add_argument("--year-to", type=int, default=None, help="发表年份上限(含)")
    ap.add_argument("--doc-type", default=None, help="文献类型筛选(如 指南/共识/综述/论著)")
    ap.add_argument("--sources", default="WeipuOA,Yiigle", help="数据源及优先级,逗号分隔(默认维普优先;指南类自动反转)")
    ap.add_argument("--health", action="store_true", help="仅探测数据源可用性后退出")
    ap.add_argument("--pending-downloads", action="store_true", help="对未能自动下载的条目生成人工下载清单 pending_downloads.md")
    ap.add_argument("--complete-downloads", action="store_true", help="扫描 out-dir 中手动下载的 PDF，匹配 manifest 入库")
    ap.add_argument("--export-ris", action="store_true", help="将结果导出为 RIS 文件（EndNote/NoteExpress/Zotero 可导入）")
    ap.add_argument("--suggest-terms", default=None, metavar="QUERY",
                    help="检索词助手：口语→规范术语建议+拆词建议（纯本地，不发网络请求）")
    args = ap.parse_args()

    if args.suggest_terms is not None:
        for line in suggest_terms(args.suggest_terms):
            print(line)
        sys.exit(0)

    if args.health:
        for src, st in health_check().items():
            print(("✅" if st["ok"] else "❌") + " " + src + ": " + st["detail"])
        sys.exit(0)

    if args.batch:
        if args.query:
            print("❌ --query 与 --batch 互斥，只能二选一", file=sys.stderr)
            sys.exit(2)
        if args.complete_downloads:
            print("❌ --complete-downloads 是独立模式，不能与 --batch 组合", file=sys.stderr)
            sys.exit(2)
        if (args.export_ris or args.pending_downloads) and not args.out_dir:
            print("❌ --export-ris/--pending-downloads 需配合 --out-dir", file=sys.stderr)
            sys.exit(2)
        srcs = tuple(s.strip() for s in args.sources.split(",") if s.strip()) or ("WeipuOA", "Yiigle")
        r, report = run_batch(args.batch, args.field, args.max, args.out_dir, not args.no_pdf,
                              args.min_relevance, srcs, args.year_from, args.year_to, args.doc_type)
        for line in report:
            print(line)
        b = r["batch"]
        print(f"汇总: {b['total']} 条检索 | 命中 {len(r['files'])} 条 | "
              f"full={b['full']} metadata={b['metadata_only']} low={b['low_relevance']} not_found={b['not_found']}")
        if args.out_dir:
            save_manifest(r, args.out_dir)
            if args.export_ris:
                path, n = export_ris(r, args.out_dir)
                print(f"📄 RIS 已导出: {path}（{n} 条）")
            if args.pending_downloads:
                path, n = write_pending_downloads(r, args.out_dir)
                print(f"📝 人工下载清单: {path}（{n} 条）")
        sys.exit(0)

    if not args.query:
        print("❌ 需提供 --query 或 --batch", file=sys.stderr)
        sys.exit(2)

    if args.complete_downloads:
        if not args.out_dir:
            print("❌ --complete-downloads 需配合 --out-dir", file=sys.stderr)
            sys.exit(2)
        matched, left = complete_downloads(args.out_dir)
        for f, t in matched:
            print(f"  ✅ 入库 {f} ← {t}")
        print(f"匹配 {len(matched)} 个，剩余未匹配 PDF {left} 个")
        sys.exit(0)

    srcs = tuple(s.strip() for s in args.sources.split(",") if s.strip()) or ("WeipuOA", "Yiigle")
    r = fetch_cn_oa(args.query, args.field, args.max, args.out_dir, not args.no_pdf, args.min_relevance,
                    sources=srcs, year_from=args.year_from, year_to=args.year_to, doc_type=args.doc_type)
    if args.out_dir:
        save_manifest(r, args.out_dir)
    print(r["disclosure"])
    for e in r["files"]:
        rel = e["relevance"]
        tag = {"ok": "", "low": "[相关性存疑]", "irrelevant": "[不相关]"}[rel["state"]]
        rank = ("⭐" + e["journal_rank"]) if e.get("journal_rank") else ""
        pdf = ("PDF:" + os.path.basename(e["path"])) if e.get("path") else (
            ("浏览器下载:" + e["download_url"][:50]) if e.get("download_url") else e.get("download_error", "仅元数据"))
        print("  %s %s | %s %s %s;%s(%s) p=%s | doi=%s | %s" %
              (tag, e["title"][:40], rank, e["journal"], e["year"], e["volume"], e["issue"],
               e.get("pages") or "-", e["doi"][:32], pdf))
        if args.citation:
            print("      引用: " + citation(e))
    if not r["files"]:
        print()
        print("💡 没有可输出结果——常见原因与对策：")
        print('  ① 检索词偏口语或偏僻 → python scripts/cn_med_oa.py --suggest-terms "%s"' % args.query)
        print("  ② 多个词互相污染（平台是 OR 匹配）→ 拆成单短语分别检索")
        print("  ③ 中华系核心刊多数不在 OA 库（指南类例外）→ 见 SKILL.md「能下什么/不能下什么」")
        print("  ④ 平台偶发超时 → 稍后重试，或加 --timeout 30")
    if args.pending_downloads and args.out_dir:
        path, n = write_pending_downloads(r, args.out_dir)
        print(f"📝 人工下载清单: {path}（{n} 条）")
    if args.export_ris:
        if not args.out_dir:
            print("❌ --export-ris 需配合 --out-dir", file=sys.stderr)
            sys.exit(2)
        path, n = export_ris(r, args.out_dir)
        print(f"📄 RIS 已导出: {path}（{n} 条，EndNote/NoteExpress/Zotero 可直接导入）")
    att_txt = json.dumps(r.get("attempts") or [], ensure_ascii=False)
    if r["final_status"] not in ("full", "metadata_only") and ("retry_exhausted" in att_txt or "timed out" in att_txt.lower()):
        print()
        print(humanize_neterr(att_txt))
    sys.exit(0 if r["final_status"] in ("full", "metadata_only") else 1)


if __name__ == "__main__":
    main()
