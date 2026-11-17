# -*- coding: utf-8 -*-
"""
lit_norm_core.py — 文献归一 / 去重键 / 预印本-发表版配对 的**单一真源**（stdlib-only，无外部依赖）。

归属：ct-base §20.19（族归属）+ §20.19.7 红线2（本地引擎保留兜底）。
为何存在：归一内核此前在 normalize.py / dedupe_engine.py / meta-analysis block_a.py /
ct-registry coze lit_dedup_node.py / lit_rrf_node.py **五处各自重实现**（含 2026-11-02
CJK 题名归一升级只落在 normalize.py，其余四份是旧版）。本模块抽离纯函数作为权威版，
各消费端改为 `import` 薄壳，coze 端由构建脚本派生字面副本（selfcheck 断言 SHA 一致）。

消费端：
  - ct-literature/scripts/normalize.py        （import 薄壳，保留 merge* 高层函数）
  - ct-literature/adapters/dedupe_engine.py   （import 薄壳，保留 v2 / UnionFind / extract_identifiers）
  - meta-analysis/adapters/block_a.py         （import 薄壳，保留 meta 专属相似度/作者比对）
  - ct-registry/.../lit_dedup_node.py        （构建派生副本，import 本模块）
  - ct-registry/.../lit_rrf_node.py          （构建派生副本，import 本模块；消除 :48 逐字复制）

注意：CJK 题名归一依赖 adapters/cn_ref_normalizer.py（中文繁简/全半角）。若该模块在
运行环境不可导入，_norm_title 优雅退化为英文路径（与旧 coze 行为一致），绝不崩溃。
"""
import importlib.util
import os
import re
from difflib import SequenceMatcher

# ── 小写 source → 规范显示名（与 normalize.py 保持一致；Coze 端节点输出小写，
#    本地 fetch_* 输出大写，merge 时一律归一为规范名，避免大小写把分组/优先级撕裂）──
_SOURCE_CANON = {
    "openalex": "OpenAlex",
    "europepmc": "EuropePMC",
    "biorxiv": "bioRxiv",
    "medrxiv": "medRxiv",
    "semantic_scholar": "SemanticScholar",
    "arxiv": "arXiv",
    "pubmed": "PubMed",
    "ncbi": "PubMed",
    "medline": "PubMed",
    "zotero": "Zotero",
    "cnki": "CNKI", "知网": "CNKI",
    "wanfang": "WanFang", "万方": "WanFang",
    "sinomed": "SinoMed", "cbm": "SinoMed",
    "vip": "VIP", "维普": "VIP",
}


def _load_cn_title_normalizer():
    """加载 CJK 题名归一函数（升级项 I，2026-11-02）。

    与 normalize.py 同款：可经包导入或按文件加载，全失败返回 None —— 中文题名退化到
    原逻辑（去重仍可用，只是繁简/全半角变体不会合并），绝不让主流程崩溃。
    """
    try:
        from adapters.cn_ref_normalizer import normalize_cn_title
        return normalize_cn_title
    except Exception:
        pass
    try:
        _p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "adapters", "cn_ref_normalizer.py")
        _spec = importlib.util.spec_from_file_location("_ct_cn_ref_normalizer", _p)
        if _spec is not None:
            _m = importlib.util.module_from_spec(_spec)
            _spec.loader.exec_module(_m)
            return _m.normalize_cn_title
    except Exception:
        return None
    return None


_CN_TITLE_NORM = _load_cn_title_normalizer()
_CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def _canon_source(s):
    """source 归一为规范显示名（大小写不敏感；未知源原样返回）。"""
    if not s:
        return s
    return _SOURCE_CANON.get(str(s).strip().lower(), s)


def _norm_title(t):
    if not t:
        return ""
    # 中文题名走受控 CJK 归一（全半角 / 繁体 / 中文标点），否则同一篇论文会被
    # 不同库的写法撕裂成两条（升级项 I，2026-11-02）。英文题名路径保持原样，
    # 输出字节级不变，避免影响既有去重结果。
    if _CN_TITLE_NORM is not None and _CJK_RE.search(t):
        return _CN_TITLE_NORM(t)
    t = t.lower()
    t = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", t)
    return " ".join(t.split())


def _bare_doi(v):
    """DOI 字段兜底归一：剥掉 https://doi.org/ 等 URL 前缀 → 裸 DOI。"""
    if not v:
        return v
    s = str(v).strip()
    low = s.lower()
    for p in ("https://doi.org/", "http://doi.org/",
              "https://dx.doi.org/", "http://dx.doi.org/"):
        if low.startswith(p):
            return s[len(p):]
    return s


def _norm_doi(d):
    if not d:
        return None
    d = _bare_doi(d).strip().lower()
    m = re.search(r"10\.\d{4,9}/[^\s]+", d)
    if not m:
        return d
    # strip a trailing terminal punctuation a source may have appended to the DOI
    # (e.g. "10.1056/NEJMoa2403614.") so the bare DOI resolves / links cleanly.
    return m.group(0).rstrip(".,;:)]")


def dedupe_key(w):
    """去重键：优先 DOI，否则归一化标题。无效记录返回 None。"""
    if not isinstance(w, dict):
        return None
    doi = _norm_doi(w.get("doi"))
    title = _norm_title(w.get("title"))
    key = doi or ("t:" + title)
    if not key or key == "t:":
        return None
    return key


def _dedupe_preprint_published(works, title_threshold=0.85, author_threshold=0.3):
    """检测预印本-发表版配对，保留发表版（策略 A），返回新列表。

    一篇预印本（type=preprint）若在结果集中存在正式发表版本（type!=preprint），
    且归一化标题相似度 >= title_threshold、第一作者重叠 >= author_threshold，则视为
    同一研究：预印本被移除（superseded），发表版回填 preprint_doi 并加 has_preprint=True。
    仅在同一函数调用内配对，不引入外部 API；标题改动大或作者群大幅变动的发表版可能漏匹配。
    """
    preprints = [w for w in works if w.get("type") == "preprint"]
    if not preprints:
        return works

    superseded_dois = set()
    for p in preprints:
        pt = _norm_title(p.get("title"))
        if not pt:
            continue
        pa = [a.strip() for a in (p.get("authors") or []) if a and a.strip()]
        pa_set = set(a.lower() for a in pa)
        for w in works:
            if w.get("type") == "preprint":
                continue
            jt = _norm_title(w.get("title"))
            if not jt:
                continue
            sim = SequenceMatcher(None, pt, jt).ratio()
            if sim < title_threshold:
                continue
            ja = [a.strip() for a in (w.get("authors") or []) if a and a.strip()]
            ja_set = set(a.lower() for a in ja)
            overlap = len(pa_set & ja_set) / max(len(pa_set), 1)
            if overlap < author_threshold:
                continue
            # 配对成功 → 保留发表版 w，移除预印本 p
            if not w.get("preprint_doi"):
                w["preprint_doi"] = p.get("doi")
            w["has_preprint"] = True
            # 发表版缺失的字段从预印本回填
            for fld in ("abstract_snippet", "mesh", "keywords"):
                if not w.get(fld) and p.get(fld):
                    w[fld] = p.get(fld)
            superseded_dois.add(p.get("doi"))
            break  # 一个预印本只配对一个发表版

    if superseded_dois:
        works = [w for w in works if w.get("doi") not in superseded_dois]
    return works
