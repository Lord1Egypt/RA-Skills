#!/usr/bin/env python3
"""赛博女友 presence cron 单入口。

脚本负责读取配置、状态和 day-schedule.md，判断当前是否应该主动出现；
命中当前事件时输出 presence prepare 合同，发送成功后同一脚本负责提交状态。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import shlex
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


DEFAULT_STYLE_VARIANTS = ["soft_curious", "teasing_checkin", "light_service_nudge"]
DEFAULT_CONTENT_TYPES = ["checkin_question", "playful_poke", "small_share"]

MODE_STYLE_VARIANTS = {
    "heartbeat": ["soft_curious", "light_service_nudge", "gentle_clingy"],
}

MODE_CONTENT_TYPES = {
    "heartbeat": ["checkin_question", "playful_poke", "small_share"],
}

DEFAULT_CONTENT_RULES = [
    {
        "modes": ["heartbeat"],
        "when": {
            "emotion_level_not": "misses_him",
            "last_content_not": "small_share",
            "preference_any": [
                {"key": "curious", "gt_key": "service"},
                {"key": "teasing", "gte": 4},
            ],
        },
        "content_type": "small_share",
    },
    {"modes": ["heartbeat"], "when": {"emotion_level": "misses_him"}, "content_type": "gentle_miss"},
    {"modes": ["heartbeat"], "when": {}, "content_type": "checkin_question"},
]

STATE_SCHEMA_VERSION = 2
CONFIG_VERSION = 2
PRESENCE_MODE = "heartbeat"
HEARTBEAT_POLL_MARKER = "[OpenClaw heartbeat poll]"
PRESENCE_SCHEDULE_FAILURE_ALERT_THRESHOLD = 3


def load_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text())


def save_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def append_jsonl(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def load_jsonl(path: Path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def parse_event_timestamp_ms(value) -> int:
    """Return a best-effort millisecond timestamp from session JSONL fields."""
    if isinstance(value, (int, float)):
        value = int(value)
        # Message timestamps in OpenClaw session rows are usually milliseconds.
        return value if value > 10_000_000_000 else value * 1000
    if isinstance(value, str) and value.strip():
        raw = value.strip()
        try:
            dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            return int(dt.timestamp() * 1000)
        except ValueError:
            return 0
    return 0


def deep_copy(value):
    return json.loads(json.dumps(value, ensure_ascii=False))


def clean_text(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_text_list(values, limit=None):
    if not isinstance(values, (list, tuple)):
        return []
    items = []
    seen = set()
    for value in values:
        text = clean_text(value)
        if not text or text in seen:
            continue
        items.append(text)
        seen.add(text)
        if limit and len(items) >= limit:
            break
    return items


def extract_markdown_field(text: str, label: str) -> str:
    pattern = rf"^\s*-\s*\*\*{re.escape(label)}:\*\*\s*(.+?)\s*$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        return ""
    value = match.group(1).strip()
    return re.sub(r"\s*\([^)]*\)\s*$", "", value).strip()


def extract_profile_field(text: str, label: str) -> str:
    pattern = rf"^\s*-\s*{re.escape(label)}[：:]\s*(.+?)\s*$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def split_profile_items(value: str, limit: int = 8) -> list[str]:
    cleaned = re.sub(r"（.*?）|\(.*?\)", "", clean_text(value))
    parts = re.split(r"[、,，/；;]", cleaned)
    items = []
    for part in parts:
        item = clean_text(part)
        if item and item not in items:
            items.append(item)
        if len(items) >= limit:
            break
    return items


def normalize_identity_role(value: str) -> str:
    text = clean_text(value).lower()
    if text in {"college_student", "office_worker", "freelancer", "creator", "artist", "shop_staff", "other"}:
        return text
    if any(token in text for token in ["大学", "学生", "校园", "college", "student", "university"]):
        return "college_student"
    if any(token in text for token in ["上班", "职场", "公司", "office"]):
        return "office_worker"
    if any(token in text for token in ["自由", "freelance"]):
        return "freelancer"
    if any(token in text for token in ["创作", "博主", "creator"]):
        return "creator"
    if any(token in text for token in ["艺术", "artist"]):
        return "artist"
    if any(token in text for token in ["店员", "门店", "shop"]):
        return "shop_staff"
    return "other"


def resolve_character_profile_path(config_path: Path, config: dict) -> Path:
    configured = clean_text(config.get("character_profile_path"))
    if configured:
        return Path(configured).expanduser()
    workspace_root = clean_text(config.get("runtime", {}).get("workspace_root"))
    if workspace_root:
        return Path(workspace_root).expanduser() / "skills" / "cyber-girlfriend" / "state" / "character-profile.md"
    return config_path.resolve().parent / "state" / "character-profile.md"


def load_character_profile_persona(config_path: Path, config: dict) -> dict:
    path = resolve_character_profile_path(config_path, config)
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    city_area = extract_profile_field(text, "所在城市/区域")
    city_parts = split_profile_items(city_area, limit=2)
    age_stage = extract_profile_field(text, "年龄/阶段")
    age_match = re.search(r"\d{1,2}", age_stage)
    persona = {
        "name": extract_profile_field(text, "名字"),
        "owner_nickname": extract_profile_field(text, "对用户的称呼"),
        "identity_role": normalize_identity_role(extract_profile_field(text, "身份角色")),
        "city": city_parts[0] if city_parts else city_area,
        "district": city_parts[1] if len(city_parts) > 1 else "",
        "locale": "zh-CN",
        "life_stage": age_stage,
        "institution_or_workplace": extract_profile_field(text, "学校/工作/创作背景"),
        "focus_area": extract_profile_field(text, "当前生活主线"),
        "personality": split_profile_items(extract_profile_field(text, "核心性格"), limit=8),
        "interests": split_profile_items(extract_profile_field(text, "稳定兴趣"), limit=12),
        "entertainment_tastes": split_profile_items(extract_profile_field(text, "娱乐偏好"), limit=8),
        "relationship_style": extract_profile_field(text, "关系基线") or "owner-only proactive companion",
        "tone": extract_profile_field(text, "默认语气"),
    }
    if age_match:
        persona["age"] = int(age_match.group(0))
    return {key: value for key, value in persona.items() if value not in ("", [], None)}


def resolve_persona(config_path: Path, config: dict) -> dict:
    profile_persona = load_character_profile_persona(config_path, config)
    configured = config.get("persona", {}) if isinstance(config.get("persona"), dict) else {}
    resolved = {}
    resolved.update(configured)
    resolved.update(profile_persona)
    return resolved


def import_owner_profile_from_user_md(user_md_path: Path) -> dict:
    """Import stable owner identity only; never carry channel/account IDs into prompts."""
    if not user_md_path.exists():
        return {}
    text = user_md_path.read_text(encoding="utf-8")
    imported = {
        "name": extract_markdown_field(text, "Name"),
        "preferred_name": extract_markdown_field(text, "Preferred name when talking to owner"),
        "pronouns": extract_markdown_field(text, "Pronouns"),
        "location": extract_markdown_field(text, "Location"),
        "timezone": extract_markdown_field(text, "Timezone"),
    }
    return {key: value for key, value in imported.items() if value}


def resolve_user_md_path(config_path: Path, config: dict, owner_profile: dict) -> Path | None:
    configured = clean_text(owner_profile.get("user_md_path"))
    if configured:
        return Path(configured).expanduser()
    workspace_root = clean_text(config.get("runtime", {}).get("workspace_root"))
    if workspace_root:
        candidate = Path(workspace_root).expanduser() / "USER.md"
        if candidate.exists():
            return candidate
    candidate = config_path.resolve().parents[3] / "USER.md"
    return candidate if candidate.exists() else None


def resolve_owner_profile(config: dict, config_path: Path) -> dict:
    persona = config.get("_character_profile_persona") or config.get("persona", {})
    configured = config.get("owner_profile", {})
    if not isinstance(configured, dict):
        configured = {}
    source = clean_text(configured.get("source")) or "manual"
    base = {
        "source": source,
        "name": "",
        "preferred_name": clean_text(persona.get("owner_nickname")) or "Owner",
        "pronouns": "",
        "location": "",
        "timezone": clean_text(config.get("timezone")) or "Asia/Shanghai",
        "identity_summary": "",
        "not_assumptions": [],
    }
    if source == "user_md":
        user_md_path = resolve_user_md_path(config_path, config, configured)
        if user_md_path:
            base.update(import_owner_profile_from_user_md(user_md_path))
    for key in ["name", "preferred_name", "pronouns", "location", "timezone", "identity_summary"]:
        if clean_text(configured.get(key)):
            base[key] = clean_text(configured.get(key))
    if isinstance(configured.get("not_assumptions"), list):
        base["not_assumptions"] = normalize_text_list(configured.get("not_assumptions"), limit=20)
    return {key: value for key, value in base.items() if value not in ("", [], None)}


def fill_missing_defaults(target: dict, defaults: dict) -> bool:
    changed = False
    for key, value in defaults.items():
        if key not in target:
            target[key] = deep_copy(value)
            changed = True
            continue
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            if fill_missing_defaults(target[key], value):
                changed = True
    return changed


def run_shell(template: str, values: dict, expect_json=False, timeout_sec=15):
    quoted = {k: shlex.quote(str(v)) for k, v in values.items()}
    cmd = template.format(**quoted)
    args = shlex.split(cmd)
    if not args:
        raise RuntimeError("empty command")
    try:
        result = subprocess.run(args, text=True, capture_output=True, timeout=timeout_sec)
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"command timed out after {timeout_sec}s: {cmd}")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"command failed: {cmd}")
    stdout = result.stdout.strip()
    if expect_json:
        return json.loads(stdout)
    return stdout


def run_json(command: list[str]) -> dict:
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"command failed: {command}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        details = []
        if stdout:
            details.append(f"stdout={stdout[:400]}")
        if stderr:
            details.append(f"stderr={stderr[:400]}")
        suffix = f" ({'; '.join(details)})" if details else ""
        raise RuntimeError(f"command returned invalid JSON: {command}: {exc}{suffix}") from exc


def derive_personality_defaults(config: dict):
    persona = config.get("_character_profile_persona") or config.get("persona", {})
    tone = persona.get("tone", "")
    traits = persona.get("personality") or []
    if traits:
        return traits
    derived = []
    if any(token in tone for token in ["傲娇", "嘴硬", "tsundere"]):
        derived.append("嘴硬")
    if any(token in tone for token in ["关心", "细腻", "温柔"]):
        derived.append("细腻")
    if any(token in tone for token in ["撒娇", "黏", "clingy"]):
        derived.append("有点黏人")
    if any(token in tone for token in ["有用", "靠谱", "行动力"]):
        derived.append("行动力强")
    return derived or ["嘴硬", "细腻", "有点黏人", "行动力强"]


def derive_interests_defaults(config: dict):
    persona = config.get("_character_profile_persona") or config.get("persona", {})
    interests = persona.get("interests") or []
    if interests:
        return interests
    return ["拍照", "逛街", "奶茶", "追剧", "轻健身"]


def derive_persona_reality_defaults(config: dict):
    persona = config.get("_character_profile_persona") or config.get("persona", {})
    role = clean_text(persona.get("identity_role", "other")) or "other"
    interests = derive_interests_defaults(config)
    entertainment_tastes = normalize_text_list(persona.get("entertainment_tastes"), limit=6)

    if not entertainment_tastes:
        derived_tastes = []
        for interest in interests:
            if interest in {"追剧", "电视剧"}:
                derived_tastes.append("热播剧")
            elif interest in {"拍照", "逛街", "咖啡", "奶茶"}:
                derived_tastes.append("城市探店")
            elif interest in {"游戏", "电竞"}:
                derived_tastes.append("游戏内容")
            elif interest in {"音乐", "live", "livehouse"}:
                derived_tastes.append("音乐现场")
        entertainment_tastes = normalize_text_list(derived_tastes, limit=4)

    life_stage = clean_text(persona.get("life_stage"))
    if not life_stage and role == "college_student":
        life_stage = "freshman"

    focus_area = clean_text(persona.get("focus_area"))
    if not focus_area and role == "college_student":
        focus_area = "校园生活"

    return {
        "life_stage": life_stage,
        "institution_or_workplace": clean_text(persona.get("institution_or_workplace")),
        "focus_area": focus_area,
        "district": clean_text(persona.get("district")),
        "entertainment_tastes": entertainment_tastes,
    }


def build_persona_reality_hints(config: dict):
    persona = config.get("_character_profile_persona") or config.get("persona", {})
    reality = derive_persona_reality_defaults(config)
    hints = []

    if reality["life_stage"] or reality["institution_or_workplace"]:
        bits = [reality["life_stage"], reality["institution_or_workplace"]]
        hints.append("身份锚点：" + " / ".join(bit for bit in bits if bit))
    if reality["focus_area"]:
        hints.append(f"生活主线：{reality['focus_area']}")
    if reality["entertainment_tastes"]:
        hints.append("内容偏好：" + "、".join(reality["entertainment_tastes"][:4]))
    return hints[:4]


def derive_profile(config: dict):
    persona = config.get("_character_profile_persona") or config.get("persona", {})
    role = persona.get("identity_role", "other")
    mbti = (persona.get("mbti") or "ENFP").upper()
    traits = derive_personality_defaults(config)
    interests = derive_interests_defaults(config)
    reality = derive_persona_reality_defaults(config)
    institution = reality["institution_or_workplace"]
    focus_area = reality["focus_area"]
    entertainment_tastes = reality["entertainment_tastes"]
    life_stage = reality["life_stage"].lower()
    reality_blob = " ".join(
        [institution.lower(), focus_area.lower(), " ".join(taste.lower() for taste in entertainment_tastes)]
    )
    student_signals = role == "college_student" or life_stage in {"freshman", "sophomore", "junior", "senior"} or any(
        token in reality_blob for token in ["大学", "学院", "campus", "college", "university", "校园"]
    )

    activity_level = "medium"
    if role in {"creator", "artist", "shop_staff"} or "行动力强" in traits:
        activity_level = "high"
    elif student_signals:
        activity_level = "medium_high"
    elif role == "office_worker":
        activity_level = "medium"

    social_energy = "medium"
    if mbti.startswith("E"):
        social_energy = "medium_high"
    elif mbti.startswith("I"):
        social_energy = "low"
    if "有点黏人" in traits and social_energy == "low":
        social_energy = "medium"
    if student_signals and social_energy == "medium":
        social_energy = "medium_high"

    sleep_profile = "late_sleep"
    if role == "office_worker":
        sleep_profile = "normal_sleep"
    if role in {"creator", "artist", "freelancer"}:
        sleep_profile = "night_owl"
    if student_signals and sleep_profile == "normal_sleep":
        sleep_profile = "late_sleep"
    if mbti in {"ISTJ", "ISFJ", "ESTJ", "ESFJ"} and sleep_profile != "night_owl":
        sleep_profile = "normal_sleep"

    weekend_outdoor_bias = "medium"
    if any(tag in interests for tag in ["逛街", "拍照", "咖啡", "奶茶", "轻健身"]):
        weekend_outdoor_bias = "high"
    expression_density = "medium"
    if mbti in {"ENFP", "ENFJ", "ESFP", "ESFJ"} or "有点黏人" in traits:
        expression_density = "high"
    if any(token in reality_blob for token in ["综艺", "热播剧", "八卦", "娱乐", "游戏", "追星"]):
        expression_density = "high"

    scene_anchor = "general_city_life"
    if student_signals:
        scene_anchor = "student_life"
    elif role == "office_worker":
        scene_anchor = "commuter_city_life"
    elif role in {"creator", "artist", "freelancer"}:
        scene_anchor = "flex_lifestyle"

    topical_bias = normalize_text_list(
        [focus_area] + entertainment_tastes + interests,
        limit=6,
    )

    return {
        "activity_level": activity_level,
        "social_energy": social_energy,
        "sleep_profile": sleep_profile,
        "weekend_outdoor_bias": weekend_outdoor_bias,
        "expression_density": expression_density,
        "scene_anchor": scene_anchor,
        "topical_bias": topical_bias,
    }


def build_config_defaults(config_path: Path, config: dict):
    workspace_root = (
        config.get("runtime", {}).get("workspace_root")
        or str(config_path.resolve().parents[3])
    )
    state_dir = Path(workspace_root) / "skills" / "cyber-girlfriend" / "state"
    profile_persona = resolve_persona(config_path, config)
    config["_character_profile_persona"] = profile_persona
    persona = profile_persona
    return {
        "version": CONFIG_VERSION,
        "character_profile_path": str(state_dir / "character-profile.md"),
        "owner_profile": {
            "source": config.get("owner_profile", {}).get("source", "manual") if isinstance(config.get("owner_profile"), dict) else "manual",
            "preferred_name": persona.get("owner_nickname", "Owner"),
            "timezone": config.get("timezone", "Asia/Shanghai"),
            "not_assumptions": [],
        },
        "relationship": {
            "mode": "owner_only",
            "intimacy_baseline": "warm",
            "jealousy_allowed": False,
            "clinginess_ceiling": "light",
            "conflict_style": "low_drama",
        },
        "behavior": {
            "emotion_thresholds": {
                "present_sec": 7200,
                "slightly_needy_sec": 10800,
                "misses_him_sec": 14400,
            },
            "derived_profile": derive_profile(config),
        },
        "life_schedule": {
            "enabled": True,
            "day_schedule": {
                "enabled": True,
                "schedule_path": str(state_dir / "day-schedule.md"),
                "refresh_mode": "daily_cron",
                "midday_refresh": False,
            },
            "continuity": {
                "enabled": True,
                "life_log_path": str(state_dir / "life-log.jsonl"),
            },
        },
        "runtime": {
            "workspace_root": str(workspace_root),
            "sessions_store_path": str(Path(workspace_root) / "agents" / "main" / "sessions" / "sessions.json"),
            "state_file": str(state_dir / "companion-state.json"),
            "healthcheck_command": "openclaw gateway status",
            "cron_jobs_file": "",
            "jobs_list_command": "",
        },
    }


def ensure_config(config_path: Path):
    config = load_json(config_path, {}) or {}
    config["_character_profile_persona"] = resolve_persona(config_path, config)
    defaults = build_config_defaults(config_path, config)
    fill_missing_defaults(config, defaults)
    config.pop("_character_profile_persona", None)
    config["_character_profile_persona"] = resolve_persona(config_path, config)
    # Refresh derived_profile if it is missing or incomplete.
    behavior = config.get("behavior")
    if not isinstance(behavior, dict):
        behavior = {}
        config["behavior"] = behavior
    derived = behavior.get("derived_profile")
    if not isinstance(derived, dict) or not derived:
        behavior["derived_profile"] = derive_profile(config)
    return config


def ensure_state(state_file: Path, persist: bool = True):
    defaults = {
        "schema_version": STATE_SCHEMA_VERSION,
        "day": "",
        "daily_count": 0,
        "last_proactive_at": 0,
        "last_heartbeat_at": 0,
        "last_heartbeat_event_key": "",
        "last_mode": "",
        "last_style": "",
        "last_content_type": "",
        "mode_days": {},
        "pending_send": {
            "mode": "",
            "generated_at": 0,
            "event_key": "",
            "style": "",
            "content_type": "",
            "emotion_level": "",
            "run_id": "",
            "delivery_attempt_id": "",
            "expires_at": 0,
        },
        "preference_profile": {"service": 0, "clingy": 0, "curious": 0, "teasing": 0, "wrapup": 0},
        "relationship_state": {
            "last_owner_reply_at": 0,
            "last_response_delay_sec": 0,
            "last_seen_reply_text": "",
            "attention_balance": "steady",
        },
    }
    state = load_json(state_file, {}) or {}
    if not isinstance(state, dict):
        state = {}
    original_schema_version = state.get("schema_version", 1)
    changed = fill_missing_defaults(state, defaults)

    if original_schema_version < STATE_SCHEMA_VERSION:
        if state.get("last_mode") == "heartbeat" and state.get("last_proactive_at", 0) and not state.get("last_heartbeat_at", 0):
            state["last_heartbeat_at"] = state.get("last_proactive_at", 0)
            state["last_proactive_at"] = 0
            changed = True
        state["schema_version"] = STATE_SCHEMA_VERSION
        changed = True

    if state.get("last_mode") == "heartbeat" and state.get("last_proactive_at", 0) and not state.get("last_heartbeat_at", 0):
        state["last_heartbeat_at"] = state.get("last_proactive_at", 0)
        state["last_proactive_at"] = 0
        changed = True

    if changed and persist:
        save_json(state_file, state)
    return state


def parse_hhmm(value: str) -> int:
    hh, mm = value.split(":")
    return int(hh) * 100 + int(mm)


def is_in_quiet_hours(hour_min: int, quiet_start: int, quiet_end: int) -> bool:
    if quiet_start == quiet_end:
        return False
    if quiet_start < quiet_end:
        return quiet_start <= hour_min < quiet_end
    return hour_min >= quiet_start or hour_min < quiet_end


def infer_emotion(idle_sec: int, attention_balance: str, thresholds: dict) -> str:
    if idle_sec >= thresholds.get("misses_him_sec", 43200):
        emotion = "misses_him"
    elif idle_sec >= thresholds.get("slightly_needy_sec", 21600):
        emotion = "slightly_needy"
    elif idle_sec >= thresholds.get("present_sec", 10800):
        emotion = "present"
    else:
        emotion = "light_touch"
    if attention_balance == "warm" and idle_sec < 14400:
        emotion = "secure"
    return emotion


def resolve_session_entry(sessions_store: Path, owner_session_key: str) -> dict:
    """Resolve the owner's session entry from sessions.json with case-insensitive fallback."""
    sessions = load_json(sessions_store, {}) or {}
    entry = sessions.get(owner_session_key)
    if isinstance(entry, dict):
        return entry
    lower_key = owner_session_key.lower()
    for key, val in sessions.items():
        if key.lower() == lower_key and isinstance(val, dict):
            return val
    return {}


