#!/usr/bin/env python3
"""Clawlens - OpenClaw Usage Insights Report Generator.

Analyzes OpenClaw conversation history and generates a multi-dimensional
report covering usage stats, task classification, friction analysis,
skills ecosystem, autonomous behavior audit, and multi-channel analysis.

Output formats: Markdown (default) or self-contained HTML with dark theme.

Pipeline:
  Stage 1: Data Collection (local) - scan session files, extract metadata
  Stage 2: LLM Facet Extraction (per-session, cached) - qualitative analysis
  Stage 3: Aggregation (local) - merge metadata + facets into stats
  Stage 4: Report Generation (parallel LLM) - generate report sections
"""

from __future__ import annotations

import argparse
import asyncio
import html as html_mod
import json
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import litellm

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VERSION = "1.1.0"

TASK_CATEGORIES = [
    "email_management",
    "scheduling",
    "info_retrieval",
    "content_creation",
    "coding_assistance",
    "automation",
    "smart_home",
    "file_operations",
    "communication",
    "planning",
    "personal_assistant",
]

FRICTION_CLAW = [
    "misunderstood_intent",
    "wrong_execution",
    "ignored_preference",
    "hallucinated_info",
    "excessive_action",
]

FRICTION_USER = [
    "insufficient_context",
    "unclear_instruction",
    "wrong_channel",
    "contradictory_request",
]

OUTCOMES = [
    "fully_achieved",
    "mostly_achieved",
    "partially_achieved",
    "not_achieved",
    "unclear",
]

SATISFACTION = [
    "happy",
    "satisfied",
    "likely_satisfied",
    "dissatisfied",
    "frustrated",
    "unsure",
]

ALL_SECTIONS = [
    "usage_overview",
    "task_classification",
    "friction_analysis",
    "skills_ecosystem",
    "autonomous_audit",
    "channel_analysis",
]

CATEGORY_LABELS = {
    "zh": {
        "email_management": "邮件管理",
        "scheduling": "日程协调",
        "info_retrieval": "信息检索",
        "content_creation": "内容创作",
        "coding_assistance": "编码辅助",
        "automation": "自动化脚本",
        "smart_home": "智能家居控制",
        "file_operations": "文件操作",
        "communication": "通信/消息",
        "planning": "规划/任务管理",
        "personal_assistant": "个人助理/杂项",
    },
    "en": {
        "email_management": "Email Management",
        "scheduling": "Scheduling",
        "info_retrieval": "Info Retrieval",
        "content_creation": "Content Creation",
        "coding_assistance": "Coding Assistance",
        "automation": "Automation",
        "smart_home": "Smart Home",
        "file_operations": "File Operations",
        "communication": "Communication",
        "planning": "Planning",
        "personal_assistant": "Personal Assistant",
    },
}

