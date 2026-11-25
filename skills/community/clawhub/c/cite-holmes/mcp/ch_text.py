"""cite-holmes v6.0.0 模块层：ch_text（由手术脚本从单文件引擎分层，
判定语义与 API 见壳 verify_refs.py 与 ADR-0010）。一切跨层符号与被
测试 patch 的函数一律经 _ROOT（由壳注入主壳命名空间）——patch 语义
与 trunk/mcp 双壳隔离（目录前缀加载）共同由该机制保证。"""

import argparse
import csv
import difflib
import hashlib
import ipaddress
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import escape as html_escape
from urllib.parse import urlparse, urlunparse, quote

_ROOT = None  # 由 verify_refs 壳注入


def _bind(root):
    global _ROOT
    _ROOT = root


VERSION = "6.9.0"


# ---------------- 可选配置（v1.9，main() 按命令行/环境覆写） ----------------
# OpenAlex 2026-02 起生产调用需 API key（每日免费额度）；Semantic Scholar 免钥
# 走共享限速池，带 key 独享 1 req/s。mailto 用于 Crossref polite pool（限速更宽松）。
def md_cell(text, limit=90):
    """Markdown 表格单元格转义：竖线转义、换行剥除、截断。"""
    t = str(text if text is not None else "")
    t = t.replace("\r", " ").replace("\n", " ").replace("|", "\\|")
    return t[:limit]


def csv_safe(cell: str) -> str:
    """CSV 公式注入中和（OWASP 做法）：= + - @ 制表符 回车 开头的单元格前置单引号。"""
    c = str(cell)
    if c[:1] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + c
    return c


def bib_safe(value: str) -> str:
    """BibTeX 字段值加固：剥除花括号与换行/控制字符，防 @entry 逃逸。"""
    v = str(value if value is not None else "")
    return v.replace("{", "").replace("}", "").replace("\r", " ").replace("\n", " ")


# ---------------- CiteScore 置信度评分（v1.3.0） ----------------
# 五态加权：verified +10 / partial +4 / unreachable 0 / unverified -2 / invalid -8
# 归一化到 0-100，等级 A(>=85) B(70-84) C(50-69) D(<50)
def _norm_name(s) -> str:
    """人名/期刊名规范化：小写、只留字母数字与 CJK。"""
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", str(s or "").lower())


def _claimed_surnames(authors: str) -> list:
    """从 "Smith J, Zhang W, 王五" 形式的作者串提取姓氏 token（每段第一个词）。"""
    out = []
    for part in re.split(r"[,，;；、]", str(authors or "")):
        toks = part.strip().split()
        if toks:
            out.append(toks[0])
    return out


def _author_consistent(claimed: list, csl_authors) -> bool:
    """声称姓氏与 CSL 登记作者列表比对：任一命中即一致（拼写/变体从宽）。
    v1.7 二轮评审修正：①跨语言不可比（中文译名 vs 拼音登记）跳过判定——
    与期刊核查同款守卫；②单字母 initial 不参与子串匹配（防 "L."/"G." 命中
    无关长名，使检查对 APA 格式与长作者列表失效）；③规范化后为空的声称
    token 跳过。登记列表缺失或无声称作者 → 跳过判定。"""
    reg = []
    for a in csl_authors or []:
        if not isinstance(a, dict):
            continue
        for k in ("family", "given", "name"):
            v = _norm_name(a.get(k))
            if v:
                reg.append(v)
    claimed_n = [c for c in (_norm_name(x) for x in claimed) if c]
    if not reg or not claimed_n:
        return True

    # v3.15 跨族守卫：声称与登记主导文字系统不同（任意族组合）→ 跳过判定
    sf_c = _script_family(claimed_n[0])
    if sf_c != "none" and all(_script_family(r) != sf_c for r in reg):
        return True
    for c in claimed_n:
        for r in reg:
            if c == r:
                return True
            if len(c) >= 2 and len(r) >= 2 and (c in r or r in c):
                return True
    return False


TIER_RULES = [
    (
        "official",
        [
            r"\.gov(\.[a-z]{2})?$",
            r"\.edu(\.[a-z]{2})?$",
            r"\.gov\.cn$",
            r"\.edu\.cn$",
            r"^docs\.",
            r"^developer\.",
            r"^documentation\.",
            r"^support\.",
            r"^www\.anthropic\.com$",
            r"^openai\.com$",
            r"^www\.nature\.com$",
            r"^www\.nejm\.org$",
            r"^www\.who\.int$",
            r"^www\.fda\.gov$",
            r"^www\.ema\.europa\.eu$",
            r"^arxiv\.org$",
            r"^export\.arxiv\.org$",
            r"^www\.thelancet\.com$",
            r"^jamanetwork\.com$",
            r"^pubmed\.ncbi\.nlm\.nih\.gov$",
            r"^doi\.org$",
            r"^www\.sciencedirect\.com$",
            r"^link\.springer\.com$",
            r"^ieeexplore\.ieee\.org$",
            r"^www\.stats\.gov\.cn$",
            r"^www\.nhc\.gov\.cn$",
        ],
    ),
    (
        "journal",
        [
            r"^pubmed\.ncbi\.nlm\.nih\.gov$",
            r"^doi\.org$",
            r"^journals?\.",
            r"^academic\.",
            r"^scholar\.",
            r"^kns\.",
            r"^oa\.cqvip\.com$",
            r"(^|\.)yiigle\.com$",
            # v4.2.0 中文医学注册库（dogfood 实测：万方题录 URL 被误层为 blog）
            r"(^|\.)wanfangdata\.com\.cn$",
            r"(^|\.)cnki\.(?:net|com\.cn)$",
        ],
    ),
    (
        "preprint",
        [r"^arxiv\.org$", r"^biorxiv\.org$", r"^medrxiv\.org$", r"^ssrn\.com$", r"^chemrxiv\.org$"],
    ),
    (
        "media",
        [
            r"^www\.reuters\.com$",
            r"^apnews\.com$",
            r"^www\.bbc\.",
            r"^www\.nytimes\.com$",
            r"^www\.bloomberg\.com$",
            r"^www\.ft\.com$",
            r"^www\.economist\.com$",
            r"^news\.yahoo\.com$",
            r"^www\.thepaper\.cn$",
            r"^www\.caixin\.com$",
            r"^www\.jiemian\.com$",
            r"^36kr\.com$",
            r"^www\.infoq\.cn$",
            r"^techcrunch\.com$",
            r"^www\.theverge\.com$",
            r"^arstechnica\.com$",
            r"^www\.wired\.com$",
        ],
    ),
    (
        "community",
        [
            r"^github\.com$",
            r"^stackoverflow\.com$",
            r"^en\.wikipedia\.org$",
            r"^zh\.wikipedia\.org$",
            r"^www\.zhihu\.com$",
            r"^zhuanlan\.zhihu\.com$",
            r"^stackexchange\.com$",
            r"^www\.reddit\.com$",
            r"^news\.ycombinator\.com$",
            r"^www\.v2ex\.com$",
            r"^segmentfault\.com$",
            r"^juejin\.cn$",
        ],
    ),
    (
        "social",
        [
            r"(^|\.)x\.com$",
            r"(^|\.)twitter\.com$",
            r"(^|\.)weibo\.com$",
            r"(^|\.)t\.me$",
            r"(^|\.)facebook\.com$",
            r"(^|\.)youtube\.com$",
            r"(^|\.)bilibili\.com$",
            r"(^|\.)douyin\.com$",
            r"(^|\.)xiaohongshu\.com$",
            r"(^|\.)medium\.com$",
        ],
    ),
]
TRUSTED_TIERS = {"official", "journal", "preprint", "media"}