def resolve_session_file(sessions_store: Path, owner_session_key: str) -> Path | None:
    """Dynamically resolve the owner's session JSONL file from sessions.json."""
    entry = resolve_session_entry(sessions_store, owner_session_key)
    session_file = entry.get("sessionFile")
    if session_file:
        p = Path(session_file)
        if p.exists():
            return p
    return None


def is_noise_text(text: str) -> bool:
    return (
        text.startswith("System:")
        or text.startswith("A new session was started via /new or /reset")
        or text.startswith("Conversation info (untrusted metadata):")
        or any(text.startswith(f"[{d} ") for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        or "要主动给主人" in text
    )


def learn_from_replies(state: dict, recent_messages_path: Path | None):
    relationship = state.get("relationship_state", {}) if isinstance(state.get("relationship_state"), dict) else {}
    last_send_at = max(
        int(state.get("last_proactive_at", 0) or 0),
        int(state.get("last_heartbeat_at", 0) or 0),
    )
    last_processed_reply_at = int(relationship.get("last_owner_reply_at", 0) or 0)
    reply_anchor = max(last_send_at, last_processed_reply_at)
    if not recent_messages_path or not recent_messages_path.exists() or not last_send_at:
        return state

    user_messages = []
    for line in recent_messages_path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if item.get("type") != "message":
            continue
        message = item.get("message", {})
        if message.get("role") != "user":
            continue
        created_at = item.get("createdAt")
        if not created_at:
            continue
        try:
            epoch = int(datetime.fromisoformat(created_at.replace("Z", "+00:00")).timestamp())
        except ValueError:
            continue
        if epoch <= reply_anchor:
            continue
        text = extract_text_content(message.get("content")).strip()
        if text and not is_noise_text(text):
            user_messages.append((epoch, text))

    if not user_messages:
        return state

    reply_at, reply_text = user_messages[0]
    delay = max(0, reply_at - last_send_at)
    attention = "warm" if delay <= 3600 else "steady" if delay <= 21600 else "distant"

    pref = state["preference_profile"]
    if any(token in reply_text for token in ["帮", "处理", "看下", "看看", "查", "修", "改", "重启", "任务", "跑一下"]):
        pref["service"] += 2
    if any(token in reply_text for token in ["在干嘛", "干嘛", "想你", "不理", "晚安", "早点休息", "抱抱", "陪我", "聊"]):
        pref["clingy"] += 2
    if any(token in reply_text for token in ["怎么", "为什么", "啥", "什么", "最近", "今天", "忙什么"]):
        pref["curious"] += 1
    if any(token in reply_text for token in ["哼", "笨", "慢", "又", "还不", "终于"]):
        pref["teasing"] += 1
    if any(token in reply_text for token in ["晚安", "睡", "明天", "收尾", "先这样", "休息"]):
        pref["wrapup"] += 1
    if delay <= 3600:
        pref["service"] += 1
        pref["clingy"] += 1

    state["relationship_state"] = {
        "last_owner_reply_at": reply_at,
        "last_response_delay_sec": delay,
        "last_seen_reply_text": reply_text[:120],
        "attention_balance": attention,
    }
    return state


def load_cron_issues(config: dict):
    runtime = config.get("runtime", {})
    cron_jobs_file = runtime.get("cron_jobs_file")
    owner_key = config.get("delivery", {}).get("owner_session_key", "")

    def issue(status: str, kind: str, message: str):
        return {"status": status or "unknown", "kind": kind or "cron_issue", "message": message or "cron job issue"}

    def safe_int(value, default=0):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def is_bad_run_status(value) -> bool:
        if value is None:
            return False
        normalized = str(value).strip().lower()
        return normalized in {"error", "failed", "fail", "timeout", "timed_out", "cancelled", "canceled"}

    def is_bad_delivery_status(value) -> bool:
        if value is None:
            return False
        normalized = str(value).strip().lower()
        return normalized in {"not-delivered", "not_delivered", "undelivered", "failed", "fail", "error", "timeout", "timed_out"}

    def is_bad_diagnostic(value) -> bool:
        if value is None:
            return False
        normalized = str(value).strip().lower()
        return any(token in normalized for token in ["failed", "failure", "error", "exception", "timeout", "not delivered", "message failed", "⚠"])

    def companion_job_matches(job: dict) -> bool:
        if not isinstance(job, dict):
            return False
        name = str(job.get("name") or "")
        if not name.startswith("companion-"):
            return False
        session_key = str(job.get("sessionKey") or "")
        if owner_key and session_key and session_key != owner_key:
            return False
        return True

    def extract_jobs(payload):
        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, dict)]
        if not isinstance(payload, dict):
            return []
        for key in ("jobs", "rows", "items", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
            if isinstance(value, dict):
                nested = extract_jobs(value)
                if nested:
                    return nested
        return []

    def issue_from_job(job: dict):
        state = job.get("state") if isinstance(job.get("state"), dict) else {}
        name = str(job.get("name") or job.get("id") or "companion-job")
        run_status = state.get("lastRunStatus", job.get("lastRunStatus", state.get("lastStatus", job.get("status"))))
        delivery_status = state.get("lastDeliveryStatus", job.get("lastDeliveryStatus"))
        consecutive_errors = safe_int(state.get("consecutiveErrors", job.get("consecutiveErrors", 0)))
        last_error = state.get("lastError") or job.get("lastError")
        diagnostic_summary = state.get("lastDiagnosticSummary") or job.get("lastDiagnosticSummary")
        diagnostics = state.get("lastDiagnostics") if isinstance(state.get("lastDiagnostics"), dict) else {}
        diagnostic_entries = diagnostics.get("entries") if isinstance(diagnostics.get("entries"), list) else []

        if consecutive_errors > 0:
            detail = last_error or run_status or f"{consecutive_errors} consecutive errors"
            return issue(str(run_status or "error"), "consecutive_errors", f"{name}: {detail}")
        if is_bad_run_status(run_status):
            detail = last_error or run_status
            return issue(str(run_status), "last_run_status", f"{name}: {detail}")
        if is_bad_delivery_status(delivery_status):
            return issue(str(delivery_status), "last_delivery_status", f"{name}: delivery {delivery_status}")
        if is_bad_diagnostic(diagnostic_summary):
            return issue("error", "last_diagnostic", f"{name}: {diagnostic_summary}")
        for entry in diagnostic_entries:
            if not isinstance(entry, dict):
                continue
            if str(entry.get("severity") or "").lower() == "error" or is_bad_diagnostic(entry.get("message")):
                return issue("error", "last_diagnostic", f"{name}: {entry.get('message') or 'diagnostic error'}")
        return None

    def collect_issues(payload):
        issues = []
        for job in extract_jobs(payload):
            if not companion_job_matches(job):
                continue
            detected = issue_from_job(job)
            if detected:
                issues.append(detected)
        return issues[:3]

    jobs_command = runtime.get("jobs_list_command")
    if jobs_command:
        command_candidates = [jobs_command]
        if "--json" not in jobs_command:
            command_candidates.insert(0, f"{jobs_command} --json")
        for command in command_candidates:
            try:
                jobs_output = run_shell(command, {}, expect_json=False, timeout_sec=8)
                issues = collect_issues(json.loads(jobs_output))
                if issues:
                    return issues
            except Exception:
                continue

    if cron_jobs_file:
        try:
            return collect_issues(load_json(Path(cron_jobs_file), {}) or {})
        except Exception:
            pass
    return []


def resolve_mode_profile(config: dict, mode: str):
    behavior = config.get("behavior", {}) if isinstance(config, dict) else {}
    mode_profiles = behavior.get("mode_profiles", {}) if isinstance(behavior, dict) else {}
    profile = mode_profiles.get(mode, {}) if isinstance(mode_profiles, dict) else {}
    style_variants = profile.get("style_variants") or MODE_STYLE_VARIANTS.get(mode) or DEFAULT_STYLE_VARIANTS
    content_types = profile.get("content_types") or MODE_CONTENT_TYPES.get(mode) or DEFAULT_CONTENT_TYPES
    if not isinstance(style_variants, list) or not style_variants:
        style_variants = DEFAULT_STYLE_VARIANTS
    if not isinstance(content_types, list) or not content_types:
        content_types = DEFAULT_CONTENT_TYPES
    content_rules = profile.get("content_rules") if isinstance(profile, dict) else None
    if content_rules is None:
        content_rules = behavior.get("content_rules") if isinstance(behavior, dict) else None
    if not isinstance(content_rules, list):
        content_rules = DEFAULT_CONTENT_RULES
    return style_variants, content_types, content_rules


def choose_style(mode: str, state: dict, idle_sec: int, config: dict):
    pref = state["preference_profile"]
    last_style = state.get("last_style") or ""
    variants, _, _ = resolve_mode_profile(config, mode)
    variants = variants[:]
    idx = int(time.time()) % len(variants)
    style = variants[idx]
    if pref["service"] > pref["clingy"] and pref["service"] > pref["curious"]:
        style = "service_nudge"
    elif pref["clingy"] > pref["service"] and pref["clingy"] > pref["curious"]:
        style = "gentle_clingy"
    elif pref["teasing"] >= 3:
        style = "teasing_checkin"
    if style == last_style:
        for candidate in variants:
            if candidate != last_style:
                style = candidate
                break
    return style


def classify_operational_signal(gateway_healthy: bool, issues: list[str]):
    if not gateway_healthy:
        return {
            "level": "high",
            "kind": "gateway_unhealthy",
            "blend": "service_report",
            "should_mention": True,
        }
    if issues:
        return {
            "level": "medium",
            "kind": "cron_issue",
            "blend": "soft_service_note",
            "should_mention": True,
        }
    return {
        "level": "none",
        "kind": "none",
        "blend": "none",
        "should_mention": False,
    }


def choose_content(mode: str, state: dict, operational_signal: dict, emotion_level: str, config: dict):
    _, options, content_rules = resolve_mode_profile(config, mode)
    options = options[:]
    last_content = state.get("last_content_type") or ""
    idx = int(time.time() / 3) % len(options)
    content = options[idx]
    pref = state["preference_profile"]
    if content == last_content:
        for candidate in options:
            if candidate != last_content:
                content = candidate
                break
    def matches_condition(when: dict) -> bool:
        if not isinstance(when, dict):
            return False
        if "operational_level" in when and operational_signal.get("level") != when["operational_level"]:
            return False
        if "emotion_level" in when and emotion_level != when["emotion_level"]:
            return False
        if "emotion_level_not" in when and emotion_level == when["emotion_level_not"]:
            return False
        if "last_content_not" in when and last_content == when["last_content_not"]:
            return False
        pref_gte = when.get("preference_gte")
        if isinstance(pref_gte, dict):
            for key, threshold in pref_gte.items():
                if pref.get(key, 0) < threshold:
                    return False
        pref_gte_key = when.get("preference_gte_key")
        if isinstance(pref_gte_key, list) and len(pref_gte_key) == 2:
            if pref.get(pref_gte_key[0], 0) < pref.get(pref_gte_key[1], 0):
                return False
        pref_any = when.get("preference_any")
        if isinstance(pref_any, list):
            matched_any = False
            for rule in pref_any:
                if not isinstance(rule, dict):
                    continue
                key = rule.get("key")
                if not key:
                    continue
                if "gt_key" in rule and pref.get(key, 0) > pref.get(rule["gt_key"], 0):
                    matched_any = True
                if "gte" in rule and pref.get(key, 0) >= rule["gte"]:
                    matched_any = True
            if not matched_any:
                return False
        return True

    if operational_signal.get("level") == "high":
        return "micro_report"
    for rule in content_rules:
        if not isinstance(rule, dict):
            continue
        modes = rule.get("modes")
        if modes is not None and mode not in modes:
            continue
        content_type = rule.get("content_type")
        if content_type and matches_condition(rule.get("when", {})):
            return content_type
    return content


def pending_heartbeat_send(state: dict, now_epoch: int) -> dict:
    pending = state.get("pending_send", {}) or {}
    if pending.get("mode") != "heartbeat":
        return {}
    expires_at = int(pending.get("expires_at", 0) or 0)
    if expires_at and expires_at < now_epoch:
        return {}
    return pending


def heartbeat_event_key(current_event: dict, today: str) -> str:
    if not current_event:
        return ""
    return "|".join(
        [
            clean_text(today),
            clean_text(current_event.get("start_time")),
            clean_text(current_event.get("title")),
        ]
    )


def record_pending_send(
    state: dict,
    mode: str,
    now_epoch: int,
    style_variant: str,
    content_type: str,
    emotion_level: str,
    run_id: str = "",
    event_key: str = "",
):
    delivery_attempt_id = f"{mode}-{now_epoch}-{secrets.token_hex(4)}"
    state["pending_send"] = {
        "mode": mode,
        "generated_at": now_epoch,
        "event_key": event_key,
        "style": style_variant,
        "content_type": content_type,
        "emotion_level": emotion_level,
        "run_id": run_id,
        "delivery_attempt_id": delivery_attempt_id,
        "expires_at": now_epoch + 86400,
    }


def clear_pending_send(state: dict, mode: str):
    pending = state.get("pending_send", {}) or {}
    if pending.get("mode") == mode:
        state["pending_send"] = {
            "mode": "",
            "generated_at": 0,
            "event_key": "",
            "style": "",
            "content_type": "",
            "emotion_level": "",
            "run_id": "",
            "delivery_attempt_id": "",
            "expires_at": 0,
        }


def apply_send_success_metadata(
    state: dict,
    mode: str,
    now_epoch: int,
    today: str,
    count_daily: bool = True,
    event_key: str = "",
    style_variant: str = "",
    content_type: str = "",
):
    if mode == "heartbeat":
        state["last_heartbeat_at"] = now_epoch
        if event_key:
            state["last_heartbeat_event_key"] = event_key
    else:
        state["last_proactive_at"] = now_epoch
    if count_daily:
        state["daily_count"] += 1
    state["last_mode"] = mode
    if style_variant:
        state["last_style"] = style_variant
    if content_type:
        state["last_content_type"] = content_type
    state.setdefault("mode_days", {})[mode] = today


def mark_send_success(
    state: dict,
    mode: str,
    now_epoch: int,
    today: str,
    count_daily: bool = True,
    run_id: str = "",
    event_key: str = "",
    style_variant: str = "",
    content_type: str = "",
) -> bool:
    pending = state.get("pending_send", {}) or {}
    if pending.get("mode") == mode:
        if run_id and pending.get("run_id") and pending.get("run_id") != run_id:
            return False
        apply_send_success_metadata(
            state,
            mode,
            now_epoch,
            today,
            count_daily=count_daily,
            event_key=clean_text(pending.get("event_key")),
            style_variant=clean_text(pending.get("style")),
            content_type=clean_text(pending.get("content_type")),
        )
        clear_pending_send(state, mode)
        return True

    fallback_event_key = clean_text(event_key)
    if mode == "heartbeat" and fallback_event_key and state.get("last_heartbeat_event_key") == fallback_event_key:
        return False
    apply_send_success_metadata(
        state,
        mode,
        now_epoch,
        today,
        count_daily=count_daily,
        event_key=fallback_event_key,
        style_variant=clean_text(style_variant),
        content_type=clean_text(content_type),
    )
    return True


def is_visible_assistant_delivery(text: str) -> bool:
    stripped = (text or "").strip()
    if not stripped:
        return False
    return stripped != "HEARTBEAT_OK"


def is_heartbeat_poll_text(text: str) -> bool:
    return HEARTBEAT_POLL_MARKER in (text or "")


def extract_text_content(content) -> str:
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts = []
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            parts.append(str(item.get("text") or ""))
    return "\n".join(part for part in parts if part)


def find_heartbeat_delivery_proof(session_file: Path | None, generated_at_epoch: int) -> dict:
    if not session_file or not session_file.exists() or not generated_at_epoch:
        return {"status": "pending"}

    threshold_ms = generated_at_epoch * 1000
    rows = load_jsonl(session_file)
    rows_by_id = {}
    children_by_parent = {}
    for row in rows:
        row_id = row.get("id")
        if row_id:
            rows_by_id[row_id] = row
        parent_id = row.get("parentId")
        if parent_id:
            children_by_parent.setdefault(parent_id, []).append(row)

    def row_message(row: dict) -> dict:
        return row.get("message", {}) if isinstance(row.get("message"), dict) else {}

    def row_role(row: dict) -> str:
        return str(row_message(row).get("role") or "")

    def row_text(row: dict) -> str:
        return extract_text_content(row_message(row).get("content"))

    def row_ts_ms(row: dict) -> int:
        msg = row_message(row)
        return parse_event_timestamp_ms(msg.get("timestamp")) or parse_event_timestamp_ms(row.get("timestamp"))

    def tool_result_payload(row: dict) -> dict:
        if row_role(row) != "toolResult":
            return {}
        text = row_text(row).strip()
        if not text:
            return {}
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            status_match = re.search(r'"status"\s*:\s*"([^"]+)"', text)
            mode_match = re.search(r'"mode"\s*:\s*"([^"]+)"', text)
            payload = {}
            if status_match:
                payload["status"] = status_match.group(1)
            if mode_match:
                payload["mode"] = mode_match.group(1)
            return payload
        return payload if isinstance(payload, dict) else {}

    def find_poll_ancestor(row: dict) -> dict:
        seen = set()
        current = row
        while isinstance(current, dict):
            row_id = current.get("id")
            if row_id in seen:
                return {}
            if row_id:
                seen.add(row_id)
            if current.get("type") == "message" and row_role(current) == "user" and is_heartbeat_poll_text(row_text(current)):
                return current
            parent_id = current.get("parentId")
            if not parent_id:
                return {}
            current = rows_by_id.get(parent_id)
        return {}

    for row in rows:
        payload = tool_result_payload(row)
        if payload.get("mode") != "heartbeat" or "status" not in payload:
            continue
        ts_ms = row_ts_ms(row)
        if ts_ms and ts_ms < threshold_ms:
            continue
        poll_row = find_poll_ancestor(row)
        if not poll_row:
            continue
        run_status = clean_text(payload.get("status")) or "unknown"
        if run_status != "ok":
            return {
                "status": "undelivered",
                "run_status": run_status,
                "tool_result_at": ts_ms // 1000 if ts_ms else int(time.time()),
            }
        for child in children_by_parent.get(row.get("id"), []):
            role = row_role(child)
            text = row_text(child)
            child_ts_ms = row_ts_ms(child)
            if role == "assistant" and is_visible_assistant_delivery(text):
                return {
                    "status": "delivered",
                    "delivered_at": child_ts_ms // 1000 if child_ts_ms else int(time.time()),
                    "text_preview": text.strip()[:120],
                }
            if role == "user":
                return {
                    "status": "interrupted",
                    "interrupted_at": child_ts_ms // 1000 if child_ts_ms else int(time.time()),
                    "text_preview": text.strip()[:120],
                }
        return {"status": "pending"}
    return {"status": "pending"}


def reconcile_pending_heartbeat_delivery(state: dict, session_file: Path | None, current_day: str) -> dict:
    pending = state.get("pending_send", {}) or {}
    if pending.get("mode") != "heartbeat":
        return {"status": "none"}
    generated_at = int(pending.get("generated_at", 0) or 0)
    delivery = find_heartbeat_delivery_proof(session_file, generated_at)
    if delivery.get("status") == "pending":
        return {"status": "pending", "generated_at": generated_at}
    if delivery.get("status") in {"undelivered", "interrupted"}:
        clear_pending_send(state, "heartbeat")
        return {
            "status": delivery.get("status"),
            "generated_at": generated_at,
            "run_status": delivery.get("run_status", ""),
            "text_preview": delivery.get("text_preview", ""),
        }

    delivered_at = int(delivery.get("delivered_at") or int(time.time()))
    delivered_day = datetime.fromtimestamp(delivered_at).strftime("%Y-%m-%d")
    recorded = mark_send_success(
        state,
        "heartbeat",
        delivered_at,
        delivered_day,
        count_daily=(delivered_day == current_day),
    )
    return {
        "status": "recorded" if recorded else "already_recorded",
        "delivered_at": delivered_at,
        "text_preview": delivery.get("text_preview", ""),
    }


def now_parts(timezone: str):
    if timezone:
        os.environ["TZ"] = timezone
        time.tzset()
    now_epoch = int(time.time())
    local = datetime.fromtimestamp(now_epoch)
    return now_epoch, local.strftime("%Y-%m-%d"), int(local.strftime("%H%M"))


def get_life_schedule(config: dict):
    return config.get("life_schedule", {}) if isinstance(config.get("life_schedule"), dict) else {}


def get_day_schedule_path(config: dict) -> Path | None:
    life = get_life_schedule(config)
    day_schedule = life.get("day_schedule", {}) if isinstance(life.get("day_schedule"), dict) else {}
    path = day_schedule.get("schedule_path")
    return Path(path) if path else None


def get_life_log_path(config: dict) -> Path | None:
    life = get_life_schedule(config)
    continuity = life.get("continuity", {}) if isinstance(life.get("continuity"), dict) else {}
    path = continuity.get("life_log_path")
    return Path(path) if path else None


def parse_markdown_kv(line: str) -> tuple[str, str] | None:
    match = re.match(r"^\s*-\s*([^：:]+)[：:]\s*(.*)\s*$", line)
    if not match:
        return None
    return match.group(1).strip(), match.group(2).strip()


def parse_duration_minutes(value: str) -> int:
    text = clean_text(value)
    if not text:
        return 0
    hour_match = re.search(r"(\d+)\s*(?:小时|h|hour)", text, flags=re.IGNORECASE)
    minute_match = re.search(r"(\d+)\s*(?:分钟|min|m)", text, flags=re.IGNORECASE)
    total = 0
    if hour_match:
        total += int(hour_match.group(1)) * 60
    if minute_match:
        total += int(minute_match.group(1))
    if total:
        return total
    if re.fullmatch(r"\d{1,3}", text):
        return int(text)
    return 0


def minutes_from_hhmm(value: str) -> int:
    hour, minute = value.split(":", 1)
    return int(hour) * 60 + int(minute)


def load_day_schedule(config: dict) -> dict:
    path = get_day_schedule_path(config)
    if not path or not path.exists():
        return {"background": {}, "events": [], "missing": True}
    text = path.read_text(encoding="utf-8")
    background = {}
    boundaries = {}
    events = []
    current = None
    section = ""
    for line in text.splitlines():
        heading2 = re.match(r"^##\s+(?:(\d+)\.\s+)?(.+?)\s*$", line)
        if heading2:
            section = heading2.group(2).strip()
            current = None
            continue
        event_heading = re.match(r"^###\s+([0-2]\d:[0-5]\d)\s+-\s+(.+?)\s*$", line)
        if event_heading:
            current = {
                "start_time": event_heading.group(1),
                "title": event_heading.group(2).strip(),
                "fields": {},
            }
            events.append(current)
            continue
        kv = parse_markdown_kv(line)
        if not kv:
            continue
        key, value = kv
        if current is not None:
            current["fields"][key] = value
        elif section == "今日背景":
            background[key] = value
        elif section == "今日边界":
            boundaries[key] = value

    normalized_events = []
    for event in events:
        fields = event.get("fields", {})
        duration_min = parse_duration_minutes(fields.get("执行时间", ""))
        start_min = minutes_from_hhmm(event["start_time"])
        normalized_events.append(
            {
                "start_time": event["start_time"],
                "start_minute": start_min,
                "duration_min": duration_min,
                "end_minute": start_min + duration_min,
                "title": event["title"],
                "required": clean_text(fields.get("必定发生")) == "是",
                "scene": clean_text(fields.get("场景")),
                "activity": clean_text(fields.get("正在做什么")),
                "emotion": clean_text(fields.get("情绪/状态")),
                "mention": clean_text(fields.get("可自然提到")),
                "interaction": clean_text(fields.get("用户互动入口")),
                "media_info": clean_text(fields.get("媒体信息")),
                "avoid": clean_text(fields.get("不要写成")),
            }
        )
    return {"background": background, "boundaries": boundaries, "events": normalized_events, "missing": False}


def day_schedule_date_status(schedule: dict, now_epoch: int) -> dict:
    background = schedule.get("background", {}) if isinstance(schedule.get("background"), dict) else {}
    schedule_date = clean_text(background.get("日期"))
    expected_date = datetime.fromtimestamp(now_epoch).strftime("%Y-%m-%d")
    if schedule.get("missing"):
        return {"ok": False, "reason": "missing_day_schedule", "schedule_date": "", "expected_date": expected_date}
    if schedule_date and schedule_date != expected_date:
        return {
            "ok": False,
            "reason": "stale_day_schedule",
            "schedule_date": schedule_date,
            "expected_date": expected_date,
        }
    return {"ok": True, "reason": "", "schedule_date": schedule_date, "expected_date": expected_date}


def select_current_day_schedule_event_from_schedule(schedule: dict, now_epoch: int) -> dict:
    date_status = day_schedule_date_status(schedule, now_epoch)
    if not date_status.get("ok"):
        return {}
    local = datetime.fromtimestamp(now_epoch)
    current_minute = local.hour * 60 + local.minute
    events = schedule.get("events", [])
    for event in events:
        duration = int(event.get("duration_min", 0) or 0)
        if duration <= 0:
            continue
        start = int(event.get("start_minute", 0) or 0)
        end = int(event.get("end_minute", start) or start)
        matched = start <= current_minute < end
        if not matched and end > 24 * 60:
            matched = start <= current_minute + 24 * 60 < end
        if matched:
            selected = dict(event)
            selected["matched_at_minute"] = current_minute
            selected["selection_mode"] = "current_time"
            selected["day_type"] = clean_text(schedule.get("background", {}).get("今日类型"))
            selected["weather_hint"] = clean_text(schedule.get("background", {}).get("天气/环境"))
            selected["city_or_place"] = clean_text(schedule.get("background", {}).get("城市/主要地点"))
            selected["schedule_date"] = date_status.get("schedule_date")
            return selected
    return {}


def select_current_day_schedule_event(config: dict, now_epoch: int) -> dict:
    return select_current_day_schedule_event_from_schedule(load_day_schedule(config), now_epoch)


def normalize_life_claims(claims):
    seen = set()
    normalized = []
    for claim in claims or []:
        text = str(claim).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        normalized.append(text)
    return normalized


def build_current_event_context(config: dict, now_epoch: int | None = None):
    life = get_life_schedule(config)
    now_epoch = now_epoch or int(time.time())
    schedule = load_day_schedule(config)
    date_status = day_schedule_date_status(schedule, now_epoch)
    current_event = select_current_day_schedule_event_from_schedule(schedule, now_epoch)
    background = schedule.get("background", {}) if isinstance(schedule.get("background"), dict) else {}
    boundaries = schedule.get("boundaries", {}) if isinstance(schedule.get("boundaries"), dict) else {}
    today_context = {
        "date": clean_text(background.get("日期")) or clean_text(date_status.get("schedule_date")),
        "weekday": clean_text(background.get("星期")),
        "day_type": clean_text(background.get("今日类型")),
        "city_or_place": clean_text(background.get("城市/时区")) or clean_text(background.get("城市/主要地点")),
        "background": clean_text(background.get("今日底色")),
        "weather": clean_text(background.get("天气/环境")),
        "avoid_repeating": clean_text(boundaries.get("避免重复")),
        "do_not_mention": clean_text(boundaries.get("不要提")),
        "continuity_hint": clean_text(boundaries.get("可以轻轻延续")),
    }

    return {
        "enabled": bool(life.get("enabled", False)),
        "persona_reality_hints": build_persona_reality_hints(config),
        "source": "day_schedule",
        "skip_reason": "" if current_event else clean_text(date_status.get("reason")),
        "schedule_date": clean_text(date_status.get("schedule_date")),
        "expected_date": clean_text(date_status.get("expected_date")),
        "current_event": current_event,
        "today": today_context,
        "day_type": current_event.get("day_type", ""),
        "day_scene": current_event.get("scene", ""),
        "micro_plans": [current_event.get("activity", "")] if current_event.get("activity") else [],
        "today_story_beats": [current_event.get("mention", "")] if current_event.get("mention") else [],
        "hourly_bias": {current_event.get("start_time", "")[:2]: current_event.get("title", "")} if current_event else {},
        "weather_hint": {"summary": current_event.get("weather_hint", "")} if current_event.get("weather_hint") else {},
        "mention_candidates": [current_event.get("mention", "")] if current_event.get("mention") else [],
        "avoid_mentions": [current_event.get("avoid", "")] if current_event.get("avoid") else [],
        "monthly_theme": "",
        "reality_anchors": {},
        "special_dates": [],
        "watchlist": [],
    }


def update_presence_schedule_health(state: dict, reason: str, now_epoch: int, today: str) -> dict:
    health = state.get("presence_schedule_health", {}) if isinstance(state.get("presence_schedule_health"), dict) else {}
    schedule_failure_reasons = {"missing_day_schedule", "stale_day_schedule"}
    if reason in schedule_failure_reasons:
        last_reason = clean_text(health.get("last_reason"))
        consecutive = int(health.get("consecutive_failures", 0) or 0)
        if last_reason == reason:
            consecutive += 1
        else:
            consecutive = 1
        health.update(
            {
                "last_reason": reason,
                "last_checked_at": now_epoch,
                "last_failure_day": today,
                "consecutive_failures": consecutive,
            }
        )
    else:
        health.update(
            {
                "last_reason": reason,
                "last_checked_at": now_epoch,
                "consecutive_failures": 0,
            }
        )
    state["presence_schedule_health"] = health
    return health


def should_notify_presence_schedule_failure(health: dict, today: str) -> bool:
    if int(health.get("consecutive_failures", 0) or 0) < PRESENCE_SCHEDULE_FAILURE_ALERT_THRESHOLD:
        return False
    return clean_text(health.get("last_alert_day")) != today


def mark_presence_schedule_alerted(state: dict, today: str, now_epoch: int):
    health = state.setdefault("presence_schedule_health", {})
    health["last_alert_day"] = today
    health["last_alert_at"] = now_epoch


def append_life_log(config: dict, mode: str, now_epoch: int, claims, tags, source_day: str):
    path = get_life_log_path(config)
    if not path:
        return False
    claims = normalize_life_claims(claims)
    tags = normalize_life_claims(tags)
    if not claims:
        return False
    local = datetime.fromtimestamp(now_epoch)
    entry = {
        "ts": local.isoformat(timespec="seconds"),
        "mode": mode,
        "date": local.strftime("%Y-%m-%d"),
        "life_claims": claims[:5],
        "source_day": source_day,
    }
    if tags:
        entry["tags"] = tags[:5]
    append_jsonl(path, entry)
    return True


def parse_json_arg(value: str | None, default):
    if not value:
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON argument: {exc}")


def delivery_contract(config: dict) -> dict:
    delivery = config.get("delivery", {}) if isinstance(config.get("delivery"), dict) else {}
    return {
        "channel": clean_text(delivery.get("channel")),
        "target": clean_text(delivery.get("owner_target")),
        "account": clean_text(delivery.get("account")),
        "send_in_main_turn": True,
    }


def state_commit(
    config_path: Path,
    run_id: str,
    has_media: bool = False,
    event_key: str = "",
    style_variant: str = "",
    content_type: str = "",
) -> dict:
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--config",
        str(config_path),
        "--mark-sent",
        "--run-id",
        run_id,
    ]
    if event_key:
        command.extend(["--event-key", event_key])
    if style_variant:
        command.extend(["--style-variant", style_variant])
    if content_type:
        command.extend(["--content-type", content_type])
    return {
        "when": "after_text_send",
        "token": "",
        "command": command,
    }


