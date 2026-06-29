#!/usr/bin/env python3
"""CNexus 2.0 Pure Gateway — L0-spec HTTP server, zero legacy import conflicts."""

import os, sys, json, math, time, traceback, cgi, shutil, subprocess, threading, ast, base64, re
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from urllib import request as urlrequest

# ── Phase 4 纯函数 kernel 加载 ─────────────────────────────────────────
# 绕过 src/__init__.py（它会尝试 import 旧 CNexusOSKernel 然后炸裂）
KERNEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "kernel")

def _load_kernel_module(name, fname):
    import importlib.util as u
    # Phase 4 reducers use relative imports (e.g. "from kernel.state_snapshot import ...")
    # so we need src/ on sys.path for the dependency chain.
    src_dir = os.path.dirname(KERNEL_DIR)
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    spec = u.spec_from_file_location(name, os.path.join(KERNEL_DIR, fname))
    m = u.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_obs_mod    = _load_kernel_module("observe_reducer",    "observe_reducer.py")
_cog_mod    = _load_kernel_module("cognize_reducer",    "cognize_reducer.py")
_dec_mod    = _load_kernel_module("decide_reducer",     "decide_reducer.py")
_spk_mod    = _load_kernel_module("speak_reducer",      "speak_reducer.py")
_sto_mod    = _load_kernel_module("store_reducer",      "store_reducer.py")
_rfl_mod    = _load_kernel_module("reflect_reducer",    "reflect_reducer.py")
_snp_mod    = _load_kernel_module("state_snapshot",     "state_snapshot.py")
_idp_mod    = _load_kernel_module("identity_position",  "identity_position.py")
_l2d_mod    = _load_kernel_module("l2_degradation_policy", "l2_degradation_policy.py")

observe_fn     = _obs_mod.observe_fn
cognize_fn     = _cog_mod.cognize_fn
decide_fn      = _dec_mod.decide_fn
speak_fn       = _spk_mod.speak_fn
store_fn       = _sto_mod.store_fn
reflect_fn     = _rfl_mod.reflect_fn
BlockStore     = _sto_mod.BlockStore
StateSnapshot  = _snp_mod.StateSnapshot

# ── Cognitive Engine State ──────────────────────────────────────────────
_engine_state = {
    "active": True,
    "engine_initialized": True,
    "state": StateSnapshot(),
    "memory_store": BlockStore(),
    "trace": [],
    "gtbs_events": [],
    "runtime_logs": [],
    "token_traces": [],
    "current_iteration": 0,
    "model_registry": {},
    "started_at": time.time(),
    "activation": {
        "scores": {},  # node_id -> activation score (0..1)
        "wormhole_links": [],  # [{source, target, similarity, energy}]
    },
    "consolidation": {
        "last_activity_at": time.time(),
        "last_shallow_at": 0,
        "last_rem_at": 0,
        "rem_running": False,
        "total_pruned": 0,
        "total_facts": 0,
        "last_rem_report": None,
    },
    "projection": {
        "nodes": {},
        "links": [],
    },
}

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "127.0.0.1:11434")

# ── Spreading Activation with Temporal Decay (personal memory graph) ──
_ACTIVATION_DECAY = 0.8
_ACTIVATION_THRESHOLD = 0.4
_ACTIVATION_SPREAD_HOP1 = 0.5
_ACTIVATION_SPREAD_HOP2 = 0.2
_ACTIVATION_SEED_PULSE = 1.0
_ACTIVATION_MAX_SCORE = 1.0
_activation_lock = threading.Lock()

# ── Wormhole Protocol (semantic cosine bridges) ──
_WORMHOLE_SIM_THRESHOLD = float(os.environ.get("CNEXUS_WORMHOLE_SIM_THRESHOLD", "0.75"))
_WORMHOLE_ENERGY_COEFF = float(os.environ.get("CNEXUS_WORMHOLE_ENERGY_COEFF", "0.40"))
_WORMHOLE_MAX_LINKS = int(os.environ.get("CNEXUS_WORMHOLE_MAX_LINKS", "64"))
_WORMHOLE_MAX_COMPARE = int(os.environ.get("CNEXUS_WORMHOLE_MAX_COMPARE", "28"))
_VECTOR_CACHE = {}  # node_text -> [float]
_vector_cache_lock = threading.Lock()

# ── Multi-Modal & Code Intelligence ──
_CNEXUS_VISION_MODEL = os.environ.get("CNEXUS_VISION_MODEL", "llava")

# ── REM Deep Sleep & Memory Consolidation ──
_REM_IDLE_SECONDS = int(os.environ.get("CNEXUS_REM_IDLE_SECONDS", "1800"))
_REM_COOLDOWN_SECONDS = int(os.environ.get("CNEXUS_REM_COOLDOWN", "3600"))
_REM_ACTIVE_NODE_THRESHOLD = int(os.environ.get("CNEXUS_REM_ACTIVE_THRESHOLD", "20"))
_REM_NODE_THRESHOLD = int(os.environ.get("CNEXUS_REM_NODE_THRESHOLD", "36"))
_REM_TRACE_KEEP = int(os.environ.get("CNEXUS_REM_TRACE_KEEP", "12"))
_REM_COMPACT_WINDOW_SECONDS = int(os.environ.get("CNEXUS_REM_COMPACT_WINDOW", str(7 * 86400)))
_REM_SCORE_PRUNE_MAX = 0.02
_REM_WATCHDOG_INTERVAL = int(os.environ.get("CNEXUS_REM_WATCHDOG_INTERVAL", "60"))
_REM_MAX_FACTS = 5
_rem_lock = threading.Lock()


def _default_model_registry():
    return {
        "cnexus-local": {
            "id": "cnexus-local",
            "name": "CNexus 2.0 Local",
            "provider": "cnexus",
            "base_url": "",
            "model": "cognitive-kernel",
            "api_key": "",
            "api_key_set": True,
            "is_default": True,
            "enabled": True,
        },
        "ollama-local": {
            "id": "ollama-local",
            "name": "Ollama 本地",
            "provider": "ollama",
            "base_url": f"http://{OLLAMA_HOST}",
            "model": "llama3.2",
            "api_key": "",
            "api_key_set": True,
            "is_default": False,
            "enabled": False,
        },
        "deepseek-chat": {
            "id": "deepseek-chat",
            "name": "DeepSeek Chat",
            "provider": "openai_compatible",
            "base_url": "https://api.deepseek.com",
            "model": "deepseek-v4-flash",
            "api_key": "",
            "api_key_set": False,
            "is_default": False,
            "enabled": False,
        },
        "openai-default": {
            "id": "openai-default",
            "name": "OpenAI",
            "provider": "openai",
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4o-mini",
            "api_key": "",
            "api_key_set": False,
            "is_default": False,
            "enabled": False,
        },
    }


_engine_state["model_registry"] = _default_model_registry()

def _iso_ts():
    return time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())


def _gtbs_row(phase, tx_id, trace_id, kind, entry, caller="http", mutability="explicit", shadow=False, extra=None):
    row = {
        "event_type": phase,
        "transaction_id": tx_id,
        "ts": _iso_ts(),
        "payload": {
            "write_intent_kind": kind,
            "mutability": mutability,
            "provenance": {
                "trace_id": trace_id,
                "caller": caller,
                "channel": "cnexus-2.0-personal",
                "entry_registry": entry,
            },
            "phase": phase,
        },
    }
    if shadow:
        row["payload"]["shadow"] = True
        row["payload"]["gtbs_mode"] = "SHADOW"
    if extra:
        row["payload"].update(extra)
    return row


def _append_runtime_log(message, category="gtbs", level="info", trace_id=None):
    entry = {
        "id": f"log-{int(time.time()*1000)}-{len(_engine_state['runtime_logs'])}",
        "timestamp": _iso_ts(),
        "level": level,
        "category": category,
        "message": message,
        "meta": {"trace_id": trace_id} if trace_id else {},
    }
    _engine_state["runtime_logs"].append(entry)
    if len(_engine_state["runtime_logs"]) > 500:
        _engine_state["runtime_logs"] = _engine_state["runtime_logs"][-500:]


def _record_flow_logs(iteration, trace_id, input_text, decision):
    """Emit categorized runtime logs that drive the 7-layer Neural Flow model."""
    preview = (input_text or "").strip()[:80]
    intent = _decision_intent(decision)
    _append_runtime_log(f"感官输入 · {preview or '(empty)'}", category="chat", trace_id=trace_id)
    _append_runtime_log(f"执行链激活 · intent={intent}", category="execution", trace_id=trace_id)
    _append_runtime_log("记忆写入 episodic/emotion", category="capture", trace_id=trace_id)
    _append_runtime_log(f"认知脉冲 #{iteration} · CSE trace", category="cse", trace_id=trace_id)


def _record_cycle_gtbs(iteration, trace_id, input_text, decision, speech, store_result):
    """Project one 6-step cognitive cycle into GTBS-compatible debugger events."""
    it = iteration
    preview = (input_text or "").strip()[:80]
    rows = [
        _gtbs_row("proposal", f"tx-{it}-dispatch", trace_id, "chat_dispatch", "process_interaction"),
        _gtbs_row(
            "proposal", f"tx-{it}-observe", trace_id, "observe", "observe_fn",
            caller="internal", mutability="implicit", shadow=True,
            extra={"reason": preview or "empty input"},
        ),
        _gtbs_row(
            "proposal", f"tx-{it}-cognize", trace_id, "cognize", "cognize_fn",
            caller="internal", mutability="implicit", shadow=True,
        ),
        _gtbs_row(
            "proposal", f"tx-{it}-decide", trace_id, "decide", "decide_fn",
            caller="internal", mutability="advisory",
            extra={"intent": (decision or {}).get("intent", "converse")},
        ),
        _gtbs_row(
            "commit", f"tx-{it}-speak", trace_id, "chat", "speak_fn",
            extra={"reply_preview": str((speech or {}).get("text", ""))[:120]},
        ),
        _gtbs_row(
            "commit", f"tx-{it}-store", trace_id, "capture", "store_fn",
            extra={
                "target_stores": ["episodic", "emotion"],
                "blocks_written": (store_result or {}).get("blocks_written", {}),
            },
        ),
        _gtbs_row(
            "proposal", f"tx-{it}-reflect", trace_id, "reflect", "reflect_fn",
            caller="internal", mutability="advisory", shadow=True,
        ),
    ]
    _engine_state["gtbs_events"].extend(rows)
    if len(_engine_state["gtbs_events"]) > 2000:
        _engine_state["gtbs_events"] = _engine_state["gtbs_events"][-2000:]
    _append_runtime_log(
        f"6-step cycle #{it} · intent={(decision or {}).get('intent', 'converse')} · input={preview or '(empty)'}",
        category="gtbs",
        trace_id=trace_id,
    )
    _record_flow_logs(it, trace_id, input_text, decision)


def _seed_boot_events():
    if _engine_state["gtbs_events"]:
        return
    trace_id = "v2-boot-0"
    boot_rows = [
        _gtbs_row("proposal", "tx-boot-1", trace_id, "system_boot", "kernel_boot", caller="internal", mutability="advisory"),
        _gtbs_row("commit", "tx-boot-2", trace_id, "runtime_ready", "gateway_health", caller="internal"),
    ]
    _engine_state["gtbs_events"].extend(boot_rows)
    _append_runtime_log("CNexus 2.0 personal kernel online", category="control_plane", trace_id=trace_id)


_seed_boot_events()

def _resolve_model_row(model_id=None):
    registry = _engine_state["model_registry"]
    mid = model_id or _active_chat_model_id()
    row = registry.get(mid)
    if not row and mid in _default_model_registry():
        row = dict(_default_model_registry()[mid])
        registry[mid] = row
    return row


def _should_use_external_llm(model_row):
    if not model_row or not model_row.get("enabled", True):
        return False
    provider = model_row.get("provider", "")
    if provider in ("cnexus", ""):
        return False
    if provider == "ollama":
        return True
    return bool((model_row.get("api_key") or "").strip())


def _llm_chat_url(model_row):
    base = (model_row.get("base_url") or "").rstrip("/")
    provider = model_row.get("provider", "")
    if provider == "ollama" or ":11434" in base:
        return f"{base}/api/chat"
    if base.endswith("/v1"):
        return f"{base}/chat/completions"
    return f"{base}/v1/chat/completions"


def _invoke_external_llm(model_row, user_text, memory_context=None):
    url = _llm_chat_url(model_row)
    provider = model_row.get("provider", "")
    is_ollama = provider == "ollama" or "/api/chat" in url
    messages = []
    ctx = (memory_context or "").strip()
    if ctx:
        messages.append({
            "role": "system",
            "content": (
                "You are CNexus 2.0 personal cognitive assistant.\n"
                "--- Subconscious Memory (spreading activation, instant recall) ---\n"
                f"{ctx}"
            ),
        })
    messages.append({"role": "user", "content": user_text})
    body = {
        "model": model_row.get("model") or "llama3.2",
        "messages": messages,
        "stream": False,
    }
    data = json.dumps(body).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    api_key = (model_row.get("api_key") or "").strip()
    if api_key and not is_ollama:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urlrequest.Request(url, data=data, headers=headers, method="POST")
    with urlrequest.urlopen(req, timeout=120) as resp:
        payload = json.loads(resp.read().decode("utf-8", errors="replace"))

    reply = ""
    tokens_in = 0
    tokens_out = 0
    if is_ollama:
        reply = str((payload.get("message") or {}).get("content") or "")
        tokens_in = int(payload.get("prompt_eval_count") or 0)
        tokens_out = int(payload.get("eval_count") or 0)
    else:
        reply = str((payload.get("choices") or [{}])[0].get("message", {}).get("content") or "")
        usage = payload.get("usage") or {}
        tokens_in = int(usage.get("prompt_tokens") or 0)
        tokens_out = int(usage.get("completion_tokens") or 0)

    if not reply.strip():
        raise ValueError("LLM 返回空回复")
    if tokens_in <= 0:
        tokens_in = _estimate_tokens(user_text)
    if tokens_out <= 0:
        tokens_out = _estimate_tokens(reply)
    return {
        "reply": reply.strip(),
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "provider": provider,
        "model_id": model_row.get("id"),
    }


