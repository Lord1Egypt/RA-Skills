"""cite-holmes v6.0.0 模块层：ch_semantic（由手术脚本从单文件引擎分层，
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


SEMANTIC_SUPPORTS = ("supported", "partial", "not_in_source", "contradicted", "unclear")
_SEMANTIC_CAP = ("not_in_source", "contradicted")


def build_semantic_audit(ref: dict):
    """解析 semantic 字段：dict（新）→ 结构化底稿对象；字符串/缺失（旧）→ None。
    非法 support 值按 unclear 处理并留注记——宁可降级也不让脏数据静默通过。"""
    s = ref.get("semantic")
    if not isinstance(s, dict):
        return None
    support = str(s.get("support") or "").strip().lower()
    note = ""
    if support not in SEMANTIC_SUPPORTS:
        if support:
            note = f"semantic.support 非法值「{support[:30]}」，按 unclear 处理"
        support = "unclear"
    own_note = str(s.get("note") or "").strip()
    if note and own_note:
        note = note + "；" + own_note
    else:
        note = note or own_note
    return {
        "claim": str(s.get("claim") or "").strip(),
        "support": support,
        "quote": str(s.get("quote") or "").strip(),
        "note": note,
    }


def apply_semantic_cap(results: list) -> None:
    """v1.11 语义封顶：语义判定 not_in_source / contradicted 时，机械层 verified
    不得覆盖——封顶 partial 并转人工复核（能力边界矩阵明示语义层不归机械层承诺，
    但模型已做出的否定性判定机械层必须尊重）。在 mark_duplicates 之后统一执行：
    所有判定已收齐，verify_one 的任何 early-return 路径都被覆盖，且串行/并行/
    缓存复用三条路径行为一致。invalid 条目不动（不得反向"提升"为 partial）。"""
    for r in results:
        sa = r.get("semantic_audit") or {}
        if sa.get("support") not in _SEMANTIC_CAP:
            continue
        if r.get("verdict") == "invalid":
            continue
        if r.get("verdict") == "verified":
            r["verdict"] = "partial"
        r["needs_human_check"] = True
        why = (
            "来源未包含所引论断"
            if sa.get("support") == "not_in_source"
            else "来源内容与该论断相矛盾"
        )
        r["note"] = (
            (r.get("note") + "；") if r.get("note") else ""
        ) + f"语义层判定 {sa.get('support')}（{why}）→ 封顶 partial，需人工复核"


def apply_l4_cascade(results: list, timeout: float) -> None:
    """v3.1 L4 证据升级级联（主流程接入）：语义层 not_in_source/unclear 且配置了
    --judge-url 的条目，升级取官方摘要（PMID→PubMed efetch）或全文（arXiv→ar5iv/abs）
    做段落检索（bge-m3，TF-IDF 保底）后交外置裁判。
    判定策略保守：裁判结论只追加注记/needs_human_check，绝不翻案（不把 partial 提回
    verified，不动 invalid）；未配置 --judge-url 时零网络调用零行为变化（审核安全）。"""
    if not _ROOT.judge_endpoint_available():
        return

    # v3.9.0 位 B(fastjudge_design 落地):--fast-judge-url 时先对学生模型预筛
    # (小型分类器延迟极低),按「高置信 REFUTES 优先」排序后再做贵的官方文本升级——
    # 排序路由不跳过任何条目(诚实:总核验量不变,变的是处理次序与可观测性)。
    def _fj_prefilter(r):
        if not (_ROOT._OPTS.get("fast_judge_url") or "").strip():
            return 0  # 无预筛:保持原顺序
        sa = r.get("semantic_audit") or {}
        claim = str(sa.get("claim") or "").strip()
        src = "\n".join(
            x for x in (str(r.get("title") or ""), str(r.get("journal") or "")) if x.strip()
        )
        if not claim or len(src.strip()) < 20:
            return 0
        fj = _ROOT.fast_judge_vote(claim, src, timeout=timeout)
        r.setdefault("checks", {})["fast_judge_prescreen"] = {
            "label": fj.get("label"),
            "prob": fj.get("prob"),
        }
        if fj.get("label") == "REFUTES" and float(fj.get("prob") or 0) >= 0.95:
            return 2  # 高置信反驳:疑似错引,升级复核优先级最高
        return 1

    cands = []
    for r in results:
        try:
            sa = r.get("semantic_audit") or {}
            if sa.get("support") not in ("not_in_source", "unclear"):
                continue
            claim = str(sa.get("claim") or "").strip()
            if not claim or r.get("verdict") == "invalid":
                continue
            pmid = str(r.get("pmid") or "").strip()
            m = re.search(r"(\d{4}\.\d{4,5})(?:v\d+)?", str(r.get("arxiv") or ""))
            if not ((pmid and _ROOT.PMID_RE.match(pmid)) or m):
                continue
            cands.append((_fj_prefilter(r), r))
        except Exception as e:
            try:
                r.setdefault("checks", {})["l4_evidence_cascade"] = {
                    "degraded": f"cascade-error:{type(e).__name__}"
                }
            except Exception:
                pass
    cands.sort(key=lambda t: -t[0])
    if any(p == 2 for p, _ in cands):
        n_hi = sum(1 for p, _ in cands if p == 2)
        print(f"[L4] fast-judge 预筛:{n_hi} 条疑似错引置前复核")
    for _prio, r in cands:
        try:
            sa = r.get("semantic_audit") or {}
            if sa.get("support") not in ("not_in_source", "unclear"):
                continue
            claim = str(sa.get("claim") or "").strip()
            if not claim or r.get("verdict") == "invalid":
                continue
            pmid = str(r.get("pmid") or "").strip()
            m = re.search(r"(\d{4}\.\d{4,5})(?:v\d+)?", str(r.get("arxiv") or ""))
            if pmid and _ROOT.PMID_RE.match(pmid):
                src_name = "pubmed-abstract"
                text = _ROOT.fetch_pubmed_abstract(pmid, timeout)
            elif m:
                src_name = "arxiv-fulltext"
                text = _ROOT.fetch_fulltext(m.group(0), timeout)
            else:
                continue
            chk = r.setdefault("checks", {})
            if not text:
                chk["l4_evidence_cascade"] = {
                    "trigger": sa.get("support"),
                    "evidence_source": src_name,
                    "degraded": "no-text",
                }
                continue
            hits = _ROOT.retrieve_evidence(claim, text, k=2)
            if not hits:
                chk["l4_evidence_cascade"] = {
                    "trigger": sa.get("support"),
                    "evidence_source": src_name,
                    "degraded": "no-chunks",
                }
                continue
            jd = _ROOT.judge_claim_via_endpoint(claim, "\n\n".join(hits), timeout=timeout)
            rec = {
                "trigger": sa.get("support"),
                "evidence_source": src_name,
                "top_chunk_chars": len(hits[0]),
                "judge_verdict": jd.get("verdict"),
            }
            if _ROOT._OPTS.get("nli_url"):
                no = _ROOT.nli_vote("\n\n".join(hits), claim, timeout=timeout)
                agg = aggregate_l2(jd.get("verdict") or "NEI", no)
                rec["nli"] = agg["nli"]
                rec["l2_confidence"] = agg["confidence"]
            if jd.get("degraded"):
                rec["degraded"] = jd["degraded"]
            chk["l4_evidence_cascade"] = rec
            add = lambda s: r.update(
                {"note": ((r.get("note") + "；") if r.get("note") else "") + s}
            )
            if rec.get("l2_confidence") == "contested":
                r["needs_human_check"] = True
                add(
                    f"L2 分歧：裁判判 {jd.get('verdict')} 而 NLI 第三票判 {rec.get('nli')}"
                    "→ 标记人工复核（不自动翻案）"
                )
            if jd.get("verdict") == "SUPPORTS":
                add("L4 升级：官方文本段落级证据经外置裁判判定支持（语义封顶维持，供人工复核参考）")
            elif jd.get("verdict") == "CONTRADICTS":
                r["needs_human_check"] = True
                add("L4 升级：外置裁判在官方文本段落级判定反驳（与语义层否定一致）")
            else:
                add("L4 升级：段落检索后外置裁判仍判证据不足")
        except Exception as e:  # 单条失败不拖垮整跑
            try:
                r.setdefault("checks", {})["l4_evidence_cascade"] = {
                    "degraded": f"cascade-error:{type(e).__name__}"
                }
            except Exception:
                pass


def fast_judge_vote(claim: str, source: str, timeout: float = 30) -> dict:
    """v3.5.0 fast-judge 预筛(外挂小型分类器,OpenAI 兼容端点)。
    输入格式与训练一致(SENTENCE/SOURCE);失败/未配置返回 {"label": None}
    ——预筛层整体弃权,绝不影响主流程。"""
    url = _ROOT._OPTS.get("fast_judge_url") or ""
    if not url or not (claim or "").strip():
        return {"label": None}
    try:
        inp = f"SENTENCE: {claim[:800]}\n\nSOURCE:\n{(source or '')[:6000]}"
        body = json.dumps({"input": inp}).encode()
        req = urllib.request.Request(
            url.rstrip("/") + "/api/fastjudge",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8", "ignore"))
    except Exception:
        return {"label": None}


def apply_fast_judge(results: list, timeout: float) -> None:
    """v3.5.0 fast-judge 预筛(--fast-judge-url 时激活;零配置零变化):
    只服务「语义层待定(not_in_source/unclear)且 L4 级联没给出官方文本判定」的
    条目——外挂学生分类器对 claim×元数据底稿做预筛,高置信 SUPPORTS 仅追加供
    人工参考的 note。永不产生/修改 verdict、永不设 needs_human_check
    (设计红线 fastjudge_design.md;阈值校准 calibration_fastjudge.json:
    SCitance v2.2 claim 级分组 dev,泄漏 0)。"""
    if not (_ROOT._OPTS.get("fast_judge_url") or "").strip():
        return
    thr = float(_ROOT._OPTS.get("fast_judge_threshold") or 0.9)
    for r in results:
        try:
            sa = r.get("semantic_audit") or {}
            if sa.get("support") not in ("not_in_source", "unclear"):
                continue
            claim = str(sa.get("claim") or "").strip()
            if not claim or r.get("verdict") == "invalid":
                continue
            chk = (r.get("checks") or {}).get("l4_evidence_cascade") or {}
            if chk.get("judge_verdict"):
                continue  # L4 已有官方文本判定——预筛让位
            src = "\n".join(
                x for x in (str(r.get("title") or ""), str(r.get("journal") or "")) if x.strip()
            )
            if len(src.strip()) < 20:
                continue  # 无元数据底稿——预筛弃权
            fj = _ROOT.fast_judge_vote(claim, src, timeout=timeout)
            rec = {"label": fj.get("label"), "prob": fj.get("prob")}
            if fj.get("label") == "SUPPORTS" and float(fj.get("prob") or 0) >= thr:
                r["note"] = (
                    (r.get("note") + "；") if r.get("note") else ""
                ) + f"fast-judge 预筛倾向支持（p={float(fj['prob']):.2f}，供人工参考，非判定）"
                rec["action"] = "note-only"
            r.setdefault("checks", {})["fast_judge"] = rec
        except Exception:
            continue


def fetch_pubmed_abstract(pmid: str, timeout: float) -> str:
    """L4 Phase1 证据源：E-utilities efetch 取摘要（夜间雷达管线同源）。失败返回 ""。"""
    u = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi" + _ROOT._ncbi_qs(
        f"?db=pubmed&id={pmid}&rettype=abstract&retmode=text"
    )
    if _ROOT._cb_open(u):
        return ""
    try:
        req = urllib.request.Request(
            u, headers={"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            _ROOT._cb_record(u, False)
            return r.read().decode("utf-8", "ignore")[:4000]
    except Exception:
        _ROOT._cb_record(u, True)
        return ""


def fetch_fulltext(arxiv_id: str, timeout: float) -> str:
    """L4 Phase2 全文源：arXiv HTML（ar5iv 镜像,优先）/abs 页兜底。失败返回 ""。"""
    aid = re.sub(r"v\d+$", "", arxiv_id)
    for url in (f"https://ar5iv.labs.arxiv.org/html/{aid}", f"https://arxiv.org/abs/{aid}"):
        if _ROOT._cb_open(url):
            continue
        for attempt in range(2):  # v3.1：传输错误单次重试（弱网出口 SSL 间歇断流实测）
            try:
                req = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent": f"Mozilla/5.0 (compatible; cite-holmes/{_ROOT.VERSION})"
                    },
                )
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    _ROOT._cb_record(url, False)
                    text = r.read().decode("utf-8", "ignore")
                # 粗剥 HTML 标签
                return re.sub(
                    r"<[^>]+>", " ", re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.S)
                )[:120000]
            except Exception:
                if attempt == 0:
                    time.sleep(2)
                    continue
                _ROOT._cb_record(url, True)
    return ""


def _embed_ollama(texts: list) -> list:
    """bge-m3 嵌入（本机 ollama,HTTP 零依赖）。不可用返回 [] → 调用方降级 TF-IDF。
    v3.1：ollama+bge-m3 对部分短文本产 NaN（500 unsupported value: NaN，实测约 9%
    的短科学声明）——单条 500 时对该条用「文本加倍」变体重试（语义嵌入仍有效），
    再失败才整批降级。"""

    def _call(inp):
        payload = json.dumps({"model": "bge-m3", "input": inp}).encode()
        req = urllib.request.Request(
            "http://127.0.0.1:11434/api/embed",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode()).get("embeddings") or []

    try:
        try:
            return _call(texts)
        except urllib.error.HTTPError as e:
            if e.code != 500 or not texts:
                raise
        # NaN 疑似：单条加倍逐条重建（仅查询路径,量小）
        out = []
        for t in texts:
            try:
                out.append(_call([t])[0])
            except urllib.error.HTTPError:
                out.append(_call([(t or " ") * 2])[0])  # 加倍变体绕 NaN
        return out
    except Exception:
        return []


def retrieve_evidence(query: str, fulltext: str, k: int = 2) -> list:
    """L4 Phase2 段落检索：bge-m3 余弦 top-k；ollama 不可用降级 TF-IDF（保底）。"""
    chunks = _ROOT.chunk_text(fulltext)
    if not chunks:
        return []
    embs = _ROOT._embed_ollama([query] + chunks)
    if len(embs) == len(chunks) + 1 and embs[0]:
        import math

        q = embs[0]
        norms = [math.sqrt(sum(x * x for x in e)) or 1.0 for e in embs]
        scores = [
            sum(a * b for a, b in zip(q, e)) / (norms[0] * n) for e, n in zip(embs[1:], norms[1:])
        ]
        top = sorted(range(len(chunks)), key=lambda i: -scores[i])[:k]
        return [chunks[i] for i in top]
    return [chunks[i] for i in _ROOT._tfidf_top(query, chunks, k)]


def nli_vote(premise: str, hypothesis: str, timeout: float = 30) -> dict:
    """v3.3.0 L2 NLI 第三票(独立 HTTP 服务,nli_service.py 形态)。失败/未配置返回
    {"label": None}——聚合层按弃权处理,绝不影响主流程。"""
    url = _ROOT._OPTS.get("nli_url") or ""
    if not url:
        return {"label": None}
    try:
        body = json.dumps(
            {"premise": (premise or "")[:6000], "hypothesis": (hypothesis or "")[:1000]}
        ).encode()
        req = urllib.request.Request(
            url.rstrip("/") + "/api/nli", data=body, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8", "ignore"))
    except Exception:
        return {"label": None}


_NLI_MAP = {"entailment": "SUPPORTS", "contradiction": "CONTRADICTS", "neutral": "NEI"}


def aggregate_l2(gen_verdict: str, nli_out: dict) -> dict:
    """生成式裁判 + NLI 第三票 → 聚合(实验验证:REFUTES F1 0→0.63)。
    产品哲学:聚合结论只用于注记/复核标记——contested 必须 needs_human_check,
    绝不自动翻转机械层判定(与 L4 保守策略一致)。"""
    nv = _NLI_MAP.get((nli_out or {}).get("label") or "")
    if nv is None or (nli_out or {}).get("abstain"):
        return {"confidence": "single", "nli": "abstained"}
    if nv == gen_verdict:
        return {"confidence": "high", "nli": nv}
    return {"confidence": "contested", "nli": nv}


def judge_endpoint_available() -> bool:
    """L2 外置裁判端点是否配置(--judge-url,OpenAI 兼容:ollama/llama-server/GLM 网关)。"""
    return bool(_ROOT._OPTS.get("judge_url"))


def _scan_label(text: str, labels: tuple) -> str:
    """末位词边界标签提取（思考型模型的思维链里前面可能顺嘴提到其它标签）。"""
    best = None
    for m in re.finditer(r"\b(" + "|".join(labels) + r")\b", text or "", re.I):
        best = m.group(1).upper()
    return best or ""


def judge_claim_via_endpoint(claim: str, evidence: str, timeout: float = 60) -> dict:
    """L4 裁判调用：外部端点判 SUPPORTS/CONTRADICTS/NEI（v3.1 双端点加固）。
    - URL 以 /v1 结尾 → OpenAI 兼容（ollama /v1、llama-server、GLM 网关）；
      content 为空时回退 reasoning 字段（qwen3 等思考模型把结论留在 reasoning——
      实测 /no_think 软开关与 /v1 透传 think 均不可靠，故三者都做）。
    - 其他 URL → ollama 原生 /api/chat：think:false + format JSON schema 枚举强制直答
      （思考模型唯一可靠路径，harness 实测）。
    判不出 → NEI + degraded 注记；无端点 → NEI + no-judge-endpoint。零新依赖。"""
    if not _ROOT.judge_endpoint_available():
        return {"verdict": "NEI", "degraded": "no-judge-endpoint"}
    labels = ("SUPPORTS", "CONTRADICTS", "NEI")
    prompt = (
        "你是证据核查裁判。给定 CLAIM 与 EVIDENCE,只输出三选一标签：\n"
        "SUPPORTS（证据支持声明）/ CONTRADICTS（证据反驳声明）/ NEI（证据不足）。\n\n"
        f"CLAIM: {claim[:800]}\n\nEVIDENCE: {evidence[:3000]}\n\n标签:"
    )
    api = _ROOT._OPTS["judge_url"].rstrip("/")
    model = _ROOT._OPTS.get("judge_model", "qwen3.8-27b")
    try:
        if api.endswith("/v1"):
            body = json.dumps(
                {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt + " /no_think"}],
                    "temperature": 0,
                    "max_tokens": 96,
                }
            ).encode()
            req = urllib.request.Request(
                api + "/chat/completions", data=body, headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                msg = (
                    json.loads(r.read().decode("utf-8", "ignore"))
                    .get("choices", [{}])[0]
                    .get("message", {})
                )
            tag = _scan_label(msg.get("content") or "", labels)
            if tag:
                return {"verdict": tag}
            reas = msg.get("reasoning") or ""
            tag = _scan_label(reas, labels)
            if tag:
                return {"verdict": tag, "degraded": "parsed-from-reasoning"}
            return {
                "verdict": "NEI",
                "degraded": "unparsed-reply:" + (msg.get("content") or reas)[:40],
            }
        schema = {
            "type": "object",
            "properties": {"label": {"type": "string", "enum": list(labels)}},
            "required": ["label"],
        }
        body = json.dumps(
            {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "think": False,
                "stream": False,
                "format": schema,
                "options": {"temperature": 0, "num_predict": 32},
            }
        ).encode()
        req = urllib.request.Request(
            api + "/api/chat", data=body, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            msg = json.loads(r.read().decode("utf-8", "ignore")).get("message", {})
        out = (msg.get("content") or msg.get("thinking") or "").strip()
        try:
            out = json.loads(out).get("label", out)
        except Exception:
            pass
        tag = _scan_label(str(out), labels)
        if tag:
            return {"verdict": tag}
        return {"verdict": "NEI", "degraded": "unparsed-reply:" + str(out)[:40]}
    except Exception as e:
        return {"verdict": "NEI", "degraded": f"endpoint-error:{type(e).__name__}"}