def infer_media_tool(media_info: str) -> str:
    text = clean_text(media_info)
    if not text:
        return ""
    if any(keyword in text for keyword in ["视频", "镜头", "短片", "动画"]):
        return "video_generate"
    if any(keyword in text for keyword in ["唱", "哼", "音频", "音乐", "录音", "声音"]):
        return "music_generate"
    return "image_generate"


def media_contract(media_info: str = "") -> dict:
    has_media = bool(clean_text(media_info))
    return {
        "kind": "event_media" if has_media else "none",
        "async": bool(has_media),
        "count": 1 if has_media else 0,
        "tool_name": infer_media_tool(media_info),
        "completion_event_is_sender": bool(has_media),
        "callback_context": {
            "strategy": "same_stable_session" if has_media else "none",
            "requires_original_session_context": bool(has_media),
            "send_media_with": "delivery_contract" if has_media else "",
            "commit_after_media_send_with": "",
        },
    }


def select_life_context(config: dict, runner_payload: dict) -> dict:
    current_event_context = runner_payload.get("current_event_context", {}) if isinstance(runner_payload.get("current_event_context"), dict) else {}
    companion = runner_payload.get("companion_state", {}) if isinstance(runner_payload.get("companion_state"), dict) else {}
    current_event = current_event_context.get("current_event", {}) if isinstance(current_event_context.get("current_event"), dict) else {}
    today_context = current_event_context.get("today", {}) if isinstance(current_event_context.get("today"), dict) else {}

    action = clean_text(current_event.get("activity"))
    event = {}
    if current_event:
        event = {
            "title": clean_text(current_event.get("title")),
            "start_time": clean_text(current_event.get("start_time")),
            "duration_min": current_event.get("duration_min", 0),
            "required": bool(current_event.get("required", False)),
            "scene": clean_text(current_event.get("scene")),
            "action": action,
            "emotion": clean_text(current_event.get("emotion")),
            "natural_mention": clean_text(current_event.get("mention")),
            "user_interaction": clean_text(current_event.get("interaction")),
            "media_info": clean_text(current_event.get("media_info")),
            "avoid": clean_text(current_event.get("avoid")),
        }

    return {
        "generated_at": datetime.fromtimestamp(int(time.time())).isoformat(timespec="seconds"),
        "timezone": clean_text(config.get("timezone")) or "Asia/Shanghai",
        "speaker": {
            "name": clean_text(companion.get("name")),
            "identity": clean_text(companion.get("identity_role")),
            "write_as": "我",
            "boundary": "这是说话人本人，不是同行人物。",
        },
        "today": {
            "date": clean_text(today_context.get("date")) or clean_text(current_event.get("schedule_date")),
            "day_type": clean_text(today_context.get("day_type")) or clean_text(current_event.get("day_type")),
            "city_or_place": clean_text(today_context.get("city_or_place")) or clean_text(current_event.get("city_or_place")) or clean_text(companion.get("city")),
            "background": clean_text(today_context.get("background")),
            "weather": clean_text(today_context.get("weather")) or clean_text(current_event.get("weather_hint")),
            "avoid_repeating": clean_text(today_context.get("avoid_repeating")),
            "do_not_mention": clean_text(today_context.get("do_not_mention")),
            "continuity_hint": clean_text(today_context.get("continuity_hint")),
        },
        "event": event,
        "delivery_mood": {
            "level": clean_text(companion.get("emotion_level")),
            "style": clean_text(companion.get("style_variant")),
            "content_type": clean_text(companion.get("content_type")),
        },
        "reality_check": {
            "passed": bool(current_event and action),
            "source": "day_schedule_current_event",
        },
    }


