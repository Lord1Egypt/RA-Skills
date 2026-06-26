# FILE_META
# INPUT:  PipelineOptions + filesystem (~/.openclaw/agents/*/sessions/)
# OUTPUT: list[dict] (discover) + list[SessionCandidate] (filter) + ProcessResult (per session)
# POS:    skill lib — single pipeline entry used by the openclaw adapter
# MISSION: Unified collection pipeline: discover → filter → process (v2).

"""The unified collection pipeline.

Flow per ``docs/collect-pipeline-v2.md`` §4.1:

    ① discover_sessions  → raw session file list
    ② filter_sessions    → eligibility + runtime status → SessionCandidate
    ③ process_session    → all-segment DAG walk, concat with
                            [COMPACTION_BOUNDARY], OpenAI conversion, write.

Consumed by ``lib.adapters.openclaw`` (discover/parse) which in turn is
driven by ``scan_adapter.py`` and ``cli.py`` — a single code path drives
every trajectory file that lands in the output directory.
"""

from __future__ import annotations

import json
import os
import re
from typing import Optional

from ..convert.converter import build_model_config, convert_to_trajectory
from ..parse.dag import (
    check_session_models,
    extract_all_segments,
    get_model_from_nodes,
    get_raw_model_from_nodes,
    parse_jsonl,
)
from ..parse.metadata_stripper import (
    is_system_startup_message,
    strip_metadata_prefix,
)
from ..parse.session_index import read_session_id_from_header
from .pipeline_options import (
    PipelineOptions,
    ProcessResult,
    SessionCandidate,
)

# Accepts all OpenClaw session filename shapes:
#   {uuid}.jsonl                              plain
#   {uuid}-topic-{id}.jsonl                   topic branch
#   {ISO-ts}_{uuid}.jsonl                     fork / pi-coding-agent newSession
#   any of the above with .reset.<timestamp>  archived
# The captured `sid` is only a fallback — real session_id comes from the
# {"type":"session","id":...} header line.
_SESSION_FILENAME_RE = re.compile(
    r"^(?:\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z_)?"
    r"(?P<sid>[0-9a-f-]+)"
    r"(?:-topic-[^.]+)?"
    r"\.jsonl(?:\.reset\..+)?$"
)

# Domain classifier knobs — lives here so process_session is self-contained.
_DOMAIN_CODE_TOOLS = {"edit", "write", "grep", "find", "apply_patch"}
_DOMAIN_WEB_TOOLS = {"web_search", "web_fetch"}
_DOMAIN_MSG_TOOLS = {"message"}
_DOMAIN_MEDIA_TOOLS = {"image", "image_generate", "tts", "pdf"}
_DOMAIN_SESSION_TOOLS = {"sessions_spawn", "sessions_send", "subagents"}
_DOMAIN_CRON_TOOLS = {"cron"}
_DOMAIN_MONITOR_KEYWORDS = {"monitor", "监控", "告警", "health", "status check"}


# ── ① discover ────────────────────────────────────────────────

def discover_sessions(options: PipelineOptions) -> list[dict]:
    """Scan ``options.sessions_dirs`` for OpenClaw session files.

    Returns a list of ``{session_id, agent_id, file_path, file_mtime}``
    dicts. Pure I/O — does not read file contents. Non-matching filenames
    and unreadable files are silently skipped. Results are sorted by
    ``file_mtime`` descending (newest first) and de-duplicated by
    ``(agent_id, session_id)``.
    """
    seen: set[tuple[str, str]] = set()
    result: list[dict] = []
    for sessions_dir in options.sessions_dirs:
        if not os.path.isdir(sessions_dir):
            continue
        agent_id = os.path.basename(os.path.dirname(sessions_dir)) or "unknown"
        try:
            entries = os.listdir(sessions_dir)
        except OSError:
            continue
        for name in entries:
            m = _SESSION_FILENAME_RE.match(name)
            if not m:
                continue
            file_path = os.path.join(sessions_dir, name)
            # Header is authoritative — fork/topic filenames don't carry the
            # true session_id in the filename.
            session_id = read_session_id_from_header(file_path) or m.group("sid")
            key = (agent_id, session_id)
            if key in seen:
                continue
            try:
                mtime = os.path.getmtime(file_path)
            except OSError:
                continue
            seen.add(key)
            result.append({
                "session_id": session_id,
                "agent_id": agent_id,
                "file_path": file_path,
                "file_mtime": mtime,
            })
    result.sort(key=lambda x: x["file_mtime"], reverse=True)
    return result