# ---------------- 医学信源预设（--profile medical 时并入 journal 层） ----------------
MEDICAL_JOURNAL_PATTERNS = [
    r"\.cochranelibrary\.com$",
    r"^bestpractice\.bmj\.com$",
    r"^www\.bmj\.com$",
    r"^www\.embase\.com$",
    r"^clinicaltrials\.gov$",
    r"^www\.chinacdc\.cn$",
    r"^www\.cdc\.gov$",
    r"^www\.nmpa\.gov\.cn$",
    r"^www\.nice\.org\.uk$",
    r"\.wanfangdata\.com\.cn$",
    r"^guide\.medlive\.cn$",
    r"^rs\.yiigle\.com$",
    r"^(www\.)?chictr\.org\.cn$",
]

DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
PMID_RE = re.compile(r"^\d{6,9}$")
# arXiv ID：新式 YYMM.NNNNN——MM 限 01-12（月份段非法的伪 ID 会让官方 API 挂起，
# 必须在客户端拒掉）——可带 v2 版本号；旧式 类目/编号（hep-th/9901001、math.GT/0309136）
ARXIV_NEW_RE = re.compile(r"^\d{2}(?:0[1-9]|1[0-2])\.\d{4,5}(v\d+)?$", re.IGNORECASE)
ARXIV_OLD_RE = re.compile(r"^[a-z\-]+(?:\.[A-Z]{2})?/\d{7}(v\d+)?$", re.IGNORECASE)
ARXIV_URL_RE = re.compile(
    r"^https?://(?:www\.|export\.)?arxiv\.org/(?:abs|pdf|format)/"
    r"([a-z\-]+(?:\.[A-Z]{2})?/\d{7}|\d{2}(?:0[1-9]|1[0-2])\.\d{4,5})(v\d+)?",
    re.IGNORECASE,
)
REQUIRED_FIELDS = ("title", "url", "source", "year")


def extract_arxiv_id(ref: dict) -> str:
    """从引用中提取 arXiv ID（v1.5）：显式 arxiv 字段优先（支持 "arXiv:" 前缀），
    其次识别 url 中的 arxiv.org/abs|pdf/<id>。格式校验通过才返回，否则 ""。"""
    raw = str(ref.get("arxiv") or "").strip()
    if not raw:
        m = ARXIV_URL_RE.match(str(ref.get("url") or "").strip())
        if m:
            raw = m.group(1) + (m.group(2) or "")
    raw = re.sub(r"(?i)^arxiv\s*:\s*", "", raw).strip()
    if ARXIV_NEW_RE.match(raw) or ARXIV_OLD_RE.match(raw):
        return raw
    return ""


def classify_tier(url: str, medical: bool = False) -> str:
    host = (urlparse(url).hostname or "").lower()
    if not host:
        return "unknown"
    for tier, patterns in TIER_RULES:
        for pat in patterns:
            if re.search(pat, host):
                return tier
    if medical:
        for pat in MEDICAL_JOURNAL_PATTERNS:
            if re.search(pat, host):
                return "journal"
    return "blog"


def normalize_url(url: str) -> str:
    p = urlparse(url.strip())
    return urlunparse((p.scheme.lower(), (p.netloc or "").lower(), p.path.rstrip("/"), "", "", ""))


PUBMED_URL_RE = re.compile(r"^https?://pubmed\.ncbi\.nlm\.nih\.gov/(\d+)/?$")


def _cjk_norm(s: str) -> str:
    """v3.10 中英混排标题归一化：全角→半角、去空白与标点、小写，仅保留
    字母数字与 CJK 表意文字。跨语言桥接比对与克隆引用检测共用——中文文献
    引用中全角标点/空格变体极常见，不归一会把同一题名误判成两个。"""
    out = []
    for ch in str(s or "").lower():
        o = ord(ch)
        if 0xFF01 <= o <= 0xFF5E:  # 全角 ASCII 区 → 半角
            ch = chr(o - 0xFEE0)
        elif ch == "\u3000":  # 全角空格
            continue
        if ch.isalnum() or "\u4e00" <= ch <= "\u9fff":
            out.append(ch)
    return "".join(out)