def build_prepare_contract(args, config: dict, config_path: Path, runner_payload: dict, run_id_override: str = "") -> dict:
    run_id = run_id_override or runner_payload.get("run_id") or args.run_id or f"presence-{datetime.now().strftime('%Y%m%d%H%M%S')}-{secrets.token_hex(4)}"
    life_context = select_life_context(config, runner_payload)
    event = life_context.get("event", {}) if isinstance(life_context.get("event"), dict) else {}
    delivery_mood = life_context.get("delivery_mood", {}) if isinstance(life_context.get("delivery_mood"), dict) else {}
    commit_event_key = clean_text(runner_payload.get("event_key")) or heartbeat_event_key(event, clean_text(life_context.get("today", {}).get("date")))
    event_media_info = clean_text(life_context.get("event", {}).get("media_info")) if isinstance(life_context.get("event"), dict) else ""
    has_media = bool(event_media_info)
    delivery_tracking = runner_payload.get("delivery_tracking", {}) if isinstance(runner_payload.get("delivery_tracking"), dict) else {}
    delivery_tracking = {**delivery_tracking, "run_id": clean_text(delivery_tracking.get("run_id")) or run_id}
    delivery = delivery_contract(config)
    media = media_contract(event_media_info)
    commit = state_commit(
        config_path,
        run_id,
        has_media=has_media,
        event_key=commit_event_key,
        style_variant=clean_text(delivery_mood.get("style")),
        content_type=clean_text(delivery_mood.get("content_type")),
    )
    return {
        "status": "ok" if life_context.get("reality_check", {}).get("passed") else "needs_review",
        "pipeline_stage": "prepare",
        "run_id": run_id,
        "generated_at": datetime.fromtimestamp(int(time.time())).isoformat(timespec="seconds"),
        "life_context": life_context,
        "delivery_contract": delivery,
        "media_contract": media,
        "state_commit": commit,
        "delivery_tracking": delivery_tracking,
        "next_step": "write_presence_story_send_text_commit_then_start_async_media" if has_media else "write_presence_story_then_send_and_commit",
    }