# ── helpers reused by filter + process ────────────────────────

def _first_substantive_user_text(nodes: list[dict]) -> str:
    """Return the first user message text with startup/metadata stripped.

    Empty string when no substantive user message exists.
    """
    for node in nodes:
        if node.get("type") != "message":
            continue
        msg = node.get("message", {})
        if msg.get("role") != "user":
            continue
        for block in msg.get("content", []):
            if isinstance(block, dict) and block.get("type") == "text":
                raw = block.get("text", "")
                if is_system_startup_message(raw):
                    return ""
                return strip_metadata_prefix(raw)
        return ""
    return ""


def _is_cron_task(nodes: list[dict]) -> bool:
    """Detect a cron-triggered session.

    OpenClaw cron emits the first user message with a ``[cron: …]`` prefix.
    The identification is fragile on purpose — if OpenClaw renames the
    prefix, we want the failure to be loud rather than silently retaining
    cron tasks under ``include_cron_tasks=false``.
    """
    text = _first_substantive_user_text(nodes)
    return text.startswith("[cron:")


def build_summary(
    nodes: list[dict], *, max_per: int = 15, max_total: int = 45
) -> str:
    """v2 §5.1 session list summary.

    Iterates substantive user messages in order, truncates each at
    ``max_per`` characters, joins with `` → `` and stops once the cumulative
    character count hits ``max_total``. Returns ``"[无用户输入]"`` when the
    session has no usable user text (e.g. all gateway events).
    """
    snippets: list[str] = []
    total = 0
    for node in nodes:
        if node.get("type") != "message":
            continue
        msg = node.get("message", {})
        if msg.get("role") != "user":
            continue
        text = ""
        for block in msg.get("content", []):
            if isinstance(block, dict) and block.get("type") == "text":
                raw = block.get("text", "")
                if is_system_startup_message(raw):
                    text = ""
                    break
                text = strip_metadata_prefix(raw)
                break
        if not text:
            continue
        text = " ".join(text.split())
        if not text:
            continue
        if len(text) > max_per:
            text = text[:max_per] + "..."
        snippets.append(text)
        total += len(text)
        if total >= max_total:
            break
    if not snippets:
        return "[无用户输入]"
    return " → ".join(snippets)


def _session_times_from_nodes(nodes: list[dict]) -> tuple[str, str]:
    """First and last ISO timestamps in the node list. Empty on miss."""
    started = ""
    ended = ""
    for node in nodes:
        ts = node.get("timestamp")
        if ts:
            started = ts
            break
    for node in reversed(nodes):
        ts = node.get("timestamp")
        if ts:
            ended = ts
            break
    return started, ended


def find_latest_sids_by_agent(raw: list[dict]) -> set[str]:
    """Per-agent most-recent-mtime session id set.

    The latest session of each agent may still be in use. CLI's default
    is to skip it unless the user forces through with ``force_active``.
    Reset (archived) files are ignored here — they are by construction
    not the live session.
    """
    by_agent: dict[str, list[dict]] = {}
    for s in raw:
        if ".reset." in s.get("file_path", ""):
            continue
        by_agent.setdefault(s.get("agent_id", "unknown"), []).append(s)

    latest_ids: set[str] = set()
    for sessions in by_agent.values():
        if not sessions:
            continue
        latest = max(sessions, key=lambda s: s.get("file_mtime", 0.0))
        sid = latest.get("session_id")
        if sid:
            latest_ids.add(sid)
    return latest_ids


# ── ② filter ─────────────────────────────────────────────────