def _run_6step(input_text: str, model_id=None) -> dict:
    """Run a full 6-step cognitive cycle, matching Phase 4 reducer signatures."""
    _touch_user_activity()
    st = _engine_state["state"]
    ms = _engine_state["memory_store"]
    _engine_state["current_iteration"] += 1

    # 1. OBSERVE
    obs = observe_fn(input_text, st)
    # 2. COGNIZE
    cog = cognize_fn(obs, st, [])
    # Decide expects context as dict — convert CognizeContext if needed
    ctx = cog.context
    if hasattr(ctx, 'state_snapshot'):
        # Convert object to dict
        ctx = {k: getattr(ctx, k) for k in ['state_snapshot', 'recall_items', 'context_bundle', 'observation_type'] if hasattr(ctx, k)}
    # 3. DECIDE
    dec = decide_fn(ctx, st)
    # 4. SPEAK — external LLM or built-in kernel
    model_row = _resolve_model_row(model_id)
    if model_row and model_row.get("provider") == "ollama":
        _sync_ollama_registry()
        model_row = _resolve_model_row(model_id)
    # Threshold trigger: O(1) subconscious recall — no RAG scan
    activation_hits = _threshold_activated_fragments(limit=3)
    activation_context = _format_activation_context(activation_hits)
    token_source = "estimated"
    token_mode = "fast"
    llm_usage = None
    llm_error = None
    llm_source = "kernel"
    if _should_use_external_llm(model_row):
        try:
            llm_usage = _invoke_external_llm(model_row, input_text, activation_context or None)
            spk = {
                "text": llm_usage["reply"],
                "inference_type": "llm",
                "confidence": 0.9,
                "latency_ms": 0,
                "metadata": {"provider": model_row.get("provider"), "model_id": model_row.get("id")},
            }
            token_source = "provider"
            llm_source = "provider"
            token_mode = str(model_row.get("model") or model_row.get("provider") or "llm")
        except Exception as exc:
            llm_error = str(exc)
            spk = speak_fn(dec, ctx, st)
            spk = dict(spk) if isinstance(spk, dict) else {"text": str(spk)}
            spk["metadata"] = {**(spk.get("metadata") or {}), "llm_fallback": llm_error}
    else:
        spk = speak_fn(dec, ctx, st)
    # 5. STORE
    iteration_meta = {"iteration": _engine_state["current_iteration"], **obs}
    sto = store_fn(spk, st, iteration_meta, ms)
    # 6. REFLECT
    rfl = reflect_fn(sto, st, _engine_state.get("trace", [])[-3:], ms)

    _engine_state["trace"].append({
        "iteration": _engine_state["current_iteration"],
        "trace_id": f"v2-trace-{_engine_state['current_iteration']}",
        "timestamp": time.time(),
        "input": input_text,
        "observation": obs, "cognition": cog,
        "decision": dec, "speech": spk,
        "store": sto, "reflection": rfl,
    })
    trace_id = f"v2-trace-{_engine_state['current_iteration']}"
    _record_cycle_gtbs(_engine_state["current_iteration"], trace_id, input_text, dec, spk, sto)
    reply = spk.get("text", spk.get("response_text", "")) if isinstance(spk, dict) else _speech_text(spk)
    _schedule_activation_post_turn(input_text, reply, trace_id)
    if llm_usage:
        _record_token_trace(
            trace_id,
            input_text,
            reply,
            entry="converse",
            mode=token_mode,
            tokens_in=llm_usage["tokens_in"],
            tokens_out=llm_usage["tokens_out"],
            source="provider",
            model_id=llm_usage.get("model_id"),
            provider=llm_usage.get("provider"),
        )
    else:
        _record_token_trace(
            trace_id,
            input_text,
            reply,
            entry="converse",
            mode=token_mode,
            source=token_source,
            model_id=model_row.get("id") if model_row else None,
            provider=(model_row or {}).get("provider"),
        )
    return {
        "reply": reply,
        "emotion": {"valence": st.emotion.val, "arousal": st.emotion.arousal, "dominance": st.emotion.dominance},
        "intent": dec.get("intent", "converse"),
        "iteration": _engine_state["current_iteration"],
        "llm_source": llm_source,
        "llm_error": llm_error,
        "model_id": model_row.get("id") if model_row else None,
        "model_name": model_row.get("model") if model_row else None,
        "activation_injected": len(activation_hits),
        "activation_context": activation_context,
        "activation_hits": [
            {"id": spec["id"], "title": spec["title"], "score": round(score, 4)}
            for score, spec in activation_hits
        ],
    }

# ── HTTP Server ─────────────────────────────────────────────────────────
def api_status():
    """返回 CNexus 2.0 的个人版 L0 状态（与 adapter.ts 的 statusToMindOverview 对齐）"""
    st = _engine_state["state"]
    ms = _engine_state["memory_store"]
    return {
        # ── 数据契约对齐：前端 statusToMindOverview 严格校验 schema_version / cards / feeds / system / chat_context / memory_items ──
        "schema_version": "2.0",
        "active": True,
        "engine_initialized": True,
        "memory_count": len(ms.blocks),
        "execution_count": _engine_state["current_iteration"],
        "current_iteration": _engine_state["current_iteration"],
        "status": "online",
        "emotion": {"valence": st.emotion.val, "arousal": st.emotion.arousal, "dominance": st.emotion.dominance},
        "goal": {"current": (st.goal or {}).get("current", "explore"), "progress": (st.goal or {}).get("progress", 0.0)},
        "relationship": {"closeness": (st.relationship or {}).get("closeness", 0.5)},
        "cog_state": {
            "active_intent": (st.meta or {}).get("active_intent", "idle"),
            "accumulated_weight": (st.meta or {}).get("weight", 0),
            "total_observations": _engine_state["current_iteration"],
        },
        "attention": {"focus": "general", "level": 0.5},
        # ── MindOverview 顶层必需字段 ──
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
        "cards": {
            "goal": {"title": (st.goal or {}).get("current", "探索"), "progress": (st.goal or {}).get("progress", 0.0), "progress_label": f"{round((st.goal or {}).get('progress', 0.0)*100)}%", "alignment": 0.75, "alignment_label": "75%", "priority": 0.5, "priority_label": "中"},
            "identity": {"summary": "CNexus 2.0 Personal", "stability": 0.7, "stability_label": "70%", "consistency": 0.8, "consistency_label": "80%", "updated_ago": "now"},
            "belief": {"content": (st.goal or {}).get("current", "探索"), "confidence": 0.65, "confidence_label": "65%", "evidence_count": _engine_state["current_iteration"], "conflict_count": 0},
            "focus": {"title": (st.meta or {}).get("active_intent", "idle"), "attention_label": "50%", "duration_label": "realtime", "related_goals": 1},
        },
        "feeds": {
            "episodic": [
                {"text": item.get("title", ""), "ago": "recent"}
                for item in _memory_items_for_overview()
                if item.get("tag") == "episode"
            ][:8] or [{"text": "等待对话或上传以生成记忆节点", "ago": "now"}],
            "reflections": [{"text": f"已完成 {_engine_state['current_iteration']} 次认知循环", "ago": "now"}],
            "changes": [f"memory_blocks={len(ms.blocks)}", "stable"],
        },
        "system": {
            "health_score": 0.85,
            "health_label": "stable",
            "memory_capacity_pct": min(99, len(ms.blocks) * 2),
            "governance_label": "personal",
            "governance_conflicts": 0,
            "reflective_active": 0,
            "last_update_ago": "now",
            "api_online": True,
        },
        "chat_context": {"goal": (st.goal or {}).get("current", "探索"), "belief": "探索", "identity": "CNexus 2.0 Personal"},
        "memory_items": _memory_items_for_overview(),
        "consolidation": _consolidation_status(),
        "wormhole_links": _wormhole_links_snapshot(),
        "projection_links": _projection_links_snapshot(),
    }

_prepare_cache: dict = {}
_file_cache: dict = {}


def _normalize_memory_tag(label):
    raw = str(label or "episode").lower()
    if raw in ("code_class", "code_function", "vision_component"):
        return raw
    if raw in ("episodic", "episode"):
        return "episode"
    if raw in ("goal", "belief", "identity", "insight", "semantic"):
        return "belief" if raw == "semantic" else raw
    if raw == "emotion":
        return "insight"
    return "term"


def _extract_keywords(text, limit=6):
    if not text:
        return []
    import re
    tokens = re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z]{3,}", str(text))
    seen = set()
    out = []
    for tok in tokens:
        key = tok.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(tok[:24])
        if len(out) >= limit:
            break
    return out


def _activation_scores():
    return _engine_state.setdefault("activation", {}).setdefault("scores", {})


def _sync_activation_nodes(specs):
    scores = _activation_scores()
    for spec in specs:
        scores.setdefault(spec["id"], 0.0)


def _attach_activation_fields(spec):
    score = float(_activation_scores().get(spec["id"], 0.0))
    out = {
        **spec,
        "score": round(score, 4),
        "activity": round(score, 4),
        "is_active": score > _ACTIVATION_THRESHOLD,
    }
    if spec.get("node_type"):
        out["node_type"] = spec["node_type"]
    return out


def _projection_store():
    return _engine_state.setdefault("projection", {"nodes": {}, "links": []})


def _projection_links_snapshot():
    return [
        {
            "source": link.get("source"),
            "target": link.get("target"),
            "type": link.get("type"),
        }
        for link in _projection_store().get("links", [])
    ]


def _build_activation_adjacency(specs):
    by_cluster = {}
    for spec in specs:
        cluster = str(spec.get("cluster") or spec["id"])
        by_cluster.setdefault(cluster, []).append(spec["id"])
    adj = {spec["id"]: set() for spec in specs}
    for spec in specs:
        nid = spec["id"]
        parent = str(spec.get("parent_id") or "").strip()
        if parent and parent in adj:
            adj[nid].add(parent)
            adj[parent].add(nid)
        cluster = str(spec.get("cluster") or "")
        for peer in by_cluster.get(cluster, ()):
            if peer != nid:
                adj[nid].add(peer)
    id_set = set(adj.keys())
    for link in _projection_store().get("links", []):
        src = str(link.get("source") or "")
        tgt = str(link.get("target") or "")
        if src in id_set and tgt in id_set:
            adj[src].add(tgt)
            adj[tgt].add(src)
    return adj


def _collect_memory_node_specs():
    items = []
    seen = set()

    def push(item_id, title, tag, desc="", meta="recent", cluster=None, parent_id=None, node_type=None):
        title = str(title or "").strip()[:120]
        tag_norm = _normalize_memory_tag(tag)
        dedupe_key = item_id if tag_norm in ("code_class", "code_function", "vision_component") else title
        if not title or dedupe_key in seen:
            return
        seen.add(dedupe_key)
        cluster_key = str(cluster or parent_id or meta or item_id)
        item = {
            "id": item_id,
            "title": title,
            "tag": tag_norm,
            "desc": str(desc or "")[:160],
            "meta": meta,
            "cluster": cluster_key,
            "parent_id": str(parent_id or ""),
        }
        if node_type:
            item["node_type"] = node_type
        items.append(item)

    st = _engine_state["state"]
    goal = (st.goal or {}).get("current", "探索")
    push("goal-current", goal, "goal", f"progress={(st.goal or {}).get('progress', 0):.0%}", "L0", cluster="core", parent_id=None)

    for block in _engine_state["memory_store"].blocks:
        data = block.get("data") or {}
        block_id = block.get("block_id", f"mem-{len(items)}")
        label = str(block.get("label", "episodic"))
        is_semantic = label == "semantic" or str(block_id).startswith("sem-rem-")
        is_projection = label in ("code_class", "code_function", "vision_component") or str(block_id).startswith(("class:", "func:", "vision:"))
        if not is_semantic and not is_projection and block not in _engine_state["memory_store"].blocks[-20:]:
            continue
        title = (data.get("content") or data.get("label") or "REM fact")[:120] if is_semantic else (data.get("filename") or data.get("label") or block.get("label", "memory"))
        if is_projection:
            title = (data.get("label") or title)[:120]
        content = str(data.get("content") or data.get("response_text") or "")
        tag = label if is_projection else ("semantic" if is_semantic else label)
        meta = "long-term" if is_semantic else ("projection" if is_projection else "upload")
        cluster = data.get("cluster") or ("long-term" if is_semantic else block_id)
        parent_id = data.get("parent_id") or ("" if not is_projection else data.get("parent_id", ""))
        push(block_id, title, tag, content[:160], meta, cluster=cluster, parent_id=parent_id, node_type=tag if is_projection else None)
        for kw in data.get("keywords") or _extract_keywords(content, 5):
            push(
                f"kw-{block_id}-{kw}",
                kw,
                "term",
                content[:80],
                "keyword",
                cluster=cluster,
                parent_id=block_id,
            )

    for entry in _engine_state.get("trace", [])[-14:]:
        inp = str(entry.get("input") or "").strip()
        if not inp:
            continue
        trace_id = entry.get("trace_id", f"v2-trace-{entry.get('iteration', 0)}")
        speech = entry.get("speech") or {}
        reply = _speech_text(speech)
        push(trace_id, inp[:100], "episode", f"trace {trace_id}", "dialogue", cluster=trace_id, parent_id=None)
        intent = _decision_intent(entry.get("decision"))
        push(
            f"{trace_id}-intent",
            f"意图 · {intent}",
            "insight",
            inp[:80],
            trace_id,
            cluster=trace_id,
            parent_id=trace_id,
        )
        for kw in _extract_keywords(inp, 4):
            push(
                f"{trace_id}-kw-{kw}",
                kw,
                "term",
                inp[:80],
                "concept",
                cluster=trace_id,
                parent_id=trace_id,
            )
        if reply:
            for kw in _extract_keywords(reply, 5):
                push(
                    f"{trace_id}-rk-{kw}",
                    kw,
                    "insight",
                    reply[:80],
                    "reply_concept",
                    cluster=trace_id,
                    parent_id=trace_id,
                )

    for node in _projection_store().get("nodes", {}).values():
        push(
            node["id"],
            node.get("title") or node["id"],
            node.get("tag") or node.get("node_type") or "term",
            node.get("desc", ""),
            node.get("meta", "projection"),
            cluster=node.get("cluster"),
            parent_id=node.get("parent_id"),
            node_type=node.get("node_type") or node.get("tag"),
        )

    return items[:64]