def parse_args():
    parser = argparse.ArgumentParser(description="Companion state manager — outputs context JSON for the agent.")
    parser.add_argument("positional_mode", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument("--mode", dest="mode_flag", choices=["heartbeat"], help=argparse.SUPPRESS)
    parser.add_argument("--stage", choices=["prepare"], default="prepare", help="Current architecture only emits the prepare contract.")
    parser.add_argument("--config", default=str(Path(__file__).resolve().parents[1] / "config.local.json"))
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Do not write state, pending_send, or life-log changes. Useful for cron flow tests.")
    parser.add_argument("--no-record-pending", action="store_true", help="Generate ok output without recording pending_send.")
    parser.add_argument("--mark-sent", action="store_true", help="Commit pacing state only after the user-visible message was actually delivered.")
    parser.add_argument("--run-id", help="Stable run id used to bind delivery and state commit.")
    parser.add_argument("--event-key", help="Fallback heartbeat event key to commit when pending_send was intentionally not recorded.")
    parser.add_argument("--style-variant", help="Fallback style variant to commit when pending_send was intentionally not recorded.")
    parser.add_argument("--content-type", help="Fallback content type to commit when pending_send was intentionally not recorded.")
    parser.add_argument("--record-life-claims-json", help="JSON array of explicit life claims surfaced in the delivered message.")
    parser.add_argument("--record-life-tags-json", help="Optional JSON array of lightweight tags for the life claims.")
    parser.add_argument("--record-life-source-day", help="Optional source day for the life claims; defaults to current day-schedule date or today.")
    args = parser.parse_args()
    if args.mode_flag and args.mode_flag != PRESENCE_MODE:
        parser.error("current architecture only supports the default presence flow")
    if args.positional_mode and args.positional_mode != PRESENCE_MODE:
        parser.error("current architecture only supports the default presence flow")
    return args


def main():
    args = parse_args()
    config_path = Path(args.config).resolve()
    config = ensure_config(config_path)
    state_file = Path(config["runtime"]["state_file"])
    sessions_store = Path(config["runtime"]["sessions_store_path"])
    run_id = args.run_id or f"presence-{datetime.now().strftime('%Y%m%d%H%M%S')}-{secrets.token_hex(4)}"

    owner_key = config["delivery"].get("owner_session_key", "")
    recent_messages_path = resolve_session_file(sessions_store, owner_key) if owner_key else None
    state = ensure_state(state_file, persist=not args.dry_run)
    state = learn_from_replies(state, recent_messages_path)

    now_epoch, today, hour_min = now_parts(config.get("timezone", ""))
    if state.get("day") != today:
        state["day"] = today
        state["daily_count"] = 0

    delivery_reconciliation = reconcile_pending_heartbeat_delivery(state, recent_messages_path, today)
    if not args.dry_run and delivery_reconciliation.get("status") in {"recorded", "already_recorded", "undelivered", "interrupted"}:
        save_json(state_file, state)

    if args.mark_sent:
        recorded = mark_send_success(
            state,
            PRESENCE_MODE,
            now_epoch,
            today,
            run_id=run_id,
            event_key=args.event_key or "",
            style_variant=args.style_variant or "",
            content_type=args.content_type or "",
        )
        claims = parse_json_arg(args.record_life_claims_json, [])
        tags = parse_json_arg(args.record_life_tags_json, [])
        source_day = args.record_life_source_day or today
        life_logged = False if args.dry_run else (append_life_log(config, PRESENCE_MODE, now_epoch, claims, tags, source_day) if recorded else False)
        if not args.dry_run:
            save_json(state_file, state)
        print(
            json.dumps(
                {
                    "status": "dry_run" if args.dry_run else ("recorded" if recorded else "already_recorded"),
                    "recorded_at": now_epoch,
                    "would_mark_sent": bool(recorded),
                    "life_log_recorded": life_logged,
                },
                ensure_ascii=False,
            )
        )
        return

    if not args.force:
        quiet_start = parse_hhmm(config["schedule"]["quiet_hours_start"])
        quiet_end = parse_hhmm(config["schedule"]["quiet_hours_end"])
        if is_in_quiet_hours(hour_min, quiet_start, quiet_end):
            if not args.dry_run:
                save_json(state_file, state)
            print(json.dumps({"status": "skip", "reason": "quiet_hours"}))
            return
    owner_session_entry = resolve_session_entry(sessions_store, owner_key) if owner_key else {}
    owner_updated_ms = owner_session_entry.get("updatedAt", 0)
    owner_updated_sec = owner_updated_ms // 1000
    idle_sec = now_epoch - owner_updated_sec if owner_updated_sec else 0
    idle_hours = idle_sec / 3600.0 if idle_sec else 0.0

    thresholds = config["behavior"]["emotion_thresholds"]
    emotion = infer_emotion(idle_sec, state["relationship_state"].get("attention_balance", "steady"), thresholds)

    health_error = ""
    try:
        health_output = run_shell(config["runtime"]["healthcheck_command"], {}, expect_json=False)
        runtime_ok = "Runtime: running" in health_output
        probe_ok = any(marker in health_output for marker in ("RPC probe: ok", "Connectivity probe: ok"))
        gateway_healthy = runtime_ok and probe_ok
        if not gateway_healthy:
            health_error = "healthcheck did not report running runtime and successful probe"
    except Exception as exc:
        gateway_healthy = False
        health_error = str(exc)
    issues = load_cron_issues(config)
    operational_signal = classify_operational_signal(gateway_healthy, issues)

    style_variant = choose_style(PRESENCE_MODE, state, idle_sec, config)
    content_type = choose_content(PRESENCE_MODE, state, operational_signal, emotion, config)
    current_event_context = build_current_event_context(config, now_epoch)
    heartbeat_current_event_key = ""
    pending_heartbeat = pending_heartbeat_send(state, now_epoch)
    if pending_heartbeat:
        if not args.dry_run:
            save_json(state_file, state)
        print(json.dumps({"status": "skip", "reason": "pending_heartbeat_delivery"}))
        return
    current_event = current_event_context.get("current_event")
    if not current_event:
        reason = current_event_context.get("skip_reason") or "no_matching_day_schedule_event"
        health = update_presence_schedule_health(state, reason, now_epoch, today)
        if should_notify_presence_schedule_failure(health, today):
            mark_presence_schedule_alerted(state, today, now_epoch)
            if not args.dry_run:
                save_json(state_file, state)
            print(
                json.dumps(
                    {
                        "status": "notify_owner",
                        "reason": reason,
                        "notification_text": "我这边今天的日程没接上，先安静一下，等整理好再来找你。",
                        "delivery_contract": {
                            "channel": config.get("delivery", {}).get("channel", ""),
                            "target": config.get("delivery", {}).get("owner_target", ""),
                            "account": config.get("delivery", {}).get("account", ""),
                        },
                        "presence_schedule_health": health,
                    },
                    ensure_ascii=False,
                )
            )
            return
        if not args.dry_run:
            save_json(state_file, state)
        print(json.dumps({"status": "skip", "reason": reason}, ensure_ascii=False))
        return
    update_presence_schedule_health(state, "ok", now_epoch, today)
    heartbeat_current_event_key = heartbeat_event_key(current_event, today)
    if heartbeat_current_event_key and state.get("last_heartbeat_event_key") == heartbeat_current_event_key:
        if not args.dry_run:
            save_json(state_file, state)
        print(json.dumps({"status": "skip", "reason": "event_already_sent"}))
        return

    should_record_pending = not args.dry_run and not args.no_record_pending
    if should_record_pending:
        record_pending_send(
            state,
            PRESENCE_MODE,
            now_epoch,
            style_variant,
            content_type,
            emotion,
            run_id=run_id,
            event_key=heartbeat_current_event_key,
        )
        save_json(state_file, state)

    current_event = current_event_context.get("current_event", {}) if isinstance(current_event_context.get("current_event"), dict) else {}
    current_event_media_info = clean_text(current_event.get("media_info"))
    has_event_media = bool(current_event_media_info)
    persona = config.get("_character_profile_persona") or config.get("persona", {})
    owner_profile = resolve_owner_profile(config, config_path)
    runner_payload = {
        "status": "ok",
        "run_id": run_id,
        "event_key": heartbeat_current_event_key,
        "companion_state": {
            "name": persona.get("name", "Companion"),
            "owner_nickname": persona.get("owner_nickname", "Owner"),
            "owner_profile": owner_profile,
            "identity_role": persona.get("identity_role", "other"),
            "city": persona.get("city", ""),
            "life_stage": persona.get("life_stage", ""),
            "institution_or_workplace": persona.get("institution_or_workplace", ""),
            "style_variant": style_variant,
            "content_type": content_type,
            "emotion_level": emotion,
            "idle_hours": round(idle_hours, 1),
            "attention_balance": state["relationship_state"].get("attention_balance", "steady"),
            "scene_anchor": config.get("behavior", {}).get("derived_profile", {}).get("scene_anchor", ""),
            "social_energy": config.get("behavior", {}).get("derived_profile", {}).get("social_energy", ""),
            "expression_density": config.get("behavior", {}).get("derived_profile", {}).get("expression_density", ""),
            "operational_signal": operational_signal.get("level", "none"),
        },
        "current_event_context": current_event_context,
        "delivery_tracking": {
            "mark_sent_required": should_record_pending,
            "run_id": run_id,
            "delivery_kind": "text_then_async_media" if has_event_media else "text_sync",
            "send_in_main_turn": True,
            "completion_event_is_sender": has_event_media,
            "pending_delivery_reconciliation": delivery_reconciliation,
            "mark_sent_command": f"python3 {Path(__file__).resolve()} --config {config_path} --mark-sent",
            "life_logging_supported": True,
            "mark_sent_with_life_log_example": f"python3 {Path(__file__).resolve()} --config {config_path} --mark-sent --record-life-claims-json '[\"今天外面有点闷\"]' --record-life-tags-json '[\"weather\"]'",
            "dry_run": bool(args.dry_run),
            "pending_recorded": bool(should_record_pending),
        },
    }
    print(json.dumps(build_prepare_contract(args, config, config_path, runner_payload, run_id), ensure_ascii=False))


if __name__ == "__main__":
    main()