def filter_sessions(
    raw: list[dict],
    options: PipelineOptions,
    *,
    manifest: dict | None = None,
    latest_sids: set[str] | None = None,
    system_prompt_index: dict[str, str] | None = None,
) -> list[SessionCandidate]:
    """v2 §4.2 ② + ③ eligibility + runtime status + list truncation.

    Inputs beyond ``raw`` and ``options``:
      * ``manifest`` — optional manifest dict for submitted/rejected lookup.
        When ``None`` we treat every session as unseen.
      * ``latest_sids`` — set of session ids that are "latest per agent"
        (possibly still active). Precomputed by the caller so filter_sessions
        stays filesystem-cheap.
      * ``system_prompt_index`` — optional mapping of session_id → SP from
        the cache-trace index, used for the ``no_cache_trace`` eligibility
        check. When ``None`` we treat every session as missing the trace.

    Returns a list of ``SessionCandidate``. When
    ``options.include_ineligible`` is false, ineligible candidates are
    dropped from the result (default CLI behavior); otherwise they are
    kept so the UI can show why a session was skipped.

    Runtime-status filtering:
      * ``submitted`` → always dropped (already delivered).
      * ``rejected`` → dropped unless ``force_rejected`` or
        ``include_ineligible``.
      * ``active`` → dropped unless ``force_active`` or ``include_ineligible``.
    """
    manifest = manifest or {}
    latest_sids = latest_sids or set()
    system_prompt_index = system_prompt_index or {}

    submitted_ids = {
        k.replace(".trajectory.json", "")
        for k in manifest.get("submitted", {})
    }
    rejected_map = manifest.get("rejected", {})
    explicit = set(options.explicit_session_ids or [])

    rules = options.eligibility
    candidates: list[SessionCandidate] = []

    for entry in raw:
        session_id = entry["session_id"]
        agent_id = entry.get("agent_id", "unknown")
        file_path = entry["file_path"]

        # Explicit-mode scope filter
        if explicit and session_id not in explicit:
            continue

        # Runtime status
        runtime_status: Optional[str] = None
        if session_id in submitted_ids:
            runtime_status = "submitted"
        elif session_id in rejected_map:
            runtime_status = "rejected"
        elif session_id in latest_sids:
            runtime_status = "active"

        if runtime_status == "submitted" and not explicit:
            continue
        if runtime_status == "rejected" and not explicit and not options.force_rejected:
            if not options.include_ineligible:
                continue
        if runtime_status == "active" and not explicit and not options.force_active:
            if not options.include_ineligible:
                continue

        # Since filter
        if options.since_ts is not None:
            if entry.get("file_mtime", 0.0) < options.since_ts:
                continue

        # Read file — costly but v2 needs the whole session to run the checks.
        try:
            nodes = parse_jsonl(file_path)
        except Exception:
            continue

        candidate = _build_candidate(
            session_id=session_id,
            agent_id=agent_id,
            file_path=file_path,
            nodes=nodes,
            rules=rules,
            system_prompt_index=system_prompt_index,
            runtime_status=runtime_status,
        )
        candidates.append(candidate)

    if not options.include_ineligible:
        candidates = [c for c in candidates if c.eligible]

    # Sort preserves raw's mtime-desc order (discover already did that); we
    # only truncate to list_size.
    return candidates[:options.list_size]