def _script_family(s: str) -> str:
    """v3.15 文字系统族判定（跨语言守卫用）：返回文本的主导文字系统。
    latin / cyrillic / greek / han / kana / hangul / none。假名在场即判 kana
    （假名仅用于日文——中日汉字题名借此可分）。跨族题名的字符相似度天然
    不可信，这正是守卫要扩到「中英之外」的依据：俄文/希腊文/日文声称题名
    对英文登记名，旧守卫（只认 CJK）会漏判导致 sim 低被误判 invalid。"""
    from collections import Counter

    cnt = Counter()
    for ch in str(s or ""):
        o = ord(ch)
        if 0x0400 <= o <= 0x04FF:
            cnt["cyrillic"] += 1
        elif 0x0370 <= o <= 0x03FF or 0x1F00 <= o <= 0x1FFF:
            cnt["greek"] += 1
        elif 0x3040 <= o <= 0x30FF:
            cnt["kana"] += 1
        elif 0xAC00 <= o <= 0xD7AF or 0x1100 <= o <= 0x11FF:
            cnt["hangul"] += 1
        elif 0x4E00 <= o <= 0x9FFF or 0x3400 <= o <= 0x4DBF:
            cnt["han"] += 1
        elif ch.isalpha():
            cnt["latin"] += 1
    if not cnt:
        return "none"
    if cnt.get("kana"):
        return "kana"
    return cnt.most_common(1)[0][0]


def _title_sim(a: str, b: str) -> float:
    """题名比对双通道取 max：序列相似度（SequenceMatcher）+ 词集 Jaccard。
    后者对「登记版题名词序重排」鲁棒——ACR/EULAR 分类标准登记题名把年份
    提前（"2013 classification criteria...: an American College..."），
    声称题名（参考文献写法）与登记题名词序不同，纯序列比对给 <0.5 误判
    （实测 2026-10-14，PMID 24122180）。v4.3.0 起为模块级（OpenAlex 找锚
    通道复用同一比对口径，避免两套相似度漂移）。"""
    a_n, b_n = _cjk_norm(a).lower(), _cjk_norm(b).lower()
    seq = difflib.SequenceMatcher(None, a_n, b_n).ratio()
    # 词集用原始题名（保留空格）切词——_cjk_norm 输出是无空格连续串，
    # 在其上 findall 只会得到一个超长 token，Jaccard 退化为包含度（实测踩坑）
    ta = set(re.findall(r"[a-z0-9\u4e00-\u9fff]+", str(a).lower()))
    tb = set(re.findall(r"[a-z0-9\u4e00-\u9fff]+", str(b).lower()))
    jac = (len(ta & tb) / len(ta | tb)) if (ta or tb) else 0.0
    return max(seq, jac)


_CN_JOURNAL_TA = {
    "中华儿科杂志": "Zhonghua Er Ke Za Zhi",
    "中华医学杂志": "Zhonghua Yi Xue Za Zhi",
    "中华结核和呼吸杂志": "Zhonghua Jie He He Hu Xi Za Zhi",
    "中华心血管病杂志": "Zhonghua Xin Xue Guan Bing Za Zhi",
    "中华内科杂志": "Zhonghua Nei Ke Za Zhi",
    "中华外科杂志": "Zhonghua Wai Ke Za Zhi",
    "中华妇产科杂志": "Zhonghua Fu Chan Ke Za Zhi",
    "中华放射学杂志": "Zhonghua Fang She Xue Za Zhi",
    "中华血液学杂志": "Zhonghua Xue Ye Xue Za Zhi",
    "中华护理杂志": "Zhonghua Hu Li Za Zhi",
    "中华预防医学杂志": "Zhonghua Yu Fang Yi Xue Za Zhi",
    "中华流行病学杂志": "Zhonghua Liu Xing Bing Xue Za Zhi",
    "中华肿瘤杂志": "Zhonghua Zhong Liu Za Zhi",
    "中华耳鼻咽喉头颈外科杂志": "Zhonghua Er Bi Yan Hou Tou Jing Wai Ke Za Zhi",
    "中华眼科杂志": "Zhonghua Yan Ke Za Zhi",
    "中华口腔医学杂志": "Zhonghua Kou Qiang Yi Xue Za Zhi",
    "中华病理学杂志": "Zhonghua Bing Li Xue Za Zhi",
}


def _ta_for_journal(source: str) -> str:
    """中文刊名 → NLM TA；否则原样返回（英文引用的著录缩写通常即 TA）。"""
    s = re.sub(r"[\s《》*]+", "", str(source or ""))
    return _CN_JOURNAL_TA.get(s) or str(source or "").strip()


_JOURNAL_ACRO = {
    # 不透明缩写(不可按词首拆分匹配的 NLM 缩写)→全称;小写无句点
    "jama": "journal of the american medical association",
    "pnas": "proceedings of the national academy of sciences",
    "bmj": "british medical journal",
    "jco": "journal of clinical oncology",
    "jnci": "journal of the national cancer institute",
    "ajr": "american journal of roentgenology",
    "jid": "journal of investigative dermatology",
    "jacc": "journal of the american college of cardiology",
}


def _journal_tokens(s: str) -> list:
    return re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]", str(s).lower())


def _journal_acro_expand(name: str) -> str:
    """不透明缩写展开(双向);其余原样返回。"""
    k = re.sub(r"[^a-z0-9 ]", "", str(name).lower()).strip()
    if k in _JOURNAL_ACRO:
        return _JOURNAL_ACRO[k]
    return str(name)