def _memory_items_for_overview():
    specs = _collect_memory_node_specs()
    _sync_activation_nodes(specs)
    return [_attach_activation_fields(spec) for spec in specs]


def _threshold_activated_fragments(limit=3):
    specs = _collect_memory_node_specs()
    _sync_activation_nodes(specs)
    scores = _activation_scores()
    candidates = []
    for spec in specs:
        s = float(scores.get(spec["id"], 0.0))
        if s > _ACTIVATION_THRESHOLD:
            candidates.append((s, spec))
    candidates.sort(key=lambda x: -x[0])
    return candidates[:limit]


def _format_activation_context(hits):
    if not hits:
        return ""
    lines = []
    for i, (score, spec) in enumerate(hits, 1):
        lines.append(f"{i}. [{spec['tag']}] {spec['title']} (activation={score:.2f})")
        if spec.get("desc"):
            lines.append(f"   {spec['desc'][:140]}")
    return "\n".join(lines)


def _match_seed_node_ids(text, specs):
    text_l = (text or "").lower()
    seeds = set()
    keywords = _extract_keywords(text, 8)
    for spec in specs:
        title = spec["title"]
        title_l = title.lower()
        if len(title) >= 2 and title_l in text_l:
            seeds.add(spec["id"])
            continue
        for kw in keywords:
            kw_l = kw.lower()
            if kw_l in title_l or title_l in kw_l:
                seeds.add(spec["id"])
                break
    return seeds


def _node_embedding_text(spec):
    title = str(spec.get("title") or "").strip()
    desc = str(spec.get("desc") or "").strip()
    text = f"{title} {desc}".strip()
    return text[:512]


def _ollama_list_embed_models():
    """Return Ollama model names that support /api/embeddings."""
    base = _ollama_base_url()
    try:
        req = urlrequest.Request(f"{base}/api/tags", method="GET")
        with urlrequest.urlopen(req, timeout=3) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception:
        return []
    out = []
    for item in payload.get("models") or []:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "").strip()
        if not name:
            continue
        caps = item.get("capabilities") or []
        lower = name.lower()
        if "embed" in caps or "embedding" in caps or "embed" in lower:
            out.append(name)
    return out


def _resolve_embed_model():
    preferred = os.environ.get("CNEXUS_EMBED_MODEL", "").strip()
    installed = _ollama_list_embed_models()
    if preferred:
        for name in installed:
            if name == preferred or name.startswith(preferred + ":"):
                return name
        if "embed" not in preferred.lower():
            return preferred
    if installed:
        return installed[0]
    return preferred or "nomic-embed-text"


def _embedding_cache_key(text, backend):
    return f"{backend}:{text}"


def _cache_embedding_vector(text, backend, vector):
    if not text or not vector:
        return
    with _vector_cache_lock:
        _VECTOR_CACHE[_embedding_cache_key(text, backend)] = vector


def _get_cached_embedding(text, backend=None):
    text = str(text or "").strip()
    if not text:
        return []
    with _vector_cache_lock:
        if backend:
            return list(_VECTOR_CACHE.get(_embedding_cache_key(text, backend)) or [])
        for name in ("ollama", "cloud"):
            cached = _VECTOR_CACHE.get(_embedding_cache_key(text, name))
            if cached:
                return list(cached)
    return []


def _get_ollama_embedding(text):
    """Zero-dependency local embedding via Ollama /api/embeddings."""
    text = str(text or "").strip()
    if not text:
        return []
    cached = _get_cached_embedding(text, "ollama")
    if cached:
        return cached
    if not _probe_ollama():
        return []
    model = _resolve_embed_model()
    url = f"{_ollama_base_url()}/api/embeddings"
    body = json.dumps({"model": model, "prompt": text}).encode("utf-8")
    try:
        req = urlrequest.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlrequest.urlopen(req, timeout=5.0) as response:
            res_data = json.loads(response.read().decode("utf-8", errors="replace"))
            vector = res_data.get("embedding") or []
            if vector:
                _cache_embedding_vector(text, "ollama", vector)
                return vector
    except Exception as exc:
        _append_runtime_log(f"本地向量降级 · {exc}", category="embed", level="warn")
    return []


