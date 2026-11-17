#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cite-holmes MCP server — 五工具 tools + resources + prompts 形态。

运行(需 FastMCP 环境):
    uvx --from "git+https://github.com/docsor1212/cite-holmes#subdirectory=mcp" cite-holmes-mcp
    # 或自行准备 FastMCP 环境后: python mcp/server.py   # stdio 模式
分发(免安装直跑):
    uvx --from "git+https://github.com/docsor1212/cite-holmes#subdirectory=mcp" cite-holmes-mcp

设计原则:
- 核心验证逻辑 verify_references_impl / explain_verdict_impl 不依赖 fastmcp
  (纯调用 scripts/verify_refs.py),无 fastmcp 环境下本模块仍可安全 import 与测试。
- 零密钥:verify_references 默认检查不需要 API key;可选 key 经环境变量
  OPENALEX_API_KEY / S2_API_KEY / NCBI_API_KEY 传入(只附加到用户自己的请求)。
- 语义层(来源是否支撑论断)不在机械工具范围,由 agent 自行判定后可用
  semantic 字段回灌 CLI 做封顶。
"""
import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))

# 引擎定位:优先包内嵌入式副本(uvx/git 分发形态,mcp/verify_refs.py,由发布链
# 从 trunk scripts/verify_refs.py 同步并校验 sha);回退 trunk 布局(开发形态,
# ../scripts/verify_refs.py)。两条路径互为镜像——一致性门禁见 mcp/sync_engine.sh。
for _cand in (_HERE, os.path.join(os.path.dirname(_HERE), "scripts")):
    if os.path.isfile(os.path.join(_cand, "verify_refs.py")):
        if _cand not in sys.path:
            sys.path.insert(0, _cand)
        break

import verify_refs as vr  # noqa: E402
from verify_refs import check_document as _check_document_impl  # noqa: E402  # v3.7.0

try:
    from fastmcp import FastMCP
    _MCP_OK = True
except ImportError:  # pragma: no cover - 无 fastmcp 环境下仅使用 impl
    _MCP_OK = False

MAX_CLAIMS = 50          # G5:批量上限——agent 传 500 条会打爆单次会话
_CLIP_STR = 800          # G5:标量字段截断长度


def _clip(obj, limit=_CLIP_STR):
    """递归截断结果中的长字符串(防超大输出撑爆 MCP 消息;结构保持不变)。"""
    if isinstance(obj, str):
        return obj if len(obj) <= limit else obj[:limit] + f"…[+{len(obj) - limit} chars]"
    if isinstance(obj, list):
        return [_clip(x, limit) for x in obj]
    if isinstance(obj, dict):
        return {k: _clip(v, limit) for k, v in obj.items()}
    return obj


def _clip_count(obj, limit):
    """返回截断后对象与被截断字段数(与 _clip 同构但计数,供截断语义化透出)。"""
    n = 0
    def walk(o):
        nonlocal n
        if isinstance(o, str):
            if len(o) > limit:
                n += 1
            return o if len(o) <= limit else o[:limit] + f"…[+{len(o) - limit} chars]"
        if isinstance(o, list):
            return [walk(x) for x in o]
        if isinstance(o, dict):
            return {k: walk(v) for k, v in o.items()}
        return o
    return walk(obj), n


def verify_references_impl(claims: list, timeout: float = 15.0,
                           max_field_chars: int = 800) -> dict:
    """机械验证一组引用(纯实现,无 MCP 依赖)。

    claims: [{"title": str, "url"?: str, "doi"?: str, "pmid"?: str,
              "arxiv"?: str, "source"?: str, "year"?: int}, ...]
    返回: {"version", "scorecard": {score, grade, counts}, "results": [...]}
    边界: 批量上限 MAX_CLAIMS(50);输出长字段截断(_CLIP_STR)。
    """
    if not isinstance(claims, list) or not claims:
        return {"error": "claims must be a non-empty array of reference objects",
                "hint": 'e.g. [{"title": "...", "doi": "10.xxxx/..."}]'}
    if len(claims) > MAX_CLAIMS:
        return {"error": f"claims batch too large: {len(claims)} > {MAX_CLAIMS}",
                "hint": "分批调用(每批 ≤50),或先用检索侧收敛候选清单"}
    vr._net_reset()
    results = []
    for i, ref in enumerate(claims, 1):
        if not isinstance(ref, dict):
            results.append({"index": i, "title": str(ref)[:48], "verdict": "invalid",
                            "note": "条目不是对象", "needs_human_check": True})
            continue
        try:
            r = vr.verify_one(ref, i, False, float(timeout), False)
        except Exception as e:
            # v5.8.0 语义保真：程序故障≠确凿判死（invalid 保留给真实伪造）
            r = {"index": i, "title": str(ref.get("title") or "")[:48],
                 "verdict": "unverified",
                 "note": f"处理异常（{type(e).__name__}）——非判定结果，建议重跑或反馈",
                 "needs_human_check": True}
        results.append(r)
    vr.mark_duplicates(results)
    vr.apply_semantic_cap(results)
    sc = vr.compute_scorecard(results)
    out = {"version": vr.VERSION, "scorecard": sc, "results": results}
    if max_field_chars and max_field_chars > 0:
        out, clipped = _clip_count(out, max_field_chars)
        if clipped:
            # v3.9.0 截断语义化:不静默丢信息——标记截断并指路完整明细
            out["output_clipped"] = {
                "clipped_fields": clipped, "limit": max_field_chars,
                "hint": "长字段已截断;完整逐项明细用 CLI --export auditjson 获取"}
    return out


def explain_verdict_impl(result: dict) -> dict:
    """五态判定语义解释器:verdict+checks → 中文判定依据 + 建议动作。

    输入为 verify_references 返回的单条 result(含 checks 明细)。
    纯静态映射,零网络调用——LLM 友好的解释原语。
    """
    v = result.get("verdict")
    checks = result.get("checks") or {}
    notes = (result.get("note") or "")
    base = {
        "verified": ("来源存在、处于权威层级、字段完整，且通过官方注册库交叉核验",
                     "可支撑正文结论；引用时保留原始链接与判定时间"),
        "partial": ("来源可达但存在降级因素（社区层级/字段缺失/元数据存疑/撤稿/语义否定）",
                    "降级使用：正文引用需注明保留意见，或先人工复核再升级"),
        "unreachable": ("本次抓取失败（404/超时/反爬），不等于不存在",
                        "先开报告附带的 Wayback 存档链对照；关键来源反复失败则更换信源"),
        "invalid": ("标识符不存在、指向错误论文或拼接伪造——机械层确凿判死",
                    "不得引用；从清单删除或更换信源"),
        "unverified": ("未执行检查（离线模式或跳过）",
                       "联网环境重跑以获得真实判定"),
    }.get(v)
    if base is None:
        return {"error": f"unknown verdict: {v}"}
    why, action = base
    steps = []
    c = checks or {}
    if c.get("doi_metadata", {}).get("matched"):
        steps.append("DOI.org 注册元数据比对一致（标题/年份）")
    if c.get("arxiv_metadata", {}).get("matched"):
        steps.append("arXiv 官方 API 元数据比对一致")
    if c.get("s2", {}).get("matched"):
        steps.append("Semantic Scholar 第三源交叉确认")
    if c.get("retraction", {}).get("retracted"):
        steps.append("⚠️ Crossref/Retraction Watch 命中撤稿记录")
    if c.get("openalex", {}).get("confirmed"):
        steps.append("OpenAlex 书目级存在性确认")
    if c.get("url", {}).get("reachable") is True:
        steps.append(f"来源页可达（HTTP {c.get('url', {}).get('status')}）")
    if c.get("url", {}).get("status") == 403:
        steps.append("着陆页 403（注册库已确认存在性，未受反爬影响）")
    if c.get("wayback", {}).get("archive_found"):
        steps.append("Wayback 存档对照可用")
    if not steps:
        steps.append("（无已执行的结构化检查记录——offline 模式或早期返回）")
    return {"verdict": v, "why": why, "evidence_steps": steps,
            "suggested_action": action,
            "raw_note": notes[:300]}


def _capability_text() -> str:
    cap = vr.capability_matrix()
    lines = ["# cite-holmes capability matrix",
             "", "## Mechanical layer catches", ""]
    lines += [f"- {x}" for x in cap["caught"]]
    lines += ["", "## Semantic layer (model/agent judgment)", ""]
    lines += [f"- {x}" for x in cap["semantic"]]
    lines += ["", "## Unsupported inputs", ""]
    lines += [f"- {x}" for x in cap.get("unsupported", [])]
    return "\n".join(lines)


if _MCP_OK:
    mcp = FastMCP("cite-holmes")

    @mcp.tool
    def verify_references(claims: list, timeout: float = 15.0,
                          max_field_chars: int = 800) -> str:
        """Verify a list of references for hallucinated/fabricated citations.

        Each claim object: {"title": str (required), "url"/"doi"/"pmid"/"arxiv": str (optional),
        "source": str, "year": int}. Returns CiteScore (0-100) plus per-reference verdicts:
        verified / partial / unreachable / invalid. Pure mechanical verification against
        official registries (DOI.org, PubMed E-utilities, arXiv, Crossref/Retraction Watch);
        no API keys required, no telemetry."""
        return json.dumps(verify_references_impl(claims, timeout, max_field_chars),
                          ensure_ascii=False, indent=1)

    @mcp.tool
    def check_document(claims: list, document: str, timeout: float = 15.0,
                       anchor_threshold: float = 0.34) -> str:
        """Context-level citation check: parse in-text citation markers in a
        document ([12], [1-4], (Author, Year), doi.org links), bind each to the
        verified reference list, and score anchor-word overlap between the
        citing sentence and the cited title (low = possible mis-citation for
        human review). Complements verify_references: list-level vs context-level."""
        vr._net_reset()
        results = []
        for i, ref in enumerate(claims, 1):
            if not isinstance(ref, dict):
                # 审计 P1-③：逐条隔离镜像——非对象条目确凿 invalid，不再让
                # except 兜底内的 ref.get 二次抛出把整个 tool call 打崩
                results.append({"index": i, "title": str(ref)[:48],
                                "verdict": "invalid", "note": "条目不是对象",
                                "needs_human_check": True})
                continue
            try:
                results.append(vr.verify_one(ref, i, False, float(timeout), False))
            except Exception:
                results.append({"index": i, "title": str(ref.get("title") or "")[:48],
                                "verdict": "unverified", "note": "处理异常——非判定结果",
                                "needs_human_check": True})
        vr.mark_duplicates(results)
        vr.apply_semantic_cap(results)
        cd = _check_document_impl(document, results, float(anchor_threshold))
        return json.dumps({"version": vr.VERSION, "document_check": cd},
                          ensure_ascii=False, indent=1)

    @mcp.tool
    def explain_verdict(result: dict) -> str:
        """Explain one verdict from verify_references in plain language.

        Pass a single result object (with its checks) back; returns why the verdict
        was reached (evidence steps), what it means, and the suggested next action.
        Zero network calls — static explanation layer."""
        return json.dumps(explain_verdict_impl(result), ensure_ascii=False, indent=1)

    @mcp.tool
    def discover_references(topic: str, limit: int = 8, timeout: float = 20.0,
                            sort: str = "relevance") -> str:
        """Literature discovery for deep-research agents: search a topic across
        PubMed + OpenAlex and machine-verify EVERY hit at birth (five-state
        verdicts against official registries, retraction checks included).

        Returns per-reference verdicts plus source notes (rate-limit/skip
        declarations). A deep-research loop can drop invalid hits immediately
        and keep verified ones. Batch ceiling: limit is capped at 25."""
        limit = max(1, min(int(limit or 8), 25))
        refs, notes = vr.discover_refs(topic, limit, float(timeout),
                                       sort=sort if sort in (
                                           "relevance", "cited", "newest")
                                       else "relevance")
        if not refs:
            return json.dumps({"version": vr.VERSION, "topic": topic,
                               "notes": notes, "results": [],
                               "hint": "双源零命中——换检索词或检查网络"},
                              ensure_ascii=False, indent=1)
        payload = json.loads(verify_references_impl(refs, timeout, 800))
        payload["discover_notes"] = notes
        return json.dumps(payload, ensure_ascii=False, indent=1)

    @mcp.tool
    def build_review_kit(results: list, topic: str = "") -> str:
        """Turn verified results into a review-ready kit (markdown).

        Pass the results array returned by verify_references/discover_references;
        returns a comparison table (verified first, citation counts), an annotated
        bibliography, and a paste-ready GB/T 7714 list — every row carrying its
        verdict (partial never reads as verified). Zero network calls."""
        safe = [dict(r, title=vr._CLIP_STR and str(r.get("title") or "")[:800])
                if isinstance(r, dict) and r.get("verdict") else r
                for r in (results or [])]
        kit = vr.build_review_kit(safe, [], topic=str(topic or "")[:200])
        return _clip(kit, _CLIP_STR)

    @mcp.resource("cite-holmes://capability-matrix")
    def capability_matrix_resource() -> str:
        """What this verifier catches, what stays with the semantic layer,
        and which inputs are unsupported."""
        return _capability_text()

    @mcp.resource("cite-holmes://changelog")
    def changelog_resource() -> str:
        """Version history summary (major releases)."""
        return ("cite-holmes versions: v1.2 medical mode + exports; v1.3 CiteScore; "
                "v1.4 DOI cross-check; v1.5 arXiv verification + Wayback; v1.6 circuit "
                "breaker + DOI-PMID cross-check; v1.7 author check + HTML report; "
                "v1.8 retraction detection + OpenAlex; v1.9 Semantic Scholar + BibTeX "
                "import + keys; v1.10 parallel + degraded-network; v1.11 arXiv fallback "
                "+ semantic audit; v1.12 disk cache + proxy + security declaration; "
                "v1.13 task-language description; v2.0 MCP three-primitives + arXiv "
                "version note + NCBI key + evidence chain; v3.0 BLUF dual-reader "
                "reports + scholarly contexts; v3.1 L4 cascade wired into the main "
                "flow + thinking-model-proof judge client; v3.2 BLUF spec conformance "
                "(JSON object) + offline retraction cache; v3.3 NLI third vote "
                "panel. Current: " + vr.VERSION)

    @mcp.prompt
    def fact_check_workflow(topic: str) -> str:
        """Three-step workflow: research the topic, then machine-verify every citation."""
        return (
            f"Research task: {topic}\n\n"
            "1. Search iteratively (both languages if the topic spans CN/EN); fetch the "
            "2-5 most valuable sources in full.\n"
            "2. Register every reference you cite as "
            '{"title", "url"/"doi"/"pmid"/"arxiv", "source", "year"} and call '
            "verify_references on the full list.\n"
            "3. For every non-verified verdict, call explain_verdict on that result and "
            "follow its suggested_action before writing conclusions. Never cite an "
            "unverified reference in the final text.")


def main(argv=None):
    """CLI 入口([project.scripts] cite-holmes-mcp):stdio 默认,可选 http。

    uvx --from "git+https://github.com/docsor1212/cite-holmes#subdirectory=mcp" \
        cite-holmes-mcp --help
    """
    ap = argparse.ArgumentParser(
        prog="cite-holmes-mcp",
        description="cite-holmes MCP server — 机械引用核验(5 tools + resources + prompts)")
    ap.add_argument("--transport", choices=("stdio", "http", "sse"), default="stdio",
                    help="传输方式(默认 stdio;http 监听 127.0.0.1:8760)")
    ap.add_argument("--host", default="127.0.0.1", help="http/sse 模式监听地址")
    ap.add_argument("--port", type=int, default=8760, help="http/sse 模式监听端口")
    args = ap.parse_args(argv)
    if not _MCP_OK:
        print('缺少 FastMCP 运行环境：uvx --from "git+https://github.com/'
              'docsor1212/cite-holmes#subdirectory=mcp" cite-holmes-mcp', file=sys.stderr)
        return 1
    if args.transport == "stdio":
        mcp.run()
    else:
        mcp.run(transport=args.transport, host=args.host, port=args.port)
    return 0


if __name__ == "__main__":
    sys.exit(main())