def _journal_consistent(claimed: str, registry: str) -> bool:
    """期刊名一致性(宽容口径,与 v1.6 DOI 路径同哲学):
    ①规范化后互含→一致 ②NLM 式缩写:短名各词按序匹配长名词首(可跳虚词)
    →一致 ③不透明缩写(JAMA/PNAS 等)经 _JOURNAL_ACRO 展开后再比 ④跨语言跳过。"""
    c = str(claimed or "").strip().lower()
    r = str(registry or "").strip().lower()
    if not c or not r:
        return True
    cn, rn = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", c), re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", r)
    if not cn or not rn:
        return True  # 跨语言不可比,跳过
    if bool(re.search(r"[\u4e00-\u9fff]", c)) != bool(re.search(r"[\u4e00-\u9fff]", r)):
        return True  # 拉丁 vs CJK:字系不同不可比,跳过(v1.6 同语义)
    if cn in rn or rn in cn:
        return True
    for a, b in ((c, r), (r, c)):
        ea, eb = _journal_acro_expand(a), _journal_acro_expand(b)
        if ea != a or eb != b:
            an, bn = re.sub(r"[^a-z0-9]+", "", ea), re.sub(r"[^a-z0-9]+", "", eb)
            if an in bn or bn in an:
                return True
            ta, tb = _journal_tokens(ea), _journal_tokens(eb)
            short, long_ = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
            stop = {"of", "the", "and", "in", "for", "on"}
            long_content = [w for w in long_ if w not in stop]
            j, hit = 0, 0
            ok = True
            for st in short:
                if st in stop:
                    continue
                while j < len(long_content) and not long_content[j].startswith(st):
                    j += 1
                if j >= len(long_content):
                    ok = False
                    break
                hit += 1
                j += 1
            if ok and hit >= max(1, len([w for w in short if w not in stop])):
                return True
    ct, rt = _journal_tokens(c), _journal_tokens(r)
    short, long_ = (ct, rt) if len(ct) <= len(rt) else (rt, ct)
    stop = {"of", "the", "and", "in", "for", "on"}
    long_content = [w for w in long_ if w not in stop]
    j, hit, ok = 0, 0, True
    for st in short:
        if st in stop:
            continue
        while j < len(long_content) and not long_content[j].startswith(st):
            j += 1
        if j >= len(long_content):
            ok = False
            break
        hit += 1
        j += 1
    return bool(ok and hit >= max(1, len([w for w in short if w not in stop])))


FIELD_ZH = {
    "title": "标题(title)",
    "url": "链接(url)",
    "source": "来源(source)",
    "year": "年份(year)",
}


def missing_fields(ref: dict) -> list:
    miss = [f for f in REQUIRED_FIELDS if not ref.get(f)]
    if "url" in miss and (
        (ref.get("doi") and DOI_RE.match(str(ref["doi"]).strip()))
        or (ref.get("pmid") and PMID_RE.match(str(ref["pmid"]).strip()))
        or extract_arxiv_id(ref)
    ):
        miss.remove("url")
    return [FIELD_ZH.get(f, f) for f in miss]


def ref_to_url(ref: dict) -> str:
    """url → doi → arxiv → pmid 四级解析，返回最终可检查的 URL。字段统一强转为字符串。"""
    url = str(ref.get("url") or "").strip()
    if url:
        return url
    doi = str(ref.get("doi") or "").strip()
    if doi and DOI_RE.match(doi):
        return f"https://doi.org/{doi}"
    arxiv = extract_arxiv_id(ref)
    if arxiv:
        return f"https://arxiv.org/abs/{arxiv}"
    pmid = str(ref.get("pmid") or "").strip()
    if pmid and PMID_RE.match(pmid):
        return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
    return ""


# ---------------- BibTeX 导入（v1.9，对标 Zotero/EndNote 工作流） ----------------


def _bib_unbrace(value: str) -> str:
    """BibTeX 字段值清理：还原常见 TeX 转义（\\& → & 等）、去花括号与转义残留、
    压缩空白。刻意不做重音展开（Schr\\"oder 类）——标题比对走模糊相似度，无需精确。"""
    v = re.sub(r"\\([{}&%$#_])", r"\1", str(value or ""))
    v = v.replace("{", "").replace("}", "").replace("\\", "")
    return re.sub(r"\s+", " ", v).strip()


def _bib_entry_to_ref(etype: str, f: dict) -> dict:
    """BibTeX 字段 → 引用 schema。source 依次取 journal/booktitle/journaltitle/
    publisher；howpublished 含 \\url 宏时只取链接不进 source（避免垃圾来源名）。"""

    def g(k):
        return _bib_unbrace(f.get(k, ""))

    url = g("url")
    if not url:
        for k in ("url", "howpublished", "note"):
            m = re.search(r"\\url\{([^}]+)\}", str(f.get(k) or ""))
            if m:
                url = m.group(1).strip()
                break
    src = g("journal") or g("booktitle") or g("journaltitle") or g("publisher")
    if not src:
        hp = str(f.get("howpublished") or "")
        if hp and "\\url" not in hp:
            src = _bib_unbrace(hp)
    ref = {
        "title": g("title"),
        # BibTeX 多作者分隔符 " and " 归一为逗号——姓氏提取按逗号分段
        "authors": g("author").replace(" and ", ", "),
        "source": src,
        "year": re.sub(r"[^0-9]", "", g("year"))[:4] or None,
        "doi": g("doi"),
        "url": url,
        "pmid": re.sub(r"[^0-9]", "", g("pmid")),
    }
    eprint = g("eprint")
    if eprint and g("archiveprefix").lower() in ("arxiv", ""):
        ref["arxiv"] = eprint
    return {k: v for k, v in ref.items() if v not in ("", None)} or {"title": ""}


