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
VERIFY_SSL = os.environ.get("CN_MED_OA_VERIFY_SSL", "0") == "1"
CACHE_DIR = os.environ.get("CN_MED_OA_CACHE", os.path.join(os.path.expanduser("~"), ".cache", "cn-med-oa"))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
SKILL_VER = "2.0.0"

# ===== HTTP（禁代理 + 可选SSL校验 + 重试退避，移植 pubmed-verifier _api_get 思路）=====
_ctx = ssl.create_default_context()
if not VERIFY_SSL:
    _ctx.check_hostname = False
    _ctx.verify_mode = ssl.CERT_NONE
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
                min_relevance="low"):
    """检索 + 下载。返回 {query, field, attempts, final_status, files, disclosure, stats}。

    final_status:
      full            有相关(ok)结果且至少下载 1 篇
      metadata_only   有相关结果，未下载/无PDF
      low_relevance   有结果但全部相关性不足(被守门标记)
      not_found       检索无结果
    min_relevance: "ok" 只保留相关 / "low" 保留 low 及以上 / "irrelevant" 全保留
    """
    result = {"query": query, "field": field, "attempts": [], "final_status": "not_found",
              "files": [], "disclosure": "", "stats": {}}
    if not query:
        result["disclosure"] = "❌ 未提供检索词"
        return result

    rows, err = weipu_search(query, field=field, size=max_results + 3)
    result["attempts"].append({"source": "WeipuOA", "op": "search", "count": len(rows), "error": err})
    if not rows:
        result["disclosure"] = "❌ 维普OA无结果" + (("：" + err) if err else "")
        return result

    state_order = {"ok": 0, "low": 1, "irrelevant": 2}
    scored = []
    n_irrel = 0
    for idx, r in enumerate(rows):
        rel = relevance_gate(query, r, field)
        if state_order[rel["state"]] > state_order[min_relevance]:
            n_irrel += 1
            continue
        scored.append((state_order[rel["state"]], idx, r, rel))
    # 相关性优先、平台原序稳定：ok 填满名额，low 只在 ok 不足时补位
    # （否则"肝硬化"场景下 OR 匹配的"动脉粥样硬化"会挤掉真正的"肝硬化心肌病"）
    scored.sort(key=lambda x: (x[0], x[1]))
    kept = [(r, rel) for _, _, r, rel in scored[:max_results]]
    result["stats"] = {"returned": len(rows), "kept": len(kept), "filtered": n_irrel}

    if not kept:
        result["final_status"] = "low_relevance"
        sample_note = ""
        for r in rows[:3]:
            rg = relevance_gate(query, r, field)
            if rg.get("note"):
                sample_note = " " + rg["note"]
                break
        result["disclosure"] = ("⚠️ 检索返回 %d 条但相关性均不足（最高覆盖率 %.2f）。"
                                "建议改用规范医学单短语，或换字段 subject/keyword 重试。%s" %
                                (len(rows), max((relevance_gate(query, r, field)["score"] for r in rows), default=0),
                                 sample_note))
        return result

    got_full = got_meta = n_ok = 0
    for r, rel in kept:
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
                # PDF 文本交叉验证卷期（主源已是 API，这里升级一致性标记）
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
    if got_full:
        parts.append("✅ 下载 %d 篇全文" % got_full)
    if got_meta:
        parts.append("%d 篇仅元数据" % got_meta)
    if ok_n < len(result["files"]):
        parts.append("⚠️ %d 条相关性存疑(已标记 relevance.state)" % (len(result["files"]) - ok_n))
    chk = sum(1 for e in result["files"] if e.get("needs_human_check"))
    if chk:
        parts.append("🔶 %d 条卷期需人工核对(vol_source=%s)" %
                     (chk, ",".join(sorted(set(e.get("vol_source", "?") for e in result["files"] if e.get("needs_human_check"))))))
    result["disclosure"] = "维普OA：" + "，".join(parts)
    return result


def save_manifest(result, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, "cn_refs.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return path


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


def main():
    ap = argparse.ArgumentParser(description="中文医学文献OA聚合下载器(维普OA) v" + SKILL_VER)
    ap.add_argument("--query", required=True, help="检索词(建议规范医学单短语)")
    ap.add_argument("--field", default="title", choices=list(WEIPU_FIELDS.keys()), help="检索字段")
    ap.add_argument("--max", type=int, default=5, help="最大结果数")
    ap.add_argument("--out-dir", default=None, help="下载目录(不填则只检索元数据)")
    ap.add_argument("--no-pdf", action="store_true", help="仅元数据,不下载PDF")
    ap.add_argument("--min-relevance", default="low", choices=["ok", "low", "irrelevant"],
                    help="相关性过滤阈值: ok=只留相关 low=保留存疑 irrelevant=全保留")
    ap.add_argument("--citation", action="store_true", help="输出 GB/T 7714 引用行")
    args = ap.parse_args()

    r = fetch_cn_oa(args.query, args.field, args.max, args.out_dir, not args.no_pdf, args.min_relevance)
    if args.out_dir:
        save_manifest(r, args.out_dir)
    print(r["disclosure"])
    for e in r["files"]:
        rel = e["relevance"]
        tag = {"ok": "", "low": "[相关性存疑]", "irrelevant": "[不相关]"}[rel["state"]]
        pdf = ("PDF:" + os.path.basename(e["path"])) if e.get("path") else e.get("download_error", "仅元数据")
        print("  %s %s | %s %s;%s(%s) p=%s | doi=%s | %s" %
              (tag, e["title"][:42], e["journal"], e["year"], e["volume"], e["issue"],
               e.get("pages") or "-", e["doi"][:32], pdf))
        if args.citation:
            print("      引用: " + citation(e))
    sys.exit(0 if r["final_status"] in ("full", "metadata_only") else 1)


if __name__ == "__main__":
    main()
