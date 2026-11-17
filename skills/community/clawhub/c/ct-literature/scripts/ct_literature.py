#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ct_literature.py — orchestration entry point.

One-shot pipeline: fetch OpenAlex (required) + optional Europe PMC / Semantic Scholar
-> normalize (merge + dedupe) -> HTML / XLSX report. Reads only public literature;
zero confidential data or information input.

Usage:
  python scripts/ct_literature.py --topic "osimertinib" --review-type systematic-review \
      --year-from 2018 --safety --run --out-dir ./out
"""
import argparse
import hashlib
import json
import os
import queue
import re
import sys
import threading
import time
import uuid
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPTS_DIR)
# adapters/ 位于技能根目录（scripts/ 的上一级）——保证 CLI 直接运行时能找到
sys.path.insert(0, os.path.dirname(_SCRIPTS_DIR))
from adapters import fetch_openalex
from adapters import fetch_europepmc
from adapters import fetch_pubmed      # 升级项 B：NCBI E-utilities（PubMed/MEDLINE + CDSR）
from adapters import fetch_semantic_scholar
from adapters import fetch_preprints
from adapters import fetch_arxiv
from adapters.fetch_coze_unified import dispatch as coze_dispatch, DISPATCHABLE_SOURCES, clip_by_date_window
from adapters import source_registry  # 架构韧性：连接器注册表 + 跨源熔断 + RRF 排名融合
# NOTE（2026-10-27）：`adapters.dedupe_engine` **不再在此顶层导入**。v1.6.0 起去重策略
# 已上移 coze lit_dedup 节点，生产路径走 `_dispatch_merge` 薄客户端（`adapters._coze_strategy`），
# 本模块对 dedupe_engine 无任何调用点（原顶层 import 是死引用）。
# 改为延迟导入的意义：CHANGELOG v1.6.0 要求「发布包剥离本地策略副本（源码保护）」，
# 顶层 import 会让剥离 dedupe_engine.py 后的发布包在启动时 ImportError。
# 本地实现仅由 tests/（`test_dedupe_engine.py` 等，不随包发布）按需导入使用。
# `normalize` 同理（2026-10-27 源码保护）：living-review 合并策略亦属本地策略副本，
# 改为 --merge-existing 分支内延迟导入；发布薄客户端镜像剥离该文件后，
# 未启用跨轮合并时完全不受影响，启用时优雅跳过（见 run() 内 merge_existing 分支）。
from xlsx_delivery import resolve_report_lang  # ct-base 共享件（publish_inject 注入）
import export_xlsx
import export_html
import score_relevance
import screen_prisma
import format_citations
import obsidian_exporter
import zotero_exporter
import topic_translator  # 检索词 中文→英文 翻译（本地词典 + 联网兜底）
import mesh_mapper       # 本地 MeSH 术语索引（概念归一化审计用，仅读 references/mesh_terms_mapping.json）
from adapters import verify_citations  # P0: citation identifier verification (anti-hallucination)
import evidence_log      # P0: provenance audit trail (ct-base §17.1)
from adapters import search_cache  # 本地搜索缓存（2026-10-26，TTL + --no-cache）
from adapters import fetch_prospero    # P1: PROSPERO systematic-review registry (key-gated, opt-in)
from adapters import guideline_corpus  # G: curated LOCAL guideline corpus (build-time: build_guidelines.py)
from adapters import http_utils  # shared GET+retry; load_openalex_key() auto-loads key from env/.env
# 升级项 G/H/I（2026-11-02）：三个纯本地增量适配器，均不改变 Coze 检索层。
from adapters import anchor_injector   # G: 段落级 Block ID 锚点（溯源 DOI → 段落）
from adapters import zotero_import     # H: Zotero 本地库导入（只读、MCP-free、无 key）
from adapters import cn_ref_normalizer  # I: 中文库导入（用户合法导出 RIS/JSON）+ CJK 归一化
import i18n  # bilingual (EN/ZH) localization


# ── friendly degradation notice (rate-limit / fetch failure) ─────────────────────
def _friendly_source_note(source, exc):
    """Build a bilingual, actionable degradation note when a source fails to fetch.

    Returns {"source", "status", "message_zh", "message_en", "banner"} so renderers can
    show the user's-locale string while the evidence log keeps BOTH languages. The console
    `banner` uses the current OS locale. Never aborts the pipeline — a failed source just
    degrades coverage, and the user is told exactly what happened and what to do.
    """
    rl = isinstance(exc, http_utils.RateLimitError)
    if rl and source == "OpenAlex" and exc.keyless:
        key, kw = "openalex.rate_limited", {"url": http_utils.OPENALEX_SIGNUP_URL}
    elif rl:
        key, kw = "source.rate_limited", {"source": source}
    else:
        key, kw = "source.error", {"source": source, "err": str(exc)}
    cur = i18n.t(key, **kw)                       # current OS locale
    i18n.set_lang("zh"); msg_zh = i18n.t(key, **kw)
    i18n.set_lang("en"); msg_en = i18n.t(key, **kw)
    i18n.set_lang(None)                          # reset to auto-detect
    return {"source": source, "status": "rate_limited" if rl else "error",
            "message_zh": msg_zh, "message_en": msg_en, "banner": cur}


# ── progress event stream (--progress json) ───────────────────────────────────
# human（默认）：保持可读控制台进度；json：stdout 只输出 NDJSON 事件流（供 agent 流式消费）。
_PROGRESS = "human"
_ORIG_STDOUT = None  # json 模式下保留真 stdout；子模块进度 print 转 stderr 保持 NDJSON 纯净


def _out(human_msg=None, event=None, **fields):
    """Emit one progress line.

    - human mode (default): print `human_msg` (None = silent, for json-only events).
    - json mode: print a single-line JSON object {"event": <event>, **fields} on the
      real stdout (always flushed so an agent can stream it); the human message is
      included as `message` so the streaming frontend can render it (sub-module prints
      are redirected to stderr by main()).
    """
    if _PROGRESS == "json":
        rec = {"event": event} if event else {}
        if human_msg is not None:
            rec["message"] = human_msg
        rec.update(fields)
        print(json.dumps(rec, ensure_ascii=False),
              file=_ORIG_STDOUT if _ORIG_STDOUT is not None else sys.stdout,
              flush=True)
    elif human_msg:
        print(human_msg, flush=True)


def _verify_top_n(works, n, timeout=15, check_consistency=True):
    """Verify only the top-N (already ranked) works concurrently.

    Used by `--verify top`: the most relevant / most-cited surviving works get full
    identifier verification; the rest are marked `unverified_sampled` (no network call).
    Each work's own `sources` list drives source-aware skip (a paper already returned by
    OpenAlex / Europe PMC skips the redundant same-source re-resolution).

    Returns (results_map, skipped_count).
    """
    target = works[:n]
    results = {}
    if not target:
        return results, len(works)
    _nw = min(8, len(target))
    with ThreadPoolExecutor(max_workers=_nw) as _ex:
        _futs = {}
        for _w in target:
            _ss = _w.get("sources") or ([_w.get("source")] if _w.get("source") else None)
            _futs[_ex.submit(verify_citations.verify_one, _w, timeout, _ss,
                              check_consistency)] = \
                verify_citations.work_key(_w)
        for _f in as_completed(_futs):
            results[_futs[_f]] = _f.result()
    return results, len(works) - len(target)


# P0 new capabilities default flags
DEFAULT_CITATION_STYLE = "apa"
# Export default = OFF: HTML + Excel are the standard deliverables; bib / ris /
# references_<style>.md are generated on demand (--export-bib or a chat request).
DEFAULT_EXPORT_BIB = False
DEFAULT_PRISMA = True
DEFAULT_RANK = "cited"  # keep legacy cited-by ordering unless --rank relevance

# ── 检索结构模型（组小学借鉴，2026-09-30 引入；P0/P1 全为 additive，向后兼容）──
# 检索深度 = 资源预算（lane/源/扩展/救援），非证据质量评级。
# 不传 --depth 时沿用旧 --max 语义（DEFAULT_DEPTH=None）。
DEPTH_PRESETS = {
    "quick":    {"max": 20,  "rescue": False, "expand": False},
    "standard": {"max": 50,  "rescue": True,  "expand": True},
    "deep":     {"max": 100, "rescue": True,  "expand": True},
}
DEFAULT_DEPTH = None

# 结构化 PICO 概念（干预/对照/结局独立成轴，避免全部压进 --topic 单串）
CONCEPT_TYPES = {
    "condition", "population", "intervention", "comparator",
    "outcome", "endpoint", "study_design", "biomarker", "drug", "indication",
}
# 证据维度分轨（组小学 QueryLane.evidence_dimension）：安全性信号不被疗效文献稀释
EVIDENCE_DIMENSIONS = ("general", "safety")


def _parse_concepts(raw_list):
    """解析 --concept TYPE=VALUE（可重复）为结构化概念列表。

    每个概念保留 input（用户原词）+ type；中文词经 topic_translator 翻英用于检索，
    经 mesh_mapper 尝试 MeSH 归一化并记录 mapping_status（exact_label / synonym /
    unmapped_literal）——失败保留原词并降级，绝不删除用户输入。
    返回 (concepts, errors)：concepts 为 dict 列表，errors 为非法提示串列表。
    """
    concepts, errors = [], []
    for item in (raw_list or []):
        if "=" not in item:
            errors.append("%r 缺少 TYPE=VALUE 格式" % item)
            continue
        ctype, cval = item.split("=", 1)
        ctype, cval = ctype.strip().lower(), cval.strip()
        if not cval:
            errors.append("%r 值为空" % item)
            continue
        if ctype not in CONCEPT_TYPES:
            errors.append("未知概念类型 %r（可选：%s）" % (
                ctype, ", ".join(sorted(CONCEPT_TYPES))))
            continue
        rec = {"type": ctype, "input": cval, "input_zh": cval,
               "translated": False, "value_en": cval,
               "mesh_id": None, "mesh_label": None, "mapping_status": "unmapped_literal"}
        # 中文→英文（检索用词）
        _tp = topic_translator.translate_topic(cval, online_fallback=True)
        if _tp["translated"]:
            rec["translated"] = True
            rec["value_en"] = _tp["topic_en"]
        # MeSH 归一化（仅审计 mapping_status，不阻塞检索）
        _m = _resolve_concept_mesh(cval)
        if _m:
            rec["mesh_id"] = _m.get("mesh_id")
            rec["mesh_label"] = _m.get("term")
            rec["mapping_status"] = ("exact_label" if cval.lower() == (_m.get("term") or "").lower()
                                      else "synonym")
        concepts.append(rec)
    return concepts, errors


_MESH_CACHE = None
def _resolve_concept_mesh(value):
    """用本地 references/mesh_terms_mapping.json 做 MeSH 归一化（仅审计用）。

    保守归一化：仅接受 term_key / entry_term / 中文翻译的**精确**匹配（大小写不敏感）；
    模糊子串匹配一律拒绝，未命中则返回 None → 概念记为 unmapped_literal（保留原词、
    不编造 MeSH）。这遵循组小学「自动术语扩展只接受精确 ID/标签/唯一同义」的硬规则。
    """
    global _MESH_CACHE
    try:
        if _MESH_CACHE is None:
            _MESH_CACHE = mesh_mapper.load_mesh_terms()
        _v = value.lower().strip()
        for _tk, _ti in _MESH_CACHE.get("terms", {}).items():
            _cands = [str(_tk)] + [str(x) for x in _ti.get("entry_terms", [])]
            if _ti.get("zh"):
                _cands.append(str(_ti["zh"]))
            if _v in [c.lower() for c in _cands]:
                return {"term": _tk, "mesh_id": _ti.get("mesh_id"), "zh": _ti.get("zh")}
    except Exception:
        pass
    return None


def _build_search_topic(topic_en, concepts):
    """把结构化概念 AND 拼接到检索式（干预/对照/结局分轴，不互相 OR 以免召回失真）。

    去重：概念词若已出现在主题中（或概念间重复），跳过，避免 'aspirin aspirin' 这类冗余。
    """
    if not concepts:
        return topic_en
    _seen, terms = set(), []
    _topic_l = topic_en.lower()
    for c in concepts:
        v = c.get("value_en")
        if not v:
            continue
        _vk = v.lower()
        if _vk in _seen or _vk in _topic_l:
            continue
        _seen.add(_vk)
        terms.append(v)
    if not terms:
        return topic_en
    return (topic_en + " " + " ".join(terms)).strip()


def _build_lane_plan(review_type, safety, concepts, depth, sources_enabled):
    """组小学 dry-run 规划视图：每条 lane 有 purpose / evidence_dimension / sources / notes。"""
    # 一次库车道（升级项 B 起含 PubMed）按启用情况拼接，避免规划视图漏报新车道。
    _biblio = "+".join([s for s in ("OpenAlex", "EuropePMC", "PubMed")
                        if s in sources_enabled]) or "OpenAlex"
    lanes = [{
        "purpose": "核心证据检索（主题 + 结构化概念 AND 拼接）",
        "evidence_dimension": "general",
        "sources": _biblio,
        "notes": "干预/对照/结局分轴，避免全部压进单一关键词",
    }]
    if safety:
        lanes.append({
            "purpose": "已发表安全性 / CSM 定性子集（独立 lane，不被疗效文献稀释）",
            "evidence_dimension": "safety",
            "sources": _biblio + "(含 AE/PV/毒性 关键词打标)",
            "notes": "产出 Safety-Related 表；定性，不替代 ct-safety 的 FAERS 定量",
        })
    for c in (concepts or []):
        lanes.append({
            "purpose": "概念轴 %s=%s（MeSH=%s, %s）" % (
                c["type"], c["input"], c.get("mesh_label") or "—", c["mapping_status"]),
            "evidence_dimension": "general",
            "sources": _biblio,
            "notes": "mapping_status 入证据溯源日志",
        })
    if depth in ("standard", "deep"):
        lanes.append({
            "purpose": "弱化结果救援（合并集偏薄时一轮放宽检索回补）",
            "evidence_dimension": "general",
            "sources": "OpenAlex(broaden)",
            "notes": "仅当合并唯一文献 < 阈值触发；无 eligible seed 记 skipped",
        })
    return lanes


# NOTE(2026-10-26): Coze→本地降级逻辑已迁入 adapters/source_registry.fetch_source
# （架构韧性层：声明式源表 + 跨源熔断 + RRF 融合）。run() online 分支改走
# source_registry.fetch_source；本处旧包装函数 _coze_dispatch_with_fallback 与
# _empty_payload 一并删除，避免重复实现（单源真相）。


def _parse_date(s):
    """Parse YYYY-MM-DD (or longer ISO) to a date object; None if missing/invalid."""
    if not s:
        return None
    s = str(s)[:10]
    if len(s) == 10 and s[4] == "-" and s[7] == "-":
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except Exception:
            return None
    return None


def _dispatch_merge(payloads, engine):
    """Route to the configured dedupe engine (2026-10-26 上移 coze lit_dedup，纯薄客户端).

    engine 取值由 coze lit_dedup 节点解释：
      v1: legacy 去重（DOI/title 为主）
      v2: 多标识归一（DOI/PMID/PMCID/arXiv）+ 传递闭包 + 模糊标题
    两者策略逻辑均在 coze 端执行；本地仅负责把 payloads 送上去、把结果取回来。

    去重 / 归一化 / PRISMA 组装的**策略逻辑**全部在 coze 端 lit_dedup 节点执行
    （含 v1/v2 两种引擎），本地仅负责把 payloads 送上去、把结果取回来。
    纯薄客户端：coze 不可用 → 返回空结果（不本地兜底），feature unavailable。

    本地 normalize.merge* / dedupe_engine.merge_v2* 实现仍保留供单测 / 离线，
    但发布包须剥离（源码保护）；生产路径一律走 coze。
    """
    from adapters._coze_strategy import call_coze_strategy
    final = call_coze_strategy("lit_dedup", {"engine": engine, "payloads": payloads})
    if final is None:
        return [], {"raw_count": None, "duplicates_removed": None,
                    "error": "coze lit_dedup unavailable"}
    works = final.get("projects") or []
    stats = {
        "raw_count": final.get("raw_count"),
        "duplicates_removed": final.get("duplicates_removed"),
    }
    return works, stats


def _guideline_topic_candidates(raw):
    """从检索式派生指南语料的匹配候选（升级项 I，2026-11-02）。

    语料 `topic` 字段是短英文主题（"diabetes" / "NSCLC"），而 `load()` 用子串匹配
    （`candidate in haystack`）。直接把完整检索式 `(type 2 diabetes OR T2DM)`
    传进去必然 0 命中——这不是「没有指南」，是匹配键形态不兼容。
    候选按区分度从高到低：整串 → 各 OR 分支 → 各分支里最长的词。
    """
    cands = []
    s = (raw or "").strip()
    if s:
        cands.append(s)
    inner = s[1:-1] if (s.startswith("(") and s.endswith(")")) else s
    parts = [p.strip() for p in re.split(r"\s+OR\s+", inner, flags=re.I) if p.strip()]
    for p in parts:
        if p not in cands:
            cands.append(p)
    toks = sorted({t for t in re.findall(r"[A-Za-z][A-Za-z0-9\-]{4,}", inner)},
                  key=len, reverse=True)
    for t in toks:
        if t not in cands:
            cands.append(t)
    return cands


def run(topic, review_type="all", year_from=None, year_to=None, safety=False,
        max_results=50, with_europepmc=True, with_semantic_scholar=False,
        with_biorxiv=True, with_medrxiv=True, with_arxiv=False,
        with_prospero=False, prospero_token=None, prospero_header="PROSPERO-ACCESS-TOKEN",
        with_guidelines=False, guideline_sources=None, guideline_max=20,
        verify_mode="all", verify_top_n=15, verify_consistency=True,
        verify_dois=False,
        out_dir="./out", make_xlsx=True, make_html=True, openalex_key=None,
        citation_style=DEFAULT_CITATION_STYLE, export_bib=DEFAULT_EXPORT_BIB,
        prisma=DEFAULT_PRISMA, rank=DEFAULT_RANK, keywords=None,
        obsidian=False, zotero=False, lang="auto", cochrane=False,
        merge_existing=None, stamp_date=None, preprint_fallback=True,
        download_pdf=False, include_reviews=True, online=False, offline=False,
        original_only=False, only_type=None,
        concepts=None, depth=None, rescue=False,
        snowball=True, snowball_max=10, snowball_seeds=3, snowball_from=None,
        interactive=False, report_first=True,         date_from=None, date_to=None,
        from_pack=None, topic_en=None,
        no_cache=False, cache_ttl=None, use_scihub=False, dedupe_engine="v1",
        zotero_import_path=None, merge_cn=None, guidelines_region=None, anchor=False,
        merge_cn_source=None, with_pubmed=False, pubmed_fallback=True):
    """merge_existing: path to a PREVIOUS run's .merged.json (or a payload dict /
    list of records). When set, this run's works are unioned with that history and
    every record is stamped first_seen / last_seen (living review / surveillance).
    Read from disk only — no network. Default None => behaviour unchanged.
    download_pdf: 是否在检索完成后进入 PDF 批量下载流程（opt-in）。
    zotero_import_path: Zotero 集合路径（升级项 H）——从本机 Zotero 本地 API 只读导入，
        作为补充检索源并入去重；None = 不启用。
    merge_cn: 中文库导出文件路径列表（升级项 I）——用户自行从 CNKI/万方/SinoMed
        导出的 RIS/JSON，纯导入、不爬取；None/[] = 不启用。
    guidelines_region: "china" / "global" / "both"（升级项 I）——指南证据车道区域过滤，
        None = 不过滤（等价 both，向后兼容）。
    anchor: 是否注入段落级 Block ID 锚点（升级项 G，默认 False）——需要本地 PDF；
        仅在 pdfs/ 目录有对应文件时生效，缺失则如实记录 pdf_missing。
    with_pubmed: 是否显式挂载 NCBI E-utilities 车道（升级项 B，默认 False）。
        PubMed/MEDLINE 与 CDSR 均可由该车道覆盖，是 Europe PMC 的对等替代通道；
        显式挂载时**无条件**参与检索（不受 Europe PMC 健康状态影响）。
    pubmed_fallback: Europe PMC 腿不可用（异常 / 0 命中）时自动启用 PubMed 车道补位
        （升级项 B，默认 True，`--no-pubmed-fallback` 关闭）。仅在未显式挂载
        PubMed（with_pubmed=False）且 Europe PMC 已启用时才会触发，不会重复检索。
    online: 使用 Coze 端统一检索（6 个文献源走 Coze 服务端），中间调用不记飞书；
        CLI 层默认 True（--local/--offline 显式回退），函数签名默认 False 保持程序化调用方兼容。
    offline: 强制本地兜底（不调 Coze），与老版本行为完全一致。
    snowball: U1 引用网络扩展（OpenAlex references + cited_by 1-hop）。
    interactive: U3 用户确认门控（暂停等待确认搜索策略 / 筛选结果）。
    report_first: U7 Report-first 模式（先建报告骨架再实时填充；用户看到报告从空到满的生长过程）。
    from_pack: pack_payloads.json 路径（批量打包预取结果，batch_lib --pack 下游）。
        命中的源跳过检索；未覆盖的源按原路由执行，覆盖度与非 pack 模式一致。
    no_cache: 本地搜索缓存停用（既不读也不写；等价 --no-cache / CT_LIT_NO_CACHE=1）。
    cache_ttl: 缓存 TTL 秒数（None = 环境变量 CT_LIT_CACHE_TTL > 默认 24h）。
    use_scihub: Sci-Hub 最后兑底显式开启（默认 False；仅 --use-scihub /
        CT_LIT_ALLOW_SCIHUB=1 时激活，法律风险用户自担，机构环境严禁开启）。"""
    # request_id（0.5.02，2026-11-11）：本次用户请求唯一 ID（uuid4）。透传 run() 内
    # 所有 Coze 调用（6 源检索 + 末尾飞书汇总），云端 feishu_write 按它做幂等去重——
    # 同一 request_id 恒写 1 行，根除「同请求被触发两次」的飞书双写（searchlog 实测）。
    # 2026-11-11 Fix E：优先继承 ct-advisor 注入的 CT_REQUEST_ID（一次用户请求内所有
    # 兄弟技能/端点调用共享同一 ID），无则新生成 uuid4。
    _request_id = os.environ.get("CT_REQUEST_ID") or uuid.uuid4().hex
    # Resolve once at the pipeline entry so EVERY deliverable (xlsx / html / md /
    # obsidian / zotero) shares the same language. Downstream modules used to
    # resolve "auto" against the *server* OS locale, which is en_US in the
    # published workbench -> all-English deliverables for Chinese users.
    lang = resolve_report_lang(lang, skill="literature")
    os.makedirs(out_dir, exist_ok=True)
    # snowball_from 聚焦模式：给定 DOI/PMID/题名时，跳过关键词检索、仅做引文网络扩展。
    # topic 缺省时用 seed 作为展示主题，避免下游把 None 当主题翻译。
    _sf_mode = bool(snowball_from)
    if _sf_mode and not topic:
        topic = snowball_from
    # normalize --keywords (comma-separated string) → list once, so scoring AND all
    # exporters (HTML banner / XLSX scope / meta JSON) see the same shape
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    # Chinese topic → English via bundled offline dictionary (term_map + drug_name_map).
    # The translated query goes to the APIs; the ORIGINAL topic is preserved for meta /
    # reports / evidence log so the user's wording stays reproducible.
    _topic_zh = topic
    _tp = None
    if topic_en and str(topic_en).strip():
        # 用户显式指定的英文检索词（工作台「可编辑英文检索词」链路）：跳过自动翻译。
        # 构造与 translate_topic 同形的返回，下游 meta/报告链路零改动。
        topic = str(topic_en).strip()
        _tp = {"translated": True, "topic_en": topic, "hits": None, "untranslated": []}
        _out("[i18n] " + i18n.t("topic.translated", en=topic) + "（用户指定）",
             "topic_translated", zh=_topic_zh, en=topic, manual=True)
    else:
        # 修复 2026-09-19：run() 作用域无 args（CLI 解析只在 main()），坏引用导致
        # NameError 崩溃。translate_topic 默认 online_fallback=True，直接用默认值，
        # 语义与修复前一致（block_a 已前置翻译纯英文，此处原样短路）。
        _tp = topic_translator.translate_topic(topic, online_fallback=True)
        if _tp["translated"]:
            topic = _tp["topic_en"]
            if _tp["untranslated"]:
                _out("[i18n] " + i18n.t("topic.partial", rest="、".join(_tp["untranslated"])),
                     "topic_translated", zh=_topic_zh, en=topic, partial=True)
            else:
                _out("[i18n] " + i18n.t("topic.translated", en=topic),
                     "topic_translated", zh=_topic_zh, en=topic, partial=False)
    # ---- 组小学借鉴：结构化概念（P0-1）+ 检索深度（P0-3）----
    # concepts 已在 main() 解析；此处把概念 AND 拼入实际检索式（search_topic），
    # 但 DISPLAY/META 仍用原 topic（_topic_zh），保持用户措辞可复现。
    _concepts = list(concepts or [])
    _search_topic = _build_search_topic(topic, _concepts)
    if _concepts:
        _out("[concepts] %d 个结构化概念（干预/对照/结局分轴）已 AND 拼入检索式；"
             "MeSH 归一化状态见证据溯源日志" % len(_concepts),
             "concepts", n=len(_concepts), types=[c["type"] for c in _concepts])
    http_utils.notify_openalex_key_if_missing(openalex_key)
    # Semantic Scholar key 提示（无条件触发，与是否启用该源无关——即使默认关闭，
    # 也应在首次使用/未配置时告知申请路径、不外发承诺与提速收益）
    http_utils.notify_s2_key_if_missing()
    oa_json = os.path.join(out_dir, "openalex.json")
    epmc_json = os.path.join(out_dir, "europepmc.json")
    pubmed_json = os.path.join(out_dir, "pubmed.json")  # 升级项 B：NCBI 车道中间产物
    s2_json = os.path.join(out_dir, "semantic_scholar.json")
    biorxiv_json = os.path.join(out_dir, "biorxiv.json")
    medrxiv_json = os.path.join(out_dir, "medrxiv.json")
    arxiv_json = os.path.join(out_dir, "arxiv.json")
    prospero_json = os.path.join(out_dir, "prospero.json")
    merged_json = os.path.join(out_dir, ".merged.json")

    # ---- 批量打包预取结果（--from-pack；batch_lib --pack 模式下游，2026-10-20）----
    # pack_payloads.json = dispatch 同构的 source payload 列表
    # （{"source": 显示名, "works": [...], "count": N, "total_count": N}）。
    # 命中的源不再检索；未覆盖的源（本地优先路由：openalex 有 key /
    # semantic_scholar）按原逻辑继续执行，保证覆盖度与非 pack 模式一致。
    _pack_payloads = []
    _pack_payload_sources = set()
    if from_pack:
        try:
            with open(from_pack, "r", encoding="utf-8") as _pf:
                _pk = json.load(_pf)
            if isinstance(_pk, dict):
                _pk = _pk.get("payloads") or _pk.get("results") or []
            if not isinstance(_pk, list):
                # 畸形载荷（如 payloads 是字符串）→ 显式告警后按空处理，
                # 退化为正常检索，而不是静默遍历字符串字符。
                _out("[WARN] --from-pack 载荷结构异常（%s），按空处理"
                     % type(_pk).__name__, "from_pack_malformed",
                     path=from_pack)
                _pk = []
            for _pp in (_pk or []):
                if isinstance(_pp, dict) and isinstance(_pp.get("works"), list):
                    _pack_payloads.append(_pp)
                    _pack_payload_sources.add(str(_pp.get("source") or ""))
        except Exception as _pe:
            _out("[ERROR] --from-pack 加载失败: %s" % _pe, "from_pack_failed",
                 error=str(_pe), path=from_pack)
            return 2

    # ---- fetch all enabled sources in PARALLEL (per-source concurrency) ----
    # Each source is independent; running them concurrently turns summed per-source
    # latency into the latency of the SLOWEST source.
    #
    # --online 模式：6 个文献源走 Coze 服务端（中间调用 log_feishu=False），
    #   Coze 不可用时自动降级本地 fetch（与老版本行为一致）。
    # --offline 模式：强制本地兜底（不调 Coze）。
    # 默认（CLI 不带 --local/--offline）：online（Coze 统一检索 + 飞书汇总留痕），
    #   2026-09-08 起翻转；函数签名默认仍为 online=False（程序化调用方兼容）。
    # ---- B 类三项上移（2026-11-04, Coze 0.4.00）：coze 优先 + 本地末位兜底 ----
    # 延迟 import：避免启动时加载 coze 出站配置。线上 0.3.99 期间 helper 对
    # 白名单外 source 会 fail-closed 并自动降级本地，生产行为不变（§20.19.7 红线 2）。
    from adapters._coze_lit_pipeline import (
        rrf_fuse as _coze_rrf_fuse,
        prisma_screen as _coze_prisma_screen,
        prospero_fetch as _coze_prospero_fetch,
    )

    def _coze_log(msg):
        _out(msg, "coze_b_pipeline")

    # RRF 输入快照：jobs 为空（全 from-pack）时也必须定义，否则 rank=rrf
    # 会在下方引用 _source_ranks / _rrf_payloads_snapshot 处 NameError
    # （既存隐患，一并根因修复）。
    _source_ranks = {}
    _rrf_payloads_snapshot = []
    jobs = []
    if online:
        # Coze 统一检索：遍历 SOURCE_REGISTRY（声明式源表）构建 jobs；
        # fetch_source 内含熔断 + coze→本地降级，行为 100% 向后兼容原 _coze_sources。
        for _name, _spec in source_registry.SOURCE_REGISTRY.items():
            if not _spec["active"] or not _spec["coze_routable"]:
                continue
            if _name in _pack_payload_sources:
                continue  # pack 已预取该源，跳过检索
            _src = _spec["coze_id"]
            if _src == "europepmc" and not with_europepmc:
                continue
            if _src == "semantic_scholar" and not with_semantic_scholar:
                continue
            if _src == "biorxiv" and not with_biorxiv:
                continue
            if _src == "medrxiv" and not with_medrxiv:
                continue
            if _src == "arxiv" and not with_arxiv:
                continue
            # 闭包捕获 _src/_name；fetch_source 复用 coze→本地降级逻辑。
            # cochrane 一并下传：本地兜底路径（OpenAlex ISSN / Europe PMC 期刊过滤）
            # 需要它才能真正限定 CDSR，否则 online 模式只能靠客户端二次过滤。
            jobs.append((_name, lambda s=_src, n=_name: source_registry.fetch_source(
                n, _search_topic, year_from, year_to, max_results, online=True,
                offline=offline, cochrane=cochrane,
                date_from=date_from, date_to=date_to, request_id=_request_id)))
        # PubMed（升级项 B）：NCBI E-utilities 独立车道，无 Coze 节点
        # （SOURCE_REGISTRY 中 coze_routable=False），故不参与上面的遍历，
        # 在此单独挂载；fetch_source 会走 local-only 分支。
        if with_pubmed and "PubMed" not in _pack_payload_sources:
            jobs.append(("PubMed", lambda: source_registry.fetch_source(
                "PubMed", _search_topic, year_from, year_to, max_results,
                online=True, offline=offline, cochrane=cochrane,
                date_from=date_from, date_to=date_to, request_id=_request_id)))
        # PROSPERO：2026-11-04 B 类三项上移，coze prospero 优先 + 本地末位兜底
        # （ct-base §20.19.7 红线 2）。检索式构造留本地；正式 token 时 helper
        # 自动保持本地路径；offline 分支（下方 else）不接 coze，尊重 --offline 语义。
        if with_prospero:
            jobs.append(("PROSPERO", lambda: _coze_prospero_fetch(
                _search_topic, review_type, year_from, year_to, safety,
                max_results, prospero_json, prospero_token,
                local_fn=lambda: fetch_prospero.fetch(
                    _search_topic, review_type, year_from, year_to, safety, max_results,
                    run=True, out=prospero_json, token=prospero_token,
                    header_name=prospero_header),
                log_fn=_coze_log)))
    else:
        # 老版本行为（本地 fetch），100% 向后兼容
        if "OpenAlex" not in _pack_payload_sources:
            jobs.append(("OpenAlex", lambda: fetch_openalex.fetch(
                _search_topic, review_type, year_from, year_to, safety, max_results,
                run=True, out=oa_json, api_key=openalex_key,
                include_reviews=include_reviews, date_from=date_from, date_to=date_to)))
        if with_europepmc and "EuropePMC" not in _pack_payload_sources:
            jobs.append(("EuropePMC", lambda: fetch_europepmc.fetch(
                _search_topic, review_type, year_from, year_to, safety, max_results,
                run=True, out=epmc_json, cochrane=cochrane,
                include_reviews=include_reviews, date_from=date_from, date_to=date_to)))
        # PubMed（升级项 B）：NCBI E-utilities 独立车道。offline 分支保持与其它源
        # 一致的直连 fetch 风格（可写 pubmed.json 中间产物，便于事后审计）。
        if with_pubmed and "PubMed" not in _pack_payload_sources:
            jobs.append(("PubMed", lambda: fetch_pubmed.fetch(
                _search_topic, review_type, year_from, year_to, safety, max_results,
                run=True, out=pubmed_json, cochrane=cochrane,
                include_reviews=include_reviews, date_from=date_from, date_to=date_to)))
        if with_semantic_scholar and "SemanticScholar" not in _pack_payload_sources:
            jobs.append(("SemanticScholar", lambda: fetch_semantic_scholar.fetch(
                _search_topic, review_type, year_from, year_to, safety, max_results,
                run=True, out=s2_json)))
        if with_biorxiv and "bioRxiv" not in _pack_payload_sources:
            jobs.append(("bioRxiv", lambda: fetch_preprints.fetch(
                _search_topic, review_type, year_from, year_to, safety, max_results,
                run=True, out=biorxiv_json, server="biorxiv",
                date_from=date_from, date_to=date_to)))
        if with_medrxiv and "medRxiv" not in _pack_payload_sources:
            jobs.append(("medRxiv", lambda: fetch_preprints.fetch(
                _search_topic, review_type, year_from, year_to, safety, max_results,
                run=True, out=medrxiv_json, server="medrxiv",
                date_from=date_from, date_to=date_to)))
        if with_arxiv and "arXiv" not in _pack_payload_sources:
            jobs.append(("arXiv", lambda: fetch_arxiv.fetch(
                _search_topic, review_type, year_from, year_to, safety, max_results,
                run=True, out=arxiv_json)))
        if with_prospero:
            jobs.append(("PROSPERO", lambda: fetch_prospero.fetch(
                _search_topic, review_type, year_from, year_to, safety, max_results,
                run=True, out=prospero_json, token=prospero_token, header_name=prospero_header)))

    # ---- 本地搜索缓存（2026-10-26；2026-11-13 作用域根因修复）----
    # TTL 内同 (source, 检索式, 年份/日期窗口, safety, max, cochrane, reviews) 的
    # per-source payload 直接复用，省 Coze 配额 + 提速；命中打 cache_hit 事件
    # 透明可审计，绝不静默替换。error payload 不缓存（写入侧把关）。
    # ⚠️ 缓存文件默认落用户级共享目录（resolve_cache_file），不再绑定每次唯一的
    # out_dir —— 旧行为导致缓存从不跨运行命中，实测 98.9% 同 topic 重复调用白跑。
    # 可逆：CT_LIT_CACHE_LOCAL=1 恢复旧行为；CT_LIT_CACHE_DIR 自定义位置。
    _cache_file = search_cache.resolve_cache_file(out_dir)
    # P2（2026-11-13 落地 / 2026-11-14 口径修正）：run 级「本次是否产生新检索」
    # 计数。list.append 在 CPython 下原子，供并行 jobs 安全累加。整次 run 全部
    # 命中缓存时不再写全量 A 汇总，但改发一条**轻量 cache_hit 行**，保证「每需求
    # 至少一条记录」（用户 2026-11-14 确认）；两类 payload 共用 P3 稳定键护栏，
    # 故同请求两轮 run 恒 1 行，不因恢复留痕而放大存储。
    # 可逆：CT_LIT_LOG_ON_CACHE_HIT=1 强制缓存命中时也写全量 A 汇总。
    _fresh_fetches = []

    def _cache_wrap(name, fn):
        _ck = search_cache.cache_key(
            name, _search_topic, review_type=review_type,
            year_from=year_from, year_to=year_to, safety=safety,
            max_results=max_results, cochrane=cochrane,
            include_reviews=include_reviews, date_from=date_from, date_to=date_to)

        def _wrapped():
            hit = None if no_cache else search_cache.load(_cache_file, _ck, ttl=cache_ttl)
            if hit is not None:
                _out("[cache] %s 命中本地缓存（TTL 内），跳过检索（--no-cache 可强制刷新）"
                     % name, "cache_hit", source=name)
                return hit
            _fresh_fetches.append(name)   # 未命中 → 本次 run 真实跑了一次检索
            _res = fn()
            if not no_cache:
                search_cache.save(_cache_file, _ck, _res)
            return _res
        return _wrapped

    jobs = [(n, _cache_wrap(n, f)) for n, f in jobs]

    # ---- snowball_from 聚焦模式：跳过全部关键词检索源与预取包（省配额、避免污染）----
    # 语料改由下方引文网络扩展（resolve_seed + referenced_works / cited_by 两跳）直接构成。
    if _sf_mode:
        jobs = []
        _pack_payloads = []

    # 记录本次实际参与缓存判定的 jobs 数（snowball / from-pack 可能为 0），
    # 供末尾 P2 判定使用；jobs 后续会被消费，不能再依赖其长度。
    _n_jobs = len(jobs)

    payloads = []
    if _pack_payloads:
        payloads.extend(_pack_payloads)
        _out("[from-pack] 已加载预取结果 %d 个源：%s（这些源跳过检索）"
             % (len(_pack_payloads), ", ".join(sorted(_pack_payload_sources)) or "-"),
             "from_pack", path=from_pack, sources=sorted(_pack_payload_sources))
    source_notes = []  # degradation notices for sources that failed to fetch (rate-limit / error)
    # ---- P0: citation verification pipeline (producer = fetch, consumer = worker pool).
    # Runs CONCURRENTLY with the fetch phase: as soon as a source yields its works they are
    # queued for verification — no need to wait for all downloads to finish. Each work is
    # verified the moment it arrives ("verify one as it lands"). ----
    _verify_q = queue.Queue()
    _verify_results = {}
    _verify_workers = []
    # Cross-source duplicates (the same work indexed by OpenAlex AND Europe PMC) share a
    # work_key — verify once, attach to every copy by key (see attach_verifications).
    _seen_keys = set()
    # Source-aware streaming verification runs in `all` and `background` modes.
    # In `top` mode we verify after ranking (only the top-N).
    # from-pack 预取结果与在线 fetch 一视同仁：同样进入 P0 引文验证
    # （Coze 端批量返回的 works 也要过反幻觉校验，ct-base §17.1）。
    # 注意 jobs 为空（全部源被 pack 覆盖）时也必须验证，故用 or 而非 and。
    _should_stream = (verify_mode in ("all", "background") and (jobs or _pack_payloads))
    if _should_stream:
        _out("[verify] mode=%s (streaming; source-aware skip on same-source re-resolution)"
             % verify_mode,
             "verify_mode", mode=verify_mode)
        _verify_done = 0
        _verify_lock = threading.Lock()

        def _verify_worker():
            nonlocal _verify_done
            while True:
                _item = _verify_q.get()
                if _item is None:
                    _verify_q.task_done()
                    break
                _w, _k, _src = _item
                try:
                    # verify_one always tries DOI -> PMID -> OpenAlex id. When the DOI
                    # is bot-blocked (big-publisher 403) it falls back to the bot-friendly
                    # PMID / OpenAlex APIs instead of being mislabeled "unresolved".
                    # (skip_sources is accepted for API compat but no longer suppresses
                    # that reliable fallback — see verify_citations CHANGELOG v0.6.6.)
                    _verify_results[_k] = verify_citations.verify_one(
                        _w, timeout=15, skip_sources=[_src] if _src else None,
                        check_consistency=verify_consistency)
                except Exception as _ve:  # one failure must not abort the pool
                    _verify_results[_k] = {"citation_verified": False,
                                          "citation_verify_status": "unresolved",
                                          "citation_verify_note": "verify-error: %s" % _ve}
                with _verify_lock:
                    _verify_done += 1
                    _done = _verify_done
                # message 必填：前端（workbench app.js）只渲染带 message 的 progress
                # 事件，2026-10-13 修复——此前 done=N 无 message，引文验证阶段
                # （全程最长，可达数分钟）在网页端零进度反馈。
                # total 取 _seen_keys 实时大小：验证条目随各源 fetch 完成动态入队
                # （596-598 行），启动时无法预知；producer put 先于对应 worker 的
                # done+=1，故恒有 done ≤ total（曾误用 len(jobs)=源数，出现 16/4）。
                _vt = len(_seen_keys)
                _out("⏳ 引文验证 %d/%d" % (_done, _vt),
                     "verify_progress", done=_done, total=_vt)
                _verify_q.task_done()

        _vw = min(24, max(4, (len(jobs) or 1) * 4))  # widened pool; per-host politeness enforced
        # by the connection-pool caps in http_utils (doi.org 8 / Crossref 4 / OpenAlex 6 /
        # EPMC 6), not by the worker count — so a 50-work verify finishes much sooner.
        for _ in range(_vw):
            _t = threading.Thread(target=_verify_worker, daemon=True)
            _t.start()
            _verify_workers.append(_t)
        # from-pack 预取 works 入队（与 fetch jobs 的生产者逻辑一致；
        # 否则 pack 模式下引文验证会被静默跳过，P0 反幻觉失效）。
        for _pp in _pack_payloads:
            for _w in (_pp.get("works") or []):
                _wk = verify_citations.work_key(_w)
                if _wk not in _seen_keys:
                    _seen_keys.add(_wk)
                    _verify_q.put((_w, _wk, _w.get("source")))

    # ---- U7: report-first skeleton (emit BEFORE fetch — user sees report growing) ----
    if report_first and make_html:
        try:
            _rf_html_out = os.path.join(out_dir, "lit_report.html")
            _rf_data = {"count": 0, "works": [], "meta": {
                "topic": _topic_zh,
                "topic_en": _tp.get("topic_en") if _tp["translated"] else None,
                "review_type": review_type, "year_from": year_from, "year_to": year_to,
                "safety": safety, "keywords": keywords,
            }}
            _rf_text = export_html.render(_rf_data, lang, safety=safety, report_first=True)
            with open(_rf_html_out, "w", encoding="utf-8") as _rf_f:
                _rf_f.write(_rf_text)
            _out("[OK] report-first skeleton -> %s (re-rendered after fetch)" % _rf_html_out,
                 "report_first_skeleton", path=_rf_html_out)
        except Exception as _rfe:
            _out("[WARN] report-first skeleton failed: %s" % _rfe, "report_first_failed", error=str(_rfe))

    # ---- time notice: a real run can take several minutes; tell the user up front ----
    # Honest estimate by verification scope; verification (`all`) overlaps with the fetch
    # phase but on large result sets still dominates the wall-clock time. Output path is
    # shown so the user knows where to look while waiting. Locale follows the OS.
    _est = i18n.t("run.est.%s" % verify_mode)
    if verify_mode == "top":
        _vmode = i18n.t("run.vmode.top", n=verify_top_n)
    else:
        _vmode = i18n.t("run.vmode.%s" % verify_mode)
    _out(i18n.t("run.starting", est=_est, vmode=_vmode, out=out_dir),
         "run_start", est=_est, vmode=_vmode, out=out_dir)

    # 各源 payload 按源名汇总（含失败源的 None）。提到 if 外初始化，
    # 供后面的 PubMed 备用车道判断「Europe PMC 腿是否真的不可用」。
    _res = {}
    if jobs:
        _t0 = time.time()
        _t_start = {n: time.time() for n, _ in jobs}
        # R7: warn the user before a potentially long online dispatch (Coze cloud);
        # no fabricated intermediate results, no parallel re-submission of same query.
        if online:
            _out(i18n.t("run.busy_hint"), "busy_hint")
        with ThreadPoolExecutor(max_workers=len(jobs)) as _ex:
            _futs = {_ex.submit(fn): name for name, fn in jobs}
            for _fut in as_completed(_futs):
                _name = _futs[_fut]
                try:
                    _p = _fut.result()
                    _res[_name] = _p
                    _n = len((_p or {}).get("works") or [])
                    _out("[OK] source %s: %d works in %.1fs"
                         % (_name, _n, time.time() - _t_start[_name]),
                         "source_done", source=_name, n=_n,
                         secs=round(time.time() - _t_start[_name], 1))
                    # stream this source's works into the verification queue immediately
                    if _should_stream and _p is not None:
                        for _w in (_p.get("works") or []):
                            _wk = verify_citations.work_key(_w)
                            if _wk not in _seen_keys:  # cross-source duplicates: verify once
                                _seen_keys.add(_wk)
                                _verify_q.put((_w, _wk, _w.get("source")))
                except Exception as _e:  # one source failing must not kill the pipeline
                    _note = _friendly_source_note(_name, _e)
                    _out(_note["banner"], "source_failed", source=_name,
                         status=_note.get("status"), message_en=_note.get("message_en"))
                    source_notes.append(_note)
                    _res[_name] = None
        # re-assemble in the original (stable) source order
        for _name, _ in jobs:
            _p = _res.get(_name)
            if _p is not None:
                payloads.append(_p)
        # 架构韧性：构建跨源排名映射（供 --rank rrf 使用），纯本地计算。
        # 2026-11-04：同时存一份**同一时刻**的 payloads 快照，供 coze lit_rrf
        # 重算 ranks（拍板口径「连 ranks 构建一起上移」）；本地 _source_ranks
        # 保留作末位兜底，两端输入一致才能等价（canary 可比对）。
        _source_ranks = source_registry.build_source_ranks(payloads)
        _rrf_payloads_snapshot = list(payloads)
        _out("[OK] parallel fetch: %d source(s) in %.1fs"
             % (len(jobs), time.time() - _t0),
             "fetch_done", sources=len(jobs), secs=round(time.time() - _t0, 1))
    else:
        if not from_pack:
            _out("[WARN] no sources enabled", "no_sources")

    # Drain the verification workers (they finish as the queue empties).
    # Normal modes drain here; `background` mode defers the drain until AFTER the
    # unverified fast preview is rendered (two-phase delivery).
    def _drain_verifiers():
        for _ in _verify_workers:
            _verify_q.put(None)
        for _t in _verify_workers:
            _t.join()

    if verify_mode != "background":
        _drain_verifiers()

    # ---- 升级项 H/I：外部本地源导入（Zotero 本地库 / 用户导出的中文库，2026-11-02）----
    # 纪律：两者都是**只读导入**——不联网检索、不爬取站点、不含 Cookie/浏览器驱动。
    # payload 形状与 fetch_* 完全一致，因此直接并入 payloads，参与同一套去重 /
    # 引文验证 / PRISMA 统计。失败一律如实告警并继续（不阻断主检索）。
    _import_stats = {}
    if merge_cn:
        for _cnf in merge_cn:
            try:
                _cnp = cn_ref_normalizer.payload_from_file(_cnf, source=merge_cn_source)
                payloads.append(_cnp)
                _import_stats.setdefault("cn", []).append(
                    {"file": _cnf, "source": _cnp["source"], "count": _cnp["count"]})
                _out("[OK] 中文库导入 %s → %s：%d 条（用户合法导出，非爬取）"
                     % (os.path.basename(_cnf), _cnp["source"], _cnp["count"]),
                     "cn_import", file=_cnf, source=_cnp["source"], count=_cnp["count"])
            except Exception as _ce:
                _out("[WARN] 中文库导入失败 %s: %s" % (_cnf, _ce), "cn_import_failed",
                     file=_cnf, error=str(_ce))
    if zotero_import_path:
        try:
            _zp = zotero_import.fetch(zotero_import_path)
            payloads.append(_zp)
            _import_stats["zotero"] = {"collection": _zp.get("collection"),
                                       "count": _zp["count"], "stats": _zp.get("stats")}
            _out("[OK] Zotero 导入「%s」：%d 条（只读本地 API，无 key）"
                 % (_zp.get("collection") or zotero_import_path, _zp["count"]),
                 "zotero_import", collection=_zp.get("collection"), count=_zp["count"])
        except Exception as _ze:
            # Zotero 未开本地 API / 未运行是常见情况：如实告警并继续，绝不静默当 0 条
            _out("[WARN] Zotero 导入跳过：%s" % _ze, "zotero_import_failed",
                 error=str(_ze))

    # ---- 升级项 B：PubMed 备用车道（Europe PMC 腿不可用时自动补位）----
    # 背景：Europe PMC 是本技能唯一**原生同时覆盖** PubMed/MEDLINE 与 Cochrane CDSR
    # 的源。它一旦限流/不可达，PubMed 与 Cochrane 的覆盖会同时归零，而 OpenAlex
    # 只兜住 PubMed 那一半（CDSR 无过滤器）。NCBI E-utilities 直连车道与 Europe PMC
    # 相互独立，可在后者故障时把两半都补回来。
    #
    # 触发条件（三者同时满足）：
    #   ① --pubmed-fallback（默认开）；② 未显式 --with-pubmed（避免同一源检索两次）；
    #   ③ Europe PMC 腿确实不可用——抛异常，或有 hit_count 但 0 条落地。
    # 为什么必须放在 _dispatch_merge 之前：备用腿的产物要与常规源 payload 走同一套
    # 去重 / 评分 / PRISMA / 报告，否则下游全部漏掉这条腿。
    if pubmed_fallback and not with_pubmed and with_europepmc and not _sf_mode:
        _epmc_p = _res.get("EuropePMC")
        if _epmc_p is None:
            # --from-pack 模式下命中源不参与检索（jobs 里没有它），_res 自然查不到；
            # 但它的 payload 已经在 _pack_payloads 里进来了。不兜这一手的话，
            # 会误判「Europe PMC 腿不可用」从而多加一次本不必要的 PubMed 检索。
            _epmc_p = next((p for p in payloads
                            if (p or {}).get("source") == "EuropePMC"), None)
        _epmc_ok = bool(_epmc_p) and (
            len(_epmc_p.get("works") or []) > 0 or bool(_epmc_p.get("hit_count")))
        if not _epmc_ok:
            _out("[PubMed-fallback] Europe PMC 腿不可用（请求异常或 0 命中），"
                 "启用 NCBI E-utilities 备用车道补位；该腿与 Europe PMC 相互独立，"
                 "可覆盖 PubMed/MEDLINE 与 Cochrane CDSR（--no-pubmed-fallback 可关闭）",
                 "pubmed_fallback", source="EuropePMC")
            try:
                _pub = source_registry.fetch_source(
                    "PubMed", _search_topic, year_from, year_to, max_results,
                    online=online, offline=offline, cochrane=cochrane,
                    date_from=date_from, date_to=date_to, request_id=_request_id)
                _pub_n = len((_pub or {}).get("works") or [])
                _out("[OK] source PubMed (fallback): %d works" % _pub_n,
                     "source_done", source="PubMed", n=_pub_n, fallback=True)
                payloads.append(_pub)
                source_notes.append({
                    "source": "PubMed",
                    "status": "fallback",
                    "note": "Europe PMC 腿不可用，已由 NCBI E-utilities 车道补位"
                            "（PubMed/MEDLINE + Cochrane CDSR）",
                })
            except Exception as _pe:
                _note = _friendly_source_note("PubMed", _pe)
                _out(_note["banner"], "source_failed", source="PubMed",
                     status=_note.get("status"), message_en=_note.get("message_en"))
                source_notes.append(_note)

    # ---- snowball_from 聚焦模式：不依赖关键词检索与去重服务，语料由引文网络扩展直接构成 ----
    if _sf_mode:
        works, dedup_stats = [], {}
    else:
        works, dedup_stats = _dispatch_merge(payloads, dedupe_engine)

    # ---- fail-loud：去重服务不可用 ≠ 检索无结果（2026-10-27，v1.6.0 薄客户端）──
    # 去重策略已上移 coze lit_dedup，本地是纯薄客户端：coze 不可用时
    # _dispatch_merge 返回空列表。**空列表是服务故障，不是「没检索到文献」**——
    # 静默往下跑会产出一份 0 篇的「成功」报告，用户无从区分二者。此处显式标脏：
    # ① 控制台/JSON 事件醒目告警；② 写进 source_notes（→ evidence_log 留痕）；
    # ③ 写进 meta.data_integrity（→ HTML/XLSX 报告可呈现）。不中断流程。
    _dedupe_unavailable = bool(dedup_stats.get("error"))
    if _dedupe_unavailable:
        _out("[FATAL] 去重服务不可用（coze lit_dedup 未响应）：合并去重未执行，"
             "works 为空系**服务故障**所致、而非检索无结果。本次结果不可信，"
             "请勿据此出报告——请确认 ct-search 端点已部署 lit_dedup 节点后重跑。",
             "dedupe_unavailable", error=dedup_stats.get("error"))
        source_notes.append({
            "source": "lit_dedup",
            "status": "unavailable",
            "note": "coze lit_dedup 未响应：合并去重未执行，结果为空且不可信"
                    "（非「检索无结果」）",
        })

    # ---- 路线 B：月份级日期窗口客户端兜底裁剪（合并后最终保险）----
    # 复用 fetch_coze_unified.clip_by_date_window：publication_date 精滤 +
    # 缺日期回退 year 粗兜底。online（Coze）与 offline 通道均覆盖——dispatch
    # 已对单源裁过，此处对合并去重后的全集再裁一次兜底（含 europepmc 空日期
    # 场景：靠 year 先砍跨年超窗，边界年内保守保留交周报人工判断）。
    if date_from or date_to:
        works, _dw = clip_by_date_window(works, date_from, date_to)
        if _dw["dropped"] or _dw["year_fallback"]:
            _out("[date-window] 合并后裁剪：丢弃 %d 篇超窗、%d 篇边界年内缺精确日期"
                 "（year 兜底保守保留）、%d 篇无日期，窗口 [%s, %s]"
                 % (_dw["dropped"], _dw["year_fallback"], _dw["no_date"],
                    date_from, date_to),
                 "date_window_clip", dropped=_dw["dropped"],
                 year_fallback=_dw["year_fallback"], no_date=_dw["no_date"])

    # ---- P0-2：证据维度分轨（组小学 QueryLane.evidence_dimension 思想）----
    # 安全性文献独立打标，使其不被疗效文献稀释；下游 Safety-Related 表据此播种。
    for _w in works:
        _w["evidence_dimension"] = "safety" if _w.get("is_safety") else "general"

    # ---- snowball_from：从指定文献（DOI/PMID/题名）出发的引文网络扩展（前后向两跳）----
    # 解析 seed → OpenAlex 文献 → 展开其 references（后向）+ cited_by（前向）。
    # 返回的列表首元素是该种子文献本身（direction="seed"），其余为其邻居。
    if _sf_mode:
        try:
            _sf_works = fetch_openalex.snowball_from(
                snowball_from, direction="both",
                max_refs=min(max(snowball_max, 1), 50), api_key=openalex_key)
        except Exception as _sfe:
            _out("[WARN] snowball_from failed: %s" % _sfe,
                 "snowball_from_failed", error=str(_sfe))
            _sf_works = []
        if not _sf_works:
            _out(i18n.t("snowball_from.not_found", seed=snowball_from),
                 "snowball_from_not_found", seed=snowball_from)
        else:
            _sf_seed = _sf_works[0]
            _out(i18n.t("snowball_from.seed", title=(_sf_seed.get("title") or "")[:80],
                        id=_sf_seed.get("id")), "snowball_from_seed",
                 id=_sf_seed.get("id"), title=_sf_seed.get("title"))
            _fwd = sum(1 for w in _sf_works if w.get("snowball_direction") == "cited_by")
            _bwd = sum(1 for w in _sf_works if w.get("snowball_direction") == "references")
            _out(i18n.t("snowball_from.done", total=len(_sf_works), fwd=_fwd, bwd=_bwd),
                 "snowball_from_done", total=len(_sf_works), fwd=_fwd, bwd=_bwd)
        works = _sf_works
        dedup_stats = {"snowball_from": True, "duplicates_removed": 0,
                       "raw_count": len(_sf_works)}
        for _w in works:
            _w.setdefault("evidence_dimension",
                          "safety" if _w.get("is_safety") else "general")
        # 聚焦模式：关掉关键词雪球块（避免对已有语料二次扩展）与弱化结果救援
        snowball = False

    # ---- P1-6：弱化结果救援（组小学 weak-result rescue）----
    # 仅 standard/deep 深度、且合并唯一文献偏薄、且概念曾收窄过检索式时，
    # 用更宽检索式（仅主题、去概念收窄）回补一轮。单次、非致命。
    if (rescue and depth in ("standard", "deep") and len(works) < 5
            and _search_topic.strip() != topic.strip() and not _sf_mode):
        try:
            _rescue_path = os.path.join(out_dir, "rescue_openalex.json")
            _out("[rescue] 合并唯一文献仅 %d 篇，触发弱化结果救援（放宽至主题级检索）"
                 % len(works), "rescue", before=len(works))
            _rb = fetch_openalex.fetch(
                topic, review_type, year_from, year_to, safety, max_results,
                run=True, out=_rescue_path, api_key=openalex_key,
                include_reviews=include_reviews, date_from=date_from, date_to=date_to)
            if _rb and _rb.get("works"):
                works, dedup_stats = _dispatch_merge(payloads + [_rb], dedupe_engine)
                for _w in works:
                    _w.setdefault("evidence_dimension",
                                  "safety" if _w.get("is_safety") else "general")
                _out("[rescue] 回补后唯一文献 %d 篇" % len(works),
                     "rescue_done", after=len(works))
            else:
                _out("[rescue] 回补无新增（记 skipped，不自称覆盖）", "rescue_skipped")
        except Exception as _re:
            _out("[WARN] rescue failed: %s" % _re, "rescue_failed", error=str(_re))

    # ---- U1: snowball (citation-network expansion via OpenAlex) ----
    # Expand top-seed works via 1-hop references + cited_by to find related
    # papers that keyword search may miss. Deduped against existing corpus.
    if snowball and works:
        try:
            _snowball_max = min(max(snowball_max, 1), 50)
            _snowball_seeds = min(max(snowball_seeds, 1), 10)
            # Only OpenAlex-sourced seeds have a usable OpenAlex ID (URL form)
            # for the references / cited_by endpoints; Europe PMC / S2 seeds use
            # different ID schemes (PMID, S2 corpus id) and must be skipped.
            _seeds = [s for s in works[:_snowball_seeds * 2]
                      if s.get("id") and str(s.get("id", "")).startswith("http")]
            _seed_ids = [s["id"].strip("/").split("/")[-1] for s in _seeds[:_snowball_seeds]]
            if _seed_ids:
                _out(i18n.t("snowball.starting", seeds=_snowball_seeds, max_per_seed=_snowball_max),
                     "snowball_start", seeds=_snowball_seeds, max_per_seed=_snowball_max)
                _snow_works = []
                for _sid in _seed_ids:
                    _ext = fetch_openalex.fetch_snowball(
                        _sid, direction="both", max_refs=_snowball_max,
                        api_key=openalex_key)
                    _snow_works.extend(_ext)
                if _snow_works:
                    _before = len(works)
                    works, dedup_stats = _dispatch_merge(
                        [{"source": "OpenAlex", "query": "snowball", "works": _snow_works}] + payloads,
                        dedupe_engine)
                    _added = len(works) - _before
                    for _w in works:
                        _w.setdefault("evidence_dimension",
                                      "safety" if _w.get("is_safety") else "general")
                    if _added > 0:
                        _out(i18n.t("snowball.done", added=_added, seeds=len(_seed_ids)),
                             "snowball_done", added=_added, seeds=len(_seed_ids))
                    else:
                        _out(i18n.t("snowball.empty"), "snowball_empty")
                else:
                    _out(i18n.t("snowball.empty"), "snowball_empty")
            else:
                _out(i18n.t("snowball.skipped"), "snowball_skipped")
        except Exception as _sexc:
            _out("[WARN] snowball failed: %s" % _sexc, "snowball_failed", error=str(_sexc))
    elif not snowball:
        _out(i18n.t("snowball.skipped"), "snowball_skipped")

    # ---- cross-run incremental merge (living review / surveillance) ----
    # Opt-in via --merge-existing: union this run's works with a PREVIOUS run's local
    # .merged.json and stamp first_seen / last_seen. Pure local file read. When
    # merge_existing is None this block is a no-op and the pipeline is byte-identical
    # to before. Runs BEFORE the Cochrane filter so retained records are filtered too.
    merge_stats = None
    if merge_existing:
        # 延迟导入（源码保护）：normalize 属本地策略副本，发布包剥离。
        # 完整版正常合并；发布薄客户端镜像优雅跳过（不崩溃、不本地兜底实现）。
        try:
            import normalize
        except ImportError:
            normalize = None
        if normalize is None:
            _out("[merge-existing] 本地合并策略模块不可用（发布薄客户端镜像），"
                 "已跳过跨轮合并；如需 living-review 请使用完整版。",
                 "merge_existing_skipped")
        else:
            works, merge_stats = normalize.merge_with_history(
                works, merge_existing, today=stamp_date)
            _out("[merge-existing] +%d new / %d carryover / %d retained-from-history "
                 "= %d works (stamp %s)"
                 % (merge_stats["new"], merge_stats["carryover"],
                    merge_stats["retained_only"], merge_stats["total"],
                    merge_stats["stamp"]),
                 "merge_existing", **merge_stats)

    # ---- preprint candidates for non-OA works (default-ON; opt-out via --no-preprint-fallback) ----
    # For works with no OA full text (is_oa false / open_access_url empty), search
    # bioRxiv / medRxiv (Europe PMC PPR) + arXiv by title and attach an author-verified
    # candidate to work["preprint"] (ported from meta-analysis pdf_fetch: "prefer
    # missing over wrong" — any author-check failure drops the candidate).
    preprint_stats = None
    if preprint_fallback:
        from adapters import preprint_fallback as _pf
        preprint_stats = _pf.enrich(works, progress=lambda m: _out(m, "preprint"))
        _out("[preprint-fallback] scanned=%d candidates=%d rejected=%d no-authors=%d "
             "servers=%s" % (preprint_stats["scanned"], preprint_stats["candidates"],
                             preprint_stats["rejected"], preprint_stats["skipped_no_authors"],
                             ",".join(preprint_stats["servers"])),
             "preprint_fallback", **preprint_stats)

    # Full API total for the Cochrane journal-filtered Europe PMC query — captured
    # from the fetcher's `hit_count` (independent of --max), so it reports the true
    # Cochrane count rather than just the capped sample we fetched for reading.
    _epmc_payload = next((p for p in payloads if p.get("source") == "EuropePMC"), None)
    _epmc_hit = (_epmc_payload or {}).get("hit_count")
    # Coze-unified payloads carry `total_count` instead of `hit_count` (local fetch
    # sets hit_count). Without this fallback the Cochrane total silently reports
    # None on every --online run. (2026-10-30 field incident.)
    if _epmc_hit is None and _epmc_payload:
        _epmc_hit = _epmc_payload.get("total_count")
        if _epmc_hit is None:
            _epmc_hit = _epmc_payload.get("count")

    # ---- Cochrane-only focus (--cochrane): keep only works whose publication is
    # the Cochrane Database of Systematic Reviews. The Europe PMC leg is already
    # journal-filtered; this also drops any non-Cochrane OpenAlex/other hits so
    # the merged set is a clean Cochrane set. Uses the unified `publication`
    # field (present in every source's normalized record). ----
    if cochrane:
        _before = len(works)
        # Schema-tolerant journal match. The local fetch_europepmc normalizer emits
        # `publication`, but coze-unified payloads emit `journal_iso` (and no
        # `publication` at all). Matching only `publication` therefore matched
        # nothing on every --online run and silently emptied the whole result set.
        # `is_cochrane` (set by the local normalizer) is honored when present.
        # (2026-10-30 field incident: SGLT2i/CKD dedup run -> 0 works, empty report.)
        _COCHRANE_FIELDS = ("publication", "journal_iso", "journal", "venue",
                            "container_title")
        works = [w for w in works
                 if w.get("is_cochrane")
                 or any("cochrane" in str(w.get(_f) or "").lower()
                        for _f in _COCHRANE_FIELDS)]
        cochrane_count = len(works)          # sample kept for reading / reporting
        cochrane_total = _epmc_hit           # full API total (independent of --max)
        _out("[cochrane] kept %d Cochrane work(s) from %d merged; "
             "full Cochrane total (Europe PMC) = %s"
             % (len(works), _before, cochrane_total), "cochrane_filter",
             kept=len(works), total=_before, full_total=cochrane_total)

        # The server-side journal filter only exists on the local Europe PMC leg.
        # On the coze-unified path the flag is not pushed upstream, so the fetch is
        # NOT CDSR-restricted and this client-side filter is the only enforcement.
        if _epmc_payload and (_epmc_payload.get("_provenance") == "coze"):
            _out("[WARN] --cochrane 经 coze 统一后端检索时，Cochrane 期刊过滤未在后端"
                 "生效：本次 Europe PMC 段未按 CDSR 限定，客户端过滤后可能漏掉真实存在的"
                 "Cochrane 系统评价。需要严格的 Cochrane 检索请加 --no-online（本地直连 "
                 "Europe PMC）或改用 literature_probe --layer cochrane。",
                 "cochrane_filter_not_pushed")

        # Fail fast. --cochrane is a Cochrane-ONLY focus mode: it discards every
        # non-CDSR record. When it empties a previously non-empty set, the pipeline
        # used to sail on and emit an empty .merged.json (count=0, prisma
        # identified_records=0) plus "仅找到 0 篇唯一文献" — a silent zero that reads
        # as "no literature exists" instead of "the focus filter matched nothing".
        if _before > 0 and not works:
            raise SystemExit(
                "[ERROR] --cochrane 是「仅 Cochrane」聚焦模式，本次 %d 条合并记录中"
                "没有一条来自 Cochrane Database of Systematic Reviews，过滤后为空。\n"
                "        该标志会丢弃全部非 CDSR 记录，不能用于普通跨库查重。\n"
                "        若要「跨库检索 + Cochrane 层查重」，请去掉 --cochrane"
                "（Europe PMC 默认已开启），\n"
                "        Cochrane 层命中数由 meta-analysis 的 "
                "literature_probe.py --layer cochrane 单独给出。\n"
                "        若确实只要 Cochrane 系统评价，请放宽主题词或加 --no-online 重试。"
                % _before)
    else:
        cochrane_count = None
        cochrane_total = None

    # ---- P0-C: relevance scoring (annotates merged works, incremental) ----
    works = score_relevance.score_works(works, topic=topic, keywords=keywords)

    # ---- 缓存命中 run 的纯计算节点本地化（2026-11-14）----
    # _cache_wrap 只包住各源检索 jobs；lit_prisma / lit_rrf 是「确定性规则、
    # 零 IO」的纯计算策略节点，即便 7 个源全部命中本地缓存，默认仍会各发
    # 1 次 Coze HTTP（其中 prisma 默认开启）。这是「重复需求请求数压不到 0」
    # 的最后一处放大点：结果完全来自缓存，云端不会产出任何新信息。
    # 条件与末尾 P2 的 _cache_only 同源（_n_jobs>0 且无 fresh fetch），
    # 独立开关 CT_LIT_PURE_LOCAL_ON_CACHE=0 可恢复云端优先（canary 比对用）。
    _pure_local_on_cache = (
        _n_jobs > 0 and not _fresh_fetches
        and os.environ.get("CT_LIT_PURE_LOCAL_ON_CACHE", "1") != "0"
    )

    # ---- P0-B: deterministic PRISMA title/abstract screen (no LLM) ----
    # 2026-11-04 B 类三项上移：coze lit_prisma 优先 + 本地末位兜底（红线 2）。
    prisma_block = None
    if prisma:
        _prisma_params = {
            "topic": topic, "review_type": review_type, "safety": safety,
            "duplicates_removed": dedup_stats["duplicates_removed"],
            "exclude_non_original": original_only, "require_types": only_type,
        }
        sp = _coze_prisma_screen(
            works, _prisma_params,
            local_fn=lambda: screen_prisma.screen(
                works, topic=topic, review_type=review_type, safety=safety,
                duplicates_removed=dedup_stats["duplicates_removed"],
                exclude_non_original=original_only, require_types=only_type),
            log_fn=_coze_log, prefer_local=_pure_local_on_cache)
        works = sp["works"]
        prisma_block = sp["prisma"]

    # ---- ranking ----
    if rank == "relevance":
        try:
            works = sorted(works, key=lambda w: -(float(w.get("relevance_score") or 0)))
        except Exception:
            pass
    elif rank == "rrf":
        # 跨源倒数排名融合：多源共识论文上浮，弥补单源 cited_by 偏差（架构韧性）
        # 2026-11-04 B 类三项上移：coze lit_rrf 优先（连 build_source_ranks
        # 一起上移，传同一时刻 payloads 快照），失败降级本地 rrf_fuse（红线 2）。
        try:
            works = _coze_rrf_fuse(
                works, _rrf_payloads_snapshot,
                local_fn=lambda: source_registry.rrf_fuse(works, _source_ranks),
                log_fn=_coze_log, prefer_local=_pure_local_on_cache)
        except Exception as _e:
            _out("[WARN] rrf 融合失败，回退 cited 排序: %s" % _e, "rrf_failed", error=str(_e))

    # ---- P0: citation verification (anti-hallucination, ct-base §17.1) ----
    # `all`: verification already ran concurrently with fetch above; attach + summarize.
    # `top`: verify only the top-N (ranked) works concurrently, leave the rest unverified.
    # `none`: skip verification entirely (preview-style annotation, no network).
    vsum = None
    if verify_mode == "all":
        verify_citations.attach_verifications(works, _verify_results)
        vsum = verify_citations.summarize_results(_verify_results)
        vsum["mode"] = "all"
        vsum["skipped_preview"] = False
        _out("[OK] citation verification (concurrent, all): %s"
             % json.dumps(vsum, ensure_ascii=False),
             "verify_done", mode="all", summary=vsum)
    elif verify_mode == "top":
        _tv, _skipped = _verify_top_n(works, verify_top_n,
                                      check_consistency=verify_consistency)
        verify_citations.attach_verifications(works, _tv)
        # mark works beyond the top-N as sampled-out (no network call)
        for _w in works[verify_top_n:]:
            _w.setdefault("citation_verified", False)
            _w.setdefault("citation_verify_status", "unverified_sampled")
            _w.setdefault("citation_verify_note",
                          "not verified (sampled out; --verify top N=%d)" % verify_top_n)
        vsum = verify_citations.summarize_results(_tv)
        vsum["unverified_sampled"] = _skipped
        vsum["total"] = len(works)
        vsum["mode"] = "top"
        vsum["top_n"] = verify_top_n
        vsum["skipped_preview"] = False
        _out("[OK] citation verification (top-%d, sampled %d): %s"
             % (verify_top_n, _skipped, json.dumps(vsum, ensure_ascii=False)),
             "verify_done", mode="top", top_n=verify_top_n,
             sampled=_skipped, summary=vsum)
    else:  # verify_mode == "background" — handled by the two-phase block below
        pass

    # ---- G: curated LOCAL guideline corpus (build-time populated by build_guidelines.py) ----
    # Independent of the literature works: kept OUT of normalize.merge so it does not
    # pollute citation verification / PRISMA. Reads a PINNED local corpus (references/
    # guidelines/guidelines_index.json) — ZERO network at analysis time. Emitted as
    # guidelines.json + a `guidelines` block in the merged state. To refresh/extend the
    # corpus, the author runs: python adapters/build_guidelines.py --topic <topic> --run
    guidelines_payload = None
    if with_guidelines:
        try:
            _gl_json = os.path.join(out_dir, "guidelines.json")
            guidelines_payload = guideline_corpus.load(
                _topic_zh, review_type=review_type,
                sources=(guideline_sources.strip() if guideline_sources else None),
                max_results=guideline_max, out=_gl_json,
                region=guidelines_region)
            # 既有缺陷修复（2026-11-02）：语料的 topic 字段是英文短词，而此处原先只传中文
            # 原文 → 中文主题恒 0 条（`--guidelines-region china` 因此也必然空转，
            # 看起来像"中国证据少"，实为匹配键语言/形态不一致）。0 命中时按候选词
            # 依次重试（英文检索式 → 各 OR 分支 → 最长词），仍 0 则如实报告，不编造。
            if not guidelines_payload.get("count"):
                for _gq in _guideline_topic_candidates(topic):
                    if not _gq or _gq == _topic_zh:
                        continue
                    _gl_retry = guideline_corpus.load(
                        _gq, review_type=review_type,
                        sources=(guideline_sources.strip() if guideline_sources else None),
                        max_results=guideline_max, out=None,
                        region=guidelines_region)
                    if _gl_retry.get("count"):
                        guidelines_payload = _gl_retry
                        with open(_gl_json, "w", encoding="utf-8") as _gf:
                            json.dump(_gl_retry, _gf, ensure_ascii=False, indent=2)
                        _out("[i18n] 指南语料按「%s」重试命中 %d 条"
                             % (_gq, _gl_retry["count"]),
                             "guidelines_i18n_retry", query=_gq,
                             count=_gl_retry["count"])
                        break
            if guidelines_payload.get("corpus_missing"):
                _out("[WARN] guideline corpus not built yet — run build_guidelines.py first",
                     "guidelines_missing",
                     note="python adapters/build_guidelines.py --topic %s --run" % _topic_zh)
            else:
                _out("[OK] guideline corpus loaded: %d records"
                     % guidelines_payload.get("count", 0),
                     "guidelines_done", count=guidelines_payload.get("count", 0),
                     source_status=guidelines_payload.get("source_status", {}))
        except Exception as _ge:
            _out("[WARN] guideline corpus load failed: %s" % _ge, "guidelines_failed",
                 error=str(_ge))

    # ---- build meta / evidence / exports (shared by all verify modes) ----
    def _finalize(works, vsum, suffix="", guidelines=None):
        """Render intermediate state + all exports for a given (works, vsum) pair.

        suffix=""            -> normal deliverables (lit_report.xlsx / lit_report.html)
        suffix="_verified"   -> verified refresh: lit_report_verified.xlsx + re-render
                                lit_report.html (overwrites the preview with the
                                verified version).
        Returns the primary deliverable path.
        """
        meta = {"topic": _topic_zh, "review_type": review_type,
                "year_from": year_from, "year_to": year_to, "safety": safety,
                "citation_style": citation_style if export_bib else None,
                "rank": rank, "keywords": keywords,
                "prisma": prisma_block,
                "verification": vsum,
                "with_prospero": with_prospero,
                "cochrane": cochrane,
                "cochrane_count": cochrane_count,
                "cochrane_total": cochrane_total,
                "source_notes": source_notes,
                "merge_existing": merge_stats,   # living-review delta (None when off)
                "concepts": _concepts,           # 组小学借鉴：结构化 PICO 概念（审计）
                "depth": depth,                  # 检索深度预算
                "imports": _import_stats or None,  # H/I：Zotero / 中文库导入留痕（审计）
                "search_topic": _search_topic}  # 实际检索式（含概念 AND 拼接）
        if _tp["translated"]:  # 中文→英文翻译信息（供报告展示与溯源）
            meta["topic_en"] = _tp["topic_en"]
            meta["topic_translated"] = True
            meta["topic_hits"] = _tp["hits"]
            meta["topic_untranslated"] = _tp["untranslated"]
        oa_status = http_utils.get_openalex_key_status()
        config = {
            "openalex_key": oa_status,
            "openalex_key_url": http_utils.OPENALEX_SIGNUP_URL,
            "semantic_scholar_key": "configured" if http_utils.load_s2_key() else "missing",
            "prospero_token": "configured" if (with_prospero and prospero_token) else (
                "missing" if with_prospero else "not_used"),
        }
        meta["config"] = config
        # 升级项 B：NCBI 车道状态入 meta（报告可呈现，避免「有没有跑备用腿」不可见）
        _pubmed_ran = any((p or {}).get("source") == "PubMed" for p in payloads)
        meta["pubmed"] = {
            "explicit": bool(with_pubmed),
            "fallback_enabled": bool(pubmed_fallback),
            "ran": bool(_pubmed_ran),
            "trigger": ("explicit" if with_pubmed else
                        ("fallback" if _pubmed_ran else "not_run")),
        }
        # 数据完整性标脏（fail-loud）：去重服务不可用时让报告显式呈现，
        # 避免「0 篇」被误读为「检索无结果」（2026-10-27）
        if _dedupe_unavailable:
            meta["data_integrity"] = {
                "dedupe_unavailable": True,
                "reason": dedup_stats.get("error"),
                "warning": "去重服务（coze lit_dedup）不可用，本次结果为空且不可信",
            }
        # 四态 ledger：显式关闭的源记为 skipped（not_run），其缺口诚实呈现、不归零
        _disabled = []
        if not with_europepmc:
            _disabled.append("EuropePMC")
        # 升级项 B：PubMed 默认不参与（与 Europe PMC 重复覆盖），只有显式
        # --with-pubmed 或 Europe PMC 故障触发 fallback 才会跑。没跑就如实记 skipped，
        # 跑了（无论显式还是补位）都不记——避免把「备用腿已补位」误报成「源缺口」。
        if not with_pubmed and not _pubmed_ran:
            _disabled.append("PubMed")
        if not with_semantic_scholar:
            _disabled.append("SemanticScholar")
        if not with_biorxiv:
            _disabled.append("bioRxiv")
        if not with_medrxiv:
            _disabled.append("medRxiv")
        if not with_arxiv:
            _disabled.append("arXiv")
        if not with_prospero:
            _disabled.append("PROSPERO")
        if not with_guidelines:
            _disabled.append("Guidelines")
        if not cochrane:
            _disabled.append("Cochrane")
        # ---- 升级项 G：段落级锚点（仅作用于本地已下载 PDF）-------------------
        # 溯源粒度 DOI 级 → 段落级（{doc_hash}:{page}-{block_index}）。缺失 PDF /
        # 扫描版无文本层一律如实计数，**绝不编造锚点**；失败不影响主报告产出。
        _anchor_stats = None
        if anchor:
            try:
                _anchor_stats = anchor_injector.attach(
                    works, pdf_dir=os.path.join(out_dir, "pdfs"))
                _out("[OK] 段落锚点：%d/%d 篇已锚定（blocks=%d · pdf_missing=%d · "
                     "no_text=%d · unavailable=%d）"
                     % (_anchor_stats["anchored"], _anchor_stats["total"],
                        _anchor_stats["blocks"], _anchor_stats["pdf_missing"],
                        _anchor_stats["no_text"], _anchor_stats["unavailable"]),
                     "anchors_done", **_anchor_stats)
            except Exception as _ae:
                _out("[WARN] 段落锚点生成失败（不影响报告）: %s" % _ae,
                     "anchors_failed", error=str(_ae))
        evidence = evidence_log.build_log(
            payloads, topic, meta, vsum, config=config, degraded=source_notes,
            disabled_sources=_disabled, concepts=_concepts,
            depth=depth, search_topic=_search_topic, anchors=_anchor_stats)
        ev_res = evidence_log.write_log(evidence, out_dir)
        meta["evidence_log"] = evidence
        _out("[OK] evidence_log -> %s / %s" % (ev_res["json"], ev_res["md"]),
             "evidence_log", json_path=ev_res["json"], md_path=ev_res["md"])
        if oa_status == "missing":
            _out("[WARN] OpenAlex ran in keyless mode — re-run with a configured key for full coverage.",
                 "warn", kind="keyless")
        out_data = {"count": len(works), "works": works}
        if guidelines is not None:
            out_data["guidelines"] = guidelines
            meta["guidelines"] = {
                "count": guidelines.get("count", 0),
                "total_sources": guidelines.get("total_sources"),
                "api_sources": guidelines.get("api_sources"),
                "portal_sources": guidelines.get("portal_sources"),
                "source_status": guidelines.get("source_status", {}),
            }
        if prisma_block:
            out_data["prisma"] = prisma_block
        out_data["evidence_log"] = evidence
        out_data["verification"] = vsum
        out_data["meta"] = meta  # topic / keywords / review_type / year span → HTML & XLSX headers
        with open(merged_json, "w", encoding="utf-8") as f:
            json.dump(out_data, f, ensure_ascii=False, indent=2)
        _out("[OK] intermediate state -> %s (hidden; reused by standalone tools)" % merged_json,
             "intermediate", path=merged_json)
        primary = None
        _ver = {"verified": bool(suffix)}
        # ---- DOI-focused audit artifact (--verify-dois; additive, network-free here) ----
        # The doi_* fields are populated by the verification pass above; this only
        # renders the human-review list. Guarded so a normal run is byte-identical.
        if verify_dois and run:
            try:
                _mis = verify_citations.collect_doi_mismatches(works)
                _rep = verify_citations.render_doi_mismatch_report(works, topic=_topic_zh)
                _mp = os.path.join(out_dir, "doi_mismatch%s.md" % suffix)
                with open(_mp, "w", encoding="utf-8") as _df:
                    _df.write(_rep)
                _out("[OK] doi mismatch report (%d flagged) -> %s" % (len(_mis), _mp),
                     "export_done", kind="doi_mismatch", path=_mp,
                     count=len(_mis), **_ver)
                if _mis:
                    _out("[TIP] DOI 存疑条目已单列，建议人工复核：%s" % _mp, "tip", **_ver)
            except Exception as _de:
                _out("[WARN] doi mismatch report failed: %s" % _de,
                     "export_failed", kind="doi_mismatch", error=str(_de), **_ver)
        if export_bib:
            try:
                fc = format_citations.export_citations(
                    {"count": len(works), "works": works}, style=citation_style,
                    out_dir=out_dir, lang="auto")
                _out("[OK] citations(%s) -> %s / %s" % (
                    citation_style, fc["bib_path"], fc["ris_path"]),
                    "export_done", kind="citations",
                    bib=fc["bib_path"], ris=fc["ris_path"], **_ver)
            except Exception as _ce:
                _out("[WARN] citation export failed: %s" % _ce,
                     "export_failed", kind="citations", error=str(_ce), **_ver)
        if make_xlsx:
            xlsx_out = os.path.join(out_dir, "lit_report%s.xlsx" % suffix)
            try:
                export_xlsx.export_workbook(
                    {"count": len(works), "works": works, "meta": meta},
                    xlsx_out, lang=lang, safety=safety)
                _out("[OK] xlsx  -> %s" % xlsx_out, "export_done", kind="xlsx",
                     path=xlsx_out, **_ver)
                primary = primary or xlsx_out
            except Exception as _xe:
                _out("[WARN] xlsx export failed: %s" % _xe,
                     "export_failed", kind="xlsx", error=str(_xe), **_ver)
        if make_html:
            html_out = os.path.join(out_dir, "lit_report.html")
            try:
                html_text = export_html.render(out_data, lang, safety=safety, report_first=report_first)
                with open(html_out, "w", encoding="utf-8") as f:
                    f.write(html_text)
                _out("[OK] html  -> %s" % html_out, "export_done", kind="html",
                     path=html_out, **_ver)
                primary = html_out
            except Exception as _he:
                _out("[WARN] html export failed: %s" % _he,
                     "export_failed", kind="html", error=str(_he), **_ver)
        # ---- 结果不足建议卡（2026-10-01 新增：结果太少时主动建议扩展检索）----
        _FEW_RESULTS_THRESHOLD = 10
        if len(works) <= _FEW_RESULTS_THRESHOLD:
            _suggestions = []
            if not snowball and not _sf_mode:
                _suggestions.append(i18n.t("suggest.snowball"))
            if not depth or depth == "quick":
                _suggestions.append(i18n.t("suggest.deep"))
            if not concepts:
                _suggestions.append(i18n.t("suggest.pico"))
            # 罕见病关键词启发式 → 建议专源
            _query_lower = (_search_topic or "").lower()
            if any(h in _query_lower for h in ("orphanet", "rare disease", "prevalence<", "prevalence <")):
                _suggestions.append(i18n.t("suggest.rare_disease"))
            if _suggestions:
                _out(i18n.t("suggest.few_results_prefix", n=len(works)), "suggest_few")
                for _s in _suggestions:
                    _out("  · " + _s, "suggest_item", suggestion=_s)
        # end-user guidance on optional add-ons (surfaced to the chat after the run)
        _out("[TIP] Excel 报告是完整结果，可在此基础上继续筛选 / 透视等进一步处理。", "tip", **_ver)
        if not export_bib:
            _out("[TIP] 如需 Zotero(RIS) / BibTeX / APA 等引文格式下载、或协助对 OA 文献下载 PDF，告诉我即可按需生成（也可用 --export-bib / --download-pdf）。附加功能不清楚时，对话中输入「菜单」让我列选。", "tip", **_ver)
        if obsidian:
            try:
                ob = obsidian_exporter.export_obsidian(
                    {"count": len(works), "works": works}, out_dir=out_dir, lang=lang)
                _out("[OK] obsidian notes=%d -> %s" % (ob["count"], ob["folder"]),
                     "export_done", kind="obsidian", count=ob["count"],
                     folder=ob["folder"], **_ver)
                _out("     moc -> %s" % ob["moc"], "export_done",
                     kind="obsidian_moc", path=ob["moc"], **_ver)
            except Exception as _oe:
                _out("[WARN] obsidian export failed: %s" % _oe,
                     "export_failed", kind="obsidian", error=str(_oe), **_ver)
        if zotero:
            try:
                zo = zotero_exporter.export_zotero(
                    {"count": len(works), "works": works}, out_dir=out_dir)
                _out("[OK] zotero csv/ris -> %s / %s" % (zo["csv"], zo["ris"]),
                     "export_done", kind="zotero", csv=zo["csv"], ris=zo["ris"], **_ver)
            except Exception as _ze:
                _out("[WARN] zotero export failed: %s" % _ze,
                     "export_failed", kind="zotero", error=str(_ze), **_ver)
        return primary

    # Two-phase (background) verification: fast unverified preview first, then a
    # verified refresh once the background verification workers finish. The user /
    # agent gets a usable report at fetch-time (~seconds) instead of waiting for the
    # full verification pass; verify_progress events keep streaming meanwhile.
    if verify_mode == "background":
        for _w in works:
            _w.setdefault("citation_verified", False)
            _w.setdefault("citation_verify_status", "pending_background")
            _w.setdefault("citation_verify_note",
                          "verification running in background (--verify background)")
        vsum_bg = {"total": len(works), "pending": len(works),
                   "skipped_preview": True, "mode": "background"}
        _out("[OK] background verification: fast unverified preview (results attach later)",
             "verify_mode", mode="background")
        primary = _finalize(works, vsum_bg, suffix="", guidelines=guidelines_payload)
        _out("[OK] report ready (unverified preview): %s" % primary,
             "report_ready", primary=primary or "")
        _drain_verifiers()
        verify_citations.attach_verifications(works, _verify_results)
        vsum = verify_citations.summarize_results(_verify_results)
        vsum["total"] = len(works)
        vsum["mode"] = "background"
        vsum["skipped_preview"] = False
        _out("[OK] citation verification (background): %s"
             % json.dumps(vsum, ensure_ascii=False),
             "verify_done", mode="background", summary=vsum)
        primary_v = _finalize(works, vsum, suffix="_verified", guidelines=guidelines_payload)
        _out("[OK] report verified -> %s" % primary_v,
             "report_verified", primary=primary_v or "")
        primary = primary_v or primary
    else:
        primary = _finalize(works, vsum, suffix="", guidelines=guidelines_payload)

    # ---- PDF 批量下载（opt-in via --download-pdf）----
    if download_pdf:
        try:
            from adapters.pdf_download import PdfDownloader
            pdf_dir = os.path.join(out_dir, "pdfs")
            # Excel 回写职责交给 PdfDownloader 自身：构造时传 xlsx_out，run() 结束即
            # 自动把 PDF 本地路径写回「PDF 本地路径」列。这样独立直驱 PdfDownloader
            # 的脚本（dl_top10.py / dl_latest40.py）只要同样传入 xlsx_out，就不会再
            # 漏写（用户 2026-09-08 加固：此前该步骤只在主流程内联，独立路径易漏）。
            _xlsx_out = os.path.join(out_dir, "lit_report.xlsx") if make_xlsx else None
            dl = PdfDownloader(out_dir=pdf_dir, merged_json=merged_json,
                               xlsx_out=_xlsx_out, lang=lang, safety=safety,
                               citations_out_dir=out_dir,
                               citation_style=citation_style,
                               use_scihub=use_scihub,
                               # request_id 透传到 publisher_pdf_batch 顶层信封，
                               # 让 Coze 端 feishu_write 对批量下载留痕同样可幂等去重。
                               request_id=_request_id,
                               progress=lambda m: _out(m, "pdf_download"))
            _out(f"[PDF] 开始批量下载 {len(works)} 篇文献的 PDF：每篇约需 10–20 秒"
                 f"（视网络与限流而定），请耐心等待完成，无需任何操作。")
            pdf_stats = dl.run(works)
            # run() 已自动回写 Excel（若构造时给了 xlsx_out），结果经 stats["xlsx_updated"] 透传
            _xlsx_updated = pdf_stats.get("xlsx_updated") or ""
            if pdf_stats.get("rejected"):
                # 总量超上限被拒：提示缩小范围（用户 2026-09-06：>50 直接拒绝避免超时）
                _out(f"[PDF] 拒绝下载 (elapsed {pdf_stats.get('elapsed_s', 0)}s): "
                     f"{pdf_stats.get('rejected_reason', '')}",
                     "pdf_download_rejected", reason=pdf_stats.get("rejected_reason", ""))
            else:
                # 耗时统计反馈（用户 2026-09-07：每次 PDF 下载都要报用时）
                _ok, _tot = pdf_stats.get("ok", 0), pdf_stats.get("total", 0)
                # 用户可读反馈：不倾倒技术性 JSON（stats 细节仅经 json 事件透传）
                _el = pdf_stats.get("elapsed_s")
                _base = f"[PDF] 下载完成: {_ok}/{_tot} 篇成功"
                if _el is not None:
                    _base += f"，用时 {_el}s（{pdf_stats.get('elapsed_min', 0)} 分钟）"
                # ⚠️ 红线（用户 2026-09-08）：结果面板只呈现标准产物（html/xlsx），
                # 绝不逐个打开 PDF——几十个 PDF 同时打开会卡死 UI。下载反馈只透传
                # 计数字段与「Excel 已回写」标志，**不泄漏任何 PDF 文件路径**；
                # 仅用纯文本告知用户共同保存目录 pdf_dir，由其自行打开。
                if _xlsx_updated:
                    _out(f"{_base}。PDF 已保存至 {pdf_dir}，Excel 报告「PDF 本地路径」列已更新。"
                         f"下载台账 pdf_manifest.csv（来源/状态/大小/页数/信任级）已生成于运行目录。"
                         f"结果面板不逐个打开 PDF，请到该目录查看。",
                         "pdf_download_done",
                         ok=_ok, total=_tot, elapsed_s=pdf_stats.get("elapsed_s"),
                         xlsx_updated=_xlsx_updated,
                         manifest_path=pdf_stats.get("manifest_path") or "")
                elif _ok > 0:
                    _out(f"{_base}。PDF 已保存至 {pdf_dir}。"
                         f"下载台账 pdf_manifest.csv 已生成于运行目录。"
                         f"结果面板不逐个打开 PDF，请到该目录查看。",
                         "pdf_download_done",
                         ok=_ok, total=_tot, elapsed_s=pdf_stats.get("elapsed_s"),
                         manifest_path=pdf_stats.get("manifest_path") or "")
                else:
                    _out(f"{_base}。未下载到可用 PDF（多为付费墙 / 无 OA 直链）。"
                         f"PDF 目录：{pdf_dir}。",
                         "pdf_download_done",
                         ok=_ok, total=_tot, elapsed_s=pdf_stats.get("elapsed_s"))
        except Exception as e:
            _out(f"[PDF] 批量下载失败: {type(e).__name__}: {e}", "pdf_download_failed", error=str(e))

    if online:
        # 最终汇总记一条飞书（log_feishu=True）：统计信息经 querystr 透传，
        # Coze 端飞书节点原样落 querystr 列，供审计追踪整次多源检索的汇总。
        # 🔴 汇总 payload 只放统计信息，**不携带版本字段**——§2.1（2026-09-17 定）：
        # skill_version / coze_version 唯一落点是飞书 resultstr，由 Coze 端写入。
        # ---- 2026-11-13 写放大治理 / 2026-11-14 口径修正（P2 + P3）----
        # P2：整次 run 全部命中本地缓存 → 未产生任何新检索，故不重复写全量
        #     A 汇总，但改发一条轻量 cache_hit 行，保证「每需求至少一条记录」。
        #     CT_LIT_LOG_ON_CACHE_HIT=1 可强制写全量 A 汇总（回退开关）。
        # P3：adapters.feishu_write_guard 按「业务载荷 + 时间窗」原子 claim，
        #     挡住同一次请求被触发两次造成的结构性双写（实测 40.6% / 日 50%）。
        #     两类 payload 共用同一稳定键白名单 → 首轮 A 汇总 claim 后，
        #     第二轮 cache_hit 被抑制，仍恒 1 行。
        #     指纹必须剔除 request_id：两次重复 run 各自 uuid4，含进去护栏失效。
        _cache_only = (_n_jobs > 0 and not _fresh_fetches
                       and os.environ.get("CT_LIT_LOG_ON_CACHE_HIT") != "1")
        _guard_payload = None
        try:
            # ---- 一次需求的完整审计上下文（2026-11-14 信息完备性修复）----
            # 旧版 A 类记录只有 6 个键：topic/query + sources_ok/fail/hits_merged
            # + type。实测 650 行里「检索参数」「答案/产物引用」「缓存信号」
            # 「结构化错误」四类关键字段覆盖率全为 0%，导致记录既无法复现
            # （不知道用了什么年份/筛选条件），也无法回溯结果（不知道给用户
            # 返回了什么），更无法验证本轮缓存/写放大治理的收益。
            # 以下字段全部为**纯增量**，不新增飞书列、不改 Coze 端契约。
            _p_ok = [p for p in payloads if isinstance(p, dict) and not p.get("error")]
            _p_fail = [p for p in payloads if isinstance(p, dict) and p.get("error")]
            _failed_sources = [str(p.get("source") or p.get("name") or "?")
                               for p in _p_fail]
            _run_params = {
                "year_from": year_from, "year_to": year_to,
                "date_from": date_from, "date_to": date_to,
                "review_type": review_type, "safety": bool(safety),
                "max_results": max_results, "cochrane": bool(cochrane),
                "include_reviews": include_reviews, "rank": rank,
                "prisma": bool(prisma), "verify_mode": verify_mode,
                "sources_enabled": [n for n, _ in jobs],
            }
            try:
                _answer_hash = hashlib.md5(json.dumps(
                    works, ensure_ascii=False, sort_keys=True,
                    default=str).encode("utf-8")).hexdigest()[:16]
            except Exception:
                _answer_hash = ""
            _summary_status = (
                "error" if (_p_fail and not _p_ok and not works) else
                "empty" if not works else
                "partial" if _p_fail else "ok")
            _summary_payload = {
                "type": "literature_summary",
                # call_type 显式落点（2026-11-13 修复）：让取数工具（feishu_log_fetch）
                # 能把「检索步」与「批量下载」两套 schema 拆开统计，不再混算稀释。
                "call_type": "literature_summary",
                "topic": _topic_zh,
                "query": topic,
                "sources_ok": len(_p_ok),
                "sources_fail": len(_p_fail),
                "sources_requested": _n_jobs,
                "sources_failed": _failed_sources,
                "hits_merged": len(works),
                # zero_hits 告警标记（2026-11-13 修复）：hits_merged==0 时置 true，
                # 既给取数工具明确的 warn 信号，也提示 Coze 端触发兜底（扩源/提示用户），
                # 避免用户静默拿到空摘要。
                "zero_hits": len(works) == 0,
                # ── 新增：检索可复现性 / 结果可回溯性 / 治理可观测性 ──
                "params": _run_params,
                "cache_hits": max(0, _n_jobs - len(_fresh_fetches)),
                "fresh_fetches": len(_fresh_fetches),
                "answer_hash": _answer_hash,
                "artifact_ref": os.path.basename(primary or ""),
                # log_only 由 Coze 端刻意不写 status（避免谎报 0 命中），
                # 故本地在 querystr 侧显式给出汇总状态与结构化错误码。
                "summary_status": _summary_status,
                "error_type": "source_fetch_failed" if _p_fail else "",
                "error_code": ("LIT_SRC_ALL_FAILED" if _p_fail and not _p_ok
                               else "LIT_SRC_PARTIAL" if _p_fail else ""),
                # request_id 透传（2026-11-13 修复）：便于取数工具 §6 按请求精确归因。
                "request_id": _request_id,
            }
            # mode="log_only"（2026-09-11）：本次调用**只要一条飞书留痕**，不要检索结果。
            # Coze 端 route_by_mode 据此直连 feishu_write 节点（跳过 search_node），
            # 因此不再为了一条汇总记录白跑一次真实 openalex 检索（省配额、不污染结果日志）。
            # log_only 隐含 force_coze=True（在 dispatch 内强制），保证配了 OpenAlex key
            # 的机器上也不会被「本地直连」早返回吞掉那条例外的留痕。
            # source/keyword 仅为兼容既有签名，log_only 下不产生任何检索。
            # 0.5.09 / 2026-11-14：恢复「每需求至少一条记录」，但缓存命中只写
            # **轻量 cache_hit 行**。不重复完整检索统计（首次需求那条 A 汇总
            # 已含），只保留四类必要信息：
            #   ① 稳定键（type/call_type/topic/query/params）→ P3 护栏仍能与
            #      首轮同请求去重，避免恢复留痕反而放大存储；
            #   ② 诊断口径必需键（hits_merged / sources_fail / zero_hits）→
            #      ct-update 的 literature_record_failures 不会因缺键把缓存命中
            #      误判成「检索零命中」；源成败一律取本次 run 的真实 _p_ok /
            #      _p_fail，**不硬编码「全成功」**——缓存里可能存着失败源，
            #      谎报 sources_fail=0 会让该次调用在诊断侧凭空变成健康记录；
            #   ③ 缓存治理观测键（cache_hits / fresh_fetches / answer_hash）；
            #   ④ 语义标记（cache_hit / served_from）。
            # type / call_type 保持 literature_summary：取数工具按 type 分桶，
            # 新增第三类会稀释 A 类统计，故用布尔标记区分即可。
            if _cache_only:
                _log_payload = {
                    "type": "literature_summary",
                    "call_type": "literature_summary",
                    "cache_hit": True,
                    "served_from": "local_cache",
                    "topic": _topic_zh,
                    "query": topic,
                    "params": _run_params,
                    # 0.5.09 复核修正（2026-11-14）：源成败必须与全量 A 汇总同口径，
                    # 取运行时真实的 _p_ok / _p_fail。缓存命中 ≠ 各源都成功：
                    # 缓存文件里可能存着带 error 的失败 payload，若硬写
                    # sources_ok=_n_jobs / sources_fail=0，ct-update 的
                    # literature_record_failures 会把这次调用判成完全健康。
                    "sources_ok": len(_p_ok),
                    "sources_fail": len(_p_fail),
                    "sources_requested": _n_jobs,
                    "sources_failed": _failed_sources,
                    "hits_merged": len(works),
                    "zero_hits": len(works) == 0,
                    "cache_hits": _n_jobs,
                    "fresh_fetches": 0,
                    "answer_hash": _answer_hash,
                    "summary_status": _summary_status,
                    "error_type": "source_fetch_failed" if _p_fail else "",
                    "error_code": ("LIT_SRC_ALL_FAILED" if _p_fail and not _p_ok
                                   else "LIT_SRC_PARTIAL" if _p_fail else ""),
                    "request_id": _request_id,
                }
                _log_event = "feishu_summary_cache_hit"
            else:
                _log_payload = _summary_payload
                _log_event = "feishu_summary"

            # 🔴 护栏指纹必须只用「两轮重复 run 必然相同」的稳定键。
            # 2026-11-14 补全信息后，_summary_payload 新增了 cache_hits /
            # fresh_fetches / artifact_ref / answer_hash 等：第一轮全未命中
            # （fresh=7），第二轮全命中（fresh=0）；产物 basename 也可能因
            # out_dir 带时间戳而不同。若沿用旧的「全量减 request_id」，
            # 两次 run 指纹不同 → P3 护栏失效 → 40.6% 结构性双写复发。
            # 稳定键 = 用户输入（topic/query）+ 检索参数（params）+ 常量；
            # 两类 payload 都带这 5 个键且取值相同，故 cache_hit 行同样受
            # 护栏覆盖：首轮 A 汇总 claim 后，第二轮 cache_hit 被抑制。
            _GUARD_STABLE_KEYS = ("type", "call_type", "topic", "query", "params")
            _guard_payload = json.dumps(
                {k: _log_payload[k] for k in _GUARD_STABLE_KEYS
                 if k in _log_payload},
                ensure_ascii=False, sort_keys=True)
            from adapters import feishu_write_guard
            _allowed, _reason = feishu_write_guard.claim(
                _guard_payload, skillname="ct-literature")
            if not _allowed:
                _out(None, "feishu_summary_skipped_duplicate", reason=_reason,
                     call_type=_log_payload.get("call_type"))
            else:
                coze_dispatch("openalex", topic, year_from, year_to, max_results,
                              run=True, log_feishu=True, force_coze=True, mode="log_only",
                              # 2026-11-15：留痕载荷显式带 mode=log_only。
                              # 该行只是审计留痕、**不做检索**，若 hits_merged 因任何
                              # 原因落 0，取数侧会把它误判成「检索零命中」（实测 14 条
                              # 误报全部出自缺此标记的老版极简载荷）。显式标记后，
                              # ct-update 的判定可据此直接排除，不必靠字段完整度猜。
                              querystr=json.dumps({**_log_payload, "mode": "log_only"},
                                                  ensure_ascii=False),
                              skillname="ct-literature", request_id=_request_id)
                # 飞书留痕对用户静默（审计后台可见即可）；仅 json 事件流保留供 agent 诊断
                _out(None, _log_event,
                     cache_hits=_log_payload.get("cache_hits"),
                     fresh_fetches=_log_payload.get("fresh_fetches"))
        except Exception as e:
            # 写入失败 → 撤销 claim 登记，允许时间窗内重试（否则该请求彻底无留痕）
            if _guard_payload is not None:
                try:
                    from adapters import feishu_write_guard
                    feishu_write_guard.release(_guard_payload, skillname="ct-literature")
                except Exception:
                    pass
            _out(None, "feishu_summary_failed", error=str(e))

    _out("[OK] run finished: %s" % primary, "run_done", primary=primary or "")
    return primary


def main():
    ap = argparse.ArgumentParser(description="ct-literature pipeline (public literature search).")
    # v1.5.3：--reconcile-manual 独立模式不需要 --topic，故 required 改由下方手动校验
    ap.add_argument("--topic", required=False, default=None, help="free-text topic / drug / disease")
    ap.add_argument("--topic-en", dest="topic_en", default=None,
                    help="explicit English search term; when set, auto-translation is skipped")
    ap.add_argument("--review-type", default="all",
                    choices=["all", "systematic-review", "scoping-review",
                             "meta-analysis", "rct", "case-report"])
    ap.add_argument("--year-from", type=int, help="lower bound publication year")
    ap.add_argument("--year-to", type=int, help="upper bound publication year")
    ap.add_argument("--date-from", default=None, metavar="YYYY-MM-DD",
                    help="精确发表日期下界（月份级过滤）；与 --year-from 二选一，优先于年份级")
    ap.add_argument("--date-to", default=None, metavar="YYYY-MM-DD",
                    help="精确发表日期上界（默认今天）；与 --date-from 配合做窗口过滤")
    ap.add_argument("--recent-months", type=int, default=None, metavar="N",
                    help="便捷开关：仅检索最近 N 个月（≈今天-N*30天 起）；当 --date-from 缺省时生效")
    ap.add_argument("--safety", action="store_true",
                    help="safety / CSM bias (AE, toxicity, case report, PV)")
    ap.add_argument("--max", type=int, default=50, help="max works per source")
    ap.add_argument("--with-europepmc", action=argparse.BooleanOptionalAction, default=True,
                    help="search Europe PMC (MEDLINE/MeSH, biomedical precision); default ON; "
                         "use --no-with-europepmc to disable")
    ap.add_argument("--with-pubmed", action=argparse.BooleanOptionalAction, default=False,
                    help="search NCBI E-utilities (PubMed/MEDLINE + Cochrane CDSR) as an "
                         "independent lane; default OFF (Europe PMC already covers both). "
                         "Use --with-pubmed to force it on, or rely on the automatic "
                         "fallback below.")
    ap.add_argument("--pubmed-fallback", action=argparse.BooleanOptionalAction, default=True,
                    help="auto-enable the NCBI PubMed lane when the Europe PMC leg fails "
                         "(exception or 0 hits); default ON — this is the backup plan for "
                         "Europe PMC rate-limiting/outage, restoring both PubMed/MEDLINE and "
                         "Cochrane CDSR coverage. Use --no-pubmed-fallback to disable.")
    ap.add_argument("--with-semantic-scholar", action="store_true",
                    help="(low-priority supplementary source) search via Semantic Scholar "
                         "(citation-ranked); its API key requires a manual form review and is "
                         "not auto-issued, so it auto-skips when absent and never affects the "
                         "OpenAlex / Europe PMC primary output")
    ap.add_argument("--with-biorxiv", action=argparse.BooleanOptionalAction, default=True,
                    help="include bioRxiv preprints (biomedical preprints, via Europe PMC PPR index); "
                         "default ON; use --no-with-biorxiv to disable")
    ap.add_argument("--with-medrxiv", action=argparse.BooleanOptionalAction, default=True,
                    help="include medRxiv preprints (medical/clinical preprints, via Europe PMC PPR index); "
                         "default ON; use --no-with-medrxiv to disable")
    ap.add_argument("--with-arxiv", action="store_true",
                    help="include arXiv (physics/CS/ML methodology breadth; opt-in supplementary)")
    ap.add_argument("--no-preprint-fallback", action="store_true",
                    help="禁用预印本候选回退（默认开启：非 OA 文献自动按标题检索 "
                         "bioRxiv/medRxiv/arXiv 预印本候选，经作者姓氏同篇校验后标注到 "
                         "XLSX/HTML 的 'Preprint candidate' 列，并在下载期为付费墙文献 "
                         "回退下载免费预印本/OA 直链）；用本开关可关闭。")
    # 兼容项：旧版 server 可能发射 --preprint-fallback（意图「开启」）。
    # 回退默认即开启，故此处仅作无害接受（不产生任何副作用），
    # 防止遗留调用方触发 argparse "unrecognized arguments" 崩溃。
    ap.add_argument("--preprint-fallback", action="store_true",
                    help=argparse.SUPPRESS)
    ap.add_argument("--cochrane", action="store_true",
                    help="(focus) restrict the Europe PMC leg to the Cochrane Database of "
                         "Systematic Reviews via a verified journal filter, then keep only "
                         "Cochrane works after merge — a clean Cochrane-only retrieval. "
                         "Pairs with meta-analysis's in-skill dedup probe (same filter string).")
    # ---- source selection: comma-separated subset that OVERRIDES the --with-* flags ----
    # 供 meta-analysis A1 选题阶段的「检索数据源」修订直接消费（tool_card params.sources
    # → --sources）。canonical 名与 fetch_coze_unified._SOURCE_DISPLAY 一致。
    ap.add_argument("--sources", default=None,
                    help="comma-separated subset of sources to search; when set it OVERRIDES "
                         "the individual --with-* defaults (a source is enabled iff listed). "
                         "Names: OpenAlex, EuropePMC, PubMed, bioRxiv, medRxiv, "
                         "SemanticScholar, arXiv, PROSPERO, Guidelines, Cochrane. NOTE: "
                         "OpenAlex is the pipeline base and is always enabled — it cannot be "
                         "switched off. NOTE: 'PubMed' selects the NCBI E-utilities lane "
                         "directly; before the lane existed it aliased to EuropePMC (which "
                         "still covers PubMed/MEDLINE) — use 'EuropePMC' for that leg.")
    # ---- P1: PROSPERO systematic-review registry (opt-in, key-gated, UNVERIFIED) ----
    ap.add_argument("--with-prospero", action="store_true",
                    help="(P1, supplementary) include PROSPERO systematic-review registry "
                         "hits (duplication-avoidance / protocol discovery). Requires an API "
                         "token; currently key-gated + UNVERIFIED (the public REST API auth "
                         "header is undocumented) — degrades to a no-op skip when no token.")
    ap.add_argument("--prospero-token", default=os.environ.get("PROSPERO_API_TOKEN"),
                    help="PROSPERO API token (env PROSPERO_API_TOKEN). Required for --with-prospero.")
    ap.add_argument("--prospero-header", default="PROSPERO-ACCESS-TOKEN",
                    help="header name carrying the PROSPERO token (default: "
                         "PROSPERO-ACCESS-TOKEN; override if the real header differs)")
    # ---- G: curated LOCAL guideline corpus (build-time populated by build_guidelines.py) ----
    ap.add_argument("--with-guidelines", action=argparse.BooleanOptionalAction,
                    default=False,
                    help="(G) load the CURATED LOCAL guideline corpus (references/guidelines/"
                         "guidelines_index.json) — ZERO network at analysis time. The corpus is "
                         "built/refreshed by the author via: python adapters/build_guidelines.py "
                         "--topic <topic> --run. Emits guidelines.json + a `guidelines` block in "
                         ".merged.json. Opt-in (use --no-with-guidelines to disable).")
    ap.add_argument("--guideline-sources", default=None,
                    help="comma-separated subset of guideline sources (default: all 12+)")
    ap.add_argument("--guideline-max", type=int, default=20,
                    help="max records per live api source (default 20)")
    # ---- I: 指南证据车道区域（升级项 I，2026-11-02）----
    ap.add_argument("--guidelines-region", dest="guidelines_region", default=None,
                    choices=["china", "global", "both"],
                    help="(I) guideline evidence lane by region: china = CDE/NMPA 中国向语料; "
                         "global = 非中国监管语料; both/不传 = 不过滤（向后兼容）。"
                         "配合 --with-guidelines 生效，语料中无 region 字段的条目按 global 处理。")
    # ---- H: Zotero 本地库导入（升级项 H，2026-11-02）----
    ap.add_argument("--zotero-import", dest="zotero_import", default=None, metavar="COLLECTION",
                    help="(H) import a LOCAL Zotero collection as an extra source, read-only via "
                         "the Zotero local API (no API key, MCP-free). COLLECTION is a path like "
                         "'肿瘤/NSCLC' (use adapters/zotero_import.py --list to see paths). "
                         "Requires Zotero 7 → 设置→高级→允许本机应用通信.")
    # ---- I: 中文库导入槽（升级项 I，2026-11-02）----
    ap.add_argument("--merge-cn", dest="merge_cn", action="append", default=None,
                    metavar="EXPORT_FILE",
                    help="(I) merge a USER-EXPORTED Chinese-database file (RIS or JSON, exported "
                         "from CNKI / WanFang / SinoMed under the user's own institutional access). "
                         "Repeatable. Pure offline import — NO crawling, NO site access. "
                         "Source name is inferred from the filename or pass --merge-cn-source.")
    ap.add_argument("--merge-cn-source", dest="merge_cn_source", default=None,
                    choices=["CNKI", "WanFang", "SinoMed", "VIP"],
                    help="explicit source name for --merge-cn files whose filename gives no hint")
    # ---- G: 段落级锚点（升级项 G，2026-11-02）----
    ap.add_argument("--anchor", action="store_true",
                    help="(G) inject paragraph-level Block ID anchors into local PDFs "
                         "(out/pdfs) so evidence provenance drops from DOI-level to "
                         "paragraph-level. Pure local; entries without a PDF are reported "
                         "as pdf_missing, never faked.")
    ap.add_argument("--run", action="store_true", help="execute network requests")
    ap.add_argument("--no-xlsx", action="store_true",
                    help="skip Excel (.xlsx) export (default: auto-generate)")
    ap.add_argument("--no-html", action="store_true",
                    help="skip standalone HTML report (default: auto-generate)")
    ap.add_argument("--out-dir", default="./out")
    ap.add_argument("--openalex-key", default=http_utils.load_openalex_key(),
                    help="OpenAlex API key (Bearer). Auto-loaded from env OPENALEX_API_KEY "
                         "or skill .env. Free key lifts rate limit 100 -> 100k credits/day.")
    # ---- P0 new flags ----
    ap.add_argument("--citation-style", default=DEFAULT_CITATION_STYLE,
                    choices=format_citations.STYLES,
                    help="citation style for references export (default: apa)")
    ap.add_argument("--export-bib", action=argparse.BooleanOptionalAction,
                    default=DEFAULT_EXPORT_BIB,
                    help="export references.bib / references.ris / references_<style>.md "
                         "(default: off — HTML + Excel are the standard deliverables; "
                         "enable for Zotero RIS / BibTeX / APA downloads)")
    ap.add_argument("--prisma", action=argparse.BooleanOptionalAction,
                    default=DEFAULT_PRISMA,
                    help="run deterministic PRISMA title/abstract screen + funnel "
                         "(default: on; use --no-prisma to disable)")
    ap.add_argument("--rank", default=DEFAULT_RANK, choices=["cited", "relevance", "rrf"],
                    help="order works by cited_by_count (default) or relevance_score")
    ap.add_argument("--dedupe-engine", default="v1", choices=["v1", "v2"],
                    help="多源去重引擎：v1=仅 DOI/标题精确匹配（兼容老版本）；"
                         "v2=多标识归一（DOI/PMID/PMCID/arXiv）+ 传递闭包 + 模糊标题匹配")
    ap.add_argument("--keywords", default=None,
                    help="comma-separated extra keywords for relevance scoring")
    # ---- 组小学借鉴：检索结构模型（P0/P1，2026-09-30）----
    ap.add_argument("--depth", default=DEFAULT_DEPTH,
                    choices=list(DEPTH_PRESETS.keys()) + [None],
                    help="检索深度预算（非证据质量评级）：quick=快速定位/标准/广覆盖。"
                         "决定每源上限与是否触发弱化结果救援；不传则沿用 --max 旧语义")
    ap.add_argument("--concept", action="append", default=[], metavar="TYPE=VALUE",
                    help="结构化 PICO 概念（可重复），TYPE∈{%s}；如 "
                         "--concept intervention=osimertinib --concept comparator=chemotherapy "
                         "--concept outcome=overall-survival。概念 AND 拼入检索式、独立成轴，"
                         "并做 MeSH 归一化审计（mapping_status 入证据溯源日志）"
                         % ", ".join(sorted(CONCEPT_TYPES)))
    # ---- P0: citation verification scope (anti-hallucination, ct-base §17.1) ----
    # NOTE: `none` was removed on purpose — the verification gate is a hard P0 control and
    # must never be fully disabled from the CLI. Lowest selectable scope is `top`.
    ap.add_argument("--verify", default="all", choices=["all", "top", "background"],
                    help="citation verification scope (anti-hallucination, ct-base §17.1 — "
                         "cannot be fully disabled): all = verify every work (default); "
                         "top = verify only the top-N by rank (fastest, good for large result "
                         "sets); background = two-phase: emit an unverified report immediately, "
                         "then re-render with verification results when the background pass "
                         "finishes. All modes skip re-resolution of identifiers already trusted "
                         "by provenance.")
    ap.add_argument("--verify-top-n", type=int, default=15,
                    help="N for --verify top (default 15): how many top-ranked works get the "
                         "full check. This does NOT disable verification — it only sizes the "
                         "top-N sample under --verify top; identifier resolution still runs.")
    ap.add_argument("--no-consistency", action="store_true",
                    help="skip the title/author consistency cross-check (identifier still "
                         "resolved, but not compared against the resolved paper's metadata). "
                         "⚠️ WARNING: weakens the anti-hallucination guarantee; debugging only.")
    ap.add_argument("--verify-dois", action="store_true",
                    help="add a DOI-focused audit pass: write doi_verified / doi_mismatch onto "
                         "each work and emit doi_mismatch.md (a human-review list of DOIs that "
                         "resolve to a different paper / are malformed). Off by default; needs "
                         "--run. Standalone equivalent: scripts/verify_dois.py.")
    # ---- F: literature-manager integration ----
    ap.add_argument("--obsidian", action="store_true",
                    help="export Obsidian notes (per-paper .md + MOC index, "
                         "internal [[links]]); writes <out-dir>/obsidian/")
    ap.add_argument("--zotero", action="store_true",
                    help="export Zotero-importable zotero.csv + zotero.ris into <out-dir>/")
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "en"],
                    help="UI language for xlsx / html / markdown / obsidian outputs. "
                         "auto = CT_LITERATURE_LANG / config / default zh (never the "
                         "server OS locale, which is en_US in the published workbench); "
                         "force en for an English deliverable.")
    # ---- G: cross-run incremental merge (living review / surveillance) ----
    ap.add_argument("--merge-existing", default=None, metavar="MERGED_JSON",
                    help="(living review) path to a PREVIOUS run's .merged.json: this "
                         "run's works are UNIONed with that history and every record is "
                         "stamped first_seen / last_seen. Records seen before keep their "
                         "earliest first_seen and get a refreshed last_seen; records only "
                         "in history are retained (last_seen NOT refreshed, "
                         "seen_this_run=false) so the evidence base can only grow. "
                         "Reads the local file only — ZERO network. Off by default.")
    ap.add_argument("--stamp-date", default=None, metavar="YYYY-MM-DD",
                    help="date stamp for --merge-existing first_seen / last_seen "
                         "(default: today). Useful for backfilling a historical run.")
    ap.add_argument("--download-pdf", action="store_true",
                    help="(opt-in) 检索完成后进入 PDF 批量下载流程：OA 直链/预印本直接下载，"
                         "其余经 coze 批量下载节点处理（直下探测→浏览器+S3，支持二次重试）")
    ap.add_argument("--include-reviews", action=argparse.BooleanOptionalAction,
                    default=True,
                    help="include review-type publications in results (default: on; "
                         "use --no-include-reviews to exclude at the source and save quota)")
    ap.add_argument("--original-only", action="store_true",
                    help="只要原创研究：PRISMA 初筛用 doc-type 甄别排除"
                         " review/guideline/protocol（标题/摘要级规则）")
    ap.add_argument("--only-type", dest="only_type", default=None,
                    metavar="TYPES",
                    help="只要指定文献类型（反向模式，--original-only 的泛化），"
                         "逗号分隔：original/review/guideline/protocol。"
                         "例：--only-type review（只收综述）；"
                         "--only-type guideline,protocol。注意：无信号记录也会被排除")
    ap.add_argument("--online", action="store_true",
                    help="(默认已开启，保留兼容 no-op) 使用 Coze 端统一检索（6 个文献源走 Coze "
                         "服务端）；Coze 不可用时自动降级本地 fetch")
    ap.add_argument("--no-cache", dest="no_cache", action="store_true",
                    help="停用本地搜索缓存（本次运行不读不写；默认开，TTL 24h，"
                         "同检索条件直接复用上次 per-source payload 以省 Coze 配额）")
    ap.add_argument("--cache-ttl", dest="cache_ttl", type=int, default=None,
                    metavar="SECONDS",
                    help="本地搜索缓存 TTL 秒数（默认 24h；也可用环境变量 CT_LIT_CACHE_TTL）")
    ap.add_argument("--use-scihub", dest="use_scihub", action="store_true",
                    help="⚠️ Sci-Hub 最后兑底（默认关闭）：仅当 OA/预印本/coze 全部失败后"
                         "经 Sci-Hub 镜像解析 PDF。法律与合规风险用户后果自负，"
                         "机构环境（GCP/申办方项目）严禁开启；也可用环境变量 "
                         "CT_LIT_ALLOW_SCIHUB=1 开启")
    ap.add_argument("--local", action="store_true",
                    help="显式本地直连各源公共 API，不经 Coze 端点（即 2026-09-08 之前的默认行为）")
    ap.add_argument("--offline", action="store_true",
                    help="强制本地兜底（不调 Coze），与老版本行为完全一致；优先级高于 --local")
    ap.add_argument("--health-reset", dest="health_reset", action="store_true",
                    help="清空跨源熔断状态（source_registry 持久化的 health.json），"
                         "强制下次检索重新试探 Coze 端点（端点已恢复时用于解除降级）")
    ap.add_argument("--from-pack", dest="from_pack", default=None, metavar="FILE",
                    help="从批量打包预取结果加载（batch_lib --pack 模式产出的 "
                         "pack_payloads.json：dispatch 同构的 source payload 列表）。"
                         "这些源跳过检索，其余源按原路由执行（openalex 有 key 仍走本地 "
                         "keyed pool；semantic_scholar 仍本地优先）")
    ap.add_argument("--no-online-translate", dest="online_translate", action="store_false",
                    default=True,
                    help="关闭联网翻译兜底（默认开启：本地词典 miss 时调 ct-base kw_localize "
                         "兜底；CT_TRANSLATE_ONLINE=0 也可关闭）")
    ap.add_argument("--progress", default="human", choices=["human", "json"],
                    help="progress output mode: human (readable console, default) or "
                         "json (NDJSON event stream on stdout — run_start / source_done / "
                         "source_failed / fetch_done / verify_done / export_done; for agent use)")
    # U1: snowball (citation-network expansion via OpenAlex references / cited_by)
    ap.add_argument("--snowball", action="store_true",
                    help="expand top-seed works via OpenAlex citation network (1-hop "
                         "references + cited_by); adds related papers that keyword search misses")
    ap.add_argument("--snowball-max", type=int, default=10,
                    help="max citation-network works per seed (default 10, max 50)")
    ap.add_argument("--snowball-seeds", type=int, default=3,
                    help="top-N seed works to snowball from (default 3)")
    # U1b: snowball_from — 从指定文献（DOI/PMID/题名）出发的引文网络扩展
    ap.add_argument("--snowball-from", dest="snowball_from", default=None,
                    metavar="DOI/PMID/TITLE",
                    help="从指定文献出发做前后向引文网络扩展（OpenAlex references + cited_by "
                         "两跳）：给定 DOI / PMID / 题名，解析为 OpenAlex 文献后扩展其参考文献与"
                         "施引文献。聚焦模式：跳过关键词检索，仅输出该文献的引文网络（--expand 为其别名）")
    ap.add_argument("--expand", dest="snowball_from", metavar="DOI/PMID/TITLE",
                    help="--snowball-from 的别名（citation expand / snowball from <seed>）")
    # U3: interactive mode (lit-search inspired: pause for user confirmation at key stages)
    ap.add_argument("--interactive", action="store_true",
                    help="pause for user confirmation before search strategy and after screening "
                         "(lit-search Phase 0/2 inspired)")
    # U7: report-first mode (tooluniverse-drug-research inspired: build report skeleton first,
    # fill evidence incrementally so the user sees the report grow instead of waiting)
    ap.add_argument("--report-first", action="store_true",
                    help="Report-first mode: emit a skeleton HTML report immediately, then "
                         "re-render incrementally as evidence fills in (works -> verification). "
                         "Gives the user/agent visible progress during a long run.")
    ap.add_argument("--reconcile-manual", dest="reconcile_manual", metavar="OUT_DIR",
                    default=None,
                    help="手动回传归位（v1.5.3，独立模式）：扫描 <OUT_DIR>/pdfs/manual_incoming/ "
                         "下用户用机构权限手动下载的 PDF，按 DOI（文件名/正文）匹配并归位到 "
                         "<OUT_DIR>/pdfs/ 标准命名，回写 .merged.json（信任级：高·机构权限）。"
                         "配合 --download-pdf 运行末导出的 needs_manual.csv 使用，"
                         "合法合规，优先于 Sci-Hub 兑底")
    # A1: Meta-analysis 选题评估（接真实检索产出 → spec → 引擎，opt-in 灰度）
    ap.add_argument("--meta-topic-eval", dest="meta_topic_eval", action="store_true",
                    help="(opt-in) 检索完成后把 --cochrane meta 列表 + coverage + 异质性存根"
                         "结构化为 meta_topic_spec.json（SAFE PREVIEW，不跑引擎；"
                         "待 LLM 填充 overlap_axes / 临床-指南缺口后手动跑引擎）")
    ap.add_argument("--meta-topic-eval-run", dest="meta_topic_eval_run", action="store_true",
                    help="(opt-in) 同上并直接运行 meta-analysis 选题评估引擎，"
                         "产出 meta_topic_eval.json/.md（需先 --run 完成检索）")
    args = ap.parse_args()

    # ---- --reconcile-manual：独立模式，不跑检索 ----
    if args.reconcile_manual:
        from adapters.manual_reconcile import reconcile_from_merged
        _rd = os.path.normpath(args.reconcile_manual)
        if not os.path.isdir(_rd):
            print(f"[ERROR] OUT_DIR 不存在: {_rd}", file=sys.stderr)
            return 2
        _st, _mp = reconcile_from_merged(_rd, log=lambda m: print(m))
        if not _mp:
            print(f"[ERROR] 未找到 {_rd}/.merged.json —— 先跑一次 --download-pdf 检索下载",
                  file=sys.stderr)
            return 2
        print(f"[DONE] incoming={_st.get('incoming', 0)} matched={_st.get('matched', 0)} "
              f"unmatched={_st.get('unmatched', 0)} invalid={_st.get('invalid', 0)} "
              f"no_doi={_st.get('no_doi', 0)}")
        return 0
    # snowball_from 聚焦模式可独立运行（无需关键词主题）；否则 --topic 必填。
    if not args.topic and not args.snowball_from:
        ap.error("--topic is required (除非使用 --snowball-from / --reconcile-manual 独立模式)")

    # ---- 组小学借鉴：解析结构化概念 + 深度预算（P0/P1，2026-09-30）----
    _concepts, _concept_errs = _parse_concepts(args.concept)
    for _ce in _concept_errs:
        print("[WARN] --concept 解析: %s" % _ce, file=sys.stderr)
    # 深度预算覆盖 --max 默认值（若用户显式传 --max 则以 --max 为准）
    _depth = args.depth
    _max = args.max
    _rescue = False
    if _depth:
        _preset = DEPTH_PRESETS[_depth]
        _rescue = _preset["rescue"]
        # 仅当用户未显式改 --max 时用预设上限（argparse 默认 50 === 旧默认，视为未改）
        if args.max == 50:
            _max = _preset["max"]
    if _concept_errs:
        _out("[note] 存在非法 --concept，已跳过；其余概念仍生效", "note", kind="concept_err")

    # ---- --sources: comma-separated subset that OVERRIDES the --with-* / --cochrane flags ----
    # Consumed by meta-analysis A1 topic-selection revisions (tool_card params.sources →
    # --sources). A source is enabled iff listed. OpenAlex is the pipeline base and
    # run() enables it unconditionally, so it can never be switched off (warn if omitted).
    if args.sources:
        # 升级项 B：pubmed 不再别名到 europepmc。此前 PubMed 只能经 Europe PMC 到达，
        # 故把 pubmed 映射到 europepmc；现在 NCBI E-utilities 是独立车道，
        # 写 pubmed 就该真的走 NCBI（要 Europe PMC 那条腿请显式写 europepmc）。
        _ALIAS = {"openalex": "openalex", "europepmc": "europepmc", "pubmed": "pubmed",
                  "ncbi": "pubmed", "medline": "pubmed",
                  "biorxiv": "biorxiv", "medrxiv": "medrxiv",
                  "semanticscholar": "semantic_scholar", "arxiv": "arxiv",
                  "prospero": "prospero", "guidelines": "guidelines", "cochrane": "cochrane"}
        _sel, _unknown = set(), []
        for _raw in (s for s in args.sources.split(",") if s.strip()):
            _k = _ALIAS.get(_raw.strip().lower().replace(" ", "").replace("_", "").replace("-", ""))
            if _k is None:
                _unknown.append(_raw.strip())
            else:
                _sel.add(_k)
        if _unknown:
            raise SystemExit(
                "[ERROR] unknown --sources: %s\n        known: OpenAlex, EuropePMC, "
                "PubMed, bioRxiv, medRxiv, SemanticScholar, arXiv, PROSPERO, "
                "Guidelines, Cochrane"
                % ", ".join(_unknown))
        if "openalex" not in _sel:
            print("[warn] OpenAlex is the pipeline base and is always enabled; "
                  "--sources cannot disable it.", file=sys.stderr)
        args.with_europepmc = "europepmc" in _sel
        args.with_pubmed = "pubmed" in _sel
        args.with_biorxiv = "biorxiv" in _sel
        args.with_medrxiv = "medrxiv" in _sel
        args.with_semantic_scholar = "semantic_scholar" in _sel
        args.with_arxiv = "arxiv" in _sel
        args.with_prospero = "prospero" in _sel
        args.with_guidelines = "guidelines" in _sel
        args.cochrane = "cochrane" in _sel

    global _PROGRESS, _ORIG_STDOUT
    _PROGRESS = args.progress
    if args.progress == "json":
        # 子模块（fetch/report 等）的进度 print 全部转 stderr，stdout 只留 NDJSON 事件流
        _ORIG_STDOUT = sys.stdout
        sys.stdout = sys.stderr

    # ---- 路线 B：月份级日期窗口（--recent-months 折算 date_from/date_to）----
    date_from, date_to = args.date_from, args.date_to
    if args.recent_months:
        if args.recent_months <= 0:
            print("[ERROR] --recent-months 必须为正整数", file=sys.stderr)
            sys.exit(2)
        date_to = date_to or datetime.now().date().isoformat()
        date_from = date_from or (datetime.now() - timedelta(days=30 * args.recent_months)).date().isoformat()
    for _ds, _name in ((date_from, "--date-from"), (date_to, "--date-to")):
        if _ds:
            try:
                datetime.strptime(_ds, "%Y-%m-%d")
            except ValueError:
                print("[ERROR] %s 格式须为 YYYY-MM-DD: %r" % (_name, _ds), file=sys.stderr)
                sys.exit(2)

    if not args.run:
        # A1: 选题评估需先完成检索（--run）；PREVIEW 模式仅给提示，不执行
        if getattr(args, "meta_topic_eval", False) or getattr(args, "meta_topic_eval_run", False):
            print("[note] --meta-topic-eval / --meta-topic-eval-run 需先完成检索（--run）。"
                  "当前 PREVIEW 模式未执行选题评估；请加 --run 重跑检索后自动触发。",
                  file=sys.stderr)
        extra = []
        if args.with_europepmc:
            extra.append("EuropePMC")
        if args.with_pubmed:
            extra.append("PubMed(NCBI)")
        elif args.pubmed_fallback:
            extra.append("PubMed(fallback-if-EPMC-down)")
        if args.with_semantic_scholar:
            extra.append("SemanticScholar")
        if args.with_biorxiv:
            extra.append("bioRxiv")
        if args.with_medrxiv:
            extra.append("medRxiv")
        if args.with_arxiv:
            extra.append("arXiv")
        if args.with_prospero:
            extra.append("PROSPERO(token-gated)")
        if args.cochrane:
            extra.append("Cochrane(EPMC journal filter)")
        if args.with_guidelines:
            extra.append("Guidelines(12+)")
        if args.merge_existing:
            extra.append("merge-existing(%s)" % args.merge_existing)
        # 升级项 H/I：本地导入源（不联网，仅告知会并入去重）
        if args.zotero_import:
            extra.append("Zotero(import:%s)" % args.zotero_import)
        if args.merge_cn:
            extra.append("ChineseDB(import:%s)"
                         % ", ".join(os.path.basename(p) for p in args.merge_cn))
        srcs = "OpenAlex" + (" + " + ", ".join(extra) if extra else "")
        # ---- 组小学借鉴：lane 规划视图（dry-run，不联网）----
        _src_enabled = ["OpenAlex"]
        if args.with_europepmc:
            _src_enabled.append("EuropePMC")
        if args.with_pubmed:
            _src_enabled.append("PubMed")
        if args.with_semantic_scholar:
            _src_enabled.append("SemanticScholar")
        if args.with_biorxiv:
            _src_enabled.append("bioRxiv")
        if args.with_medrxiv:
            _src_enabled.append("medRxiv")
        if args.with_arxiv:
            _src_enabled.append("arXiv")
        if args.with_prospero:
            _src_enabled.append("PROSPERO")
        if args.with_guidelines:
            _src_enabled.append("Guidelines")
        if args.cochrane:
            _src_enabled.append("Cochrane")
        _lanes = _build_lane_plan(args.review_type, args.safety, _concepts,
                                  _depth, _src_enabled)
        _out("[PREVIEW] would run literature pipeline: topic=%r review_type=%r safety=%s "
             "sources=[%s] depth=%s (use --run)" % (
                 args.topic, args.review_type, args.safety, srcs, _depth),
             "preview", topic=args.topic, review_type=args.review_type,
             safety=args.safety, sources=srcs, depth=_depth)
        _out("[PREVIEW] 规划 lane 数=%d（证据维度分轨，组小学借鉴）：" % len(_lanes),
             "preview_lanes", n=len(_lanes))
        for _ln in _lanes:
            _out("   · [%s] %s  → 源:%s  (%s)" % (
                _ln["evidence_dimension"], _ln["purpose"], _ln["sources"], _ln["notes"]),
                 "preview_lane", **_ln)
        return

    # ---- U3 交互式门控（2026-10-23 实装）----
    # 修复前：--interactive 只是被接收进 run()，run() 函数体内零使用 —— 勾了等于没勾
    # （CLI 帮助却写着"pause for user confirmation"，属宣称未实现）。
    # 现在：先广播检索策略（progress 事件，前端可渲染），再在**有 TTY** 时暂停等确认；
    # 无 TTY（工作台子进程 / CI）绝不阻塞，但如实广播"门控未生效"，不假装暂停过。
    if args.interactive:
        _g_extra = []
        for _flag, _nm in ((args.with_europepmc, "EuropePMC"),
                           (args.with_pubmed, "PubMed"),
                           (args.with_semantic_scholar, "SemanticScholar"),
                           (args.with_biorxiv, "bioRxiv"),
                           (args.with_medrxiv, "medRxiv"),
                           (args.with_arxiv, "arXiv"),
                           (args.with_guidelines, "Guidelines"),
                           (args.cochrane, "Cochrane")):
            if _flag:
                _g_extra.append(_nm)
        _g_plan = ("topic=%r review_type=%r safety=%s sources=[%s] max=%s "
                   "year=%s-%s depth=%s" % (
                       args.topic, args.review_type, args.safety,
                       "OpenAlex" + (" + " + ", ".join(_g_extra) if _g_extra else ""),
                       args.max, args.year_from or "", args.year_to or "",
                       getattr(args, "depth", None)))
        try:
            _is_tty = bool(sys.stdin) and sys.stdin.isatty()
        except Exception:
            _is_tty = False
        if not _is_tty:
            _out("[WARN] --interactive 需要交互式终端；当前 stdin 不是 TTY（工作台子进程 / CI），"
                 "门控不阻塞、直接执行。检索策略：" + _g_plan,
                 "interactive_gate_skipped", interactive=True, tty=False, plan=_g_plan)
        else:
            _out("[GATE] 检索策略确认（--interactive）：" + _g_plan,
                 "interactive_gate", interactive=True, tty=True, plan=_g_plan)
            try:
                _ans = input("确认执行以上检索策略？[Y/n] ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                _ans = "n"
            if _ans not in ("", "y", "yes"):
                _out("[ABORT] 用户取消：未执行检索。", "interactive_abort",
                     interactive=True, plan=_g_plan)
                return

    # 架构韧性：--health-reset 清空熔断状态，强制下次检索重新试探 Coze 端点
    if args.health_reset:
        source_registry.reset_health()
        _out("[OK] 跨源熔断状态已清空（health.json）", "health_reset")

    run(args.topic, args.review_type, args.year_from, args.year_to, args.safety,
        _max, args.with_europepmc, args.with_semantic_scholar,
        args.with_biorxiv, args.with_medrxiv, args.with_arxiv,
        with_prospero=args.with_prospero, prospero_token=args.prospero_token,
        prospero_header=args.prospero_header,
        with_guidelines=args.with_guidelines,
        guideline_sources=args.guideline_sources,
        guideline_max=args.guideline_max,
        verify_mode=args.verify,
        verify_top_n=args.verify_top_n,
        verify_consistency=not args.no_consistency,
        verify_dois=args.verify_dois,
        out_dir=args.out_dir,
        make_xlsx=not args.no_xlsx, make_html=not args.no_html,
        openalex_key=args.openalex_key, citation_style=args.citation_style,
        export_bib=args.export_bib, prisma=args.prisma, rank=args.rank,
        keywords=args.keywords, obsidian=args.obsidian, zotero=args.zotero,
        lang=resolve_report_lang(args.lang, skill="literature"), cochrane=args.cochrane,
        merge_existing=args.merge_existing, stamp_date=args.stamp_date,
        preprint_fallback=not args.no_preprint_fallback,
        download_pdf=args.download_pdf,
        include_reviews=args.include_reviews, dedupe_engine=args.dedupe_engine,
        original_only=args.original_only,
        only_type=tuple(t.strip().lower() for t in args.only_type.split(","))
                  if args.only_type else None,
        # 组小学借鉴：检索结构模型（P0/P1，2026-09-30）
        concepts=_concepts, depth=_depth, rescue=_rescue,
        # U1 snowball + U3 interactive + U7 report-first（2026-09-30）
        snowball=args.snowball, snowball_max=args.snowball_max,
        snowball_seeds=args.snowball_seeds, snowball_from=args.snowball_from,
        interactive=args.interactive,
        report_first=args.report_first,
        date_from=date_from, date_to=date_to,
        from_pack=args.from_pack,
        # 本地搜索缓存（2026-10-26）：默认开（TTL 24h），--no-cache / --cache-ttl 控制
        no_cache=args.no_cache, cache_ttl=args.cache_ttl,
        # Sci-Hub 最后兑底（2026-10-26）：默认关闭，--use-scihub 显式开启（后果自负）
        use_scihub=args.use_scihub,
        # 默认 online（Coze 统一检索 + 飞书汇总留痕）；--local/--offline 显式回退本地直连。
        # run() 签名默认值保持不变（程序化调用方零影响），CLI 层翻转默认。
        online=not (args.local or args.offline), offline=args.offline,
        topic_en=args.topic_en,
        # 升级项 G/H/I（2026-11-02）：纯本地增量，全部 opt-in，不影响默认检索流程
        zotero_import_path=args.zotero_import,
        merge_cn=args.merge_cn,
        merge_cn_source=args.merge_cn_source,
        with_pubmed=args.with_pubmed, pubmed_fallback=args.pubmed_fallback,
        guidelines_region=args.guidelines_region,
        anchor=args.anchor)

    # ---- A1: Meta-analysis 选题评估（接真实检索产出 → spec → 引擎）----
    if getattr(args, "meta_topic_eval", False) or getattr(args, "meta_topic_eval_run", False):
        _run_meta_topic_eval(args, args.out_dir)


# ── A1: Meta-analysis 选题评估支撑函数（接真实检索产出 → spec → 引擎）─────────────
def _build_meta_topic_spec(merged, args=None):
    """把 ct_literature 检索产出（.merged.json）结构化为 meta_topic_eval 的 spec。

    仅做事实提取（候选 meta / RCT 计数代理 / 源覆盖度 / 异质性存根）；
    需 LLM 判断的字段（PICOS 重叠轴、临床/指南缺口、数据可及）留"待判定"标记，
    不越过脚本能力边界伪造判断，符合 CT 系列证据纪律。
    """
    works = merged.get("works", []) or []
    meta = merged.get("meta", {}) or {}
    ev_log = merged.get("evidence_log", {}) or {}

    # ---- 候选 meta：Cochrane（is_cochrane）或 doc_type==review ----
    existing_metas = []
    for w in works:
        is_coch = w.get("is_cochrane") is True
        is_review = (w.get("doc_type") == "review") or (w.get("type") == "review")
        if is_coch or is_review:
            existing_metas.append({
                "title": w.get("title") or "(untitled)",
                "year": w.get("year") or 0,
                "type": "cochrane" if is_coch else "review",
                "n_studies": None,          # 需 LLM/下游从摘要提取纳入研究数
                "overlap_axes": [],         # 待 LLM 判定 PICOS 重叠轴
            })
    meta_overlap_unresolved = True  # 自动提取未判定重叠轴，引擎据此不自动触发 D1

    # ---- 原始研究充分性（rct_count 代理 + total_n + 源覆盖度）----
    # 真实 OpenAlex 经 ct_literature 检索不提供可靠的 RCT/研究设计粒度：study_type
    # 字段常为 type 的复制（review/article/...）或零星不可靠——端到端验证中 nondiab
    # 因 1 个偶含 "random" 的 study_type 被低估为 rct_count=1，而实际 article=15，
    # 误触发 D2。故一律以「原始研究代理」= type==article 计数，basis 标 article_proxy，
    # 并在报告注明需下游用 Cochrane/RCT 过滤核实真实 RCT 数。
    article_n = sum(1 for w in works if w.get("type") == "article")
    rct_count = article_n
    rct_basis = "article_proxy"
    # total_n：累加 n_participants（若有），否则 None（引擎按 0 → 触发 D2 最坏假设）
    total_n = 0
    _n_hit = False
    for w in works:
        n = w.get("n_participants") or w.get("n_enrolled") or w.get("sample_size")
        if isinstance(n, int):
            total_n += n
            _n_hit = True
    if not _n_hit:
        total_n = None

    # 源覆盖度（五态）→ 证据充分性代理
    _cov_map = {"no_sources": "critical_gap", "critical_gap": "critical_gap",
                "partial": "partial", "empty": "partial", "healthy": "healthy"}
    coverage = _cov_map.get(ev_log.get("coverage"), "unknown")

    primary_studies = {
        "rct_count": rct_count,
        "rct_count_basis": rct_basis,
        "total_n": total_n,
        "coverage": coverage,
        # 异质性探测存根：ct_literature 不产出真实 I²，需下游 R/RevMan 基于各研究
        # 效应量预估算；此处给中性 0.5 并显式标注，避免脚本伪造判断。
        "heterogeneity_i2_est": 0.5,
        "i2_note": "stub: 需下游 R/RevMan 基于各研究效应量预估算真实 I²",
    }

    # ---- PICOS：从检索概念（concepts）提取 ----
    concepts = meta.get("concepts") or []
    picos = {"population": "", "intervention": "", "comparator": "",
             "outcome": "", "study_design": "RCT"}
    _ctype_map = {"population": "population", "pop": "population",
                  "intervention": "intervention", "interventions": "intervention",
                  "comparator": "comparator", "control": "comparator",
                  "outcome": "outcome", "outcomes": "outcome"}
    for c in concepts:
        t = str(c.get("type", "")).lower()
        key = _ctype_map.get(t)
        if key and not picos.get(key):
            picos[key] = c.get("input") or c.get("input_zh") or ""

    spec = {
        "topic": meta.get("topic") or getattr(args, "topic", "") or "",
        "picos": picos,
        "evidence": {
            "existing_metas": existing_metas,
            "primary_studies": primary_studies,
            # 数据可及：脚本无法判定，默认乐观（True/low），由 LLM 核实，不误触发 D3
            "data_accessibility": {"full_text_available": True,
                                   "grey_literature_risk": "low"},
        },
        # 临床/指南缺口：脚本无法判定，留空，F5 维度给提示待 LLM 补充
        "context": {"clinical_gap": "", "guideline_gap": False},
        # 自动构建标记：重叠轴未判定、PICOS/临床缺口待 LLM 补充
        "meta_overlap_unresolved": meta_overlap_unresolved,
        "spec_source": "ct_literature_autobuild",
    }
    return spec


def _run_meta_topic_eval(args, out_dir):
    """检索完成后：构建 spec 并（可选）跑选题评估引擎。返回退出码。"""
    merged_path = os.path.join(out_dir, ".merged.json")
    if not os.path.isfile(merged_path):
        _out("[ERROR] 未找到 %s —— 需先跑一次检索（--run）产出中间状态" % merged_path,
             "meta_topic_eval_no_merged")
        return 2
    try:
        with open(merged_path, "r", encoding="utf-8") as f:
            merged = json.load(f)
    except Exception as e:
        _out("[ERROR] 读取 .merged.json 失败: %s" % e, "meta_topic_eval_read_err",
             error=str(e))
        return 2

    spec = _build_meta_topic_spec(merged, args)
    spec_path = os.path.join(out_dir, "meta_topic_spec.json")
    with open(spec_path, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
    _out("[OK] meta_topic_spec -> %s（候选 meta=%d，rct_count=%s，coverage=%s）"
         % (spec_path, len(spec["evidence"]["existing_metas"]),
            spec["evidence"]["primary_studies"]["rct_count"],
            spec["evidence"]["primary_studies"]["coverage"]),
         "meta_topic_spec", path=spec_path)

    if args.meta_topic_eval_run:
        # 直接调用引擎函数式入口（不重复进程，纯 stdlib）
        try:
            _sd = os.path.dirname(os.path.abspath(__file__))
            if _sd not in sys.path:
                sys.path.insert(0, _sd)
            from meta_topic_eval import evaluate as _mte_eval
        except Exception as e:
            _out("[ERROR] 无法加载 meta_topic_eval 引擎: %s" % e,
                 "meta_topic_eval_import_err", error=str(e))
            return 2
        _mte_eval(spec, out_dir=out_dir, run=True)
    else:
        _out("[SAFE PREVIEW] 已生成 meta_topic_spec.json（未跑引擎）。"
             "由 LLM 补充 overlap_axes / 临床-指南缺口 / 数据可及后，"
             "运行 `python scripts/meta_topic_eval.py --spec %s --run`"
             % spec_path, "meta_topic_eval_preview", path=spec_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