def parse_bibtex(text: str) -> list:
    """v1.9 最小 BibTeX 解析器（纯 stdlib）：支持 @article/@inproceedings/@book/
    @misc 等常规条目、嵌套花括号值、引号值与多行字段。@comment/@preamble/@string
    跳过。解析不抛异常——坏条目降级为缺字段引用，由后续检查如实标注；
    完全无法解析时返回空列表（调用方给可操作报错）。"""
    refs = []
    i, n = 0, len(text)
    while i < n:
        if text[i] != "@":
            i += 1
            continue
        m = re.match(r"@([A-Za-z]+)\s*([{(])\s*([^,\s]*)\s*,", text[i:])
        if not m:
            i += 1
            continue
        etype = m.group(1).lower()
        close_ch = "}" if m.group(2) == "{" else ")"
        i += m.end()
        if etype in ("comment", "preamble", "string"):
            continue
        fields = {}
        depth = 1
        while i < n and depth > 0:
            ch = text[i]
            if ch == close_ch:
                depth -= 1
                i += 1
                if depth == 0:
                    break
                continue
            fm = re.match(r"\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*", text[i:])
            if not fm:
                i += 1 if ch not in ", \t\r\n" else re.match(r"[, \t\r\n]+", text[i:]).end()
                continue
            i += fm.end()
            if i < n and text[i] == "{":  # 花括号值：计数嵌套
                k, d = i + 1, 1
                while k < n and d > 0:
                    if text[k] == "{":
                        d += 1
                    elif text[k] == "}":
                        d -= 1
                    k += 1
                raw = text[i + 1 : k - 1]
                i = k
            elif i < n and text[i] == '"':  # 引号值（内部可含花括号）
                k = text.find('"', i + 1)
                k = n if k < 0 else k
                raw = text[i + 1 : k]
                i = k + 1
            else:  # 裸值（数字/缩写）
                k = i
                while k < n and text[k] not in ",}\n)":
                    k += 1
                raw = text[i:k].strip()
                i = k
            fields[fm.group(1).lower()] = raw
            while i < n and text[i] in ", \t\r\n":
                i += 1
        if fields:
            refs.append(_bib_entry_to_ref(etype, fields))
    return refs


def load_refs_file(path: str) -> list:
    """--refs 加载：JSON 数组或 BibTeX（v1.9）。.bib 扩展名直接走 BibTeX 解析；
    JSON 解析失败且内容以 @ 开头时自动降级 BibTeX（用户存错扩展名也能跑）。"""
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    if path.lower().endswith(".bib"):
        refs = parse_bibtex(text)
        if not refs:
            raise ValueError("BibTeX 文件中没有解析到任何条目（应有 @article{...} 等）")
        return refs
    if path.lower().endswith((".md", ".markdown")):
        # v4.0.0 医学文档直接核验：markdown 参考文献节 Vancouver 条目提取
        refs = parse_markdown_refs(text)
        if not refs:
            raise ValueError(
                "markdown 中未解析到编号参考文献条目（应有 '## 参考文献' 节与 '1. ' 编号行）"
            )
        return refs
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        if text.lstrip().startswith("@"):
            refs = parse_bibtex(text)
            if not refs:
                raise ValueError("内容以 @ 开头但 BibTeX 解析到 0 条，请检查文件格式")
            return refs
        raise


_REF_SECTION_RE = re.compile(r"(?:^|\n)#{0,6}\s*(?:\d+[.、]?\s*)?(?:参考文献|References)[^\n]*\n")


