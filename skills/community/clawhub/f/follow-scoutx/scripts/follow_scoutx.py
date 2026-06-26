#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
from typing import Any
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_FEED_URL = "https://input.reai.group/v1/public/feed"
DEFAULT_X_FEED_URL = "https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-x.json"
DEFAULT_PODCAST_FEED_URL = "https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-podcasts.json"
DEFAULT_TIMEOUT_SECONDS = 60
DEFAULT_USER_AGENT = "FollowScoutXSkill/0.1 (+https://input.reai.group)"
PROFILE_VERSION = 1
DEFAULT_SUMMARY_BUDGET_CHARS = 1200
DEFAULT_FEISHU_MESSAGE_CHAR_LIMIT = 6000
DEFAULT_GENERIC_MESSAGE_CHAR_LIMIT = 12000
SOURCE_TYPES = ("scoutx", "x", "podcast")
SOURCE_TYPE_LABELS = {
    "scoutx": "ScoutX",
    "x": "X",
    "podcast": "Podcast",
}
SOURCE_TYPE_ENV_VARS = {
    "scoutx": "FOLLOW_SCOUTX_FEED_URL",
    "x": "FOLLOW_SCOUTX_X_FEED_URL",
    "podcast": "FOLLOW_SCOUTX_PODCAST_FEED_URL",
}
SOURCE_MODE_TO_TYPES = {
    "scoutx": ["scoutx"],
    "curated": ["scoutx"],
    "media": ["scoutx"],
    "first_party": ["x", "podcast"],
    "first-party": ["x", "podcast"],
    "primary": ["x", "podcast"],
    "mixed": ["scoutx", "x", "podcast"],
    "all": ["scoutx", "x", "podcast"],
}
SOURCE_TYPE_ALIASES = {
    "scoutx": "scoutx",
    "media": "scoutx",
    "curated": "scoutx",
    "x": "x",
    "twitter": "x",
    "tweet": "x",
    "tweets": "x",
    "podcast": "podcast",
    "podcasts": "podcast",
    "播客": "podcast",
}
MESSAGE_GROUPS = {
    "first_party": ("x", "podcast"),
    "scoutx": ("scoutx",),
}
MESSAGE_GROUP_ORDER = ("first_party", "scoutx")
MESSAGE_GROUP_CHOICES = ("all", "first_party", "scoutx")
MESSAGE_GROUP_LIMIT_KEYS = {
    "first_party": "max_first_party_items",
    "scoutx": "max_scoutx_items",
}
MESSAGE_GROUP_NAME_SUFFIXES = {
    "first_party": "first-party",
    "scoutx": "scoutx",
}
STYLE_TO_SUMMARY_BUDGET = {
    "short": 700,
    "medium": 900,
    "long": 1200,
}
STYLE_TO_ITEM_TIMEOUT_SECONDS = {
    "short": 45,
    "medium": 60,
    "long": 90,
}
AI_TOPIC_ALIASES = {
    "ai": [
        "ai",
        "artificial intelligence",
        "人工智能",
        "ai agent",
        "ai agents",
        "agent",
        "agents",
        "agentic",
        "智能体",
        "llm",
        "llms",
        "大模型",
        "模型",
        "openai",
        "anthropic",
        "claude",
        "gpt",
        "gemini",
        "llama",
        "grok",
        "cursor",
        "codex",
    ],
    "人工智能": [
        "人工智能",
        "ai",
        "artificial intelligence",
        "智能体",
        "agent",
        "agents",
        "agentic",
        "llm",
        "大模型",
        "模型",
        "openai",
        "anthropic",
        "claude",
        "gpt",
        "gemini",
        "llama",
        "grok",
        "cursor",
        "codex",
    ],
    "artificial intelligence": [
        "artificial intelligence",
        "ai",
        "人工智能",
        "agent",
        "agents",
        "agentic",
        "智能体",
        "llm",
        "大模型",
        "模型",
        "openai",
        "anthropic",
        "claude",
        "gpt",
        "gemini",
        "llama",
        "grok",
        "cursor",
        "codex",
    ],
    "ai相关": [
        "ai",
        "人工智能",
        "artificial intelligence",
        "agent",
        "agents",
        "agentic",
        "智能体",
        "llm",
        "大模型",
        "模型",
        "openai",
        "anthropic",
        "claude",
        "gpt",
        "gemini",
        "llama",
        "grok",
        "cursor",
        "codex",
    ],
    "ai 相关": [
        "ai",
        "人工智能",
        "artificial intelligence",
        "agent",
        "agents",
        "agentic",
        "智能体",
        "llm",
        "大模型",
        "模型",
        "openai",
        "anthropic",
        "claude",
        "gpt",
        "gemini",
        "llama",
        "grok",
        "cursor",
        "codex",
    ],
}
DAY_TO_CRON = {
    "sun": "0",
    "mon": "1",
    "tue": "2",
    "wed": "3",
    "thu": "4",
    "fri": "5",
    "sat": "6",
}


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def current_script_path() -> str:
    return str(Path(__file__).resolve())