def _call_cloud_embeddings_api(text):
    """Elastic cloud fallback — only when API keys are explicitly configured."""
    text = str(text or "").strip()
    if not text:
        return []
    cached = _get_cached_embedding(text, "cloud")
    if cached:
        return cached

    deepseek_key = (os.environ.get("DEEPSEEK_API_KEY") or "").strip()
    openai_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if deepseek_key:
        url = (os.environ.get("DEEPSEEK_EMBED_URL") or "https://api.deepseek.com/v1/embeddings").rstrip("/")
        model = (os.environ.get("CNEXUS_CLOUD_EMBED_MODEL") or "deepseek-embedding-v2").strip()
        api_key = deepseek_key
        provider = "deepseek"
    elif openai_key:
        url = (os.environ.get("OPENAI_EMBED_URL") or "https://api.openai.com/v1/embeddings").rstrip("/")
        model = (os.environ.get("CNEXUS_CLOUD_EMBED_MODEL") or "text-embedding-3-small").strip()
        api_key = openai_key
        provider = "openai"
    else:
        return []

    body = json.dumps({"model": model, "input": text}).encode("utf-8")
    try:
        req = urlrequest.Request(
            url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        with urlrequest.urlopen(req, timeout=12.0) as response:
            res_data = json.loads(response.read().decode("utf-8", errors="replace"))
            vector = None
            if isinstance(res_data.get("embedding"), list):
                vector = res_data["embedding"]
            else:
                rows = res_data.get("data") or []
                if rows and isinstance(rows[0], dict):
                    vector = rows[0].get("embedding")
            if vector:
                _cache_embedding_vector(text, "cloud", vector)
                _append_runtime_log(
                    f"云端向量容灾 · provider={provider} dim={len(vector)}",
                    category="embed",
                    level="info",
                )
                return vector
    except Exception as exc:
        _append_runtime_log(f"云端向量降级 · {exc}", category="embed", level="warn")
    return []


def _get_embedding_with_fallback(text):
    """
    智能向量检索层：优先本地 Ollama，本地断供后仅在配置了密钥时弹性降级云端；
    仍失败则返回空向量，虫洞协议自动退化为纯文本图谱关联。
    """
    text = str(text or "").strip()
    if not text:
        return []

    cached = _get_cached_embedding(text)
    if cached:
        return cached

    embedding = _get_ollama_embedding(text)
    if embedding:
        return embedding

    cloud_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if cloud_key:
        return _call_cloud_embeddings_api(text)

    return []


def _wormhole_embedding_backend():
    """Use one vector space per wormhole pass (avoid mixed local/cloud dimensions)."""
    if _probe_ollama() and _ollama_list_embed_models():
        return "ollama"
    if (os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")):
        return "cloud"
    return None


def _get_wormhole_embedding(text, backend):
    text = str(text or "").strip()
    if not text or not backend:
        return []
    cached = _get_cached_embedding(text, backend)
    if cached:
        return cached
    if backend == "ollama":
        return _get_ollama_embedding(text)
    if backend == "cloud":
        return _call_cloud_embeddings_api(text)
    return _get_embedding_with_fallback(text)


def _calculate_cosine_similarity(v1, v2):
    """Pure-Python cosine similarity."""
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_a = sum(a * a for a in v1) ** 0.5
    norm_b = sum(b * b for b in v2) ** 0.5
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def _has_physical_link(a, b, adj):
    return b in adj.get(a, set()) or a in adj.get(b, set())


def _wormhole_links_store():
    return _engine_state.setdefault("activation", {}).setdefault("wormhole_links", [])


def _wormhole_links_snapshot():
    links = _wormhole_links_store()
    return [
        {
            "source": link.get("source"),
            "target": link.get("target"),
            "similarity": link.get("similarity"),
            "energy": link.get("energy"),
        }
        for link in links
    ]


def _spread_wormhole_resonance(seed_ids, specs, adj, scores):
    """Dual-track diffusion: semantic wormhole radiation after physical spread."""
    if not seed_ids or not specs:
        _wormhole_links_store()[:] = []
        return []

    embed_backend = _wormhole_embedding_backend()
    if not embed_backend:
        _wormhole_links_store()[:] = []
        return []

    by_id = {spec["id"]: spec for spec in specs}
    links = []
    seen_pairs = set()
    denom = max(1e-9, 1.0 - _WORMHOLE_SIM_THRESHOLD)

    for sid in seed_ids:
        if sid not in by_id:
            continue
        source_energy = float(scores.get(sid, 0.0))
        if source_energy < 0.05:
            continue
        active_vector = _get_wormhole_embedding(_node_embedding_text(by_id[sid]), embed_backend)
        if not active_vector:
            continue

        candidates = []
        for tid, spec in by_id.items():
            if tid == sid or _has_physical_link(sid, tid, adj):
                continue
            pair = tuple(sorted((sid, tid)))
            if pair in seen_pairs:
                continue
            text = _node_embedding_text(spec)
            if len(text) < 2:
                continue
            candidates.append((tid, text, float(scores.get(tid, 0.0))))

        candidates.sort(key=lambda x: -x[2])
        compared = 0
        for tid, target_text, _ in candidates:
            if compared >= _WORMHOLE_MAX_COMPARE:
                break
            pair = tuple(sorted((sid, tid)))
            if pair in seen_pairs:
                continue
            target_vector = _get_wormhole_embedding(target_text, embed_backend)
            if not target_vector:
                continue
            compared += 1
            similarity = _calculate_cosine_similarity(active_vector, target_vector)
            if similarity < _WORMHOLE_SIM_THRESHOLD:
                continue
            normalized_sim = (similarity - _WORMHOLE_SIM_THRESHOLD) / denom
            radiated = source_energy * normalized_sim * _WORMHOLE_ENERGY_COEFF
            scores[tid] = min(_ACTIVATION_MAX_SCORE, scores.get(tid, 0.0) + radiated)
            seen_pairs.add(pair)
            links.append({
                "source": sid,
                "target": tid,
                "similarity": round(similarity, 4),
                "energy": round(radiated, 4),
            })

    links.sort(key=lambda x: (-x["similarity"], -x["energy"]))
    capped = links[:_WORMHOLE_MAX_LINKS]
    store = _wormhole_links_store()
    store[:] = capped
    return capped


def _spread_activation(seed_ids, adj, scores):
    hop1 = set()
    for sid in seed_ids:
        for nb in adj.get(sid, ()):
            if nb not in seed_ids:
                hop1.add(nb)
    hop2 = set()
    for h1 in hop1:
        for nb in adj.get(h1, ()):
            if nb not in seed_ids and nb not in hop1:
                hop2.add(nb)
    for sid in seed_ids:
        scores[sid] = min(_ACTIVATION_MAX_SCORE, scores.get(sid, 0.0) + _ACTIVATION_SEED_PULSE)
    for nid in hop1:
        scores[nid] = min(_ACTIVATION_MAX_SCORE, scores.get(nid, 0.0) + _ACTIVATION_SPREAD_HOP1)
    for nid in hop2:
        scores[nid] = min(_ACTIVATION_MAX_SCORE, scores.get(nid, 0.0) + _ACTIVATION_SPREAD_HOP2)


def _count_active_scores(scores):
    return sum(1 for v in scores.values() if float(v) > _ACTIVATION_THRESHOLD)


def _activation_post_turn(user_text, reply, trace_id):
    with _activation_lock:
        scores = _activation_scores()
        specs = _collect_memory_node_specs()
        _sync_activation_nodes(specs)
        for nid in list(scores.keys()):
            scores[nid] = float(scores[nid]) * _ACTIVATION_DECAY
        adj = _build_activation_adjacency(specs)
        seeds = _match_seed_node_ids(user_text, specs) | _match_seed_node_ids(reply, specs)
        if trace_id:
            for spec in specs:
                if spec.get("cluster") == trace_id or spec["id"] == trace_id or spec["id"].startswith(trace_id):
                    seeds.add(spec["id"])
        if not seeds and specs:
            for spec in reversed(specs):
                if spec.get("tag") == "episode":
                    seeds.add(spec["id"])
                    break
        _spread_activation(seeds, adj, scores)
        wormholes = _spread_wormhole_resonance(seeds, specs, adj, scores)
        active_n = _count_active_scores(scores)
    _append_runtime_log(
        (
            f"潜意识扩散 · seeds={len(seeds)} active>{_ACTIVATION_THRESHOLD}={active_n} "
            f"wormholes={len(wormholes)}"
        ),
        category="cognition",
        trace_id=trace_id,
    )


def _schedule_activation_post_turn(user_text, reply, trace_id):
    threading.Thread(
        target=_activation_post_turn,
        args=(user_text, reply, trace_id),
        daemon=True,
        name="cnexus-activation-spread",
    ).start()
    _background_cognitive_update()


def _consolidation_state():
    return _engine_state.setdefault("consolidation", {})


def _touch_user_activity():
    _consolidation_state()["last_activity_at"] = time.time()


def _consolidation_status():
    c = _consolidation_state()
    specs = _collect_memory_node_specs()
    scores = _activation_scores()
    active_nodes = sum(1 for spec in specs if float(scores.get(spec["id"], 0.0)) > _ACTIVATION_THRESHOLD)
    semantic_facts = sum(
        1 for b in _engine_state["memory_store"].blocks
        if b.get("label") == "semantic" or str(b.get("block_id", "")).startswith("sem-rem-")
    )
    now = time.time()
    idle_seconds = max(0, int(now - float(c.get("last_activity_at", now))))
    return {
        "rem_running": bool(c.get("rem_running")),
        "rem_due": _should_trigger_rem_sleep(),
        "idle_seconds": idle_seconds,
        "active_nodes": active_nodes,
        "node_count": len(specs),
        "semantic_facts": semantic_facts,
        "total_pruned": int(c.get("total_pruned", 0)),
        "total_facts": int(c.get("total_facts", 0)),
        "last_shallow_at": c.get("last_shallow_at"),
        "last_rem_at": c.get("last_rem_at"),
        "last_rem_report": c.get("last_rem_report"),
    }


def _background_cognitive_update():
    """浅度睡眠：对话后轻量代谢，不阻塞主链。"""
    try:
        c = _consolidation_state()
        c["last_shallow_at"] = time.time()
        trace = _engine_state.get("trace", [])
        if len(trace) > 40:
            _engine_state["trace"] = trace[-35:]
        scores = _activation_scores()
        live_ids = {spec["id"] for spec in _collect_memory_node_specs()}
        for nid in list(scores.keys()):
            if nid not in live_ids:
                scores.pop(nid, None)
        if len(_engine_state.get("gtbs_events", [])) > 1500:
            _engine_state["gtbs_events"] = _engine_state["gtbs_events"][-1500:]
    except Exception:
        pass


def _should_trigger_rem_sleep():
    c = _consolidation_state()
    if c.get("rem_running"):
        return False
    now = time.time()
    if now - float(c.get("last_rem_at", 0)) < _REM_COOLDOWN_SECONDS:
        return False
    idle = now - float(c.get("last_activity_at", now))
    if idle >= _REM_IDLE_SECONDS:
        return True
    if time.localtime().tm_hour == 3 and idle >= 300:
        return True
    specs = _collect_memory_node_specs()
    scores = _activation_scores()
    active = sum(1 for spec in specs if float(scores.get(spec["id"], 0.0)) > _ACTIVATION_THRESHOLD)
    if active >= _REM_ACTIVE_NODE_THRESHOLD:
        return True
    if len(specs) >= _REM_NODE_THRESHOLD:
        return True
    return False


def _protected_node_ids(specs):
    protected = {"goal-current"}
    for spec in specs:
        nid = spec["id"]
        if nid.startswith("sem-rem-") or spec.get("tag") in ("code_class", "code_function", "vision_component"):
            protected.add(nid)
    for entry in _engine_state.get("trace", [])[-5:]:
        trace_id = entry.get("trace_id") or f"v2-trace-{entry.get('iteration', 0)}"
        protected.add(trace_id)
        protected.add(f"{trace_id}-intent")
    return protected


def _rem_remove_blocks_for_iterations(iterations):
    removed = 0
    it_set = {int(i) for i in iterations}
    ms = _engine_state["memory_store"]
    kept = []
    for block in ms.blocks:
        block_id = str(block.get("block_id", ""))
        drop = False
        if block_id.startswith("ep:it"):
            try:
                if int(block_id.split("ep:it", 1)[1]) in it_set:
                    drop = True
            except Exception:
                pass
        if not drop:
            for it in it_set:
                if block_id.startswith(f"kw-ep:it{it}-"):
                    drop = True
                    break
        if drop:
            removed += 1
        else:
            kept.append(block)
    ms.blocks = kept
    return removed


def _rem_remove_traces(trace_ids, iterations):
    trace = _engine_state.get("trace", [])
    id_set = set(trace_ids)
    it_set = {int(i) for i in iterations}
    kept = []
    removed = 0
    for entry in trace:
        tid = entry.get("trace_id")
        it = int(entry.get("iteration", 0))
        if tid in id_set or it in it_set:
            removed += 1
        else:
            kept.append(entry)
    _engine_state["trace"] = kept
    return removed


def _rem_synaptic_prune(report):
    specs = _collect_memory_node_specs()
    adj = _build_activation_adjacency(specs)
    scores = _activation_scores()
    protected = _protected_node_ids(specs)
    pruned_ids = set()

    for spec in specs:
        nid = spec["id"]
        if nid in protected or nid.startswith("sem-rem-"):
            continue
        score = float(scores.get(nid, 0.0))
        degree = len(adj.get(nid, set()))
        tag = spec.get("tag", "term")
        if score > _REM_SCORE_PRUNE_MAX:
            continue
        if tag in ("goal", "identity", "belief", "episode") and degree > 0:
            continue
        if tag in ("term", "insight") and degree <= 1:
            pruned_ids.add(nid)

    block_removed = 0
    ms = _engine_state["memory_store"]
    kept_blocks = []
    for block in ms.blocks:
        block_id = str(block.get("block_id", ""))
        if block.get("label") == "semantic" or block_id.startswith("sem-rem-"):
            kept_blocks.append(block)
            continue
        drop = block_id in pruned_ids
        if not drop:
            for nid in pruned_ids:
                if block_id.startswith(f"kw-{nid}-") or (nid.startswith("kw-") and nid == block_id):
                    drop = True
                    break
        if not drop and block.get("label") not in ("emotion", "persona", "semantic"):
            imp = float(block.get("importance", 1))
            if block_id.startswith("kw-") and imp < 0.55 and float(scores.get(block_id, 0.0)) <= _REM_SCORE_PRUNE_MAX:
                drop = True
        if drop:
            block_removed += 1
            pruned_ids.add(block_id)
        else:
            kept_blocks.append(block)
    ms.blocks = kept_blocks

    for nid in list(pruned_ids):
        scores.pop(nid, None)

    report["pruned_nodes"] = len(pruned_ids)
    report["pruned_blocks"] = block_removed
    c = _consolidation_state()
    c["total_pruned"] = int(c.get("total_pruned", 0)) + len(pruned_ids)
    return pruned_ids


def _rem_collect_compaction_sources():
    now = time.time()
    trace = list(_engine_state.get("trace", []))
    keep_recent = max(_REM_TRACE_KEEP, 5)
    to_compact = trace[:-keep_recent] if len(trace) > keep_recent else []
    week_cutoff = now - _REM_COMPACT_WINDOW_SECONDS
    filtered = []
    for entry in to_compact:
        ts = float(entry.get("timestamp") or 0)
        if ts and ts > week_cutoff:
            filtered.append(entry)
        elif not ts:
            filtered.append(entry)
    to_compact = filtered or to_compact

    sources = []
    for entry in to_compact:
        iteration = int(entry.get("iteration", 0))
        trace_id = entry.get("trace_id") or f"v2-trace-{iteration}"
        inp = str(entry.get("input") or "").strip()
        reply = _speech_text(entry.get("speech") or {})
        text = "\n".join(x for x in (inp, reply) if x).strip()
        if not text:
            continue
        sources.append({
            "type": "trace",
            "iteration": iteration,
            "trace_id": trace_id,
            "text": text[:600],
        })

    specs = _collect_memory_node_specs()
    scores = _activation_scores()
    for spec in specs:
        if spec["id"].startswith("sem-rem-"):
            continue
        if spec.get("tag") in ("term", "insight") and float(scores.get(spec["id"], 0.0)) >= 0.5:
            blob = f"{spec.get('title', '')} {spec.get('desc', '')}".strip()
            if blob:
                sources.append({"type": "node", "id": spec["id"], "text": blob[:240]})

    return sources, to_compact


def _parse_consolidation_facts(raw_text):
    facts = []
    for line in str(raw_text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        for prefix in ("- ", "* ", "• "):
            if line.startswith(prefix):
                line = line[len(prefix):].strip()
        line = line.lstrip("0123456789.) ").strip()
        if len(line) >= 6:
            facts.append(line[:320])
        if len(facts) >= _REM_MAX_FACTS:
            break
    return facts[:_REM_MAX_FACTS]


def _heuristic_compact_facts(sources):
    facts = []
    seen = set()
    for src in sources:
        text = src.get("text", "")
        snippet = text.split("\n", 1)[0].strip()
        if len(snippet) >= 8 and snippet not in seen:
            seen.add(snippet)
            facts.append(f"经对话沉淀：{snippet[:180]}")
        for kw in _extract_keywords(text, 4):
            if kw.lower() not in seen:
                seen.add(kw.lower())
                facts.append(f"用户关注主题：{kw}")
        if len(facts) >= _REM_MAX_FACTS:
            break
    return facts[:_REM_MAX_FACTS] or ["近期交互不足以形成新的长期常识节点"]


def _invoke_consolidation_llm(sources):
    fragments = []
    for i, src in enumerate(sources[:24], 1):
        fragments.append(f"[{i}] {src.get('text', '')[:400]}")
    corpus = "\n".join(fragments)
    if not corpus.strip():
        return []

    model_row = _resolve_model_row(None)
    if model_row and model_row.get("provider") == "ollama":
        _sync_ollama_registry()
        model_row = _resolve_model_row(None)
    if not _should_use_external_llm(model_row):
        return _heuristic_compact_facts(sources)

    prompt = (
        "你是 CNexus 潜意识反思者。请阅读以下零散对话与记忆碎片，提炼 3-5 条高度浓缩、可长期复用的常识性事实。\n"
        "要求：每条一行，不要编号以外的多余解释；中文输出；避免重复；保留用户真实意图。\n\n"
        f"{corpus}"
    )
    try:
        usage = _invoke_external_llm(model_row, prompt, memory_context=None)
        facts = _parse_consolidation_facts(usage.get("reply", ""))
        return facts or _heuristic_compact_facts(sources)
    except Exception:
        return _heuristic_compact_facts(sources)


def _rem_apply_compaction(facts, to_compact, report):
    if not facts:
        return
    now = time.time()
    batch_id = int(now * 1000)
    scores = _activation_scores()
    ms = _engine_state["memory_store"]

    for i, fact in enumerate(facts, 1):
        block_id = f"sem-rem-{batch_id}-{i}"
        keywords = _extract_keywords(fact, 5)
        ms.add({
            "label": "semantic",
            "block_id": block_id,
            "data": {
                "content": fact,
                "label": "REM semantic fact",
                "keywords": keywords,
                "consolidated_at": now,
                "source_count": len(to_compact),
            },
            "importance": 0.95,
            "timestamp": now,
        })
        scores[block_id] = _ACTIVATION_MAX_SCORE
        for kw in keywords:
            kid = f"kw-{block_id}-{kw}"
            scores[kid] = min(_ACTIVATION_MAX_SCORE, 0.75)

    if to_compact:
        trace_ids = [e.get("trace_id") for e in to_compact if e.get("trace_id")]
        iterations = [int(e.get("iteration", 0)) for e in to_compact]
        report["pruned_traces"] = _rem_remove_traces(trace_ids, iterations)
        report["pruned_blocks"] = report.get("pruned_blocks", 0) + _rem_remove_blocks_for_iterations(iterations)

    c = _consolidation_state()
    c["total_facts"] = int(c.get("total_facts", 0)) + len(facts)
    report["facts_created"] = len(facts)


def _rem_reanchor_graph(facts, report):
    scores = _activation_scores()
    if "goal-current" in scores:
        scores["goal-current"] = max(float(scores.get("goal-current", 0.0)), 0.35)
    for block in _engine_state["memory_store"].blocks:
        block_id = str(block.get("block_id", ""))
        if block_id.startswith("sem-rem-"):
            scores[block_id] = _ACTIVATION_MAX_SCORE
    report["reanchored"] = len(facts)


def _run_rem_deep_sleep(force=False):
    if not force and not _should_trigger_rem_sleep():
        return {"ok": True, "skipped": "not_due", "status": _consolidation_status()}

    with _rem_lock:
        c = _consolidation_state()
        if c.get("rem_running"):
            return {"ok": True, "skipped": "running", "status": _consolidation_status()}
        c["rem_running"] = True

    report = {
        "ok": True,
        "phase": "rem_deep_sleep",
        "started_at": time.time(),
        "pruned_nodes": 0,
        "pruned_blocks": 0,
        "pruned_traces": 0,
        "facts_created": 0,
        "reanchored": 0,
    }
    trace_id = f"rem-{int(time.time())}"
    try:
        _rem_synaptic_prune(report)
        sources, to_compact = _rem_collect_compaction_sources()
        report["compaction_sources"] = len(sources)
        facts = []
        if sources:
            facts = _invoke_consolidation_llm(sources)
            _rem_apply_compaction(facts, to_compact, report)
            _rem_reanchor_graph(facts, report)
        else:
            report["skipped_compaction"] = "no_sources"

        c = _consolidation_state()
        c["last_rem_at"] = time.time()
        c["last_rem_report"] = {
            **report,
            "finished_at": time.time(),
        }
        _append_runtime_log(
            (
                f"REM深度睡眠 · pruned={report.get('pruned_nodes', 0)} "
                f"traces={report.get('pruned_traces', 0)} facts={report.get('facts_created', 0)}"
            ),
            category="cognition",
            trace_id=trace_id,
        )
    except Exception as exc:
        report["ok"] = False
        report["error"] = str(exc)
        _append_runtime_log(f"REM深度睡眠失败 · {exc}", category="cognition", level="error", trace_id=trace_id)
    finally:
        _consolidation_state()["rem_running"] = False

    report["status"] = _consolidation_status()
    return report


def _rem_watchdog_loop():
    while True:
        try:
            time.sleep(_REM_WATCHDOG_INTERVAL)
            if _should_trigger_rem_sleep():
                _run_rem_deep_sleep(force=False)
        except Exception:
            pass


def _start_rem_watchdog():
    threading.Thread(
        target=_rem_watchdog_loop,
        daemon=True,
        name="cnexus-rem-watchdog",
    ).start()


# ── Multi-Modal Ingestion & Code AST Projection ─────────────────────────


def _ollama_list_vision_models():
    base = _ollama_base_url()
    try:
        req = urlrequest.Request(f"{base}/api/tags", method="GET")
        with urlrequest.urlopen(req, timeout=3) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception:
        return []
    out = []
    for item in payload.get("models") or []:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "").strip()
        if not name:
            continue
        lower = name.lower()
        caps = item.get("capabilities") or []
        if any(k in lower for k in ("llava", "bakllava", "vision", "qwen2-vl", "moondream")):
            out.append(name)
        elif "vision" in caps or "image" in caps:
            out.append(name)
    return out


def _resolve_vision_model():
    preferred = os.environ.get("CNEXUS_VISION_MODEL", _CNEXUS_VISION_MODEL).strip() or "llava"
    installed = _ollama_list_vision_models()
    if not installed:
        return preferred
    for name in installed:
        if name == preferred or name.startswith(preferred + ":"):
            return name
    for name in installed:
        if preferred.split(":")[0] in name:
            return name
    return installed[0]


def _parse_visual_relationships(raw_text):
    nodes = {}
    links = []
    for line in str(raw_text or "").splitlines():
        line = line.strip()
        if "->" not in line:
            continue
        parts = re.split(r"\s*->\s*", line, maxsplit=1)
        if len(parts) != 2:
            continue
        a, b = parts[0].strip(" -•*\t"), parts[1].strip(" -•*\t")
        if not a or not b:
            continue
        aid = f"vision:{a}"[:120]
        bid = f"vision:{b}"[:120]
        nodes[aid] = {"id": aid, "label": a[:120], "type": "vision_component", "title": a[:120]}
        nodes[bid] = {"id": bid, "label": b[:120], "type": "vision_component", "title": b[:120]}
        links.append({"source": aid, "target": bid, "type": "vision_flow"})
    return list(nodes.values()), links


def _analyze_architecture_image(image_base64):
    """Ollama vision model → structured component graph."""
    raw = str(image_base64 or "").strip()
    if not raw:
        return [], []
    if "," in raw:
        raw = raw.split(",", 1)[1]
    if not _probe_ollama():
        return [], []
    model = _resolve_vision_model()
    url = f"{_ollama_base_url()}/api/generate"
    prompt = (
        "Identify key system components, blocks, or modules in this architecture diagram.\n"
        "Output ONLY a list of components and their connections in this format:\n"
        "ComponentA -> ComponentB\n"
        "ComponentC -> ComponentA"
    )
    body = {
        "model": model,
        "prompt": prompt,
        "images": [raw],
        "stream": False,
    }
    try:
        req = urlrequest.Request(
            url,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlrequest.urlopen(req, timeout=30.0) as response:
            res_data = json.loads(response.read().decode("utf-8", errors="replace"))
            raw_text = res_data.get("response", "")
            return _parse_visual_relationships(raw_text)
    except Exception as exc:
        _append_runtime_log(f"视觉摄入失败 · {exc}", category="capture", level="warn")
        return [], []


def _project_code_ast(file_content, file_name):
    """Stdlib AST projection — classes, functions, inheritance in ~1ms."""
    nodes = []
    links = []
    file_name = str(file_name or "snippet.py").strip() or "snippet.py"
    try:
        tree = ast.parse(file_content or "", filename=file_name)
    except SyntaxError as se:
        return {"nodes": nodes, "links": links, "error": str(se)}
    except Exception as exc:
        return {"nodes": nodes, "links": links, "error": str(exc)}

    class_stack = []

    class _AstProjector(ast.NodeVisitor):
        def visit_ClassDef(self, node):
            class_id = f"class:{file_name}:{node.name}"
            nodes.append({
                "id": class_id,
                "label": f"Class: {node.name}",
                "title": f"Class: {node.name}",
                "type": "code_class",
                "file": file_name,
            })
            for base in node.bases:
                base_name = None
                if isinstance(base, ast.Name):
                    base_name = base.id
                elif isinstance(base, ast.Attribute):
                    base_name = base.attr
                if base_name:
                    target = f"class_inherits:{base_name}"
                    links.append({"source": class_id, "target": target, "type": "inherits"})
                    nodes.append({
                        "id": target,
                        "label": f"Ext: {base_name}",
                        "title": f"Ext: {base_name}",
                        "type": "code_class",
                        "file": file_name,
                    })
            class_stack.append(node.name)
            self.generic_visit(node)
            class_stack.pop()

        def visit_FunctionDef(self, node):
            func_id = f"func:{file_name}:{node.name}"
            nodes.append({
                "id": func_id,
                "label": f"Def: {node.name}()",
                "title": f"Def: {node.name}()",
                "type": "code_function",
                "file": file_name,
            })
            if class_stack:
                parent_id = f"class:{file_name}:{class_stack[-1]}"
                links.append({"source": parent_id, "target": func_id, "type": "defines"})
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node):
            func_id = f"func:{file_name}:{node.name}"
            nodes.append({
                "id": func_id,
                "label": f"Def: {node.name}()",
                "title": f"Def: {node.name}()",
                "type": "code_function",
                "file": file_name,
            })
            if class_stack:
                parent_id = f"class:{file_name}:{class_stack[-1]}"
                links.append({"source": parent_id, "target": func_id, "type": "defines"})
            self.generic_visit(node)

    _AstProjector().visit(tree)
    dedup = {}
    for n in nodes:
        dedup[n["id"]] = n
    return {"nodes": list(dedup.values()), "links": links, "file": file_name}


def _register_projection(nodes, links, cluster, source_kind="code"):
    """Write AST/vision nodes into projection store + memory blocks."""
    proj = _projection_store()
    now = time.time()
    scores = _activation_scores()
    registered_ids = []
    parent_by_target = {}
    for link in links:
        if link.get("type") == "defines":
            parent_by_target[link["target"]] = link["source"]

    for node in nodes:
        nid = str(node.get("id") or "").strip()
        if not nid:
            continue
        ntype = node.get("type") or "term"
        title = str(node.get("label") or node.get("title") or nid)[:120]
        parent_id = parent_by_target.get(nid, "")
        record = {
            "id": nid,
            "title": title,
            "tag": ntype,
            "node_type": ntype,
            "desc": f"{source_kind}:{node.get('file', cluster)}"[:160],
            "meta": source_kind,
            "cluster": cluster or nid,
            "parent_id": parent_id,
            "file": node.get("file", ""),
        }
        proj["nodes"][nid] = record
        registered_ids.append(nid)
        scores[nid] = _ACTIVATION_MAX_SCORE
        _engine_state["memory_store"].add({
            "label": ntype,
            "block_id": nid,
            "data": {
                **node,
                **record,
                "content": title,
                "cluster": cluster,
            },
            "importance": 0.95,
            "timestamp": now,
        })

    seen_links = {(l.get("source"), l.get("target"), l.get("type")) for l in proj["links"]}
    for link in links:
        key = (link.get("source"), link.get("target"), link.get("type"))
        if key in seen_links:
            continue
        seen_links.add(key)
        proj["links"].append({
            "source": link.get("source"),
            "target": link.get("target"),
            "type": link.get("type", "rel"),
            "cluster": cluster,
        })

    _schedule_projection_wormhole(registered_ids)
    _touch_user_activity()
    _append_runtime_log(
        f"{'代码' if source_kind == 'code' else '视觉'}投影 · nodes={len(registered_ids)} links={len(links)}",
        category="capture",
    )
    return registered_ids


def _schedule_projection_wormhole(node_ids):
    """Seed full activation + wormhole resonance for newly projected nodes."""
    if not node_ids:
        return

    def _run():
        with _activation_lock:
            specs = _collect_memory_node_specs()
            _sync_activation_nodes(specs)
            scores = _activation_scores()
            for nid in node_ids:
                scores[nid] = _ACTIVATION_MAX_SCORE
            adj = _build_activation_adjacency(specs)
            _spread_wormhole_resonance(set(node_ids), specs, adj, scores)

    threading.Thread(target=_run, daemon=True, name="cnexus-projection-wormhole").start()


def api_ingest_image(data):
    image_b64 = data.get("image_base64") or data.get("image") or ""
    nodes, links = _analyze_architecture_image(image_b64)
    if not nodes:
        return {
            "ok": False,
            "error": "vision_analysis_empty",
            "detail": "Ollama vision unavailable or no relationships parsed",
        }
    cluster = f"vision-{int(time.time() * 1000)}"
    node_ids = _register_projection(nodes, links, cluster, source_kind="vision")
    return {
        "ok": True,
        "nodes": len(nodes),
        "links": len(links),
        "node_ids": node_ids,
        "projection_links": links,
    }


def api_ingest_code(data):
    content = data.get("content") or data.get("source") or ""
    file_name = data.get("file_name") or data.get("filename") or "snippet.py"
    if not str(content).strip():
        return {"ok": False, "error": "missing content"}
    result = _project_code_ast(content, file_name)
    nodes = result.get("nodes") or []
    links = result.get("links") or []
    if not nodes:
        return {
            "ok": False,
            "error": result.get("error") or "ast_empty",
            "detail": "No classes or functions found",
        }
    cluster = f"code:{file_name}"
    node_ids = _register_projection(nodes, links, cluster, source_kind="code")
    return {
        "ok": True,
        "file": file_name,
        "nodes": len(nodes),
        "links": len(links),
        "node_ids": node_ids,
        "projection_links": links,
        "ast_error": result.get("error"),
    }


def gateway_health():
    return {
        "gateway": "alive",
        "operational_ready": True,
        "full_ready": True,
        "boot_phase": "boot_4_ready",
        "cognitive_status": "ready",
        "progress": 100,
        "reachable": True,
        "booted": True,
        "version": "2.0.0-personal",
        "status": "ok",
    }


def system_capability():
    return {
        "api": True,
        "chat": True,
        "memory": True,
        "llm": True,
        "upload": True,
        "full": True,
        "operational_ready": True,
        "full_ready": True,
        "ready_for_chat": True,
        "ready_for_upload": True,
        "status": "ready",
    }


def system_ready():
    return {
        "status": "ready",
        "boot_id": "personal-static",
        "boot_phase": "boot_4_ready",
        "token_valid": True,
        "ws": "disabled",
        "http": "alive",
        "memory": "ready",
        "uptime_ms": int((time.time() - _engine_state["started_at"]) * 1000),
        "version": "2.0.0-personal",
        "operational_ready": True,
        "full_ready": True,
        "ready_for_chat": True,
        "ready_for_upload": True,
        "ready": True,
    }


def memory_stats():
    ms = _engine_state["memory_store"]
    return {"total": len(ms.blocks), "by_layer": {"episodic": len(ms.blocks)}, "avg_importance": 0.6}


def _model_public(row):
    return {
        "id": row["id"],
        "name": row.get("name", row["id"]),
        "provider": row.get("provider", "openai_compatible"),
        "base_url": row.get("base_url", ""),
        "model": row.get("model", ""),
        "api_key_set": bool(row.get("api_key_set") or (row.get("api_key") or "").strip()),
        "is_default": bool(row.get("is_default")),
        "enabled": bool(row.get("enabled", True)),
    }


def _active_chat_model_id():
    for row in _engine_state["model_registry"].values():
        if row.get("is_default") and row.get("enabled", True):
            return row["id"]
    for row in _engine_state["model_registry"].values():
        if row.get("enabled", True):
            return row["id"]
    return "cnexus-local"


def api_models():
    _sync_ollama_registry()
    rows = [_model_public(row) for row in _engine_state["model_registry"].values()]
    rows.sort(key=lambda r: (not r["is_default"], r["name"]))
    return {"models": rows}


def _upsert_model(model_id, body, create=False):
    registry = _engine_state["model_registry"]
    if create and model_id in registry:
        return None, "model_exists"
    if not create and model_id not in registry:
        if model_id in _default_model_registry():
            registry[model_id] = dict(_default_model_registry()[model_id])
        else:
            return None, "not_found"

    row = dict(registry.get(model_id, {"id": model_id}))
    for key in ("name", "provider", "base_url", "model"):
        if key in body and body[key] is not None:
            row[key] = body[key]
    if "api_key" in body:
        row["api_key"] = str(body.get("api_key") or "")
        row["api_key_set"] = bool(str(body.get("api_key") or "").strip()) or row.get("provider") == "ollama"
    if "enabled" in body:
        row["enabled"] = bool(body["enabled"])
    if "is_default" in body and body["is_default"]:
        for other in registry.values():
            other["is_default"] = False
        row["is_default"] = True
    elif "is_default" in body:
        row["is_default"] = bool(body["is_default"])

    if row.get("provider") == "ollama":
        row["api_key_set"] = True
    registry[model_id] = row
    return _model_public(row), None


def create_model(body):
    preset_id = (body.get("presetId") or body.get("preset_id") or "").strip()
    if preset_id:
        model_id = preset_id
        row, err = _upsert_model(model_id, body, create=False)
        if err == "not_found":
            row, err = _upsert_model(model_id, {**body, "id": model_id}, create=True)
    else:
        model_id = f"custom-{int(time.time()*1000)}"
        registry = _engine_state["model_registry"]
        registry[model_id] = {
            "id": model_id,
            "name": body.get("name") or "Custom Model",
            "provider": body.get("provider") or "openai_compatible",
            "base_url": body.get("base_url") or "",
            "model": body.get("model") or "",
            "api_key": body.get("api_key") or "",
            "api_key_set": bool((body.get("api_key") or "").strip()),
            "is_default": bool(body.get("is_default")),
            "enabled": bool(body.get("enabled", True)),
        }
        row, err = _upsert_model(model_id, body, create=False)
    if err:
        return None, err
    return row, None


def test_model(model_id):
    registry = _engine_state["model_registry"]
    row = registry.get(model_id)
    if not row and model_id in _default_model_registry():
        row = dict(_default_model_registry()[model_id])
        registry[model_id] = row
    if not row:
        return {"success": False, "detail": f"model not found: {model_id}"}

    provider = row.get("provider", "")
    if provider == "cnexus":
        return {"success": True, "detail": "CNexus 内置认知内核可用"}
    if provider == "ollama":
        host = (row.get("base_url") or f"http://{OLLAMA_HOST}").rstrip("/")
        try:
            installed = _ollama_list_chat_models(host)
            target = row.get("model") or ""
            resolved = _resolve_ollama_model_name(target, installed) if installed else target
            if resolved and resolved != target:
                row["model"] = resolved
                registry[model_id] = row
            if installed and resolved:
                probe = json.dumps({
                    "model": resolved,
                    "messages": [{"role": "user", "content": "ping"}],
                    "stream": False,
                }).encode("utf-8")
                req = urlrequest.Request(
                    f"{host}/api/chat",
                    data=probe,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urlrequest.urlopen(req, timeout=30) as resp:
                    json.loads(resp.read().decode("utf-8", errors="replace"))
                return {"success": True, "detail": f"Ollama 已连接 · 模型 {resolved}"}
            if not installed:
                return {"success": False, "detail": "Ollama 已运行但未找到可对话模型，请先 ollama pull"}
            return {"success": True, "detail": f"Ollama 已连接，可用模型 {len(installed)} 个"}
        except Exception as exc:
            return {"success": False, "detail": f"Ollama 不可达: {exc}"}

    if not (row.get("api_key") or "").strip() and provider != "ollama":
        return {"success": False, "detail": "未配置 API Key"}
    return {"success": True, "detail": "API Key 已保存（个人版跳过云端连通性实测）"}


def _ollama_base_url():
    row = _engine_state["model_registry"].get("ollama-local") or {}
    return (row.get("base_url") or f"http://{OLLAMA_HOST}").rstrip("/")


def _ollama_list_chat_models(base_url=None):
    """Return full Ollama model names that support chat/completion (not embed-only)."""
    base = (base_url or _ollama_base_url()).rstrip("/")
    try:
        req = urlrequest.Request(f"{base}/api/tags", method="GET")
        with urlrequest.urlopen(req, timeout=3) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception:
        return []
    out = []
    for item in payload.get("models") or []:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "").strip()
        if not name:
            continue
        caps = item.get("capabilities") or []
        lower = name.lower()
        if caps and not any(c in caps for c in ("completion", "chat", "tools")):
            continue
        if "embed" in lower and not any(c in caps for c in ("completion", "chat", "tools")):
            continue
        out.append(name)
    return out


def _resolve_ollama_model_name(preferred, installed):
    """Map registry name (e.g. llama3.2) to installed tag (e.g. llama3.2:3b)."""
    preferred = str(preferred or "").strip()
    if not installed:
        return preferred or "llama3.2"
    if preferred in installed:
        return preferred
    for name in installed:
        base = name.split(":")[0]
        if base == preferred or name.startswith(preferred + ":"):
            return name
    return installed[0]


def _sync_ollama_registry():
    """Probe local Ollama and enable ollama-local when the service is reachable."""
    registry = _engine_state["model_registry"]
    row = registry.get("ollama-local")
    if not row:
        return ollama_status()
    base = _ollama_base_url()
    installed = _ollama_list_chat_models(base)
    running = bool(installed) or _probe_ollama()

    if running and installed:
        preferred = str(row.get("model") or "llama3.2")
        row["model"] = _resolve_ollama_model_name(preferred, installed)
        row["enabled"] = True
        row["api_key_set"] = True
        cloud_ready = any(
            other.get("id") not in ("ollama-local", "cnexus-local")
            and other.get("enabled")
            and other.get("provider") not in ("cnexus", "ollama", "")
            and (other.get("api_key_set") or bool((other.get("api_key") or "").strip()))
            for other in registry.values()
        )
        if not cloud_ready:
            for other in registry.values():
                other["is_default"] = False
            row["is_default"] = True
    elif running:
        row["enabled"] = True
        row["api_key_set"] = True
    else:
        row["enabled"] = False
        if row.get("is_default"):
            row["is_default"] = False
            local = registry.get("cnexus-local")
            if local:
                local["is_default"] = True

    registry["ollama-local"] = row
    return ollama_status()


def _probe_ollama():
    try:
        req = urlrequest.Request(f"{_ollama_base_url()}/api/tags", method="GET")
        with urlrequest.urlopen(req, timeout=2) as resp:
            return resp.status == 200
    except Exception:
        return False


def _find_ollama_binary():
    found = shutil.which("ollama")
    if found:
        return found
    for candidate in (
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe"),
        os.path.expandvars(r"%ProgramFiles%\Ollama\ollama.exe"),
    ):
        if candidate and os.path.isfile(candidate):
            return candidate
    return None


def ollama_status():
    binary = _find_ollama_binary()
    running = _probe_ollama()
    return {
        "installed": bool(binary),
        "binary_found": bool(binary),
        "running": running,
        "host": OLLAMA_HOST,
        "download_url": "https://ollama.com/download",
        "binary_path": binary,
    }


def ollama_start():
    if _probe_ollama():
        return {"ok": True, "detail": "already_running", "running": True}
    binary = _find_ollama_binary()
    if not binary:
        return {
            "ok": False,
            "detail": "not_installed",
            "running": False,
            "download_url": "https://ollama.com/download",
        }
    try:
        subprocess.Popen(
            [binary, "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        time.sleep(1.2)
        running = _probe_ollama()
        return {"ok": running, "detail": "started" if running else "start_failed", "running": running}
    except Exception as exc:
        return {"ok": False, "detail": str(exc), "running": False}


def ollama_stop():
    if not _probe_ollama():
        return {"ok": True, "detail": "already_stopped", "running": False}
    return {"ok": False, "detail": "externally_managed", "running": True}


def api_logs(limit=100):
    logs = _engine_state.get("runtime_logs", [])
    tail = logs[-max(1, int(limit)) :]
    return {"logs": tail, "count": len(logs)}


def gtbs_events(limit=300):
    events = _engine_state.get("gtbs_events", [])
    tail = events[-max(1, int(limit)) :]
    return {"events": tail, "count": len(events)}


def execution_status():
    ollama = ollama_status()
    active_id = _active_chat_model_id()
    active_row = _engine_state["model_registry"].get(active_id, {})
    ollama_running = bool(ollama.get("running"))
    return {
        "active_chat_provider": active_id,
        "active_embed_provider": "ollama-local" if ollama_running else None,
        "providers": {
            active_id: {
                "state": "ready",
                "capabilities": ["chat", "memory"],
                "reachable": True,
                "issues": [],
                "details": {"provider": active_row.get("provider")},
            },
            "ollama": {
                "state": "ready" if ollama_running else "offline",
                "capabilities": ["embed", "chat"] if ollama_running else [],
                "reachable": ollama_running,
                "issues": [] if ollama_running else ["Ollama 服务未运行"],
                "details": {"host": ollama.get("host")},
            },
        },
        "suggested_actions": [] if ollama_running else ["start_ollama"],
        "embedding": {"active_mode": "ollama" if ollama_running else "hash"},
        "ollama": {
            "running": ollama_running,
            "installed": bool(ollama.get("installed")),
            "binary_found": bool(ollama.get("binary_found")),
            "host": ollama.get("host"),
            "download_url": ollama.get("download_url"),
            "binary_path": ollama.get("binary_path"),
        },
    }


def _payload_dict(data):
    payload = data.get("payload")
    return payload if isinstance(payload, dict) else {}


def _extract_intent_text(data):
    payload = _payload_dict(data)
    for key in ("message", "text", "input", "content"):
        val = payload.get(key) or data.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return ""


def _handle_gateway_intent(data):
    intent_type = (data.get("type") or "").strip()
    payload = _payload_dict(data)
    text = _extract_intent_text(data)
    trace_id = str(data.get("trace_id") or f"v2-{int(time.time()*1000)}")

    if intent_type == "chat_prepare":
        _prepare_cache[trace_id] = text
        return {
            "trace_id": trace_id,
            "status": "completed",
            "ok": True,
            "result": {
                "prepare_id": trace_id,
                "user_message": text,
                "memory_context": "",
                "governance_injection": "",
                "system_prompt": "CNexus 2.0 Personal Cognitive Kernel",
                "outbound_preview": text,
                "has_injection": False,
                "chat_governance_notes": [],
                "expires_in_seconds": 300,
            },
        }

    if intent_type == "chat_confirm":
        prepare_id = str(payload.get("prepare_id") or trace_id)
        msg = _prepare_cache.get(prepare_id) or text
        try:
            result = _run_6step(msg) if msg else {"reply": "请先输入消息"}
            reply = result.get("reply", "已处理")
        except Exception as exc:
            reply = f"引擎处理异常: {exc}"
        return {
            "trace_id": trace_id,
            "status": "completed",
            "ok": True,
            "result": {
                "reply": reply,
                "model_name": "CNexus 2.0 Local",
                "human_authorized": True,
                "latency_ms": 50,
            },
        }

    if intent_type == "file_process":
        _touch_user_activity()
        file_id = str(payload.get("file_id") or trace_id)
        entry = _file_cache.get(file_id, {})
        content = entry.get("content", "")
        filename = entry.get("filename", "document")
        mem_id = f"mem-{int(time.time()*1000)}"
        keywords = _extract_keywords(content, 6)
        _engine_state["memory_store"].add({
            "label": "episodic",
            "block_id": mem_id,
            "data": {"filename": filename, "content": content[:2000], "keywords": keywords},
            "importance": 0.7,
            "timestamp": time.time(),
        })
        trace_id = f"v2-trace-file-{int(time.time()*1000)}"
        upload_rows = [
            _gtbs_row("proposal", f"{file_id}-upload", trace_id, "file_upload", "gateway_file_upload"),
            _gtbs_row(
                "commit", f"{file_id}-index", trace_id, "capture", "file_process",
                extra={"target_stores": ["episodic"], "filename": filename},
            ),
        ]
        _engine_state["gtbs_events"].extend(upload_rows)
        _append_runtime_log(f"文档索引 · {filename}", category="capture", trace_id=trace_id)
        _append_runtime_log(f"导入流注入记忆层 · {filename}", category="embed", trace_id=trace_id)
        for kw in _extract_keywords(content, 4):
            _engine_state["memory_store"].add({
                "label": "episodic",
                "block_id": f"kw-{mem_id}-{kw}",
                "data": {"content": kw, "filename": filename, "keywords": [kw]},
                "importance": 0.45,
                "timestamp": time.time(),
            })
        preview = content[:400] if content else filename
        return {
            "trace_id": trace_id,
            "status": "completed",
            "ok": True,
            "result": {
                "file_id": file_id,
                "status": "indexed",
                "filename": filename,
                "chunk_count": 1,
                "memory_ids": [mem_id],
                "summary": preview[:120],
                "keywords": [],
                "preview": preview,
            },
        }

    if text:
        try:
            result = _run_6step(text)
            reply = result.get("reply", "已处理")
        except Exception:
            reply = "引擎处理中（模拟模式）"
    else:
        reply = "请输入有效消息"
    return {
        "trace_id": trace_id,
        "status": "completed",
        "ok": True,
        "result": {
            "reply": reply,
            "model_name": "CNexus 2.0 Local",
            "source": "personal_kernel",
            "type": "text",
        },
    }


def _parse_multipart(handler):
    ctype = handler.headers.get("Content-Type", "")
    if "multipart/form-data" not in ctype:
        return None
    return cgi.FieldStorage(
        fp=handler.rfile,
        headers=handler.headers,
        environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": ctype},
        keep_blank_values=True,
    )


def _handle_file_upload(handler):
    _touch_user_activity()
    form = _parse_multipart(handler)
    if not form:
        return {"ok": False, "error": "expected multipart upload"}, 400
    file_item = form["file"] if "file" in form else None
    if file_item is None or not getattr(file_item, "file", None):
        return {"ok": False, "error": "missing file"}, 400
    raw = file_item.file.read()
    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError:
        content = raw.decode("utf-8", errors="replace")
    filename = getattr(file_item, "filename", None) or "upload.txt"
    file_id = f"file-{int(time.time()*1000)}"
    trace_id = file_id
    _file_cache[file_id] = {"filename": filename, "content": content}
    return {
        "file_id": file_id,
        "filename": filename,
        "file_type": os.path.splitext(filename)[1].lstrip(".") or "txt",
        "trace_id": trace_id,
        "ok": True,
    }, 200


# ── Shadow API projections (personal L0 → enterprise contract shapes) ─────


def _speech_text(speech):
    if speech is None:
        return ""
    if isinstance(speech, dict):
        return str(speech.get("text") or speech.get("response_text") or "")
    for attr in ("text", "response_text"):
        if hasattr(speech, attr):
            return str(getattr(speech, attr) or "")
    return str(speech)


def _decision_intent(decision):
    if isinstance(decision, dict):
        return decision.get("intent", "converse")
    if hasattr(decision, "intent"):
        return getattr(decision, "intent", "converse")
    return "converse"


def _find_trace(trace_id):
    for entry in reversed(_engine_state.get("trace", [])):
        if entry.get("trace_id") == trace_id:
            return entry
    return None


def _estimate_tokens(text):
    if not text:
        return 0
    return max(1, int(len(str(text)) * 0.75))


def _cost_level(total):
    if total < 400:
        return "low"
    if total < 1500:
        return "mid"
    if total < 4000:
        return "high"
    return "spike"


def _record_token_trace(
    trace_id,
    input_text,
    output_text,
    entry="converse",
    mode="fast",
    tokens_in=None,
    tokens_out=None,
    source="estimated",
    model_id=None,
    provider=None,
):
    tin = tokens_in if tokens_in is not None else _estimate_tokens(input_text)
    tout = tokens_out if tokens_out is not None else _estimate_tokens(output_text)
    total = tin + tout
    row = {
        "trace_id": trace_id,
        "tokens_in": tin,
        "tokens_out": tout,
        "total": total,
        "mode": mode,
        "cost_level": _cost_level(total),
        "entry": entry,
        "event_count": 7,
        "source": source,
        "model_id": model_id,
        "provider": provider,
    }
    _engine_state.setdefault("token_traces", []).append(row)
    if len(_engine_state["token_traces"]) > 10:
        _engine_state["token_traces"] = _engine_state["token_traces"][-10:]


def _exec_traces_from_cycles(limit=20):
    traces = _engine_state.get("trace", [])[-limit:]
    manifests = []
    for entry in traces:
        manifests.append({
            "trace_id": entry.get("trace_id", f"v2-trace-{entry.get('iteration', 0)}"),
            "graph_id": "personal-6step",
            "template_name": "chat_single_turn",
            "status": "completed",
        })
    return manifests


def _build_cognitive_output(window=200, mode="live"):
    window = max(1, int(window or 200))
    cycles = _engine_state.get("trace", [])[-window:]
    st = _engine_state["state"]
    ms = _engine_state["memory_store"]
    iteration_count = _engine_state.get("current_iteration", 0)
    memory_count = len(ms.blocks)
    valence = getattr(st.emotion, "val", 0.0)
    arousal = getattr(st.emotion, "arousal", 0.0)
    goal = (st.goal or {}).get("current", "探索")

    summary = [{
        "text": f"个人版 L0 内核已完成 {iteration_count} 次认知循环，当前记忆块 {memory_count} 个，系统状态 stable。",
        "confidence": 0.92,
        "source": "trace_projection",
    }]
    if cycles:
        last = cycles[-1]
        inp = str(last.get("input") or "")[:100]
        reply = _speech_text(last.get("speech"))[:100]
        intent = _decision_intent(last.get("decision"))
        summary.insert(0, {
            "text": f"最近对话 trace={last.get('trace_id')} · 意图={intent} · 用户「{inp}」→ 内核「{reply}」",
            "confidence": 0.9,
            "source": "personal_kernel",
        })

    patterns = [{
        "text": f"情绪轨迹 valence={valence:.2f} arousal={arousal:.2f}，认知熵趋于稳定。",
        "confidence": 0.82,
        "source": "emotion_projection",
    }]
    if iteration_count >= 2:
        patterns.append({
            "text": "连续对话后 episodic 写入稳定，6 步循环无异常拒绝。",
            "confidence": 0.78,
            "source": "store_projection",
        })

    insights = [{
        "title": "主脑深度思考中",
        "description": f"当前目标「{goal}」，个人版离线内核以 6 步 reducer 链运行，无需外部 LLM。",
        "confidence": 0.86,
        "why": "trace 投影显示 observe→reflect 全链路 commit 成功",
        "source": "personal_kernel",
        "novelty": 0.42,
        "evidence": [f"iteration={iteration_count}", f"memory_blocks={memory_count}"],
    }]
    if memory_count > 0:
        insights.append({
            "title": "记忆网络正在生长",
            "description": f"已索引 {memory_count} 个记忆块，记忆流图因子节点将随对话/上传持续增加。",
            "confidence": 0.8,
            "why": "BlockStore 非空",
            "source": "memory_projection",
            "novelty": 0.55,
            "evidence": ["episodic store active"],
        })

    discoveries = []
    if cycles:
        discoveries.append({
            "id": f"disc-{cycles[-1].get('trace_id', 'latest')}",
            "title": "新认知循环完成",
            "description": f"trace {cycles[-1].get('trace_id')} 已通过 GTBS 7 事件投影。",
            "confidence": 0.84,
            "novelty": 0.7,
            "why": "本轮为最新一次 6 步执行",
            "evidence": [str(cycles[-1].get("input", ""))[:60]],
            "source": "novel_trace",
            "first_seen_at": _iso_ts(),
        })

    actions = [{
        "action": "continue_dialogue",
        "priority": 0.85,
        "rationale": "继续对话以积累 episodic 记忆并驱动流图脉冲",
        "category": "engagement",
        "impact": 0.75,
        "reversibility": 0.95,
        "why": "个人版最佳价值来自持续认知循环",
    }]
    if memory_count == 0:
        actions.insert(0, {
            "action": "upload_document",
            "priority": 0.9,
            "rationale": "导入文档以填充记忆流图节点",
            "category": "memory",
            "impact": 0.8,
            "reversibility": 0.9,
            "why": "memory_items 为空，流图因子链尚未形成",
        })

    narrative_parts = [s["text"] for s in summary[:2]]
    if insights:
        narrative_parts.append(insights[0]["description"])
    narrative = " ".join(narrative_parts)

    return {
        "summary": summary,
        "patterns": patterns,
        "insights": insights,
        "rules": [{
            "text": "个人版使用内置 6 步认知内核，不依赖 Ollama 或外部 API Key。",
            "confidence": 0.95,
            "source": "policy",
        }],
        "experiences": [{
            "text": f"已完成 {iteration_count} 次离线认知循环，治理状态 personal/stable。",
            "confidence": 0.88,
            "source": "experience:trace",
        }],
        "discoveries": discoveries,
        "actions": actions,
        "top_actions": actions[:1],
        "narrative": narrative,
        "generated_at": _iso_ts(),
        "window_size": window,
        "mode": mode,
        "exec_traces": _exec_traces_from_cycles(20),
    }


def cse_live(window=200):
    return _build_cognitive_output(window, mode="live")


def cse_synthesize(window=200):
    out = _build_cognitive_output(window, mode="synth")
    out["narrative"] = "【重新分析】" + (out.get("narrative") or "")
    if out.get("discoveries"):
        out["discoveries"][0]["title"] = "合成分析 · " + out["discoveries"][0]["title"]
    return out


def token_observatory(limit=100):
    traces = list(reversed(_engine_state.get("token_traces", [])))[: max(1, int(limit))]
    return {"token_traces": traces, "count": len(traces)}


def runtime_introspect():
    traces = _engine_state.get("token_traces", [])
    return {"token_traces": list(reversed(traces)), "count": len(traces)}


def token_field(trace_id):
    entry = _find_trace(trace_id)
    token_row = next((t for t in reversed(_engine_state.get("token_traces", [])) if t.get("trace_id") == trace_id), None)
    if not entry and not token_row:
        return {"detail": f"trace not found: {trace_id}"}

    inp = str((entry or {}).get("input") or "")
    reply = _speech_text((entry or {}).get("speech"))
    tin = token_row.get("tokens_in") if token_row else _estimate_tokens(inp)
    tout = token_row.get("tokens_out") if token_row else _estimate_tokens(reply)
    total = tin + tout

    phases = ["observe", "cognize", "decide", "speak", "store", "reflect"]
    by_phase = {}
    token_events = []
    per_phase = max(1, total // len(phases))
    for i, phase in enumerate(phases):
        by_phase[phase] = per_phase
        token_events.append({
            "trace_id": trace_id,
            "event_id": f"{trace_id}-{phase}",
            "source": "personal_kernel",
            "tokens_in": per_phase if phase == "observe" else 0,
            "tokens_out": per_phase if phase == "speak" else 0,
            "total": per_phase,
            "phase": phase,
            "mode": "fast",
            "entry": f"{phase}_fn",
            "cost_level": _cost_level(per_phase),
            "timestamp": time.time() - (len(phases) - i) * 10,
        })

    return {
        "trace_id": trace_id,
        "total_cost": round(total * 0.0001, 6),
        "total_tokens": total,
        "field": {phase: float(by_phase[phase]) for phase in phases},
        "gradient": {phase: round(1.0 - i * 0.12, 2) for i, phase in enumerate(phases)},
        "by_phase": by_phase,
        "bindings": [{"spine_event_id": f"tx-{phase}", "tokens": by_phase[phase]} for phase in phases[:3]],
        "influence": {"hot_paths": [{"from": "observe", "to": "speak", "severity": "mid", "weight": 0.82}], "max_weight": 0.82},
        "identity_id": "cnexus-2.0-personal",
        "token_events": token_events,
        "causal": {"nodes": [{"id": phase, "label": phase} for phase in phases], "edges": []},
    }


def kernel_records_recent(limit=20):
    traces = _engine_state.get("trace", [])
    ids = [t.get("trace_id") for t in reversed(traces) if t.get("trace_id")]
    return {"trace_ids": ids[: max(1, int(limit))]}


def _gtbs_events_for_trace(trace_id):
    out = []
    for row in _engine_state.get("gtbs_events", []):
        payload = row.get("payload") or {}
        prov = payload.get("provenance") or {}
        if prov.get("trace_id") == trace_id:
            out.append(row)
    return out


def kernel_record(trace_id):
    entry = _find_trace(trace_id)
    if not entry:
        return None
    steps = [
        ("observe", "观察输入"),
        ("cognize", "认知整合"),
        ("decide", "决策意图"),
        ("speak", "生成话语"),
        ("store", "写入记忆"),
        ("reflect", "反思调整"),
    ]
    nodes = []
    edges = []
    for i, (step, label) in enumerate(steps):
        node_id = f"{step}-{i}"
        nodes.append({"id": node_id, "label": label, "type": step, "phase": step})
        if i > 0:
            edges.append({"from": f"{steps[i-1][0]}-{i-1}", "to": node_id, "kind": "causal"})
    inp = str(entry.get("input") or "")
    reply = _speech_text(entry.get("speech"))
    return {
        "version": "2.0-personal",
        "trace_id": trace_id,
        "intent_type": _decision_intent(entry.get("decision")),
        "result": {"reply": reply, "input": inp},
        "identity": "CNexus 2.0 Personal",
        "graph_invariant": "personal-6step-v1",
        "graph": {"id": "personal-6step", "nodes": len(nodes), "edges": len(edges)},
        "nodes": nodes,
        "edges": edges,
        "state_projection": {"emotion": api_status().get("emotion", {}), "goal": api_status().get("goal", {})},
        "causal_projection": {"links": edges},
        "explain_projection": {"summary": f"用户输入「{inp[:80]}」经 6 步认知循环后输出回复。"},
        "equivalence": None,
        "replay_signature": trace_id,
        "audit_log": {"source": "shadow_projection", "steps": len(steps)},
        "audit": {"ok": True, "edition": "personal"},
        "events": _gtbs_events_for_trace(trace_id),
        "derivation": {"pipeline": "6-step-reducer", "iteration": entry.get("iteration")},
        "elapsed_ms": 48,
    }


def kernel_learn(trace_id):
    entry = _find_trace(trace_id)
    if not entry:
        return None
    inp = str(entry.get("input") or "")
    reply = _speech_text(entry.get("speech"))
    intent = _decision_intent(entry.get("decision"))
    steps = [
        f"1. 观察：接收用户输入「{inp[:60]}」",
        f"2. 认知：整合当前状态与上下文",
        f"3. 决策：确定意图为 {intent}",
        f"4. 话语：生成内核回复",
        f"5. 存储：写入 episodic / emotion 块",
        f"6. 反思：调整下一轮认知权重",
    ]
    story = f"用户说「{inp[:80]}」，个人版内核经过 6 步离线认知循环，最终以「{reply[:80]}」回应。"
    return {
        "version": "2.0",
        "trace_id": trace_id,
        "execution_tier": "L0-personal",
        "mode": "fast",
        "summary": story,
        "steps": steps,
        "beginner_view": f"你问了：{inp[:100]}。CNexus 思考后回答：{reply[:100]}。",
        "intermediate_view": story,
        "expert_view": f"trace={trace_id} · intent={intent} · 6-step reducer chain · GTBS events=7",
        "execution_story": story,
        "memory_view": ["episodic block appended", "emotion snapshot updated"],
        "reasoning_trace": steps,
        "why_this_result": f"决策模块选择 intent={intent}，话语模块据此生成回复。",
        "why_it_feels_fast_or_slow": "个人版本地 reducer 无网络延迟，通常为毫秒级。",
        "mental_model": "观察→认知→决策→话语→存储→反思 六步循环",
        "user_intent_summary": inp[:200],
    }


def memory_recall(query):
    q = (query or "").strip().lower()
    hits = []
    for block in _engine_state["memory_store"].blocks:
        data = block.get("data") or {}
        content = str(data.get("content") or data.get("response_text") or data.get("filename") or "")
        if not q or q in content.lower():
            hits.append(content[:240])
    if not hits:
        for entry in reversed(_engine_state.get("trace", [])):
            inp = str(entry.get("input") or "")
            if q and q in inp.lower():
                hits.append(f"对话记忆：{inp[:200]}")
    context = "\n---\n".join(hits[:5]) if hits else f"未检索到与「{query}」相关的记忆片段（个人版 BlockStore 检索）。"
    return {"context": context}


class V2Handler(BaseHTTPRequestHandler):
    def _json(self, data, st=200):
        self.send_response(st)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        body = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length > 0 else b"{}"
        try:
            return json.loads(body) if body else {}
        except Exception:
            return {}

    def do_PUT(self):
        p = urlparse(self.path)
        path = p.path.rstrip("/") or "/"
        if path.startswith("/models/"):
            model_id = path[len("/models/") :]
            row, err = _upsert_model(model_id, self._read_json(), create=False)
            if err == "not_found":
                return self._json({"detail": f"model not found: {model_id}"}, 404)
            return self._json({"model": row})
        self._json({"ok": False, "error": "not found"}, 404)

    def do_GET(self):
        p = urlparse(self.path)
        path = p.path.rstrip("/") or "/"
        qs = parse_qs(p.query)

        # ── WebSocket 升级请求：立即返回 426 Upgrade Required + 关连接 ──
        # 目的是让浏览器 WebSocket 构造函数快速 reject，避免进入 50 次递归重试死循环
        if self.headers.get("Upgrade", "").lower() == "websocket":
            self.send_response(426)
            self.send_header("Connection", "close")
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"WebSocket not supported")
            return
        # ── API routes take priority ──
        # ── API route: status (直通前端 statusToMindOverview) ──
        if path == "/api/status":
            return self._json(api_status())

        # ── API route: converse ──
        text = qs.get("text", [None])[0]
        if path == "/api/converse" and text:
            try:
                result = _run_6step(text)
                return self._json({"ok": True, "status": "success", "reply": result["reply"], **result})
            except Exception as e:
                return self._json({"ok": False, "error": str(e)}, 500)

        # ── API route: /v1/system/compute (前端疯狂请求，不能 404) ──
        if path == "/v1/gateway/health":
            return self._json(gateway_health())
        if path == "/v1/gateway/state":
            return self._json(gateway_health())
        if path == "/v1/system/capability":
            return self._json(system_capability())
        if path in ("/v1/system/ready", "/v1/system/ready/stream"):
            return self._json(system_ready())
        if path == "/v1/health":
            return self._json({"status": "ok", "service": "cnexus-2.0-personal"})
        if path == "/v1/memory/stats":
            return self._json(memory_stats())
        if path == "/v1/execution/status":
            return self._json(execution_status())
        if path == "/v1/ollama/status":
            return self._json(ollama_status())
        if path == "/models":
            return self._json(api_models())
        if path.startswith("/models/") and path.endswith("/test"):
            model_id = path[len("/models/") : -len("/test")]
            return self._json(test_model(model_id))
        if path.startswith("/models/"):
            model_id = path[len("/models/") :]
            row = _engine_state["model_registry"].get(model_id)
            if not row:
                return self._json({"detail": f"model not found: {model_id}"}, 404)
            return self._json({"model": _model_public(row)})
        if path.startswith("/logs"):
            limit = int(qs.get("limit", ["100"])[0] or 100)
            return self._json(api_logs(limit))
        if path.startswith("/v1/gtbs/events"):
            limit = int(qs.get("limit", ["300"])[0] or 300)
            return self._json(gtbs_events(limit))

        # ── Shadow APIs: CSE / Spine / Kernel / Memory recall ──
        if path == "/v1/cse/live":
            window = int(qs.get("window", ["200"])[0] or 200)
            return self._json(cse_live(window))
        if path == "/v1/spine/token/observatory":
            limit = int(qs.get("limit", ["100"])[0] or 100)
            return self._json(token_observatory(limit))
        if path == "/v1/runtime/introspect":
            return self._json(runtime_introspect())
        if path.startswith("/v1/spine/token/trace/"):
            trace_id = path[len("/v1/spine/token/trace/"):]
            return self._json(token_field(trace_id))
        if path == "/v1/kernel/records/recent":
            limit = int(qs.get("limit", ["20"])[0] or 20)
            return self._json(kernel_records_recent(limit))
        if path.startswith("/v1/kernel/record/"):
            rest = path[len("/v1/kernel/record/"):]
            if rest.endswith("/learn"):
                trace_id = rest[:-len("/learn")]
                payload = kernel_learn(trace_id)
                if payload is None:
                    return self._json({"detail": f"record not found: {trace_id}"}, 404)
                return self._json(payload)
            trace_id = rest
            payload = kernel_record(trace_id)
            if payload is None:
                return self._json({"detail": f"record not found: {trace_id}"}, 404)
            return self._json(payload)
        if path == "/v1/memory/recall":
            query = qs.get("query", [""])[0] or ""
            return self._json(memory_recall(query))

        if path in ("/v1/system/compute", "/v1/mind/overview"):
            return self._json(api_status())

        # ── WebSocket 请求路径检测（已由 Upgrade 头机制拦截，此处仅捕获其余非 Upgrade 路径） ──
        # 无需额外处理

        # ── /v1/gateway/intent/{trace_id} GET：前端从 WS fallback 到 HTTP 轮询 ──
        if path.startswith("/v1/gateway/intent/") and path != "/v1/gateway/intent":
            # 返回模拟完成结果，前端会显示回复
            return self._json({"status": "completed", "result": {"reply": "模拟认知回复：已接收到意图请求，引擎正在思考。", "source": "offline_mock", "type": "text"}})

        # ── 其他 /v1/gateway/ 或 /v1/ 路由 ──
        if path.startswith("/v1/gateway/") or path.startswith("/v1/") or path == "/health" or path.startswith("/logs"):
            return self._json({"status": "ok", "ok": True, "message": "L0 fallback - WS/L3 not available"})

        # ── Static file serving (Next.js static export) ──
        _UI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui")
        # Map paths to files — strict asset-aware SPA fallback
        clean_path = path.lstrip("/")
        if not clean_path:
            clean_path = "index.html"
        local_path = os.path.join(_UI_DIR, clean_path)

        # If it's a directory, serve index.html from it
        if os.path.isdir(local_path):
            local_path = os.path.join(local_path, "index.html")

        # If physical file exists, serve it directly
        if os.path.isfile(local_path):
            self._serve_static(local_path)
            return

        # ── Chunk hash fallback: nextjs sometimes loads e.g. 278.js but file is 278.42d36886d35e02ce.js ──
        import glob as _glob
        import re as _re
        if clean_path.startswith("_next/static/chunks/"):
            basename = os.path.basename(clean_path)
            dirpart = os.path.dirname(local_path)
            # Match basename without hash: e.g. "278.js" → "278.*.js" in same dir
            pattern = _re.sub(r"^(\d+)(\.\w+)$", r"\1.*\2", basename)
            if basename != pattern:
                matches = _glob.glob(os.path.join(dirpart, pattern))
                if matches:
                    self._serve_static(matches[0])
                    return

        # Static assets (.js, .css, images, etc.) — NOT FOUND must 404
        asset_exts = [".js", ".css", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".json", ".svg", ".ico", ".map", ".woff", ".woff2", ".ttf", ".eot"]
        if any(clean_path.endswith(ext) for ext in asset_exts):
            self._json({"ok": False, "error": f"Asset not found: " + path}, 404)
            return

        # SPA fallback: page routes (e.g. /dashboard, /desktop) → index.html
        fallback = os.path.join(_UI_DIR, "index.html")
        if os.path.isfile(fallback):
            self._serve_static(fallback)
        else:
            self._json({"ok": False, "error": "index.html missing"}, 500)



    def do_POST(self):
        p = urlparse(self.path)
        path = p.path.rstrip("/") or "/"
        # ── API route: converse ──
        if path == "/api/converse":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length > 0 else b"{}"
            try:
                data = json.loads(body) if body else {}
                text = data.get("text") or data.get("message", "")
                if not text:
                    return self._json({"ok": False, "error": "missing text"}, 400)
                _sync_ollama_registry()
                model_id = data.get("model_id")
                result = _run_6step(text, model_id=model_id)
                return self._json({"ok": True, "status": "success", "reply": result["reply"], **result})
            except Exception as e:
                return self._json({"ok": False, "error": str(e)}, 500)
        # ── /v1/gateway/intent POST：前端聊天/上传走 Gateway 契约 {type, payload} ──
        if path == "/v1/gateway/intent":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length > 0 else b"{}"
            try:
                data = json.loads(body) if body else {}
            except Exception:
                data = {}
            return self._json(_handle_gateway_intent(data))

        if path == "/v1/gateway/file/upload":
            payload, status = _handle_file_upload(self)
            return self._json(payload, status)

        if path == "/v1/memory/capture":
            _touch_user_activity()
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length > 0 else b"{}"
            try:
                data = json.loads(body) if body else {}
            except Exception:
                data = {}
            content = (data.get("content") or "").strip()
            mem_id = f"mem-{int(time.time()*1000)}"
            if content:
                keywords = _extract_keywords(content, 6)
                _engine_state["memory_store"].add({
                    "label": data.get("layer", "episodic"),
                    "block_id": mem_id,
                    "data": {
                        "content": content[:2000],
                        "label": data.get("label", "capture"),
                        "keywords": keywords,
                    },
                    "importance": float(data.get("importance", 0.6)),
                    "timestamp": time.time(),
                })
                for kw in keywords:
                    _engine_state["memory_store"].add({
                        "label": "episodic",
                        "block_id": f"kw-{mem_id}-{kw}",
                        "data": {"content": kw, "keywords": [kw], "label": kw},
                        "importance": 0.45,
                        "timestamp": time.time(),
                    })
            return self._json({"memory_id": mem_id, "status": "stored", "ok": True})

        if path == "/v1/memory/rem-sleep":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length > 0 else b"{}"
            try:
                data = json.loads(body) if body else {}
            except Exception:
                data = {}
            force = bool(data.get("force"))
            return self._json(_run_rem_deep_sleep(force=force))

        if path == "/api/ingest/image":
            _touch_user_activity()
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length > 0 else b"{}"
            try:
                data = json.loads(body) if body else {}
            except Exception:
                data = {}
            return self._json(api_ingest_image(data))

        if path == "/api/ingest/code":
            _touch_user_activity()
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length > 0 else b"{}"
            try:
                data = json.loads(body) if body else {}
            except Exception:
                data = {}
            return self._json(api_ingest_code(data))

        if path == "/v1/cse/synthesize":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length > 0 else b"{}"
            try:
                data = json.loads(body) if body else {}
            except Exception:
                data = {}
            window = int(data.get("window") or 200)
            return self._json(cse_synthesize(window))

        if path == "/models":
            row, err = create_model(self._read_json())
            if err:
                return self._json({"detail": err}, 400)
            return self._json({"model": row})
        if path.startswith("/models/") and path.endswith("/test"):
            model_id = path[len("/models/") : -len("/test")]
            return self._json(test_model(model_id))
        if path == "/v1/ollama/start":
            return self._json(ollama_start())
        if path == "/v1/ollama/stop":
            return self._json(ollama_stop())

        # ── 其他 /v1/* POST 路由 ──
        if path.startswith("/v1/"):
            # 前端 POST /v1/system/compute 期望返回 status 结构
            return self._json(api_status())
        self._json({"ok": False, "error": "not found"}, 404)

    def _serve_static(self, filepath):
        """Serve a static file with correct MIME type. If file missing, 404 immediately — no 404.html fallback that causes silent hangs."""
        if not os.path.isfile(filepath):
            self._json({"ok": False, "error": f"File not found: {os.path.basename(filepath)}"}, 404)
            return
        ext = os.path.splitext(filepath)[1].lower()
        mime = {
            ".html": "text/html; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".json": "application/json; charset=utf-8",
            ".png": "image/png",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
            ".txt": "text/plain; charset=utf-8",
        }.get(ext, "application/octet-stream")
        try:
            with open(filepath, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", len(data))
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self._json({"ok": False, "error": str(e)}, 500)

    def log_message(self, fmt, *args):
        # Silent logging — avoid spamming console
        pass

def main():
    port = 7864
    server = HTTPServer(("127.0.0.1", port), V2Handler)
    server.allow_reuse_address = True
    print(f" CNexus 2.0 Unified Server live on http://127.0.0.1:{port}")
    print(f"   GET  /              — Next.js static frontend (6 views)")
    print(f"   GET  /api/status    — L0 cognitive state snapshot")
    print(f"   GET  /api/converse?text=... — run 6-step cycle")
    print(f'   POST /api/converse  -- json body with "text" field')
    print(f"   POST /v1/memory/rem-sleep — REM deep sleep consolidation")
    print(f"   POST /api/ingest/image  — vision architecture projection")
    print(f"   POST /api/ingest/code   — AST code space projection")
    _start_rem_watchdog()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()

if __name__ == "__main__":
    main()