def parse_markdown_refs(text: str) -> list:
    """v4.0.0 从 markdown「参考文献」节提取 Vancouver 编号条目（医学文档主流形态：
    `1. **作者, et al.** 题名. *期刊*. 年;卷(期):页.`——无 DOI/PMID/URL）。
    提取的条目走 PubMed 题名反查通道（pubmed_title_reverse_lookup）获得官方核验。
    解析保守：无编号行/段数不足/题名过短的行跳过。

    v4.2.0（GB/T 7714 变体实测扩展）：16 条带内联 PMID 的 GB/T 著录全军覆没驱动——
    - 编号行支持 `[1] ` 方括号（与 `1. ` 并列，GB/T 最常见变体）；
    - 标题行支持裸「参考文献」行（无 # 前缀）；
    - 内联标识符提取：`PMID: 39429074` / `DOI: 10.xxx/yyy` 进 ref 字段——
      著录里带着官方锚，此前却被当无标识符引用盲查；
    - 卷(期):页提取 → volume/issue/pages（卷期页锚定通道原料）；
    - `[J]`/`[EB/OL]` 类型标记剥除；期刊段内「年, 卷(期): 页」残尾清理。"""
    refs = []
    m = _REF_SECTION_RE.search(text)
    body = text[m.end() :] if m else text
    for raw in body.splitlines():
        line = re.sub(r"\*\*|\*|__|_", "", raw.strip())
        mm = re.match(r"^(?:\[(\d{1,3})\][.、]?|(\d{1,3})[.、)])\s+(.{10,})$", line)
        if not mm:
            continue
        rest = (mm.group(3) or "").strip()
        if not rest:
            continue
        # 缩写句点不劈（v4.6.0 dogfood 实锤：'U.S. Food and Drug Administration'
        # 被切分器劈开，机构名当了题名）——「单大写字母+.」紧跟的句点不切分；
        # 普通首字母缩略后的题名界（如 N H. Title）不受影响
        segs = [s.strip(" *") for s in re.split(r"(?<![A-Z]\.[A-Z])\.\s+", rest) if s.strip(" *")]
        if len(segs) < 2:
            continue
        year = None
        # 后随数字的年份排除（批准文号 H20093320 里的 2009 不是年份）
        ym = re.search(r"(19|20)\d{2}(?!\d)", rest)
        if ym:
            year = int(ym.group(0))
        # 无作者段变体判定：GB/T 允许题名先行著录（`题名[J]. 期刊, 年, 卷(期): 页.`，
        # 机构共识/指南常见）——segs[0] 以文献类型标记结尾即为题名段
        if re.search(r"\[[A-Z]{1,2}(?:/OL)?\]\s*$", segs[0] or ""):
            # v4.7.0 点式缩写自愈（审计 P2-A 语义级修复）：链式缩写守卫保护了
            # U.S. 型机构名，也把欧式点式作者（HANSEN J.J. Title[J]）并进了首段。
            # 自愈条件：首段含 ". "（有被守卫吞掉的切分点）+ 基线切分的尾段仍以
            # 类型码结尾（=真题名）+ 头部含点式缩写模式（J.J——区别于普通题名）
            # + 无年份逗号（非期刊段）。三者齐备才拆回，普通题名零影响。
            parts0 = [p.strip(" *") for p in re.split(r"\.\s+", segs[0]) if p.strip(" *")]
            # 审计 P1 形态门：作者头（首段）须呈「姓氏 点式缩写」（HANSEN J.J /
            # SMITH A.B, JONES C.D）——题名自身含 U.S./Q.T.（Cost-effectiveness
            # of U.S. pharmacogenomics...）时形态不符，不拆（基线行为保持）。
            # 题名重建取 parts0[1:] 全部（题名内部的点式缩写也被守卫切开过）
            _authorish = parts0[0].count(" ") <= 4 and all(
                re.match(r"^[A-Za-z'\u2019\-]+(?:,? [A-Z](?:\.[A-Z])+\.?)?$", p.strip())
                for p in parts0[0].split(",")
                if p.strip()
            )
            if (
                len(parts0) >= 2
                and _authorish
                and re.search(r"\[[A-Z]{1,2}(?:/OL)?\]\s*$", parts0[-1])
                and not re.search(r"[,，]\s*(19|20)\d{2}", segs[0])
            ):
                # 该分支的内部切分点全是被守卫阻断的链式缩写（字母.字母.），
                # 切分吃掉的句点属题名本体——". " 重组还原（Q.T. interval 形态）
                segs = [parts0[0], ". ".join(parts0[1:])] + segs[1:]
                title, source = segs[1], (segs[2] if len(segs) >= 3 else "")
            else:
                title, source = segs[0], (segs[1] if len(segs) >= 2 else "")
        elif len(segs) >= 3:
            title, source = segs[1], segs[2]
        else:
            title, source = segs[0], ""
        if source and re.fullmatch(r"(19|20)\d{2}.*", source):
            source = ""
        # 访问日期残段（"(2023)[2026-10-05]" 形态）不作期刊名
        if source and re.match(r"^\((?:19|20)\d{2}\)\[[\d-]+\]$", source):
            source = ""
        if len(title) < 15:
            continue
        # 文献类型标记剥除（[J]/[EB/OL]/[M]/[C] 等 GB/T 类型码）
        title = re.sub(r"\[[A-Z]{1,2}(?:/OL)?\]\s*$", "", title).strip()
        source = re.sub(r"\[[A-Z]{1,2}(?:/OL)?\]\s*$", "", source).strip()
        # 期刊段残尾清理（"中华儿科杂志, 2024, 62(11): 1030-1042" → 期刊名）
        source = re.sub(r"[,，]\s*(?:19|20)\d{2}\s*[,，]?.*$", "", source).strip(" .,，")
        entry = {"title": title, "source": source, "year": year}
        # 内联标识符提取（authoritative anchor 前置——ref_to_url 已支持 PMID→官方 URL）
        pm = re.search(r"PMID\s*[:：]?\s*(\d{6,9})", rest, re.I)
        if pm:
            entry["pmid"] = pm.group(1)
        dm = re.search(r"\b(10\.\d{4,9}/[^\s，,;；)]+)", rest)
        if dm:
            entry["doi"] = dm.group(1).rstrip(".,;)")
        # v4.6.0：EB/OL 著录的 URL 提取（说明书/指南/共识的中文医学文档高频形态）
        # ——仅当无 doi/pmid（强锚优先不遮蔽）；[EB/OL] 引用从裸 unverified 升
        # 「可达性+官方层级」判据
        if "doi" not in entry and "pmid" not in entry:
            um = re.search(r"https?://[^\s，,;；)\]。，＞>”（“]+", rest)
            if um:
                entry["url"] = um.group(0).rstrip(".>）")
        # 卷(期):页 锚定在年份之后提取（避免误抓随机数字）。
        # 实测形态：`2024, 62(11): 1030-1042` / `2014, 134(5): e1474-502` /
        #           `2020, 8: 218`（无期）/ `2020, 35(12)`（无页）
        lm = re.search(
            r"(?:19|20)\d{2}\s*[,，]\s*(\d{1,4})\s*(?:\((\d{1,4})\))?"
            r"(?:\s*[:：]\s*([A-Za-z]{0,2}\d+[A-Za-z0-9]*))?",
            rest,
        )
        if lm:
            entry["volume"] = lm.group(1)
            entry["issue"] = lm.group(2) or ""
            entry["pages"] = lm.group(3) or ""
        refs.append(entry)
    return refs


def clean_title(line: str) -> str:
    """v3.3.1 标题清洗(demo 原型移植):剥序号前缀/ID 后缀/作者段——提升
    DOI/arXiv 元数据匹配的标题相似度(实测 demo 端 AlphaFold 整行 0.66→清洗后 0.9+)。"""
    t = re.sub(r"^(?:\[\d+\]|\d+[.)])\s*", "", line.strip())
    t = re.split(r"\s+(?:doi|pmid|arxiv)\s*[:：]", t, flags=re.I)[0]
    t = re.sub(
        r"(?:,|\.\s)\s*(?:et al\.?|and\s+[A-Z][a-z]+)[^0-9]{0,40}" r"(?:19|20)\d{2}", "", t, count=1
    )
    t = re.sub(r"[.。]\s*(?:19|20)\d{2}.*$", "", t)
    return t.strip()[:200] or line.strip()[:200]


def chunk_text(text: str, size: int = 900, overlap: int = 120) -> list:
    """段落分块（字符级,重叠防切断句界证据）。"""
    if not text:
        return []
    chunks, i = [], 0
    while i < len(text):
        chunks.append(text[i : i + size])
        i += size - overlap
    return chunks


def _tfidf_top(query: str, chunks: list, k: int = 2) -> list:
    """TF-IDF 保底检索（无 ollama 时）。纯标准库实现,选 top-k 索引。"""
    import math

    def tokens(t):
        return re.findall(r"[a-zA-Z0-9\u4e00-\u9fff]+", t.lower())

    q = tokens(query)
    if not q or not chunks:
        return list(range(min(k, len(chunks))))
    df = {}
    for ch in chunks:
        for w in set(tokens(ch)):
            df[w] = df.get(w, 0) + 1
    scores = []
    for ch in chunks:
        toks = tokens(ch)
        tf = {}
        for w in toks:
            tf[w] = tf.get(w, 0) + 1
        sc = sum(tf.get(w, 0) * math.log((len(chunks) + 1) / (df.get(w, 0) + 1)) for w in q)
        scores.append(sc)
    return sorted(range(len(chunks)), key=lambda i: -scores[i])[:k]