def _build_candidate(
    *,
    session_id: str,
    agent_id: str,
    file_path: str,
    nodes: list[dict],
    rules,
    system_prompt_index: dict[str, str],
    runtime_status: Optional[str],
) -> SessionCandidate:
    """Run all eligibility checks on a session and shape the candidate record."""
    started_at, ended_at = _session_times_from_nodes(nodes)
    summary = build_summary(nodes)
    has_compaction = any(
        n.get("type") == "compaction" and n.get("summary") for n in nodes
    )
    model = get_raw_model_from_nodes(nodes) or ""

    # Total assistant turns across the whole session (matches the number a
    # human would count when skimming the log).
    turns = _count_assistant_turns(nodes)

    eligible = True
    reject_reason: Optional[str] = None
    reject_detail: Optional[dict] = None

    # 1. Session-level model whitelist (hard reject; cannot be overridden)
    ok, bad = check_session_models(nodes, rules.model_whitelist)
    if not ok:
        eligible = False
        reject_reason = "non_allowed_model_in_session"
        reject_detail = {"non_allowed_models": bad}

    # 2. Minimum assistant turns
    if eligible and turns < rules.min_turns:
        eligible = False
        reject_reason = "turns_too_low"
        reject_detail = {"turns": turns, "required": rules.min_turns}

    # 3. Minimum tool_use count
    if eligible and rules.min_tool_use_count > 0:
        tool_use_count = _count_tool_use_blocks(nodes)
        if tool_use_count < rules.min_tool_use_count:
            eligible = False
            reject_reason = "tool_use_too_low"
            reject_detail = {
                "tool_use_count": tool_use_count,
                "required": rules.min_tool_use_count,
            }

    # 4. Minimum reasoning turns
    if eligible and rules.min_reasoning_turns > 0:
        reasoning_turns = _count_reasoning_turns(nodes)
        if reasoning_turns < rules.min_reasoning_turns:
            eligible = False
            reject_reason = "reasoning_too_low"
            reject_detail = {
                "reasoning_turns": reasoning_turns,
                "required": rules.min_reasoning_turns,
            }

    # 5. cache-trace presence
    if eligible:
        has_cache = session_id in system_prompt_index
        if not has_cache and not rules.allow_non_cache_trace:
            eligible = False
            reject_reason = "no_cache_trace"
            reject_detail = {"detail": "no system prompt and allow_non_cache_trace=false"}

    # 6. cron identification (only a gate when include_cron_tasks=false)
    if eligible and not rules.include_cron_tasks and _is_cron_task(nodes):
        eligible = False
        reject_reason = "cron_task_excluded"
        reject_detail = {"detail": "cron task excluded by config"}

    return SessionCandidate(
        session_id=session_id,
        agent_id=agent_id,
        file_path=file_path,
        model=model,
        turns=turns,
        has_compaction=has_compaction,
        started_at=started_at,
        ended_at=ended_at,
        summary=summary,
        eligible=eligible,
        reject_reason=reject_reason,
        reject_detail=reject_detail,
        runtime_status=runtime_status,
    )


def _count_assistant_turns(nodes: list[dict]) -> int:
    return sum(
        1 for n in nodes
        if n.get("type") == "message"
        and n.get("message", {}).get("role") == "assistant"
    )


def _count_tool_use_blocks(nodes: list[dict]) -> int:
    count = 0
    for n in nodes:
        if n.get("type") != "message":
            continue
        msg = n.get("message", {})
        if msg.get("role") != "assistant":
            continue
        for block in msg.get("content", []):
            if isinstance(block, dict) and block.get("type") == "toolCall":
                count += 1
    return count


def _count_reasoning_turns(nodes: list[dict]) -> int:
    count = 0
    for n in nodes:
        if n.get("type") != "message":
            continue
        msg = n.get("message", {})
        if msg.get("role") != "assistant":
            continue
        for block in msg.get("content", []):
            if isinstance(block, dict) and block.get("type") == "thinking":
                count += 1
                break
    return count


# ── ③ process ────────────────────────────────────────────────