def user_home() -> Path:
    override = os.getenv("FOLLOW_SCOUTX_HOME", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return Path.home() / ".follow_scoutx"


def profile_path() -> Path:
    return user_home() / "profile.json"


def state_path() -> Path:
    return user_home() / "state.json"


def prompt_sync_state_path() -> Path:
    return user_home() / "prompt_sync_state.json"


def local_service_config_path() -> Path:
    return user_home() / "service.json"


def prompts_dir() -> Path:
    return user_home() / "prompts"


def prompt_backups_dir() -> Path:
    return prompts_dir() / "backups"


def bundled_prompts_dir() -> Path:
    return skill_root() / "prompts"


def service_config_path() -> Path:
    return skill_root() / "service.json"


def default_service_config() -> dict[str, Any]:
    return {
        "feed_url": DEFAULT_FEED_URL,
        "scoutx_feed_url": DEFAULT_FEED_URL,
        "x_feed_url": DEFAULT_X_FEED_URL,
        "podcast_feed_url": DEFAULT_PODCAST_FEED_URL,
        "meta_url": "",
        "timeout_seconds": DEFAULT_TIMEOUT_SECONDS,
    }


def with_service_defaults(config: dict[str, Any]) -> dict[str, Any]:
    merged = default_service_config()
    merged.update(config)
    scoutx_feed_url = str(merged.get("scoutx_feed_url") or merged.get("feed_url") or DEFAULT_FEED_URL)
    merged["feed_url"] = str(merged.get("feed_url") or scoutx_feed_url)
    merged["scoutx_feed_url"] = scoutx_feed_url
    merged["x_feed_url"] = str(merged.get("x_feed_url") or DEFAULT_X_FEED_URL)
    merged["podcast_feed_url"] = str(merged.get("podcast_feed_url") or DEFAULT_PODCAST_FEED_URL)
    merged["timeout_seconds"] = int(merged.get("timeout_seconds") or DEFAULT_TIMEOUT_SECONDS)
    return merged


def load_service_config() -> dict[str, Any]:
    local_path = local_service_config_path()
    if local_path.exists():
        return with_service_defaults(json.loads(local_path.read_text(encoding="utf-8")))

    bundled_path = service_config_path()
    if bundled_path.exists():
        return with_service_defaults(json.loads(bundled_path.read_text(encoding="utf-8")))

    return default_service_config()


def is_placeholder_feed_url(url: str | None) -> bool:
    if not url:
        return True
    parsed = urllib.parse.urlparse(url)
    host = (parsed.netloc or "").lower()
    return host.endswith(".example.com") or host == "example.com"


def ensure_real_feed_url(url: str | None) -> str:
    if is_placeholder_feed_url(url):
        raise SystemExit(
            "Follow ScoutX operator setup incomplete: the bundled feed URL is still a placeholder. "
            "Update the distributed skill package's service.json or run configure-service on this installation. "
            "Normal end users should not be asked to provide a feed URL."
        )
    return str(url)


def save_service_config(config: dict[str, Any]) -> None:
    save_json(local_service_config_path(), config)


def default_profile() -> dict[str, Any]:
    now = utcnow_iso()
    return {
        "version": PROFILE_VERSION,
        "created_at": now,
        "updated_at": now,
        "schedule": {
            "frequency": "daily",
            "time": "09:00",
            "days": ["mon"],
        },
        "delivery": {
            "channel": "in_chat",
            "target": "",
        },
        "preferences": {
            "language": "zh-CN",
            "source_mode": "scoutx",
            "source_types": ["scoutx"],
            "topics": [],
            "keywords_include": [],
            "keywords_exclude": [],
            "preferred_sources": [],
            "max_items": 8,
            "max_first_party_items": None,
            "max_scoutx_items": None,
        },
        "style": {
            "length": "short",
            "tone": "clear",
        },
    }


def default_state() -> dict[str, Any]:
    return {
        "last_preview_at": None,
        "last_feed_fetch_at": None,
        "last_digest_item_ids": [],
    }


def default_prompt_sync_state() -> dict[str, Any]:
    return {
        "managed_hashes": {},
        "last_synced_at": None,
    }


def load_json(path: Path, fallback: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return json.loads(json.dumps(fallback))
    return json.loads(path.read_text(encoding="utf-8"))


def merge_missing_defaults(payload: dict[str, Any], defaults: dict[str, Any]) -> dict[str, Any]:
    for key, value in defaults.items():
        if key not in payload:
            payload[key] = json.loads(json.dumps(value))
            continue
        if isinstance(payload[key], dict) and isinstance(value, dict):
            merge_missing_defaults(payload[key], value)
    return payload


def save_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prompt_content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def backup_prompt_file(path: Path) -> Path:
    prompt_backups_dir().mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = prompt_backups_dir() / f"{path.stem}.{timestamp}.bak{path.suffix}"
    suffix = 1
    while backup_path.exists():
        backup_path = prompt_backups_dir() / f"{path.stem}.{timestamp}.{suffix}.bak{path.suffix}"
        suffix += 1
    shutil.copyfile(path, backup_path)
    return backup_path


def sync_bundled_prompts() -> dict[str, Any]:
    sync_state = merge_missing_defaults(
        load_json(prompt_sync_state_path(), default_prompt_sync_state()),
        default_prompt_sync_state(),
    )
    managed_hashes = {
        str(name): str(value)
        for name, value in (sync_state.get("managed_hashes") or {}).items()
        if str(name).strip() and str(value).strip()
    }
    installed: list[str] = []
    updated: list[str] = []
    preserved_custom: list[str] = []
    backed_up: list[str] = []

    for source in bundled_prompts_dir().glob("*.md"):
        filename = source.name
        bundled_text = source.read_text(encoding="utf-8")
        bundled_hash = prompt_content_hash(bundled_text)
        target = prompts_dir() / filename
        managed_hash = managed_hashes.get(filename)

        if not target.exists():
            target.write_text(bundled_text, encoding="utf-8")
            managed_hashes[filename] = bundled_hash
            installed.append(filename)
            continue

        local_text = target.read_text(encoding="utf-8")
        local_hash = prompt_content_hash(local_text)
        if local_hash == bundled_hash:
            managed_hashes[filename] = bundled_hash
            continue

        if managed_hash and local_hash != managed_hash:
            preserved_custom.append(filename)
            continue

        backup_path = backup_prompt_file(target)
        target.write_text(bundled_text, encoding="utf-8")
        managed_hashes[filename] = bundled_hash
        backed_up.append(str(backup_path))
        updated.append(filename)

    sync_state["managed_hashes"] = managed_hashes
    sync_state["last_synced_at"] = utcnow_iso()
    save_json(prompt_sync_state_path(), sync_state)
    return {
        "installed": installed,
        "updated": updated,
        "preserved_custom": preserved_custom,
        "backed_up": backed_up,
        "last_synced_at": sync_state["last_synced_at"],
    }


def ensure_local_files() -> dict[str, Any]:
    home = user_home()
    home.mkdir(parents=True, exist_ok=True)
    prompts_dir().mkdir(parents=True, exist_ok=True)

    if not profile_path().exists():
        save_json(profile_path(), default_profile())
    if not state_path().exists():
        save_json(state_path(), default_state())
    if not local_service_config_path().exists():
        save_service_config(load_service_config())
    return sync_bundled_prompts()


def load_profile() -> dict[str, Any]:
    ensure_local_files()
    profile = load_json(profile_path(), default_profile())
    return merge_missing_defaults(profile, default_profile())


def save_profile(profile: dict[str, Any]) -> None:
    profile["version"] = PROFILE_VERSION
    profile["updated_at"] = utcnow_iso()
    save_json(profile_path(), profile)


def load_state() -> dict[str, Any]:
    ensure_local_files()
    return load_json(state_path(), default_state())


def save_state(state: dict[str, Any]) -> None:
    save_json(state_path(), state)


def load_prompt_texts() -> dict[str, str]:
    ensure_local_files()
    mapping = {
        "digest_intro": "digest_intro.md",
        "summarize_content": "summarize_content.md",
        "summarize_tweets": "summarize_tweets.md",
        "summarize_podcast": "summarize_podcast.md",
        "translate": "translate.md",
    }
    prompts: dict[str, str] = {}
    for key, filename in mapping.items():
        prompt_path = prompts_dir() / filename
        prompts[key] = prompt_path.read_text(encoding="utf-8").strip()
    return prompts


def split_csv(value: str | None) -> list[str] | None:
    if value is None:
        return None
    items = [part.strip() for part in value.split(",")]
    return [item for item in items if item]


def normalize_source_type(value: str) -> str | None:
    key = value.strip().lower().replace("-", "_")
    if key in SOURCE_TYPE_ALIASES:
        return SOURCE_TYPE_ALIASES[key]
    if key == "first_party":
        return None
    return key if key in SOURCE_TYPES else None


def normalize_source_types(values: list[str] | None, *, strict: bool = False) -> list[str]:
    if not values:
        return ["scoutx"]
    normalized: list[str] = []
    invalid: list[str] = []
    for value in values:
        source_type = normalize_source_type(value)
        if source_type and source_type not in normalized:
            normalized.append(source_type)
        elif not source_type:
            invalid.append(value)
    if invalid and strict:
        expected = ", ".join(SOURCE_TYPES)
        invalid_text = ", ".join(invalid)
        raise ValueError(f"Unknown source type(s): {invalid_text}. Expected one of: {expected}.")
    return normalized or ["scoutx"]


def source_types_for_mode(mode: str | None) -> list[str]:
    if not mode:
        return ["scoutx"]
    key = mode.strip().lower().replace(" ", "_")
    return list(SOURCE_MODE_TO_TYPES.get(key, ["scoutx"]))


def profile_source_types(profile: dict[str, Any]) -> list[str]:
    preferences = profile.get("preferences") or {}
    configured = preferences.get("source_types")
    if configured:
        return normalize_source_types([str(value) for value in configured])
    return source_types_for_mode(str(preferences.get("source_mode") or "scoutx"))


def selected_message_group_ids(profile: dict[str, Any], message_group: str | None = "all") -> list[str]:
    selected_sources = set(profile_source_types(profile))
    group_ids = [
        group_id
        for group_id in MESSAGE_GROUP_ORDER
        if any(source_type in selected_sources for source_type in MESSAGE_GROUPS[group_id])
    ]
    if message_group and message_group != "all":
        return [group_id for group_id in group_ids if group_id == message_group]
    return group_ids


def source_types_for_message_group(profile: dict[str, Any], message_group: str | None = "all") -> list[str]:
    selected_sources = profile_source_types(profile)
    if not message_group or message_group == "all":
        return selected_sources
    allowed_sources = set(MESSAGE_GROUPS.get(message_group, ()))
    return [source_type for source_type in selected_sources if source_type in allowed_sources]


def group_limit_key(group_id: str) -> str:
    return MESSAGE_GROUP_LIMIT_KEYS[group_id]


def configured_group_limits(profile: dict[str, Any]) -> dict[str, int]:
    preferences = profile.get("preferences") or {}
    group_ids = selected_message_group_ids(profile, "all")
    if not group_ids:
        return {}

    total_limit = max(0, int(preferences.get("max_items", 8) or 0))
    base_limit = total_limit // len(group_ids)
    remainder = total_limit % len(group_ids)
    limits = {
        group_id: base_limit + (1 if index < remainder else 0)
        for index, group_id in enumerate(group_ids)
    }

    for group_id in group_ids:
        key = group_limit_key(group_id)
        explicit_limit = preferences.get(key)
        if explicit_limit is not None:
            limits[group_id] = max(0, int(explicit_limit))
    return limits


def message_group_label(group_id: str, language: str) -> str:
    if group_id == "first_party":
        if language == "en":
            return "First-party Sources (X / Podcasts)"
        if language == "bilingual":
            return "First-party Sources / 一手信息源（X 平台 / 播客）"
        return "一手信息源（X 平台 / 播客）"
    if language == "en":
        return "ScoutX Curated Media"
    if language == "bilingual":
        return "ScoutX Curated Media / ScoutX 优质自媒体信息源"
    return "ScoutX 优质自媒体信息源"


def update_profile_from_args(profile: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.frequency:
        profile["schedule"]["frequency"] = args.frequency
    if args.time:
        profile["schedule"]["time"] = args.time
    if args.days is not None:
        profile["schedule"]["days"] = split_csv(args.days) or []

    if args.language:
        profile["preferences"]["language"] = args.language
    if args.source_mode:
        source_types = source_types_for_mode(args.source_mode)
        profile["preferences"]["source_mode"] = args.source_mode
        profile["preferences"]["source_types"] = source_types
    if args.source_types is not None:
        try:
            source_types = normalize_source_types(split_csv(args.source_types) or [], strict=True)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        profile["preferences"]["source_types"] = source_types
        if source_types == ["scoutx"]:
            profile["preferences"]["source_mode"] = "scoutx"
        elif source_types == ["x", "podcast"]:
            profile["preferences"]["source_mode"] = "first_party"
        elif source_types == ["scoutx", "x", "podcast"]:
            profile["preferences"]["source_mode"] = "mixed"
        else:
            profile["preferences"]["source_mode"] = "custom"
    if args.topics is not None:
        profile["preferences"]["topics"] = split_csv(args.topics) or []
    if args.keywords_include is not None:
        profile["preferences"]["keywords_include"] = split_csv(args.keywords_include) or []
    if args.keywords_exclude is not None:
        profile["preferences"]["keywords_exclude"] = split_csv(args.keywords_exclude) or []
    if args.preferred_sources is not None:
        profile["preferences"]["preferred_sources"] = split_csv(args.preferred_sources) or []
    if args.max_items is not None:
        profile["preferences"]["max_items"] = args.max_items
    if arg_value(args, "max_first_party_items") is not None:
        profile["preferences"]["max_first_party_items"] = args.max_first_party_items
    if arg_value(args, "max_scoutx_items") is not None:
        profile["preferences"]["max_scoutx_items"] = args.max_scoutx_items

    if args.delivery_channel:
        profile["delivery"]["channel"] = args.delivery_channel
    if args.delivery_target is not None:
        profile["delivery"]["target"] = args.delivery_target

    if args.length:
        profile["style"]["length"] = args.length
    if args.tone:
        profile["style"]["tone"] = args.tone

    return profile


def summary_char_budget(profile: dict[str, Any]) -> int:
    style = str(profile.get("style", {}).get("length") or "medium").strip().lower()
    return STYLE_TO_SUMMARY_BUDGET.get(style, DEFAULT_SUMMARY_BUDGET_CHARS)


def item_timeout_seconds(profile: dict[str, Any]) -> int:
    style = str(profile.get("style", {}).get("length") or "medium").strip().lower()
    return STYLE_TO_ITEM_TIMEOUT_SECONDS.get(style, 60)


def normalize_feed_item(raw: dict[str, Any]) -> dict[str, Any]:
    source_values = raw.get("sources") or []
    sources = [str(value).strip() for value in source_values if str(value).strip()]
    return {
        "content_id": str(raw.get("content_id") or raw.get("id") or raw.get("url") or "").strip(),
        "source_type": "scoutx",
        "source_label": SOURCE_TYPE_LABELS["scoutx"],
        "title": html.unescape(str(raw.get("title") or "").strip()),
        "summary": str(raw.get("summary") or raw.get("summary_text") or raw.get("description") or raw.get("content") or "").strip(),
        "url": str(raw.get("url") or raw.get("canonical_url") or "").strip(),
        "published_at": str(raw.get("published_at") or raw.get("publishedAt") or "").strip(),
        "sources": sources or [SOURCE_TYPE_LABELS["scoutx"]],
        "tags": [str(value).strip() for value in raw.get("tags") or [] if str(value).strip()],
        "metadata": {},
    }


def normalize_x_feed_items(feed_payload: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for account in feed_payload.get("x") or []:
        name = str(account.get("name") or account.get("handle") or "Unknown").strip()
        handle = str(account.get("handle") or "").strip()
        for tweet in account.get("tweets") or []:
            tweet_id = str(tweet.get("id") or tweet.get("url") or "").strip()
            text = str(tweet.get("text") or "").strip()
            if not text:
                continue
            title_prefix = f"@{handle}" if handle else name
            title = f"{title_prefix}: {text.splitlines()[0][:120]}"
            items.append(
                {
                    "content_id": f"x:{tweet_id}" if tweet_id else f"x:{handle}:{tweet.get('createdAt') or tweet.get('url')}",
                    "source_type": "x",
                    "source_label": SOURCE_TYPE_LABELS["x"],
                    "title": title,
                    "summary": text,
                    "url": str(tweet.get("url") or "").strip(),
                    "published_at": str(tweet.get("createdAt") or tweet.get("published_at") or "").strip(),
                    "sources": [f"X / {name}", f"@{handle}" if handle else name],
                    "tags": ["x"],
                    "metadata": {
                        "name": name,
                        "handle": handle,
                        "likes": tweet.get("likes"),
                        "retweets": tweet.get("retweets"),
                        "replies": tweet.get("replies"),
                        "is_quote": tweet.get("isQuote"),
                    },
                }
            )
    return items


def normalize_podcast_feed_items(feed_payload: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for episode in feed_payload.get("podcasts") or []:
        name = str(episode.get("name") or "Unknown Podcast").strip()
        title = html.unescape(str(episode.get("title") or "Untitled podcast episode").strip())
        content = str(
            episode.get("transcript")
            or episode.get("content")
            or episode.get("summary")
            or episode.get("description")
            or ""
        ).strip()
        items.append(
            {
                "content_id": f"podcast:{episode.get('guid') or episode.get('url') or title}",
                "source_type": "podcast",
                "source_label": SOURCE_TYPE_LABELS["podcast"],
                "title": title,
                "summary": content,
                "url": str(episode.get("url") or "").strip(),
                "published_at": str(episode.get("publishedAt") or episode.get("published_at") or "").strip(),
                "sources": [f"Podcast / {name}"],
                "tags": ["podcast"],
                "metadata": {
                    "name": name,
                    "guid": episode.get("guid"),
                },
            }
        )
    return items


def normalize_items_for_source(source_type: str, feed_payload: dict[str, Any]) -> list[dict[str, Any]]:
    if source_type == "x":
        return normalize_x_feed_items(feed_payload)
    if source_type == "podcast":
        return normalize_podcast_feed_items(feed_payload)
    return [normalize_feed_item(item) for item in feed_payload.get("items") or []]


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_paragraphs(text: str) -> list[str]:
    normalized = normalize_whitespace(text)
    if not normalized:
        return []
    return [part.strip() for part in re.split(r"\n\s*\n", normalized) if part.strip()]


def split_sentences(text: str) -> list[str]:
    normalized = normalize_whitespace(text)
    if not normalized:
        return []
    parts = re.split(r"(?<=[。！？!?；;])\s*", normalized)
    return [part.strip() for part in parts if part.strip()]


def strip_trailing_noise(paragraphs: list[str]) -> list[str]:
    noise_patterns = [
        "本文来自",
        "参考资料",
        "责任编辑",
        "编辑：",
        "作者：",
        "文章来源",
    ]
    cleaned = list(paragraphs)
    while cleaned and any(pattern in cleaned[-1] for pattern in noise_patterns):
        cleaned.pop()
    return cleaned


def dedupe_sentences(sentences: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for sentence in sentences:
        key = re.sub(r"\s+", "", sentence)
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(sentence)
    return deduped


def sentence_priority(sentence: str) -> int:
    keywords = [
        "因此",
        "所以",
        "综上",
        "总之",
        "最终",
        "结论是",
        "认为",
        "指出",
        "提出",
        "强调",
        "观点是",
        "数据显示",
        "结果表明",
        "研究发现",
        "超过",
        "增长到",
        "关键",
        "重要",
        "核心",
        "值得注意的是",
    ]
    score = 0
    for keyword in keywords:
        if keyword in sentence:
            score += 2
    if re.search(r"\d", sentence):
        score += 1
    if re.search(r"%|亿美元|万亿|million|billion|stars?|GPU|API|Beta|Alpha", sentence, re.IGNORECASE):
        score += 1
    return score


def compress_summary_text(text: str, *, char_budget: int = DEFAULT_SUMMARY_BUDGET_CHARS) -> str:
    paragraphs = strip_trailing_noise(split_paragraphs(text))
    if not paragraphs:
        return ""

    if len("".join(paragraphs)) <= char_budget:
        return "\n\n".join(paragraphs)

    first_paragraph = paragraphs[0]
    last_paragraph = paragraphs[-1] if len(paragraphs) > 1 else ""
    middle_paragraphs = paragraphs[1:-1] if len(paragraphs) > 2 else []

    middle_sentences = dedupe_sentences(
        [sentence for paragraph in middle_paragraphs for sentence in split_sentences(paragraph)]
    )
    selected_middle = [sentence for sentence in middle_sentences if sentence_priority(sentence) > 0]
    if not selected_middle:
        selected_middle = middle_sentences[:8]

    assembled_parts: list[str] = [first_paragraph]
    if selected_middle:
        assembled_parts.append(" ".join(selected_middle))
    if last_paragraph and last_paragraph != first_paragraph:
        assembled_parts.append(last_paragraph)

    result = "\n\n".join(part for part in assembled_parts if part).strip()
    if len(result) <= char_budget:
        return result

    parts = [first_paragraph]
    if last_paragraph and last_paragraph != first_paragraph:
        remaining_budget = max(char_budget - len(first_paragraph) - len(last_paragraph) - 4, 0)
    else:
        remaining_budget = max(char_budget - len(first_paragraph) - 2, 0)

    if remaining_budget > 0 and selected_middle:
        middle_text = ""
        for sentence in selected_middle:
            candidate = f"{middle_text} {sentence}".strip()
            if len(candidate) > remaining_budget:
                break
            middle_text = candidate
        if middle_text:
            parts.append(middle_text)

    if last_paragraph and last_paragraph != first_paragraph:
        parts.append(last_paragraph)

    result = "\n\n".join(part for part in parts if part).strip()
    if len(result) <= char_budget:
        return result

    return result[:char_budget].rstrip()


def compress_transcript_text(text: str, *, char_budget: int = DEFAULT_SUMMARY_BUDGET_CHARS) -> str:
    paragraphs = split_paragraphs(text)
    if not paragraphs:
        return ""
    selected: list[str] = []
    current_len = 0
    for paragraph in paragraphs:
        candidate_len = current_len + len(paragraph) + (2 if selected else 0)
        if candidate_len > char_budget:
            remaining = char_budget - current_len - (2 if selected else 0)
            if remaining > 80:
                selected.append(paragraph[:remaining].rstrip())
            break
        selected.append(paragraph)
        current_len = candidate_len
    return "\n\n".join(selected).strip()


def compress_item_summary(item: dict[str, Any], *, char_budget: int = DEFAULT_SUMMARY_BUDGET_CHARS) -> str:
    summary = str(item.get("summary") or "")
    if item.get("source_type") == "podcast":
        return compress_transcript_text(summary, char_budget=char_budget)
    return compress_summary_text(summary, char_budget=char_budget)


def item_primary_text(item: dict[str, Any]) -> str:
    return "\n".join(
        [
            str(item.get("title") or ""),
            str(item.get("summary") or ""),
        ]
    ).lower()


def item_metadata_text(item: dict[str, Any]) -> str:
    return "\n".join(
        [
            str(item.get("source_type") or ""),
            str(item.get("source_label") or ""),
            " ".join(item.get("sources") or []),
            " ".join(item.get("tags") or []),
        ]
    ).lower()


def split_filter_terms(values: list[str]) -> list[str]:
    terms: list[str] = []
    for value in values:
        normalized = str(value).strip().lower()
        if not normalized:
            continue
        parts = re.split(r"[/|｜、，,]+", normalized)
        terms.extend(part.strip() for part in parts if part.strip())
    return list(dict.fromkeys(terms))


def expand_include_terms(values: list[str]) -> list[str]:
    expanded: list[str] = []
    for term in split_filter_terms(values):
        expanded.extend(AI_TOPIC_ALIASES.get(term, [term]))
    return list(dict.fromkeys(expanded))


def term_matches_haystack(term: str, haystack: str) -> bool:
    normalized = term.strip().lower()
    if not normalized:
        return False
    if re.fullmatch(r"[a-z0-9][a-z0-9 .:+_-]*", normalized):
        escaped = re.escape(normalized).replace(r"\ ", r"\s+")
        pattern = rf"(?<![a-z0-9]){escaped}(?![a-z0-9])"
        return re.search(pattern, haystack) is not None
    return normalized in haystack


def item_matches_profile(item: dict[str, Any], profile: dict[str, Any]) -> bool:
    preferences = profile["preferences"]
    include_terms = expand_include_terms(preferences.get("topics", []) + preferences.get("keywords_include", []))
    exclude_terms = split_filter_terms(preferences.get("keywords_exclude", []))
    preferred_sources = {value.lower() for value in preferences.get("preferred_sources", [])}
    item_sources = {value.lower() for value in item.get("sources", [])}
    primary_haystack = item_primary_text(item)
    metadata_haystack = item_metadata_text(item)
    full_haystack = "\n".join(part for part in [primary_haystack, metadata_haystack] if part).strip()

    if preferred_sources and not (preferred_sources & item_sources):
        return False
    if include_terms and not any(term_matches_haystack(term, primary_haystack) for term in include_terms):
        return False
    if exclude_terms and any(term_matches_haystack(term, full_haystack) for term in exclude_terms):
        return False
    return True


def service_feed_url(service_config: dict[str, Any], source_type: str) -> str:
    if source_type == "x":
        return str(service_config.get("x_feed_url") or DEFAULT_X_FEED_URL)
    if source_type == "podcast":
        return str(service_config.get("podcast_feed_url") or DEFAULT_PODCAST_FEED_URL)
    return str(service_config.get("scoutx_feed_url") or service_config.get("feed_url") or DEFAULT_FEED_URL)


def fetch_feed(
    *,
    source_type: str = "scoutx",
    feed_url: str | None = None,
    feed_file: str | None = None,
) -> dict[str, Any]:
    if feed_file:
        return json.loads(Path(feed_file).read_text(encoding="utf-8"))

    service_config = load_service_config()
    env_var = SOURCE_TYPE_ENV_VARS.get(source_type, "FOLLOW_SCOUTX_FEED_URL")
    target_url = feed_url or os.getenv(env_var, service_feed_url(service_config, source_type))
    target_url = ensure_real_feed_url(target_url)
    timeout = int(
        os.getenv(
            "FOLLOW_SCOUTX_TIMEOUT_SECONDS",
            str(service_config.get("timeout_seconds") or DEFAULT_TIMEOUT_SECONDS),
        )
    )
    request = urllib.request.Request(
        url=target_url,
        headers={
            "Accept": "application/json",
            "User-Agent": os.getenv("FOLLOW_SCOUTX_USER_AGENT", DEFAULT_USER_AGENT),
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code} {exc.reason}: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Failed to fetch central feed: {exc.reason}") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Central feed returned invalid JSON: {raw}") from exc


def arg_value(args: argparse.Namespace, name: str) -> Any:
    return getattr(args, name, None)


def allow_partial_feed_results(args: argparse.Namespace) -> bool:
    if bool(arg_value(args, "allow_partial_feeds")):
        return True
    env_value = os.getenv("FOLLOW_SCOUTX_ALLOW_PARTIAL_FEEDS", "").strip().lower()
    if env_value in {"0", "false", "no"}:
        return False
    return True


def fetch_selected_feed_payload(profile: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    message_group = arg_value(args, "message_group") or "all"
    source_types = source_types_for_message_group(profile, message_group)
    feeds: dict[str, Any] = {}
    errors: list[str] = []

    if not source_types:
        raise SystemExit(f"No sources are selected for message group: {message_group}.")

    for source_type in source_types:
        feed_url = arg_value(args, "feed_url") if source_type == "scoutx" else arg_value(args, f"{source_type}_feed_url")
        feed_file = arg_value(args, "feed_file") if source_type == "scoutx" else arg_value(args, f"{source_type}_feed_file")
        if arg_value(args, "feed_file") and len(source_types) == 1 and not feed_file:
            feed_file = arg_value(args, "feed_file")
        try:
            feeds[source_type] = fetch_feed(source_type=source_type, feed_url=feed_url, feed_file=feed_file)
        except (SystemExit, OSError, json.JSONDecodeError) as exc:
            errors.append(f"{source_type}: {exc}")

    if not feeds:
        raise SystemExit("; ".join(errors) or "No selected feeds could be loaded.")
    if errors and not allow_partial_feed_results(args):
        error_text = "; ".join(errors)
        raise SystemExit(
            "Failed to load all selected feeds. "
            "Partial feed results are disabled for this run.\n"
            f"{error_text}\n"
            "Rerun with --allow-partial-feeds to continue with partial results."
        )

    generated_at = utcnow_iso()
    for payload in feeds.values():
        generated_at = str(payload.get("generated_at") or payload.get("generatedAt") or generated_at)
        if generated_at:
            break

    return {
        "status": "partial" if errors else "ok",
        "generated_at": generated_at,
        "source_types": source_types,
        "feeds": feeds,
        "loaded_source_types": list(feeds.keys()),
        "failed_source_types": [
            source_type
            for source_type in source_types
            if source_type not in feeds
        ],
        "errors": errors,
    }


def limit_items_by_source(items: list[dict[str, Any]], source_types: list[str], limit: int) -> list[dict[str, Any]]:
    if len(source_types) <= 1:
        return items[:limit]

    buckets = {
        source_type: [item for item in items if item.get("source_type") == source_type]
        for source_type in source_types
    }
    selected: list[dict[str, Any]] = []
    index = 0
    while len(selected) < limit:
        added = False
        for source_type in source_types:
            bucket = buckets.get(source_type) or []
            if index < len(bucket):
                selected.append(bucket[index])
                added = True
                if len(selected) >= limit:
                    break
        if not added:
            break
        index += 1
    return selected


def normalize_feed_payload_items(profile: dict[str, Any], feed_payload: dict[str, Any]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    if "feeds" in feed_payload:
        for source_type in feed_payload.get("source_types") or profile_source_types(profile):
            normalized.extend(normalize_items_for_source(source_type, feed_payload.get("feeds", {}).get(source_type) or {}))
    else:
        source_types = profile_source_types(profile)
        if "x" in feed_payload and "x" in source_types:
            normalized.extend(normalize_items_for_source("x", feed_payload))
        if "podcasts" in feed_payload and "podcast" in source_types:
            normalized.extend(normalize_items_for_source("podcast", feed_payload))
        if "items" in feed_payload and "scoutx" in source_types:
            normalized.extend(normalize_items_for_source("scoutx", feed_payload))
    return normalized


def build_digest_groups(
    profile: dict[str, Any],
    feed_payload: dict[str, Any],
    *,
    message_group: str | None = "all",
) -> list[dict[str, Any]]:
    normalized = normalize_feed_payload_items(profile, feed_payload)
    matched = [item for item in normalized if item_matches_profile(item, profile)]
    limits = configured_group_limits(profile)
    groups: list[dict[str, Any]] = []

    for group_id in selected_message_group_ids(profile, message_group):
        group_source_types = [
            source_type
            for source_type in MESSAGE_GROUPS[group_id]
            if source_type in profile_source_types(profile)
        ]
        group_limit = limits.get(group_id, 0)
        group_items = [
            item
            for item in matched
            if item.get("source_type") in group_source_types
        ]
        groups.append(
            {
                "group_id": group_id,
                "label": message_group_label(group_id, profile["preferences"].get("language", "zh-CN")),
                "source_types": group_source_types,
                "limit": group_limit,
                "items": limit_items_by_source(group_items, group_source_types, group_limit) if group_limit > 0 else [],
            }
        )
    return groups


def flatten_digest_groups(groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item for group in groups for item in group.get("items", [])]


def build_preview_items(
    profile: dict[str, Any],
    feed_payload: dict[str, Any],
    *,
    message_group: str | None = "all",
) -> list[dict[str, Any]]:
    return flatten_digest_groups(build_digest_groups(profile, feed_payload, message_group=message_group))


def digest_copy(language: str) -> dict[str, str]:
    if language == "zh-CN":
        return {
            "title": "Follow ScoutX 摘要",
            "empty": "No matching items found.",
            "partial": "本次为降级结果：部分信息源拉取失败，仅投递可用内容。",
            "failed_sources": "Failed sources",
            "generated_at": "Generated at",
            "items": "Items",
            "source": "Source",
            "published": "Published",
            "link": "Link",
        }
    if language == "bilingual":
        return {
            "title": "Follow ScoutX Digest / 摘要",
            "empty": "No matching items found.",
            "partial": "Partial result / 部分降级：some selected feeds failed, so only available content is delivered.",
            "failed_sources": "Failed sources",
            "generated_at": "Generated at",
            "items": "Items",
            "source": "Source",
            "published": "Published",
            "link": "Link",
        }
    return {
        "title": "Follow ScoutX Digest",
        "empty": "No matching items found.",
        "partial": "Partial result: some selected feeds failed, so only available content is delivered.",
        "failed_sources": "Failed sources",
        "generated_at": "Generated at",
        "items": "Items",
        "source": "Source",
        "published": "Published",
        "link": "Link",
    }


def feed_payload_status(feed_payload: dict[str, Any]) -> str:
    return "partial" if feed_payload.get("errors") else "ok"


def partial_warning_lines(profile: dict[str, Any], feed_payload: dict[str, Any]) -> list[str]:
    if feed_payload_status(feed_payload) != "partial":
        return []
    copy = digest_copy(profile["preferences"].get("language", "zh-CN"))
    failed_sources = feed_payload.get("failed_source_types") or []
    errors = feed_payload.get("errors") or []
    lines = [copy["partial"]]
    if failed_sources:
        lines.append(f"{copy['failed_sources']}: {', '.join(str(value) for value in failed_sources)}")
    if errors:
        lines.extend(str(value) for value in errors)
    return lines


def digest_title(profile: dict[str, Any], *, part_index: int | None = None, part_count: int | None = None) -> str:
    language = profile["preferences"].get("language", "zh-CN")
    title = digest_copy(language)["title"]
    if not part_index or not part_count or part_count <= 1:
        return title
    if language == "en":
        return f"{title} (Part {part_index}/{part_count})"
    if language == "bilingual":
        return f"{title} (Part {part_index}/{part_count}) / 第 {part_index}/{part_count} 条"
    return f"{title}（第 {part_index}/{part_count} 条）"


def render_digest_item_block(
    profile: dict[str, Any],
    item: dict[str, Any],
    *,
    index: int,
) -> str:
    language = profile["preferences"].get("language", "zh-CN")
    copy = digest_copy(language)
    per_item_budget = summary_char_budget(profile)
    source = item["sources"][0] if item["sources"] else "unknown"
    lines = [f"{index}. {item['title']}"]
    summary = compress_item_summary(item, char_budget=per_item_budget) if item["summary"] else ""
    if summary:
        lines.append(summary)
    lines.append(f"{copy['source']}: {source}")
    if item["published_at"]:
        lines.append(f"{copy['published']}: {item['published_at']}")
    if item["url"]:
        lines.append(f"{copy['link']}: {item['url']}")
    return "\n".join(lines).strip()


def split_oversized_block(block: str, limit: int) -> list[str]:
    if len(block) <= limit:
        return [block]

    pieces: list[str] = []
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", block) if part.strip()]
    current = ""
    for paragraph in paragraphs or [block]:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if current and len(candidate) > limit:
            pieces.append(current)
            current = paragraph
            continue
        if len(candidate) <= limit:
            current = candidate
            continue

        lines = [line.rstrip() for line in paragraph.splitlines() if line.strip()]
        if current:
            pieces.append(current)
            current = ""
        current_line_block = ""
        for line in lines or [paragraph]:
            candidate_line_block = f"{current_line_block}\n{line}".strip() if current_line_block else line
            if current_line_block and len(candidate_line_block) > limit:
                pieces.append(current_line_block)
                current_line_block = line
                continue
            if len(candidate_line_block) <= limit:
                current_line_block = candidate_line_block
                continue

            if current_line_block:
                pieces.append(current_line_block)
                current_line_block = ""
            start = 0
            while start < len(line):
                end = min(start + limit, len(line))
                pieces.append(line[start:end].rstrip())
                start = end
        if current_line_block:
            pieces.append(current_line_block)
    if current:
        pieces.append(current)
    return [piece for piece in pieces if piece.strip()]


def digest_metadata_prefixes() -> tuple[str, ...]:
    prefixes: list[str] = []
    for language in ("zh-CN", "en", "bilingual"):
        copy = digest_copy(language)
        prefixes.extend(
            [
                f"{copy['source']}:",
                f"{copy['published']}:",
                f"{copy['link']}:",
            ]
        )
    return tuple(dict.fromkeys(prefixes))


def is_digest_metadata_line(line: str) -> bool:
    return line.startswith(digest_metadata_prefixes())


def digest_item_continuation_title(profile: dict[str, Any], title: str) -> str:
    language = profile["preferences"].get("language", "zh-CN")
    if language == "en":
        return f"{title} (cont.)"
    if language == "bilingual":
        return f"{title} (cont.) / 续"
    return f"{title}（续）"


def split_digest_item_block(
    profile: dict[str, Any],
    block: str,
    limit: int,
    *,
    section_header: str | None = None,
) -> list[str]:
    text = block.strip()
    if not text:
        return []
    if len(text) <= limit and not section_header:
        return [text]

    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    if not lines:
        return [f"{section_header}\n\n{text}".strip()] if section_header else [text]

    metadata_lines: list[str] = []
    body_lines = lines[:]
    while body_lines and is_digest_metadata_line(body_lines[-1]):
        metadata_lines.insert(0, body_lines.pop())

    title = body_lines[0]
    summary = "\n".join(body_lines[1:]).strip()
    leading_title = f"{section_header}\n\n{title}".strip() if section_header else title
    continuation_title = digest_item_continuation_title(profile, title)

    chunks: list[str] = []
    if summary:
        summary_limit = max(200, limit - max(len(leading_title), len(continuation_title)) - 1)
        summary_chunks = split_oversized_block(summary, summary_limit)
        for index, summary_chunk in enumerate(summary_chunks):
            chunk_title = leading_title if index == 0 else continuation_title
            chunks.append(f"{chunk_title}\n{summary_chunk}".strip())
    else:
        chunks.append(leading_title)

    metadata_block = "\n".join(metadata_lines).strip()
    if not metadata_block:
        return chunks

    if not chunks:
        chunks.append(leading_title)

    if len(f"{chunks[-1]}\n{metadata_block}") <= limit:
        chunks[-1] = f"{chunks[-1]}\n{metadata_block}".strip()
        return chunks

    metadata_limit = max(120, limit - len(continuation_title) - 1)
    for metadata_chunk in split_oversized_block(metadata_block, metadata_limit):
        chunks.append(f"{continuation_title}\n{metadata_chunk}".strip())
    return chunks


def delivery_channel_hint(profile: dict[str, Any]) -> str:
    hint = os.getenv("FOLLOW_SCOUTX_DELIVERY_CHANNEL_HINT", "").strip()
    if hint:
        return hint
    delivery = profile.get("delivery") or {}
    return str(delivery.get("channel") or "in_chat").strip() or "in_chat"


def delivery_message_char_limit(profile: dict[str, Any], *, channel_hint: str | None = None) -> int:
    override = os.getenv("FOLLOW_SCOUTX_MAX_MESSAGE_CHARS", "").strip()
    if override:
        return max(500, int(override))
    hint = (channel_hint or delivery_channel_hint(profile)).strip().lower()
    if hint == "feishu":
        return DEFAULT_FEISHU_MESSAGE_CHAR_LIMIT
    return DEFAULT_GENERIC_MESSAGE_CHAR_LIMIT


def build_delivery_messages(
    profile: dict[str, Any],
    groups: list[dict[str, Any]],
    generated_at: str,
    *,
    feed_payload: dict[str, Any] | None = None,
    channel_hint: str | None = None,
) -> list[str]:
    language = profile["preferences"].get("language", "zh-CN")
    copy = digest_copy(language)
    limit = delivery_message_char_limit(profile, channel_hint=channel_hint)
    prefix_reserve = 180
    body_limit = max(800, limit - prefix_reserve)

    all_items = flatten_digest_groups(groups)
    if not all_items:
        return [
            "\n".join(
                [
                    digest_title(profile),
                    "",
                    f"{copy['generated_at']}: {generated_at}",
                    f"{copy['items']}: 0",
                    "",
                    copy["empty"],
                ]
            ).strip()
            + "\n"
        ]

    blocks: list[str] = []
    multiple_groups = len(groups) > 1
    for group in groups:
        items = group.get("items", [])
        group_label = str(group.get("label") or message_group_label(str(group.get("group_id") or "scoutx"), language))
        if multiple_groups:
            section_header = f"{group_label}\n{copy['items']}: {len(items)}"
            if items:
                first_block = render_digest_item_block(profile, items[0], index=1)
                blocks.extend(
                    split_digest_item_block(
                        profile,
                        first_block,
                        body_limit,
                        section_header=section_header,
                    )
                )
                remaining_items = items[1:]
                start_index = 2
            else:
                blocks.append(f"{section_header}\n\n{copy['empty']}")
                remaining_items = []
                start_index = 1
        else:
            remaining_items = items
            start_index = 1

        for index, item in enumerate(remaining_items, start=start_index):
            blocks.extend(
                split_digest_item_block(
                    profile,
                    render_digest_item_block(profile, item, index=index),
                    body_limit,
                )
            )

    chunk_bodies: list[str] = []
    current_blocks: list[str] = []
    current_length = 0
    for block in blocks:
        projected_length = current_length + 2 + len(block) if current_blocks else len(block)
        if current_blocks and projected_length > body_limit:
            chunk_bodies.append("\n\n".join(current_blocks).strip())
            current_blocks = [block]
            current_length = len(block)
            continue
        current_blocks.append(block)
        current_length = projected_length
    if current_blocks:
        chunk_bodies.append("\n\n".join(current_blocks).strip())

    messages: list[str] = []
    chunk_count = len(chunk_bodies)
    warning_lines = partial_warning_lines(profile, feed_payload or {})
    for index, body in enumerate(chunk_bodies, start=1):
        prefix = [
            digest_title(profile, part_index=index if chunk_count > 1 else None, part_count=chunk_count if chunk_count > 1 else None),
            "",
        ]
        if warning_lines:
            prefix.extend(warning_lines + [""])
        prefix.extend(
            [
            f"{copy['generated_at']}: {generated_at}",
            f"{copy['items']}: {len(all_items)}",
            ]
        )
        messages.append("\n".join(prefix + ["", body]).strip() + "\n")
    return messages


def render_delivery_messages_as_text(messages: list[str]) -> str:
    if len(messages) <= 1:
        return messages[0] if messages else ""
    rendered_parts: list[str] = []
    for index, message in enumerate(messages, start=1):
        rendered_parts.append(f"[Message {index}/{len(messages)}]\n{message.strip()}")
    return "\n\n---\n\n".join(rendered_parts).strip() + "\n"


def render_digest(
    profile: dict[str, Any],
    items: list[dict[str, Any]],
    generated_at: str,
    *,
    group_id: str | None = None,
    feed_payload: dict[str, Any] | None = None,
) -> str:
    language = profile["preferences"].get("language", "zh-CN")
    copy = digest_copy(language)
    title = copy["title"]
    if group_id:
        title = f"{title}｜{message_group_label(group_id, language)}"
    per_item_budget = summary_char_budget(profile)
    lines = [
        title,
        "",
    ]
    warning_lines = partial_warning_lines(profile, feed_payload or {})
    if warning_lines:
        lines.extend(warning_lines + [""])
    lines.extend(
        [
            f"{copy['generated_at']}: {generated_at}",
            f"{copy['items']}: {len(items)}",
            "",
        ]
    )
    if not items:
        lines.append(copy["empty"])
        return "\n".join(lines).strip() + "\n"

    for index, item in enumerate(items, start=1):
        source = item["sources"][0] if item["sources"] else "unknown"
        lines.append(f"{index}. {item['title']}")
        summary = compress_item_summary(item, char_budget=per_item_budget) if item["summary"] else ""
        if summary:
            lines.append(summary)
        lines.append(f"{copy['source']}: {source}")
        if item["published_at"]:
            lines.append(f"{copy['published']}: {item['published_at']}")
        if item["url"]:
            lines.append(f"{copy['link']}: {item['url']}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def render_digest_groups(
    profile: dict[str, Any],
    groups: list[dict[str, Any]],
    generated_at: str,
    *,
    feed_payload: dict[str, Any] | None = None,
) -> str:
    if len(groups) <= 1:
        rendered = [
            render_digest(
                profile,
                group.get("items", []),
                generated_at,
                group_id=str(group.get("group_id") or ""),
                feed_payload=feed_payload,
            )
            for group in groups
        ]
        return "\n---\n\n".join(part.strip() for part in rendered if part.strip()) + "\n"
    return render_delivery_messages_as_text(build_delivery_messages(profile, groups, generated_at, feed_payload=feed_payload))


def build_prepare_digest_payload(
    profile: dict[str, Any],
    feed_payload: dict[str, Any],
    groups: list[dict[str, Any]],
) -> dict[str, Any]:
    generated_at = str(feed_payload.get("generated_at") or utcnow_iso())
    per_item_budget = summary_char_budget(profile)
    per_item_timeout = item_timeout_seconds(profile)
    items = flatten_digest_groups(groups)

    def payload_item(item: dict[str, Any]) -> dict[str, Any]:
        return {
            "content_id": item["content_id"],
            "source_type": item.get("source_type", "scoutx"),
            "source_label": item.get("source_label", SOURCE_TYPE_LABELS["scoutx"]),
            "title": item["title"],
            "summary_text": compress_item_summary(item, char_budget=per_item_budget),
            "canonical_url": item["url"],
            "published_at": item["published_at"],
            "sources": item["sources"],
            "tags": item["tags"],
            "metadata": item.get("metadata", {}),
        }

    return {
        "status": feed_payload_status(feed_payload),
        "generated_at": generated_at,
        "config": {
            "language": profile["preferences"].get("language", "zh-CN"),
            "style": profile.get("style", {}),
            "schedule": profile.get("schedule", {}),
            "preferences": {
                "source_mode": profile["preferences"].get("source_mode", "scoutx"),
                "source_types": profile_source_types(profile),
                "topics": profile["preferences"].get("topics", []),
                "keywords_include": profile["preferences"].get("keywords_include", []),
                "keywords_exclude": profile["preferences"].get("keywords_exclude", []),
                "preferred_sources": profile["preferences"].get("preferred_sources", []),
                "max_items": profile["preferences"].get("max_items", 8),
                "max_first_party_items": profile["preferences"].get("max_first_party_items"),
                "max_scoutx_items": profile["preferences"].get("max_scoutx_items"),
            },
        },
        "stats": {
            "item_count": len(items),
            "message_count": len(groups),
            "group_counts": {
                str(group.get("group_id")): len(group.get("items", []))
                for group in groups
            },
            "group_limits": {
                str(group.get("group_id")): group.get("limit", 0)
                for group in groups
            },
            "source_counts": {
                source_type: len([item for item in items if item.get("source_type") == source_type])
                for source_type in SOURCE_TYPES
            },
            "feed_generated_at": generated_at,
        },
        "processing": {
            "per_item_input_char_budget": per_item_budget,
            "per_item_timeout_seconds": per_item_timeout,
            "mode": "item_by_item",
        },
        "output_contract": {
            "title": digest_copy(profile["preferences"].get("language", "zh-CN"))["title"],
            "header_lines": [
                "Generated at: <feed generated time>",
                "Items: <number of selected items>",
            ],
            "item_template": [
                "<index>. <localized title based on the item when config.language is zh-CN or bilingual; otherwise use an English title>",
                "<one compact but complete paragraph localized to config.language and based only on the item's summary_text>",
                "Source: <primary source>",
                "Published: <published_at if present>",
                "Link: <canonical_url>",
            ],
            "failure_template": [
                "<index>. <localized title based on the item when config.language is zh-CN or bilingual; otherwise use an English title>",
                "Status: failed",
                "Reason: <why the item could not be fully generated within the allowed budget or timeout>",
                "Source: <primary source>",
                "Published: <published_at if present>",
                "Link: <canonical_url>",
            ],
            "rules": [
                "Use only the selected items in this payload.",
                "If groups contains more than one group, keep them in one digest by default and render one section per group.",
                "The first_party group covers X posts and podcasts; the scoutx group covers ScoutX curated media.",
                "Do not invent facts beyond title, summary_text, source, published_at, and canonical_url.",
                "Respect item.source_type: scoutx is the curated ScoutX media feed, x is first-party X posts, and podcast is first-party podcast transcript content.",
                "Process items one by one, not all at once.",
                "Treat processing.per_item_timeout_seconds as the maximum target time for each item.",
                "If an item cannot be fully produced within the allowed budget or timeout, emit the failure_template for that item instead of skipping it.",
                "Do not silently drop items.",
                "Keep one numbered section per item.",
                "Do not merge item 4..n into grouped placeholders such as 'more updates', '更多动态', or '更多精选内容'.",
                "Do not aggregate multiple selected items into one numbered entry, one paragraph, or one bullet.",
                "If the final digest is too long for the target channel, split it into multiple messages while preserving section boundaries when possible.",
                "Do not rewrite into bullet-point highlights under each item.",
                "Preserve original links exactly.",
                "Respect config.language and the prompt texts in prompts.",
                "If config.language is zh-CN, localize both the title line and the summary paragraph into Chinese, especially for first_party items.",
                "Do not leave first_party items in raw English when config.language is zh-CN unless a proper noun, handle, product name, or very short quote should remain in the original language for clarity.",
            ],
        },
        "groups": [
            {
                "group_id": group.get("group_id"),
                "label": group.get("label"),
                "source_types": group.get("source_types", []),
                "limit": group.get("limit", 0),
                "item_count": len(group.get("items", [])),
                "items": [payload_item(item) for item in group.get("items", [])],
            }
            for group in groups
        ],
        "items": [payload_item(item) for item in items],
        "loaded_source_types": feed_payload.get("loaded_source_types") or [],
        "failed_source_types": feed_payload.get("failed_source_types") or [],
        "prompts": load_prompt_texts(),
        "errors": feed_payload.get("errors") or [],
    }


def command_configure(args: argparse.Namespace) -> int:
    profile = load_profile()
    profile = update_profile_from_args(profile, args)
    save_profile(profile)
    json.dump(profile, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


def command_show_profile(_args: argparse.Namespace) -> int:
    json.dump(load_profile(), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


def command_show_state(_args: argparse.Namespace) -> int:
    json.dump(load_state(), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


def command_show_service(_args: argparse.Namespace) -> int:
    json.dump(load_service_config(), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


def command_configure_service(args: argparse.Namespace) -> int:
    service_config = load_service_config()
    if args.feed_url is not None:
        service_config["feed_url"] = args.feed_url
        service_config["scoutx_feed_url"] = args.feed_url
    if arg_value(args, "scoutx_feed_url") is not None:
        service_config["scoutx_feed_url"] = args.scoutx_feed_url
        service_config["feed_url"] = args.scoutx_feed_url
    if arg_value(args, "x_feed_url") is not None:
        service_config["x_feed_url"] = args.x_feed_url
    if arg_value(args, "podcast_feed_url") is not None:
        service_config["podcast_feed_url"] = args.podcast_feed_url
    if args.meta_url is not None:
        service_config["meta_url"] = args.meta_url
    if args.timeout_seconds is not None:
        service_config["timeout_seconds"] = args.timeout_seconds
    save_service_config(service_config)
    json.dump(service_config, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


def command_preview(args: argparse.Namespace) -> int:
    profile = load_profile()
    feed_payload = fetch_selected_feed_payload(profile, args)
    message_group = arg_value(args, "message_group") or "all"
    groups = build_digest_groups(profile, feed_payload, message_group=message_group)
    items = flatten_digest_groups(groups)
    generated_at = str(feed_payload.get("generated_at") or utcnow_iso())

    state = load_state()
    state["last_preview_at"] = utcnow_iso()
    state["last_feed_fetch_at"] = generated_at
    state["last_digest_item_ids"] = [item["content_id"] for item in items if item["content_id"]]
    save_state(state)

    if args.json:
        delivery_messages = build_delivery_messages(profile, groups, generated_at, feed_payload=feed_payload)
        payload = {
            "status": feed_payload_status(feed_payload),
            "generated_at": generated_at,
            "profile": profile,
            "groups": groups,
            "items": items,
            "stats": {
                "group_counts": {
                    str(group.get("group_id")): len(group.get("items", []))
                    for group in groups
                },
                "item_count": len(items),
            },
            "delivery": {
                "channel_hint": delivery_channel_hint(profile),
                "message_count": len(delivery_messages),
                "message_char_limit": delivery_message_char_limit(profile),
                "messages": delivery_messages,
            },
            "loaded_source_types": feed_payload.get("loaded_source_types") or [],
            "failed_source_types": feed_payload.get("failed_source_types") or [],
            "errors": feed_payload.get("errors") or [],
        }
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    sys.stdout.write(render_digest_groups(profile, groups, generated_at, feed_payload=feed_payload))
    return 0


def command_deliver(args: argparse.Namespace) -> int:
    profile = load_profile()
    feed_payload = fetch_selected_feed_payload(profile, args)
    message_group = arg_value(args, "message_group") or "all"
    groups = build_digest_groups(profile, feed_payload, message_group=message_group)
    items = flatten_digest_groups(groups)
    generated_at = str(feed_payload.get("generated_at") or utcnow_iso())

    state = load_state()
    state["last_preview_at"] = utcnow_iso()
    state["last_feed_fetch_at"] = generated_at
    state["last_digest_item_ids"] = [item["content_id"] for item in items if item["content_id"]]
    save_state(state)

    delivery_messages = build_delivery_messages(profile, groups, generated_at, feed_payload=feed_payload)
    if args.json:
        payload = {
            "status": feed_payload_status(feed_payload),
            "generated_at": generated_at,
            "channel_hint": delivery_channel_hint(profile),
            "message_char_limit": delivery_message_char_limit(profile),
            "message_count": len(delivery_messages),
            "message_group": message_group,
            "group_counts": {
                str(group.get("group_id")): len(group.get("items", []))
                for group in groups
            },
            "item_count": len(items),
            "messages": delivery_messages,
            "loaded_source_types": feed_payload.get("loaded_source_types") or [],
            "failed_source_types": feed_payload.get("failed_source_types") or [],
            "errors": feed_payload.get("errors") or [],
        }
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    sys.stdout.write(render_delivery_messages_as_text(delivery_messages))
    return 0


def command_prepare_digest(args: argparse.Namespace) -> int:
    profile = load_profile()
    feed_payload = fetch_selected_feed_payload(profile, args)
    message_group = arg_value(args, "message_group") or "all"
    groups = build_digest_groups(profile, feed_payload, message_group=message_group)
    items = flatten_digest_groups(groups)

    state = load_state()
    state["last_preview_at"] = utcnow_iso()
    state["last_feed_fetch_at"] = str(feed_payload.get("generated_at") or utcnow_iso())
    state["last_digest_item_ids"] = [item["content_id"] for item in items if item["content_id"]]
    save_state(state)

    payload = build_prepare_digest_payload(profile, feed_payload, groups)
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


def build_openclaw_cron_expression(profile: dict[str, Any]) -> str:
    schedule = profile.get("schedule") or {}
    time_value = str(schedule.get("time") or "09:00").strip() or "09:00"
    if ":" in time_value:
        hour_str, minute_str = time_value.split(":", 1)
    else:
        hour_str, minute_str = time_value, "00"

    hour = int(hour_str)
    minute = int(minute_str)
    frequency = str(schedule.get("frequency") or "daily").strip().lower()
    if frequency == "weekly":
        days = [str(value).strip().lower() for value in schedule.get("days") or []]
        cron_days = [DAY_TO_CRON[day] for day in days if day in DAY_TO_CRON]
        if not cron_days:
            cron_days = [DAY_TO_CRON["mon"]]
        return f"{minute} {hour} * * {','.join(cron_days)}"
    return f"{minute} {hour} * * *"


def build_selected_feed_urls(
    profile: dict[str, Any],
    service_config: dict[str, Any],
    *,
    feed_url: str | None = None,
    x_feed_url: str | None = None,
    podcast_feed_url: str | None = None,
    message_group: str | None = "all",
) -> dict[str, str]:
    explicit_urls = {
        "scoutx": feed_url,
        "x": x_feed_url,
        "podcast": podcast_feed_url,
    }
    feed_urls: dict[str, str] = {}
    for source_type in source_types_for_message_group(profile, message_group):
        env_value = os.getenv(SOURCE_TYPE_ENV_VARS[source_type])
        resolved = explicit_urls[source_type] or env_value or service_feed_url(service_config, source_type)
        feed_urls[source_type] = ensure_real_feed_url(resolved)
    return feed_urls


def feed_env_prefix(feed_urls: dict[str, str]) -> str:
    parts = []
    for source_type, feed_url in feed_urls.items():
        parts.append(f"{SOURCE_TYPE_ENV_VARS[source_type]}={shlex.quote(feed_url)}")
    return " ".join(parts)


def runtime_env_prefix(
    feed_urls: dict[str, str],
    *,
    delivery_channel_hint_value: str | None = None,
) -> str:
    parts = []
    feed_prefix = feed_env_prefix(feed_urls)
    if feed_prefix:
        parts.append(feed_prefix)
    if delivery_channel_hint_value:
        parts.append(f"FOLLOW_SCOUTX_DELIVERY_CHANNEL_HINT={shlex.quote(delivery_channel_hint_value)}")
    return " ".join(part for part in parts if part).strip()


def should_use_prepare_digest(profile: dict[str, Any], *, message_group: str = "all") -> bool:
    language = str(profile.get("preferences", {}).get("language") or "zh-CN").strip()
    if language == "en":
        return False
    source_types = source_types_for_message_group(profile, message_group)
    return any(source_type in {"x", "podcast"} for source_type in source_types)


def openclaw_delivery_payload_text(run_command: str) -> str:
    return (
        f"Run `{run_command}`. The command returns JSON with a `messages` array. "
        "Send each entry in `messages` as a separate assistant message in order without rewriting. "
        "If there is exactly one entry, use it as your final answer. "
        "If there are multiple entries, send entries 1..n-1 first, then send the last entry as your final answer. "
        "Do not merge, summarize, or reformat the chunks."
    )


def openclaw_prepare_digest_payload_text(run_command: str) -> str:
    return (
        f"Run `{run_command}`. The command returns a structured JSON payload with `status`, `config`, `groups`, "
        "`items`, `prompts`, `output_contract`, `failed_source_types`, and `errors`. "
        "Write the final digest strictly following `prompts` and `output_contract`. "
        "Respect `config.language`: if it is `zh-CN`, write the digest in Chinese; if it is `bilingual`, keep it bilingual and compact. "
        "When `config.language` is `zh-CN`, localize first-party source titles and summaries into natural Chinese instead of leaving them in raw English. "
        "Keep exactly one numbered section per selected item. Preserve links exactly. "
        "If `status` is `partial`, briefly explain that some selected feeds failed and name `failed_source_types` before the digest body. "
        "If the final digest is too long for the target channel, split it into multiple assistant messages while preserving section boundaries when possible. "
        "Do not drop selected items. Do not invent facts beyond the payload."
    )


def build_openclaw_cron_command(
    profile: dict[str, Any],
    *,
    feed_urls: dict[str, str],
    script_path: str,
    name: str,
    agent: str,
    session: str,
    channel: str | None,
    to: str | None,
    timeout_seconds: int,
    message_group: str = "all",
    main_session_system_event: bool = False,
) -> str:
    cron_expr = build_openclaw_cron_expression(profile)
    if main_session_system_event:
        delivery_channel = "main_session_system_event"
        parts = [
            "openclaw",
            "cron",
            "add",
            "--name",
            name,
            "--cron",
            cron_expr,
            "--agent",
            agent,
            "--session",
            "main",
        ]
    else:
        resolved_channel, resolved_to = resolve_openclaw_delivery(profile, channel=channel, to=to)
        delivery_channel = resolved_channel
        parts = [
            "openclaw",
            "cron",
            "add",
            "--name",
            name,
            "--cron",
            cron_expr,
            "--agent",
            agent,
            "--session",
            session,
        ]

    env_prefix = runtime_env_prefix(feed_urls, delivery_channel_hint_value=delivery_channel)
    if should_use_prepare_digest(profile, message_group=message_group):
        run_parts = ["python3", script_path, "prepare-digest"]
        if message_group != "all":
            run_parts.extend(["--message-group", message_group])
        run_command = f"{env_prefix} {' '.join(shlex.quote(part) for part in run_parts)}".strip()
        payload = openclaw_prepare_digest_payload_text(run_command)
    else:
        run_parts = ["python3", script_path, "deliver", "--json"]
        if message_group != "all":
            run_parts.extend(["--message-group", message_group])
        run_command = f"{env_prefix} {' '.join(shlex.quote(part) for part in run_parts)}".strip()
        payload = openclaw_delivery_payload_text(run_command)

    if main_session_system_event:
        parts.extend(["--system-event", payload, "--exact", "--timeout-seconds", str(timeout_seconds)])
        return " ".join(shlex.quote(part) for part in parts)

    parts.extend(
        [
        "--message",
        payload,
        "--announce",
        "--channel",
        resolved_channel,
        ]
    )
    if resolved_to:
        parts.extend(["--to", resolved_to])
    parts.extend(["--best-effort-deliver", "--exact", "--timeout-seconds", str(timeout_seconds)])
    return " ".join(shlex.quote(part) for part in parts)


def build_openclaw_cron_args(
    profile: dict[str, Any],
    *,
    feed_urls: dict[str, str],
    script_path: str,
    name: str,
    agent: str,
    session: str,
    channel: str | None,
    to: str | None,
    timeout_seconds: int,
    message_group: str = "all",
    main_session_system_event: bool = False,
) -> list[str]:
    cron_expr = build_openclaw_cron_expression(profile)
    if main_session_system_event:
        delivery_channel = "main_session_system_event"
        resolved_channel = None
        resolved_to = None
        args = [
            "openclaw",
            "cron",
            "add",
            "--name",
            name,
            "--cron",
            cron_expr,
            "--agent",
            agent,
            "--session",
            "main",
        ]
    else:
        resolved_channel, resolved_to = resolve_openclaw_delivery(profile, channel=channel, to=to)
        delivery_channel = resolved_channel
        args = [
            "openclaw",
            "cron",
            "add",
            "--name",
            name,
            "--cron",
            cron_expr,
            "--agent",
            agent,
            "--session",
            session,
        ]

    env_prefix = runtime_env_prefix(feed_urls, delivery_channel_hint_value=delivery_channel)
    if should_use_prepare_digest(profile, message_group=message_group):
        run_parts = ["python3", script_path, "prepare-digest"]
        if message_group != "all":
            run_parts.extend(["--message-group", message_group])
        run_command = f"{env_prefix} {' '.join(shlex.quote(part) for part in run_parts)}".strip()
        payload = openclaw_prepare_digest_payload_text(run_command)
    else:
        run_parts = ["python3", script_path, "deliver", "--json"]
        if message_group != "all":
            run_parts.extend(["--message-group", message_group])
        run_command = f"{env_prefix} {' '.join(shlex.quote(part) for part in run_parts)}".strip()
        payload = openclaw_delivery_payload_text(run_command)

    if main_session_system_event:
        args.extend(["--system-event", payload, "--exact", "--timeout-seconds", str(timeout_seconds)])
        return args

    args.extend(["--message", payload, "--announce", "--channel", resolved_channel])
    if resolved_to:
        args.extend(["--to", resolved_to])
    args.extend(
        [
            "--best-effort-deliver",
            "--exact",
            "--timeout-seconds",
            str(timeout_seconds),
        ]
    )
    return args


def openclaw_message_groups_for_profile(profile: dict[str, Any]) -> list[str]:
    return ["all"]


def openclaw_job_name(base_name: str, message_group: str, *, split: bool) -> str:
    if not split or message_group == "all":
        return base_name
    suffix = MESSAGE_GROUP_NAME_SUFFIXES[message_group]
    return f"{base_name}-{suffix}"


def build_openclaw_job_specs(
    profile: dict[str, Any],
    service_config: dict[str, Any],
    *,
    feed_url: str | None,
    x_feed_url: str | None,
    podcast_feed_url: str | None,
    script_path: str,
    name: str,
    agent: str,
    session: str,
    channel: str | None,
    to: str | None,
    timeout_seconds: int,
    main_session_system_event: bool = False,
) -> list[dict[str, Any]]:
    message_groups = openclaw_message_groups_for_profile(profile)
    split = len(message_groups) > 1
    jobs: list[dict[str, Any]] = []
    for message_group in message_groups:
        job_name = openclaw_job_name(name, message_group, split=split)
        feed_urls = build_selected_feed_urls(
            profile,
            service_config,
            feed_url=feed_url,
            x_feed_url=x_feed_url,
            podcast_feed_url=podcast_feed_url,
            message_group=message_group,
        )
        command = build_openclaw_cron_command(
            profile,
            feed_urls=feed_urls,
            script_path=script_path,
            name=job_name,
            agent=agent,
            session=session,
            channel=channel,
            to=to,
            timeout_seconds=timeout_seconds,
            message_group=message_group,
            main_session_system_event=main_session_system_event,
        )
        jobs.append(
            {
                "name": job_name,
                "message_group": message_group,
                "label": message_group_label(message_group, profile["preferences"].get("language", "zh-CN"))
                if message_group != "all"
                else None,
                "feed_urls": feed_urls,
                "command": command,
                "args": build_openclaw_cron_args(
                    profile,
                    feed_urls=feed_urls,
                    script_path=script_path,
                    name=job_name,
                    agent=agent,
                    session=session,
                    channel=channel,
                    to=to,
                    timeout_seconds=timeout_seconds,
                    message_group=message_group,
                    main_session_system_event=main_session_system_event,
                ),
            }
        )
    return jobs


def resolve_openclaw_delivery(
    profile: dict[str, Any],
    *,
    channel: str | None = None,
    to: str | None = None,
) -> tuple[str, str | None]:
    delivery = profile.get("delivery") or {}
    raw_channel = str(channel or delivery.get("channel") or "last").strip()
    raw_to = str(to if to is not None else delivery.get("target") or "").strip()
    if raw_channel in {"", "in_chat", "stdout", "current", "current_chat"}:
        raw_channel = "last"
    if raw_channel == "feishu" and raw_to.startswith("user:ou_"):
        raw_to = raw_to.removeprefix("user:")
    if raw_channel == "feishu" and raw_to.startswith("group:oc_"):
        raw_to = raw_to.removeprefix("group:")
    if raw_channel != "last" and not raw_to:
        raise SystemExit(
            "OpenClaw delivery target is required for external channels. "
            "Pass --to or save it with configure --delivery-target."
        )
    return raw_channel, raw_to or None


def openclaw_delivery_diagnostics(
    profile: dict[str, Any],
    *,
    channel: str | None = None,
    to: str | None = None,
    session: str = "isolated",
    main_session_system_event: bool = False,
) -> dict[str, Any]:
    delivery = profile.get("delivery") or {}
    intended_channel = str(channel or delivery.get("channel") or "").strip().lower()
    if main_session_system_event:
        if intended_channel == "feishu":
            return {
                "stable": False,
                "delivery_mode": "main_session_system_event",
                "channel": None,
                "to": None,
                "session": "main",
                "warnings": [
                    "Feishu delivery cannot use --main-session-system-event. "
                    "System events only return results to the main session and do not explicitly announce to Feishu.",
                    "Use explicit Feishu delivery instead: --channel feishu --to <ou_xxx|oc_xxx>.",
                ],
                "recommended_action": (
                    "Remove --main-session-system-event and install the cron job with an explicit Feishu "
                    "channel/target."
                ),
            }
        return {
            "stable": True,
            "delivery_mode": "main_session_system_event",
            "channel": None,
            "to": None,
            "session": "main",
            "warnings": [],
            "recommended_action": "",
        }

    resolved_channel, resolved_to = resolve_openclaw_delivery(profile, channel=channel, to=to)
    warnings: list[str] = []

    if resolved_channel == "last":
        warnings.append(
            "OpenClaw channel resolves to 'last'. Scheduled jobs can lose the previous chat context; "
            "prefer saving an explicit channel and target before installing the cron job."
        )
        if session == "isolated":
            warnings.append(
                "The job also uses an isolated session, so it cannot rely on inherited chat context. "
                "Use --channel feishu --to <ou_xxx|oc_xxx> for Feishu, or pass --allow-channel-last "
                "only when you have verified OpenClaw can route 'last' for this installation."
            )

    return {
        "stable": not warnings,
        "delivery_mode": "announce",
        "channel": resolved_channel,
        "to": resolved_to,
        "session": session,
        "warnings": warnings,
        "recommended_action": ""
        if not warnings
        else "Configure an explicit delivery channel/target, then rerun install-openclaw-cron.",
    }


def require_stable_openclaw_delivery(diagnostics: dict[str, Any], *, allow_channel_last: bool) -> None:
    if diagnostics.get("stable"):
        return
    if allow_channel_last and diagnostics.get("delivery_mode") == "announce" and diagnostics.get("channel") == "last":
        return
    warning_text = "\n".join(f"- {warning}" for warning in diagnostics.get("warnings", []))
    current_chat_guidance = "For current-chat delivery, use --main-session-system-event."
    extra_guidance = (
        "Or rerun install-openclaw-cron with --allow-channel-last after you verify this OpenClaw installation "
        "can reliably route channel=last."
    )
    if diagnostics.get("delivery_mode") == "main_session_system_event":
        current_chat_guidance = (
            "For Feishu delivery, remove --main-session-system-event and use "
            "--channel feishu --to <ou_xxx|oc_xxx>."
        )
        extra_guidance = ""
    raise SystemExit(
        "Refusing to install an unstable OpenClaw cron delivery configuration.\n"
        f"{warning_text}\n"
        "Save an explicit delivery target, for example:\n"
        "  python3 scripts/follow_scoutx.py configure --delivery-channel feishu --delivery-target ou_xxx\n"
        f"{current_chat_guidance}"
        + (f" {extra_guidance}" if extra_guidance else "")
    )


def iter_json_objects(payload: Any) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    if isinstance(payload, dict):
        objects.append(payload)
        for value in payload.values():
            objects.extend(iter_json_objects(value))
    elif isinstance(payload, list):
        for value in payload:
            objects.extend(iter_json_objects(value))
    return objects


def openclaw_job_identity(job: dict[str, Any]) -> tuple[str, str]:
    job_id = str(job.get("id") or job.get("jobId") or job.get("job_id") or "").strip()
    job_name = str(job.get("name") or job.get("jobName") or job.get("job_name") or "").strip()
    return job_id, job_name


def replacement_job_names(base_name: str) -> set[str]:
    names = {base_name}
    for suffix in MESSAGE_GROUP_NAME_SUFFIXES.values():
        names.add(f"{base_name}-{suffix}")
    return names


def find_openclaw_jobs_by_name(names: set[str]) -> list[dict[str, str]]:
    completed = subprocess.run(
        ["openclaw", "cron", "list", "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise SystemExit(
            "Failed to list existing OpenClaw cron jobs before replacement.\n"
            f"stdout: {completed.stdout.strip()}\n"
            f"stderr: {completed.stderr.strip()}"
        )

    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"OpenClaw cron list returned invalid JSON: {completed.stdout}") from exc

    matches: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for job in iter_json_objects(payload):
        job_id, job_name = openclaw_job_identity(job)
        if not job_id or not job_name or job_name not in names or job_id in seen_ids:
            continue
        seen_ids.add(job_id)
        matches.append({"id": job_id, "name": job_name})
    return matches


def remove_openclaw_job(job_id: str) -> dict[str, Any]:
    completed = subprocess.run(
        ["openclaw", "cron", "rm", job_id],
        check=False,
        capture_output=True,
        text=True,
    )
    return {
        "id": job_id,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def command_show_openclaw_cron(args: argparse.Namespace) -> int:
    profile = load_profile()
    service_config = load_service_config()
    diagnostics = openclaw_delivery_diagnostics(
        profile,
        channel=args.channel,
        to=args.to,
        session=args.session,
        main_session_system_event=args.main_session_system_event,
    )
    jobs = build_openclaw_job_specs(
        profile,
        service_config,
        feed_url=args.feed_url,
        x_feed_url=arg_value(args, "x_feed_url"),
        podcast_feed_url=arg_value(args, "podcast_feed_url"),
        script_path=args.script_path,
        name=args.name,
        agent=args.agent,
        session=args.session,
        channel=args.channel,
        to=args.to,
        timeout_seconds=args.timeout_seconds,
        main_session_system_event=args.main_session_system_event,
    )
    if args.json:
        channel, to = (None, None) if args.main_session_system_event else resolve_openclaw_delivery(profile, channel=args.channel, to=args.to)
        payload = {
            "name": args.name,
            "cron": build_openclaw_cron_expression(profile),
            "agent": args.agent,
            "session": "main" if args.main_session_system_event else args.session,
            "channel": channel,
            "to": to,
            "mode": "split" if len(jobs) > 1 else "single",
            "script_path": args.script_path,
            "timeout_seconds": args.timeout_seconds,
            "delivery_diagnostics": diagnostics,
            "jobs": [
                {
                    "name": job["name"],
                    "message_group": job["message_group"],
                    "label": job["label"],
                    "feed_urls": job["feed_urls"],
                    "command": job["command"],
                }
                for job in jobs
            ],
        }
        if len(jobs) == 1:
            payload["feed_urls"] = jobs[0]["feed_urls"]
            payload["command"] = jobs[0]["command"]
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    for job in jobs:
        sys.stdout.write(job["command"] + "\n")
    for warning in diagnostics.get("warnings", []):
        sys.stderr.write(f"Warning: {warning}\n")
    return 0


def command_install_openclaw_cron(args: argparse.Namespace) -> int:
    profile = load_profile()
    service_config = load_service_config()
    diagnostics = openclaw_delivery_diagnostics(
        profile,
        channel=args.channel,
        to=args.to,
        session=args.session,
        main_session_system_event=args.main_session_system_event,
    )
    jobs = build_openclaw_job_specs(
        profile,
        service_config,
        feed_url=args.feed_url,
        x_feed_url=arg_value(args, "x_feed_url"),
        podcast_feed_url=arg_value(args, "podcast_feed_url"),
        script_path=args.script_path,
        name=args.name,
        agent=args.agent,
        session=args.session,
        channel=args.channel,
        to=args.to,
        timeout_seconds=args.timeout_seconds,
        main_session_system_event=args.main_session_system_event,
    )

    if not args.apply:
        payload = {
            "mode": "dry_run",
            "delivery_mode": "split" if len(jobs) > 1 else "single",
            "apply_blocked": not diagnostics["stable"] and not args.allow_channel_last,
            "replace_existing": args.replace_existing,
            "delivery_diagnostics": diagnostics,
            "commands": [job["command"] for job in jobs],
            "jobs": [
                {
                    "name": job["name"],
                    "message_group": job["message_group"],
                    "label": job["label"],
                    "feed_urls": job["feed_urls"],
                    "command": job["command"],
                }
                for job in jobs
            ],
        }
        if len(jobs) == 1:
            payload["command"] = jobs[0]["command"]
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    require_stable_openclaw_delivery(diagnostics, allow_channel_last=args.allow_channel_last)

    removed_jobs: list[dict[str, Any]] = []
    if args.replace_existing:
        existing_jobs = find_openclaw_jobs_by_name(replacement_job_names(args.name))
        for existing_job in existing_jobs:
            removed_jobs.append(remove_openclaw_job(existing_job["id"]))
        failed_removals = [result for result in removed_jobs if result["returncode"] != 0]
        if failed_removals:
            payload = {
                "mode": "apply",
                "replace_existing": True,
                "removed_jobs": removed_jobs,
                "error": "Failed to remove one or more existing OpenClaw cron jobs.",
            }
            json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write("\n")
            return 1

    results = []
    for job in jobs:
        completed = subprocess.run(
            job["args"],
            check=False,
            capture_output=True,
            text=True,
        )
        results.append(
            {
                "name": job["name"],
                "message_group": job["message_group"],
                "command": job["command"],
                "returncode": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            }
        )
    payload = {
        "mode": "apply",
        "delivery_mode": "split" if len(jobs) > 1 else "single",
        "replace_existing": args.replace_existing,
        "removed_jobs": removed_jobs,
        "results": results,
    }
    if len(results) == 1:
        payload["command"] = results[0]["command"]
        payload["returncode"] = results[0]["returncode"]
        payload["stdout"] = results[0]["stdout"]
        payload["stderr"] = results[0]["stderr"]
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if all(result["returncode"] == 0 for result in results) else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Local profile manager and preview client for Follow ScoutX.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    configure_parser = subparsers.add_parser("configure", help="Create or update the local profile")
    configure_parser.add_argument("--frequency", choices=["daily", "weekly"])
    configure_parser.add_argument("--time")
    configure_parser.add_argument("--days")
    configure_parser.add_argument("--language", choices=["zh-CN", "en", "bilingual"])
    configure_parser.add_argument(
        "--source-mode",
        choices=["scoutx", "first_party", "mixed"],
        help="High-level source selection: scoutx, first_party (X + podcast), or mixed",
    )
    configure_parser.add_argument(
        "--source-types",
        help="Comma-separated source types: scoutx,x,podcast",
    )
    configure_parser.add_argument("--delivery-channel")
    configure_parser.add_argument("--delivery-target")
    configure_parser.add_argument("--topics")
    configure_parser.add_argument("--keywords-include")
    configure_parser.add_argument("--keywords-exclude")
    configure_parser.add_argument("--preferred-sources")
    configure_parser.add_argument("--max-items", type=int)
    configure_parser.add_argument(
        "--max-first-party-items",
        type=int,
        help="Maximum items for the first-party message group (X + podcast)",
    )
    configure_parser.add_argument(
        "--max-scoutx-items",
        type=int,
        help="Maximum items for the ScoutX curated media message group",
    )
    configure_parser.add_argument("--length", choices=["short", "medium", "long"])
    configure_parser.add_argument("--tone")
    configure_parser.set_defaults(handler=command_configure)

    show_profile_parser = subparsers.add_parser("show-profile", help="Show the saved local profile")
    show_profile_parser.set_defaults(handler=command_show_profile)

    show_state_parser = subparsers.add_parser("show-state", help="Show the local state file")
    show_state_parser.set_defaults(handler=command_show_state)

    show_service_parser = subparsers.add_parser("show-service", help="Show the bundled central service config")
    show_service_parser.set_defaults(handler=command_show_service)

    configure_service_parser = subparsers.add_parser(
        "configure-service",
        help="Create or update the local service endpoint override used by this installation",
    )
    configure_service_parser.add_argument("--feed-url")
    configure_service_parser.add_argument("--scoutx-feed-url")
    configure_service_parser.add_argument("--x-feed-url")
    configure_service_parser.add_argument("--podcast-feed-url")
    configure_service_parser.add_argument("--meta-url")
    configure_service_parser.add_argument("--timeout-seconds", type=int)
    configure_service_parser.set_defaults(handler=command_configure_service)

    preview_parser = subparsers.add_parser("preview", help="Preview a digest using the saved local profile")
    preview_parser.add_argument("--feed-url")
    preview_parser.add_argument("--feed-file")
    preview_parser.add_argument("--x-feed-url")
    preview_parser.add_argument("--x-feed-file")
    preview_parser.add_argument("--podcast-feed-url")
    preview_parser.add_argument("--podcast-feed-file")
    preview_parser.add_argument("--message-group", choices=MESSAGE_GROUP_CHOICES, default="all")
    preview_parser.add_argument("--allow-partial-feeds", action="store_true")
    preview_parser.add_argument("--json", action="store_true")
    preview_parser.set_defaults(handler=command_preview)

    deliver_parser = subparsers.add_parser(
        "deliver",
        help="Render a final markdown digest suitable for OpenClaw --announce delivery",
    )
    deliver_parser.add_argument("--feed-url")
    deliver_parser.add_argument("--feed-file")
    deliver_parser.add_argument("--x-feed-url")
    deliver_parser.add_argument("--x-feed-file")
    deliver_parser.add_argument("--podcast-feed-url")
    deliver_parser.add_argument("--podcast-feed-file")
    deliver_parser.add_argument("--message-group", choices=MESSAGE_GROUP_CHOICES, default="all")
    deliver_parser.add_argument("--allow-partial-feeds", action="store_true")
    deliver_parser.add_argument("--json", action="store_true")
    deliver_parser.set_defaults(handler=command_deliver)

    prepare_digest_parser = subparsers.add_parser(
        "prepare-digest",
        help="Output a structured JSON payload for prompt-controlled LLM digest generation",
    )
    prepare_digest_parser.add_argument("--feed-url")
    prepare_digest_parser.add_argument("--feed-file")
    prepare_digest_parser.add_argument("--x-feed-url")
    prepare_digest_parser.add_argument("--x-feed-file")
    prepare_digest_parser.add_argument("--podcast-feed-url")
    prepare_digest_parser.add_argument("--podcast-feed-file")
    prepare_digest_parser.add_argument("--message-group", choices=MESSAGE_GROUP_CHOICES, default="all")
    prepare_digest_parser.add_argument("--allow-partial-feeds", action="store_true")
    prepare_digest_parser.set_defaults(handler=command_prepare_digest)

    openclaw_cron_parser = subparsers.add_parser(
        "show-openclaw-cron",
        help="Print a recommended openclaw cron add command using the saved schedule and service config",
    )
    openclaw_cron_parser.add_argument("--feed-url")
    openclaw_cron_parser.add_argument(
        "--script-path",
        default=current_script_path(),
    )
    openclaw_cron_parser.add_argument("--x-feed-url")
    openclaw_cron_parser.add_argument("--podcast-feed-url")
    openclaw_cron_parser.add_argument("--name", default="follow-scoutx-daily")
    openclaw_cron_parser.add_argument("--agent", default="main")
    openclaw_cron_parser.add_argument("--session", default="isolated")
    openclaw_cron_parser.add_argument("--channel")
    openclaw_cron_parser.add_argument("--to")
    openclaw_cron_parser.add_argument("--timeout-seconds", type=int, default=300)
    openclaw_cron_parser.add_argument(
        "--main-session-system-event",
        action="store_true",
        help="Use OpenClaw main-session system events for stable current-chat delivery instead of announce/channel delivery.",
    )
    openclaw_cron_parser.add_argument("--json", action="store_true")
    openclaw_cron_parser.set_defaults(handler=command_show_openclaw_cron)

    install_openclaw_cron_parser = subparsers.add_parser(
        "install-openclaw-cron",
        help="Create the recommended OpenClaw cron job for this Follow ScoutX installation",
    )
    install_openclaw_cron_parser.add_argument("--feed-url")
    install_openclaw_cron_parser.add_argument(
        "--script-path",
        default=current_script_path(),
    )
    install_openclaw_cron_parser.add_argument("--x-feed-url")
    install_openclaw_cron_parser.add_argument("--podcast-feed-url")
    install_openclaw_cron_parser.add_argument("--name", default="follow-scoutx-daily")
    install_openclaw_cron_parser.add_argument("--agent", default="main")
    install_openclaw_cron_parser.add_argument("--session", default="isolated")
    install_openclaw_cron_parser.add_argument("--channel")
    install_openclaw_cron_parser.add_argument("--to")
    install_openclaw_cron_parser.add_argument("--timeout-seconds", type=int, default=300)
    install_openclaw_cron_parser.add_argument(
        "--main-session-system-event",
        action="store_true",
        help="Use OpenClaw main-session system events for stable current-chat delivery instead of announce/channel delivery.",
    )
    install_openclaw_cron_parser.add_argument(
        "--allow-channel-last",
        action="store_true",
        help="Allow installing a cron job that delivers to channel=last. Use only after verifying OpenClaw can route it reliably.",
    )
    install_openclaw_cron_parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="Before applying, remove existing OpenClaw cron jobs with the same generated names by listing jobs and deleting by id.",
    )
    install_openclaw_cron_parser.add_argument("--apply", action="store_true")
    install_openclaw_cron_parser.set_defaults(handler=command_install_openclaw_cron)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