FRICTION_LABELS = {
    "zh": {
        "misunderstood_intent": "误解指令",
        "wrong_execution": "执行错误",
        "ignored_preference": "未遵循偏好",
        "hallucinated_info": "编造信息",
        "excessive_action": "过度操作",
        "insufficient_context": "上下文不足",
        "unclear_instruction": "指令模糊",
        "wrong_channel": "渠道不当",
        "contradictory_request": "矛盾请求",
    },
    "en": {
        "misunderstood_intent": "Misunderstood Intent",
        "wrong_execution": "Wrong Execution",
        "ignored_preference": "Ignored Preference",
        "hallucinated_info": "Hallucinated Info",
        "excessive_action": "Excessive Action",
        "insufficient_context": "Insufficient Context",
        "unclear_instruction": "Unclear Instruction",
        "wrong_channel": "Wrong Channel",
        "contradictory_request": "Contradictory Request",
    },
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SessionMeta:
    session_id: str
    session_key: str
    channel: str
    chat_type: str
    model: str
    updated_at: float
    total_tokens: int
    input_tokens: int
    output_tokens: int
    origin_label: str
    origin_provider: str
    start_time: str
    user_message_count: int
    assistant_message_count: int
    tool_use_counts: dict[str, int] = field(default_factory=dict)
    compaction_count: int = 0
    message_timestamps: list[str] = field(default_factory=list)
    message_hours: list[int] = field(default_factory=list)
    duration_minutes: float = 0.0
    first_user_message: str = ""
    has_errors: bool = False
    cost_total: float = 0.0
    transcript_text: str = ""


@dataclass
class SessionFacets:
    session_id: str
    underlying_goal: str = ""
    task_categories: dict[str, int] = field(default_factory=dict)
    outcome: str = "unclear"
    satisfaction: str = "unsure"
    friction_counts: dict[str, int] = field(default_factory=dict)
    friction_detail: str = ""
    skills_used: list[str] = field(default_factory=list)
    is_autonomous: bool = False
    autonomous_outcome: str = "n/a"
    brief_summary: str = ""


@dataclass
class AggregateStats:
    total_sessions: int = 0
    sessions_with_facets: int = 0
    total_messages: int = 0
    total_user_messages: int = 0
    total_assistant_messages: int = 0
    total_tokens: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    date_range: tuple[str, str] = ("", "")
    days_active: int = 0
    hour_distribution: dict[int, int] = field(default_factory=dict)
    weekday_distribution: dict[int, int] = field(default_factory=dict)
    task_categories: dict[str, int] = field(default_factory=dict)
    high_value_tasks: list[dict] = field(default_factory=list)
    friction_counts: dict[str, int] = field(default_factory=dict)
    friction_by_attribution: dict[str, int] = field(default_factory=dict)
    top_friction_patterns: list[dict] = field(default_factory=list)
    skills_installed: list[str] = field(default_factory=list)
    skills_used: dict[str, int] = field(default_factory=dict)
    skills_unused: list[str] = field(default_factory=list)
    channel_distribution: dict[str, int] = field(default_factory=dict)
    channel_task_types: dict[str, dict] = field(default_factory=dict)
    autonomous_sessions: int = 0
    autonomous_outcomes: dict[str, int] = field(default_factory=dict)
    outcomes: dict[str, int] = field(default_factory=dict)
    satisfaction: dict[str, int] = field(default_factory=dict)
    session_summaries: list[dict] = field(default_factory=list)
    tool_use_counts: dict[str, int] = field(default_factory=dict)
    models_used: dict[str, int] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

_verbose = False
_model_api_base: str | None = None
_model_api_key: str | None = None

_API_TYPE_TO_LITELLM_PREFIX = {
    "openai-completions": "openai",
    "anthropic-messages": "anthropic",
}


def log(msg: str) -> None:
    if _verbose:
        print(f"[clawlens] {msg}", file=sys.stderr)


def resolve_openclaw_model(agent_id: str = "main") -> tuple[str, str, str]:
    """Resolve LLM model from OpenClaw configuration.

    Reads ~/.openclaw/openclaw.json for the primary model and provider info,
    then ~/.openclaw/agents/{agent_id}/agent/auth-profiles.json for credentials.

    Returns:
        (litellm_model_string, api_base_url, api_key)

    Raises:
        RuntimeError: if config files are missing or malformed.
    """
    openclaw_dir = Path.home() / ".openclaw"

    # --- Read primary model from global config ---
    config_path = openclaw_dir / "openclaw.json"
    if not config_path.exists():
        raise RuntimeError(f"{config_path} not found")
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        raise RuntimeError(f"Failed to read {config_path}: {e}")

    try:
        primary = config["agents"]["defaults"]["model"]["primary"]
    except (KeyError, TypeError):
        raise RuntimeError(
            f"agents.defaults.model.primary not found in {config_path}"
        )

    # Parse "provider/model-id"
    if "/" not in primary:
        raise RuntimeError(
            f"Invalid primary model format '{primary}', expected 'provider/model-id'"
        )
    provider_name, model_id = primary.split("/", 1)

    # --- Look up provider details ---
    providers = config.get("models", {}).get("providers", {})
    if provider_name not in providers:
        raise RuntimeError(
            f"Provider '{provider_name}' not found in models.providers of {config_path}"
        )
    provider = providers[provider_name]
    base_url = provider.get("baseUrl")
    api_type = provider.get("api")
    if not base_url:
        raise RuntimeError(f"baseUrl missing for provider '{provider_name}'")
    if not api_type:
        raise RuntimeError(f"api type missing for provider '{provider_name}'")

    litellm_prefix = _API_TYPE_TO_LITELLM_PREFIX.get(api_type)
    if not litellm_prefix:
        raise RuntimeError(
            f"Unsupported API type '{api_type}' for provider '{provider_name}'. "
            f"Supported: {list(_API_TYPE_TO_LITELLM_PREFIX.keys())}"
        )

    # --- Read auth credentials ---
    auth_path = openclaw_dir / "agents" / agent_id / "agent" / "auth-profiles.json"
    if not auth_path.exists():
        raise RuntimeError(f"{auth_path} not found")
    try:
        auth_data = json.loads(auth_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        raise RuntimeError(f"Failed to read {auth_path}: {e}")

    # Find profile via lastGood
    last_good = auth_data.get("lastGood", {})
    profile_name = last_good.get(provider_name)
    if not profile_name:
        raise RuntimeError(
            f"No lastGood auth profile for provider '{provider_name}' in {auth_path}"
        )
    profiles = auth_data.get("profiles", {})
    profile = profiles.get(profile_name)
    if not profile:
        raise RuntimeError(
            f"Auth profile '{profile_name}' not found in {auth_path}"
        )

    auth_type = profile.get("type", "")
    if auth_type == "api_key":
        api_key = profile.get("key", "")
    elif auth_type == "oauth":
        api_key = profile.get("access", "")
        # Warn if token might be expired
        expires = profile.get("expires")
        if expires and isinstance(expires, (int, float)):
            if expires < time.time() * 1000:
                log(f"WARNING: OAuth token for provider '{provider_name}' may be expired")
    else:
        raise RuntimeError(
            f"Unknown auth type '{auth_type}' for profile '{profile_name}'"
        )

    if not api_key:
        raise RuntimeError(
            f"No API key/token found in auth profile '{profile_name}'"
        )

    litellm_model = f"{litellm_prefix}/{model_id}"
    log(f"Resolved OpenClaw model: {primary} -> litellm={litellm_model}, base={base_url}")
    return litellm_model, base_url, api_key


# ---------------------------------------------------------------------------
# Stage 1: Data Collection
# ---------------------------------------------------------------------------

def parse_jsonl(filepath: Path) -> list[dict]:
    """Read a JSONL file, skip malformed lines."""
    entries: list[dict] = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    log(f"  Skipping malformed line {line_num} in {filepath.name}")
    except FileNotFoundError:
        log(f"  File not found: {filepath}")
    except OSError as e:
        log(f"  Error reading {filepath}: {e}")
    return entries


def build_transcript(entries: list[dict], max_chars: int = 80000) -> str:
    """Build a readable transcript from JSONL entries for LLM analysis."""
    parts: list[str] = []
    total_chars = 0
    for entry in entries:
        if entry.get("type") == "compaction":
            text = f"[COMPACTION SUMMARY]: {entry.get('summary', '')}"
            parts.append(text)
            total_chars += len(text)
        elif entry.get("type") == "message":
            msg = entry.get("message", {})
            role = msg.get("role", "unknown")
            if role == "toolResult":
                tool_name = msg.get("toolName", "unknown")
                is_error = msg.get("isError", False)
                content_blocks = msg.get("content", [])
                result_text = ""
                for block in content_blocks:
                    if isinstance(block, dict) and block.get("type") == "text":
                        result_text += block.get("text", "")[:500]
                prefix = f"[TOOL RESULT: {tool_name}]" + (" [ERROR]" if is_error else "")
                text = f"{prefix}: {result_text}"
            else:
                content_blocks = msg.get("content", [])
                text_parts = []
                for block in content_blocks:
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                        elif block.get("type") == "tool_use":
                            tool_name = block.get("name", "unknown")
                            tool_input = json.dumps(block.get("input", {}), ensure_ascii=False)
                            if len(tool_input) > 300:
                                tool_input = tool_input[:300] + "..."
                            text_parts.append(f"[TOOL CALL: {tool_name}({tool_input})]")
                    elif isinstance(block, str):
                        text_parts.append(block)
                role_label = "USER" if role == "user" else "ASSISTANT"
                text = f"[{role_label}]: {' '.join(text_parts)}"

            parts.append(text)
            total_chars += len(text)
            if total_chars > max_chars:
                parts.append("[... transcript truncated ...]")
                break

    return "\n\n".join(parts)


def extract_session_meta(session_key: str, session_entry: dict, entries: list[dict]) -> SessionMeta | None:
    """Extract structured metadata from a session's JSONL entries."""
    session_id = session_entry.get("sessionId", "")

    # Find session header
    start_time = ""
    for entry in entries:
        if entry.get("type") == "session":
            start_time = entry.get("timestamp", "")
            break

    user_msg_count = 0
    asst_msg_count = 0
    tool_counts: dict[str, int] = Counter()
    compaction_count = 0
    timestamps: list[str] = []
    hours: list[int] = []
    first_user_msg = ""
    has_errors = False
    cost_total = 0.0
    sum_input_tokens = 0
    sum_output_tokens = 0

    for entry in entries:
        if entry.get("type") == "compaction":
            compaction_count += 1
            continue
        if entry.get("type") != "message":
            continue

        msg = entry.get("message", {})
        role = msg.get("role", "")
        ts = entry.get("timestamp", "")

        if ts:
            timestamps.append(ts)
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                hours.append(dt.hour)
            except (ValueError, TypeError):
                pass

        if role == "user":
            user_msg_count += 1
            if not first_user_msg:
                for block in msg.get("content", []):
                    if isinstance(block, dict) and block.get("type") == "text":
                        first_user_msg = block.get("text", "")[:200]
                        break
                    elif isinstance(block, str):
                        first_user_msg = block[:200]
                        break
        elif role == "assistant":
            asst_msg_count += 1
            for block in msg.get("content", []):
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    tool_name = block.get("name", "unknown")
                    tool_counts[tool_name] += 1
            usage = msg.get("usage", {})
            if usage:
                sum_input_tokens += usage.get("inputTokens", 0) or 0
                sum_output_tokens += usage.get("outputTokens", 0) or 0
                cost_info = usage.get("cost", {})
                if isinstance(cost_info, dict):
                    cost_total += cost_info.get("total", 0) or 0
        elif role == "toolResult":
            if msg.get("isError", False):
                has_errors = True

    # Filter: skip trivial sessions
    if user_msg_count < 2:
        return None

    # Calculate duration
    duration_minutes = 0.0
    if len(timestamps) >= 2:
        try:
            t_start = datetime.fromisoformat(timestamps[0].replace("Z", "+00:00"))
            t_end = datetime.fromisoformat(timestamps[-1].replace("Z", "+00:00"))
            duration_minutes = (t_end - t_start).total_seconds() / 60.0
        except (ValueError, TypeError):
            pass

    if duration_minutes < 1.0:
        return None

    origin = session_entry.get("origin", {})

    meta = SessionMeta(
        session_id=session_id,
        session_key=session_key,
        channel=session_entry.get("lastChannel", "unknown"),
        chat_type=session_entry.get("chatType", "unknown"),
        model=session_entry.get("model", "unknown"),
        updated_at=session_entry.get("updatedAt", 0),
        total_tokens=session_entry.get("totalTokens", 0) or (sum_input_tokens + sum_output_tokens),
        input_tokens=session_entry.get("inputTokens", 0) or sum_input_tokens,
        output_tokens=session_entry.get("outputTokens", 0) or sum_output_tokens,
        origin_label=origin.get("label", ""),
        origin_provider=origin.get("provider", ""),
        start_time=start_time,
        user_message_count=user_msg_count,
        assistant_message_count=asst_msg_count,
        tool_use_counts=dict(tool_counts),
        compaction_count=compaction_count,
        message_timestamps=timestamps,
        message_hours=hours,
        duration_minutes=round(duration_minutes, 1),
        first_user_message=first_user_msg,
        has_errors=has_errors,
        cost_total=round(cost_total, 6),
        transcript_text=build_transcript(entries),
    )
    return meta


def _normalize_timestamp(ts: float) -> float:
    """Normalize a timestamp to seconds. Handles millisecond timestamps."""
    if ts > 1e12:  # milliseconds
        return ts / 1000.0
    return ts


def collect_sessions(agent_id: str, days: int, max_sessions: int) -> list[SessionMeta]:
    """Stage 1: Scan session files and extract metadata.

    Reads the sessions.json index first, then also discovers unindexed JSONL
    files on disk to ensure historical sessions are not missed.
    """
    base_dir = Path.home() / ".openclaw" / "agents" / agent_id / "sessions"

    if not base_dir.exists():
        log(f"Sessions directory not found: {base_dir}")
        print(f"Error: Sessions directory not found at {base_dir}", file=sys.stderr)
        return []

    cutoff_s = time.time() - (days * 86400)

    # Build index from sessions.json (maps sessionId -> metadata)
    sessions_index: dict[str, dict] = {}
    index_path = base_dir / "sessions.json"
    if index_path.exists():
        log(f"Reading session index: {index_path}")
        with open(index_path, "r", encoding="utf-8") as f:
            raw_index = json.load(f)
        for key, entry in raw_index.items():
            sid = entry.get("sessionId", "")
            if sid:
                entry["_session_key"] = key
                sessions_index[sid] = entry
        log(f"  Index contains {len(sessions_index)} sessions")

    # Discover all JSONL files on disk (including unindexed ones)
    all_jsonl = sorted(base_dir.glob("*.jsonl"))
    log(f"  Found {len(all_jsonl)} JSONL files on disk")

    # Filter by file modification time as a quick pre-filter
    candidate_files: list[tuple[Path, float]] = []
    for jp in all_jsonl:
        try:
            mtime = jp.stat().st_mtime
            if mtime >= cutoff_s:
                candidate_files.append((jp, mtime))
        except (PermissionError, OSError):
            continue

    # Sort by modification time (most recent first), cap at max_sessions
    candidate_files.sort(key=lambda x: x[1], reverse=True)
    candidate_files = candidate_files[:max_sessions]
    log(f"  {len(candidate_files)} files within last {days} days")

    results: list[SessionMeta] = []
    seen_ids: set[str] = set()

    for jsonl_path, _mtime in candidate_files:
        # Extract session ID from filename (e.g. "abc123.jsonl" -> "abc123")
        sid = jsonl_path.stem
        # Skip topic files like "{sessionId}-topic-{threadId}.jsonl"
        if "-topic-" in sid:
            continue
        if sid in seen_ids:
            continue
        seen_ids.add(sid)

        entries = parse_jsonl(jsonl_path)
        if not entries:
            continue

        # Use index metadata if available, otherwise build minimal entry
        index_entry = sessions_index.get(sid, {})
        session_key = index_entry.get("_session_key", f"file:{sid}")

        meta = extract_session_meta(session_key, index_entry, entries)
        if meta:
            # Ensure session_id is set even if not in index
            if not meta.session_id:
                meta.session_id = sid
            results.append(meta)
            log(f"  Collected: {sid[:8]}... ({meta.user_message_count} user msgs, {meta.duration_minutes}min)")

    log(f"Stage 1 complete: {len(results)} valid sessions")
    return results


# ---------------------------------------------------------------------------
# Stage 2: LLM Facet Extraction
# ---------------------------------------------------------------------------

def get_cache_dir(agent_id: str) -> Path:
    cache_dir = Path.home() / ".openclaw" / "agents" / agent_id / "sessions" / ".clawlens-cache" / "facets"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def load_cached_facets(agent_id: str, session_id: str) -> SessionFacets | None:
    cache_path = get_cache_dir(agent_id) / f"{session_id}.json"
    if not cache_path.exists():
        return None
    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return SessionFacets(**data)
    except (json.JSONDecodeError, TypeError, KeyError):
        return None


def save_cached_facets(agent_id: str, facets: SessionFacets) -> None:
    cache_path = get_cache_dir(agent_id) / f"{facets.session_id}.json"
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(asdict(facets), f, ensure_ascii=False, indent=2)


FACET_EXTRACTION_PROMPT = """Analyze this OpenClaw conversation session and extract structured facets.

You are analyzing interactions between a user and their personal AI assistant (OpenClaw/Claw), NOT a coding tool. Focus on assistant-style tasks like email, scheduling, info retrieval, content creation, etc. Coding tasks are also possible.

TASK CATEGORIES (count how many distinct requests the user made in each category):
- email_management: email drafting, reading, organizing, replying
- scheduling: calendar, reminders, appointments, time management
- info_retrieval: searching, looking up, Q&A, fact-checking
- content_creation: writing, editing, summarizing documents, creative work
- coding_assistance: code help, debugging, scripting, code review
- automation: setting up cron jobs, workflows, automations
- smart_home: device control, IoT, home automation
- file_operations: file management, organization, backup
- communication: messaging across channels, social media
- planning: project planning, task management, goal setting
- personal_assistant: general assistance, misc tasks

OUTCOME (overall for the session):
- fully_achieved: all user goals met
- mostly_achieved: most goals met, minor gaps
- partially_achieved: some goals met, significant gaps
- not_achieved: user goals not met
- unclear: cannot determine from transcript

SATISFACTION (infer from user responses):
- happy / satisfied / likely_satisfied / dissatisfied / frustrated / unsure

FRICTION (identify specific instances):
Claw-side:
- misunderstood_intent: Claw misunderstood what user wanted
- wrong_execution: Claw executed incorrectly
- ignored_preference: Claw didn't follow known user preferences
- hallucinated_info: Claw made up facts or information
- excessive_action: Claw did more than asked

User-side:
- insufficient_context: user didn't provide enough context
- unclear_instruction: user's instruction was ambiguous
- wrong_channel: task was initiated in an inappropriate channel
- contradictory_request: user gave conflicting instructions

AUTONOMOUS BEHAVIOR:
Set is_autonomous=true if this session appears to be initiated by Claw itself (cron job, heartbeat, scheduled task, background monitoring) rather than by the user. Signs: first message is from assistant, mentions scheduled/automated check, no initial user prompt.
If autonomous, set autonomous_outcome to: "confirmed" (user acknowledged positively), "adopted" (user acted on it), "rejected" (user rejected/corrected), "ignored" (no user response), "n/a" (not autonomous).

SKILLS:
List any skill/tool names that were explicitly invoked (from tool_use blocks or mentions).

SESSION TRANSCRIPT:
{transcript}

RESPOND WITH ONLY A VALID JSON OBJECT (no markdown fences, no explanation):
{{
  "underlying_goal": "one sentence describing user's primary goal",
  "task_categories": {{"category_key": count, ...}},
  "outcome": "one of: fully_achieved, mostly_achieved, partially_achieved, not_achieved, unclear",
  "satisfaction": "one of: happy, satisfied, likely_satisfied, dissatisfied, frustrated, unsure",
  "friction_counts": {{"friction_key": count, ...}},
  "friction_detail": "brief narrative of what went wrong (or 'none' if no friction)",
  "skills_used": ["skill_name", ...],
  "is_autonomous": false,
  "autonomous_outcome": "n/a",
  "brief_summary": "2-3 sentence summary of the session"
}}"""


CHUNK_SUMMARY_PROMPT = """Summarize this portion of an OpenClaw conversation session.
Preserve key details: what the user asked for, what Claw did, any friction or errors, tools/skills used, and whether goals were met.
Keep the summary under 2000 characters.

TRANSCRIPT CHUNK:
{chunk}

SUMMARY:"""


async def llm_call(prompt: str, model: str, max_tokens: int = 4096, retries: int = 3) -> str:
    """Make an LLM call via litellm with retry."""
    kwargs: dict[str, Any] = dict(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.3,
    )
    if _model_api_base:
        kwargs["api_base"] = _model_api_base
    if _model_api_key:
        kwargs["api_key"] = _model_api_key

    for attempt in range(retries + 1):
        try:
            response = await litellm.acompletion(**kwargs)
            return response.choices[0].message.content or ""
        except Exception as e:
            if attempt < retries:
                wait = 2 ** attempt
                log(f"  LLM call failed (attempt {attempt + 1}): {e}, retrying in {wait}s...")
                await asyncio.sleep(wait)
            else:
                log(f"  LLM call failed after {retries + 1} attempts: {e}")
                raise


async def summarize_long_transcript(transcript: str, model: str) -> str:
    """Chunk and summarize a long transcript before facet extraction."""
    chunk_size = 60000  # chars per chunk
    chunks = [transcript[i:i + chunk_size] for i in range(0, len(transcript), chunk_size)]
    log(f"  Summarizing long transcript: {len(chunks)} chunks")

    summaries = []
    for i, chunk in enumerate(chunks):
        prompt = CHUNK_SUMMARY_PROMPT.replace("{chunk}", chunk)
        summary = await llm_call(prompt, model, max_tokens=2048)
        summaries.append(f"[Part {i + 1}]: {summary}")

    return "\n\n".join(summaries)


def parse_facets_json(raw: str, session_id: str) -> SessionFacets:
    """Parse LLM output into SessionFacets, handling common issues."""
    # Strip markdown fences if present
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Try to find JSON object in the text
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                data = json.loads(text[start:end])
            except json.JSONDecodeError:
                log(f"  Failed to parse facets JSON for {session_id[:8]}")
                return SessionFacets(session_id=session_id)
        else:
            log(f"  No JSON found in facets response for {session_id[:8]}")
            return SessionFacets(session_id=session_id)

    return SessionFacets(
        session_id=session_id,
        underlying_goal=data.get("underlying_goal", ""),
        task_categories=data.get("task_categories", {}),
        outcome=data.get("outcome", "unclear"),
        satisfaction=data.get("satisfaction", "unsure"),
        friction_counts=data.get("friction_counts", {}),
        friction_detail=data.get("friction_detail", ""),
        skills_used=data.get("skills_used", []),
        is_autonomous=data.get("is_autonomous", False),
        autonomous_outcome=data.get("autonomous_outcome", "n/a"),
        brief_summary=data.get("brief_summary", ""),
    )


async def extract_single_facet(
    meta: SessionMeta, model: str, agent_id: str, semaphore: asyncio.Semaphore
) -> SessionFacets:
    """Extract facets for a single session."""
    async with semaphore:
        transcript = meta.transcript_text

        # Handle long transcripts
        if len(transcript) > 100000:
            transcript = await summarize_long_transcript(transcript, model)

        prompt = FACET_EXTRACTION_PROMPT.replace("{transcript}", transcript)

        try:
            raw = await llm_call(prompt, model, max_tokens=2048)
            facets = parse_facets_json(raw, meta.session_id)
            save_cached_facets(agent_id, facets)
            log(f"  Facets extracted: {meta.session_id[:8]}... -> {facets.brief_summary[:60]}")
            return facets
        except Exception as e:
            log(f"  Facet extraction failed for {meta.session_id[:8]}: {e}")
            return SessionFacets(session_id=meta.session_id)


async def extract_facets(
    sessions: list[SessionMeta],
    agent_id: str,
    model: str,
    concurrency: int,
    no_cache: bool,
    max_uncached: int = 50,
) -> list[SessionFacets]:
    """Stage 2: Extract facets for all sessions."""
    log(f"Stage 2: Extracting facets for {len(sessions)} sessions (model={model})")

    results: list[SessionFacets] = []
    to_extract: list[SessionMeta] = []

    for meta in sessions:
        if not no_cache:
            cached = load_cached_facets(agent_id, meta.session_id)
            if cached:
                results.append(cached)
                log(f"  Cached: {meta.session_id[:8]}...")
                continue
        to_extract.append(meta)

    log(f"  {len(results)} cached, {len(to_extract)} to extract")

    # Cap uncached extractions
    if len(to_extract) > max_uncached:
        log(f"  Capping to {max_uncached} uncached sessions")
        to_extract = to_extract[:max_uncached]

    if to_extract:
        semaphore = asyncio.Semaphore(concurrency)
        tasks = [extract_single_facet(m, model, agent_id, semaphore) for m in to_extract]
        extracted = await asyncio.gather(*tasks)
        results.extend(extracted)

    log(f"Stage 2 complete: {len(results)} total facets")
    return results


# ---------------------------------------------------------------------------
# Stage 3: Aggregation
# ---------------------------------------------------------------------------

def scan_installed_skills() -> list[str]:
    """Scan ~/.openclaw/skills/ for installed skill names."""
    skills_dir = Path.home() / ".openclaw" / "skills"
    if not skills_dir.exists():
        log("Skills directory not found, skipping installed skills scan")
        return []

    skills: list[str] = []
    for item in skills_dir.iterdir():
        if item.is_dir():
            # Check if it looks like a skill (has SKILL.md or _meta.json)
            if (item / "SKILL.md").exists() or (item / "_meta.json").exists():
                skills.append(item.name)
    log(f"Found {len(skills)} installed skills")
    return skills


def aggregate(sessions: list[SessionMeta], facets: list[SessionFacets]) -> AggregateStats:
    """Stage 3: Aggregate all metadata and facets into statistics."""
    log(f"Stage 3: Aggregating {len(sessions)} sessions, {len(facets)} facets")

    stats = AggregateStats()
    stats.total_sessions = len(sessions)
    stats.sessions_with_facets = len(facets)

    facets_by_id = {f.session_id: f for f in facets}

    all_timestamps: list[str] = []
    active_dates: set[str] = set()
    task_cats: Counter = Counter()
    friction_all: Counter = Counter()
    friction_claw_total = 0
    friction_user_total = 0
    channel_counts: Counter = Counter()
    channel_tasks: dict[str, Counter] = defaultdict(Counter)
    skills_used: Counter = Counter()
    tool_counts: Counter = Counter()
    model_counts: Counter = Counter()
    outcomes: Counter = Counter()
    satisfaction_counts: Counter = Counter()
    auto_sessions = 0
    auto_outcomes: Counter = Counter()
    session_summaries: list[dict] = []

    for meta in sessions:
        stats.total_user_messages += meta.user_message_count
        stats.total_assistant_messages += meta.assistant_message_count
        stats.total_messages += meta.user_message_count + meta.assistant_message_count
        stats.total_tokens += meta.total_tokens
        stats.total_input_tokens += meta.input_tokens
        stats.total_output_tokens += meta.output_tokens
        stats.total_cost += meta.cost_total

        all_timestamps.extend(meta.message_timestamps)
        for h in meta.message_hours:
            stats.hour_distribution[h] = stats.hour_distribution.get(h, 0) + 1

        for ts in meta.message_timestamps:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                date_str = dt.strftime("%Y-%m-%d")
                active_dates.add(date_str)
                wd = dt.weekday()
                stats.weekday_distribution[wd] = stats.weekday_distribution.get(wd, 0) + 1
            except (ValueError, TypeError):
                pass

        channel_counts[meta.channel] += 1
        for tool, count in meta.tool_use_counts.items():
            tool_counts[tool] += count
        model_counts[meta.model] += 1

        # Merge facets
        f = facets_by_id.get(meta.session_id)
        if f:
            for cat, count in f.task_categories.items():
                count = count if isinstance(count, (int, float)) else 1
                task_cats[cat] += int(count)
                channel_tasks[meta.channel][cat] += int(count)

            for fric, count in f.friction_counts.items():
                count = count if isinstance(count, (int, float)) else 1
                friction_all[fric] += int(count)
                if fric in FRICTION_CLAW:
                    friction_claw_total += int(count)
                elif fric in FRICTION_USER:
                    friction_user_total += int(count)

            for skill in f.skills_used:
                skills_used[skill] += 1

            outcomes[f.outcome] += 1
            satisfaction_counts[f.satisfaction] += 1

            if f.is_autonomous:
                auto_sessions += 1
                auto_outcomes[f.autonomous_outcome] += 1

            if len(session_summaries) < 50:
                session_summaries.append({
                    "session_id": meta.session_id,
                    "channel": meta.channel,
                    "summary": f.brief_summary,
                    "goal": f.underlying_goal,
                    "outcome": f.outcome,
                    "friction_detail": f.friction_detail,
                    "duration_minutes": meta.duration_minutes,
                    "is_autonomous": f.is_autonomous,
                })

    # Date range
    if all_timestamps:
        try:
            sorted_ts = sorted(all_timestamps)
            start_dt = datetime.fromisoformat(sorted_ts[0].replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(sorted_ts[-1].replace("Z", "+00:00"))
            stats.date_range = (start_dt.strftime("%Y-%m-%d"), end_dt.strftime("%Y-%m-%d"))
        except (ValueError, TypeError):
            pass

    stats.days_active = len(active_dates)
    stats.task_categories = dict(task_cats.most_common())
    stats.friction_counts = dict(friction_all.most_common())
    stats.friction_by_attribution = {"claw": friction_claw_total, "user": friction_user_total}
    stats.channel_distribution = dict(channel_counts.most_common())
    stats.channel_task_types = {ch: dict(ct) for ch, ct in channel_tasks.items()}
    stats.outcomes = dict(outcomes)
    stats.satisfaction = dict(satisfaction_counts)
    stats.autonomous_sessions = auto_sessions
    stats.autonomous_outcomes = dict(auto_outcomes)
    stats.session_summaries = session_summaries
    stats.tool_use_counts = dict(tool_counts.most_common())
    stats.models_used = dict(model_counts.most_common())
    stats.total_cost = round(stats.total_cost, 4)

    # Skills ecosystem
    installed = scan_installed_skills()
    stats.skills_installed = installed
    stats.skills_used = dict(skills_used.most_common())
    stats.skills_unused = [s for s in installed if s not in skills_used]

    # High-value tasks: categories with highest counts
    if task_cats:
        top = task_cats.most_common(3)
        stats.high_value_tasks = [{"category": cat, "count": cnt} for cat, cnt in top]

    # Top friction patterns (with detail from summaries)
    friction_details: list[dict] = []
    for summary in session_summaries:
        if summary.get("friction_detail") and summary["friction_detail"] != "none":
            friction_details.append(summary)
    stats.top_friction_patterns = friction_details[:10]

    log(f"Stage 3 complete: {stats.total_sessions} sessions, {stats.days_active} active days")
    return stats


# ---------------------------------------------------------------------------
# Stage 4: Report Generation
# ---------------------------------------------------------------------------

def _make_dimension_prompt(dimension: str, stats: AggregateStats, lang: str) -> str:
    """Build the LLM prompt for a specific report dimension."""
    lang_instruction = (
        "Write in Chinese (zh-CN). Use second person ('你'). Be direct and actionable."
        if lang == "zh"
        else "Write in English. Use second person ('you'). Be direct and actionable."
    )

    stats_json = json.dumps(asdict(stats), ensure_ascii=False, default=str)

    # Trim stats_json if too long - keep under 50K chars
    if len(stats_json) > 50000:
        # Remove transcript-heavy fields
        trimmed = asdict(stats)
        trimmed.pop("session_summaries", None)
        stats_json = json.dumps(trimmed, ensure_ascii=False, default=str)

    base = f"""You are generating one section of a usage insights report for an OpenClaw personal AI assistant user.
{lang_instruction}

Based on the following aggregated usage data, write the section described below.

FORMAT: Output well-structured Markdown. Use tables, lists, and bold text for emphasis.
Do NOT output JSON. Output only the markdown content for this section (no top-level heading, I will add it).
Do NOT add a section number prefix.

AGGREGATED DATA:
{stats_json}

"""
    section_instructions = {
        "usage_overview": """SECTION: Usage Overview (使用概览)

Write a usage overview section containing:
1. A statistics table with: total sessions, total messages, active days, input/output tokens, total cost
2. Activity time distribution: describe peak hours (from hour_distribution) and weekday patterns (from weekday_distribution, 0=Monday)
3. Models used breakdown
4. Token consumption trend description

Use tables for quantitative data. Highlight notable patterns.""",

        "task_classification": """SECTION: Task Classification (任务分类)

Write a task classification section containing:
1. A table showing each task category, its count, and percentage of total
2. Highlight the top 3 most frequent categories with brief analysis
3. Identify high-value tasks (highest frequency = most automation potential)
4. Note any surprising or notable patterns in how the user uses Claw

Category labels to use: """
        + json.dumps(CATEGORY_LABELS.get(lang, CATEGORY_LABELS["en"]), ensure_ascii=False),

        "friction_analysis": """SECTION: Friction Analysis (摩擦分析)

Write a friction analysis section containing:
1. Summary: total friction events, split between Claw-side vs User-side
2. A table of Claw-side friction types with counts and a brief example from session_summaries
3. A table of User-side friction types with counts and a brief example
4. Top 3 friction patterns described narratively with specific examples from top_friction_patterns
5. Actionable recommendations to reduce friction

Friction labels to use: """
        + json.dumps(FRICTION_LABELS.get(lang, FRICTION_LABELS["en"]), ensure_ascii=False),

        "skills_ecosystem": """SECTION: Skills Ecosystem Analysis (Skills 生态分析)

Write a skills ecosystem section containing:
1. Overview: number of installed vs actually used skills
2. A table of used skills ranked by frequency
3. List of installed but unused skills with cleanup suggestions
4. Based on task_categories distribution, suggest what kinds of skills could be useful
5. Note any skills that are heavily relied upon

If no skills data is available, note that and suggest the user explore the skill ecosystem.""",

        "autonomous_audit": """SECTION: Autonomous Behavior Audit (自主行为审计)

Write an autonomous behavior audit section containing:
1. Total autonomous sessions count
2. Breakdown by outcome: confirmed, adopted, rejected, ignored
3. User confirmation/adoption rate vs rejection/ignore rate
4. Flag any concerning patterns
5. Trend assessment: is autonomous behavior accuracy improving?

If no autonomous sessions were detected, briefly note that and explain what autonomous behavior means in the OpenClaw context.""",

        "channel_analysis": """SECTION: Multi-Channel Analysis (多渠道分析)

Write a multi-channel analysis section containing:
1. A table showing each channel, session count, and percentage
2. Cross-tabulation: which task types are done on which channels
3. Channel mismatch detection: identify tasks that might be better suited to a different channel
4. Optimization suggestions for channel usage

If only one channel is used, note that and suggest exploring multi-channel workflows.""",
    }

    return base + section_instructions.get(dimension, f"SECTION: {dimension}\nGenerate content for this dimension.")


def _make_synthesis_prompt(dimension_outputs: dict[str, str], stats: AggregateStats, lang: str) -> str:
    """Build the synthesis prompt for the at-a-glance summary."""
    lang_instruction = (
        "Write in Chinese (zh-CN). Use second person ('你'). Be concise and insightful."
        if lang == "zh"
        else "Write in English. Use second person ('you'). Be concise and insightful."
    )

    combined = "\n\n---\n\n".join(
        f"### {dim}\n{content}" for dim, content in dimension_outputs.items()
    )

    return f"""You are writing the executive summary for an OpenClaw usage insights report.
{lang_instruction}

Based on all the dimension analyses below, write a concise "At a Glance" summary (4-6 sentences) covering:
1. **What's working well** - the most effective usage patterns
2. **What's hindering** - the biggest friction or inefficiency
3. **Quick win** - one immediately actionable improvement
4. **Forward-looking** - one ambitious suggestion for deeper integration

Output ONLY the summary paragraph in Markdown. No headings, no bullet points - just a flowing paragraph.

DIMENSION ANALYSES:
{combined}"""


async def _generate_report_sections(
    stats: AggregateStats,
    sections: list[str],
    model: str,
    lang: str,
    concurrency: int,
) -> tuple[dict[str, str], str]:
    """Generate LLM content for each report section and the synthesis.

    Returns:
        (dimension_outputs, at_a_glance) - raw Markdown strings per section
    """
    log(f"Generating report sections: {sections}")

    semaphore = asyncio.Semaphore(concurrency)

    async def gen_section(dim: str) -> tuple[str, str]:
        async with semaphore:
            prompt = _make_dimension_prompt(dim, stats, lang)
            log(f"  Generating: {dim}")
            try:
                content = await llm_call(prompt, model, max_tokens=4096)
                log(f"  Done: {dim} ({len(content)} chars)")
                return dim, content
            except Exception as e:
                log(f"  Failed: {dim}: {e}")
                error_note = "此章节生成失败，请重试。" if lang == "zh" else "This section failed to generate. Please retry."
                return dim, f"*{error_note}*"

    tasks = [gen_section(dim) for dim in sections]
    results = await asyncio.gather(*tasks)
    dimension_outputs = dict(results)

    log("  Generating: at_a_glance (synthesis)")
    try:
        synthesis_prompt = _make_synthesis_prompt(dimension_outputs, stats, lang)
        at_a_glance = await llm_call(synthesis_prompt, model, max_tokens=1024)
    except Exception:
        at_a_glance = ""

    return dimension_outputs, at_a_glance


async def generate_report(
    stats: AggregateStats,
    sections: list[str],
    model: str,
    lang: str,
    concurrency: int,
) -> str:
    """Stage 4: Generate the final Markdown report."""
    log(f"Stage 4: Generating Markdown report")

    dimension_outputs, at_a_glance = await _generate_report_sections(
        stats, sections, model, lang, concurrency,
    )

    # Assemble final report
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    date_start, date_end = stats.date_range

    if lang == "zh":
        title = "Clawlens 使用洞察报告"
        meta_line = f"> 分析期间: {date_start} ~ {date_end} | {stats.total_sessions} 会话 | {stats.total_messages} 消息 | {stats.days_active} 活跃天"
        summary_heading = "概览摘要"
        footer = f"*报告由 clawlens v{VERSION} 生成于 {now_str}*"
    else:
        title = "Clawlens Usage Insights Report"
        meta_line = f"> Analysis period: {date_start} ~ {date_end} | {stats.total_sessions} sessions | {stats.total_messages} messages | {stats.days_active} active days"
        summary_heading = "At a Glance"
        footer = f"*Report generated by clawlens v{VERSION} at {now_str}*"

    section_headings = {
        "zh": {
            "usage_overview": "使用概览",
            "task_classification": "任务分类",
            "friction_analysis": "摩擦分析",
            "skills_ecosystem": "Skills 生态分析",
            "autonomous_audit": "自主行为审计",
            "channel_analysis": "多渠道分析",
        },
        "en": {
            "usage_overview": "Usage Overview",
            "task_classification": "Task Classification",
            "friction_analysis": "Friction Analysis",
            "skills_ecosystem": "Skills Ecosystem",
            "autonomous_audit": "Autonomous Behavior Audit",
            "channel_analysis": "Multi-Channel Analysis",
        },
    }
    headings = section_headings.get(lang, section_headings["en"])

    parts = [
        f"# {title}",
        "",
        meta_line,
        "",
    ]

    if at_a_glance:
        parts.extend([
            f"## {summary_heading}",
            "",
            at_a_glance,
            "",
            "---",
            "",
        ])

    for i, dim in enumerate(sections, 1):
        heading = headings.get(dim, dim)
        content = dimension_outputs.get(dim, "")
        parts.extend([
            f"## {i}. {heading}",
            "",
            content,
            "",
            "---",
            "",
        ])

    parts.append(footer)

    log("Stage 4 complete: report assembled")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# HTML Report Template & Generation
# ---------------------------------------------------------------------------

HTML_CSS = """\
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface2: #232733;
  --border: #2e3345;
  --text: #e2e4eb;
  --text-dim: #8b8fa3;
  --accent: #7c6aef;
  --accent-light: #9d8ff5;
  --green: #34d399;
  --orange: #fb923c;
  --red: #f87171;
  --blue: #60a5fa;
  --cyan: #22d3ee;
  --pink: #f472b6;
  --yellow: #fbbf24;
  --code-bg: #141720;
  --code-border: #2a2f40;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
  font-size: 15px;
}

/* ---- Animations ---- */
@keyframes fadeSlideIn {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes glowPulse {
  0%, 100% { box-shadow: 0 0 15px rgba(124, 106, 239, 0.1); }
  50%      { box-shadow: 0 0 30px rgba(124, 106, 239, 0.25); }
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(-6px); }
}
@keyframes gradientShift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* ---- Hero ---- */
.hero {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #1a1040 0%, #0f1117 50%, #0a1628 100%);
  border-bottom: 1px solid var(--border);
  padding: 72px 24px 56px;
  text-align: center;
}
.hero::before {
  content: '';
  position: absolute;
  top: -20%; right: -10%;
  width: 500px; height: 500px;
  border-radius: 50%;
  background: var(--accent);
  filter: blur(160px);
  opacity: 0.12;
  pointer-events: none;
}
.hero::after {
  content: '';
  position: absolute;
  bottom: -30%; left: -5%;
  width: 400px; height: 400px;
  border-radius: 50%;
  background: var(--cyan);
  filter: blur(150px);
  opacity: 0.08;
  pointer-events: none;
}
.hero h1 {
  position: relative;
  z-index: 1;
  font-size: 2.6em;
  font-weight: 800;
  background: linear-gradient(135deg, var(--accent-light), var(--cyan), var(--accent-light));
  background-size: 200% 200%;
  animation: gradientShift 6s ease infinite;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 12px;
}
.hero .subtitle {
  position: relative; z-index: 1;
  color: var(--text-dim);
  font-size: 1.05em;
}
.hero .meta {
  position: relative; z-index: 1;
  margin-top: 24px;
  display: flex;
  gap: 14px;
  justify-content: center;
  flex-wrap: wrap;
}
.hero .meta span {
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  padding: 7px 18px;
  border-radius: 24px;
  font-size: 0.85em;
  color: var(--text-dim);
  backdrop-filter: blur(8px);
}
.hero .meta span strong { color: var(--text); }

/* ---- Grid background overlay ---- */
.grid-bg {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
  background-size: 48px 48px;
  z-index: 0;
  pointer-events: none;
}

/* ---- Sticky nav ---- */
.toc {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(15, 17, 23, 0.92);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--border);
  padding: 10px 0;
}
.toc-inner {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  gap: 4px;
  overflow-x: auto;
  scrollbar-width: none;
}
.toc-inner::-webkit-scrollbar { display: none; }
.toc a {
  color: var(--text-dim);
  text-decoration: none;
  font-size: 0.82em;
  padding: 6px 14px;
  border-radius: 6px;
  white-space: nowrap;
  transition: all 0.2s;
}
.toc a:hover {
  color: var(--text);
  background: var(--surface);
}

/* ---- Container ---- */
.container {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 24px;
}

/* ---- Sections ---- */
section {
  padding: 48px 0;
  border-bottom: 1px solid var(--border);
  animation: fadeSlideIn 0.5s ease-out both;
}
section:last-child { border-bottom: none; }

h2 {
  font-size: 1.6em;
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--text);
}
h2 .num {
  color: var(--accent);
  font-weight: 400;
  margin-right: 8px;
}
.section-desc {
  color: var(--text-dim);
  margin-bottom: 28px;
  font-size: 0.95em;
}

h3 {
  font-size: 1.15em;
  font-weight: 600;
  margin: 28px 0 12px;
  color: var(--accent-light);
}

h4 {
  font-size: 1em;
  font-weight: 600;
  margin: 20px 0 8px;
  color: var(--orange);
}

p { margin-bottom: 14px; }
ul, ol { margin: 0 0 14px 24px; }
li { margin-bottom: 4px; }

/* ---- Cards ---- */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 16px;
}

/* ---- Stat Cards ---- */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
  margin: 24px 0;
}
.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px 20px;
  text-align: center;
  animation: fadeSlideIn 0.4s ease-out both;
  transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.stat-card .icon {
  width: 44px; height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3em;
  margin: 0 auto 14px;
}
.stat-card .value {
  font-size: 2rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 4px;
}
.stat-card .label {
  color: var(--text-dim);
  font-size: 0.85em;
}

/* ---- Bar charts ---- */
.bar-chart {
  margin: 16px 0;
}
.bar-row {
  display: flex;
  align-items: center;
  margin-bottom: 6px;
  font-size: 0.85em;
}
.bar-label {
  width: 80px;
  flex-shrink: 0;
  color: var(--text-dim);
  text-align: right;
  padding-right: 12px;
  font-size: 0.82em;
}
.bar-track {
  flex: 1;
  height: 22px;
  background: rgba(255,255,255,0.03);
  border-radius: 6px;
  overflow: hidden;
  position: relative;
}
.bar-fill {
  height: 100%;
  border-radius: 6px;
  transition: width 0.6s ease;
  position: relative;
}
.bar-fill::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.08) 100%);
  border-radius: 6px;
}
.bar-value {
  width: 50px;
  flex-shrink: 0;
  text-align: right;
  color: var(--text-dim);
  font-size: 0.82em;
  padding-left: 8px;
}

/* ---- Split bar (friction) ---- */
.split-bar-container {
  margin: 16px 0;
}
.split-bar {
  height: 32px;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  margin-bottom: 8px;
}
.split-bar .segment {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8em;
  font-weight: 600;
  color: rgba(255,255,255,0.9);
  transition: width 0.6s ease;
}
.split-bar-legend {
  display: flex;
  gap: 24px;
  font-size: 0.85em;
}
.split-bar-legend .dot {
  display: inline-block;
  width: 8px; height: 8px;
  border-radius: 50%;
  margin-right: 6px;
}

/* ---- Tags / badges ---- */
.tag {
  display: inline-block;
  font-size: 0.78em;
  padding: 3px 10px;
  border-radius: 4px;
  font-weight: 500;
  margin: 2px 2px;
}
.tag-purple { background: rgba(124,106,239,0.18); color: var(--accent-light); }
.tag-green  { background: rgba(52,211,153,0.18); color: var(--green); }
.tag-orange { background: rgba(251,146,60,0.18); color: var(--orange); }
.tag-blue   { background: rgba(96,165,250,0.18); color: var(--blue); }
.tag-red    { background: rgba(248,113,113,0.18); color: var(--red); }
.tag-cyan   { background: rgba(34,211,238,0.18); color: var(--cyan); }
.tag-pink   { background: rgba(244,114,182,0.18); color: var(--pink); }
.tag-yellow { background: rgba(251,191,36,0.18); color: var(--yellow); }

/* ---- Outcome pills ---- */
.pill-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 12px 0;
}
.pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.85em;
  font-weight: 500;
  border: 1px solid;
}

/* ---- Tables ---- */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 14px 0 20px;
  font-size: 0.9em;
}
th {
  text-align: left;
  padding: 10px 14px;
  background: var(--surface2);
  color: var(--text-dim);
  font-weight: 600;
  font-size: 0.85em;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-bottom: 1px solid var(--border);
}
td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
}
tr:last-child td { border-bottom: none; }
tr:hover td { background: rgba(124, 106, 239, 0.04); }

/* ---- Code ---- */
pre {
  background: var(--code-bg);
  border: 1px solid var(--code-border);
  border-radius: 8px;
  padding: 18px 20px;
  overflow-x: auto;
  margin: 12px 0 18px;
  font-size: 0.88em;
  line-height: 1.65;
}
code {
  font-family: 'SF Mono', 'Fira Code', 'JetBrains Mono', Consolas, monospace;
  font-size: 0.92em;
}
pre code { font-size: 1em; }
:not(pre) > code {
  background: var(--surface2);
  padding: 2px 7px;
  border-radius: 4px;
  color: var(--cyan);
}

/* ---- Two-column layout ---- */
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin: 16px 0;
}

/* ---- Glance card ---- */
.glance-card {
  background: linear-gradient(135deg, rgba(124,106,239,0.08), rgba(34,211,238,0.06));
  border: 1px solid rgba(124,106,239,0.2);
  border-radius: 14px;
  padding: 28px 32px;
  margin: 24px 0;
  font-size: 1.05em;
  line-height: 1.8;
  animation: glowPulse 4s ease-in-out infinite;
}

/* ---- Footer ---- */
footer {
  text-align: center;
  padding: 40px 24px;
  color: var(--text-dim);
  font-size: 0.82em;
  border-top: 1px solid var(--border);
}

/* ---- Scroll to top ---- */
.scroll-top {
  position: fixed;
  bottom: 28px;
  right: 28px;
  width: 42px; height: 42px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  border: none;
  cursor: pointer;
  font-size: 1.3em;
  display: none;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(124,106,239,0.4);
  transition: opacity 0.3s, transform 0.3s;
  z-index: 200;
}
.scroll-top:hover { transform: scale(1.1); }
.scroll-top.visible { display: flex; }

/* ---- LLM prose content styling ---- */
.prose strong { color: var(--accent-light); }
.prose em { color: var(--text-dim); font-style: italic; }
.prose hr { border: none; border-top: 1px solid var(--border); margin: 24px 0; }

/* ---- Print ---- */
@media print {
  body { background: #fff; color: #222; }
  .toc, .scroll-top { display: none !important; }
  .hero { background: #f5f5f5; }
  .hero h1 { -webkit-text-fill-color: #333; }
  .stat-card, .card, .glance-card { box-shadow: none; border-color: #ddd; }
  section { break-inside: avoid; }
}

/* ---- Responsive ---- */
@media (max-width: 640px) {
  .hero h1 { font-size: 1.8em; }
  .two-col { grid-template-columns: 1fr; }
  .stat-grid { grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); }
}
"""

HTML_LABELS = {
    "zh": {
        "title": "Clawlens 使用洞察报告",
        "at_a_glance": "概览摘要",
        "stat_sessions": "会话",
        "stat_messages": "消息",
        "stat_tokens": "Token 消耗",
        "stat_cost": "总费用",
        "stat_days": "活跃天",
        "hour_dist": "活跃时段分布",
        "weekday_dist": "星期分布",
        "weekdays": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
        "usage_overview": "使用概览",
        "task_classification": "任务分类",
        "friction_analysis": "摩擦分析",
        "skills_ecosystem": "Skills 生态分析",
        "autonomous_audit": "自主行为审计",
        "channel_analysis": "多渠道分析",
        "friction_claw": "Claw 侧",
        "friction_user": "用户侧",
        "outcomes_title": "成果分布",
        "satisfaction_title": "满意度分布",
        "models_title": "模型使用",
        "channels_title": "渠道分布",
        "footer": "报告由 clawlens v{version} 生成于 {time}",
    },
    "en": {
        "title": "Clawlens Usage Insights Report",
        "at_a_glance": "At a Glance",
        "stat_sessions": "Sessions",
        "stat_messages": "Messages",
        "stat_tokens": "Tokens",
        "stat_cost": "Total Cost",
        "stat_days": "Active Days",
        "hour_dist": "Hourly Activity",
        "weekday_dist": "Weekday Activity",
        "weekdays": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "usage_overview": "Usage Overview",
        "task_classification": "Task Classification",
        "friction_analysis": "Friction Analysis",
        "skills_ecosystem": "Skills Ecosystem",
        "autonomous_audit": "Autonomous Behavior Audit",
        "channel_analysis": "Multi-Channel Analysis",
        "friction_claw": "Claw-side",
        "friction_user": "User-side",
        "outcomes_title": "Outcome Distribution",
        "satisfaction_title": "Satisfaction Distribution",
        "models_title": "Model Usage",
        "channels_title": "Channel Distribution",
        "footer": "Report generated by clawlens v{version} at {time}",
    },
}

# Color palette for bar charts (cycling)
_PALETTE = [
    "var(--accent)", "var(--cyan)", "var(--green)", "var(--orange)",
    "var(--blue)", "var(--pink)", "var(--yellow)", "var(--red)",
    "var(--accent-light)", "#8b5cf6", "#a78bfa",
]

OUTCOME_COLORS = {
    "fully_achieved": ("var(--green)", "rgba(52,211,153,0.18)"),
    "mostly_achieved": ("var(--blue)", "rgba(96,165,250,0.18)"),
    "partially_achieved": ("var(--orange)", "rgba(251,146,60,0.18)"),
    "not_achieved": ("var(--red)", "rgba(248,113,113,0.18)"),
    "unclear": ("var(--text-dim)", "rgba(139,143,163,0.18)"),
}

SATISFACTION_COLORS = {
    "happy": ("var(--green)", "rgba(52,211,153,0.18)"),
    "satisfied": ("var(--cyan)", "rgba(34,211,238,0.18)"),
    "likely_satisfied": ("var(--blue)", "rgba(96,165,250,0.18)"),
    "dissatisfied": ("var(--orange)", "rgba(251,146,60,0.18)"),
    "frustrated": ("var(--red)", "rgba(248,113,113,0.18)"),
    "unsure": ("var(--text-dim)", "rgba(139,143,163,0.18)"),
}


def _esc(text: str) -> str:
    """HTML-escape a string."""
    return html_mod.escape(str(text))


def _fmt_number(n: int | float) -> str:
    """Format a number with K/M suffixes for readability."""
    if isinstance(n, float):
        if n >= 1_000_000:
            return f"{n / 1_000_000:.1f}M"
        if n >= 1_000:
            return f"{n / 1_000:.1f}K"
        return f"{n:.2f}"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 10_000:
        return f"{n / 1_000:.1f}K"
    return f"{n:,}"


def _build_stat_cards(stats: AggregateStats, lang: str) -> str:
    """Build the key metrics stat card grid."""
    L = HTML_LABELS.get(lang, HTML_LABELS["en"])
    cards_data = [
        ("var(--accent)", L["stat_sessions"], _fmt_number(stats.total_sessions)),
        ("var(--cyan)", L["stat_messages"], _fmt_number(stats.total_messages)),
        ("var(--blue)", L["stat_tokens"], _fmt_number(stats.total_tokens)),
        ("var(--green)", L["stat_cost"], f"${stats.total_cost:.2f}"),
        ("var(--orange)", L["stat_days"], str(stats.days_active)),
    ]
    items = []
    for i, (color, label, value) in enumerate(cards_data):
        items.append(
            f'<div class="stat-card" style="animation-delay:{i * 0.08}s; border-left: 3px solid {color};">'
            f'<div class="value" style="color:{color};">{_esc(value)}</div>'
            f'<div class="label">{_esc(label)}</div>'
            f'</div>'
        )
    return f'<div class="stat-grid">{"".join(items)}</div>'


def _build_bar_chart(data: dict, labels: dict | None, title: str,
                     color_start: str = "var(--blue)", color_end: str = "var(--cyan)",
                     use_palette: bool = False) -> str:
    """Build a horizontal bar chart from a dict of {label: count}."""
    if not data:
        return ""
    sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)
    max_val = max(v for _, v in sorted_items) or 1
    rows = []
    for i, (key, count) in enumerate(sorted_items):
        pct = count / max_val * 100
        display_label = labels.get(key, key) if labels else str(key)
        if use_palette:
            color = _PALETTE[i % len(_PALETTE)]
            bg = f"background: {color};"
        else:
            bg = f"background: linear-gradient(90deg, {color_start}, {color_end});"
        rows.append(
            f'<div class="bar-row">'
            f'<div class="bar-label">{_esc(display_label)}</div>'
            f'<div class="bar-track">'
            f'<div class="bar-fill" style="width:{pct:.1f}%;{bg}"></div>'
            f'</div>'
            f'<div class="bar-value">{count}</div>'
            f'</div>'
        )
    return (
        f'<div class="card">'
        f'<h3>{_esc(title)}</h3>'
        f'<div class="bar-chart">{"".join(rows)}</div>'
        f'</div>'
    )


def _build_hour_chart(stats: AggregateStats, lang: str) -> str:
    """Build 24-hour activity distribution chart."""
    L = HTML_LABELS.get(lang, HTML_LABELS["en"])
    dist = stats.hour_distribution
    if not dist:
        return ""
    full_data = {f"{h:02d}:00": dist.get(h, 0) for h in range(24)}
    return _build_bar_chart(full_data, None, L["hour_dist"],
                            color_start="var(--blue)", color_end="var(--cyan)")


def _build_weekday_chart(stats: AggregateStats, lang: str) -> str:
    """Build weekday activity distribution chart."""
    L = HTML_LABELS.get(lang, HTML_LABELS["en"])
    dist = stats.weekday_distribution
    if not dist:
        return ""
    weekday_labels = L["weekdays"]
    full_data = {weekday_labels[d]: dist.get(d, 0) for d in range(7)}
    return _build_bar_chart(full_data, None, L["weekday_dist"],
                            color_start="var(--accent)", color_end="var(--pink)")


def _build_task_bars(stats: AggregateStats, lang: str) -> str:
    """Build task category breakdown bars."""
    L = HTML_LABELS.get(lang, HTML_LABELS["en"])
    cat_labels = CATEGORY_LABELS.get(lang, CATEGORY_LABELS["en"])
    return _build_bar_chart(stats.task_categories, cat_labels, L["task_classification"],
                            use_palette=True)


def _build_friction_split(stats: AggregateStats, lang: str) -> str:
    """Build the Claw vs User friction split bar."""
    L = HTML_LABELS.get(lang, HTML_LABELS["en"])
    attr = stats.friction_by_attribution
    claw = attr.get("claw", 0)
    user = attr.get("user", 0)
    total = claw + user
    if total == 0:
        return ""
    claw_pct = claw / total * 100
    user_pct = 100 - claw_pct
    return (
        f'<div class="split-bar-container">'
        f'<div class="split-bar">'
        f'<div class="segment" style="width:{claw_pct:.1f}%;background:var(--red);">'
        f'{claw} ({claw_pct:.0f}%)</div>'
        f'<div class="segment" style="width:{user_pct:.1f}%;background:var(--orange);">'
        f'{user} ({user_pct:.0f}%)</div>'
        f'</div>'
        f'<div class="split-bar-legend">'
        f'<span><span class="dot" style="background:var(--red);"></span>{_esc(L["friction_claw"])} ({claw})</span>'
        f'<span><span class="dot" style="background:var(--orange);"></span>{_esc(L["friction_user"])} ({user})</span>'
        f'</div>'
        f'</div>'
    )


def _build_pills(data: dict, color_map: dict, title: str, lang: str) -> str:
    """Build colored pill badges for outcome/satisfaction distributions."""
    if not data or all(v == 0 for v in data.values()):
        return ""
    labels_map = FRICTION_LABELS.get(lang, FRICTION_LABELS["en"])  # reuse for key->display
    pills = []
    for key, count in data.items():
        if count == 0:
            continue
        fg, bg = color_map.get(key, ("var(--text-dim)", "rgba(139,143,163,0.18)"))
        display = labels_map.get(key, key.replace("_", " ").title())
        pills.append(
            f'<span class="pill" style="color:{fg};background:{bg};border-color:{fg};">'
            f'{_esc(display)} <strong>{count}</strong></span>'
        )
    return (
        f'<div style="margin:16px 0;">'
        f'<h3>{_esc(title)}</h3>'
        f'<div class="pill-row">{"".join(pills)}</div>'
        f'</div>'
    )


def _build_model_tags(stats: AggregateStats, lang: str) -> str:
    """Build model usage tag badges."""
    L = HTML_LABELS.get(lang, HTML_LABELS["en"])
    if not stats.models_used:
        return ""
    tag_colors = ["tag-purple", "tag-cyan", "tag-blue", "tag-green", "tag-orange", "tag-pink"]
    tags = []
    for i, (model_name, count) in enumerate(sorted(stats.models_used.items(), key=lambda x: x[1], reverse=True)):
        cls = tag_colors[i % len(tag_colors)]
        tags.append(f'<span class="tag {cls}">{_esc(model_name)} ({count})</span>')
    return (
        f'<div style="margin:16px 0;">'
        f'<h3>{_esc(L["models_title"])}</h3>'
        f'<div style="margin-top:8px;">{"".join(tags)}</div>'
        f'</div>'
    )


def _build_channel_bars(stats: AggregateStats, lang: str) -> str:
    """Build channel distribution bars."""
    L = HTML_LABELS.get(lang, HTML_LABELS["en"])
    return _build_bar_chart(stats.channel_distribution, None, L["channels_title"],
                            use_palette=True)


def _md_to_html(md_text: str) -> str:
    """Convert a Markdown string to HTML. Falls back to <pre> if markdown lib unavailable."""
    try:
        import markdown
        md = markdown.Markdown(extensions=["tables", "fenced_code"])
        result = md.convert(md_text)
        md.reset()
        return result
    except ImportError:
        # Fallback: wrap in <pre> with basic escaping
        return f"<pre>{_esc(md_text)}</pre>"


async def generate_html_report(
    stats: AggregateStats,
    sections: list[str],
    model: str,
    lang: str,
    concurrency: int,
) -> str:
    """Stage 4: Generate the final HTML report."""
    log("Stage 4: Generating HTML report")

    # Reuse the same LLM section generation
    dimension_outputs, at_a_glance = await _generate_report_sections(
        stats, sections, model, lang, concurrency,
    )

    L = HTML_LABELS.get(lang, HTML_LABELS["en"])
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    date_start, date_end = stats.date_range
    lang_attr = "zh-CN" if lang == "zh" else "en"

    section_keys_to_labels = {
        "usage_overview": L["usage_overview"],
        "task_classification": L["task_classification"],
        "friction_analysis": L["friction_analysis"],
        "skills_ecosystem": L["skills_ecosystem"],
        "autonomous_audit": L["autonomous_audit"],
        "channel_analysis": L["channel_analysis"],
    }

    section_ids = {
        "usage_overview": "overview",
        "task_classification": "tasks",
        "friction_analysis": "friction",
        "skills_ecosystem": "skills",
        "autonomous_audit": "autonomous",
        "channel_analysis": "channels",
    }

    # Build nav links
    nav_links = [f'<a href="#glance">{_esc(L["at_a_glance"])}</a>']
    for dim in sections:
        sid = section_ids.get(dim, dim)
        label = section_keys_to_labels.get(dim, dim)
        nav_links.append(f'<a href="#{sid}">{_esc(label)}</a>')

    # Build data visuals
    stat_cards = _build_stat_cards(stats, lang)
    hour_chart = _build_hour_chart(stats, lang)
    weekday_chart = _build_weekday_chart(stats, lang)
    task_bars = _build_task_bars(stats, lang)
    friction_split = _build_friction_split(stats, lang)
    outcome_pills = _build_pills(stats.outcomes, OUTCOME_COLORS, L["outcomes_title"], lang)
    satisfaction_pills = _build_pills(stats.satisfaction, SATISFACTION_COLORS, L["satisfaction_title"], lang)
    model_tags = _build_model_tags(stats, lang)
    channel_bars = _build_channel_bars(stats, lang)

    # Build section HTML
    sections_html = []
    for i, dim in enumerate(sections, 1):
        sid = section_ids.get(dim, dim)
        heading = section_keys_to_labels.get(dim, dim)
        md_content = dimension_outputs.get(dim, "")
        content_html = _md_to_html(md_content)

        # Insert data visuals before LLM prose for relevant sections
        visuals = ""
        if dim == "usage_overview":
            time_charts = ""
            if hour_chart or weekday_chart:
                if hour_chart and weekday_chart:
                    time_charts = f'<div class="two-col">{hour_chart}{weekday_chart}</div>'
                else:
                    time_charts = hour_chart or weekday_chart
            visuals = stat_cards + model_tags + time_charts
        elif dim == "task_classification":
            visuals = task_bars
        elif dim == "friction_analysis":
            visuals = friction_split
        elif dim == "channel_analysis":
            visuals = channel_bars

        sections_html.append(
            f'<section id="{sid}" style="animation-delay:{(i * 0.1):.1f}s;">'
            f'<h2><span class="num">0{i}</span>{_esc(heading)}</h2>'
            f'{visuals}'
            f'<div class="prose">{content_html}</div>'
            f'</section>'
        )

    # Glance section
    glance_html = ""
    if at_a_glance:
        glance_content = _md_to_html(at_a_glance)
        glance_html = (
            f'<section id="glance">'
            f'<h2>{_esc(L["at_a_glance"])}</h2>'
            f'<div class="glance-card">{glance_content}</div>'
            f'{outcome_pills}{satisfaction_pills}'
            f'</section>'
        )

    # Meta pills for hero
    if lang == "zh":
        meta_items = [
            f'{date_start} ~ {date_end}',
            f'<strong>{stats.total_sessions}</strong> 会话',
            f'<strong>{stats.total_messages}</strong> 消息',
            f'<strong>{stats.days_active}</strong> 活跃天',
        ]
    else:
        meta_items = [
            f'{date_start} ~ {date_end}',
            f'<strong>{stats.total_sessions}</strong> sessions',
            f'<strong>{stats.total_messages}</strong> messages',
            f'<strong>{stats.days_active}</strong> active days',
        ]
    meta_spans = "".join(f"<span>{m}</span>" for m in meta_items)

    footer_text = L["footer"].format(version=VERSION, time=now_str)

    # Assemble full HTML
    html = f"""<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_esc(L["title"])}</title>
<style>
{HTML_CSS}
</style>
</head>
<body>

<div class="hero">
  <div class="grid-bg"></div>
  <h1>{_esc(L["title"])}</h1>
  <div class="meta">{meta_spans}</div>
</div>

<nav class="toc">
  <div class="toc-inner">
    {"".join(nav_links)}
  </div>
</nav>

<div class="container">
  {glance_html}
  {"".join(sections_html)}
</div>

<footer>{_esc(footer_text)}</footer>

<button class="scroll-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" title="Back to top">&uarr;</button>

<script>
(function() {{
  var btn = document.querySelector('.scroll-top');
  window.addEventListener('scroll', function() {{
    btn.classList.toggle('visible', window.scrollY > 400);
  }});
  document.querySelectorAll('.toc a').forEach(function(a) {{
    a.addEventListener('click', function(e) {{
      e.preventDefault();
      var target = document.querySelector(this.getAttribute('href'));
      if (target) target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }});
  }});
}})();
</script>

</body>
</html>"""

    log("Stage 4 complete: HTML report assembled")
    return html


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

async def async_main(args: argparse.Namespace) -> None:
    global _verbose, _model_api_base, _model_api_key
    _verbose = args.verbose

    sections = ALL_SECTIONS

    if args.model:
        model = args.model
    else:
        try:
            model, _model_api_base, _model_api_key = resolve_openclaw_model(args.agent_id)
        except RuntimeError as e:
            print(f"Error: could not auto-detect model from OpenClaw config: {e}", file=sys.stderr)
            print("Please specify --model explicitly.", file=sys.stderr)
            sys.exit(1)

    log(f"Clawlens v{VERSION}")
    log(f"Agent: {args.agent_id}, Days: {args.days}")
    log(f"Model: {model}, Lang: {args.lang}")

    # Stage 1
    log("--- Stage 1: Data Collection ---")
    sessions = collect_sessions(args.agent_id, args.days, args.max_sessions)
    if not sessions:
        if args.lang == "zh":
            msg = f"# Clawlens 使用洞察报告\n\n> 未找到足够的对话数据。请确认 agent ID (`{args.agent_id}`) 正确且存在对话记录。\n"
        else:
            msg = f"# Clawlens Usage Insights Report\n\n> No sufficient conversation data found. Please verify agent ID (`{args.agent_id}`) is correct and sessions exist.\n"
        if args.output:
            Path(args.output).write_text(msg, encoding="utf-8")
        else:
            print(msg)
        return

    # Stage 2
    log("--- Stage 2: LLM Facet Extraction ---")
    facets = await extract_facets(
        sessions, args.agent_id, model,
        args.concurrency, args.no_cache,
    )

    # Stage 3
    log("--- Stage 3: Aggregation ---")
    stats = aggregate(sessions, facets)

    # Stage 4
    log("--- Stage 4: Report Generation ---")
    fmt = getattr(args, "format", "md")
    if fmt == "html":
        report = await generate_html_report(stats, sections, model, args.lang, args.concurrency)
    else:
        report = await generate_report(stats, sections, model, args.lang, args.concurrency)

    # Output
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        log(f"Report written to {args.output}")
    else:
        print(report)

    log("Done!")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clawlens: OpenClaw Usage Insights Report Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 clawlens.py --verbose                          # auto-detect model from OpenClaw config
  python3 clawlens.py --lang en --days 7                 # auto-detect, English, last 7 days
  DEEPSEEK_API_KEY=sk-xxx python3 clawlens.py --model deepseek/deepseek-chat
  OPENAI_API_KEY=sk-xxx python3 clawlens.py --model openai/gpt-4o --lang en --days 7
  ANTHROPIC_API_KEY=sk-xxx python3 clawlens.py --model anthropic/claude-sonnet-4-20250514 --verbose -o report.md
  DEEPSEEK_API_KEY=sk-xxx python3 clawlens.py --model deepseek/deepseek-chat --format html -o report.html
""",
    )
    parser.add_argument("--agent-id", default="main", help="Agent ID (default: main)")
    parser.add_argument("--days", type=int, default=180, help="Analysis window in days (default: 180)")
    parser.add_argument(
        "--model", default=None,
        help="LLM model in litellm format (e.g. deepseek/deepseek-chat). "
             "If omitted, auto-detected from OpenClaw config (~/.openclaw/openclaw.json).",
    )
    parser.add_argument("--lang", default="zh", choices=["zh", "en"], help="Report language (default: zh)")
    parser.add_argument("--format", default="md", choices=["md", "html"], help="Output format: md or html (default: md)")
    parser.add_argument("--no-cache", action="store_true", help="Ignore cached facet results")
    parser.add_argument("--max-sessions", type=int, default=2000, help="Max sessions to process (default: 2000)")
    parser.add_argument("--concurrency", type=int, default=10, help="Max parallel LLM calls (default: 10)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print progress to stderr")
    parser.add_argument("-o", "--output", help="Output file path (default: stdout)")

    args = parser.parse_args()
    asyncio.run(async_main(args))


if __name__ == "__main__":
    main()