def process_session(
    candidate: SessionCandidate,
    options: PipelineOptions,
    *,
    real_system_prompt: str | None,
    system_prompt_source: str,
    session_meta: dict | None = None,
) -> ProcessResult:
    """v2 §4.2 ⑤ + ⑥: convert one eligible candidate to an OpenAI trajectory file.

    Does NOT update the manifest — that's the caller's job (manifest is a
    user-facing artifact owned by the openclaw adapter / cli). We only
    write the trajectory and stats files and return a ``ProcessResult``.
    """
    if not candidate.eligible:
        return ProcessResult(
            session_id=candidate.session_id,
            ok=False,
            reject_reason=candidate.reject_reason,
            reject_detail=candidate.reject_detail,
        )

    nodes = parse_jsonl(candidate.file_path)
    segments = extract_all_segments(nodes)

    # Concatenate all eras in order, injecting the compaction node between
    # them. The converter renders a compaction node as a single
    # ``[COMPACTION_BOUNDARY] <summary>`` user message (v2 §5.2).
    concatenated: list[dict] = []
    for i, (prior_comp, chain) in enumerate(segments):
        if i > 0 and prior_comp and prior_comp.get("summary"):
            concatenated.append(prior_comp)
        concatenated.extend(chain)

    if not concatenated:
        return ProcessResult(
            session_id=candidate.session_id,
            ok=False,
            reject_reason="empty_conversation",
            reject_detail={"detail": "no messages after DAG walk"},
        )

    session_meta = session_meta or {}
    model = get_model_from_nodes(nodes) or candidate.model or "unknown"
    model_config = build_model_config(
        model=model,
        provider=session_meta.get("provider", "unknown"),
        thinking_level=session_meta.get("thinking_level", "off"),
    )

    trajectory = convert_to_trajectory(
        concatenated,
        real_system_prompt=real_system_prompt or "",
        model_config=model_config,
    )

    if trajectory.get("_discarded"):
        return ProcessResult(
            session_id=candidate.session_id,
            ok=False,
            reject_reason="conversion_error",
            reject_detail={"detail": trajectory["_discarded"]},
        )

    if not trajectory["messages"]:
        return ProcessResult(
            session_id=candidate.session_id,
            ok=False,
            reject_reason="conversion_error",
            reject_detail={"detail": "empty after conversion"},
        )

    os.makedirs(options.output_dir, exist_ok=True)

    trajectory_path = os.path.join(
        options.output_dir, f"{candidate.session_id}.trajectory.json"
    )
    with open(trajectory_path, "w", encoding="utf-8") as f:
        json.dump(trajectory, f, ensure_ascii=False, indent=2)

    stats = _build_stats(
        nodes=nodes,
        trajectory=trajectory,
        candidate=candidate,
        model=model,
        model_config=model_config,
        session_meta=session_meta,
        system_prompt_source=system_prompt_source,
    )
    stats_path = os.path.join(
        options.output_dir, f"{candidate.session_id}.stats.json"
    )
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    candidate_meta = {
        "session_id": candidate.session_id,
        "agent_id": candidate.agent_id,
        "turns": stats["turns"],
        "domain": stats["domain"],
        "model": model,
        "output_path": trajectory_path,
        "message_count": len(trajectory["messages"]),
        "tool_count": len(trajectory["tools"]),
        "system_prompt_source": system_prompt_source,
    }

    return ProcessResult(
        session_id=candidate.session_id,
        ok=True,
        trajectory_path=trajectory_path,
        stats_path=stats_path,
        candidate_meta=candidate_meta,
    )


# ── stats + domain/title inference ────────────────────────────