def _dup_title_sig(r: dict) -> str:
    """v3.4 去重指纹:引用行的归一化标题(小写去非字母数字)。
    同标识符+同标题=真重复;同标识符+不同标题=T2/T7 型拼接变体,须独立判定。
    审计 B3 修复:归一改走 _cjk_norm(保留 CJK)——旧 [^a-z0-9] 归一会把纯中文
    标题折成空串,导致「异题同 DOI」的两条中文引用被误并成真重复。"""
    return _cjk_norm(r.get("title") or r.get("claim") or "")[:120]


def mark_duplicates(results: list) -> None:
    seen = {}
    kind_zh = {"url": "URL", "doi": "DOI", "pmid": "PMID"}
    for r in results:
        sig = _dup_title_sig(r)
        keys = []
        if r.get("url"):
            keys.append(("url", normalize_url(r["url"]) + "|" + sig))
        if r.get("doi"):
            keys.append(("doi", r["doi"].lower() + "|" + sig))
        if r.get("pmid"):
            keys.append(("pmid", r["pmid"] + "|" + sig))
        hit = next(((k, seen[v]) for k, v in keys if v in seen), None)
        if hit:
            kind, first = hit
            r["note"] = (
                r["note"] + "；" if r["note"] else ""
            ) + f"与 #{first} 重复（同{kind_zh[kind]}）"
            if r["verdict"] == "verified":
                r["verdict"] = "partial"
        else:
            for _, v in keys:
                seen[v] = r["index"]


def _clone_pairs_scan(results: list) -> list:
    """v3.10 克隆引用对扫描（纯函数，零网络）：返回 [{a, b, kind}]。
      R1「同题不同 DOI」：同一真论文被写成多个 DOI 变体——克隆引用，
        至少一个标识为编造/错引（LLM 生成文本最常见的伪造形态之一）。
      R2「同 DOI 不同题」：拼接变体——两键各真但组合造假的前兆形态，
        mark_duplicates 已对其实行独立核验（v3.4 指纹），此处补成对警示。
    不改变五态判定：克隆对是高价值线索而非定罪证据，最终以元数据核验为准。
    归一比对走 _cjk_norm（中英同规）；长度差+quick_ratio 预筛控制 O(n²)
    常数（千条清单为秒级）——审计 B2 披露：预筛只作用于 R1；同 DOI 对
    豁免预筛（R2 无相似度下限，完全不同的标题也要走 R2 判定），预筛
    砍掉的 R2 粗端由 doi_metadata_match 的标题比对兜住。"""
    import difflib as _d

    pairs = []
    items = []
    for r in results:
        t = _cjk_norm(r.get("title") or r.get("claim") or "")
        items.append((r, t))
    n = len(items)
    for i in range(n):
        ra, ta = items[i]
        if len(ta) < 8:
            continue
        da = (ra.get("doi") or "").lower()
        for j in range(i + 1, n):
            rb, tb = items[j]
            db = (rb.get("doi") or "").lower()
            same_doi = bool(da) and da == db
            if len(tb) < 8 or abs(len(ta) - len(tb)) > max(len(ta), len(tb)) * 0.35:
                continue
            sm = _d.SequenceMatcher(None, ta, tb)
            # 审计 B2:预筛只作用于 R1;同 DOI 对豁免(R2 无相似度下限)
            if not same_doi and sm.quick_ratio() < 0.85:
                continue
            sim = sm.ratio()
            if sim >= 0.92 and da and db and da != db:
                pairs.append(
                    {"a": ra["index"], "b": rb["index"], "kind": "clone_doi", "sim": round(sim, 2)}
                )
            elif da and da == db and sim < 0.92:
                pairs.append(
                    {
                        "a": ra["index"],
                        "b": rb["index"],
                        "kind": "clone_title",
                        "sim": round(sim, 2),
                    }
                )
    return pairs


def detect_clone_pairs(results: list) -> int:
    """v3.10 克隆引用搭档检测（主流程调用一次）：扫描克隆对并为双方追加
    警示注记。判定不改——注记明确「以元数据核验为准」。返回克隆对数。"""
    zh = {
        "clone_doi": "同题不同 DOI（克隆引用：至少一个标识为编造或错引）",
        "clone_title": "同 DOI 不同标题（拼接变体警示：判定已各自独立核验）",
    }
    seen_pairs = set()
    cnt = 0
    for p in _clone_pairs_scan(results):
        key = (p["a"], p["b"], p["kind"])
        if key in seen_pairs:
            continue
        seen_pairs.add(key)
        ra = next(r for r in results if r["index"] == p["a"])
        rb = next(r for r in results if r["index"] == p["b"])
        note = f"克隆引用对 #{p['a']}↔#{p['b']}：{zh[p['kind']]}（相似度 {p['sim']}）→ 以元数据核验为准"
        for r in (ra, rb):
            r["note"] = (r["note"] + "；" if r.get("note") else "") + note
        cnt += 1
    return cnt


def collect_clone_pairs(results: list) -> list:
    """v3.10 渲染层只读收集（不写 note——detect_clone_pairs 已写过，渲染
    时重算只为取结构化列表，纯函数幂等零成本）。"""
    return _clone_pairs_scan(results)


# ═══ v3.11.0 清单画像与版本提示：从单条伪造到整批伪装 ═══

VERDICT_ZH = {
    "verified": "✅ verified",
    "partial": "🟡 partial",
    "unreachable": "⚠️ unreachable",
    "invalid": "❌ invalid",
    "unverified": "⏸ unverified",
}


# ═══ v3.7.0 文档级引用核查(--check-document):从清单核验到上下文核验 ═══