def _build_stats(
    *,
    nodes: list[dict],
    trajectory: dict,
    candidate: SessionCandidate,
    model: str,
    model_config: dict,
    session_meta: dict,
    system_prompt_source: str,
) -> dict:
    """Compute the .stats.json body. Never mixes with trajectory content."""
    started_at, ended_at = _session_times_from_nodes(nodes)

    token_input = 0
    token_output = 0
    cache_read = 0
    cache_write = 0
    tool_use_count = 0
    tool_name_set: set[str] = set()
    compaction_count = 0
    full_user_messages = 0

    for node in nodes:
        ntype = node.get("type")
        if ntype == "compaction":
            if node.get("summary"):
                compaction_count += 1
            continue
        if ntype != "message":
            continue
        msg = node.get("message", {})
        role = msg.get("role")

        if role == "assistant":
            usage = msg.get("usage", {})
            token_input += usage.get("input", 0)
            token_output += usage.get("output", 0)
            cache_read += usage.get("cacheRead", 0)
            cache_write += usage.get("cacheWrite", 0)
            for block in msg.get("content", []):
                if isinstance(block, dict) and block.get("type") == "toolCall":
                    tool_use_count += 1
                    name = block.get("name", "")
                    if name:
                        tool_name_set.add(name)
        elif role == "user":
            for block in msg.get("content", []):
                if isinstance(block, dict) and block.get("type") == "text":
                    raw = block.get("text", "")
                    if is_system_startup_message(raw):
                        continue
                    if strip_metadata_prefix(raw):
                        full_user_messages += 1

    user_texts, tool_names = _extract_user_texts_and_tool_names(nodes)

    full_file_turns = sum(
        1 for n in nodes
        if n.get("type") == "message"
        and n.get("message", {}).get("role") == "assistant"
    )

    # Reasoning stats from OpenAI trajectory
    pure_text = 0
    rc_with_tc = 0
    rc_pure = 0
    for m in trajectory.get("messages", []):
        if m.get("role") != "assistant":
            continue
        has_tc = len(m.get("tool_calls", [])) > 0
        rc_val = m.get("reasoning_content", "")
        has_rc = isinstance(rc_val, str) and rc_val.strip() != ""
        if has_tc:
            if has_rc:
                rc_with_tc += 1
        else:
            pure_text += 1
            if has_rc:
                rc_pure += 1

    stats: dict = {
        "session_id": candidate.session_id,
        "agent_id": candidate.agent_id,
        "model": model,
        "provider": model_config["provider"],
        "thinking": model_config["thinking"],
        "cwd": session_meta.get("cwd", ""),
        "started_at": started_at,
        "ended_at": ended_at,
        "token_input": token_input,
        "token_output": token_output,
        "cache_read": cache_read,
        "cache_write": cache_write,
        "tool_use_count": tool_use_count,
        "tool_names": sorted(tool_name_set),
        "compaction_count": compaction_count,
        "full_user_messages": full_user_messages,
        "turns": full_file_turns,
        "has_compaction": candidate.has_compaction,
        "effective_asst": pure_text + rc_with_tc,
        "reasoning_asst": rc_pure + rc_with_tc,
        "system_prompt_source": system_prompt_source,
        "domain": _infer_domain(tool_names, user_texts),
        "title": _infer_title(user_texts),
        "review_status": "heuristic",
    }
    return stats


def _extract_user_texts_and_tool_names(
    nodes: list[dict],
) -> tuple[list[str], list[str]]:
    user_texts: list[str] = []
    tool_names: list[str] = []
    for node in nodes:
        if node.get("type") != "message":
            continue
        msg = node.get("message", {})
        role = msg.get("role")
        content = msg.get("content", [])

        if role == "user":
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    raw = block.get("text", "")
                    if not is_system_startup_message(raw):
                        stripped = strip_metadata_prefix(raw)
                        if stripped:
                            user_texts.append(stripped)

        elif role == "assistant":
            for block in content:
                if isinstance(block, dict) and block.get("type") == "toolCall":
                    name = block.get("name", "")
                    if name:
                        tool_names.append(name)
    return user_texts, tool_names


def _infer_domain(tool_names: list[str], user_texts: list[str]) -> str:
    tool_set = {t.lower() for t in tool_names}
    head = " ".join(user_texts[:3]).lower()

    has_code = bool(tool_set & _DOMAIN_CODE_TOOLS)
    has_web = bool(tool_set & _DOMAIN_WEB_TOOLS)
    has_browser = "browser" in tool_set
    has_msg = bool(tool_set & _DOMAIN_MSG_TOOLS)
    has_media = bool(tool_set & _DOMAIN_MEDIA_TOOLS)
    has_sessions = bool(tool_set & _DOMAIN_SESSION_TOOLS)
    has_cron = bool(tool_set & _DOMAIN_CRON_TOOLS)

    if has_msg and not has_code:
        return "communication"
    if has_media and not has_code:
        return "media_processing"
    if has_cron or has_sessions:
        return "automation"
    if any(kw in head for kw in _DOMAIN_MONITOR_KEYWORDS):
        return "monitoring"
    if has_web and not has_code:
        return "research"
    if has_code:
        return "development"
    if has_browser:
        return "research"
    return "development"


def _infer_title(user_texts: list[str], *, max_len: int = 30) -> str:
    for raw in user_texts:
        text = " ".join(raw.split())
        if not text:
            continue
        if len(text) <= max_len:
            return text
        cut = text[:max_len].rfind(" ")
        if cut > max_len // 2:
            return text[:cut] + "..."
        return text[:max_len] + "..."
    return "untitled"