_CIT_NUM = re.compile(r"\[(\d{1,3}(?:\s*[,,]\s*\d{1,3})*)\]")
_CIT_RANGE = re.compile(r"\[(\d{1,3})\s*-\s*(\d{1,3})\]")
_CIT_AY = re.compile(
    r"\(([A-Z][A-Za-z\-]+)(?:\s+et\s+al\.)?[,;]\s*(\d{4})\)"  # (Smith, 2023)/(Smith et al., 2023)
    r"|([A-Z][A-Za-z\-]+\s+et\s+al\.)\s*\((\d{4})\)"
)  # Smith et al. (2023) 叙述式
_CIT_DOI = re.compile(r"https?://(?:dx\.)?doi\.org/(10\.[^\s)\]}]+)", re.I)
_SENT_SPLIT = re.compile(r"(?<=[。！？])\s*|(?<=[.!?])\s+(?=[A-Z0-9\u4e00-\u9fff])")
_STOP = set(
    "a an the of in on at to for and or is are was were be been with as by from "
    "that this these those it its we our their his her study paper research "
    "的 与 和 在 是 了 等 对 将 被 从 而 及 其 该 项 项".split()
)


def _sentences(text: str):
    parts = _SENT_SPLIT.split(text)
    return [p.strip() for p in parts if p and len(p.strip()) > 2]


def extract_citations(text: str) -> list:
    """从正文抽取 in-text 引用标记,返回 [{marker, kind, sentence, index[]}]."""
    out = []
    for sent in _sentences(text):
        found = {}
        for m in _CIT_RANGE.finditer(sent):
            lo, hi = int(m.group(1)), int(m.group(2))
            if 1 <= lo <= hi <= 999 and hi - lo <= 20:
                found[m.group(0)] = list(range(lo, hi + 1))
        for m in _CIT_NUM.finditer(sent):
            if m.group(0) in found:
                continue
            idxs = [int(x) for x in re.split(r"\s*[,,]\s*", m.group(1))]
            if all(1 <= x <= 999 for x in idxs):
                found[m.group(0)] = idxs
        for m in _CIT_AY.finditer(sent):
            if m.group(1):
                found[m.group(0)] = ("author-year", m.group(1), m.group(2))
            else:
                found[m.group(0)] = ("author-year", m.group(3).replace(" et al.", ""), m.group(4))
        for m in _CIT_DOI.finditer(sent):
            found[m.group(0)] = ("doi", m.group(1))
        for marker, idxs in found.items():
            kind = (
                "numeric"
                if isinstance(idxs, list)
                else idxs[0] if isinstance(idxs, tuple) else "numeric"
            )
            out.append({"marker": marker, "kind": kind, "sentence": sent[:400], "index": idxs})
    return out


def _norm_word(w: str) -> str:
    """轻词形归一:去复数/时态尾缀(≥5 字符才剥,防过削)。"""
    for suf in ("ing", "ies", "ed", "es", "s"):
        if len(w) > 4 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def _content_words(s: str) -> set:
    return {
        _norm_word(w)
        for w in re.findall(r"[a-z0-9\u4e00-\u9fff]{2,}", (s or "").lower())
        if w not in _STOP
    }


def anchor_rate(sentence: str, ref: dict) -> float:
    """引文句与被引条目标题的内容词重叠率(分母=标题词,0~1)。
    匹配容忍:完全相等或 ≥5 字符前缀互吞(thermometry~thermometer、cell~cells)。"""
    csl = (ref.get("checks", {}).get("doi_metadata", {}) or {}).get("csl", {}) or {}
    tw = _content_words(ref.get("title") or csl.get("title") or "")
    if not tw:
        return 0.0
    sw = _content_words(sentence)
    hit = 0
    for t in tw:
        if (
            t in sw
            or any(t.startswith(s) or s.startswith(t) for s in sw if min(len(s), len(t)) >= 5)
            or any(s == t for s in sw)
        ):
            hit += 1
    # v3.8.0:作者姓氏出现在引文句=强绑定证据(注册库权威名),计 1 词命中
    surnames = {a.split()[0].lower() for a in (csl.get("authors") or []) if a.split()}
    if surnames & sw:
        hit += 1
    return min(hit, len(tw)) / len(tw)


def bind_citation(cit: dict, results: list) -> dict:
    """标记→条目绑定。numeric=results[index-1];author-year=姓氏+年匹配;doi=直配。"""
    idxs = cit["index"]
    if isinstance(idxs, list):
        bound, missing = [], []
        for n in idxs:
            r = next((x for x in results if x.get("index") == n), None)
            (bound if r else missing).append(r if r else n)
        return {"marker": cit["marker"], "kind": "numeric", "bound": bound, "unbound": missing}
    if idxs[0] == "doi":
        r = next((x for x in results if (x.get("doi") or "").lower() == idxs[1].lower()), None)
        return {
            "marker": cit["marker"],
            "kind": "doi",
            "bound": [r] if r else [],
            "unbound": [] if r else [idxs[1]],
        }
    _, surname, year = idxs
    cands = [
        x
        for x in results
        if str(x.get("year") or "") == year
        and surname.lower()
        in _content_words(
            json.dumps(
                (x.get("checks", {}).get("doi_metadata", {}).get("csl", {}) or {}).get(
                    "authors", []
                ),
                ensure_ascii=False,
            ).lower()
        )
        or surname.lower() in (x.get("title") or "").lower()
    ]
    return {
        "marker": cit["marker"],
        "kind": "author-year",
        "bound": cands[:1],
        "unbound": [] if cands else [f"{surname} {year}"],
    }


_INTENTS_ZH = {"methodology": "方法学", "background": "背景", "result": "结果"}


_CONTRAST_RE = re.compile(
    r"(however|in contrast|(?<!not )\bunlike\b|contrary|contradict\w*|"
    r"\brefut(e[ds]?|ing)\b|\bdisput(e[ds]?|ing)\b|"
    r"\bchallenge[sd]?\b|\bquestion(s|ed|ing)?\b|fail(s|ed|ing)? to|"
    r"unable to|inconsisten\w*|"
    r"(?<!不)但|然而|与此相反|相反|并未|未能|不一致|质疑|挑战(?!性)|反驳|矛盾|争议)",
    re.I,
)
