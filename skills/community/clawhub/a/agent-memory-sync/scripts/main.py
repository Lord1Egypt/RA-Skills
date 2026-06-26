#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OpenClaw memory sync with a single canonical index."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


ROOT = Path(__file__).resolve().parents[1]
INDEX_META = "_meta"
INDEX_NAME = "memory_index.json"
LEGACY_INDEX_NAME = "openclaw_memory_index.json"
PROFILE_NAME = "user_profile.json"
MACHINE_DIR = ".memory-sync"
STATE_INDEX_DIR = f"{MACHINE_DIR}/index"
STATE_AGENTS_DIR = f"{MACHINE_DIR}/agents"
STATE_SHARED_DIR = f"{MACHINE_DIR}/shared"
STATE_REVIEW_DIR = f"{MACHINE_DIR}/review"
STATE_CACHE_DIR = f"{MACHINE_DIR}/cache"
PATH_MAP_FILE = f"{MACHINE_DIR}/path-map.json"
DASHBOARD_DIR = "Dashboard"
SOURCES_DIR = "Sources"
OBSIDIAN_INDEX_FILE = f"{DASHBOARD_DIR}/Memory Index.md"
PROFILE_MD_FILE = f"{DASHBOARD_DIR}/User Profile.md"
MEMORY_DASHBOARD_FILE = f"{DASHBOARD_DIR}/Memory Dashboard.md"
MEMORY_DIRECTORY_FILE = f"{DASHBOARD_DIR}/Memory Directory.md"
MEMORY_PAGES_DIR = "Memories"
RETIRED_DASHBOARD_FILES = (
    f"{DASHBOARD_DIR}/Index Layers.md",
    f"{DASHBOARD_DIR}/Open Source Boundary.md",
    f"{DASHBOARD_DIR}/OpenClaw\u8bb0\u5fc6\u7d22\u5f15.md",
    f"{DASHBOARD_DIR}/\u5168\u5c40\u8bb0\u5fc6\u7d22\u5f15.md",
)
RETIRED_LAYOUT_DIRS = (
    "02-Lessons",
    "03-Reference",
    "_agents",
    "_index",
    "_review",
    "_shared",
    "_context",
)
LEGACY_CONTEXT_DIR = "_context"
CONTEXT_DIR = LEGACY_CONTEXT_DIR
CONTEXT_JSON = f"{CONTEXT_DIR}/agent_context.json"
ADAPTER_NAMES = ("codex", "claude", "openclaw", "opencode", "hermes-agent", "qoder")
AGENT_RULE_ENTRYPOINTS = {
    "openclaw": ["workspace AGENTS.md", "skill/workspace rule file loaded by OpenClaw"],
    "codex": ["project AGENTS.md", "~/.codex/AGENTS.md"],
    "claude": ["project CLAUDE.md", "project .claude/CLAUDE.md", "~/.claude/CLAUDE.md"],
    "opencode": ["project AGENTS.md", "~/.config/opencode/AGENTS.md", "CLAUDE.md compatibility file when used"],
    "hermes-agent": ["configured system prompt or rule file", "Context/hermes-agent.md handoff when no persistent rule file exists"],
    "qoder": ["Qoder user/project rules when configured", "Context/qoder.md handoff when no persistent rule file exists"],
}
AGENTS_DIR = SOURCES_DIR
SHARED_DIR = STATE_SHARED_DIR
SHARED_CONTEXT_DIR = "Context"
SHARED_MEMORY_INDEX = f"{STATE_SHARED_DIR}/shared_memory_index.json"
SHARED_PROFILE_JSON = f"{STATE_SHARED_DIR}/user_profile.json"
SHARED_CONTEXT_JSON = f"{STATE_SHARED_DIR}/agent_context.json"
PERMANENT_DIR = "Memories/Permanent"
PERSONAL_KNOWLEDGE_DIR = "Personal/Agent Knowledge"
AGENT_SKILLS_MD_FILE = f"{PERSONAL_KNOWLEDGE_DIR}/Agent Skills.md"
REFERENCE_AGENT_SKILLS_MD_FILE = f"{DASHBOARD_DIR}/Agent Skills.md"
SHARED_AGENT_SKILLS_JSON = f"{STATE_SHARED_DIR}/agent_skills.json"
DAILY_DIR = "memory"
VAULT_DAILY_DIR = "Sources/openclaw/daily"
REVIEW_DIR = STATE_REVIEW_DIR
REVIEW_PACK_NAME = "latest-pack.json"
STAGES = ("S1", "S2", "S3", "S4")
PREVIOUS_STAGE = {"S2": "S1", "S3": "S2"}
RESERVED_INDEX_KEYS = {INDEX_META, "memories", "daily_refs", "processed_dates", "version", "updated_at"}
AGENT_DAILY_PATTERN = re.compile(rf"^{re.escape(SOURCES_DIR)}/[^/]+/(daily|handoffs)/")
AGENT_EVIDENCE_PATTERN = re.compile(rf"^{re.escape(SOURCES_DIR)}/[^/]+/evidence/")
AGENT_CONVERSATION_PATTERN = re.compile(rf"^{re.escape(SOURCES_DIR)}/[^/]+/conversations/")
AGENT_SUMMARY_PATTERN = re.compile(rf"^{re.escape(SOURCES_DIR)}/[^/]+/(summaries|conversation-summaries)/")
DERIVED_SOURCE_PREFIXES = (
    f"{STATE_INDEX_DIR}/",
    f"{STATE_SHARED_DIR}/",
    f"{STATE_AGENTS_DIR}/",
    f"{MEMORY_PAGES_DIR}/",
    CONTEXT_DIR + "/",
    SHARED_CONTEXT_DIR + "/",
)
INDEX_REFERENCE_KEYS = {"path", "summary_path", "transcript_path", "source_file", "source", "file", "original_context_file"}
ALLOWED_SOURCE_PREFIXES = (
    f"{VAULT_DAILY_DIR}/",
    f"{PERMANENT_DIR}/",
    f"{PERSONAL_KNOWLEDGE_DIR}/",
    f"{SOURCES_DIR}/",
)
LEGACY_SOURCE_MARKERS = ("memory/.dreams/session-corpus/", "main/sessions/", ".jsonl")
MIN_COMPACT_LENGTH = 80
PROCESS_MEMORY_MARKERS = {
    "success_pattern": [
        "success",
        "succeeded",
        "works",
        "verified",
        "passed",
        "final fix",
        "correct approach",
        "\u6210\u529f",
        "\u9a8c\u8bc1\u901a\u8fc7",
        "\u53ef\u884c",
        "\u6700\u7ec8\u65b9\u6848",
        "\u6b63\u786e\u505a\u6cd5",
    ],
    "correction": [
        "correction",
        "corrected",
        "wrong",
        "mistake",
        "should be",
        "instead",
        "\u7ea0\u6b63",
        "\u641e\u9519",
        "\u4e0d\u5bf9",
        "\u5e94\u8be5",
        "\u6539\u6210",
        "\u504f\u5dee",
    ],
    "failure_lesson": [
        "failed",
        "failure",
        "root cause",
        "lesson",
        "do not repeat",
        "regression",
        "\u5931\u8d25",
        "\u5931\u8d25\u539f\u56e0",
        "\u6559\u8bad",
        "\u4e0d\u8981\u518d",
        "\u95ee\u9898\u5728\u4e8e",
        "\u5bfc\u81f4",
    ],
    "user_rule": [
        "agreement",
        "agreed",
        "default should",
        "always",
        "never",
        "must",
        "\u7ea6\u5b9a",
        "\u4ee5\u540e",
        "\u9ed8\u8ba4",
        "\u5fc5\u987b",
        "\u4e0d\u80fd",
        "\u5148\u8ba1\u5212",
    ],
}
PROCESS_MEMORY_MIN_MARKER_HITS = 1
STRONG_KEYWORD_ALLOWLIST: set[str] = set()
OPENCLAW_RECALL_MIN_SCORE = 0.70
OPENCLAW_RECALL_MIN_RECALLS = 1
OPENCLAW_RECALL_MAX_CANDIDATES = 80
OPENCLAW_DREAM_MIN_CONFIDENCE = 0.58

TRIGGER_WORDS = [
    "记得",
    "记忆",
    "回忆",
    "上次",
    "之前",
    "以前",
    "曾经",
    "历史",
    "背景",
    "上下文",
    "仔细想想",
    "想起来",
    "记录",
    "复盘",
    "经验",
    "remember",
    "memory",
    "recall",
    "previous",
    "last time",
    "context",
    "覚えて",
]

BLACKLIST_PATTERNS = [
    r"\bself-check\b",
    r"\bsubagent context\b",
    r"\bdry[- ]run\b",
    r"自检",
    r"闲聊",
]

SOFT_BLACKLIST_PATTERNS = [
    r"\bheartbeat\b",
    r"\bgithub trending\b",
    r"\bgh trending\b",
    r"\breview schedule\b",
    r"\btavily web search\b",
    r"\bgateway\b",
    r"\bredis-server\b",
    r"\bredis\s+service\b",
    r"心跳",
    r"异常上报",
    r"任务卡住",
    r"监控",
    r"gateway",
    r"Redis 服务",
    r"系统日志",
    r"日志警告",
    r"记忆文件状态",
    r"记忆文件断层",
    r"主动跟踪器",
    r"主动任务跟踪",
    r"已恢复正常",
    r"运行正常",
    r"无异常",
    r"安全检查",
    r"严重逾期",
    r"逾期\d+天",
]

HIGH_VALUE_PATTERNS = [
    r"\bsuccess\b",
    r"\bsucceeded\b",
    r"\bverified\b",
    r"\bpassed\b",
    r"\bworks\b",
    r"\bfix(?:ed)?\b",
    r"\bfallback\b",
    r"\btimeout\b",
    r"\bdeploy(?:ed|ment)?\b",
    r"\binstall(?:ed)?\b",
    r"\bmodel\b",
    r"\bonnx\b",
    r"\bsupertonic\b",
    r"\bgithub trending cron\b",
    r"\bgh cli\b",
    r"\btavily\b",
    r"\b403\b",
    r"\bfetch failed\b",
    r"\bcontexttoken\b",
    r"\beconnaborted\b",
    r"成功",
    r"验证通过",
    r"可行",
    r"最终方案",
    r"正确做法",
    r"修复",
    r"已修复",
    r"改成",
    r"改为",
    r"兜底",
    r"失败",
    r"超时",
    r"错误",
    r"部署",
    r"安装",
    r"模型",
    r"需要用户确认",
    r"后续",
    r"经验",
    r"教训",
]

OPERATIONAL_NOISE_PATTERNS: list[tuple[str, list[str]]] = [
    (
        "memory_sync_self_log",
        [
            r"\bmemory-sync\b.*\b(candidates?|coverage|review pack|sync complete|status|skipped=|s1\s*=|s2\s*=|s3\s*=|s4\s*=)\b",
            r"\bagent review pack written\b",
            r"\bpending review pack\b",
            r"\breview apply success\b",
            r"\bno rule-based memories were written\b",
            r"\bcandidates:\s*\d+",
            r"\bcoverage:\s*",
            r"`?review apply`?.{0,80}(成功|added=|discarded=|merged=)",
            r"`?status`?.{0,80}(正常|Memories=|S1=|S2=|S3=|S4=)",
            r"(记忆同步|记忆库同步|记忆库每日同步).{0,160}(Candidates:|Coverage:|review apply|status|Memories=|S1=|S2=|added=|discarded=|同步完成|执行结果)",
        ],
    ),
    (
        "temporary_test_path",
        [
            r"memory-sync-(?:context-)?test",
            r"test-vault",
            r"\btemp[\\/]",
            r"\btmp[\\/]",
            r"测试文件位置",
            r"临时验证",
            r"临时测试",
        ],
    ),
    (
        "routine_status",
        [
            r"\bheartbeat\b.*\b(healthy|normal|ok|passed|success|no errors?|all checks passed)\b",
            r"\b(gateway|redis|redis-server)\s+(healthy|normal|ok|running)\b",
            r"\bsystem\s+(normal|healthy|ok)\b",
            r"\b(no errors?|no exception|all checks passed)\b",
            r"心跳.*(正常|健康|通过|无错误|无异常)",
            r"自检.*(正常|健康|通过|无错误|无异常)",
            r"Gateway\s*(healthy|正常|健康)",
            r"Redis.*(运行正常|正常|健康)",
            r"系统正常",
            r"运行正常",
            r"无错误",
            r"无异常",
            r"安全检查通过",
            r"检查通过",
        ],
    ),
    (
        "duplicate_operational_status",
        [
            r"\boverdue\s*\d+\s*days?\b",
            r"逾期\s*\d+\s*天",
            r"Git\s*逾期\s*\d+\s*天",
        ],
    ),
]

DURABLE_VALUE_PATTERNS = [
    r"\bdecision\b",
    r"\bdecided\b",
    r"\bcorrection\b",
    r"\bcorrected\b",
    r"\bwrong\b",
    r"\bmistake\b",
    r"\bfailed?\b",
    r"\bfailure\b",
    r"\broot cause\b",
    r"\blesson\b",
    r"\bfix(?:ed)?\b",
    r"\bfallback\b",
    r"\bworkaround\b",
    r"\btimeout\b",
    r"\bblocked?\b",
    r"\btodo\b",
    r"\bnext action\b",
    r"\bmust\b",
    r"\bnever\b",
    r"\bshould\b",
    r"\bchanged?\b",
    r"\bconfigured?\b",
    r"\brecovered?\b",
    r"\brate[_ -]?limit\b",
    r"\b429\b",
    r"决定",
    r"结论",
    r"纠正",
    r"搞错",
    r"不对",
    r"失败",
    r"失败原因",
    r"根因",
    r"原因是",
    r"教训",
    r"修复",
    r"已修复",
    r"改成",
    r"改为",
    r"恢复",
    r"验证恢复",
    r"超时",
    r"报错",
    r"错误原因",
    r"阻塞",
    r"待办",
    r"下一步",
    r"约定",
    r"必须",
    r"不能",
    r"应该",
    r"用户要求",
    r"用户纠正",
]

GENERIC_WORDS = {
    "the",
    "and",
    "for",
    "with",
    "this",
    "that",
    "from",
    "openclaw",
    "memory",
    "sync",
    "记忆",
    "同步",
    "上次",
    "之前",
    "以前",
    "我们",
    "讨论",
    "问题",
    "这个",
    "那个",
    "文件",
    "系统",
    "功能",
    "内容",
    "命令",
    "执行",
    "查看",
    "现在",
    "可以",
    "需要",
    "已经",
    "进行",
    "结果",
    "使用",
    "操作",
    "context",
    "previous",
    "issue",
    "file",
    "system",
    "function",
}

STOPWORDS = GENERIC_WORDS | {word.lower() for word in TRIGGER_WORDS}

DOMAIN_PHRASES = [
    "memory-sync",
    "openclaw_memory_index",
    "openclaw",
    "obsidian",
    "github",
    "git",
    "autopilot",
    "记忆同步",
    "用进废退",
    "单一索引",
    "索引文件",
    "触发词",
    "命中冷却",
    "命中质量",
    "单一触发词",
    "关键词匹配",
    "自动驾驶",
    "版本管理",
    "每日文件",
    "永久记忆",
    "反作弊",
]

TECH_HINTS = [
    "api",
    "json",
    "yaml",
    "yml",
    "toml",
    "env",
    "md",
    "py",
    "skill",
    "index",
    "trigger",
    "github",
    "git",
    "obsidian",
    "openclaw",
    "触发",
    "冷却",
    "命中",
    "去重",
    "架构",
    "版本",
    "仓库",
]


BROAD_MATCH_KEYWORDS = {
    "api",
    "git",
    "github",
    "index",
    "json",
    "jsonl",
    "md",
    "openclaw",
    "obsidian",
    "py",
    "python",
    "skill",
    "trigger",
}

BLOCKED_KEYWORD_PATTERNS = [
    re.compile(r"(^|/)memory/\.dreams/session-corpus/", re.IGNORECASE),
    re.compile(r"(^|/)main/sessions/", re.IGNORECASE),
    re.compile(r"\.jsonl$", re.IGNORECASE),
    re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.IGNORECASE),
    re.compile(r"^[a-z]:[\\/]", re.IGNORECASE),
    re.compile(r"[\\/].+[\\/]", re.IGNORECASE),
]

PROFILE_LABEL_BLOCKLIST = GENERIC_WORDS | BROAD_MATCH_KEYWORDS | {
    "name",
    "what",
    "to",
    "call",
    "them",
    "what to call them",
    "assistant",
    "pronouns",
    "timezone",
    "style",
    "coding style",
    "代码偏好",
    "user",
    "human",
    "you",
    "your",
    "don",
    "dont",
    "don't",
    "today",
    "yesterday",
    "tomorrow",
    "workspace",
    "rule",
    "rules",
    "note",
    "notes",
    "source",
    "sources",
    "command",
    "cmd",
    "pattern",
    "decision",
    "allow",
    "prefix_rule",
    "gateway",
    "trending",
    "review",
    "schedule",
    "scraping",
    "transcript",
    "hidden transcript",
    "memory.md",
    "memories",
    "user.md",
    "agents.md",
    "tools.md",
    "soul.md",
    "memory/yyyy-mm-dd.md",
    "关注领域",
    "github 开发者",
}

PROJECT_HINT_KEYWORDS = {
    "memory-sync",
    "autotestplatform",
    "openclaw",
    "obsidian",
    "codex",
    "claude",
    "opencode",
    "hermes-agent",
}

PATH_LIKE_PATTERN = re.compile(
    r"[A-Za-z]:[\\/][^\s`'\"<>|]+|[\w.-]+(?:[\\/][\w.-]+)+|[\w.-]+\.(?:py|md|json|jsonl|yaml|yml|toml|env|txt)",
    re.IGNORECASE,
)


def read_json_config(name: str) -> dict[str, Any]:
    path = ROOT / "config" / name
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Config file is invalid JSON: {path} ({exc})") from exc
    if not isinstance(data, dict):
        raise ValueError(f"Config file must contain a JSON object: {path}")
    return data


def list_config(data: dict[str, Any], key: str) -> list[str] | None:
    value = data.get(key)
    if value is None:
        return None
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"Config key must be a list of strings: {key}")
    return value


def apply_rule_config() -> None:
    global BLACKLIST_PATTERNS, BROAD_MATCH_KEYWORDS, DOMAIN_PHRASES, GENERIC_WORDS
    global LEGACY_SOURCE_MARKERS, MIN_COMPACT_LENGTH, STOPWORDS, STRONG_KEYWORD_ALLOWLIST
    global TRIGGER_WORDS, BLOCKED_KEYWORD_PATTERNS, OPENCLAW_RECALL_MIN_SCORE
    global OPENCLAW_RECALL_MIN_RECALLS, OPENCLAW_RECALL_MAX_CANDIDATES, OPENCLAW_DREAM_MIN_CONFIDENCE
    global SOFT_BLACKLIST_PATTERNS, HIGH_VALUE_PATTERNS

    filters = read_json_config("filters.json")
    keywords = read_json_config("keywords.json")
    triggers = read_json_config("triggers.json")

    configured = list_config(filters, "hard_blacklist_patterns")
    if configured is not None:
        BLACKLIST_PATTERNS = configured
    elif (configured := list_config(filters, "blacklist_patterns")) is not None:
        # Backward compatible with older config files. New configs should prefer
        # hard_blacklist_patterns plus soft_blacklist_patterns.
        BLACKLIST_PATTERNS = configured

    configured = list_config(filters, "soft_blacklist_patterns")
    if configured is not None:
        SOFT_BLACKLIST_PATTERNS = configured

    configured = list_config(filters, "high_value_patterns")
    if configured is not None:
        HIGH_VALUE_PATTERNS = configured

    configured = list_config(filters, "blocked_source_markers")
    if configured is not None:
        LEGACY_SOURCE_MARKERS = tuple(configured)

    if "min_compact_length" in filters:
        try:
            MIN_COMPACT_LENGTH = int(filters["min_compact_length"])
        except (TypeError, ValueError) as exc:
            raise ValueError("Config key must be an integer: min_compact_length") from exc

    if "openclaw_recall_min_score" in filters:
        try:
            OPENCLAW_RECALL_MIN_SCORE = float(filters["openclaw_recall_min_score"])
        except (TypeError, ValueError) as exc:
            raise ValueError("Config key must be a number: openclaw_recall_min_score") from exc

    if "openclaw_recall_min_recalls" in filters:
        try:
            OPENCLAW_RECALL_MIN_RECALLS = int(filters["openclaw_recall_min_recalls"])
        except (TypeError, ValueError) as exc:
            raise ValueError("Config key must be an integer: openclaw_recall_min_recalls") from exc

    if "openclaw_recall_max_candidates" in filters:
        try:
            OPENCLAW_RECALL_MAX_CANDIDATES = int(filters["openclaw_recall_max_candidates"])
        except (TypeError, ValueError) as exc:
            raise ValueError("Config key must be an integer: openclaw_recall_max_candidates") from exc

    if "openclaw_dream_min_confidence" in filters:
        try:
            OPENCLAW_DREAM_MIN_CONFIDENCE = float(filters["openclaw_dream_min_confidence"])
        except (TypeError, ValueError) as exc:
            raise ValueError("Config key must be a number: openclaw_dream_min_confidence") from exc

    configured = list_config(keywords, "generic_words")
    if configured is not None:
        GENERIC_WORDS = set(configured)

    configured = list_config(keywords, "broad_context_keywords")
    if configured is not None:
        BROAD_MATCH_KEYWORDS = {normalize_keyword(item) for item in configured}

    configured = list_config(keywords, "domain_phrases")
    if configured is not None:
        DOMAIN_PHRASES = configured

    configured = list_config(keywords, "strong_keyword_allowlist")
    if configured is not None:
        STRONG_KEYWORD_ALLOWLIST = {normalize_keyword(item) for item in configured}

    configured = list_config(keywords, "blocked_keyword_patterns")
    if configured is not None:
        BLOCKED_KEYWORD_PATTERNS = [re.compile(pattern, re.IGNORECASE) for pattern in configured]

    configured = list_config(triggers, "trigger_words")
    if configured is not None:
        TRIGGER_WORDS = configured

    STOPWORDS = GENERIC_WORDS | {word.lower() for word in TRIGGER_WORDS}


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env(ROOT / ".env")


def default_hermes_home() -> str:
    if os.name == "nt":
        local_appdata = os.environ.get("LOCALAPPDATA", "")
        if local_appdata:
            candidate = Path(local_appdata) / "hermes"
            if candidate.exists():
                return str(candidate)
    return "~/.hermes"


def env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def env_float(name: str, default: float) -> float:
    value = os.environ.get(name)
    if not value:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def env_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


CONFIG = {
    "OPENCLAW_WORKSPACE": os.environ.get("OPENCLAW_WORKSPACE", "~/.openclaw/workspace"),
    "VAULT_PATH": os.environ.get("OBSIDIAN_VAULT_PATH", "~/Documents/obsidian/vault"),
    "HIT_COOLDOWN_HOURS": env_int("HIT_COOLDOWN_HOURS", 24),
    "S1_TTL_MIN_DAYS": env_int("S1_TTL_MIN_DAYS", 3),
    "S1_TTL_MAX_DAYS": env_int("S1_TTL_MAX_DAYS", 10),
    "NOISE_MIN_HITS": env_int("NOISE_MIN_HITS", 5),
    "NOISE_DOMINANCE_RATIO": env_float("NOISE_DOMINANCE_RATIO", 0.8),
    "GIT_SYNC_ENABLED": env_bool("GIT_SYNC_ENABLED", False),
    "GIT_PUSH_ENABLED": env_bool("GIT_PUSH_ENABLED", True),
    "GIT_REMOTE": os.environ.get("GIT_REMOTE", "origin"),
    "GIT_BRANCH": os.environ.get("GIT_BRANCH", ""),
    "OPENCLAW_IMPORT_DISTILLED": env_bool("OPENCLAW_IMPORT_DISTILLED", True),
    "CONTEXT_EXPORT_ENABLED": env_bool("CONTEXT_EXPORT_ENABLED", True),
    "LEGACY_CONTEXT_ENABLED": env_bool("LEGACY_CONTEXT_ENABLED", False),
    "DERIVED_OUTPUTS_ENABLED": env_bool("DERIVED_OUTPUTS_ENABLED", True),
    "REVIEW_MODE": os.environ.get("MEMORY_SYNC_REVIEW_MODE", "agent").strip().lower() or "agent",
    "CODEX_HOME": os.environ.get("CODEX_HOME", "~/.codex"),
    "CLAUDE_HOME": os.environ.get("CLAUDE_HOME", "~/.claude"),
    "HERMES_HOME": os.environ.get("HERMES_HOME") or default_hermes_home(),
    "QODER_HOME": os.environ.get("QODER_HOME", os.environ.get("APPDATA", "") + "/Qoder"),
}

CONTEXT_ADAPTER_LIST = "|".join(("all", *ADAPTER_NAMES))


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def parse_jsonl_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed
    return parsed.astimezone()


def parse_unix_timestamp(value: Any) -> datetime | None:
    if value is None:
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return parse_jsonl_time(str(value))
    if numeric <= 0:
        return None
    if numeric > 10_000_000_000:
        numeric = numeric / 1000
    try:
        return datetime.fromtimestamp(numeric)
    except (OverflowError, OSError, ValueError):
        return None


def expand_path(value: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(value))).resolve()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_summary(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = len(text.splitlines())
    except OSError:
        lines = None
    return {
        "path": path.as_posix(),
        "size": path.stat().st_size,
        "sha256": file_hash(path)[:16],
        "lines": lines,
    }


def safe_name(value: str, limit: int = 80) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", value).strip(" .-")
    cleaned = re.sub(r"\s+", "-", cleaned)
    return (cleaned or "memory")[:limit]


def contains_cjk(text: str) -> bool:
    return bool(re.search(r"[\u3400-\u9fff]", text))


def agent_skill_markdown_rel(agent: str) -> str:
    return f"{PERSONAL_KNOWLEDGE_DIR}/{agent}/Agent Skills.md"


SKILL_ROUTING_CATEGORIES = [
    {
        "name": "开发与调试",
        "name_en": "Development And Debugging",
        "intro": "用于实现、修改、诊断或修复代码。先判断任务是平台专用、语言或框架专用、测试平台操作，还是通用故障诊断。",
        "intro_en": "Use for implementing, changing, diagnosing, or fixing code. First decide whether the task is platform-specific, language/framework-specific, test-platform work, or general debugging.",
        "priority": "平台专用 > 语言或框架专用 > 通用调试 > 通用开发",
        "priority_en": "Platform-specific > language/framework-specific > general debugging > general development",
        "skills": {"node-inspect-debugger", "python-debugpy", "vue-expert", "opencli-autofix", "opencli-explorer", "opencli-oneshot", "auto-test-platform"},
        "keywords": ("debug", "fix", "code", "python", "node", "vue", "test", "测试", "调试", "修复", "代码"),
    },
    {
        "name": "规划与任务执行",
        "name_en": "Planning And Task Execution",
        "intro": "用于拆解任务、验证方案、维护待办或运行长期任务流。先区分一次性方案验证、个人任务管理和持久化多阶段流程。",
        "intro_en": "Use for decomposing tasks, validating approaches, maintaining todos, or running durable multi-step workflows.",
        "priority": "专用工作流 > 持久任务编排 > 个人任务管理 > 临时方案验证",
        "priority_en": "Dedicated workflow > durable orchestration > personal task management > temporary validation",
        "skills": {"apple-reminders", "spike", "taskflow", "taskflow-inbox-triage", "things-mac", "trello"},
        "keywords": ("task", "todo", "reminder", "workflow", "prototype", "validate", "计划", "任务", "待办", "验证"),
    },
    {
        "name": "代码审查与质量",
        "name_en": "Code Review And Quality",
        "intro": "用于审查代码、处理 GitHub 问题、复核方案或约束编码质量。优先选择与代码平台或审查方法直接匹配的 Skill。",
        "intro_en": "Use for reviewing code, handling GitHub issues, checking plans, or enforcing coding quality.",
        "priority": "平台问题处理 > 专用审查器 > 编码规范",
        "priority_en": "Platform issue handling > dedicated reviewer > coding guidelines",
        "skills": {"gh-issues", "github", "oracle", "karpathy-skills"},
        "keywords": ("review", "github", "issue", "pull request", "pr", "quality", "审查", "质量", "规范"),
    },
    {
        "name": "Agent 与自动化编排",
        "name_en": "Agent And Automation Orchestration",
        "intro": "用于调用外部编码 Agent、组织多 Agent 团队、连接 MCP 工具或约束 Agent 执行流程。",
        "intro_en": "Use for calling external coding agents, organizing multi-agent teams, connecting MCP tools, or constraining agent execution.",
        "priority": "明确指定的 Agent > 专用委派器 > 团队编排 > 通用 Agent 行为",
        "priority_en": "Explicit target agent > dedicated delegator > team orchestration > generic agent behavior",
        "skills": {"coding-agent", "gemini", "mcporter", "cursor-agent", "proactive-agent", "using-superpowers", "Codex", "agent-team-orchestration", "codex-cli", "openai-codex-operator", "Claude Code CLI for OpenClaw"},
        "keywords": ("agent", "codex", "claude", "gemini", "mcp", "delegate", "orchestrate", "自动化", "编排", "委派"),
    },
    {
        "name": "搜索与研究",
        "name_en": "Search And Research",
        "intro": "用于网络搜索、网站信息检索、地点与天气查询、订阅监控和多格式内容摘要。先判断是否需要指定数据源或仅做摘要。",
        "intro_en": "Use for web search, source-specific lookup, places/weather queries, feed monitoring, and multi-format summarization.",
        "priority": "指定平台或数据源 > 智能搜索路由 > 通用网页搜索 > 摘要",
        "priority_en": "Specified platform/source > smart search router > general web search > summarization",
        "skills": {"blogwatcher", "goplaces", "summarize", "weather", "smart-search", "web-search"},
        "keywords": ("search", "research", "summary", "summarize", "weather", "places", "搜索", "查询", "摘要", "研究"),
    },
    {
        "name": "文档与知识管理",
        "name_en": "Documents And Knowledge Management",
        "intro": "用于创建、转换、编辑或管理文档、笔记与知识库。优先选择目标文件格式或目标平台专用 Skill。",
        "intro_en": "Use for creating, converting, editing, or managing documents, notes, and knowledge bases.",
        "priority": "目标平台专用 > 文件格式专用 > 通用转换",
        "priority_en": "Target platform > file format > general conversion",
        "skills": {"apple-notes", "bear-notes", "nano-pdf", "notion", "obsidian", "ai-ppt-generator", "docx", "markdown-converter", "pdf", "feishu-doc-best-practices"},
        "keywords": ("document", "pdf", "docx", "markdown", "note", "notion", "obsidian", "文档", "知识", "笔记"),
    },
    {
        "name": "数据与分析",
        "name_en": "Data And Analysis",
        "intro": "用于统计使用量、分析结构化数据或生成专项分析结果；不承接已有专业金融 Skill 能覆盖的任务。",
        "intro_en": "Use for usage statistics, structured data analysis, or specialized analytical output when no domain skill is a better fit.",
        "priority": "领域专用分析 > 数据源专用 > 通用统计",
        "priority_en": "Domain analysis > source-specific analysis > general statistics",
        "skills": {"model-usage"},
        "keywords": ("data", "analysis", "usage", "stats", "analytics", "数据", "分析", "统计"),
    },
    {
        "name": "图像与视觉设计",
        "name_en": "Image And Visual Design",
        "intro": "用于生成图表、界面设计、GIF、模因或视觉定位。先区分设计产出、媒体搜索和截图坐标识别。",
        "intro_en": "Use for diagrams, UI design, GIFs, memes, or visual element location.",
        "priority": "目标产物专用 > UI 设计 > 图像搜索或生成 > 视觉定位",
        "priority_en": "Target output > UI design > image search/generation > visual locating",
        "skills": {"canvas", "diagram-maker", "gifgrep", "meme-maker", "frontend-design", "screenshot-ui-locator"},
        "keywords": ("image", "visual", "diagram", "gif", "meme", "ui", "screenshot", "图像", "视觉", "截图", "设计"),
    },
    {
        "name": "音频与视频",
        "name_en": "Audio And Video",
        "intro": "用于音视频转录、语音合成、帧提取、摄像头采集和音频可视化。优先选择输入与输出格式完全匹配的 Skill。",
        "intro_en": "Use for transcription, text-to-speech, frame extraction, camera capture, and audio visualization.",
        "priority": "专用媒体操作 > 本地处理 > 云 API",
        "priority_en": "Dedicated media operation > local processing > cloud API",
        "skills": {"camsnap", "openai-whisper", "openai-whisper-api", "sag", "sherpa-onnx-tts", "songsee", "video-frames", "ai-notes-of-video"},
        "keywords": ("audio", "video", "speech", "tts", "whisper", "frame", "camera", "音频", "视频", "语音", "转录"),
    },
    {
        "name": "内容创作与运营",
        "name_en": "Content Creation And Operations",
        "intro": "用于短视频脚本、内容选题、预测复盘、平台发布和小红书运营。这是有复用价值的扩展大类。",
        "intro_en": "Use for scripts, topic selection, content prediction/retro, publishing, and platform operations.",
        "priority": "平台专用操作 > 已安装内容工作流子 Skill > 通用内容生成",
        "priority_en": "Platform operation > installed content workflow > general content generation",
        "skills": {"ai-video-script", "douyin-publish", "xhs-auth", "xhs-content-ops", "xhs-explore", "xhs-interact", "xhs-publish", "xiaohongshu-skills", "cheat-bump", "cheat-init", "cheat-learn-from", "cheat-migrate", "cheat-on-content", "cheat-predict", "cheat-publish", "cheat-recommend", "cheat-retro", "cheat-score", "cheat-score-blind", "cheat-seed", "cheat-shoot", "cheat-status", "cheat-trends"},
        "keywords": ("content", "script", "publish", "video", "topic", "xhs", "douyin", "内容", "脚本", "发布", "选题", "小红书"),
    },
    {
        "name": "通信与协作平台",
        "name_en": "Communication And Collaboration",
        "intro": "用于发送、读取或管理邮件、即时消息、工作区内容和社交平台交互。必须优先选择用户明确指定的平台。",
        "intro_en": "Use for email, messaging, workspace content, and social-platform operations.",
        "priority": "指定平台 > 指定消息类型 > 通用协作套件",
        "priority_en": "Specified platform > message type > collaboration suite",
        "skills": {"discord", "gog", "himalaya", "imsg", "slack", "voice-call", "wacli", "xurl"},
        "keywords": ("mail", "message", "slack", "discord", "gmail", "calendar", "whatsapp", "x ", "邮件", "消息", "协作"),
    },
    {
        "name": "浏览器与桌面操作",
        "name_en": "Browser And Desktop Operations",
        "intro": "用于浏览器自动化、桌面控制、远程控制和 macOS UI 操作。先判断目标是网页、桌面、远程设备还是截图定位。",
        "intro_en": "Use for browser automation, desktop control, remote control, and macOS UI operations.",
        "priority": "目标平台专用 > 浏览器会话自动化 > 桌面或远程控制 > 通用 UI 定位",
        "priority_en": "Target platform > browser automation > desktop/remote control > UI locating",
        "skills": {"peekaboo", "Agent Browser", "antigravity", "awesun-remote-control", "desktop-control", "opencli-browser", "opencli-usage"},
        "keywords": ("browser", "desktop", "click", "screen", "remote", "网页", "浏览器", "桌面", "远程"),
    },
    {
        "name": "DevOps 与系统运维",
        "name_en": "DevOps And System Operations",
        "intro": "用于终端会话、设备连接和系统级运行维护。涉及安全加固时转到“安全与凭证”。",
        "intro_en": "Use for terminal sessions, device connection, and system operations. Security hardening belongs under security.",
        "priority": "设备或平台专用 > 终端会话管理 > 通用运维",
        "priority_en": "Device/platform-specific > terminal session management > general operations",
        "skills": {"node-connect", "tmux"},
        "keywords": ("devops", "system", "terminal", "tmux", "node", "ops", "系统", "终端", "运维"),
    },
    {
        "name": "安全与凭证",
        "name_en": "Security And Credentials",
        "intro": "用于凭证管理、主机安全审计和系统加固。任何可能修改安全设置的操作都应先确认权限和影响。",
        "intro_en": "Use for credential management, host security audit, and hardening. Confirm impact before changing security settings.",
        "priority": "凭证专用 > 平台安全审计 > 通用加固",
        "priority_en": "Credential-specific > platform audit > general hardening",
        "skills": {"1password", "healthcheck"},
        "keywords": ("secret", "password", "credential", "security", "audit", "凭证", "密码", "安全"),
    },
    {
        "name": "金融与专业领域",
        "name_en": "Finance And Professional Domains",
        "intro": "用于金融数据、股票分析、模拟交易和专业金融 Agent。不得用通用数据分析替代已有领域 Skill。",
        "intro_en": "Use for financial data, stock analysis, simulated trading, and specialized finance agents.",
        "priority": "操作型专用 Skill > 数据源专用 > 分析模型 > 专家 Agent 集合",
        "priority_en": "Operational skill > data-source skill > analytical model > expert-agent collection",
        "skills": {"china-stock-analysis", "mx-moni", "agency-agents-finance", "mx_data", "mx_select_stock", "mx_selfselect"},
        "keywords": ("finance", "stock", "trading", "investment", "金融", "股票", "交易", "投资"),
    },
    {
        "name": "Skill 与插件管理",
        "name_en": "Skill And Plugin Management",
        "intro": "用于发现、创建、验证、安装或发布 Agent Skill，以及维护 Agent 的能力目录。",
        "intro_en": "Use for finding, creating, validating, installing, publishing, and maintaining agent skills.",
        "priority": "具体创建或发布工具 > Skill 发现 > 通用管理",
        "priority_en": "Creation/publishing tool > skill discovery > general management",
        "skills": {"clawhub", "skill-creator", "find-skills"},
        "keywords": ("skill", "plugin", "clawhub", "publish", "install", "技能", "插件", "发布"),
    },
    {
        "name": "记忆与上下文",
        "name_en": "Memory And Context",
        "intro": "用于检索历史会话、沉淀经验、同步记忆和迁移跨 Agent 上下文。先区分原始日志检索、持续改进和持久化记忆。",
        "intro_en": "Use for historical session lookup, lessons, memory sync, and cross-agent context portability.",
        "priority": "明确记忆同步 > 历史日志检索 > 纠错与持续改进",
        "priority_en": "Explicit memory sync > session-log lookup > correction and improvement",
        "skills": {"session-logs", "memory-sync", "self-improvement"},
        "keywords": ("memory", "context", "session", "history", "improvement", "记忆", "上下文", "历史", "复盘"),
    },
    {
        "name": "其他专用能力",
        "name_en": "Other Specialized Capabilities",
        "intro": "用于智能家居、媒体播放、外卖订单等无法稳定归入其他大类的设备或服务专用操作。",
        "intro_en": "Use for device or service-specific operations that do not fit stable reusable categories.",
        "priority": "用户明确指定的设备或服务 > 最窄能力边界",
        "priority_en": "Explicit device/service > narrowest boundary",
        "skills": {"blucli", "eightctl", "openhue", "ordercli", "sonoscli", "spotify-player"},
        "keywords": ("device", "speaker", "music", "order", "home", "设备", "音箱", "订单", "家居"),
    },
]

SKILL_ROUTING_FIELD_NAMES = (
    "identity",
    "primary_category",
    "related_categories",
    "use_when",
    "avoid_when",
    "specificity",
    "routing_status",
    "routing_confidence",
    "routing_source",
    "routing_reviewed_sha256",
)


def skill_route_identity(agent: str, record: dict[str, Any]) -> str:
    return f"{agent}|{record.get('level', '')}|{record.get('relative_path', '')}"


def skill_route_has_valid_fields(record: dict[str, Any]) -> bool:
    return bool(record.get("identity") and record.get("primary_category") and record.get("routing_status"))


def skill_route_category_for_name(name: str) -> dict[str, Any] | None:
    for category in SKILL_ROUTING_CATEGORIES:
        if name in category["skills"]:
            return category
    return None


def classify_skill_route(record: dict[str, Any]) -> tuple[dict[str, Any], list[str], float, str]:
    category = skill_route_category_for_name(str(record.get("name", "")))
    description = str(record.get("description", ""))
    haystack = f"{record.get('name', '')} {description} {record.get('relative_path', '')}".lower()
    best_score = 0
    best_category: dict[str, Any] | None = category
    if category is None:
        for candidate in SKILL_ROUTING_CATEGORIES:
            score = sum(1 for keyword in candidate["keywords"] if keyword.lower() in haystack)
            if score > best_score:
                best_score = score
                best_category = candidate
    if best_category is None:
        best_category = SKILL_ROUTING_CATEGORIES[-1]
        confidence = 0.35
    elif category is not None:
        confidence = 0.84
    else:
        confidence = min(0.78, 0.42 + best_score * 0.12)

    related: list[str] = []
    lowered_name = str(record.get("name", "")).lower()
    if "codex" in lowered_name or "claude" in lowered_name or "coding" in haystack:
        for rel in ("开发与调试", "代码审查与质量"):
            if rel != best_category["name"] and rel not in related:
                related.append(rel)
    if "memory" in haystack and best_category["name"] != "记忆与上下文":
        related.append("记忆与上下文")
    if "document" in haystack or "markdown" in haystack or "obsidian" in haystack:
        if best_category["name"] != "文档与知识管理":
            related.append("文档与知识管理")

    specificity = "general"
    if any(token in haystack for token in ("github", "obsidian", "slack", "discord", "notion", "codex", "claude", "xhs", "douyin")):
        specificity = "platform"
    elif any(token in haystack for token in ("python", "node", "vue", "pdf", "docx", "whisper")):
        specificity = "format_or_framework"
    elif best_category["name"] in {"金融与专业领域", "内容创作与运营", "记忆与上下文"}:
        specificity = "domain"

    return best_category, related, confidence, specificity


def route_skill_records(agent: str, records: list[dict[str, Any]], previous_records: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    previous_records = previous_records or []
    previous_by_identity = {
        str(record.get("identity") or skill_route_identity(agent, record)): record
        for record in previous_records
    }
    has_previous = bool(previous_by_identity)
    routed: list[dict[str, Any]] = []
    for record in records:
        item = dict(record)
        identity = skill_route_identity(agent, item)
        item["identity"] = identity
        previous = previous_by_identity.get(identity)
        category, related, confidence, specificity = classify_skill_route(item)
        description = str(item.get("description", "")).strip()
        weak_description = not description or description == "|" or description == "No description provided."

        if previous and str(previous.get("sha256")) == str(item.get("sha256")) and skill_route_has_valid_fields(previous):
            for field in SKILL_ROUTING_FIELD_NAMES:
                if field in previous:
                    item[field] = previous[field]
            item["identity"] = identity
        else:
            if previous and skill_route_has_valid_fields(previous):
                item["primary_category"] = previous.get("primary_category") or category["name"]
                item["related_categories"] = list(previous.get("related_categories") or related)
                previous_use_when = list(previous.get("use_when") or [])
                item["use_when"] = previous_use_when or ([compact_text(description, 180)] if description else [])
                item["avoid_when"] = list(previous.get("avoid_when") or [])
                item["specificity"] = previous.get("specificity") or specificity
                item["routing_status"] = "needs_review"
                item["routing_confidence"] = min(float(previous.get("routing_confidence") or confidence), 0.65)
                item["routing_source"] = "preserved"
                item["routing_reviewed_sha256"] = previous.get("routing_reviewed_sha256") or previous.get("sha256", "")
            else:
                item["primary_category"] = category["name"]
                item["related_categories"] = related
                item["use_when"] = [compact_text(description, 180)] if description and description != "|" else []
                item["avoid_when"] = []
                item["specificity"] = specificity
                if weak_description or not item.get("frontmatter_valid", True):
                    item["routing_status"] = "needs_review"
                elif has_previous:
                    item["routing_status"] = "pending_review"
                else:
                    item["routing_status"] = "rule_suggested"
                item["routing_confidence"] = round(confidence, 2)
                item["routing_source"] = "rule"
                item["routing_reviewed_sha256"] = ""
        routed.append(item)
    return routed


def parse_skill_frontmatter(text: str) -> tuple[dict[str, str], bool]:
    if not text.startswith("---"):
        return {}, False
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, False
    data: dict[str, str] = {}
    for raw in parts[1].splitlines():
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, True


def parse_skill_doc(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    frontmatter, valid = parse_skill_frontmatter(text)
    name = frontmatter.get("name") or path.parent.name
    description = frontmatter.get("description", "").strip()
    if not description:
        body = text.split("---", 2)[-1] if text.startswith("---") else text
        for line in body.splitlines():
            clean = line.strip(" #\t-")
            if clean and not clean.lower().startswith("use this skill"):
                description = clean
                break
    return {
        "name": name,
        "description": compact_text(description or "No description provided.", 220),
        "path": path.as_posix(),
        "frontmatter_valid": valid and bool(name),
        "last_modified": datetime.fromtimestamp(path.stat().st_mtime).replace(microsecond=0).isoformat(),
        "sha256": file_hash(path)[:16],
        "enabled": ".disabled" not in path.as_posix().lower(),
    }


def parse_skill_manifest(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in text.splitlines():
        bullet = re.match(r"\s*-\s+\*\*([^*]+)\*\*\s+-\s+(.+)", raw)
        if bullet:
            result[bullet.group(1).strip()] = bullet.group(2).strip()
            continue
        table = re.match(r"\s*\|\s*([^|`*]+?)\s*\|\s*([^|]+?)\s*\|", raw)
        if table:
            name = table.group(1).strip()
            desc = table.group(2).strip()
            if name and desc and name.lower() not in {"skill", "---"}:
                result[name] = desc
    return result


def keyword_set(memory: dict[str, Any]) -> set[str]:
    source = memory.get("strong_keywords") or memory.get("keywords", [])
    return {normalize_keyword(str(item)) for item in source if not is_generic_keyword(str(item))}


def is_conversation_memory(memory: dict[str, Any]) -> bool:
    origin = str(memory.get("candidate_origin", ""))
    return memory.get("memory_lane") == "conversation" or origin.endswith("-conversation-archive")


def same_file_different_anchor(left: dict[str, Any], right: dict[str, Any]) -> bool:
    left_file = normalize_rel_path(left.get("source_file"))
    right_file = normalize_rel_path(right.get("source_file"))
    if not left_file or left_file != right_file:
        return False
    return str(left.get("source_anchor", "")).strip() != str(right.get("source_anchor", "")).strip()


def normalize_keyword(value: str) -> str:
    value = value.strip().strip("`*_#[]()<>:：，,。.!！?？;；")
    return re.sub(r"\s+", " ", value).lower()


def is_legacy_source(value: str | None) -> bool:
    source = str(value or "").replace("\\", "/").lower()
    return any(marker in source for marker in LEGACY_SOURCE_MARKERS)


def normalize_rel_path(value: str | None) -> str:
    return str(value or "").replace("\\", "/").strip("/")


def legacy_rel_path_candidates(value: str | None) -> list[str]:
    source = normalize_rel_path(value)
    if not source:
        return []
    candidates = [source]
    prefix_map = [
        ("02-Lessons/OpenClaw-Daily/", f"{VAULT_DAILY_DIR}/"),
        ("03-Reference/OpenClaw-Permanent/", f"{PERMANENT_DIR}/"),
        ("03-Reference/Memories/", f"{MEMORY_PAGES_DIR}/"),
        ("03-Reference/", f"{DASHBOARD_DIR}/"),
        ("_index/", f"{STATE_INDEX_DIR}/"),
        ("_shared/context/", f"{SHARED_CONTEXT_DIR}/"),
        ("_shared/", f"{STATE_SHARED_DIR}/"),
        ("_review/memory-sync/", f"{STATE_REVIEW_DIR}/"),
    ]
    for old, new in prefix_map:
        if source.startswith(old):
            candidates.append(new + source[len(old):])
    match = re.match(r"^_agents/([^/]+)/(daily|handoffs|evidence|conversations|permanent)/(.+)$", source)
    if match:
        agent, lane, rest = match.groups()
        candidates.append(f"{SOURCES_DIR}/{agent}/{lane}/{rest}")
    match = re.match(r"^_agents/([^/]+)/(summaries|index\.json|skills\.json|skills\.md)(?:/(.+))?$", source)
    if match:
        agent, lane, rest = match.groups()
        suffix = f"{lane}/{rest}" if rest else lane
        candidates.append(f"{STATE_AGENTS_DIR}/{agent}/{suffix}")
    deduped: list[str] = []
    for candidate in candidates:
        if candidate and candidate not in deduped:
            deduped.append(candidate)
    return deduped


def source_type_for(value: str | None) -> str:
    source = str(value or "").replace("\\", "/")
    if source.startswith(f"{VAULT_DAILY_DIR}/"):
        return "daily_copy"
    if AGENT_DAILY_PATTERN.match(source):
        return "agent_daily"
    if AGENT_EVIDENCE_PATTERN.match(source):
        return "agent_evidence"
    if AGENT_CONVERSATION_PATTERN.match(source):
        return "agent_conversation"
    if source.startswith(f"{PERSONAL_KNOWLEDGE_DIR}/"):
        return "personal_knowledge"
    if source.startswith(f"{PERMANENT_DIR}/"):
        return "permanent"
    if AGENT_SUMMARY_PATTERN.match(source):
        return "agent_summary_derived"
    if source.startswith(f"{SHARED_DIR}/"):
        return "shared_derived"
    if source.startswith(f"{STATE_AGENTS_DIR}/"):
        return "agent_summary_derived"
    if source.startswith(f"{STATE_INDEX_DIR}/") or source.startswith("_index/"):
        return "index_derived"
    if source.startswith(f"{MEMORY_PAGES_DIR}/"):
        return "memory_page_derived"
    if source.startswith(f"{CONTEXT_DIR}/") or source.startswith(f"{SHARED_CONTEXT_DIR}/"):
        return "context_derived"
    for translated in legacy_rel_path_candidates(source)[1:]:
        translated_type = source_type_for(translated)
        if translated_type != "unknown":
            return translated_type
    if is_legacy_source(source):
        return "legacy_session"
    return "unknown"


def source_agent_for(value: str | None) -> str | None:
    source = normalize_rel_path(value)
    match = re.match(rf"^{re.escape(SOURCES_DIR)}/([^/]+)/", source)
    if match:
        return match.group(1)
    if source.startswith(f"{VAULT_DAILY_DIR}/") or source.startswith("02-Lessons/OpenClaw-Daily/"):
        return "openclaw"
    if source.startswith(f"{PERMANENT_DIR}/"):
        return "shared"
    for translated in legacy_rel_path_candidates(source)[1:]:
        agent = source_agent_for(translated)
        if agent:
            return agent
    return None


def is_allowed_memory_source(value: str | None) -> bool:
    return source_type_for(value) in {
        "daily_copy",
        "agent_daily",
        "agent_evidence",
        "agent_conversation",
        "personal_knowledge",
        "permanent",
        "openclaw_distilled",
        "agent_ingest",
    }


def is_derived_output_source(value: str | None) -> bool:
    return source_type_for(value) in {
        "agent_summary_derived",
        "shared_derived",
        "index_derived",
        "memory_page_derived",
        "context_derived",
    }


def openclaw_daily_source(value: str | None) -> str | None:
    source = str(value or "").replace("\\", "/")
    match = re.fullmatch(r"memory/(\d{4}-\d{2}-\d{2}\.md)", source)
    if not match:
        return None
    return f"{VAULT_DAILY_DIR}/{match.group(1)}"


def candidate_uid(origin: str, key: str, text: str = "") -> str:
    raw = f"{origin}|{key}|{text[:500]}"
    return hashlib.sha1(raw.encode("utf-8", errors="ignore")).hexdigest()[:16]


def is_blocked_keyword(value: str) -> bool:
    token = normalize_keyword(value)
    if token in STRONG_KEYWORD_ALLOWLIST:
        return False
    if token in BROAD_MATCH_KEYWORDS:
        return True
    return any(pattern.search(token) for pattern in BLOCKED_KEYWORD_PATTERNS)


def scrub_blocked_keyword_text(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        token = match.group(0)
        return " " if is_blocked_keyword(token) else token

    return PATH_LIKE_PATTERN.sub(replace, text)


def is_generic_keyword(value: str) -> bool:
    token = normalize_keyword(value)
    if not token:
        return True
    if token in STRONG_KEYWORD_ALLOWLIST:
        return False
    if is_blocked_keyword(token):
        return True
    if token in STOPWORDS:
        return True
    if re.fullmatch(r"\d+", token):
        return True
    if len(token) == 1:
        return True
    if re.fullmatch(r"[\u4e00-\u9fff]{2}", token) and token not in DOMAIN_PHRASES:
        return True
    if len(token) == 2 and token in GENERIC_WORDS:
        return True
    return False


def is_low_signal_profile_label(value: str) -> bool:
    token = normalize_keyword(value)
    if not token:
        return True
    if token in PROFILE_LABEL_BLOCKLIST:
        return True
    if re.search(r"v\d+(?:\.\d+){0,2}", token):
        return True
    if re.fullmatch(r"\d{4}[./-]\d{1,2}[./-]\d{1,2}|\d{4}\.\d{1,2}\.\d{1,2}", token):
        return True
    if re.fullmatch(r"[0-9a-f]{7,}", token):
        return True
    if token not in STRONG_KEYWORD_ALLOWLIST and re.search(r"api[_-]?key|_api_|_url$|secret|token|password|passwd", token):
        return True
    if is_blocked_keyword(token):
        return True
    if re.search(r"\.(?:md|py|json|jsonl|yaml|yml|toml|env|txt)$", token):
        return True
    if "/" in token or "\\" in token:
        return True
    if token.startswith("step "):
        return True
    if re.fullmatch(r"[\W_]+", token):
        return True
    if re.fullmatch(r"[a-z]{1,2}", token):
        return True
    if re.fullmatch(r"(?:[a-z]+[\\/.-]){1,}[a-z]+", token):
        return True
    words = [word for word in re.split(r"\s+", token) if word]
    if words and all(word in PROFILE_LABEL_BLOCKLIST for word in words):
        return True
    if " " in token and token not in DOMAIN_PHRASES and not any(hint in token for hint in PROJECT_HINT_KEYWORDS):
        return True
    if len(token) > 16 and not any(hint in token for hint in PROJECT_HINT_KEYWORDS):
        return True
    if re.fullmatch(r"[\u4e00-\u9fff]{2,12}", token) and token not in DOMAIN_PHRASES:
        return True
    if len(words) > 3 and not any(hint in token for hint in PROJECT_HINT_KEYWORDS):
        return True
    return False


def canonical_glossary_label(value: str) -> str:
    token = normalize_keyword(value)
    for hint in sorted(PROJECT_HINT_KEYWORDS, key=len, reverse=True):
        if hint in token:
            return hint
    for allowed in sorted(STRONG_KEYWORD_ALLOWLIST, key=len, reverse=True):
        if allowed in token:
            return allowed
    return token


def memory_is_shared(memory: dict[str, Any]) -> bool:
    stage = str(memory.get("stage", "S1"))
    return (
        stage in {"S3", "S4"}
        or bool(memory.get("candidate_origin"))
        or int(memory.get("effective_hit_count", 0)) > 0
    )


def memory_project_label(memory: dict[str, Any]) -> str | None:
    strong = [normalize_keyword(str(item)) for item in memory.get("strong_keywords", [])]
    for token in strong:
        if token in PROJECT_HINT_KEYWORDS or token in STRONG_KEYWORD_ALLOWLIST:
            return token
    title = normalize_keyword(str(memory.get("title", "")))
    for token in PROJECT_HINT_KEYWORDS:
        if token in title:
            return token
    return None


def memory_context_title(memory: dict[str, Any]) -> str:
    title = str(memory.get("title", "Untitled memory")).strip()
    noisy_title = is_low_signal_profile_label(title) or re.search(
        r"^(发现的问题|改进建议|待办跟进|todo|review schedule|问题|建议)",
        title,
        re.IGNORECASE,
    )
    if noisy_title:
        keywords = [str(item) for item in memory.get("strong_keywords", []) if not is_low_signal_profile_label(str(item))]
        if keywords:
            return " / ".join(keywords[:4])
        title_hints = PROJECT_HINT_KEYWORDS - {"openclaw", "codex", "claude", "opencode", "hermes-agent"}
        blob = memory_blob(memory).lower()
        hinted = [hint for hint in sorted(title_hints, key=len, reverse=True) if hint in blob]
        if hinted:
            return " / ".join(hinted[:4])
    return title or "Untitled memory"


def normalized_memory_title(value: str) -> str:
    text = normalize_keyword(value)
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"[：:;；,，].*$", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


apply_rule_config()


def split_segments(content: str) -> list[tuple[str, str, str]]:
    """Return [(title, body, anchor)] from headings and horizontal rules."""
    lines = content.splitlines()
    segments: list[tuple[str, list[str], int]] = []
    current_title = ""
    current: list[str] = []
    start_line = 1

    def flush(end_line: int) -> None:
        nonlocal current, current_title, start_line
        body = "\n".join(current).strip()
        if body:
            title = current_title.strip() or first_title(body)
            segments.append((title, current[:], start_line))
        current = []
        current_title = ""
        start_line = end_line + 1

    for idx, line in enumerate(lines, start=1):
        heading = re.match(r"^\s{0,3}#{1,3}\s+(.+?)\s*$", line)
        divider = re.match(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$", line)
        if heading or divider:
            flush(idx - 1)
            if heading:
                current_title = heading.group(1).strip()
                current.append(line)
                start_line = idx
            else:
                start_line = idx + 1
            continue
        current.append(line)

    flush(len(lines))

    result: list[tuple[str, str, str]] = []
    for title, body_lines, start in segments:
        body = "\n".join(body_lines).strip()
        end = start + len(body_lines) - 1
        result.append((title, body, f"line {start}-{end}"))
    if not result and content.strip():
        result.append((first_title(content), content.strip(), f"line 1-{len(lines)}"))
    return result


def split_conversation_turns(content: str) -> list[tuple[str, str, str]]:
    lines = content.splitlines()
    turns: list[tuple[str, list[str], int]] = []
    current_title = ""
    current: list[str] = []
    start_line = 1
    heading_re = re.compile(r"^###\s+.+\s+(User|Assistant)\s*$")

    def flush(end_line: int) -> None:
        nonlocal current_title, current, start_line
        body = "\n".join(current).strip()
        if current_title and body:
            turns.append((current_title, current[:], start_line))
        current_title = ""
        current = []
        start_line = end_line + 1

    for idx, line in enumerate(lines, start=1):
        if heading_re.match(line.strip()):
            flush(idx - 1)
            current_title = line.strip().lstrip("#").strip()
            current = [line]
            start_line = idx
            continue
        if current_title:
            current.append(line)
    flush(len(lines))

    result: list[tuple[str, str, str]] = []
    for title, body_lines, start in turns:
        body = "\n".join(body_lines).strip()
        end = start + len(body_lines) - 1
        result.append((title, body, f"line {start}-{end}"))
    return result


def conversation_candidate_text(body: str) -> str:
    text = re.sub(r"<details>.*?</details>", "", body, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"_Source line:\s*[^_\n]+_", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def title_from_conversation_turn(agent: str, turn_title: str, body: str) -> str:
    role = "message"
    role_match = re.search(r"\b(User|Assistant)\b", turn_title)
    if role_match:
        role = role_match.group(1).lower()
    for raw in body.splitlines()[1:]:
        line = raw.strip(" #\t-")
        if not line or line.startswith(("_Source line:", "<details>", "<summary>")):
            continue
        line = re.sub(r"^(User|Assistant):\s*", "", line).strip()
        if line:
            return f"{agent} {role}: {line[:90]}"
    return f"{agent} {role}: {turn_title}"


def first_title(content: str) -> str:
    for line in content.splitlines():
        text = line.strip(" #\t")
        if text:
            return text[:60]
    return "Untitled memory"


def noise_reason_for_text(text: str) -> str | None:
    reason = blacklist_reason_for_text(text)
    if reason:
        return reason
    if classify_process_memory(text):
        return None
    compact = re.sub(r"\s+", "", text)
    if len(compact) < MIN_COMPACT_LENGTH:
        return "too_short"
    return None


def pattern_reason(patterns: list[str], text: str, prefix: str) -> str | None:
    lowered = text.lower()
    for pattern in patterns:
        if re.search(pattern, lowered, re.IGNORECASE):
            return f"{prefix}:{pattern}"
    return None


def high_value_reason_for_text(text: str) -> str | None:
    return pattern_reason(HIGH_VALUE_PATTERNS, text, "high_value")


def durable_value_reason_for_text(text: str) -> str | None:
    return pattern_reason(DURABLE_VALUE_PATTERNS, text, "durable_value")


def operational_noise_reason_for_text(text: str) -> str | None:
    for reason, patterns in OPERATIONAL_NOISE_PATTERNS:
        if pattern_reason(patterns, text, reason):
            return reason
    return None


def memory_sync_failure_lesson_reason_for_text(text: str) -> str | None:
    patterns = [
        r"\bmemory-sync\s+(review|sync|index|profile|context|candidate|source|apply).{0,100}\b(failed|failure|error|invalid|bug|regression|root cause)\b",
        r"\bmemory-sync\s+(review|sync|index|profile|context|candidate|source|apply).{0,100}\bfix(?:ed)?\b.{0,100}\b(review apply|sync|index|source_file|source_anchor|candidate|profile|context)\b",
        r"(记忆同步|记忆库同步).{0,100}(失败|报错|错误原因|根因|回归)",
        r"(记忆同步|记忆库同步).{0,100}修复.{0,100}(索引|候选|来源|source|anchor|profile|context)",
    ]
    return pattern_reason(patterns, text, "memory_sync_failure_lesson")


def blacklist_reason_for_text(text: str) -> str | None:
    high_value = high_value_reason_for_text(text)
    durable_value = durable_value_reason_for_text(text)
    operational_reason = operational_noise_reason_for_text(text)
    if operational_reason == "memory_sync_self_log":
        if memory_sync_failure_lesson_reason_for_text(text):
            return None
        return operational_reason
    if operational_reason and not durable_value:
        return operational_reason
    hard_reason = pattern_reason(BLACKLIST_PATTERNS, text, "blacklist")
    if hard_reason and not (high_value or durable_value):
        return hard_reason
    soft_reason = pattern_reason(SOFT_BLACKLIST_PATTERNS, text, "soft_blacklist")
    if soft_reason and not durable_value:
        return soft_reason
    return None


def is_noise_segment(text: str) -> bool:
    return noise_reason_for_text(text) is not None


def memory_blob(memory: dict[str, Any]) -> str:
    return "\n".join(
        [
            str(memory.get("title", "")),
            str(memory.get("summary", "")),
            str(memory.get("excerpt", "")),
            str(memory.get("source_file", "")),
            str(memory.get("original_source_file", "")),
            " ".join(str(item) for item in memory.get("keywords", [])),
            " ".join(str(item) for item in memory.get("strong_keywords", [])),
        ]
    )


def filter_reason(memory: dict[str, Any]) -> str | None:
    source = str(memory.get("source_file", ""))
    if is_legacy_source(source):
        return "legacy_session_source"
    if is_derived_output_source(source):
        return "derived_output_source"
    if not is_allowed_memory_source(source):
        return "unknown_source"
    text = memory_blob(memory)
    reason = noise_reason_for_text(text)
    if reason:
        return reason
    return None


def extract_summary(content: str, limit: int = 220) -> str:
    lines = [line.strip(" #\t-") for line in content.splitlines() if line.strip()]
    selected = " ".join(lines[:4])
    if len(selected) < 80 and len(lines) > 4:
        selected = " ".join(lines[:8])
    return selected[:limit].rstrip() + ("..." if len(selected) > limit else "")


def ingest_index_body(summary: str, source_file: str, source_anchor: str) -> str:
    return (
        f"Summary: {summary}\n\n"
        f"Original context: [[{source_file}]] {source_anchor}\n\n"
        "Policy: keep portable context compact; use source_file/source_anchor for the original record."
    )


def extract_excerpt(content: str, limit: int = 900) -> str:
    text = re.sub(r"\n{3,}", "\n\n", content.strip())
    return text[:limit].rstrip() + ("\n..." if len(text) > limit else "")


def evidence_limit_for_stage(stage: str) -> int:
    return 6000 if stage in {"S2", "S3", "S4"} else 1200


def title_from_ingest(content: str, agent: str) -> str:
    for line in content.splitlines():
        text = line.strip(" #\t-")
        if text:
            return f"{agent} handoff: {text[:70]}"
    return f"{agent} handoff {datetime.now().date().isoformat()}"


def stage_for_agent_ingest(content: str) -> str:
    lowered = content.lower()
    strong_markers = [
        "decision",
        "decided",
        "约定",
        "决定",
        "结论",
        "todo",
        "next action",
        "下一步",
        "blocker",
        "风险",
        "lesson",
        "教训",
        "handoff",
        "交接",
    ]
    if any(marker in lowered for marker in strong_markers):
        return "S2"
    return "S1"


def classify_process_memory(content: str) -> dict[str, Any] | None:
    lowered = content.lower()
    matches: dict[str, list[str]] = {}
    for lesson_type, markers in PROCESS_MEMORY_MARKERS.items():
        found = [marker for marker in markers if marker.lower() in lowered]
        if found:
            matches[lesson_type] = found[:6]
    if sum(len(items) for items in matches.values()) < PROCESS_MEMORY_MIN_MARKER_HITS:
        return None
    priority = ["correction", "failure_lesson", "user_rule", "success_pattern"]
    lesson_type = next((item for item in priority if item in matches), next(iter(matches)))
    return {
        "memory_type": "process_memory",
        "lesson_type": lesson_type,
        "process_markers": matches,
    }


def score_keyword(token: str, frequency: int, source: str) -> float:
    score = float(frequency)
    lowered = token.lower()
    if source in {"phrase", "code"}:
        score += 6
    if any(hint in lowered for hint in TECH_HINTS):
        score += 3
    if re.search(r"[_./\\-]", token):
        score += 2
    if len(token) >= 4:
        score += 1
    return score


def add_keyword(counter: Counter[tuple[str, str]], token: str, source: str) -> None:
    token = normalize_keyword(token)
    if is_generic_keyword(token):
        return
    counter[(token, source)] += 1


def chinese_ngrams(text: str) -> list[str]:
    tokens: list[str] = []
    for chunk in re.findall(r"[\u4e00-\u9fff]{2,24}", text):
        if chunk in STOPWORDS:
            continue
        if 4 <= len(chunk) <= 12 and not is_generic_keyword(chunk):
            tokens.append(chunk)
    return tokens


def extract_keyword_profile(content: str, title: str = "", limit: int = 16) -> dict[str, list[str]]:
    text = f"{title}\n{content}"
    keyword_text = scrub_blocked_keyword_text(text)
    counter: Counter[tuple[str, str]] = Counter()

    lowered = text.lower()
    for phrase in DOMAIN_PHRASES:
        if phrase.lower() in lowered:
            add_keyword(counter, phrase, "phrase")

    for phrase in STRONG_KEYWORD_ALLOWLIST:
        if phrase and phrase.lower() in lowered:
            add_keyword(counter, phrase, "phrase")

    for token in re.findall(r"\*\*([^*\n]{2,60})\*\*", text):
        add_keyword(counter, token, "phrase")

    for token in re.findall(r"`([^`]{2,80})`", text):
        if is_blocked_keyword(token):
            continue
        add_keyword(counter, token, "code")

    for token in re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", keyword_text):
        add_keyword(counter, token, "word")

    for token in chinese_ngrams(keyword_text):
        add_keyword(counter, token, "zh")

    scored: dict[str, float] = {}
    strong: set[str] = set()
    for (token, source), frequency in counter.items():
        score = score_keyword(token, frequency, source)
        scored[token] = max(scored.get(token, 0.0), score)
        normalized = normalize_keyword(token)
        if normalized in STRONG_KEYWORD_ALLOWLIST or (
            (source in {"phrase", "code"} or score >= 5) and normalized not in BROAD_MATCH_KEYWORDS
        ):
            strong.add(token)

    ordered = [token for token, _score in sorted(scored.items(), key=lambda item: item[1], reverse=True)]
    keywords = ordered[:limit]
    strong_keywords = [token for token in keywords if token in strong][: max(6, limit // 2)]
    if not strong_keywords:
        strong_keywords = keywords[:3]
    return {"keywords": keywords, "strong_keywords": strong_keywords}


def extract_keywords(content: str, limit: int = 10) -> list[str]:
    return extract_keyword_profile(content, limit=limit)["keywords"]


def cjk_query_terms(text: str) -> list[str]:
    terms: set[str] = set()
    for chunk in re.findall(r"[\u4e00-\u9fff]{2,24}", text):
        if is_generic_keyword(chunk):
            continue
        terms.add(chunk)
        max_size = min(6, len(chunk))
        for size in range(2, max_size + 1):
            for index in range(0, len(chunk) - size + 1):
                token = chunk[index : index + size]
                if not is_generic_keyword(token):
                    terms.add(token)
    return sorted(terms, key=lambda item: (-len(item), item))


def search_terms_for_query(query: str) -> list[str]:
    terms: set[str] = set()
    lowered = query.lower()
    for token in re.split(r"[\s,，。.!！?？;；:：/\\|()\[\]{}<>]+", lowered):
        token = normalize_keyword(token)
        if token and not is_generic_keyword(token):
            terms.add(token)
    profile = extract_keyword_profile(query, limit=24)
    for token in profile["strong_keywords"] + profile["keywords"]:
        token = normalize_keyword(token)
        if token and not is_generic_keyword(token):
            terms.add(token)
    terms.update(cjk_query_terms(query))
    return sorted(terms, key=lambda item: (-len(item), item))


def compact_text(value: str, limit: int = 180) -> str:
    text = re.sub(r"\s+", " ", value).strip()
    return text[:limit].rstrip() + ("..." if len(text) > limit else "")


def truncate_text(value: str, limit: int = 4000) -> str:
    text = str(value or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n\n...[truncated]"


def important_grounding_tokens(text: str) -> set[str]:
    tokens: set[str] = set()
    for pattern in (
        r"https?://[^\s`)\]]+",
        r"\b[A-Za-z]:[\\/][^\s`)\]]+",
        r"\b[\w.-]+\.(?:py|md|json|jsonl|toml|yaml|yml|sqlite|db|tsx?|jsx?|vue|onnx)\b",
        r"\b[A-Za-z][A-Za-z0-9_-]*\d[A-Za-z0-9_-]*\b",
        r"\b[A-Za-z][A-Za-z0-9_-]*[-_][A-Za-z0-9_-]+\b",
    ):
        for match in re.findall(pattern, text, re.IGNORECASE):
            tokens.add(normalize_keyword(str(match)))
    return {token for token in tokens if token and not is_generic_keyword(token)}


def critical_claim_markers(text: str) -> set[str]:
    markers = {
        "未安装",
        "缺失",
        "投递失败",
        "失败",
        "已修复",
        "修复",
        "验证通过",
        "不兼容",
        "兼容",
        "超时",
        "403",
        "fetch failed",
        "enabled",
        "disabled",
    }
    lowered = text.lower()
    return {marker for marker in markers if marker.lower() in lowered}


def critical_marker_supported(marker: str, evidence: str) -> bool:
    aliases = {
        "未安装": ["未安装", "没有安装", "未装"],
        "缺失": ["缺失", "缺少", "没有"],
        "投递失败": ["投递失败", "推送失败", "发送失败"],
        "已修复": ["已修复", "修复完成", "已解决"],
        "验证通过": ["验证通过", "测试通过", "passed"],
        "不兼容": ["不兼容", "不能兼容"],
        "fetch failed": ["fetch failed", "fetch失败"],
    }
    lowered = evidence.lower()
    return any(alias.lower() in lowered for alias in aliases.get(marker, [marker]))


def evidence_has_conflicting_polarity(evidence: str, claim: str) -> bool:
    evidence_lower = evidence.lower()
    claim_lower = claim.lower()
    negative = {"失败", "缺失", "未安装", "不可用", "不兼容", "disabled", "error"}
    positive = {"成功", "运行正常", "验证通过", "可用", "兼容", "enabled", "passed"}
    if any(item in claim_lower for item in negative) and not any(item in evidence_lower for item in negative):
        return any(item in evidence_lower for item in positive)
    if any(item in claim_lower for item in positive) and not any(item in evidence_lower for item in positive):
        return any(item in evidence_lower for item in negative)
    return False


def markdown_heading_text(value: str, fallback: str = "Untitled") -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text[:80] if text else fallback


def bounded_list(value: Any, limit: int = 16) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        text = str(item).strip()
        if text and text not in result:
            result.append(text)
        if len(result) >= limit:
            break
    return result


def clamp_float(value: Any, default: float = 0.75, minimum: float = 0.0, maximum: float = 1.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = default
    return min(max(number, minimum), maximum)


def signal(category: str, label: str, weight: float, source: str, evidence: str, detail: str = "") -> dict[str, Any]:
    return {
        "category": category,
        "label": label,
        "weight": round(float(weight), 3),
        "confidence": round(min(0.99, max(0.1, float(weight))), 3),
        "source": source,
        "evidence": compact_text(evidence),
        "detail": detail,
    }


def keyword_diagnostics(text: str) -> tuple[list[str], list[str]]:
    candidates: set[str] = set()
    keyword_text = scrub_blocked_keyword_text(text)
    candidates.update(re.findall(r"`([^`]{2,80})`", text))
    candidates.update(match.group(0) for match in PATH_LIKE_PATTERN.finditer(text))
    candidates.update(re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", keyword_text))
    candidates.update(chinese_ngrams(keyword_text))

    blocked: list[str] = []
    generic: list[str] = []
    for token in sorted(candidates, key=str.lower):
        normalized = normalize_keyword(token)
        if not normalized:
            continue
        if is_blocked_keyword(normalized):
            blocked.append(token)
        elif is_generic_keyword(normalized):
            generic.append(token)
    return blocked[:20], generic[:20]


class MemoryStore:
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.index_path = vault_path / STATE_INDEX_DIR / INDEX_NAME
        self.legacy_index_paths = [
            vault_path / STATE_INDEX_DIR / LEGACY_INDEX_NAME,
            vault_path / "_index" / LEGACY_INDEX_NAME,
            vault_path / "_index" / INDEX_NAME,
        ]
        self.loaded_from_legacy_index = False
        self.data = self.load()

    def load(self) -> dict[str, Any]:
        load_path = self.index_path
        if not load_path.exists():
            for candidate in self.legacy_index_paths:
                if candidate.exists():
                    load_path = candidate
                    self.loaded_from_legacy_index = True
                    break
        if not load_path.exists():
            return {
                INDEX_META: {
                    "schema": "openclaw-memory-index",
                    "created_at": now_iso(),
                    "updated_at": now_iso(),
                    "processed_files": {},
                }
            }
        try:
            data = json.loads(load_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Index file is invalid JSON: {load_path} ({exc})") from exc
        if INDEX_META not in data:
            data[INDEX_META] = {"schema": "openclaw-memory-index", "processed_files": {}}
        data[INDEX_META].setdefault("processed_files", {})
        processed_dates = data.pop("processed_dates", None)
        if isinstance(processed_dates, list):
            data[INDEX_META].setdefault("processed_dates", processed_dates)
        nested = data.pop("memories", None)
        if isinstance(nested, dict):
            for key, value in nested.items():
                if isinstance(value, dict) and self.is_memory_record(value):
                    data.setdefault(key, value)
        data.pop("daily_refs", None)
        data.pop("version", None)
        if "updated_at" in data:
            data[INDEX_META].setdefault("updated_at", data.pop("updated_at"))
        for value in data.values():
            if isinstance(value, dict) and self.is_memory_record(value):
                self.ensure_keyword_profile(value)
        return self.normalize_record_ids(data)

    @staticmethod
    def normalize_record_ids(data: dict[str, Any]) -> dict[str, Any]:
        records: list[tuple[str, dict[str, Any]]] = []
        passthrough: dict[str, Any] = {INDEX_META: data.get(INDEX_META, {})}
        for key, value in data.items():
            if key == INDEX_META:
                continue
            if isinstance(value, dict) and MemoryStore.is_memory_record(value):
                records.append((key, value))
            elif key not in RESERVED_INDEX_KEYS:
                passthrough[key] = value

        def record_sort_key(item: tuple[str, dict[str, Any]]) -> tuple[int, int | str]:
            key = item[0]
            match = re.match(r"memory_(\d+)$", key)
            if match:
                return (0, int(match.group(1)))
            return (1, key)

        normalized = {INDEX_META: passthrough.get(INDEX_META, {})}
        for index, (old_key, memory) in enumerate(sorted(records, key=record_sort_key), start=1):
            new_key = f"memory_{index:03d}"
            if old_key != new_key:
                memory.setdefault("legacy_id", old_key)
            normalized[new_key] = memory
        for key, value in passthrough.items():
            if key != INDEX_META:
                normalized[key] = value
        return normalized

    @staticmethod
    def is_memory_record(value: dict[str, Any]) -> bool:
        return any(field in value for field in ("title", "summary", "keywords", "source_file"))

    @staticmethod
    def ensure_keyword_profile(memory: dict[str, Any]) -> None:
        memory.setdefault("source_type", source_type_for(memory.get("source_file")))
        memory.setdefault("source_agent", source_agent_for(memory.get("source_file")) or "openclaw")
        memory.setdefault("quality_score", 1.0)
        memory.setdefault("filtered_reason", None)
        if memory.get("strong_keywords"):
            memory["keywords"] = [kw for kw in memory.get("keywords", []) if not is_generic_keyword(str(kw))][:18]
            memory["strong_keywords"] = [
                kw for kw in memory.get("strong_keywords", []) if not is_generic_keyword(str(kw))
            ][:10]
            return
        MemoryStore.refresh_keyword_profile(memory)

    @staticmethod
    def refresh_keyword_profile(memory: dict[str, Any]) -> None:
        text = "\n".join(
            [
                str(memory.get("summary", "")),
                str(memory.get("excerpt", "")),
            ]
        )
        profile = extract_keyword_profile(text, title=str(memory.get("title", "")))
        memory["keywords"] = profile["keywords"]
        memory["strong_keywords"] = profile["strong_keywords"]
        memory["source_type"] = source_type_for(memory.get("source_file"))
        memory["source_agent"] = memory.get("source_agent") or source_agent_for(memory.get("source_file")) or "openclaw"
        memory.setdefault("quality_score", 1.0)
        memory.setdefault("filtered_reason", None)

    def memories(self) -> dict[str, dict[str, Any]]:
        return {
            k: v
            for k, v in self.data.items()
            if k not in RESERVED_INDEX_KEYS and isinstance(v, dict) and self.is_memory_record(v)
        }

    def save(self) -> None:
        self.data[INDEX_META]["updated_at"] = now_iso()
        self.data.pop("memories", None)
        self.data.pop("daily_refs", None)
        self.data.pop("processed_dates", None)
        self.data.pop("version", None)
        if "updated_at" in self.data:
            self.data[INDEX_META].setdefault("legacy_updated_at", self.data.pop("updated_at"))
        self.data = self.normalize_record_ids(self.data)
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.index_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, self.index_path)
        for old_path in self.legacy_index_paths:
            if old_path.exists() and old_path != self.index_path:
                old_path.unlink()
        self.loaded_from_legacy_index = False

    def next_id(self) -> str:
        max_id = 0
        for key in self.memories():
            match = re.match(r"memory_(\d+)$", key)
            if match:
                max_id = max(max_id, int(match.group(1)))
        return f"memory_{max_id + 1:03d}"

    def capacity_factor(self) -> float:
        long_count = sum(1 for memory in self.memories().values() if memory.get("stage") in {"S2", "S3", "S4"})
        size_kb = self.index_path.stat().st_size / 1024 if self.index_path.exists() else 0
        if long_count > 50 or size_kb > 150:
            return 0.0
        if long_count < 20 or size_kb < 50:
            return 1.0
        return 0.5

    def ttl_days(self, stage: str) -> int | None:
        if stage == "S4":
            return None
        factor = self.capacity_factor()
        ranges = {
            "S1": (CONFIG["S1_TTL_MIN_DAYS"], CONFIG["S1_TTL_MAX_DAYS"]),
            "S2": (7, 15),
            "S3": (14, 30),
        }
        low, high = ranges.get(stage, ranges["S1"])
        return int(round(low + (high - low) * factor))

    def expire_at(self, stage: str, quality: float = 1.0) -> str | None:
        ttl = self.ttl_days(stage)
        if ttl is None:
            return None
        return (datetime.now() + timedelta(days=max(1, ttl * quality))).replace(microsecond=0).isoformat()

    def referenced_files(self) -> set[str]:
        refs: set[str] = set()
        for memory in self.memories().values():
            if memory.get("source_file"):
                refs.update(legacy_rel_path_candidates(str(memory["source_file"])))
            for source in memory.get("sources", []):
                if source.get("file"):
                    refs.update(legacy_rel_path_candidates(str(source["file"])))
        return refs


class MemorySync:
    def __init__(self):
        self.openclaw_path = expand_path(CONFIG["OPENCLAW_WORKSPACE"])
        self.vault_path = expand_path(CONFIG["VAULT_PATH"])
        self.store = MemoryStore(self.vault_path)

    def log(self, message: str) -> None:
        print(message)

    def source_rel(self, path: Path) -> str:
        try:
            return path.relative_to(self.openclaw_path).as_posix()
        except ValueError:
            return path.as_posix()

    def vault_rel(self, path: Path) -> str:
        try:
            return path.relative_to(self.vault_path).as_posix()
        except ValueError:
            return path.as_posix()

    def resolve_vault_rel(self, rel: str) -> Path:
        candidates = legacy_rel_path_candidates(rel)
        for candidate in candidates:
            path = self.vault_path / candidate
            if path.exists():
                return path
        return self.vault_path / (candidates[0] if candidates else normalize_rel_path(rel))

    def vault_daily_path(self, original_path: Path) -> Path:
        return self.vault_path / VAULT_DAILY_DIR / original_path.name

    def sync_daily_copy(self, original_path: Path, text: str) -> Path:
        copy_path = self.vault_daily_path(original_path)
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = copy_path.with_suffix(copy_path.suffix + ".tmp")
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, copy_path)
        self.log(f"COPY daily file to vault: {self.vault_rel(copy_path)}")
        return copy_path

    def review_mode(self) -> str:
        mode = str(CONFIG["REVIEW_MODE"]).strip().lower()
        if mode not in {"agent", "rules"}:
            self.log(f"WARN unknown MEMORY_SYNC_REVIEW_MODE={mode!r}; using agent")
            return "agent"
        return mode

    def review_pack_path(self) -> Path:
        return self.vault_path / REVIEW_DIR / REVIEW_PACK_NAME

    def clear_review_pack(self) -> None:
        path = self.review_pack_path()
        if path.exists():
            path.unlink()
        parent = path.parent
        try:
            if parent.exists() and not any(parent.iterdir()):
                parent.rmdir()
        except OSError:
            pass

    def review_candidate_id(self, source_file: str, anchor: str, text: str) -> str:
        digest = hashlib.sha1(f"{source_file}|{anchor}|{text}".encode("utf-8", errors="ignore")).hexdigest()[:16]
        safe_source = re.sub(r"[^A-Za-z0-9_.-]+", "-", source_file).strip("-")
        return f"{safe_source}:{digest}"

    def review_decision_schema(self) -> dict[str, Any]:
        return {
            "decisions": [
                {
                    "candidate_id": "string from this pack",
                    "keep": True,
                    "title": "short stable title",
                    "summary": "evidence-backed summary",
                    "keywords": ["specific", "searchable", "terms"],
                    "strong_keywords": ["terms required for precise matching"],
                    "stage": "S1|S2|S3|S4",
                    "quality_score": 0.0,
                    "memory_type": "optional, e.g. process_memory",
                    "lesson_type": "optional: success_pattern|correction|failure_lesson|user_rule",
                    "merge_with": "optional existing memory id or candidate_id from this pack",
                    "replace_summary": False,
                    "reason": "why this should be kept, discarded, or merged",
                }
            ]
        }

    def review_candidate_from_memory(
        self,
        memory: dict[str, Any],
        body: str,
        source_kind: str,
        source_agent: str = "openclaw",
    ) -> dict[str, Any]:
        source_file = str(memory.get("source_file", ""))
        anchor = str(memory.get("source_anchor", ""))
        candidate_id = self.review_candidate_id(source_file, anchor, body)
        return {
            "candidate_id": candidate_id,
            "source_kind": source_kind,
            "source_agent": source_agent,
            "source_file": source_file,
            "source_anchor": anchor,
            "original_source_file": memory.get("original_source_file"),
            "title_hint": memory.get("title", ""),
            "text": body,
            "text_hash": hashlib.sha256(body.encode("utf-8", errors="ignore")).hexdigest(),
            "rule_suggestion": {
                "summary": memory.get("summary", ""),
                "keywords": memory.get("keywords", []),
                "strong_keywords": memory.get("strong_keywords", []),
                "stage": memory.get("stage", "S1"),
                "quality_score": memory.get("quality_score", 0.75),
                "memory_type": memory.get("memory_type"),
                "lesson_type": memory.get("lesson_type"),
                "candidate_origin": memory.get("candidate_origin"),
            },
            "base_memory": memory,
        }

    def dedupe_review_candidates(self, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
        deduped: list[dict[str, Any]] = []
        seen_keys: set[str] = set()
        seen_ids: set[str] = set()
        for item in candidates:
            base = item.get("base_memory") if isinstance(item.get("base_memory"), dict) else {}
            key = str(base.get("candidate_uid") or item.get("candidate_id") or "").strip()
            candidate_id = str(item.get("candidate_id") or "").strip()
            if not key:
                key = hashlib.sha1(
                    f"{item.get('source_file')}|{item.get('source_anchor')}|{item.get('text_hash')}".encode(
                        "utf-8", errors="ignore"
                    )
                ).hexdigest()
            if key in seen_keys or (candidate_id and candidate_id in seen_ids):
                continue
            seen_keys.add(key)
            if candidate_id:
                seen_ids.add(candidate_id)
            deduped.append(item)
        return deduped

    def dedupe_memory_candidates(self, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
        deduped: list[dict[str, Any]] = []
        seen: set[str] = set()
        for memory in candidates:
            key = str(memory.get("candidate_uid") or "").strip()
            if not key:
                key = candidate_uid(
                    str(memory.get("candidate_origin") or "memory-candidate"),
                    f"{memory.get('source_file', '')}:{memory.get('source_anchor', '')}",
                    str(memory.get("summary") or memory.get("excerpt") or memory.get("title") or ""),
                )
                memory["candidate_uid"] = key
            if key in seen:
                continue
            seen.add(key)
            deduped.append(memory)
        return deduped

    def compact_existing_memories(self) -> list[dict[str, Any]]:
        rows = []
        for memory_id, memory in self.store.memories().items():
            rows.append(
                {
                    "id": memory_id,
                    "title": memory.get("title", ""),
                    "summary": memory.get("summary", ""),
                    "stage": memory.get("stage", "S1"),
                    "keywords": memory.get("keywords", [])[:10],
                    "strong_keywords": memory.get("strong_keywords", [])[:8],
                    "source_file": memory.get("source_file", ""),
                }
            )
        return rows

    def collect_conversation_archive_candidates(
        self,
        existing_uids: set[str],
        processed: dict[str, str],
    ) -> tuple[list[dict[str, Any]], dict[str, str], list[dict[str, str]], Counter[str]]:
        candidates: list[dict[str, Any]] = []
        processed_files: dict[str, str] = {}
        skipped: list[dict[str, str]] = []
        coverage: Counter[str] = Counter()
        base = self.vault_path / AGENTS_DIR
        if not base.exists():
            return candidates, processed_files, skipped, coverage

        for path in sorted(base.glob("*/conversations/*/*.md")):
            rel = self.vault_rel(path)
            parts = rel.split("/")
            if len(parts) < 5:
                continue
            agent = parts[1]
            digest = file_hash(path)
            coverage["conversation_files_scanned"] += 1
            if processed.get(rel) == digest:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            processed_files[rel] = digest
            for title, body, anchor in split_conversation_turns(text):
                coverage["conversation_segments_seen"] += 1
                candidate_text = conversation_candidate_text(body)
                reason = noise_reason_for_text(candidate_text)
                high_value_reason = high_value_reason_for_text(candidate_text)
                compact = re.sub(r"\s+", "", candidate_text)
                if (reason and not high_value_reason) or len(compact) < 80:
                    skipped.append(
                        {
                            "source_file": rel,
                            "source_anchor": anchor,
                            "title_hint": title[:80],
                            "reason": reason or "too_short_for_agent_review",
                            "high_value_reason": high_value_reason or "",
                        }
                    )
                    continue
                memory = self.build_memory(title, candidate_text, rel, anchor, rel)
                memory["title"] = title_from_conversation_turn(agent, title, candidate_text)
                memory["source_agent"] = agent
                memory["candidate_origin"] = f"{agent}-conversation-archive"
                memory["candidate_uid"] = candidate_uid(memory["candidate_origin"], f"{rel}:{anchor}", candidate_text)
                memory["memory_lane"] = "conversation"
                memory["context_storage_policy"] = "archive_then_review"
                memory["original_context_file"] = rel
                memory["original_context_anchor"] = anchor
                if memory["candidate_uid"] in existing_uids:
                    skipped.append(
                        {
                            "source_file": rel,
                            "source_anchor": anchor,
                            "title_hint": title[:80],
                            "reason": "already_indexed_candidate_uid",
                            "high_value_reason": high_value_reason or "",
                        }
                    )
                    continue
                coverage["conversation_candidates"] += 1
                candidates.append(self.review_candidate_from_memory(memory, candidate_text, "agent_conversation", agent))
        return candidates, processed_files, skipped, coverage

    def build_review_pack(self) -> dict[str, Any]:
        memory_dir = self.openclaw_path / DAILY_DIR
        if not memory_dir.exists():
            raise ValueError(f"memory directory not found: {memory_dir}")

        processed = self.store.data[INDEX_META].setdefault("processed_files", {})
        referenced = self.store.referenced_files()
        candidates: list[dict[str, Any]] = []
        processed_files: dict[str, str] = {}
        copied_daily_files: list[str] = []
        skipped: list[dict[str, str]] = []
        coverage: Counter[str] = Counter()
        existing_uids: set[str] = set()
        for memory in self.store.memories().values():
            if memory.get("candidate_uid"):
                existing_uids.add(str(memory.get("candidate_uid")))
            for uid in memory.get("merged_candidate_uids", []) or []:
                if uid:
                    existing_uids.add(str(uid))

        for path in sorted(memory_dir.glob("*.md")):
            coverage["daily_files_scanned"] += 1
            original_rel = self.source_rel(path)
            copy_path = self.vault_daily_path(path)
            copy_rel = self.vault_rel(copy_path)
            digest = file_hash(path)
            if processed.get(original_rel) == digest and (copy_path.exists() or copy_rel not in referenced):
                continue

            text = path.read_text(encoding="utf-8", errors="replace")
            self.sync_daily_copy(path, text)
            processed_files[original_rel] = digest
            copied_daily_files.append(copy_rel)

            for title, body, anchor in split_segments(text):
                coverage["segments_seen"] += 1
                compact = re.sub(r"\s+", "", body)
                reason = blacklist_reason_for_text(body)
                if reason or len(compact) < 40:
                    high_value_reason = high_value_reason_for_text(body)
                    if high_value_reason:
                        coverage["high_value_skipped"] += 1
                    skipped.append(
                        {
                            "source_file": copy_rel,
                            "source_anchor": anchor,
                            "title_hint": title[:80],
                            "reason": reason or "too_short_for_agent_review",
                            "high_value_reason": high_value_reason or "",
                        }
                    )
                    continue
                memory = self.build_memory(title, body, copy_rel, anchor, original_rel)
                memory["candidate_origin"] = "agent-review-daily"
                memory["candidate_uid"] = candidate_uid("agent-review-daily", f"{copy_rel}:{anchor}", body)
                if memory["candidate_uid"] in existing_uids:
                    skipped.append(
                        {
                            "source_file": copy_rel,
                            "source_anchor": anchor,
                            "title_hint": title[:80],
                            "reason": "already_indexed_candidate_uid",
                            "high_value_reason": high_value_reason_for_text(body) or "",
                        }
                    )
                    continue
                coverage["daily_candidates"] += 1
                candidates.append(self.review_candidate_from_memory(memory, body, "openclaw_daily", "openclaw"))

        distilled_count = 0
        session_curated_count = 0
        if CONFIG["OPENCLAW_IMPORT_DISTILLED"]:
            distilled: list[dict[str, Any]] = []
            distilled.extend(self.collect_promoted_candidates())
            distilled.extend(self.collect_dream_candidates("deep", "openclaw-deep"))
            distilled.extend(self.collect_dream_candidates("rem", "openclaw-rem"))
            session_curated = self.collect_session_corpus_candidates()
            session_curated_count = len(session_curated)
            distilled.extend(session_curated)
            distilled.extend(self.collect_recall_candidates())
            distilled = self.dedupe_memory_candidates(distilled)
            for memory in distilled:
                body = str(memory.get("excerpt") or memory.get("summary") or memory.get("title") or "")
                if not body:
                    continue
                if memory.get("candidate_uid") in existing_uids:
                    skipped.append(
                        {
                            "source_file": str(memory.get("source_file", "")),
                            "source_anchor": str(memory.get("source_anchor", "")),
                            "title_hint": str(memory.get("title", ""))[:80],
                            "reason": "already_indexed_candidate_uid",
                            "high_value_reason": high_value_reason_for_text(body) or "",
                        }
                    )
                    continue
                reason = blacklist_reason_for_text(memory_blob(memory) or body)
                if reason:
                    skipped.append(
                        {
                            "source_file": str(memory.get("source_file", "")),
                            "source_anchor": str(memory.get("source_anchor", "")),
                            "title_hint": str(memory.get("title", ""))[:80],
                            "reason": reason,
                            "high_value_reason": high_value_reason_for_text(body) or "",
                        }
                    )
                    continue
                coverage["distilled_candidates"] += 1
                candidates.append(self.review_candidate_from_memory(memory, body, "openclaw_distilled", "openclaw"))
            distilled_count = len(distilled)
        conversation_candidates, conversation_processed, conversation_skipped, conversation_coverage = (
            self.collect_conversation_archive_candidates(existing_uids, processed)
        )
        candidates.extend(conversation_candidates)
        processed_files.update(conversation_processed)
        skipped.extend(conversation_skipped)
        coverage.update(conversation_coverage)
        raw_candidate_count = len(candidates)
        candidates = self.dedupe_review_candidates(candidates)
        coverage["duplicate_candidates_removed"] = raw_candidate_count - len(candidates)
        coverage["candidate_count"] = len(candidates)
        coverage["skipped_count"] = len(skipped)

        return {
            "_meta": {
                "schema": "memory-sync-agent-review-pack",
                "generated_at": now_iso(),
                "review_mode": "agent",
                "candidate_count": len(candidates),
                "copied_daily_count": len(copied_daily_files),
                "distilled_candidate_count": distilled_count,
                "session_curated_candidate_count": session_curated_count,
                "conversation_candidate_count": len(conversation_candidates),
                "coverage": dict(coverage),
                "instructions": [
                    "The current agent must review candidates and produce decisions JSON.",
                    "Keep only evidence-backed memories; do not invent facts outside candidate text.",
                    "Use S2 for success patterns, corrections, failure lessons, and explicit user rules.",
                    "Use merge_with when a candidate duplicates an existing memory.",
                    "The script validates and writes decisions; it must keep OpenClaw source read-only.",
                ],
                "decision_schema": self.review_decision_schema(),
            },
            "processed_files": processed_files,
            "copied_daily_files": copied_daily_files,
            "skipped": skipped[:200],
            "existing_memories": self.compact_existing_memories(),
            "candidates": candidates,
        }

    def cmd_review_prepare(self) -> int:
        try:
            pack = self.build_review_pack()
        except ValueError as exc:
            self.log(f"ERROR {exc}")
            return 1
        path = self.review_pack_path()
        self.write_json_atomic(path, pack)
        self.log(f"Agent review pack written: {self.vault_rel(path)}")
        self.log(f"Agent review pack absolute path: {path}")
        self.log(f"Candidates: {pack['_meta']['candidate_count']}")
        coverage = pack.get("_meta", {}).get("coverage", {})
        if isinstance(coverage, dict):
            self.log(
                "Coverage: "
                f"daily_files={coverage.get('daily_files_scanned', 0)}, "
                f"segments={coverage.get('segments_seen', 0)}, "
                f"skipped={coverage.get('skipped_count', 0)}, "
                f"high_value_skipped={coverage.get('high_value_skipped', 0)}, "
                f"session_curated={pack['_meta'].get('session_curated_candidate_count', 0)}"
            )
        self.log("Next: current agent writes decisions JSON, then run:")
        self.log("  python scripts/main.py review apply <decisions.json>")
        return 0

    def prepare_agent_review(self, caller: str = "review") -> int:
        if caller != "review":
            self.log("Agent review mode is active; preparing review pack instead of rule-based indexing.")
        result = self.cmd_review_prepare()
        if result == 0 and caller != "review":
            self.log("No rule-based memories were written. Let the current agent review the pack and apply decisions.")
        return result

    def load_review_pack(self, pack_path: Path | None = None) -> dict[str, Any]:
        path = pack_path or self.review_pack_path()
        if not path.exists():
            raise ValueError(f"review pack not found: {path}")
        try:
            pack = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"review pack is invalid JSON: {path} ({exc})") from exc
        if pack.get("_meta", {}).get("schema") != "memory-sync-agent-review-pack":
            raise ValueError(f"not a memory-sync review pack: {path}")
        return pack

    def load_review_decisions(self, decisions_path: Path) -> list[dict[str, Any]]:
        if not decisions_path.exists():
            raise ValueError(f"decisions file not found: {decisions_path}")
        try:
            payload = json.loads(decisions_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"decisions file is invalid JSON: {decisions_path} ({exc})") from exc
        decisions = payload.get("decisions") if isinstance(payload, dict) else payload
        if not isinstance(decisions, list):
            raise ValueError("decisions JSON must be a list or an object with a decisions list")
        return [item for item in decisions if isinstance(item, dict)]

    def validate_review_decision(self, pack_item: dict[str, Any], decision: dict[str, Any]) -> list[str]:
        if decision.get("keep") is False:
            return []
        base = pack_item.get("base_memory") if isinstance(pack_item.get("base_memory"), dict) else {}
        evidence = "\n".join(
            [
                str(pack_item.get("text", "")),
                str(base.get("excerpt", "")),
                str(base.get("evidence_text", "")),
                str(base.get("summary", "")),
                str(base.get("source_file", "")),
                str(base.get("original_source_file", "")),
            ]
        )
        claim = "\n".join(
            [
                str(decision.get("title", "")),
                str(decision.get("summary", "")),
                " ".join(str(item) for item in bounded_list(decision.get("keywords"), 18)),
                " ".join(str(item) for item in bounded_list(decision.get("strong_keywords"), 10)),
            ]
        )
        evidence_norm = normalize_keyword(evidence)
        issues: list[str] = []
        for token in sorted(important_grounding_tokens(claim)):
            if token and token not in evidence_norm:
                issues.append(f"unsupported token: {token}")
        for marker in sorted(critical_claim_markers(claim)):
            if not critical_marker_supported(marker, evidence):
                issues.append(f"unsupported critical claim marker: {marker}")
        lesson_type = str(decision.get("lesson_type", "")).strip()
        if lesson_type == "failure_lesson" and not ({"失败", "失败原因", "教训", "failed", "failure"} & critical_claim_markers(evidence)):
            lowered = evidence.lower()
            if not any(
                item in lowered
                for item in (
                    "失败",
                    "故障",
                    "错误",
                    "异常",
                    "超时",
                    "投递失败",
                    "403",
                    "failed",
                    "failure",
                    "error",
                    "timeout",
                    "fetch failed",
                    "econnaborted",
                    "contexttoken",
                )
            ):
                issues.append("failure_lesson without failure evidence")
        if evidence_has_conflicting_polarity(evidence, claim):
            issues.append("claim polarity conflicts with evidence")
        return issues

    def apply_review_decision(self, base: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
        candidate = json.loads(json.dumps(base, ensure_ascii=False))
        if str(decision.get("stage", candidate.get("stage", "S1"))) in STAGES:
            candidate["stage"] = str(decision.get("stage", candidate.get("stage", "S1")))
            candidate["expire_at"] = self.store.expire_at(candidate["stage"])
        for field, limit in (("title", 120), ("summary", 500)):
            text = str(decision.get(field, candidate.get(field, ""))).strip()
            if text:
                candidate[field] = text[:limit]
        keywords = bounded_list(decision.get("keywords"), 18)
        strong_keywords = bounded_list(decision.get("strong_keywords"), 10)
        if keywords:
            candidate["keywords"] = keywords
        if strong_keywords:
            candidate["strong_keywords"] = strong_keywords
        candidate["quality_score"] = clamp_float(decision.get("quality_score"), float(candidate.get("quality_score", 0.75) or 0.75))
        for field in ("memory_type", "lesson_type"):
            value = str(decision.get(field, "")).strip()
            if value:
                candidate[field] = value
        if candidate.get("memory_type") == "process_memory":
            candidate["memory_lane"] = "process"
            if STAGES.index(candidate.get("stage", "S1")) < STAGES.index("S2"):
                candidate["stage"] = "S2"
                candidate["expire_at"] = self.store.expire_at("S2")
        if candidate.get("stage") in {"S2", "S3", "S4"} and not candidate.get("evidence_text"):
            candidate["evidence_text"] = extract_excerpt(
                str(candidate.get("excerpt") or candidate.get("summary") or ""),
                limit=evidence_limit_for_stage(str(candidate.get("stage"))),
            )
        candidate["review_mode"] = "agent"
        candidate["reviewed_at"] = now_iso()
        candidate["review_reason"] = str(decision.get("reason", "")).strip()
        candidate["source_confidence"] = "agent_reviewed"
        candidate["candidate_uid"] = candidate.get("candidate_uid") or candidate_uid(
            "agent-review",
            f"{candidate.get('source_file')}:{candidate.get('source_anchor')}",
            candidate.get("summary", ""),
        )
        return candidate

    def cmd_review_apply(self, decisions_path: Path, pack_path: Path | None = None) -> int:
        try:
            pack = self.load_review_pack(pack_path)
            decisions = self.load_review_decisions(decisions_path)
        except ValueError as exc:
            self.log(f"ERROR {exc}")
            return 1

        by_id = {str(item.get("candidate_id")): item for item in pack.get("candidates", []) if item.get("candidate_id")}
        decision_ids = {str(item.get("candidate_id", "")).strip() for item in decisions}
        missing = sorted(set(by_id) - decision_ids)
        if missing:
            self.log("ERROR decisions do not cover every review candidate.")
            self.log("Missing candidate_ids:")
            for candidate_id in missing[:20]:
                self.log(f"- {candidate_id}")
            if len(missing) > 20:
                self.log(f"- ... {len(missing) - 20} more")
            return 1
        validation_errors: list[str] = []
        for decision in decisions:
            candidate_id = str(decision.get("candidate_id", "")).strip()
            pack_item = by_id.get(candidate_id)
            if not pack_item:
                continue
            for issue in self.validate_review_decision(pack_item, decision):
                validation_errors.append(f"{candidate_id}: {issue}")
        if validation_errors:
            self.log("ERROR review decisions are not grounded in candidate evidence.")
            for issue in validation_errors[:30]:
                self.log(f"- {issue}")
            if len(validation_errors) > 30:
                self.log(f"- ... {len(validation_errors) - 30} more")
            return 1

        decision_by_id = {str(item.get("candidate_id", "")).strip(): item for item in decisions}
        ordered_decisions: list[dict[str, Any]] = []
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(candidate_id: str) -> None:
            if candidate_id in visited:
                return
            if candidate_id in visiting:
                return
            visiting.add(candidate_id)
            decision = decision_by_id.get(candidate_id)
            if decision:
                merge_with = str(decision.get("merge_with") or "").strip()
                if merge_with in decision_by_id:
                    visit(merge_with)
                ordered_decisions.append(decision)
            visiting.discard(candidate_id)
            visited.add(candidate_id)

        for decision in decisions:
            visit(str(decision.get("candidate_id", "")).strip())

        stats: Counter[str] = Counter()
        reviewed = self.store.data[INDEX_META].setdefault("reviewed_candidates", {})
        reviewed_at = now_iso()
        candidate_to_memory: dict[str, str] = {}
        for decision in ordered_decisions:
            candidate_id = str(decision.get("candidate_id", "")).strip()
            pack_item = by_id.get(candidate_id)
            if not pack_item:
                stats["unknown"] += 1
                self.log(f"SKIP unknown candidate_id: {candidate_id}")
                continue
            reviewed[candidate_id] = {
                "reviewed_at": reviewed_at,
                "keep": decision.get("keep") is not False,
                "reason": str(decision.get("reason", "")).strip(),
                "source_file": pack_item.get("source_file", ""),
                "source_anchor": pack_item.get("source_anchor", ""),
                "text_hash": pack_item.get("text_hash", ""),
            }
            if decision.get("keep") is False:
                stats["discarded"] += 1
                continue
            base = pack_item.get("base_memory")
            if not isinstance(base, dict):
                stats["invalid"] += 1
                self.log(f"SKIP invalid base memory: {candidate_id}")
                continue
            candidate = self.apply_review_decision(base, decision)
            raw_merge_with = decision.get("merge_with")
            merge_with = str(raw_merge_with).strip() if raw_merge_with is not None else ""
            if merge_with:
                target_memory_id = candidate_to_memory.get(merge_with, merge_with)
                existing = self.store.memories().get(target_memory_id)
                if existing:
                    self.merge_memory(
                        target_memory_id,
                        existing,
                        candidate,
                        1.0,
                        replace=bool(decision.get("replace_summary")),
                    )
                    candidate_to_memory[candidate_id] = target_memory_id
                    stats["merged"] += 1
                    continue
                self.log(f"WARN merge_with not found, using normal duplicate check: {merge_with}")
            _memory_id, action = self.add_or_merge(candidate)
            candidate_to_memory[candidate_id] = _memory_id
            stats[action] += 1

        processed = self.store.data[INDEX_META].setdefault("processed_files", {})
        for source, digest in pack.get("processed_files", {}).items():
            if isinstance(source, str) and isinstance(digest, str):
                processed[source] = digest
        skipped_audit = self.store.data[INDEX_META].setdefault("skipped_review_candidates", {})
        for item in pack.get("skipped", []):
            if not isinstance(item, dict):
                continue
            key = candidate_uid(
                "skipped-review",
                f"{item.get('source_file', '')}:{item.get('source_anchor', '')}",
                f"{item.get('title_hint', '')}:{item.get('reason', '')}",
            )
            skipped_audit[key] = {
                "reviewed_at": reviewed_at,
                "source_file": item.get("source_file", ""),
                "source_anchor": item.get("source_anchor", ""),
                "title_hint": item.get("title_hint", ""),
                "reason": item.get("reason", ""),
                "high_value_reason": item.get("high_value_reason", ""),
            }

        expired = self.apply_expiry()
        copied = [self.vault_path / rel for rel in pack.get("copied_daily_files", []) if isinstance(rel, str)]
        cleaned = self.clean_unrelated_daily_files(copied)
        self.persist_index_outputs(save_index=True)
        self.clear_review_pack()

        self.log(
            "Review apply complete: "
            f"added={stats['added']}, merged={stats['merged']}, discarded={stats['discarded']}, "
            f"unknown={stats['unknown']}, invalid={stats['invalid']}, expired={int(expired)}, cleaned={int(cleaned)}"
        )
        return 0

    def build_memory(
        self,
        title: str,
        body: str,
        source_file: str,
        anchor: str,
        original_source_file: str,
    ) -> dict[str, Any]:
        created = now_iso()
        stage = "S1"
        summary = extract_summary(body)
        keyword_profile = extract_keyword_profile(body, title=title)
        memory = {
            "title": title[:100],
            "summary": summary,
            "keywords": keyword_profile["keywords"],
            "strong_keywords": keyword_profile["strong_keywords"],
            "stage": stage,
            "source_agent": source_agent_for(source_file) or "openclaw",
            "source_type": source_type_for(source_file),
            "quality_score": 1.0,
            "filtered_reason": None,
            "source_file": source_file,
            "source_anchor": anchor,
            "original_source_file": original_source_file,
            "excerpt": extract_excerpt(body),
            "created_at": created,
            "last_hit_at": None,
            "last_effective_hit_at": None,
            "raw_hit_count": 0,
            "effective_hit_count": 0,
            "expire_at": self.store.expire_at(stage),
            "hit_distribution": {word: 0 for word in TRIGGER_WORDS},
            "noise_score": 0,
            "merged_from": [],
            "sources": [
                {
                    "file": source_file,
                    "anchor": anchor,
                    "original_file": original_source_file,
                    "created_at": created,
                }
            ],
        }
        self.apply_process_memory_metadata(memory, body)
        return memory

    def apply_process_memory_metadata(self, memory: dict[str, Any], body: str) -> None:
        process = classify_process_memory(body)
        if not process:
            return
        memory.update(process)
        memory["stage"] = "S2"
        memory["expire_at"] = self.store.expire_at("S2")
        memory["quality_score"] = max(float(memory.get("quality_score", 0.0) or 0.0), 0.82)
        memory["memory_lane"] = "process"
        memory["source_confidence"] = memory.get("source_confidence") or "process_marker"
        memory["evidence_text"] = extract_excerpt(body, limit=evidence_limit_for_stage("S2"))

    def build_distilled_memory(
        self,
        title: str,
        body: str,
        source_file: str,
        anchor: str,
        original_source_file: str,
        origin: str,
        stage: str,
        metadata: dict[str, Any],
    ) -> dict[str, Any]:
        memory = self.build_memory(title, body, source_file, anchor, original_source_file)
        memory["stage"] = stage
        memory["expire_at"] = self.store.expire_at(stage)
        memory["candidate_origin"] = origin
        memory["candidate_uid"] = metadata.get("candidate_uid") or candidate_uid(origin, metadata.get("openclaw_key", ""), body)
        memory["source_type"] = "openclaw_distilled"
        memory["quality_score"] = float(metadata.get("quality_score", 1.0))
        memory.update(metadata)
        if stage in {"S2", "S3", "S4"}:
            memory["evidence_text"] = extract_excerpt(body, limit=evidence_limit_for_stage(stage))
        memory["sources"][0]["candidate_origin"] = origin
        return memory

    def build_agent_ingest_memory(
        self,
        agent: str,
        title: str,
        body: str,
        source_file: str,
        anchor: str,
    ) -> dict[str, Any]:
        stage = stage_for_agent_ingest(body)
        memory = self.build_memory(title, body, source_file, anchor, source_file)
        memory["stage"] = stage
        memory["expire_at"] = self.store.expire_at(stage)
        memory["source_agent"] = agent
        memory["source_type"] = "agent_ingest"
        memory["candidate_origin"] = f"{agent}-ingest"
        memory["candidate_uid"] = candidate_uid(f"{agent}-ingest", source_file, body)
        memory["memory_lane"] = "pending"
        memory["source_confidence"] = "agent_submitted"
        memory["quality_score"] = 0.8 if stage == "S2" else 0.65
        self.apply_process_memory_metadata(memory, body)
        memory["context_storage_policy"] = "summary_with_source_link"
        memory["original_context_file"] = source_file
        memory["original_context_anchor"] = anchor
        memory["sources"][0]["candidate_origin"] = memory["candidate_origin"]
        memory["sources"][0]["agent"] = agent
        return memory

    def stage_for_openclaw_candidate(self, metadata: dict[str, Any], default: str = "S1") -> str:
        origin = str(metadata.get("candidate_origin", ""))
        if origin == "openclaw-promoted-memory":
            return "S4"
        if origin in {"openclaw-deep", "openclaw-rem"}:
            return "S3"
        score = float(metadata.get("openclaw_score") or 0)
        recalls = int(metadata.get("openclaw_recall_count") or 0)
        grounded = int(metadata.get("openclaw_grounded_count") or 0)
        rem_hits = int(metadata.get("openclaw_rem_hits") or 0)
        if rem_hits > 0 or grounded > 0 or recalls >= 2 or score >= 0.82:
            return "S3"
        if recalls >= 1 or score >= OPENCLAW_RECALL_MIN_SCORE:
            return "S2"
        return default

    def find_duplicate(self, candidate: dict[str, Any]) -> tuple[str, dict[str, Any], float] | None:
        candidate_keywords = keyword_set(candidate)
        candidate_title = normalized_memory_title(str(candidate.get("title", "")))
        best: tuple[str, dict[str, Any], float] | None = None
        for memory_id, memory in self.store.memories().items():
            if is_conversation_memory(candidate) and is_conversation_memory(memory) and same_file_different_anchor(candidate, memory):
                continue
            memory_title = normalized_memory_title(str(memory.get("title", "")))
            score = jaccard(candidate_keywords, keyword_set(memory))
            if candidate_title and candidate_title == memory_title and not is_low_signal_profile_label(candidate_title):
                score = max(score, 0.95)
            if score >= 0.60 and (best is None or score > best[2]):
                best = (memory_id, memory, score)
        return best

    def merge_memory(
        self,
        memory_id: str,
        existing: dict[str, Any],
        candidate: dict[str, Any],
        score: float,
        replace: bool = False,
    ) -> None:
        source = {
            "file": candidate["source_file"],
            "anchor": candidate["source_anchor"],
            "original_file": candidate.get("original_source_file"),
            "created_at": now_iso(),
        }
        sources = existing.setdefault("sources", [])
        if (source["file"], source["anchor"]) not in {(item.get("file"), item.get("anchor")) for item in sources}:
            sources.append(source)

        if candidate.get("candidate_uid"):
            existing["merged_candidate_uids"] = sorted(
                set(existing.get("merged_candidate_uids", []) + [str(candidate["candidate_uid"])])
            )
        existing["merged_from"] = sorted(set(existing.get("merged_from", []) + [candidate["source_file"]]))
        existing["keywords"] = list(dict.fromkeys(existing.get("keywords", []) + candidate.get("keywords", [])))[:18]
        existing["strong_keywords"] = list(
            dict.fromkeys(existing.get("strong_keywords", []) + candidate.get("strong_keywords", []))
        )[:10]
        existing.setdefault("alternate_summaries", [])
        if candidate.get("summary") and candidate.get("summary") != existing.get("summary"):
            existing["alternate_summaries"] = list(
                dict.fromkeys(existing.get("alternate_summaries", []) + [candidate.get("summary")])
            )[:8]
        should_replace = replace or not existing.get("summary") or (
            STAGES.index(candidate.get("stage", "S1")) > STAGES.index(existing.get("stage", "S1"))
        )
        if should_replace:
            existing["summary"] = candidate["summary"]
            existing["excerpt"] = candidate["excerpt"]
            existing["source_file"] = candidate["source_file"]
            existing["source_anchor"] = candidate["source_anchor"]
            existing["original_source_file"] = candidate.get("original_source_file")
        for field in (
            "candidate_origin",
            "candidate_uid",
            "openclaw_key",
            "openclaw_score",
            "openclaw_max_score",
            "openclaw_recall_count",
            "openclaw_daily_count",
            "openclaw_grounded_count",
            "openclaw_light_hits",
            "openclaw_rem_hits",
            "source_agent",
            "source_type",
                "openclaw_concept_tags",
                "openclaw_confidence",
                "context_storage_policy",
                "original_context_file",
                "original_context_anchor",
                "memory_type",
                "lesson_type",
                "process_markers",
                "memory_lane",
            "source_confidence",
            ):
            if field in candidate and (should_replace or field not in existing):
                existing[field] = candidate[field]
        if candidate.get("stage") == "S4" or STAGES.index(candidate.get("stage", "S1")) > STAGES.index(existing.get("stage", "S1")):
            existing["stage"] = candidate.get("stage", existing.get("stage", "S1"))
            existing["expire_at"] = self.store.expire_at(existing["stage"])
        existing["updated_at"] = now_iso()
        self.log(f"MERGE {candidate['source_file']} -> {memory_id} keyword_overlap={score:.2f}")

    def add_or_merge(self, candidate: dict[str, Any]) -> tuple[str, str]:
        uid = candidate.get("candidate_uid")
        if uid:
            for memory_id, existing in self.store.memories().items():
                if existing.get("candidate_uid") == uid or str(uid) in set(existing.get("merged_candidate_uids", [])):
                    return memory_id, "unchanged"
        duplicate = self.find_duplicate(candidate)
        if duplicate:
            memory_id, existing, score = duplicate
            self.merge_memory(memory_id, existing, candidate, score)
            return memory_id, "merged"
        memory_id = self.store.next_id()
        self.store.data[memory_id] = candidate
        self.log(f"ADD {memory_id}: {candidate['title']}")
        return memory_id, "added"

    def ensure_vault_copy_for_source(self, source: str) -> str | None:
        vault_source = openclaw_daily_source(source)
        if not vault_source:
            return None
        original = self.openclaw_path / source
        if not original.exists():
            return None
        copy_path = self.vault_path / vault_source
        if original.exists() and not copy_path.exists():
            text = original.read_text(encoding="utf-8", errors="replace")
            self.sync_daily_copy(original, text)
        return vault_source

    def collect_recall_candidates(self) -> list[dict[str, Any]]:
        recall_path = self.openclaw_path / "memory" / ".dreams" / "short-term-recall.json"
        phase_path = self.openclaw_path / "memory" / ".dreams" / "phase-signals.json"
        if not recall_path.exists():
            return []
        try:
            recall_data = json.loads(recall_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            self.log(f"SKIP OpenClaw recall import: invalid JSON {self.source_rel(recall_path)}")
            return []
        try:
            phase_data = json.loads(phase_path.read_text(encoding="utf-8")) if phase_path.exists() else {}
        except json.JSONDecodeError:
            phase_data = {}

        entries = recall_data.get("entries", {})
        phases = phase_data.get("entries", {}) if isinstance(phase_data, dict) else {}
        if not isinstance(entries, dict):
            return []

        selected: list[tuple[float, dict[str, Any]]] = []
        for key, entry in entries.items():
            if not isinstance(entry, dict):
                continue
            source = str(entry.get("path") or "")
            vault_source = self.ensure_vault_copy_for_source(source)
            if not vault_source:
                continue
            snippet = str(entry.get("snippet") or "").strip()
            if not snippet or noise_reason_for_text(snippet):
                continue
            phase = phases.get(key, {}) if isinstance(phases, dict) else {}
            score = float(entry.get("totalScore") or 0)
            recalls = int(entry.get("recallCount") or 0)
            grounded = int(entry.get("groundedCount") or 0)
            rem_hits = int(phase.get("remHits") or 0) if isinstance(phase, dict) else 0
            if score < OPENCLAW_RECALL_MIN_SCORE and recalls < OPENCLAW_RECALL_MIN_RECALLS and grounded == 0 and rem_hits == 0:
                continue

            start = int(entry.get("startLine") or 1)
            end = int(entry.get("endLine") or start)
            tags = [str(item) for item in entry.get("conceptTags", []) if isinstance(item, str)]
            body = snippet
            if tags:
                body = f"{snippet}\n\nTags: {', '.join(tags[:12])}"
            metadata = {
                "candidate_origin": "openclaw-short-term-recall",
                "candidate_uid": candidate_uid("openclaw-short-term-recall", str(key), snippet),
                "openclaw_key": str(key),
                "openclaw_score": score,
                "openclaw_max_score": float(entry.get("maxScore") or score),
                "openclaw_recall_count": recalls,
                "openclaw_daily_count": int(entry.get("dailyCount") or 0),
                "openclaw_grounded_count": grounded,
                "openclaw_light_hits": int(phase.get("lightHits") or 0) if isinstance(phase, dict) else 0,
                "openclaw_rem_hits": rem_hits,
                "openclaw_concept_tags": tags[:20],
                "quality_score": min(1.0, max(0.7, score)),
            }
            stage = self.stage_for_openclaw_candidate(metadata)
            candidate = self.build_distilled_memory(
                first_title(snippet),
                body,
                vault_source,
                f"line {start}-{end}",
                source,
                "openclaw-short-term-recall",
                stage,
                metadata,
            )
            selected.append((score + recalls + grounded + rem_hits, candidate))

        selected.sort(key=lambda item: item[0], reverse=True)
        return [candidate for _score, candidate in selected[:OPENCLAW_RECALL_MAX_CANDIDATES]]

    def collect_dream_candidates(self, folder: str, origin: str) -> list[dict[str, Any]]:
        dream_dir = self.openclaw_path / "memory" / "dreaming" / folder
        if not dream_dir.exists():
            return []
        candidates: list[dict[str, Any]] = []
        pattern = re.compile(r"\[confidence=([0-9.]+)\s+evidence=([^\]]+)\]")
        for path in sorted(dream_dir.glob("*.md"))[-7:]:
            text = path.read_text(encoding="utf-8", errors="replace")
            for line_no, line in enumerate(text.splitlines(), start=1):
                match = pattern.search(line)
                if not match:
                    continue
                confidence = float(match.group(1))
                evidence = match.group(2).strip()
                if confidence < OPENCLAW_DREAM_MIN_CONFIDENCE:
                    continue
                evidence_match = re.match(r"(memory/\d{4}-\d{2}-\d{2}\.md):(\d+)(?:-(\d+))?", evidence)
                if not evidence_match:
                    continue
                source = evidence_match.group(1)
                start = evidence_match.group(2)
                end = evidence_match.group(3) or start
                vault_source = self.ensure_vault_copy_for_source(source)
                if not vault_source:
                    continue
                body = pattern.sub("", line).lstrip("- ").strip()
                if not body or blacklist_reason_for_text(body):
                    continue
                metadata = {
                    "candidate_origin": origin,
                    "candidate_uid": candidate_uid(origin, f"{path.name}:{line_no}:{evidence}", body),
                    "openclaw_confidence": confidence,
                    "openclaw_evidence": evidence,
                    "quality_score": confidence,
                }
                stage = self.stage_for_openclaw_candidate(metadata, default="S2")
                candidates.append(
                    self.build_distilled_memory(
                        first_title(body),
                        body,
                        vault_source,
                        f"line {start}-{end}",
                        source,
                        origin,
                        stage,
                        metadata,
                    )
                )
        return candidates

    def parse_session_corpus_blocks(self, path: Path) -> list[dict[str, Any]]:
        text = path.read_text(encoding="utf-8", errors="replace")
        blocks: list[dict[str, Any]] = []
        current: dict[str, Any] | None = None
        for line_no, line in enumerate(text.splitlines(), start=1):
            candidate_match = re.match(r"\s*-\s+Candidate:\s*(.+?)\s*$", line)
            if candidate_match:
                if current:
                    blocks.append(current)
                current = {
                    "body": candidate_match.group(1).strip(),
                    "line_no": line_no,
                    "confidence": 0.0,
                    "evidence": "",
                }
                continue
            if not current:
                continue
            confidence_match = re.search(r"confidence:\s*([0-9.]+)", line)
            if confidence_match:
                current["confidence"] = float(confidence_match.group(1))
            evidence_match = re.search(r"evidence:\s*(memory/\.dreams/session-corpus/[^\s]+)", line)
            if evidence_match:
                current["evidence"] = evidence_match.group(1).strip()
        if current:
            blocks.append(current)
        return blocks

    def session_candidate_is_curatable(self, body: str) -> bool:
        if not high_value_reason_for_text(body):
            return False
        lowered = body.lower()
        report_markers = [
            "write a dream diary entry",
            "心跳自检报告",
            "heartbeat 报告",
            "系统状态",
            "待跟进事项",
            "改进建议",
            "review schedule",
        ]
        resolution_markers = [
            "root cause",
            "final fix",
            "correct approach",
            "solved",
            "verified",
            "根因",
            "问题根源",
            "解决方案",
            "修复内容",
            "验证",
            "验证通过",
            "已解决",
            "最终方案",
            "正确做法",
            "决定",
            "约定",
            "改为",
            "改成",
            "失败原因",
        ]
        if any(marker in lowered for marker in report_markers) and not any(marker in lowered for marker in resolution_markers):
            return False
        if classify_process_memory(body):
            return True
        topic_markers = [
            "supertonic",
            "contexttoken",
            "volcengine",
            "npmjs",
            "github trending",
            "gh trending",
            "tavily",
            "飞书插件",
            "微信插件",
            "记忆同步",
        ]
        has_topic = any(marker in lowered for marker in topic_markers)
        has_resolution = any(marker in lowered for marker in resolution_markers)
        if "github trending" in lowered or "gh trending" in lowered:
            operational_markers = [
                "fix",
                "fixed",
                "fallback",
                "gh cli",
                "tavily",
                "timeout",
                "403",
                "cron",
                "updated",
                "修复",
                "兜底",
                "超时",
                "改成",
                "改为",
            ]
            return any(marker in lowered for marker in operational_markers)
        return has_topic and has_resolution

    def session_evidence_context(self, evidence: str, radius: int = 4, limit: int = 6000) -> str:
        match = re.match(r"(memory/\.dreams/session-corpus/\d{4}-\d{2}-\d{2}\.txt):(\d+)(?:-(\d+))?", evidence)
        if not match:
            return ""
        rel = match.group(1)
        start = int(match.group(2))
        end = int(match.group(3) or start)
        path = self.openclaw_path / rel
        if not path.exists() or not path.is_file():
            return ""
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        if not lines:
            return ""
        window_start = max(1, start - radius)
        window_end = min(len(lines), end + radius)
        snippet = "\n".join(lines[window_start - 1 : window_end]).strip()
        expanded = self.expand_session_jsonl_references(snippet, limit=limit)
        return extract_excerpt(expanded or snippet, limit=limit)

    def json_text_fragments(self, value: Any) -> list[str]:
        fragments: list[str] = []
        if isinstance(value, str):
            text = value.strip()
            if text:
                fragments.append(text)
        elif isinstance(value, list):
            for item in value:
                fragments.extend(self.json_text_fragments(item))
        elif isinstance(value, dict):
            preferred = ["role", "speaker", "content", "text", "message", "output"]
            for key in preferred:
                if key in value:
                    fragments.extend(self.json_text_fragments(value[key]))
        return fragments

    def read_jsonl_reference(self, rel: str, line_no: int) -> str:
        candidates = [
            self.openclaw_path / rel,
            self.openclaw_path.parent / rel,
            Path.home() / ".openclaw" / rel,
        ]
        path = next((item for item in candidates if item.exists() and item.is_file()), None)
        if not path:
            return ""
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        if line_no < 1 or line_no > len(lines):
            return ""
        raw = lines[line_no - 1]
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            return raw
        fragments = self.json_text_fragments(payload)
        return " ".join(dict.fromkeys(fragments))

    def expand_session_jsonl_references(self, text: str, limit: int = 6000) -> str:
        pieces: list[str] = []
        pattern = re.compile(r"\[(main/sessions/[^\]#]+\.jsonl)#L(\d+)\]")
        seen: set[tuple[str, int]] = set()
        for match in pattern.finditer(text):
            rel = match.group(1)
            line_no = int(match.group(2))
            key = (rel, line_no)
            if key in seen:
                continue
            seen.add(key)
            expanded = self.read_jsonl_reference(rel, line_no)
            if expanded:
                pieces.append(f"[{rel}#L{line_no}] {expanded}")
        if not pieces:
            return text
        return extract_excerpt("\n".join(pieces), limit=limit)

    def write_curated_session_evidence(self, day: str, uid: str, body: str, evidence: str) -> tuple[str, str]:
        path = self.agent_dir("openclaw") / "evidence" / f"{day}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        marker = f"<!-- memory-sync-session-candidate:{uid} -->"
        title = first_title(body)
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="replace")
        else:
            text = f"# OpenClaw evidence {day}\n\n"
        lines = text.splitlines()
        if marker not in text:
            if text and not text.endswith("\n"):
                text += "\n"
            if "## Curated Session Evidence" not in text:
                text += "\n## Curated Session Evidence\n"
            text += (
                f"\n### {title[:100]}\n"
                f"{marker}\n"
                f"Original evidence: `{evidence}`\n\n"
                f"{body.strip()}\n"
            )
            self.write_text_atomic(path, text.rstrip() + "\n")
            lines = (text.rstrip() + "\n").splitlines()
        start = next((index + 1 for index, line in enumerate(lines) if marker in line), len(lines))
        body_start = min(len(lines), start + 3)
        body_end = min(len(lines), body_start + max(1, len(body.splitlines())) - 1)
        return self.vault_rel(path), f"line {body_start}-{body_end}"

    def collect_session_corpus_candidates(self) -> list[dict[str, Any]]:
        dream_dir = self.openclaw_path / "memory" / "dreaming" / "light"
        if not dream_dir.exists():
            return []
        candidates: list[dict[str, Any]] = []
        for path in sorted(dream_dir.glob("*.md"))[-10:]:
            for block in self.parse_session_corpus_blocks(path):
                body = str(block.get("body") or "").strip()
                evidence = str(block.get("evidence") or "").strip()
                confidence = float(block.get("confidence") or 0)
                if confidence and confidence < OPENCLAW_DREAM_MIN_CONFIDENCE:
                    continue
                if not evidence or not self.session_candidate_is_curatable(body):
                    continue
                day_match = re.search(r"session-corpus/(\d{4}-\d{2}-\d{2})\.txt", evidence)
                day = day_match.group(1) if day_match else path.stem[:10]
                uid = candidate_uid("openclaw-session-curated", evidence, body)
                full_body = self.session_evidence_context(evidence) or body
                source_file, anchor = self.write_curated_session_evidence(day, uid, full_body, evidence)
                metadata = {
                    "candidate_origin": "openclaw-session-curated",
                    "candidate_uid": uid,
                    "openclaw_confidence": confidence,
                    "openclaw_evidence": evidence,
                    "original_session_evidence": evidence,
                    "quality_score": max(0.7, min(1.0, confidence or 0.72)),
                    "source_agent": "openclaw",
                    "source_confidence": "curated_session_evidence",
                    "curated_candidate_text": body,
                }
                memory = self.build_distilled_memory(
                    first_title(body),
                    full_body,
                    source_file,
                    anchor,
                    evidence,
                    "openclaw-session-curated",
                    "S2",
                    metadata,
                )
                memory["source_type"] = "agent_ingest"
                memory["original_context_file"] = source_file
                memory["original_context_anchor"] = anchor
                memory["sources"][0]["original_file"] = evidence
                candidates.append(memory)
        return candidates

    def collect_promoted_candidates(self) -> list[dict[str, Any]]:
        memory_path = self.openclaw_path / "MEMORY.md"
        if not memory_path.exists():
            return []
        lines = memory_path.read_text(encoding="utf-8", errors="replace").splitlines()
        candidates: list[dict[str, Any]] = []
        for index, line in enumerate(lines):
            marker = re.search(r"openclaw-memory-promotion:([^ ]+)", line)
            if not marker:
                continue
            body = lines[index + 1].strip("- ").strip() if index + 1 < len(lines) else marker.group(1)
            source_match = re.search(r"source=(memory/\d{4}-\d{2}-\d{2}\.md):(\d+)-(\d+)", body)
            if not source_match or blacklist_reason_for_text(body):
                continue
            source = source_match.group(1)
            vault_source = self.ensure_vault_copy_for_source(source)
            if not vault_source:
                continue
            score_match = re.search(r"score=([0-9.]+)", body)
            metadata = {
                "candidate_origin": "openclaw-promoted-memory",
                "candidate_uid": candidate_uid("openclaw-promoted-memory", marker.group(1), body),
                "openclaw_key": marker.group(1),
                "openclaw_score": float(score_match.group(1)) if score_match else 1.0,
                "quality_score": 1.0,
            }
            candidates.append(
                self.build_distilled_memory(
                    first_title(body),
                    body,
                    vault_source,
                    f"line {source_match.group(2)}-{source_match.group(3)}",
                    source,
                    "openclaw-promoted-memory",
                    "S4",
                    metadata,
                )
            )
        return candidates

    def import_openclaw_distilled_candidates(self) -> Counter[str]:
        stats: Counter[str] = Counter()
        if not CONFIG["OPENCLAW_IMPORT_DISTILLED"]:
            return stats
        candidates: list[dict[str, Any]] = []
        candidates.extend(self.collect_promoted_candidates())
        candidates.extend(self.collect_dream_candidates("deep", "openclaw-deep"))
        candidates.extend(self.collect_dream_candidates("rem", "openclaw-rem"))
        candidates.extend(self.collect_recall_candidates())
        raw_candidate_count = len(candidates)
        candidates = self.dedupe_memory_candidates(candidates)

        stats["candidates"] = len(candidates)
        stats["duplicate_candidates_removed"] = raw_candidate_count - len(candidates)
        for candidate in candidates:
            _memory_id, action = self.add_or_merge(candidate)
            stats[action] += 1
        if stats["candidates"]:
            self.store.data[INDEX_META]["openclaw_distilled_imported_at"] = now_iso()
            self.store.data[INDEX_META]["openclaw_distilled_imported_count"] = stats["candidates"]
            self.store.data[INDEX_META]["openclaw_distilled_imported_added"] = stats["added"]
            self.store.data[INDEX_META]["openclaw_distilled_imported_merged"] = stats["merged"]
        self.log(
            "OpenClaw distilled import: "
            f"candidates={stats['candidates']}, added={stats['added']}, merged={stats['merged']}, "
            f"unchanged={stats['unchanged']}, deduped={stats['duplicate_candidates_removed']}"
        )
        return stats

    def cmd_sync(self) -> int:
        if self.review_mode() == "rules":
            return self.cmd_sync_rules()
        return self.prepare_agent_review("sync")

    def cmd_sync_rules(self) -> int:
        memory_dir = self.openclaw_path / DAILY_DIR
        if not memory_dir.exists():
            self.log(f"ERROR memory directory not found: {memory_dir}")
            return 1

        processed = self.store.data[INDEX_META].setdefault("processed_files", {})
        referenced = self.store.referenced_files()
        changed_files = 0
        memory_stats: Counter[str] = Counter()
        unrelated_files: list[Path] = []

        for path in sorted(memory_dir.glob("*.md")):
            original_rel = self.source_rel(path)
            copy_path = self.vault_daily_path(path)
            copy_rel = self.vault_rel(copy_path)
            digest = file_hash(path)
            if processed.get(original_rel) == digest and (copy_path.exists() or copy_rel not in referenced):
                continue
            changed_files += 1
            text = path.read_text(encoding="utf-8", errors="replace")
            copy_path = self.sync_daily_copy(path, text)
            candidates: list[dict[str, Any]] = []
            for title, body, anchor in split_segments(text):
                reason = noise_reason_for_text(body)
                if reason:
                    self.log(f"SKIP segment reason={reason}: {copy_rel} {anchor} {title[:60]}")
                    continue
                candidates.append(self.build_memory(title, body, copy_rel, anchor, original_rel))

            if not candidates:
                unrelated_files.append(copy_path)
                processed[original_rel] = digest
                self.log(f"MARK daily copy for cleanup check reason=no_indexable_segments: {copy_rel}")
                continue

            for candidate in candidates:
                _memory_id, action = self.add_or_merge(candidate)
                memory_stats[action] += 1
            processed[original_rel] = digest

        distilled_stats = self.import_openclaw_distilled_candidates()
        memory_stats.update(distilled_stats)
        expired = self.apply_expiry()
        cleaned = self.clean_unrelated_daily_files(unrelated_files)
        changed = changed_files > 0 or memory_stats["added"] > 0 or memory_stats["merged"] > 0 or expired or cleaned
        self.persist_index_outputs(save_index=changed)

        self.log(
            "Sync complete: "
            f"files={changed_files}, added={memory_stats['added']}, merged={memory_stats['merged']}, "
            f"distilled_candidates={memory_stats['candidates']}"
        )
        return 0

    def clean_unrelated_daily_files(self, candidates: list[Path]) -> bool:
        indexed_refs = self.indexed_source_refs()
        changed = False
        for path in candidates:
            rel = self.vault_rel(path)
            if rel in indexed_refs:
                continue
            if path.exists():
                path.unlink()
                changed = True
            self.log(f"REMOVED unrelated vault daily copy reason=no_index_relationship: {rel}")
        return changed

    def clean_unindexed_source_archives(self) -> bool:
        if self.review_pack_path().exists():
            self.log("SKIP source archive cleanup while review pack is pending")
            return False
        source_root = self.vault_path / SOURCES_DIR
        if not source_root.exists():
            return False
        indexed_refs = self.indexed_source_refs()
        changed = False
        for path in sorted(source_root.rglob("*")):
            if not path.is_file():
                continue
            if path.name == "README.md":
                continue
            rel = self.vault_rel(path)
            if rel in indexed_refs:
                continue
            path.unlink()
            changed = True
            self.log(f"REMOVED unindexed source archive: {rel}")
        for path in sorted([item for item in source_root.rglob("*") if item.is_dir()], key=lambda item: len(item.parts), reverse=True):
            try:
                path.rmdir()
            except OSError:
                pass
        return changed

    def indexed_source_refs(self) -> set[str]:
        refs = set(self.store.referenced_files())
        roots = [
            self.vault_path / STATE_AGENTS_DIR,
            self.vault_path / STATE_SHARED_DIR,
        ]
        for root in roots:
            if not root.exists():
                continue
            for path in root.rglob("*.json"):
                try:
                    payload = json.loads(path.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    continue
                self.collect_index_source_refs(payload, refs)
        return refs

    def collect_index_source_refs(self, value: Any, refs: set[str], key: str | None = None) -> None:
        if isinstance(value, dict):
            for child_key, child_value in value.items():
                self.collect_index_source_refs(child_value, refs, str(child_key))
            return
        if isinstance(value, list):
            for item in value:
                self.collect_index_source_refs(item, refs, key)
            return
        if key not in INDEX_REFERENCE_KEYS or not isinstance(value, str):
            return
        for candidate in legacy_rel_path_candidates(value):
            rel = normalize_rel_path(candidate)
            if rel.startswith(f"{SOURCES_DIR}/") or rel.startswith(f"{PERSONAL_KNOWLEDGE_DIR}/"):
                refs.add(rel)

    def apply_expiry(self) -> bool:
        now = datetime.now()
        to_delete: list[str] = []
        changed = False
        for memory_id, memory in self.store.memories().items():
            stage = memory.get("stage", "S1")
            if stage == "S4":
                continue
            expire_at = parse_time(memory.get("expire_at"))
            if not expire_at or expire_at > now:
                continue
            if stage == "S1":
                to_delete.append(memory_id)
                self.log(f"EXPIRE remove {memory_id}: {memory.get('title')}")
                changed = True
            else:
                new_stage = PREVIOUS_STAGE.get(stage, "S1")
                memory["stage"] = new_stage
                memory["expire_at"] = self.store.expire_at(new_stage)
                memory["updated_at"] = now_iso()
                self.log(f"EXPIRE downgrade {memory_id}: {stage} -> {new_stage}")
                changed = True
        for memory_id in to_delete:
            self.store.data.pop(memory_id, None)
        return changed

    def cmd_search(self, query: str) -> int:
        query_lower = query.lower()
        terms = search_terms_for_query(query)
        if not terms:
            terms = [query_lower]
        results: list[tuple[float, str, dict[str, Any]]] = []
        for memory_id, memory in self.store.memories().items():
            haystack = " ".join(
                [
                    str(memory.get("title", "")),
                    str(memory.get("summary", "")),
                    str(memory.get("excerpt", "")),
                    str(memory.get("evidence_text", "")),
                    str(memory.get("source_file", "")),
                    str(memory.get("original_source_file", "")),
                    " ".join(memory.get("keywords", [])),
                    " ".join(memory.get("strong_keywords", [])),
                ]
            ).lower()
            score = 0.0
            for kw in memory.get("strong_keywords", []):
                normalized = normalize_keyword(str(kw))
                if normalized and (normalized in query_lower or query_lower in normalized):
                    score += 8
            for kw in memory.get("keywords", []):
                normalized = normalize_keyword(str(kw))
                if normalized and (normalized in query_lower or query_lower in normalized):
                    score += 4
            matched_terms = [term for term in terms if len(term) >= 2 and term in haystack]
            score += sum(1.5 if re.search(r"[\u4e00-\u9fff]", term) and len(term) >= 3 else 1 for term in matched_terms)
            if len(matched_terms) >= 2:
                score += min(4, len(matched_terms))
            if score:
                results.append((score, memory_id, memory))
        results.sort(key=lambda item: item[0], reverse=True)

        self.log(f"Search results: {len(results)}")
        for score, memory_id, memory in results[:10]:
            self.log(f"- {memory_id} [{memory.get('stage')}] score={score:.1f} {memory.get('title')}")
            self.log(f"  {memory.get('summary', '')}")
            source = str(memory.get("source_file") or "")
            anchor = str(memory.get("source_anchor") or "")
            original = str(memory.get("original_source_file") or "")
            if source:
                self.log(f"  source: {source} {anchor}".rstrip())
            if original and original != source:
                self.log(f"  original: {original}")
            evidence = str(memory.get("evidence_text") or memory.get("excerpt") or "")
            if evidence:
                self.log(f"  evidence: {compact_text(evidence, 240)}")
        return 0

    def trigger_words_in(self, text: str) -> list[str]:
        lowered = text.lower()
        return [word for word in TRIGGER_WORDS if word.lower() in lowered]

    def matching_memories(self, text: str) -> list[tuple[str, dict[str, Any], float, list[str]]]:
        lowered = text.lower()
        matches: list[tuple[str, dict[str, Any], float, list[str]]] = []
        for memory_id, memory in self.store.memories().items():
            keywords = [str(item) for item in memory.get("keywords", []) if not is_generic_keyword(str(item))]
            strong_keywords = [
                str(item) for item in memory.get("strong_keywords", []) if not is_generic_keyword(str(item))
            ]
            matched_strong = [kw for kw in strong_keywords if kw.lower() in lowered]
            matched_general = [kw for kw in keywords if kw.lower() in lowered and kw not in matched_strong]
            matched_specific = [kw for kw in matched_strong if normalize_keyword(kw) not in BROAD_MATCH_KEYWORDS]
            title = str(memory.get("title", "")).lower()
            summary = str(memory.get("summary", "")).lower()
            title_hit = bool(title and len(title) > 5 and title in lowered)
            summary_hit = any(kw.lower() in summary for kw in matched_specific)

            if len(matched_specific) >= 3:
                quality = 1.0
            elif len(matched_specific) >= 2:
                quality = 0.85
            elif len(matched_specific) == 1 and (
                title_hit or summary_hit or len(matched_general) + len(matched_strong) - len(matched_specific) >= 2
            ):
                quality = 0.7
            else:
                continue
            matches.append((memory_id, memory, quality, matched_strong + matched_general[:3]))
        matches.sort(key=lambda item: item[2], reverse=True)
        return matches

    def cmd_trigger_check(self, text: str) -> int:
        triggers = self.trigger_words_in(text)
        self.log(f"Trigger words: {', '.join(triggers) if triggers else '(none)'}")
        if not triggers:
            return 0
        matches = self.matching_memories(text)
        self.log(f"Matched memories: {len(matches)}")
        for memory_id, memory, quality, matched in matches[:10]:
            self.log(f"- {memory_id} quality={quality:.2f} {memory.get('title')}")
            self.log(f"  keywords: {', '.join(matched) if matched else '(title match)'}")
        return 0

    def cmd_diagnose(self, text: str) -> int:
        triggers = self.trigger_words_in(text)
        reason = noise_reason_for_text(text)
        process = classify_process_memory(text)
        profile = extract_keyword_profile(text)
        blocked, generic = keyword_diagnostics(text)
        matches = self.matching_memories(text)

        self.log(f"Trigger words: {', '.join(triggers) if triggers else '(none)'}")
        self.log(f"Filtered: {'yes' if reason else 'no'}")
        if reason:
            self.log(f"Filter reason: {reason}")
        self.log(f"Process memory: {process.get('lesson_type') if process else '(none)'}")
        self.log(f"Keywords: {', '.join(profile['keywords']) if profile['keywords'] else '(none)'}")
        self.log(
            f"Strong keywords: {', '.join(profile['strong_keywords']) if profile['strong_keywords'] else '(none)'}"
        )
        self.log(f"Blocked keyword candidates: {', '.join(blocked) if blocked else '(none)'}")
        self.log(f"Generic keyword candidates: {', '.join(generic) if generic else '(none)'}")
        self.log(f"Matched memories: {len(matches)}")
        for memory_id, memory, quality, matched in matches[:10]:
            self.log(f"- {memory_id} quality={quality:.2f} {memory.get('title')}")
            self.log(f"  matched: {', '.join(matched) if matched else '(title match)'}")
        return 0

    def cmd_trigger_hit(self, text: str) -> int:
        triggers = self.trigger_words_in(text)
        if not triggers:
            self.log("No trigger word found; no hit recorded.")
            return 0

        matches = self.matching_memories(text)
        if not matches:
            self.log("Trigger found, but no indexed memory matched.")
            return 0

        now = datetime.now()
        cooldown = timedelta(hours=CONFIG["HIT_COOLDOWN_HOURS"])
        changed = 0

        for memory_id, memory, quality, matched in matches:
            memory["raw_hit_count"] = int(memory.get("raw_hit_count", 0)) + 1
            memory["last_hit_at"] = now_iso()
            distribution = memory.setdefault("hit_distribution", {word: 0 for word in TRIGGER_WORDS})
            for trigger in triggers:
                distribution[trigger] = int(distribution.get(trigger, 0)) + 1

            last_effective = parse_time(memory.get("last_effective_hit_at"))
            if last_effective and now - last_effective < cooldown:
                self.log(f"COOLDOWN raw hit only: {memory_id}")
                changed += 1
                continue

            memory["effective_hit_count"] = int(memory.get("effective_hit_count", 0)) + 1
            memory["last_effective_hit_at"] = now_iso()

            noisy = self.apply_noise_rule(memory_id, memory)
            if not noisy:
                self.promote_if_needed(memory_id, memory, quality)
            changed += 1
            self.log(f"HIT {memory_id} quality={quality:.2f} keywords={', '.join(matched)}")

        self.persist_index_outputs(save_index=True)
        self.log(f"Trigger hit complete: changed={changed}")
        return 0

    def apply_noise_rule(self, memory_id: str, memory: dict[str, Any]) -> bool:
        distribution = memory.get("hit_distribution", {})
        total = sum(int(value) for value in distribution.values())
        if total < CONFIG["NOISE_MIN_HITS"]:
            return False
        trigger, count = max(distribution.items(), key=lambda item: int(item[1]))
        if count / max(1, total) < CONFIG["NOISE_DOMINANCE_RATIO"]:
            return False

        stage = memory.get("stage", "S1")
        memory["noise_score"] = int(memory.get("noise_score", 0)) + 1
        if stage == "S1":
            self.store.data.pop(memory_id, None)
            self.log(f"NOISE remove {memory_id}: dominated by trigger '{trigger}'")
        else:
            new_stage = PREVIOUS_STAGE.get(stage, "S1")
            memory["stage"] = new_stage
            memory["expire_at"] = self.store.expire_at(new_stage, 0.7)
            memory["updated_at"] = now_iso()
            self.log(f"NOISE downgrade {memory_id}: {stage} -> {new_stage}")
        return True

    def promote_if_needed(self, memory_id: str, memory: dict[str, Any], quality: float) -> None:
        hits = int(memory.get("effective_hit_count", 0))
        current = memory.get("stage", "S1")
        target = current
        if hits >= 3:
            target = "S4"
        elif hits >= 2:
            target = "S3"
        elif hits >= 1:
            target = "S2"

        if STAGES.index(target) > STAGES.index(current):
            memory["stage"] = target
            self.log(f"PROMOTE {memory_id}: {current} -> {target}")

        memory["expire_at"] = self.store.expire_at(memory["stage"], quality)
        memory["updated_at"] = now_iso()

        if memory["stage"] == "S4" and not memory.get("permanent_file"):
            self.extract_permanent_memory(memory_id, memory)

    def extract_permanent_memory(self, memory_id: str, memory: dict[str, Any]) -> None:
        relative = f"{PERMANENT_DIR}/{memory_id}-{safe_name(memory.get('title', 'memory'))}.md"
        memory["permanent_file"] = relative
        path = self.vault_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        sources = "\n".join(f"- {item.get('file')} {item.get('anchor', '')}" for item in memory.get("sources", []))
        content = (
            f"# {memory.get('title')}\n\n"
            f"{memory.get('summary', '')}\n\n"
            "## Keywords\n\n"
            + ", ".join(memory.get("keywords", []))
            + "\n\n## Excerpt\n\n"
            + memory.get("excerpt", "")
            + "\n\n## Sources\n\n"
            + sources
            + "\n"
        )
        path.write_text(content, encoding="utf-8")

    def write_obsidian_index(self) -> bool:
        path = self.vault_path / OBSIDIAN_INDEX_FILE
        path.parent.mkdir(parents=True, exist_ok=True)
        memories = self.store.memories()
        counts = Counter(memory.get("stage", "S1") for memory in memories.values())
        updated_at = self.store.data.get(INDEX_META, {}).get("updated_at") or now_iso()
        lines = [
            "# Memory Index / 全局记忆索引",
            "",
            f"> 自动生成文件。`{STATE_INDEX_DIR}/{INDEX_NAME}` 是机器真相源，本文件是 Obsidian 可读入口。",
            "",
            f"- 更新时间：{updated_at}",
            f"- 记忆总数：{len(memories)}",
            f"- 阶段分布：S1={counts.get('S1', 0)}，S2={counts.get('S2', 0)}，S3={counts.get('S3', 0)}，S4={counts.get('S4', 0)}",
            "",
        ]
        for stage in STAGES:
            stage_items = [
                (memory_id, memory)
                for memory_id, memory in memories.items()
                if memory.get("stage", "S1") == stage
            ]
            lines.extend([f"## {stage}", ""])
            if not stage_items:
                lines.extend(["_暂无_", ""])
                continue
            for memory_id, memory in sorted(stage_items, key=lambda item: str(item[1].get("title", ""))):
                title = str(memory.get("title", "Untitled memory")).replace("\n", " ")
                summary = str(memory.get("summary", "")).replace("\n", " ")
                keywords = ", ".join(str(item) for item in memory.get("strong_keywords") or memory.get("keywords", [])[:6])
                source = str(memory.get("source_file", ""))
                expire_at = memory.get("expire_at") or "permanent"
                lines.append(f"### {memory_id} - {title}")
                lines.append("")
                if summary:
                    lines.append(summary)
                    lines.append("")
                lines.append(f"- 阶段：{memory.get('stage', 'S1')}")
                lines.append(f"- 有效命中：{memory.get('effective_hit_count', 0)}")
                if memory.get("candidate_origin"):
                    lines.append(f"- Candidate origin：{memory.get('candidate_origin')}")
                if memory.get("openclaw_score") is not None:
                    lines.append(f"- OpenClaw score：{memory.get('openclaw_score')}")
                if memory.get("openclaw_confidence") is not None:
                    lines.append(f"- OpenClaw confidence：{memory.get('openclaw_confidence')}")
                lines.append(f"- 过期时间：{expire_at}")
                if keywords:
                    lines.append(f"- 关键词：{keywords}")
                if source:
                    lines.append(f"- 来源：[[{source}]]")
                if memory.get("permanent_file"):
                    lines.append(f"- 永久文件：[[{memory['permanent_file']}]]")
                lines.append("")
        content = "\n".join(lines).rstrip() + "\n"
        if path.exists() and path.read_text(encoding="utf-8") == content:
            return False
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(content, encoding="utf-8")
        os.replace(tmp, path)
        return True

    def memory_page_rel(self, memory_id: str, memory: dict[str, Any]) -> str:
        return f"{MEMORY_PAGES_DIR}/{memory_id}.md"

    def yaml_scalar(self, value: Any) -> str:
        text = str(value or "").replace("\\", "/").replace('"', '\\"')
        return f'"{text}"'

    def yaml_list(self, values: list[Any]) -> list[str]:
        items = [str(item).strip() for item in values if str(item).strip()]
        if not items:
            return ["[]"]
        return [f"- {self.yaml_scalar(item)}" for item in items[:12]]

    def memory_page_markdown(self, memory_id: str, memory: dict[str, Any]) -> str:
        keywords = memory.get("strong_keywords") or memory.get("keywords", [])
        tags = [
            "memory-sync/memory",
            f"memory-sync/stage/{memory.get('stage', 'S1')}",
            f"agent/{self.memory_agent(memory)}",
        ]
        if memory_is_shared(memory):
            tags.append("memory-sync/shared")
        frontmatter = [
            "---",
            "type: memory",
            f"memory_id: {self.yaml_scalar(memory_id)}",
            f"stage: {self.yaml_scalar(memory.get('stage', 'S1'))}",
            f"source_agent: {self.yaml_scalar(self.memory_agent(memory))}",
            f"memory_lane: {self.yaml_scalar(memory.get('memory_lane') or ('official' if memory.get('stage') in {'S3', 'S4'} else 'pending'))}",
            f"source_file: {self.yaml_scalar(memory.get('source_file', ''))}",
            f"source_anchor: {self.yaml_scalar(memory.get('source_anchor', ''))}",
            f"expire_at: {self.yaml_scalar(memory.get('expire_at') or 'permanent')}",
            "keywords:",
            *self.yaml_list(keywords),
            "tags:",
            *self.yaml_list(tags),
            "---",
            "",
        ]
        lines = frontmatter + [
            f"# {memory.get('title', 'Untitled memory')}",
            "",
            str(memory.get("summary", "")).strip(),
            "",
            "## Status",
            "",
            f"- Stage: {memory.get('stage', 'S1')}",
            f"- Effective hits: {memory.get('effective_hit_count', 0)}",
            f"- Source agent: {self.memory_agent(memory)}",
            f"- Shared context: {'yes' if memory_is_shared(memory) else 'no'}",
            "",
            "## Links",
            "",
            f"- Index: [[{OBSIDIAN_INDEX_FILE}]]",
            f"- User profile: [[{PROFILE_MD_FILE}]]",
        ]
        source = str(memory.get("source_file", ""))
        if source:
            lines.append(f"- Source: [[{source}]]")
            readable = source.replace("/conversations/", "/conversation-summaries/")
            if readable != source and (self.vault_path / readable).exists():
                lines.append(f"- Readable transcript: [[{readable}]]")
        if memory.get("permanent_file"):
            lines.append(f"- Permanent: [[{memory['permanent_file']}]]")
        source_items = memory.get("sources") or []
        if isinstance(source_items, list) and len(source_items) > 1:
            lines.extend(["", "## Source Anchors", ""])
            for item in source_items[:20]:
                if not isinstance(item, dict):
                    continue
                item_file = str(item.get("file", ""))
                item_anchor = str(item.get("anchor", ""))
                if item_file:
                    lines.append(f"- [[{item_file}]] {item_anchor}".rstrip())
        if keywords:
            lines.extend(["", "## Keywords", "", ", ".join(str(item) for item in keywords[:12])])
        excerpt = str(memory.get("evidence_text") or memory.get("excerpt", "")).strip()
        if excerpt:
            lines.extend(["", "## Evidence", "", excerpt])
        return "\n".join(lines).rstrip() + "\n"

    def write_obsidian_memory_pages(self) -> None:
        page_dir = self.vault_path / MEMORY_PAGES_DIR
        expected: set[Path] = set()
        for memory_id, memory in self.store.memories().items():
            if str(memory.get("stage", "S1")) == "S1":
                continue
            rel = self.memory_page_rel(memory_id, memory)
            path = self.vault_path / rel
            expected.add(path.resolve())
            self.write_text_atomic(path, self.memory_page_markdown(memory_id, memory))
        if page_dir.exists():
            for path in page_dir.glob("memory_*.md"):
                if path.resolve() not in expected:
                    path.unlink()

    def write_memory_dashboard(self, profile: dict[str, Any] | None = None, context: dict[str, Any] | None = None) -> None:
        memories = self.store.memories()
        counts = Counter(memory.get("stage", "S1") for memory in memories.values())
        shared_count = sum(1 for memory in memories.values() if memory_is_shared(memory))
        top_memories = self.memory_snapshot(limit=8, shared_only=True)
        profile_brief = ""
        if profile:
            profile_brief = str(profile.get("profile_brief", ""))
        elif context:
            profile_brief = str(context.get("profile_brief", ""))
        lines = [
            "# Memory Dashboard",
            "",
            "> 自动生成的 Obsidian 记忆入口。JSON 仍是机器真相源；这里用于浏览、反链、筛选和人工校验。",
            "",
            f"- Generated: {now_iso()}",
            f"- Total memories: {len(memories)}",
            f"- Shared memories: {shared_count}",
            f"- Stage distribution: S1={counts.get('S1', 0)}, S2={counts.get('S2', 0)}, S3={counts.get('S3', 0)}, S4={counts.get('S4', 0)}",
            "",
            "## Core Links",
            "",
            f"- [[{OBSIDIAN_INDEX_FILE}]]",
            f"- [[{PROFILE_MD_FILE}]]",
            f"- [[{MEMORY_DIRECTORY_FILE}]]",
            f"- [[{SHARED_CONTEXT_DIR}/agent_brief.md]]",
            f"- Machine state: `{MACHINE_DIR}`",
            "",
        ]
        if profile_brief:
            lines.extend(["## User Brief", "", profile_brief, ""])
        lines.extend(["## Shared Memory Snapshot", ""])
        if not top_memories:
            lines.extend(["_No shared memories yet._", ""])
        for memory in top_memories:
            memory_id = str(memory.get("id", ""))
            page = self.memory_page_rel(memory_id, memories[memory_id]) if memory_id in memories else ""
            title = str(memory.get("title", "Untitled memory"))
            lines.append(f"- [[{page}|{memory_id}]] [{memory.get('stage')}] {title}")
            if memory.get("summary"):
                lines.append(f"  - {compact_text(str(memory.get('summary')), 140)}")
        lines.extend(["", "## Agent Stores", ""])
        for agent in ADAPTER_NAMES:
            lines.append(f"- {agent}: [[{STATE_AGENTS_DIR}/{agent}/index.json]]")
        lines.extend(["", "## Optional Dataview", "", "```dataview", f'TABLE stage, source_agent, expire_at FROM "{MEMORY_PAGES_DIR}" SORT stage DESC', "```", ""])
        self.write_text_atomic(self.vault_path / MEMORY_DASHBOARD_FILE, "\n".join(lines).rstrip() + "\n")

    def recent_markdown_links(self, root_rel: str, limit: int = 20) -> list[str]:
        root = self.vault_path / root_rel
        if not root.exists():
            return []
        files = sorted(
            [path for path in root.rglob("*.md") if path.is_file()],
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        return [self.vault_rel(path) for path in files[:limit]]

    def cleanup_generated_directory_readmes(self) -> None:
        for path in self.vault_path.rglob("README.md"):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            generated_by_memory_sync = (
                "[[Dashboard/Memory Directory.md|Memory Directory]]" in text
                and ("目录入口页" in text or "directory entry page" in text)
            )
            if generated_by_memory_sync:
                path.unlink()

    def write_memory_directory(self) -> None:
        language = self.preferred_language()
        zh = language == "zh"
        if zh:
            title = "Memory Directory / 记忆目录"
            note = "文件说明：这是 Memory Sync 自动生成的 Obsidian 导航目录，用正向链接连接记忆索引、跨 Agent 上下文和个人知识入口。"
            generated = "生成时间"
            dashboard_label = "核心入口"
            memory_label = "记忆卡片"
            context_label = "跨 Agent 上下文"
            personal_label = "个人知识"
            dashboard_rows = [
                (PROFILE_MD_FILE, PROFILE_MD_FILE, "动态用户画像，用于帮助 agent 理解用户偏好、项目背景和协作边界。"),
                (REFERENCE_AGENT_SKILLS_MD_FILE, REFERENCE_AGENT_SKILLS_MD_FILE, "已同步的 skill 能力总览，用于让 agent 知道当前可用工具。"),
            ]
            memory_directory_rows = [
                (OBSIDIAN_INDEX_FILE, OBSIDIAN_INDEX_FILE, "记忆内容、阶段、来源追溯都从这里进入。"),
                (MEMORY_DASHBOARD_FILE, MEMORY_DASHBOARD_FILE, "查看记忆总量、阶段分布和共享记忆概览。"),
            ]
            context_rows = [
                (f"{SHARED_CONTEXT_DIR}/agent_brief.md", f"{SHARED_CONTEXT_DIR}/agent_brief.md", "跨 agent 精简上下文，切换 agent 或交接任务前优先看这里。"),
            ]
            personal_rows = [
                (AGENT_SKILLS_MD_FILE, "Personal/Agent Knowledge/Agent Skills.md", "个人视角的 Agent Skill 总清单。", True),
                (f"{PERSONAL_KNOWLEDGE_DIR}/openclaw/USER.md", "Personal/Agent Knowledge/openclaw/USER.md", "OpenClaw 用户画像源文件。", True),
                (f"{PERSONAL_KNOWLEDGE_DIR}/openclaw/AGENTS.md", "Personal/Agent Knowledge/openclaw/AGENTS.md", "OpenClaw 行为规则源文件。", True),
                (f"{PERSONAL_KNOWLEDGE_DIR}/openclaw/MEMORY.md", "Personal/Agent Knowledge/openclaw/MEMORY.md", "OpenClaw 长期记忆源文件。", True),
            ]
        else:
            title = "Memory Directory"
            note = "File note: this auto-generated Obsidian navigation directory links memory indexes, cross-agent context, and personal knowledge entries."
            generated = "Generated"
            dashboard_label = "Core Entries"
            memory_label = "Memory Pages"
            context_label = "Cross-Agent Context"
            personal_label = "Personal Knowledge"
            dashboard_rows = [
                (PROFILE_MD_FILE, "User Profile", "Dynamic user profile for preferences, project background, and collaboration boundaries."),
                (REFERENCE_AGENT_SKILLS_MD_FILE, "Agent Skills", "Synced skill capability overview so agents know which tools are available."),
            ]
            memory_directory_rows = [
                (OBSIDIAN_INDEX_FILE, "Memory Summary Index", "Enter memories, stages, and source trace links here."),
                (MEMORY_DASHBOARD_FILE, "Memory Dashboard", "View memory counts, stage distribution, and shared-memory overview."),
            ]
            context_rows = [
                (f"{SHARED_CONTEXT_DIR}/agent_brief.md", "Cross-Agent Overview", "Portable brief for agent switching and handoff."),
            ]
            personal_rows = [
                (AGENT_SKILLS_MD_FILE, "Personal/Agent Knowledge/Agent Skills.md", "Personal Agent Skill index.", True),
                (f"{PERSONAL_KNOWLEDGE_DIR}/openclaw/USER.md", "Personal/Agent Knowledge/openclaw/USER.md", "OpenClaw user profile source.", True),
                (f"{PERSONAL_KNOWLEDGE_DIR}/openclaw/AGENTS.md", "Personal/Agent Knowledge/openclaw/AGENTS.md", "OpenClaw behavior rules source.", True),
                (f"{PERSONAL_KNOWLEDGE_DIR}/openclaw/MEMORY.md", "Personal/Agent Knowledge/openclaw/MEMORY.md", "OpenClaw long-term memory source.", True),
            ]

        def file_link(rel: str, label: str) -> str:
            return f"[[{rel}|{label}]]"

        self.cleanup_generated_directory_readmes()

        lines = [
            f"# {title}",
            "",
            f"> {note}",
            "",
            f"- {generated}: {now_iso()}",
            "",
            f"## {dashboard_label}",
            "",
        ]
        for rel, label, description in dashboard_rows:
            lines.append(f"- {file_link(rel, label)}：{description}")
        lines.extend(["", f"## {memory_label}", ""])
        for rel, label, description in memory_directory_rows:
            lines.append(f"- {file_link(rel, label)}：{description}")

        lines.extend(["", f"## {context_label}", ""])
        for rel, label, description in context_rows:
            lines.append(f"- {file_link(rel, label)}：{description}")

        lines.extend(["", f"## {personal_label}", ""])
        for rel, label, description, _should_link in personal_rows:
            lines.append(f"- {file_link(rel, label)}：{description}")

        self.write_text_atomic(self.vault_path / MEMORY_DIRECTORY_FILE, "\n".join(lines).rstrip() + "\n")

    def cleanup_retired_dashboard_pages(self) -> None:
        for rel in RETIRED_DASHBOARD_FILES:
            path = self.vault_path / rel
            if path.exists() and path.is_file():
                path.unlink()

    def cleanup_retired_layout_dirs(self) -> None:
        vault_root = self.vault_path.resolve()
        for rel in RETIRED_LAYOUT_DIRS:
            if rel == CONTEXT_DIR and CONFIG["LEGACY_CONTEXT_ENABLED"]:
                continue
            path = self.vault_path / rel
            if not path.exists():
                continue
            target = path.resolve()
            try:
                target.relative_to(vault_root)
            except ValueError as exc:
                raise RuntimeError(f"Refusing to clean path outside vault: {target}") from exc
            if target == vault_root:
                raise RuntimeError(f"Refusing to clean vault root: {target}")
            if path.is_dir():
                shutil.rmtree(path)
            elif path.is_file():
                path.unlink()

    def write_obsidian_surfaces(self, profile: dict[str, Any] | None = None, context: dict[str, Any] | None = None) -> None:
        self.write_obsidian_index()
        self.write_obsidian_memory_pages()
        self.write_memory_dashboard(profile=profile, context=context)
        self.cleanup_retired_dashboard_pages()
        self.cleanup_retired_layout_dirs()
        self.write_memory_directory()

    def memory_agent(self, memory: dict[str, Any]) -> str:
        return str(memory.get("source_agent") or "openclaw")

    def agent_dir(self, agent: str) -> Path:
        return self.vault_path / AGENTS_DIR / agent

    def agent_state_dir(self, agent: str) -> Path:
        return self.vault_path / STATE_AGENTS_DIR / agent

    def agent_memories(self, agent: str) -> dict[str, dict[str, Any]]:
        return {
            memory_id: memory
            for memory_id, memory in self.store.memories().items()
            if self.memory_agent(memory) == agent
        }

    def write_json_atomic(self, path: Path, data: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        self.replace_file_with_retry(tmp, path)

    def write_text_atomic(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(text, encoding="utf-8")
        self.replace_file_with_retry(tmp, path)

    def replace_file_with_retry(self, tmp: Path, path: Path) -> None:
        for attempt in range(8):
            try:
                os.replace(tmp, path)
                return
            except PermissionError:
                if attempt == 7:
                    raise
                time.sleep(0.15 * (attempt + 1))

    def write_path_map(self) -> None:
        payload = {
            "_meta": {
                "schema": "memory-sync-path-map",
                "generated_at": now_iso(),
                "policy": "Direct writes use the new layout. Legacy paths are read-only aliases for old indexes and source links.",
            },
            "new_layout": {
                "dashboard": DASHBOARD_DIR,
                "sources": SOURCES_DIR,
                "memories": MEMORY_PAGES_DIR,
                "context": SHARED_CONTEXT_DIR,
                "machine_state": MACHINE_DIR,
                "machine_index": STATE_INDEX_DIR,
                "machine_agents": STATE_AGENTS_DIR,
                "machine_shared": STATE_SHARED_DIR,
                "machine_review": STATE_REVIEW_DIR,
                "personal_knowledge": PERSONAL_KNOWLEDGE_DIR,
            },
            "legacy_aliases": {
                "02-Lessons/OpenClaw-Daily/": VAULT_DAILY_DIR + "/",
                "03-Reference/OpenClaw-Permanent/": PERMANENT_DIR + "/",
                "03-Reference/Memories/": MEMORY_PAGES_DIR + "/",
                "03-Reference/": DASHBOARD_DIR + "/",
                "Dashboard/\u5168\u5c40\u8bb0\u5fc6\u7d22\u5f15.md": OBSIDIAN_INDEX_FILE,
                "_index/": STATE_INDEX_DIR + "/",
                "_agents/<agent>/daily/": f"{SOURCES_DIR}/<agent>/daily/",
                "_agents/<agent>/conversations/": f"{SOURCES_DIR}/<agent>/conversations/",
                "_agents/<agent>/evidence/": f"{SOURCES_DIR}/<agent>/evidence/",
                "_agents/<agent>/summaries/": f"{STATE_AGENTS_DIR}/<agent>/summaries/",
                "_agents/<agent>/index.json": f"{STATE_AGENTS_DIR}/<agent>/index.json",
                "_agents/<agent>/skills.json": f"{STATE_AGENTS_DIR}/<agent>/skills.json",
                "_agents/<agent>/skills.md": f"{STATE_AGENTS_DIR}/<agent>/skills.md",
                "_shared/context/": SHARED_CONTEXT_DIR + "/",
                "_shared/": STATE_SHARED_DIR + "/",
                "_review/memory-sync/": STATE_REVIEW_DIR + "/",
            },
        }
        self.write_json_atomic(self.vault_path / PATH_MAP_FILE, payload)

    def agent_memory_record(self, memory_id: str, memory: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": memory_id,
            "title": memory.get("title", ""),
            "summary": memory.get("summary", ""),
            "keywords": memory.get("keywords", []),
            "strong_keywords": memory.get("strong_keywords", []),
            "stage": memory.get("stage", "S1"),
            "memory_lane": memory.get("memory_lane") or ("official" if memory.get("stage") in {"S3", "S4"} else "pending"),
            "source_agent": self.memory_agent(memory),
            "source_confidence": memory.get("source_confidence") or ("distilled" if memory.get("candidate_origin") else "inferred"),
            "source_file": memory.get("source_file", ""),
            "source_anchor": memory.get("source_anchor", ""),
            "original_context_file": memory.get("original_context_file") or memory.get("source_file", ""),
            "original_context_anchor": memory.get("original_context_anchor") or memory.get("source_anchor", ""),
            "candidate_origin": memory.get("candidate_origin"),
            "candidate_uid": memory.get("candidate_uid"),
            "memory_type": memory.get("memory_type"),
            "lesson_type": memory.get("lesson_type"),
            "process_markers": memory.get("process_markers"),
            "effective_hit_count": memory.get("effective_hit_count", 0),
            "expire_at": memory.get("expire_at"),
        }

    def write_agent_local_stores(self) -> None:
        for agent in ADAPTER_NAMES:
            source_base = self.agent_dir(agent)
            state_base = self.agent_state_dir(agent)
            for name in ("daily", "handoffs", "evidence", "conversations", "conversation-summaries", "permanent"):
                (source_base / name).mkdir(parents=True, exist_ok=True)
            state_base.mkdir(parents=True, exist_ok=True)

            memories = self.agent_memories(agent)
            records = {
                memory_id: self.agent_memory_record(memory_id, memory)
                for memory_id, memory in sorted(memories.items())
            }
            payload = {
                "_meta": {
                    "schema": "memory-sync-agent-store",
                    "agent": agent,
                    "generated_at": now_iso(),
                    "record_count": len(records),
                },
                    "memories": records,
            }
            self.write_json_atomic(state_base / "index.json", payload)

            by_date: dict[str, list[dict[str, Any]]] = {}
            for memory_id, memory in memories.items():
                source = str(memory.get("source_file", ""))
                match = re.search(r"(\d{4}-\d{2}-\d{2})\.md", source)
                day = match.group(1) if match else "undated"
                by_date.setdefault(day, []).append(self.agent_memory_record(memory_id, memory))
            summary_dir = state_base / "summaries"
            summary_dir.mkdir(parents=True, exist_ok=True)
            expected_summary_paths = {summary_dir / f"{day}.json" for day in by_date}
            for day, items in by_date.items():
                self.write_json_atomic(
                    summary_dir / f"{day}.json",
                    {
                        "_meta": {"schema": "memory-sync-agent-day-summary", "agent": agent, "date": day, "generated_at": now_iso()},
                        "items": items,
                    },
                )
            for old_summary in summary_dir.glob("*.json"):
                if old_summary not in expected_summary_paths:
                    old_summary.unlink()

        openclaw_daily = self.vault_path / VAULT_DAILY_DIR
        agent_daily = self.agent_dir("openclaw") / "daily"
        if openclaw_daily.exists():
            for path in openclaw_daily.glob("*.md"):
                target = agent_daily / path.name
                if not target.exists() or file_hash(path) != file_hash(target):
                    target.write_text(path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")

    def skill_roots(self) -> list[tuple[str, str, Path]]:
        home = Path.home()
        roots: list[tuple[str, str, Path]] = [
            ("openclaw", "workspace", self.openclaw_path / "skills"),
            ("openclaw", "user", home / ".openclaw" / "skills"),
            ("codex", "user", home / ".codex" / "skills"),
            ("codex", "system", home / ".codex" / "skills" / ".system"),
            ("codex", "plugins", home / ".codex" / "plugins" / "cache"),
            ("claude", "user", home / ".claude" / "skills"),
            ("opencode", "user", home / ".config" / "opencode" / "skills"),
            ("opencode", "windows-user", home / "AppData" / "Roaming" / "opencode" / "skills"),
            ("hermes-agent", "user", home / ".hermes-agent" / "skills"),
            ("hermes-agent", "home", self.hermes_home() / "skills"),
            ("qoder", "user", home / ".qoder" / "skills"),
            ("qoder", "extensions", home / ".qoder" / "extensions"),
            ("shared", "agents", home / ".agents" / "skills"),
        ]
        appdata = os.environ.get("APPDATA")
        if appdata:
            roots.append(("openclaw", "official-npm", Path(appdata) / "npm" / "node_modules" / "openclaw" / "skills"))
            roots.append(("qoder", "appdata", Path(appdata) / "Qoder" / "User" / "globalStorage"))
        local_appdata = os.environ.get("LOCALAPPDATA")
        if local_appdata:
            roots.append(("hermes-agent", "localappdata", Path(local_appdata) / "hermes" / "skills"))
        extra = os.environ.get("MEMORY_SYNC_SKILL_DIRS", "")
        for index, raw in enumerate([item for item in extra.split(os.pathsep) if item.strip()], start=1):
            roots.append(("custom", f"extra-{index}", expand_path(raw)))

        seen: set[str] = set()
        result = []
        for agent, level, path in roots:
            key = path.as_posix().lower()
            if key in seen:
                continue
            seen.add(key)
            result.append((agent, level, path))
        return result

    def openclaw_skill_manifest_descriptions(self) -> dict[str, str]:
        descriptions: dict[str, str] = {}
        for rel in ("SKILLS.md", "skills/ALL_SKILLS_MANIFEST.md"):
            path = self.openclaw_path / rel
            text = self.read_optional_text(path, limit=300000)
            if text:
                descriptions.update(parse_skill_manifest(text))
        return descriptions

    def collect_skill_inventory(self) -> dict[str, Any]:
        manifest_descriptions = self.openclaw_skill_manifest_descriptions()
        records: list[dict[str, Any]] = []
        seen_paths: set[str] = set()
        for agent, level, root in self.skill_roots():
            if not root.exists() or not root.is_dir():
                continue
            count = 0
            for skill_doc in sorted(root.rglob("SKILL.md")):
                if count >= 500:
                    break
                normalized = skill_doc.resolve().as_posix().lower()
                if normalized in seen_paths:
                    continue
                seen_paths.add(normalized)
                try:
                    record = parse_skill_doc(skill_doc)
                except OSError:
                    continue
                if record["name"] in manifest_descriptions and (
                    not record["description"] or record["description"] == "No description provided."
                ):
                    record["description"] = compact_text(manifest_descriptions[record["name"]], 220)
                record.update(
                    {
                        "agent": agent,
                        "level": level,
                        "root": root.as_posix(),
                        "relative_path": skill_doc.relative_to(root).as_posix(),
                    }
                )
                records.append(record)
                count += 1
        records.sort(key=lambda item: (str(item.get("agent")), str(item.get("level")), str(item.get("name"))))
        return {
            "_meta": {
                "schema": "memory-sync-agent-skill-inventory",
                "generated_at": now_iso(),
                "record_count": len(records),
                "policy": "Personal vault output may include local paths; public releases should keep only generic scan logic.",
            },
            "skills": records,
        }

    def write_skill_inventory(self) -> dict[str, Any]:
        inventory = self.collect_skill_inventory()
        by_agent: dict[str, list[dict[str, Any]]] = {}
        for record in inventory["skills"]:
            by_agent.setdefault(str(record.get("agent")), []).append(record)
        for agent, records in list(by_agent.items()):
            previous_path = self.agent_state_dir(agent) / "skills.json"
            previous_records: list[dict[str, Any]] = []
            if previous_path.exists():
                try:
                    previous_payload = json.loads(previous_path.read_text(encoding="utf-8"))
                    previous_records = list(previous_payload.get("skills", []))
                except (json.JSONDecodeError, OSError, TypeError):
                    previous_records = []
            by_agent[agent] = route_skill_records(agent, records, previous_records)
        inventory["skills"] = [
            record
            for agent in sorted(by_agent)
            for record in by_agent[agent]
        ]
        self.write_json_atomic(self.vault_path / SHARED_AGENT_SKILLS_JSON, inventory)
        for agent, records in by_agent.items():
            self.write_json_atomic(
                self.agent_state_dir(agent) / "skills.json",
                {
                    "_meta": {
                        "schema": "memory-sync-agent-skills",
                        "agent": agent,
                        "generated_at": inventory["_meta"]["generated_at"],
                        "record_count": len(records),
                    },
                    "skills": records,
                },
            )
            self.write_text_atomic(
                self.agent_state_dir(agent) / "skills.md",
                self.agent_skill_markdown(agent, records, inventory["_meta"]["generated_at"]),
            )

        for agent in sorted(by_agent):
            self.write_text_atomic(
                self.vault_path / agent_skill_markdown_rel(agent),
                self.agent_skill_markdown(agent, by_agent[agent], inventory["_meta"]["generated_at"]),
            )

        index_markdown = self.agent_skill_index_markdown(by_agent, inventory)
        self.write_text_atomic(self.vault_path / AGENT_SKILLS_MD_FILE, index_markdown)
        self.write_text_atomic(self.vault_path / REFERENCE_AGENT_SKILLS_MD_FILE, index_markdown)
        return inventory

    def preferred_language(self) -> str:
        explicit = os.environ.get("MEMORY_SYNC_LANGUAGE", "").strip().lower()
        if explicit in {"zh", "zh-cn", "chinese", "cn"}:
            return "zh"
        if explicit in {"en", "english"}:
            return "en"
        evidence = []
        for item in self.agent_knowledge_sources():
            evidence.append(self.read_optional_text(Path(item["path"]), limit=20000))
        evidence.append(self.read_optional_text(self.vault_path / PROFILE_MD_FILE, limit=20000))
        text = "\n".join(evidence)
        if contains_cjk(text):
            return "zh"
        return "en"

    def skill_description_for_language(self, record: dict[str, Any], language: str) -> str:
        description = str(record.get("description") or "").strip()
        if not description:
            return "无说明。" if language == "zh" else "No description provided."
        if language == "zh" and not contains_cjk(description):
            return f"原始说明：{description}"
        return description

    def group_skills_by_route_category(self, records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        fallback = SKILL_ROUTING_CATEGORIES[-1]["name"]
        for record in records:
            category = str(record.get("primary_category") or fallback)
            grouped.setdefault(category, []).append(record)
        for items in grouped.values():
            items.sort(key=lambda item: (str(item.get("routing_status")), str(item.get("name")), str(item.get("level")), str(item.get("relative_path"))))
        return grouped

    def skill_route_status_label(self, record: dict[str, Any], language: str) -> str:
        status = str(record.get("routing_status") or "needs_review")
        if language == "zh":
            return {
                "confirmed": "已确认",
                "pending_review": "新增待复核",
                "needs_review": "需要复核",
                "rule_suggested": "规则建议",
            }.get(status, status)
        return {
            "confirmed": "confirmed",
            "pending_review": "pending review",
            "needs_review": "needs review",
            "rule_suggested": "rule suggested",
        }.get(status, status)

    def skill_route_use_when_text(self, record: dict[str, Any], language: str) -> str:
        values = [str(value).strip() for value in record.get("use_when", []) if str(value).strip()]
        if values:
            return "；".join(values) if language == "zh" else "; ".join(values)
        return self.skill_description_for_language(record, language)

    def skill_route_avoid_when_text(self, record: dict[str, Any], language: str) -> str:
        values = [str(value).strip() for value in record.get("avoid_when", []) if str(value).strip()]
        if values:
            return "；".join(values) if language == "zh" else "; ".join(values)
        status = str(record.get("routing_status") or "")
        description = str(record.get("description") or "").strip()
        if language == "zh":
            if status == "pending_review":
                return "新增 Skill，边界和触发条件需读取完整 `SKILL.md` 后确认。"
            if not description or description == "|":
                return "描述不可用，禁止仅凭名称路由。"
            return "分类级排除规则适用；边界不清时读取完整 `SKILL.md`。"
        if status == "pending_review":
            return "New Skill; read the full `SKILL.md` before confirming boundaries."
        if not description or description == "|":
            return "Description unavailable; do not route by name alone."
        return "Use category-level exclusion rules; read the full `SKILL.md` when boundaries are unclear."

    def skill_full_list_lines(self, record: dict[str, Any], language: str) -> list[str]:
        if language == "zh":
            return [
                f"### {record.get('name')} · {record.get('level')} · {record.get('relative_path')}",
                "",
                f"- 功能简介：{self.skill_description_for_language(record, language)}",
                f"- 主要分类：{record.get('primary_category', '待复核')}",
                f"- 相关分类：{'、'.join(record.get('related_categories') or []) or '未声明'}",
                f"- 路由状态：{self.skill_route_status_label(record, language)}",
                f"- 来源层级：`{record.get('level')}`",
                f"- 相对路径：`{record.get('relative_path')}`",
                f"- 本机路径：`{record.get('path')}`",
                f"- 修改时间：{record.get('last_modified')}",
                f"- SHA256：`{record.get('sha256')}`",
                f"- 状态：{'启用' if record.get('enabled') else '禁用'}；frontmatter {'有效' if record.get('frontmatter_valid') else '可能缺失'}",
                "",
            ]
        return [
            f"### {record.get('name')} · {record.get('level')} · {record.get('relative_path')}",
            "",
            f"- Summary: {self.skill_description_for_language(record, language)}",
            f"- Primary category: {self.skill_category_label(record.get('primary_category'), language)}",
            f"- Related categories: {', '.join(self.skill_category_label(item, language) for item in (record.get('related_categories') or [])) or 'Not declared'}",
            f"- Routing status: {self.skill_route_status_label(record, language)}",
            f"- Level: `{record.get('level')}`",
            f"- Relative path: `{record.get('relative_path')}`",
            f"- Local path: `{record.get('path')}`",
            f"- Modified: {record.get('last_modified')}",
            f"- SHA256: `{record.get('sha256')}`",
            f"- State: {'enabled' if record.get('enabled') else 'disabled'}; frontmatter {'valid' if record.get('frontmatter_valid') else 'may be missing'}",
            "",
        ]

    def skill_category_label(self, category_name: Any, language: str) -> str:
        if language == "zh":
            return str(category_name or "待复核")
        for category in SKILL_ROUTING_CATEGORIES:
            if category["name"] == category_name:
                return str(category["name_en"])
        return "Needs Review"

    def skill_quality_issue_lines(self, records: list[dict[str, Any]], language: str) -> list[str]:
        counts = Counter(str(record.get("name")) for record in records)
        duplicates = sorted(name for name, count in counts.items() if count > 1)
        invalid = [record for record in records if not record.get("frontmatter_valid")]
        weak = [
            record
            for record in records
            if not str(record.get("description") or "").strip()
            or str(record.get("description") or "").strip() == "|"
            or str(record.get("description") or "").strip() == "No description provided."
        ]
        disabled = [record for record in records if not record.get("enabled")]
        pending = [record for record in records if record.get("routing_status") == "pending_review"]
        review = [record for record in records if record.get("routing_status") == "needs_review"]
        low_confidence = [record for record in records if float(record.get("routing_confidence") or 0) < 0.6]

        def items(values: list[dict[str, Any]]) -> str:
            if not values:
                return "无" if language == "zh" else "None"
            return ("、" if language == "zh" else ", ").join(
                f"{record.get('name')}（{record.get('level')}:{record.get('relative_path')}）" if language == "zh"
                else f"{record.get('name')} ({record.get('level')}:{record.get('relative_path')})"
                for record in values
            )

        if language == "zh":
            return [
                "## 质量问题",
                "",
                "> 本节只报告影响 Skill 路由可靠性的问题，不自动修改原 Skill。",
                "",
                f"- 同名 Skill：{'、'.join(duplicates) if duplicates else '无'}。必须使用 `level + relative_path` 区分。",
                f"- frontmatter 可能缺失：{items(invalid)}。",
                f"- description 无法用于路由：{items(weak)}。",
                f"- 已禁用 Skill：{items(disabled)}。",
                f"- 新增待复核 Skill：{items(pending)}。",
                f"- 需要复核 Skill：{items(review)}。",
                f"- 低置信度分类：{items(low_confidence)}。",
                "- 当前 description 在机器索引中可能被截断；遇到边界不清、适用条件冲突或排除条件缺失时，必须读取原始 `SKILL.md`。",
                "",
            ]
        return [
            "## Quality Issues",
            "",
            "> This section reports routing reliability issues only; it does not modify original Skills.",
            "",
            f"- Duplicate names: {', '.join(duplicates) if duplicates else 'None'}. Distinguish with `level + relative_path`.",
            f"- Frontmatter may be missing: {items(invalid)}.",
            f"- Description unusable for routing: {items(weak)}.",
            f"- Disabled Skills: {items(disabled)}.",
            f"- Pending review Skills: {items(pending)}.",
            f"- Needs review Skills: {items(review)}.",
            f"- Low-confidence categories: {items(low_confidence)}.",
            "- Descriptions in the machine index may be truncated; read the original `SKILL.md` when boundaries are unclear.",
            "",
        ]

    def agent_skill_index_markdown(self, by_agent: dict[str, list[dict[str, Any]]], inventory: dict[str, Any]) -> str:
        language = self.preferred_language()
        if language == "zh":
            lines = [
                "# Agent Skill 清单",
                "",
                "> 自动生成的 Obsidian 导航入口。详细 skill 清单按 agent 分开存储，这里只做导航。",
                "",
                f"- 生成时间：{inventory['_meta']['generated_at']}",
                f"- Skill 总数：{inventory['_meta']['record_count']}",
                f"- 机器索引：`{SHARED_AGENT_SKILLS_JSON}`",
                "",
                "## 按 Agent 查看",
                "",
            ]
            for agent in sorted(by_agent):
                lines.append(f"- [[{agent_skill_markdown_rel(agent)}|{agent} Skill 清单]] - {len(by_agent[agent])} 个")
            lines.extend(
                [
                    "",
                    "## 说明",
                    "",
                    f"- `{STATE_AGENTS_DIR}/<agent>/skills.json` 是每个 agent 的机器可读清单。",
                    "- `Personal/Agent Knowledge/<agent>/Agent Skills.md` 是给人看的个人知识库页面。",
                    f"- `{REFERENCE_AGENT_SKILLS_MD_FILE}` 是 Obsidian 公共入口。",
                    "",
                ]
            )
            return "\n".join(lines).rstrip() + "\n"

        lines = [
            "# Agent Skills",
            "",
            "> Auto-generated Obsidian entry. Detailed skill inventories are stored per agent; this page is navigation only.",
            "",
            f"- Generated: {inventory['_meta']['generated_at']}",
            f"- Skills: {inventory['_meta']['record_count']}",
            f"- Machine index: `{SHARED_AGENT_SKILLS_JSON}`",
            "",
            "## By Agent",
            "",
        ]
        for agent in sorted(by_agent):
            lines.append(f"- [[{agent_skill_markdown_rel(agent)}|{agent} skills]] - {len(by_agent[agent])}")
        lines.extend(
            [
                "",
                "## Notes",
                "",
                f"- `{STATE_AGENTS_DIR}/<agent>/skills.json` is the machine-readable per-agent inventory.",
                "- `Personal/Agent Knowledge/<agent>/Agent Skills.md` is the human-readable personal knowledge page.",
                f"- `{REFERENCE_AGENT_SKILLS_MD_FILE}` is the public Obsidian entry point.",
                "",
            ]
        )
        return "\n".join(lines).rstrip() + "\n"

    def agent_skill_markdown(self, agent: str, records: list[dict[str, Any]], generated_at: str) -> str:
        language = self.preferred_language()
        machine_index = f"{STATE_AGENTS_DIR}/{agent}/skills.json"
        if language == "zh":
            lines = [
                f"# {agent} Skill 路由索引",
                "",
                "> 自动生成的 Skill 匹配辅助索引。它帮助 Agent 缩小候选范围，但不替代各 Skill 自身的 `SKILL.md`；最终执行前必须读取被选中 Skill 的完整说明。",
                "",
                f"- 生成时间：{generated_at}",
                f"- Agent：{agent}",
                f"- Skill 数量：{len(records)}",
                f"- 机器索引：`{machine_index}`",
                "",
                "## 快速路由",
                "",
                "> 先判断任务所属大类，再进入唯一分类入口比较候选 Skill。不要从完整清单中仅凭名称直接选择。",
                "",
            ]
            grouped = self.group_skills_by_route_category(records)
            for category in SKILL_ROUTING_CATEGORIES:
                items = grouped.get(category["name"], [])
                if items:
                    lines.append(f"- [[#{category['name']}|{category['name']}]]：{category['intro'].split('。')[0]}。")
            lines.extend(["", "## 分类匹配指南", ""])
            for category in SKILL_ROUTING_CATEGORIES:
                items = grouped.get(category["name"], [])
                if not items:
                    continue
                lines.extend(
                    [
                        f"### {category['name']}",
                        "",
                        f"> 入口说明：{category['intro']}",
                        "",
                        f"优先级：{category['priority']}。",
                        "",
                        "候选 Skill：",
                        "",
                    ]
                )
                for record in items:
                    disabled = "" if record.get("enabled") else "，已禁用"
                    lines.extend(
                        [
                            f"- **{record.get('name')}**（`{record.get('level')}:{record.get('relative_path')}`{disabled}）",
                            f"  - 适用：{self.skill_route_use_when_text(record, language)}",
                            f"  - 排除：{self.skill_route_avoid_when_text(record, language)}",
                            f"  - 路由状态：{self.skill_route_status_label(record, language)}。",
                        ]
                    )
                lines.append("")
            lines.extend(
                [
                    "## 冲突处理规则",
                    "",
                    "1. 优先选择主要分类与当前任务完全一致的 Skill。",
                    "2. 同一分类内按“平台专用 > 语言、框架或格式专用 > 领域专用 > 通用能力”排序。",
                    "3. 同名 Skill 不按名称合并；使用 `level + relative_path` 区分，并优先读取当前 Agent 实际加载层级的版本。",
                    "4. 描述、路径或启用状态冲突时，以目标 Skill 的完整 `SKILL.md` 和 Agent 当前加载规则为准。",
                    "5. 只有任务确实跨越多个独立阶段时才组合多个 Skill；同一阶段不要同时调用能力重叠的通用 Skill。",
                    "6. `description` 缺失、为 `|`、被截断或 frontmatter 无效时，不允许自动确认路由，应进入质量问题等待复核。",
                    "7. 已确认且 `sha256` 未变化的路由信息应保留；新增 Skill 或哈希变化的 Skill 才需要 AI 重新检查。",
                    "",
                    "## 完整 Skill 清单",
                    "",
                    "> 以下清单用于审计和追溯。路由时先使用上面的分类入口；这里保留原始说明、来源层级和本机路径。",
                    "",
                ]
            )
            for record in records:
                lines.extend(self.skill_full_list_lines(record, language))
            lines.extend(self.skill_quality_issue_lines(records, language))
            return "\n".join(lines).rstrip() + "\n"

        lines = [
            f"# {agent} Skill Routing Index",
            "",
            "> Auto-generated Skill matching index. It helps agents narrow candidates, but it does not replace each Skill's own `SKILL.md`; read the selected Skill before execution.",
            "",
            f"- Generated: {generated_at}",
            f"- Agent: {agent}",
            f"- Skills: {len(records)}",
            f"- Machine index: `{machine_index}`",
            "",
            "## Quick Routing",
            "",
            "> Choose the task category first, then compare candidate Skills inside that single entry. Do not pick from the full list by name alone.",
            "",
        ]
        grouped = self.group_skills_by_route_category(records)
        for category in SKILL_ROUTING_CATEGORIES:
            items = grouped.get(category["name"], [])
            if items:
                lines.append(f"- [[#{category['name_en']}|{category['name_en']}]]: {category['intro_en'].split('.')[0]}.")
        lines.extend(["", "## Category Matching Guide", ""])
        for category in SKILL_ROUTING_CATEGORIES:
            items = grouped.get(category["name"], [])
            if not items:
                continue
            lines.extend(
                [
                    f"### {category['name_en']}",
                    "",
                    f"> Entry note: {category['intro_en']}",
                    "",
                    f"Priority: {category['priority_en']}.",
                    "",
                    "Candidate Skills:",
                    "",
                ]
            )
            for record in items:
                disabled = "" if record.get("enabled") else ", disabled"
                lines.extend(
                    [
                        f"- **{record.get('name')}** (`{record.get('level')}:{record.get('relative_path')}`{disabled})",
                        f"  - Use when: {self.skill_route_use_when_text(record, language)}",
                        f"  - Avoid when: {self.skill_route_avoid_when_text(record, language)}",
                        f"  - Routing status: {self.skill_route_status_label(record, language)}.",
                    ]
                )
            lines.append("")
        lines.extend(
            [
                "## Conflict Rules",
                "",
                "1. Prefer the Skill whose primary category exactly matches the task.",
                "2. Within a category, prefer platform-specific Skills, then language/framework/format-specific Skills, then domain-specific Skills, then generic Skills.",
                "3. Do not merge same-name Skills by name; distinguish them with `level + relative_path` and prefer the version actually loaded by the current agent.",
                "4. If description, path, or enabled state conflicts, trust the target Skill's full `SKILL.md` and the current agent's loading rules.",
                "5. Combine multiple Skills only when the task truly crosses independent phases.",
                "6. Missing, `|`, truncated, or invalid frontmatter descriptions require review before route confirmation.",
                "7. Keep confirmed routing when `sha256` is unchanged; newly added or changed Skills need agent review.",
                "",
                "## Complete Skill List",
                "",
                "> This list is for audit and traceability. Route from the category entries above first.",
                "",
            ]
        )
        for record in records:
            lines.extend(self.skill_full_list_lines(record, language))
        lines.extend(self.skill_quality_issue_lines(records, language))
        return "\n".join(lines).rstrip() + "\n"

    def sync_personal_knowledge_base(self) -> None:
        for item in self.agent_knowledge_sources():
            agent = str(item["agent"])
            source = Path(item["path"])
            if not source.exists() or not source.is_file():
                continue
            target = self.vault_path / PERSONAL_KNOWLEDGE_DIR / agent / self.agent_knowledge_target_name(item)
            body = source.read_text(encoding="utf-8", errors="replace")
            content = "\n".join(
                [
                    "---",
                    "type: agent_knowledge_source",
                    f"agent: {agent}",
                    f"source_label: {item.get('label', '')}",
                    f"source_path: {source.as_posix()}",
                    f"generated_at: {now_iso()}",
                    "---",
                    "",
                    f"# {agent} {source.name}",
                    "",
                    body.rstrip(),
                    "",
                ]
            )
            self.write_text_atomic(target, content)

    def shared_memory_records(self) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}
        for memory_id, memory in self.store.memories().items():
            if memory_is_shared(memory):
                result[memory_id] = self.agent_memory_record(memory_id, memory)
        return result

    def write_shared_layer(self, profile: dict[str, Any] | None = None, context: dict[str, Any] | None = None) -> None:
        shared_memories = self.shared_memory_records()
        self.write_json_atomic(
            self.vault_path / SHARED_MEMORY_INDEX,
            {
                "_meta": {
                    "schema": "memory-sync-shared-memory-index",
                    "generated_at": now_iso(),
                    "record_count": len(shared_memories),
                    "policy": "Only S3/S4, OpenClaw distilled, or effectively used memories enter the shared layer.",
                },
                "memories": shared_memories,
            },
        )
        if profile is not None:
            self.write_json_atomic(self.vault_path / SHARED_PROFILE_JSON, profile)
        if context is not None:
            self.write_json_atomic(self.vault_path / SHARED_CONTEXT_JSON, context)
            shared_context_dir = self.vault_path / SHARED_CONTEXT_DIR
            shared_context_dir.mkdir(parents=True, exist_ok=True)
            self.write_text_atomic(shared_context_dir / "agent_brief.md", self.adapter_markdown(context, "brief"))
            for adapter in ADAPTER_NAMES:
                self.write_text_atomic(shared_context_dir / f"{adapter}.md", self.adapter_markdown(context, adapter))

    def refresh_derived_outputs(self) -> None:
        self.ensure_index_storage_current()
        self.clean_unindexed_source_archives()
        self.write_agent_local_stores()
        self.sync_personal_knowledge_base()
        self.write_skill_inventory()
        profile = self.build_user_profile()
        self.save_user_profile(profile)
        context = self.build_agent_context(profile)
        if CONFIG["LEGACY_CONTEXT_ENABLED"]:
            self.write_agent_context("all", profile=profile, context=context)
        self.write_shared_layer(profile=profile, context=context)
        self.write_path_map()
        self.write_obsidian_surfaces(profile=profile, context=context)

    def persist_index_outputs(self, save_index: bool = True) -> None:
        if save_index or self.store.loaded_from_legacy_index:
            self.store.save()
        if CONFIG["DERIVED_OUTPUTS_ENABLED"]:
            self.refresh_derived_outputs()
        else:
            self.write_obsidian_index()

    def ensure_index_storage_current(self) -> None:
        if self.store.loaded_from_legacy_index:
            self.store.save()

    def git_run(self, args: list[str], check: bool = False) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(self.vault_path), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=check,
        )

    def run_in_dir(self, cwd: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            args,
            cwd=str(cwd),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def git_paths(self) -> list[str]:
        candidates = [
            f"{STATE_INDEX_DIR}/{INDEX_NAME}",
            f"{STATE_INDEX_DIR}/{PROFILE_NAME}",
            OBSIDIAN_INDEX_FILE,
            PROFILE_MD_FILE,
            MEMORY_DASHBOARD_FILE,
            MEMORY_PAGES_DIR,
            REFERENCE_AGENT_SKILLS_MD_FILE,
            VAULT_DAILY_DIR,
            PERMANENT_DIR,
            AGENTS_DIR,
            SHARED_DIR,
            SHARED_CONTEXT_DIR,
            PATH_MAP_FILE,
            PERSONAL_KNOWLEDGE_DIR,
        ]
        if CONFIG["LEGACY_CONTEXT_ENABLED"]:
            candidates.append(CONTEXT_DIR)
        return [path for path in candidates if (self.vault_path / path).exists()]

    def current_git_branch(self) -> str:
        configured = str(CONFIG["GIT_BRANCH"]).strip()
        if configured:
            return configured
        result = self.git_run(["branch", "--show-current"])
        return result.stdout.strip() or "main"

    def cmd_git_sync(self) -> int:
        probe = self.git_run(["rev-parse", "--is-inside-work-tree"])
        if probe.returncode != 0 or probe.stdout.strip() != "true":
            self.log(f"ERROR vault is not a git repository: {self.vault_path}")
            return 1

        paths = self.git_paths()
        if not paths:
            self.log("Git sync: no memory paths exist yet.")
            return 0

        add = self.git_run(["add", "--", *paths])
        if add.returncode != 0:
            self.log(add.stdout.strip())
            self.log(add.stderr.strip())
            return add.returncode
        staged = self.git_run(["diff", "--cached", "--quiet", "--", *paths])
        if staged.returncode == 0:
            self.log("Git sync: no staged memory changes.")
            return 0

        message = f"sync memory index {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        commit = self.git_run(["commit", "-m", message])
        if commit.returncode != 0:
            self.log(commit.stdout.strip())
            self.log(commit.stderr.strip())
            return commit.returncode

        self.log(commit.stdout.strip())
        if CONFIG["GIT_PUSH_ENABLED"]:
            push = self.git_run(["push", str(CONFIG["GIT_REMOTE"]), self.current_git_branch()])
            if push.returncode != 0:
                self.log(push.stdout.strip())
                self.log(push.stderr.strip())
                return push.returncode
            self.log(push.stdout.strip() or push.stderr.strip() or "Git push complete.")
        else:
            self.log("Git commit complete; push disabled by GIT_PUSH_ENABLED=false.")
        return 0

    def cmd_index_clean(self) -> int:
        removed: Counter[str] = Counter()
        kept = 0
        for memory_id, memory in list(self.store.memories().items()):
            reason = filter_reason(memory)
            if reason:
                removed[reason] += 1
                self.store.data.pop(memory_id, None)
                continue
            MemoryStore.refresh_keyword_profile(memory)
            kept += 1

        self.store.data[INDEX_META]["cleaned_at"] = now_iso()
        self.store.data[INDEX_META]["cleaned_removed"] = dict(removed)
        self.store.save()
        self.write_obsidian_index()
        self.log(f"Index clean complete: kept={kept}, removed={sum(removed.values())}")
        for reason, count in removed.most_common():
            self.log(f"  {reason}: {count}")
        return 0

    def cmd_status(self) -> int:
        memories = self.store.memories()
        counts = Counter(memory.get("stage", "S1") for memory in memories.values())
        self.log(f"Index: {self.store.index_path}")
        self.log(f"Memories: {len(memories)}")
        for stage in STAGES:
            self.log(f"  {stage}: {counts.get(stage, 0)}")
        processed = self.store.data.get(INDEX_META, {}).get("processed_files", {})
        self.log(f"Processed daily files: {len(processed)}")
        pack_path = self.review_pack_path()
        if pack_path.exists():
            try:
                pack = json.loads(pack_path.read_text(encoding="utf-8"))
                count = int(pack.get("_meta", {}).get("candidate_count", 0))
                self.log(f"Pending review pack: {self.vault_rel(pack_path)} candidates={count}")
            except (json.JSONDecodeError, ValueError, TypeError):
                self.log(f"Pending review pack: {self.vault_rel(pack_path)} (invalid JSON)")

        now = datetime.now()
        expiring: list[tuple[datetime, str, dict[str, Any]]] = []
        for memory_id, memory in memories.items():
            expire_at = parse_time(memory.get("expire_at"))
            if expire_at and expire_at > now and expire_at - now <= timedelta(days=3):
                expiring.append((expire_at, memory_id, memory))
        if expiring:
            self.log("Expiring within 3 days:")
            for expire_at, memory_id, memory in sorted(expiring)[:10]:
                self.log(f"- {memory_id} {memory.get('title')} at {expire_at.isoformat()}")
        return 0

    def cmd_skills_sync(self) -> int:
        self.sync_personal_knowledge_base()
        inventory = self.write_skill_inventory()
        self.log(f"Skill inventory written: {SHARED_AGENT_SKILLS_JSON}")
        self.log(f"Skill index written: {REFERENCE_AGENT_SKILLS_MD_FILE}")
        self.log(f"Personal skill index written: {AGENT_SKILLS_MD_FILE}")
        self.log(f"Skills: {inventory['_meta']['record_count']}")
        return 0

    def profile_path(self) -> Path:
        return self.vault_path / STATE_INDEX_DIR / PROFILE_NAME

    def context_path(self, name: str) -> Path:
        return self.vault_path / CONTEXT_DIR / name

    def read_optional_text(self, path: Path, limit: int = 120000) -> str:
        if not path.exists() or not path.is_file():
            return ""
        return path.read_text(encoding="utf-8", errors="replace")[:limit]

    def agent_knowledge_sources(self) -> list[dict[str, Any]]:
        home = Path.home()
        sources: list[dict[str, Any]] = [
            {"agent": "openclaw", "label": "workspace", "path": self.openclaw_path / "MEMORY.md", "weight": 0.85},
            {"agent": "openclaw", "label": "workspace", "path": self.openclaw_path / "USER.md", "weight": 1.0},
            {"agent": "openclaw", "label": "workspace", "path": self.openclaw_path / "AGENTS.md", "weight": 0.9},
            {"agent": "openclaw", "label": "workspace", "path": self.openclaw_path / "TOOLS.md", "weight": 0.55},
            {"agent": "openclaw", "label": "workspace", "path": self.openclaw_path / "SOUL.md", "weight": 0.4},
            {"agent": "codex", "label": "user", "path": home / ".codex" / "AGENTS.md", "weight": 0.75},
            {"agent": "codex", "label": "user", "path": home / ".codex" / "config.toml", "weight": 0.5},
            {"agent": "codex", "label": "user", "path": home / ".codex" / "rules" / "default.rules", "weight": 0.55},
            {"agent": "claude", "label": "user", "path": home / ".claude" / "CLAUDE.md", "weight": 0.75},
            {"agent": "opencode", "label": "user", "path": home / ".config" / "opencode" / "AGENTS.md", "weight": 0.75},
            {"agent": "opencode", "label": "windows-user", "path": home / "AppData" / "Roaming" / "opencode" / "AGENTS.md", "weight": 0.75},
            {"agent": "hermes-agent", "label": "user", "path": home / ".hermes-agent" / "AGENTS.md", "weight": 0.65},
            {"agent": "hermes-agent", "label": "home", "path": self.hermes_home() / "SOUL.md", "weight": 0.45},
            {"agent": "hermes-agent", "label": "home", "path": self.hermes_home() / "config.yaml", "weight": 0.4},
            {"agent": "qoder", "label": "user", "path": home / ".qoder" / "AGENTS.md", "weight": 0.55},
        ]

        for raw in [item for item in os.environ.get("MEMORY_SYNC_PROJECT_ROOTS", "").split(os.pathsep) if item.strip()]:
            root = expand_path(raw)
            project = re.sub(r"[^A-Za-z0-9_.-]+", "-", root.name).strip("-") or "project"
            for agent, rel, weight in [
                ("codex", "AGENTS.md", 0.7),
                ("openclaw", "AGENTS.md", 0.7),
                ("opencode", "AGENTS.md", 0.7),
                ("qoder", "AGENTS.md", 0.55),
                ("claude", "CLAUDE.md", 0.7),
                ("claude", ".claude/CLAUDE.md", 0.7),
            ]:
                sources.append(
                    {
                        "agent": agent,
                        "label": f"project-{project}-{rel.replace('/', '-')}",
                        "path": root / rel,
                        "weight": weight,
                    }
                )

        for index, raw in enumerate([item for item in os.environ.get("MEMORY_SYNC_AGENT_KNOWLEDGE_FILES", "").split(os.pathsep) if item.strip()], start=1):
            sources.append({"agent": "custom", "label": f"extra-{index}", "path": expand_path(raw), "weight": 0.45})
        return sources

    def agent_knowledge_target_name(self, item: dict[str, Any]) -> str:
        path = Path(item["path"])
        label = str(item.get("label", "")).strip()
        if label in {"workspace", "user"}:
            return path.name
        safe = re.sub(r"[^A-Za-z0-9_.-]+", "-", label).strip("-") or "source"
        return f"{safe}-{path.name}"

    def collect_profile_sources(self) -> list[tuple[str, str, float]]:
        sources: list[tuple[str, str, float]] = []
        for item in self.agent_knowledge_sources():
            path = Path(item["path"])
            text = self.read_optional_text(path)
            if text:
                sources.append((f"{item['agent']}:{item['label']}:{path.name}", text, float(item["weight"])))

        skill_doc = ROOT / "SKILL.md"
        text = self.read_optional_text(skill_doc)
        if text:
            sources.append(("memory-sync:SKILL.md", text, 0.45))
        return sources

    def add_rule_signals(self, profile: dict[str, Any], source: str, text: str, base_weight: float) -> None:
        lowered = text.lower()
        rules = [
            ("communication_style", "direct_concise", ["直接", "简洁", "concise", "direct", "少说话", "别太啰嗦", "啰嗦"], "Prefer direct, concise answers."),
            ("communication_style", "code_first", ["代码", "code", "code-first", "代码优先"], "Prefer concrete code and executable steps over long prose."),
            ("communication_style", "fast_response", ["快速", "快响应", "fast", "response time"], "Respond quickly and keep momentum."),
            ("decision_style", "plan_before_large_changes", ["先计划", "计划再", "plan", "strategy", "中长任务"], "Plan before multi-step or risky implementation."),
            ("decision_style", "iterate_while_building", ["边做边调整", "iterate", "实践 > 理论", "practice"], "Iterate through working artifacts rather than staying theoretical."),
            ("risk_preference", "confirm_before_deletion", ["删除", "delete", "destructive", "confirm before deleting", "always confirm"], "Confirm before deleting or destructive operations."),
            ("risk_preference", "do_not_exfiltrate", ["private", "隐私", "exfiltrate", "nothing goes external", "外部"], "Treat private data and external actions carefully."),
            ("workflows", "git_versioned_memory", ["git", "github", "版本", "version", "push", "commit"], "Use Git/GitHub for versioned memory assets."),
            ("workflows", "obsidian_memory_surface", ["obsidian", "vault", "知识库"], "Use Obsidian as the readable memory surface."),
            ("workflows", "automation_testing_platform", ["autotestplatform", "自动化测试", "fastapi", "vue", "pytest"], "Automation testing platform is an important recurring project."),
            ("active_projects", "memory-sync", ["memory-sync", "openclaw memory", "agent context", "user_profile", "agent_context"], "Memory-sync is the current context portability project."),
            ("active_projects", "autotestplatform", ["autotestplatform", "自动化测试平台"], "AutoTestPlatform is a recurring implementation project."),
            ("tool_preferences", "powershell_python_js", ["powershell", "python", "javascript", "pytest"], "Comfortable with PowerShell, Python, JavaScript, and pytest workflows."),
            ("tool_preferences", "multi_agent_context", ["codex", "claude", "openclaw", "opencode", "hermes", "qoder"], "Needs low-cost switching across multiple agents."),
            ("prompt_preferences", "action_oriented", ["多做事", "主动", "proactive", "解决", "执行"], "Prefer action-oriented agents that inspect, implement, and verify."),
            ("do_not_assume", "avoid_unverified_summaries", ["总结不准", "证据", "evidence", "不要擅自"], "Keep profile claims tied to evidence and avoid unsupported summaries."),
        ]
        for category, label, terms, detail in rules:
            matched = [term for term in terms if term.lower() in lowered]
            if not matched:
                continue
            profile["signals"].setdefault(category, []).append(
                signal(category, label, base_weight, source, f"matched: {', '.join(matched[:4])}", detail)
            )

    def add_memory_signals(self, profile: dict[str, Any]) -> None:
        stage_weight = {"S1": 0.35, "S2": 0.55, "S3": 0.75, "S4": 0.95}
        for memory_id, memory in self.store.memories().items():
            stage = str(memory.get("stage", "S1"))
            weight = stage_weight.get(stage, 0.35)
            weight += min(0.2, int(memory.get("effective_hit_count", 0)) * 0.05)
            source = f"memory-index:{memory_id}"
            text = "\n".join(
                [
                    str(memory.get("title", "")),
                    str(memory.get("summary", "")),
                    str(memory.get("excerpt", "")),
                    " ".join(str(item) for item in memory.get("strong_keywords", [])),
                ]
            )
            self.add_rule_signals(profile, source, text, weight)
            for keyword in memory.get("strong_keywords", [])[:8]:
                token = str(keyword).strip()
                if not token or is_generic_keyword(token) or is_low_signal_profile_label(token):
                    continue
                label = canonical_glossary_label(token)
                if is_low_signal_profile_label(label):
                    continue
                profile["signals"].setdefault("domain_glossary", []).append(
                    signal("domain_glossary", label, weight, source, text, "Strong keyword from memory index.")
                )
            title = memory_project_label(memory)
            if title:
                profile["signals"].setdefault("active_projects", []).append(
                    signal("active_projects", title[:80], weight, source, text, f"Stage {stage} memory.")
                )

    def summarize_profile_signals(self, profile: dict[str, Any]) -> None:
        summary: dict[str, list[dict[str, Any]]] = {}
        for category, items in profile.get("signals", {}).items():
            bucket: dict[str, dict[str, Any]] = {}
            for item in items:
                label = str(item.get("label", "")).strip()
                if not label:
                    continue
                if category == "domain_glossary":
                    label = canonical_glossary_label(label)
                if category in {"domain_glossary", "active_projects"} and is_low_signal_profile_label(label):
                    continue
                current = bucket.setdefault(
                    label,
                    {
                        "label": label,
                        "score": 0.0,
                        "confidence": 0.0,
                        "evidence": [],
                        "detail": item.get("detail", ""),
                    },
                )
                weight = float(item.get("weight", 0))
                current["score"] += weight
                current["confidence"] = max(float(current["confidence"]), float(item.get("confidence", 0)))
                if len(current["evidence"]) < 4:
                    current["evidence"].append({"source": item.get("source"), "evidence": item.get("evidence")})
            summary[category] = sorted(
                bucket.values(),
                key=lambda value: (float(value.get("score", 0)), float(value.get("confidence", 0))),
                reverse=True,
            )[:12]
        profile["summary"] = summary
        profile["profile_brief"] = self.profile_brief_text(profile)

    def profile_brief_text(self, profile: dict[str, Any]) -> str:
        summary = profile.get("summary", {})
        prefs = [item["label"] for item in summary.get("communication_style", [])[:3]]
        projects = [item["label"] for item in summary.get("active_projects", [])[:3]]
        tools = [item["label"] for item in summary.get("tool_preferences", [])[:3]]
        lines = []
        if prefs:
            lines.append("Communication: " + ", ".join(prefs))
        if projects:
            lines.append("Active focus: " + "; ".join(projects))
        if tools:
            lines.append("Tool context: " + ", ".join(tools))
        lines.append("Use evidence-backed memory; keep OpenClaw source read-only and version Obsidian outputs.")
        return " ".join(lines)

    def build_user_profile(self) -> dict[str, Any]:
        profile: dict[str, Any] = {
            "_meta": {
                "schema": "memory-sync-user-profile",
                "version": 1,
                "generated_at": now_iso(),
                "vault": str(self.vault_path),
                "openclaw_workspace": str(self.openclaw_path),
            },
            "signals": {},
            "summary": {},
            "profile_brief": "",
        }
        for source, text, weight in self.collect_profile_sources():
            profile["signals"].setdefault("source_inventory", []).append(
                signal("source_inventory", source, weight, source, f"{len(text)} chars", "Profile source loaded.")
            )
            self.add_rule_signals(profile, source, text, weight)
        self.add_memory_signals(profile)
        self.summarize_profile_signals(profile)
        return profile

    def write_profile_markdown(self, profile: dict[str, Any]) -> None:
        path = self.vault_path / PROFILE_MD_FILE
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# User 画像",
            "",
            "> Auto-generated from USER.md, memory index, OpenClaw distilled signals, and local agent configuration. Keep claims evidence-backed.",
            "",
            f"- Generated: {profile['_meta']['generated_at']}",
            f"- Brief: {profile.get('profile_brief', '')}",
            "",
        ]
        for category, items in profile.get("summary", {}).items():
            lines.extend([f"## {category}", ""])
            if not items:
                lines.extend(["_none_", ""])
                continue
            for item in items[:8]:
                lines.append(f"- **{item['label']}** score={item['score']:.2f} confidence={item['confidence']:.2f}")
                evidence = item.get("evidence", [])
                if evidence:
                    lines.append(f"  - evidence: {evidence[0].get('source')} - {evidence[0].get('evidence')}")
            lines.append("")
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        os.replace(tmp, path)

    def save_user_profile(self, profile: dict[str, Any]) -> None:
        path = self.profile_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, path)
        self.write_profile_markdown(profile)

    def load_or_build_profile(self) -> dict[str, Any]:
        path = self.profile_path()
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        profile = self.build_user_profile()
        self.save_user_profile(profile)
        return profile

    def read_user_profile(self) -> dict[str, Any] | None:
        path = self.profile_path()
        if not path.exists():
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None
        return payload if isinstance(payload, dict) else None

    def cmd_profile_build(self) -> int:
        profile = self.build_user_profile()
        self.save_user_profile(profile)
        self.write_agent_local_stores()
        self.write_shared_layer(profile=profile)
        self.write_path_map()
        self.write_obsidian_surfaces(profile=profile)
        self.log(f"Profile written: {self.vault_rel(self.profile_path())}")
        self.log(f"Profile markdown: {PROFILE_MD_FILE}")
        self.log(profile.get("profile_brief", ""))
        return 0

    def cmd_profile_show(self) -> int:
        profile = self.read_user_profile()
        if profile is None:
            self.log(f"Profile not found or invalid: {self.vault_rel(self.profile_path())}")
            self.log("Run `python scripts/main.py profile build` to generate it.")
            return 1
        self.log(profile.get("profile_brief", ""))
        for category in ["communication_style", "decision_style", "workflows", "active_projects", "tool_preferences"]:
            items = profile.get("summary", {}).get(category, [])[:5]
            if not items:
                continue
            self.log(f"{category}:")
            for item in items:
                self.log(f"- {item['label']} score={item['score']:.2f}")
        return 0

    def memory_snapshot(self, limit: int = 8, shared_only: bool = True) -> list[dict[str, Any]]:
        stage_score = {"S4": 4, "S3": 3, "S2": 2, "S1": 1}
        rows = []
        for memory_id, memory in self.store.memories().items():
            if shared_only and not memory_is_shared(memory):
                continue
            rows.append(
                (
                    stage_score.get(str(memory.get("stage", "S1")), 1) + int(memory.get("effective_hit_count", 0)),
                    memory_id,
                    memory,
                )
            )
        rows.sort(key=lambda item: item[0], reverse=True)
        return [
            {
                "id": memory_id,
                "stage": memory.get("stage", "S1"),
                "title": memory_context_title(memory),
                "summary": memory.get("summary", ""),
                "keywords": memory.get("strong_keywords") or memory.get("keywords", [])[:6],
                "source": memory.get("source_file", ""),
                "source_anchor": memory.get("source_anchor", ""),
                "source_agent": self.memory_agent(memory),
                "original_context_file": memory.get("original_context_file") or memory.get("source_file", ""),
                "original_context_anchor": memory.get("original_context_anchor") or memory.get("source_anchor", ""),
                "candidate_origin": memory.get("candidate_origin"),
            }
            for _score, memory_id, memory in rows[:limit]
        ]

    def build_agent_context(self, profile: dict[str, Any]) -> dict[str, Any]:
        summary = profile.get("summary", {})
        skill_inventory_path = self.vault_path / SHARED_AGENT_SKILLS_JSON
        skill_count = 0
        if skill_inventory_path.exists():
            try:
                skill_count = int(json.loads(skill_inventory_path.read_text(encoding="utf-8")).get("_meta", {}).get("record_count", 0))
            except (json.JSONDecodeError, OSError, ValueError):
                skill_count = 0
        return {
            "_meta": {
                "schema": "memory-sync-agent-context",
                "version": 1,
                "generated_at": now_iso(),
            },
            "profile_brief": profile.get("profile_brief", ""),
            "communication_style": summary.get("communication_style", [])[:6],
            "decision_style": summary.get("decision_style", [])[:6],
            "risk_preference": summary.get("risk_preference", [])[:6],
            "workflows": summary.get("workflows", [])[:8],
            "active_projects": summary.get("active_projects", [])[:8],
            "domain_glossary": summary.get("domain_glossary", [])[:16],
            "tool_preferences": summary.get("tool_preferences", [])[:8],
            "prompt_preferences": summary.get("prompt_preferences", [])[:8],
            "do_not_assume": summary.get("do_not_assume", [])[:8],
            "memory_snapshot": self.memory_snapshot(shared_only=True),
            "instruction_contract": {
                "applies_to": ["openclaw"],
                "must_read": ["AGENTS.md", "USER.md", "MEMORY.md", "memory/today-and-yesterday"],
                "conflict_protocol": [
                    "If AGENTS.md/USER.md cannot be read, say so explicitly instead of pretending.",
                    "If user instructions conflict with system/developer safety rules, follow higher-priority rules and explain the conflict.",
                    "If a requested action conflicts with AGENTS.md safety rules, surface the conflict before acting.",
                    "Never delete OpenClaw source memory; memory-sync cleanup operates on Obsidian copies and derived outputs.",
                ],
            },
            "memory_retrieval_contract": {
                "trigger_words": TRIGGER_WORDS,
                "query_policy": "Use the user's actual keyword phrase, not the full transcript. Combine built-in memory/context search with memory-sync search when the agent has built-in memory.",
                "command_template": "python <memory-sync>/scripts/main.py search \"<keyword phrase>\"",
                "rule_entrypoints": {
                    **AGENT_RULE_ENTRYPOINTS,
                },
            },
            "skill_inventory": {
                "path": SHARED_AGENT_SKILLS_JSON,
                "markdown": REFERENCE_AGENT_SKILLS_MD_FILE,
                "personal_markdown": AGENT_SKILLS_MD_FILE,
                "record_count": skill_count,
            },
            "paths": {
                "memory_index": f"{STATE_INDEX_DIR}/{INDEX_NAME}",
                "user_profile": f"{STATE_INDEX_DIR}/{PROFILE_NAME}",
                "profile_markdown": PROFILE_MD_FILE,
                "daily_copies": VAULT_DAILY_DIR,
                "context_dir": SHARED_CONTEXT_DIR,
                "legacy_context_dir": CONTEXT_DIR if CONFIG["LEGACY_CONTEXT_ENABLED"] else None,
                "skill_inventory": SHARED_AGENT_SKILLS_JSON,
                "skill_inventory_markdown": REFERENCE_AGENT_SKILLS_MD_FILE,
                "personal_knowledge": PERSONAL_KNOWLEDGE_DIR,
            },
        }

    def adapter_markdown(self, context: dict[str, Any], adapter: str) -> str:
        title = {
            "codex": "Codex Context",
            "claude": "Claude Context",
            "openclaw": "OpenClaw Context",
            "opencode": "OpenCode Context",
            "hermes-agent": "Hermes Agent Handoff",
            "qoder": "Qoder Context",
            "brief": "Agent Brief",
        }.get(adapter, adapter)
        lines = [f"# {title}", "", f"Generated: {context['_meta']['generated_at']}", "", "## User Brief", "", context.get("profile_brief", ""), ""]
        retrieval = context.get("memory_retrieval_contract", {})
        entrypoints = retrieval.get("rule_entrypoints", {}).get(adapter, [])
        if adapter in ADAPTER_NAMES:
            lines.extend([
                "## Memory Retrieval Contract",
                "",
                f"- Install automatic memory-trigger rules in: {', '.join(entrypoints) if entrypoints else 'the agent persistent rule file'}.",
                "- Trigger words are activation signals; they do not make memory-sync run unless the agent rule explicitly calls it.",
                "- Search with the user's actual keyword phrase, not the full transcript.",
                "- If the agent has built-in memory/context search, combine it with memory-sync search before answering.",
                f"- Command template: `{retrieval.get('command_template', 'python <memory-sync>/scripts/main.py search \"<keyword phrase>\"')}`",
                "",
            ])
        if adapter == "hermes-agent":
            lines.extend([
                "## Operating Contract",
                "",
                "- Before acting, read the configured hermes-agent rule/system prompt, user profile, memory snapshot, and available handoff context.",
                "- If a required rule file or handoff context is missing or unreadable, report it explicitly.",
                "- If instructions conflict with safety rules or the configured agent contract, explain the conflict and follow the higher-priority rule.",
                "- Do not claim to have followed a local rule unless the rule source was actually read.",
                "",
                "## Handoff Protocol",
                "",
                "- Carry the user's stable preferences, active projects, and current memory snapshot between agents.",
                "- Preserve evidence references; do not invent profile facts.",
                "- Prefer concise task state, clear next actions, and source paths.",
                "- Treat external publishing, destructive cleanup, and GitHub push as explicit-action zones.",
                "",
            ])
        elif adapter == "codex":
            lines.extend(["## Codex Operating Notes", "", "- Inspect files first, implement surgically, verify with commands.", "- Keep OpenClaw source read-only; write Obsidian/Git outputs only.", ""])
        elif adapter == "claude":
            lines.extend(["## Claude Operating Notes", "", "- Use the structured profile as stable context, then reason through ambiguity before writing.", "- Keep responses concise and evidence-backed.", ""])
        elif adapter == "openclaw":
            lines.extend([
                "## Operating Contract",
                "",
                "- Before acting, read AGENTS.md, USER.md, MEMORY.md, and today's/yesterday's daily memory when available.",
                "- If a required rule file is missing or unreadable, report it explicitly.",
                "- If user instructions conflict with system/developer safety rules or AGENTS.md, surface the conflict before acting.",
                "- Never delete OpenClaw source memory; use Obsidian copies and derived outputs for memory-sync cleanup.",
                "",
                "## OpenClaw Operating Notes",
                "",
                "- This is a distilled user/context state for continuity.",
                "- Raw memory remains in OpenClaw; Obsidian index is the persistent projection.",
                "",
            ])
        elif adapter == "opencode":
            lines.extend(["## OpenCode Operating Notes", "", "- Optimize for direct implementation context and minimal prose.", "- Use paths and commands from the context package.", ""])
        elif adapter == "qoder":
            lines.extend(["## Qoder Operating Notes", "", "- Use this as a portable context handoff until Qoder local chat schema is verified.", "- Prefer explicit handoff summaries and evidence-backed source links.", ""])

        for key, heading in [
            ("communication_style", "Communication"),
            ("decision_style", "Decision Style"),
            ("risk_preference", "Risk Boundaries"),
            ("workflows", "Workflows"),
            ("tool_preferences", "Tools"),
            ("active_projects", "Active Projects"),
            ("domain_glossary", "Glossary"),
            ("do_not_assume", "Do Not Assume"),
        ]:
            items = context.get(key, [])
            if not items:
                continue
            lines.extend([f"## {heading}", ""])
            for item in items[:8]:
                evidence = item.get("evidence", [])
                ref = f" ({evidence[0].get('source')})" if evidence else ""
                lines.append(f"- {item.get('label')} [score={float(item.get('score', 0)):.2f}]{ref}")
            lines.append("")

        memories = context.get("memory_snapshot", [])
        if memories:
            lines.extend(["## Memory Snapshot", ""])
            for memory in memories:
                lines.append(f"- {memory.get('id')} [{memory.get('stage')}] {memory.get('title')}")
                if memory.get("summary"):
                    lines.append(f"  Summary: {compact_text(str(memory.get('summary')), 160)}")
                source = memory.get("original_context_file") or memory.get("source")
                anchor = memory.get("original_context_anchor") or memory.get("source_anchor")
                if source:
                    lines.append(f"  Source: [[{source}]]{f' {anchor}' if anchor else ''}")
            lines.append("")
        skills = context.get("skill_inventory", {})
        if skills:
            lines.extend(["## Installed Skills", ""])
            lines.append(f"- Inventory: [[{skills.get('markdown')}]]")
            lines.append(f"- JSON: `{skills.get('path')}`")
            lines.append(f"- Count: {skills.get('record_count', 0)}")
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    def write_agent_context(
        self,
        adapter: str = "all",
        profile: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
    ) -> list[str]:
        if not CONFIG["LEGACY_CONTEXT_ENABLED"]:
            return []
        if profile is None:
            profile = self.load_or_build_profile()
        if context is None:
            context = self.build_agent_context(profile)
        base = self.vault_path / CONTEXT_DIR
        base.mkdir(parents=True, exist_ok=True)
        json_path = self.vault_path / CONTEXT_JSON
        json_path.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")

        written = [self.vault_rel(json_path)]
        adapters = ADAPTER_NAMES if adapter == "all" else (adapter,)
        brief_path = base / "agent_brief.md"
        brief_path.write_text(self.adapter_markdown(context, "brief"), encoding="utf-8")
        written.append(self.vault_rel(brief_path))
        for name in adapters:
            if name not in ADAPTER_NAMES:
                raise ValueError(f"Unknown adapter: {name}")
            path = base / f"{name}.md"
            path.write_text(self.adapter_markdown(context, name), encoding="utf-8")
            written.append(self.vault_rel(path))
        return written

    def cmd_context_export(self, adapter: str = "all") -> int:
        self.ensure_index_storage_current()
        self.clean_unindexed_source_archives()
        profile = self.load_or_build_profile()
        context = self.build_agent_context(profile)
        written = self.write_agent_context(adapter, profile=profile, context=context)
        self.write_agent_local_stores()
        self.write_shared_layer(profile=profile, context=context)
        self.write_path_map()
        self.write_obsidian_surfaces(profile=profile, context=context)
        if adapter == "all":
            shared_written = [f"{SHARED_CONTEXT_DIR}/agent_brief.md"] + [f"{SHARED_CONTEXT_DIR}/{name}.md" for name in ADAPTER_NAMES]
        else:
            shared_written = [f"{SHARED_CONTEXT_DIR}/agent_brief.md", f"{SHARED_CONTEXT_DIR}/{adapter}.md"]
        self.log("Shared context files written:")
        for item in shared_written:
            self.log(f"- {item}")
        if written:
            self.log("Legacy _context files written:")
        for item in written:
            self.log(f"- {item}")
        return 0

    def read_ingest_input(self, args: list[str]) -> str:
        if not args:
            if sys.stdin.isatty():
                raise ValueError("ingest requires text, --stdin, --file <path>, or --project <path>")
            return sys.stdin.read()
        if args[0] == "--stdin":
            if len(args) != 1:
                raise ValueError("ingest --stdin takes no extra arguments")
            return sys.stdin.read()
        if args[0] == "--file":
            if len(args) != 2:
                raise ValueError("ingest --file requires exactly one path")
            path = Path(args[1]).expanduser()
            if not path.exists() or not path.is_file():
                raise ValueError(f"ingest file not found: {path}")
            return path.read_text(encoding="utf-8", errors="replace")
        if args[0] == "--project":
            if len(args) < 2:
                raise ValueError("ingest --project requires a path")
            path = expand_path(args[1])
            note = ""
            if len(args) > 2:
                if args[2] != "--note":
                    raise ValueError("ingest --project accepts only optional --note text")
                note = " ".join(args[3:])
            return self.project_handoff_text(path, note)
        return " ".join(args)

    def project_handoff_text(self, project_path: Path, note: str = "") -> str:
        if not project_path.exists() or not project_path.is_dir():
            raise ValueError(f"project path not found: {project_path}")
        interesting = [
            "SKILL.md",
            "README.md",
            ".env.example",
            "scripts/main.py",
            "config/filters.json",
            "config/keywords.json",
            "config/triggers.json",
        ]
        summaries = []
        for rel in interesting:
            path = project_path / rel
            if path.exists() and path.is_file():
                item = file_summary(path)
                summaries.append(
                    f"- {rel}: size={item['size']} lines={item['lines']} sha256={item['sha256']}"
                )
        command_probe = self.run_in_dir(project_path, [sys.executable, "scripts/main.py", "help"])
        commands = [
            line.strip()
            for line in command_probe.stdout.splitlines()
            if line.strip().startswith("python scripts/main.py")
        ]
        git_probe = self.run_in_dir(project_path, ["git", "status", "--short"])
        git_status = git_probe.stdout.strip() if git_probe.returncode == 0 else "not a git repository"
        lines = [
            f"project: {project_path.name}",
            f"path: {project_path}",
            f"captured_at: {now_iso()}",
            "decision: capture actual project state for multi-agent handoff instead of only chat summary.",
            "source: local project files, command surface, and git status.",
        ]
        if note:
            lines.append(f"note: {note}")
        lines.extend(["", "files:", *summaries])
        if commands:
            lines.extend(["", "commands:", *[f"- {command}" for command in commands]])
        lines.extend(["", "git_status:", git_status or "clean"])
        return "\n".join(lines).rstrip() + "\n"

    def codex_home(self) -> Path:
        return expand_path(str(CONFIG["CODEX_HOME"]))

    def claude_home(self) -> Path:
        return expand_path(str(CONFIG["CLAUDE_HOME"]))

    def hermes_home(self) -> Path:
        return expand_path(str(CONFIG["HERMES_HOME"]))

    def hermes_state_db(self) -> Path:
        configured = os.environ.get("HERMES_STATE_DB", "").strip()
        if configured:
            return expand_path(configured)
        return self.hermes_home() / "state.db"

    def qoder_home(self) -> Path:
        return expand_path(str(CONFIG["QODER_HOME"]))

    def opencode_command(self) -> str:
        return shutil.which("opencode") or shutil.which("opencode.cmd") or "opencode"

    def opencode_db_path(self) -> Path:
        configured = os.environ.get("OPENCODE_DB_PATH", "").strip()
        if configured:
            return expand_path(configured)
        try:
            result = subprocess.run(
                [self.opencode_command(), "db", "path"],
                cwd=str(ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            )
        except (OSError, subprocess.SubprocessError):
            result = None
        if result and result.stdout.strip():
            return expand_path(result.stdout.strip().splitlines()[0])
        return Path.home() / ".local" / "share" / "opencode" / "opencode.db"

    def codex_rollout_files(self) -> list[Path]:
        roots = [
            self.codex_home() / "sessions",
            self.codex_home() / "archived_sessions",
        ]
        files: dict[str, Path] = {}
        for root in roots:
            if not root.exists():
                continue
            for path in root.rglob("rollout-*.jsonl"):
                files[str(path.resolve()).lower()] = path
        return sorted(files.values())

    def claude_project_files(self) -> list[Path]:
        projects = self.claude_home() / "projects"
        if not projects.exists():
            return []
        return sorted(projects.rglob("*.jsonl"))

    def codex_text_from_content(self, content: Any) -> str:
        if isinstance(content, str):
            return content.strip()
        if not isinstance(content, list):
            return ""
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text") or item.get("input_text") or item.get("output_text")
                if isinstance(text, str) and text.strip():
                    parts.append(text.strip())
        return "\n\n".join(parts).strip()

    def codex_tool_arguments(self, raw: Any) -> dict[str, Any]:
        if isinstance(raw, dict):
            return raw
        if not isinstance(raw, str) or not raw.strip():
            return {}
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            return {"raw": raw}
        return parsed if isinstance(parsed, dict) else {"raw": parsed}

    def codex_tool_summary(self, name: str, arguments: dict[str, Any]) -> str:
        if name == "exec_command":
            cmd = compact_text(str(arguments.get("cmd", "")), 120)
            return f"exec_command: {cmd}" if cmd else "exec_command"
        if name == "apply_patch":
            return "apply_patch"
        return name

    def claude_text_from_content(self, content: Any) -> str:
        if isinstance(content, str):
            return content.strip()
        parts: list[str] = []
        if isinstance(content, list):
            for item in content:
                if isinstance(item, str) and item.strip():
                    parts.append(item.strip())
                elif isinstance(item, dict):
                    item_type = item.get("type")
                    if item_type == "text" and isinstance(item.get("text"), str):
                        parts.append(item["text"].strip())
                    elif item_type == "tool_result" and isinstance(item.get("content"), str):
                        parts.append(item["content"].strip())
        return "\n\n".join(part for part in parts if part).strip()

    def claude_tool_events(self, content: Any, base_event: dict[str, Any]) -> list[dict[str, Any]]:
        if not isinstance(content, list):
            return []
        events: list[dict[str, Any]] = []
        for item in content:
            if not isinstance(item, dict):
                continue
            item_type = item.get("type")
            if item_type == "tool_use":
                name = str(item.get("name") or "tool")
                arguments = item.get("input") if isinstance(item.get("input"), dict) else {}
                event = dict(base_event)
                event.update(
                    {
                        "kind": "tool_call",
                        "name": name,
                        "call_id": item.get("id"),
                        "summary": f"claude tool: {name}",
                        "arguments": arguments,
                    }
                )
                events.append(event)
            elif item_type == "tool_result":
                content_text = str(item.get("content") or "")
                if not content_text.strip():
                    continue
                event = dict(base_event)
                event.update(
                    {
                        "kind": "tool_output",
                        "call_id": item.get("tool_use_id"),
                        "output": content_text,
                    }
                )
                events.append(event)
        return events

    def read_codex_rollout(self, path: Path, target_date: str | None, all_dates: bool) -> dict[tuple[str, str], dict[str, Any]]:
        session_id = path.stem.replace("rollout-", "")
        meta: dict[str, Any] = {"source_file": path.as_posix()}
        groups: dict[tuple[str, str], dict[str, Any]] = {}

        def ensure_group(day: str) -> dict[str, Any]:
            key = (day, session_id)
            if key not in groups:
                groups[key] = {"date": day, "session_id": session_id, "meta": dict(meta), "events": []}
            groups[key]["meta"].update({k: v for k, v in meta.items() if v})
            return groups[key]

        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_no, line in enumerate(handle, start=1):
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                timestamp = parse_jsonl_time(str(obj.get("timestamp", "")))
                day = timestamp.date().isoformat() if timestamp else ""
                payload = obj.get("payload")
                if obj.get("type") == "session_meta" and isinstance(payload, dict):
                    session_id = str(payload.get("id") or session_id)
                    meta.update(
                        {
                            "session_id": session_id,
                            "created_at": payload.get("timestamp"),
                            "cwd": payload.get("cwd"),
                            "originator": payload.get("originator"),
                            "cli_version": payload.get("cli_version"),
                            "source": payload.get("source"),
                            "model": payload.get("model"),
                            "model_provider": payload.get("model_provider"),
                            "source_file": path.as_posix(),
                        }
                    )
                    continue
                if not isinstance(payload, dict) or not timestamp:
                    continue
                if not all_dates and day != target_date:
                    continue
                if all_dates and not day:
                    continue

                group = ensure_group(day)
                event = {
                    "time": timestamp.replace(microsecond=0).isoformat(),
                    "line": line_no,
                    "source_file": path.as_posix(),
                }

                if obj.get("type") != "response_item":
                    continue
                item_type = payload.get("type")
                if item_type == "message":
                    role = str(payload.get("role") or "")
                    if role not in {"user", "assistant"}:
                        continue
                    text = self.codex_text_from_content(payload.get("content"))
                    if not text:
                        continue
                    event.update({"kind": "message", "role": role, "text": text})
                    group["events"].append(event)
                elif item_type == "function_call":
                    name = str(payload.get("name") or "tool")
                    arguments = self.codex_tool_arguments(payload.get("arguments"))
                    event.update(
                        {
                            "kind": "tool_call",
                            "name": name,
                            "call_id": payload.get("call_id"),
                            "summary": self.codex_tool_summary(name, arguments),
                            "arguments": arguments,
                        }
                    )
                    group["events"].append(event)
                elif item_type == "function_call_output":
                    output = str(payload.get("output") or "")
                    if not output.strip():
                        continue
                    event.update(
                        {
                            "kind": "tool_output",
                            "call_id": payload.get("call_id"),
                            "output": output,
                        }
                    )
                    group["events"].append(event)
        return {key: value for key, value in groups.items() if value.get("events")}

    def read_claude_project(self, path: Path, target_date: str | None, all_dates: bool) -> dict[tuple[str, str], dict[str, Any]]:
        fallback_session = path.stem
        meta: dict[str, Any] = {"source_file": path.as_posix(), "originator": "Claude Code"}
        groups: dict[tuple[str, str], dict[str, Any]] = {}

        def ensure_group(day: str, session_id: str) -> dict[str, Any]:
            key = (day, session_id)
            if key not in groups:
                groups[key] = {"date": day, "session_id": session_id, "meta": dict(meta), "events": []}
            groups[key]["meta"].update({k: v for k, v in meta.items() if v})
            return groups[key]

        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_no, line in enumerate(handle, start=1):
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                timestamp = parse_jsonl_time(str(obj.get("timestamp", "")))
                if not timestamp:
                    continue
                day = timestamp.date().isoformat()
                if not all_dates and day != target_date:
                    continue
                session_id = str(obj.get("sessionId") or fallback_session)
                msg = obj.get("message")
                if not isinstance(msg, dict):
                    continue
                role = str(msg.get("role") or obj.get("type") or "")
                if role not in {"user", "assistant"}:
                    continue
                meta.update(
                    {
                        "session_id": session_id,
                        "cwd": obj.get("cwd"),
                        "entrypoint": obj.get("entrypoint"),
                        "cli_version": obj.get("version"),
                        "source_file": path.as_posix(),
                    }
                )
                group = ensure_group(day, session_id)
                base_event = {
                    "time": timestamp.replace(microsecond=0).isoformat(),
                    "line": line_no,
                    "source_file": path.as_posix(),
                }
                text = self.claude_text_from_content(msg.get("content"))
                if text:
                    event = dict(base_event)
                    event.update({"kind": "message", "role": role, "text": text})
                    group["events"].append(event)
                group["events"].extend(self.claude_tool_events(msg.get("content"), base_event))
        return {key: value for key, value in groups.items() if value.get("events")}

    def read_openclaw_session_corpus(self, path: Path, target_date: str | None, all_dates: bool) -> dict[tuple[str, str], dict[str, Any]]:
        day = path.stem
        if not all_dates and day != target_date:
            return {}
        session_id = f"session-corpus-{day}"
        conversation = {
            "date": day,
            "session_id": session_id,
            "meta": {"source_file": path.as_posix(), "originator": "OpenClaw session-corpus", "cwd": str(self.openclaw_path)},
            "events": [],
        }
        pattern = re.compile(r"^\[(?P<source>[^\]]+)\]\s+(?P<role>User|Assistant):\s*(?P<text>.*)")
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_no, raw in enumerate(handle, start=1):
                line = raw.strip()
                if not line:
                    continue
                match = pattern.match(line)
                if match:
                    role = "user" if match.group("role") == "User" else "assistant"
                    text = match.group("text").strip()
                    source = match.group("source")
                else:
                    role = "assistant"
                    text = line
                    source = path.as_posix()
                conversation["events"].append(
                    {
                        "kind": "message",
                        "role": role,
                        "text": text,
                        "time": day,
                        "line": line_no,
                        "source_file": source,
                    }
                )
        if not conversation["events"]:
            return {}
        return {(day, session_id): conversation}

    def read_hermes_state_db(self, path: Path, target_date: str | None, all_dates: bool) -> dict[tuple[str, str], dict[str, Any]]:
        conversations: dict[tuple[str, str], dict[str, Any]] = {}
        uri = f"file:{path.as_posix()}?mode=ro"
        try:
            connection = sqlite3.connect(uri, uri=True)
            connection.row_factory = sqlite3.Row
        except sqlite3.Error as exc:
            self.log(f"ERROR cannot open Hermes state DB: {path} ({exc})")
            return {}

        try:
            tables = {
                row["name"]
                for row in connection.execute("select name from sqlite_master where type='table'")
                if row["name"]
            }
            required = {"sessions", "messages"}
            if not required.issubset(tables):
                self.log(f"ERROR Hermes state DB missing required tables: {sorted(required - tables)}")
                return {}
            rows = connection.execute(
                """
                select
                    m.id as message_id,
                    m.session_id,
                    m.role,
                    m.content,
                    m.tool_call_id,
                    m.tool_calls,
                    m.tool_name,
                    m.timestamp,
                    m.finish_reason,
                    m.reasoning,
                    m.reasoning_content,
                    s.source,
                    s.model,
                    s.title,
                    s.started_at,
                    s.ended_at,
                    s.message_count,
                    s.tool_call_count
                from messages m
                left join sessions s on s.id = m.session_id
                order by m.timestamp, m.id
                """
            ).fetchall()
        except sqlite3.Error as exc:
            self.log(f"ERROR cannot read Hermes state DB: {path} ({exc})")
            return {}
        finally:
            connection.close()

        for row in rows:
            timestamp = parse_unix_timestamp(row["timestamp"])
            if not timestamp:
                continue
            day = timestamp.date().isoformat()
            if not all_dates and day != target_date:
                continue

            session_id = str(row["session_id"] or "hermes-session")
            key = (day, session_id)
            if key not in conversations:
                conversations[key] = {
                    "date": day,
                    "session_id": session_id,
                    "meta": {
                        "source_file": path.as_posix(),
                        "originator": "Hermes Agent state.db",
                        "cwd": "",
                        "source": row["source"] or "hermes",
                        "model": row["model"] or "",
                        "title": row["title"] or "",
                        "started_at": row["started_at"],
                        "ended_at": row["ended_at"],
                    },
                    "events": [],
                }

            base_event = {
                "time": timestamp.replace(microsecond=0).isoformat(),
                "line": row["message_id"],
                "source_file": path.as_posix(),
            }
            role = str(row["role"] or "").lower()
            content = str(row["content"] or "").strip()
            if role in {"user", "assistant", "system"} and content:
                if role == "system":
                    continue
                event = dict(base_event)
                event.update({"kind": "message", "role": role, "text": content})
                conversations[key]["events"].append(event)

            tool_name = str(row["tool_name"] or "").strip()
            tool_calls_raw = str(row["tool_calls"] or "").strip()
            if tool_name or tool_calls_raw:
                arguments: dict[str, Any] = {}
                if tool_calls_raw:
                    try:
                        parsed = json.loads(tool_calls_raw)
                    except json.JSONDecodeError:
                        parsed = tool_calls_raw
                    arguments = parsed if isinstance(parsed, dict) else {"raw": parsed}
                event = dict(base_event)
                event.update(
                    {
                        "kind": "tool_call",
                        "name": tool_name or "hermes_tool",
                        "call_id": row["tool_call_id"],
                        "summary": f"hermes tool: {tool_name or 'tool call'}",
                        "arguments": arguments,
                    }
                )
                conversations[key]["events"].append(event)

        return {key: value for key, value in conversations.items() if value.get("events")}

    def opencode_session_ids_from_cli(self) -> list[str]:
        try:
            result = subprocess.run(
                [self.opencode_command(), "session", "list", "--format", "json"],
                cwd=str(ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=60,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            self.log(f"OpenCode session list unavailable: {exc}")
            return []
        if not result.stdout.strip():
            if result.stderr.strip():
                self.log(f"OpenCode session list returned no JSON: {compact_text(result.stderr, 180)}")
            return []
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            self.log(f"OpenCode session list JSON parse failed: {exc}")
            return []
        if not isinstance(payload, list):
            return []
        ids: list[str] = []
        for item in payload:
            if isinstance(item, dict) and item.get("id"):
                ids.append(str(item["id"]))
        return ids

    def opencode_export_session(self, session_id: str) -> dict[str, Any] | None:
        try:
            result = subprocess.run(
                [self.opencode_command(), "export", session_id],
                cwd=str(ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=120,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            self.log(f"OpenCode export unavailable for {session_id}: {exc}")
            return None
        if not result.stdout.strip():
            self.log(f"OpenCode export returned no JSON for {session_id}: {compact_text(result.stderr, 180)}")
            return None
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            self.log(f"OpenCode export JSON parse failed for {session_id}: {exc}")
            return None
        return payload if isinstance(payload, dict) else None

    def opencode_event_time(self, *values: Any) -> datetime | None:
        for value in values:
            if isinstance(value, dict):
                value = value.get("created") or value.get("updated")
            timestamp = parse_unix_timestamp(value)
            if timestamp:
                return timestamp
        return None

    def opencode_part_text(self, part: dict[str, Any]) -> str:
        for key in ("text", "content", "message", "output"):
            value = part.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return ""

    def append_opencode_event(
        self,
        conversations: dict[tuple[str, str], dict[str, Any]],
        session_id: str,
        meta: dict[str, Any],
        timestamp: datetime,
        event: dict[str, Any],
        target_date: str | None,
        all_dates: bool,
    ) -> None:
        day = timestamp.date().isoformat()
        if not all_dates and day != target_date:
            return
        key = (day, session_id)
        if key not in conversations:
            conversations[key] = {"date": day, "session_id": session_id, "meta": dict(meta), "events": []}
        event["time"] = timestamp.replace(microsecond=0).isoformat()
        event["source_file"] = meta.get("source_file", "")
        conversations[key]["events"].append(event)

    def parse_opencode_export(
        self,
        payload: dict[str, Any],
        source: Path,
        target_date: str | None,
        all_dates: bool,
    ) -> dict[tuple[str, str], dict[str, Any]]:
        info = payload.get("info") if isinstance(payload.get("info"), dict) else {}
        session_id = str(info.get("id") or payload.get("id") or source.stem)
        session_time = self.opencode_event_time(info.get("time"))
        meta = {
            "source_file": source.as_posix(),
            "originator": "OpenCode export",
            "cwd": str(info.get("directory") or ""),
            "source": "opencode",
            "model": "",
            "title": str(info.get("title") or ""),
            "created_at": session_time.isoformat() if session_time else "",
            "version": str(info.get("version") or ""),
        }
        conversations: dict[tuple[str, str], dict[str, Any]] = {}
        messages = payload.get("messages", [])
        if not isinstance(messages, list):
            return {}
        for message in messages:
            if not isinstance(message, dict):
                continue
            message_info = message.get("info") if isinstance(message.get("info"), dict) else {}
            message_id = str(message_info.get("id") or message.get("id") or "")
            role = str(message_info.get("role") or message.get("role") or "").lower()
            timestamp = self.opencode_event_time(message_info.get("time"), session_time)
            if not timestamp:
                continue
            model = message_info.get("model")
            if isinstance(model, dict):
                provider = str(model.get("providerID") or model.get("provider") or "")
                model_id = str(model.get("modelID") or model.get("model") or "")
                meta["model"] = "/".join(part for part in (provider, model_id) if part)
            text_parts: list[str] = []
            parts = message.get("parts", [])
            if not isinstance(parts, list):
                parts = []
            for part in parts:
                if not isinstance(part, dict):
                    continue
                part_type = str(part.get("type") or "").lower()
                if part_type == "text":
                    text = self.opencode_part_text(part)
                    if text:
                        text_parts.append(text)
                elif part_type in {"tool", "tool_call", "tool-call"}:
                    name = str(part.get("tool") or part.get("name") or part.get("toolID") or "opencode_tool")
                    event = {
                        "kind": "tool_call",
                        "line": part.get("id") or message_id,
                        "name": name,
                        "call_id": part.get("id") or part.get("callID"),
                        "summary": f"opencode tool: {name}",
                        "arguments": part.get("input") if isinstance(part.get("input"), dict) else {},
                    }
                    self.append_opencode_event(conversations, session_id, meta, timestamp, event, target_date, all_dates)
                elif part_type in {"tool_result", "tool-result"}:
                    output = self.opencode_part_text(part)
                    if output:
                        event = {
                            "kind": "tool_output",
                            "line": part.get("id") or message_id,
                            "call_id": part.get("id") or part.get("callID"),
                            "output": output,
                        }
                        self.append_opencode_event(conversations, session_id, meta, timestamp, event, target_date, all_dates)
            if role in {"user", "assistant"} and text_parts:
                event = {
                    "kind": "message",
                    "role": role,
                    "line": message_id,
                    "text": "\n\n".join(text_parts).strip(),
                }
                self.append_opencode_event(conversations, session_id, meta, timestamp, event, target_date, all_dates)
        return {key: value for key, value in conversations.items() if value.get("events")}

    def read_opencode_sqlite(self, path: Path, target_date: str | None, all_dates: bool) -> dict[tuple[str, str], dict[str, Any]]:
        conversations: dict[tuple[str, str], dict[str, Any]] = {}
        uri = f"file:{path.as_posix()}?mode=ro"
        try:
            connection = sqlite3.connect(uri, uri=True)
            connection.row_factory = sqlite3.Row
        except sqlite3.Error as exc:
            self.log(f"ERROR cannot open OpenCode DB: {path} ({exc})")
            return {}
        try:
            tables = {
                row["name"]
                for row in connection.execute("select name from sqlite_master where type='table'")
                if row["name"]
            }
            required = {"session", "message", "part"}
            if not required.issubset(tables):
                self.log(f"ERROR OpenCode DB missing required tables: {sorted(required - tables)}")
                return {}
            rows = connection.execute(
                """
                select
                    s.id as session_id,
                    s.directory,
                    s.title,
                    s.version,
                    s.time_created as session_created,
                    s.time_updated as session_updated,
                    m.id as message_id,
                    m.time_created as message_created,
                    m.time_updated as message_updated,
                    m.data as message_data,
                    p.id as part_id,
                    p.time_created as part_created,
                    p.time_updated as part_updated,
                    p.data as part_data
                from session s
                join message m on m.session_id = s.id
                left join part p on p.message_id = m.id
                order by s.time_created, m.time_created, p.time_created, p.id
                """
            ).fetchall()
        except sqlite3.Error as exc:
            self.log(f"ERROR cannot read OpenCode DB: {path} ({exc})")
            return {}
        finally:
            connection.close()

        for row in rows:
            try:
                message_data = json.loads(row["message_data"] or "{}")
            except json.JSONDecodeError:
                message_data = {}
            try:
                part_data = json.loads(row["part_data"] or "{}")
            except json.JSONDecodeError:
                part_data = {}
            if not isinstance(message_data, dict):
                message_data = {}
            if not isinstance(part_data, dict):
                part_data = {}
            timestamp = self.opencode_event_time(row["part_created"], row["message_created"], row["session_created"])
            if not timestamp:
                continue
            session_id = str(row["session_id"] or "opencode-session")
            meta = {
                "source_file": path.as_posix(),
                "originator": "OpenCode SQLite",
                "cwd": str(row["directory"] or ""),
                "source": "opencode",
                "model": "",
                "title": str(row["title"] or ""),
                "version": str(row["version"] or ""),
            }
            model = message_data.get("model")
            if isinstance(model, dict):
                provider = str(model.get("providerID") or model.get("provider") or "")
                model_id = str(model.get("modelID") or model.get("model") or "")
                meta["model"] = "/".join(part for part in (provider, model_id) if part)
            role = str(message_data.get("role") or "").lower()
            part_type = str(part_data.get("type") or "").lower()
            if role in {"user", "assistant"} and (part_type == "text" or not part_type):
                text = self.opencode_part_text(part_data) or str(message_data.get("content") or "").strip()
                if text:
                    event = {
                        "kind": "message",
                        "role": role,
                        "line": row["part_id"] or row["message_id"],
                        "text": text,
                    }
                    self.append_opencode_event(conversations, session_id, meta, timestamp, event, target_date, all_dates)
            elif part_type in {"tool", "tool_call", "tool-call"}:
                name = str(part_data.get("tool") or part_data.get("name") or part_data.get("toolID") or "opencode_tool")
                event = {
                    "kind": "tool_call",
                    "line": row["part_id"] or row["message_id"],
                    "name": name,
                    "call_id": part_data.get("id") or row["part_id"],
                    "summary": f"opencode tool: {name}",
                    "arguments": part_data.get("input") if isinstance(part_data.get("input"), dict) else {},
                }
                self.append_opencode_event(conversations, session_id, meta, timestamp, event, target_date, all_dates)
        return {key: value for key, value in conversations.items() if value.get("events")}

    def read_hermes_export_jsonl(
        self,
        text: str,
        source: str,
        target_date: str | None,
        all_dates: bool,
    ) -> dict[tuple[str, str], dict[str, Any]]:
        conversations: dict[tuple[str, str], dict[str, Any]] = {}
        for line_no, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                session = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(session, dict):
                continue
            session_id = str(session.get("id") or f"hermes-export-{line_no}")
            meta = {
                "source_file": source,
                "originator": "Hermes sessions export",
                "cwd": str(session.get("cwd") or ""),
                "source": session.get("source") or "hermes",
                "model": session.get("model") or "",
                "title": session.get("title") or "",
                "started_at": session.get("started_at"),
                "ended_at": session.get("ended_at"),
            }
            messages = session.get("messages", [])
            if not isinstance(messages, list):
                continue
            for message in messages:
                if not isinstance(message, dict):
                    continue
                timestamp = parse_unix_timestamp(message.get("timestamp"))
                if not timestamp:
                    continue
                day = timestamp.date().isoformat()
                if not all_dates and day != target_date:
                    continue
                key = (day, session_id)
                if key not in conversations:
                    conversations[key] = {"date": day, "session_id": session_id, "meta": dict(meta), "events": []}
                role = str(message.get("role") or "").lower()
                content = str(message.get("content") or "").strip()
                base_event = {
                    "time": timestamp.replace(microsecond=0).isoformat(),
                    "line": message.get("id") or line_no,
                    "source_file": source,
                }
                if role in {"user", "assistant"} and content:
                    event = dict(base_event)
                    event.update({"kind": "message", "role": role, "text": content})
                    conversations[key]["events"].append(event)
                tool_name = str(message.get("tool_name") or "").strip()
                if tool_name or message.get("tool_calls"):
                    event = dict(base_event)
                    event.update(
                        {
                            "kind": "tool_call",
                            "name": tool_name or "hermes_tool",
                            "call_id": message.get("tool_call_id"),
                            "summary": f"hermes tool: {tool_name or 'tool call'}",
                            "arguments": message.get("tool_calls") or {},
                        }
                    )
                    conversations[key]["events"].append(event)
        return {key: value for key, value in conversations.items() if value.get("events")}

    def read_hermes_export_command(self, target_date: str | None, all_dates: bool) -> dict[tuple[str, str], dict[str, Any]]:
        try:
            result = subprocess.run(
                ["hermes", "sessions", "export", "-"],
                cwd=str(ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=120,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            self.log(f"Hermes sessions export unavailable: {exc}")
            return {}
        if not result.stdout.strip():
            if result.stderr.strip():
                self.log(f"Hermes sessions export returned no data: {compact_text(result.stderr, 180)}")
            return {}
        return self.read_hermes_export_jsonl(result.stdout, "hermes sessions export -", target_date, all_dates)

    def codex_conversation_markdown(self, conversation: dict[str, Any]) -> str:
        return self.agent_conversation_markdown("codex", conversation)

    def agent_conversation_markdown(self, agent: str, conversation: dict[str, Any]) -> str:
        meta = conversation.get("meta", {})
        events = conversation.get("events", [])
        labels = {"codex": "Codex", "claude": "Claude", "openclaw": "OpenClaw", "opencode": "OpenCode", "hermes-agent": "hermes-agent", "qoder": "Qoder"}
        label = labels.get(agent, agent)
        title = f"{label} Conversation {conversation.get('date')} {str(conversation.get('session_id', ''))[:12]}"
        lines = [
            f"# {title}",
            "",
            f"- Agent: {agent}",
            f"- Date: {conversation.get('date')}",
            f"- Session: `{conversation.get('session_id')}`",
            f"- Project: `{meta.get('cwd', '')}`",
            f"- Source: `{meta.get('source_file', '')}`",
            f"- Originator: {meta.get('originator') or ''}",
            f"- Model: {meta.get('model') or ''}",
            f"- CLI version: {meta.get('cli_version') or ''}",
            f"- Event count: {len(events)}",
            "",
            "## Timeline",
            "",
        ]
        for event in events:
            time = str(event.get("time", ""))
            line_no = event.get("line")
            if event.get("kind") == "message":
                role = "User" if event.get("role") == "user" else "Assistant"
                lines.extend(
                    [
                        f"### {time} {role}",
                        "",
                        truncate_text(str(event.get("text", "")), 12000),
                        "",
                        f"_Source line: {line_no}_",
                        "",
                    ]
                )
            elif event.get("kind") == "tool_call":
                summary = markdown_heading_text(event.get("summary"), "tool call")
                arguments = event.get("arguments") if isinstance(event.get("arguments"), dict) else {}
                lines.extend(
                    [
                        f"<details>",
                        f"<summary>{time} Tool call: {summary}</summary>",
                        "",
                        "````json",
                        truncate_text(json.dumps(arguments, ensure_ascii=False, indent=2), 4000),
                        "````",
                        "",
                        f"_Source line: {line_no}_",
                        "",
                        "</details>",
                        "",
                    ]
                )
            elif event.get("kind") == "tool_output":
                lines.extend(
                    [
                        f"<details>",
                        f"<summary>{time} Tool output</summary>",
                        "",
                        "````text",
                        truncate_text(str(event.get("output", "")), 4000),
                        "````",
                        "",
                        f"_Source line: {line_no}_",
                        "",
                        "</details>",
                        "",
                    ]
                )
        return "\n".join(lines).rstrip() + "\n"

    def agent_conversation_summary_markdown(self, agent: str, conversation: dict[str, Any]) -> str:
        meta = conversation.get("meta", {})
        events = conversation.get("events", [])
        labels = {"codex": "Codex", "claude": "Claude", "openclaw": "OpenClaw", "opencode": "OpenCode", "hermes-agent": "hermes-agent", "qoder": "Qoder"}
        label = labels.get(agent, agent)
        title = f"{label} Readable Transcript {conversation.get('date')} {str(conversation.get('session_id', ''))[:12]}"
        message_count = sum(1 for event in events if event.get("kind") == "message")
        tool_count = sum(1 for event in events if event.get("kind") == "tool_call")
        lines = [
            f"# {title}",
            "",
            f"- Agent: {agent}",
            f"- Date: {conversation.get('date')}",
            f"- Session: `{conversation.get('session_id')}`",
            f"- Project: `{meta.get('cwd', '')}`",
            f"- Source: `{meta.get('source_file', '')}`",
            f"- Messages: {message_count}",
            f"- Tool calls: {tool_count}",
            "",
            "## Conversation",
            "",
        ]
        tool_lines: list[str] = []
        for event in events:
            time = str(event.get("time", ""))
            line_no = event.get("line")
            if event.get("kind") == "message":
                role = "User" if event.get("role") == "user" else "Assistant"
                lines.extend(
                    [
                        f"### {time} {role}",
                        "",
                        truncate_text(str(event.get("text", "")), 6000),
                        "",
                        f"_Source line: {line_no}_",
                        "",
                    ]
                )
            elif event.get("kind") == "tool_call":
                summary = markdown_heading_text(event.get("summary"), "tool call")
                tool_lines.append(f"- {time} `{event.get('name', 'tool')}`: {summary} (source line {line_no})")
        if tool_lines:
            lines.extend(["## Tool Activity", "", *tool_lines[:200], ""])
            if len(tool_lines) > 200:
                lines.append(f"- ... {len(tool_lines) - 200} more tool calls")
                lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    def write_conversation_archive(
        self,
        agent: str,
        conversations: dict[tuple[str, str], dict[str, Any]],
        source_count: int,
    ) -> int:
        base = self.agent_dir(agent) / "conversations"
        state_base = self.agent_state_dir(agent) / "conversations"
        state_base.mkdir(parents=True, exist_ok=True)
        written: list[dict[str, Any]] = []
        for (day, session_id), conversation in sorted(conversations.items()):
            day_dir = base / day
            day_dir.mkdir(parents=True, exist_ok=True)
            path = day_dir / f"{session_id}.md"
            self.write_text_atomic(path, self.agent_conversation_markdown(agent, conversation))
            rel = self.vault_rel(path)
            summary_dir = self.agent_dir(agent) / "conversation-summaries" / day
            summary_dir.mkdir(parents=True, exist_ok=True)
            summary_path = summary_dir / f"{session_id}.md"
            self.write_text_atomic(summary_path, self.agent_conversation_summary_markdown(agent, conversation))
            summary_rel = self.vault_rel(summary_path)
            record = {
                "agent": agent,
                "date": day,
                "session_id": session_id,
                "path": rel,
                "summary_path": summary_rel,
                "source_file": conversation.get("meta", {}).get("source_file"),
                "event_count": len(conversation.get("events", [])),
                "generated_at": now_iso(),
            }
            written.append(record)
            self.log(f"Conversation archived: {rel} events={record['event_count']}")
            self.log(f"Readable transcript written: {summary_rel}")

        by_day: dict[str, list[dict[str, Any]]] = {}
        for record in written:
            by_day.setdefault(str(record["date"]), []).append(record)
        for day, records in by_day.items():
            self.write_json_atomic(
                state_base / day / "index.json",
                {
                    "_meta": {
                        "schema": "memory-sync-conversation-day-index",
                        "agent": agent,
                        "date": day,
                        "generated_at": now_iso(),
                    },
                    "conversations": records,
                },
            )
        all_records: list[dict[str, Any]] = []
        for index_path in sorted(state_base.glob("*/index.json")):
            try:
                payload = json.loads(index_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            records = payload.get("conversations", [])
            if isinstance(records, list):
                all_records.extend([item for item in records if isinstance(item, dict)])
        self.write_json_atomic(
            state_base / "index.json",
            {
                "_meta": {
                    "schema": "memory-sync-conversation-index",
                    "agent": agent,
                    "generated_at": now_iso(),
                    "record_count": len(all_records),
                },
                "conversations": all_records,
            },
        )
        self.log(f"{agent} conversation scan complete: files={source_count}, conversations={len(written)}")
        return 0

    def cmd_conversations_scan_codex(self, target_date: str | None = None, all_dates: bool = False) -> int:
        if not all_dates and not target_date:
            target_date = datetime.now().date().isoformat()
        files = self.codex_rollout_files()
        if not files:
            self.log(f"ERROR Codex rollout files not found under: {self.codex_home() / 'sessions'}")
            return 1

        conversations: dict[tuple[str, str], dict[str, Any]] = {}
        for path in files:
            for key, value in self.read_codex_rollout(path, target_date, all_dates).items():
                conversations[key] = value
        return self.write_conversation_archive("codex", conversations, len(files))

    def cmd_conversations_scan_claude(self, target_date: str | None = None, all_dates: bool = False) -> int:
        if not all_dates and not target_date:
            target_date = datetime.now().date().isoformat()
        files = self.claude_project_files()
        if not files:
            self.log(f"ERROR Claude conversation files not found under: {self.claude_home() / 'projects'}")
            return 1
        conversations: dict[tuple[str, str], dict[str, Any]] = {}
        for path in files:
            for key, value in self.read_claude_project(path, target_date, all_dates).items():
                conversations[key] = value
        return self.write_conversation_archive("claude", conversations, len(files))

    def cmd_conversations_scan_openclaw(self, target_date: str | None = None, all_dates: bool = False) -> int:
        if not all_dates and not target_date:
            target_date = datetime.now().date().isoformat()
        corpus_dir = self.openclaw_path / "memory" / ".dreams" / "session-corpus"
        if not corpus_dir.exists():
            self.log(f"ERROR OpenClaw session-corpus not found: {corpus_dir}")
            return 1
        files = sorted(corpus_dir.glob("*.txt"))
        conversations: dict[tuple[str, str], dict[str, Any]] = {}
        for path in files:
            for key, value in self.read_openclaw_session_corpus(path, target_date, all_dates).items():
                conversations[key] = value
        return self.write_conversation_archive("openclaw", conversations, len(files))

    def cmd_conversations_scan_hermes(self, target_date: str | None = None, all_dates: bool = False) -> int:
        if not all_dates and not target_date:
            target_date = datetime.now().date().isoformat()
        db = self.hermes_state_db()
        conversations: dict[tuple[str, str], dict[str, Any]] = {}
        source_count = 0
        if db.exists():
            conversations = self.read_hermes_state_db(db, target_date, all_dates)
            source_count = 1
        else:
            self.log(f"Hermes state DB not found, trying sessions export: {db}")
        if not conversations:
            exported = self.read_hermes_export_command(target_date, all_dates)
            if exported:
                conversations = exported
                source_count = max(source_count, 1)
        if not conversations and not db.exists():
            self.log(f"ERROR Hermes conversations not found via state DB or sessions export: {db}")
            return 1
        return self.write_conversation_archive("hermes-agent", conversations, source_count or 1)

    def cmd_conversations_scan_opencode(self, target_date: str | None = None, all_dates: bool = False) -> int:
        if not all_dates and not target_date:
            target_date = datetime.now().date().isoformat()
        conversations: dict[tuple[str, str], dict[str, Any]] = {}
        session_ids = self.opencode_session_ids_from_cli()
        export_failures = 0
        for session_id in session_ids:
            payload = self.opencode_export_session(session_id)
            if not payload:
                export_failures += 1
                continue
            for key, value in self.parse_opencode_export(
                payload,
                Path(f"opencode export {session_id}"),
                target_date,
                all_dates,
            ).items():
                conversations[key] = value
        db = self.opencode_db_path()
        if session_ids and db.exists():
            for key, value in self.read_opencode_sqlite(db, target_date, all_dates).items():
                conversations.setdefault(key, value)
        if not session_ids or (export_failures and not conversations):
            if not db.exists():
                self.log(f"ERROR OpenCode DB not found: {db}")
                return 1
            conversations = self.read_opencode_sqlite(db, target_date, all_dates)
            return self.write_conversation_archive("opencode", conversations, 1)
        return self.write_conversation_archive("opencode", conversations, len(session_ids) + (1 if db.exists() else 0))

    def cmd_conversations_probe(self, agent: str) -> int:
        if agent == "hermes-agent":
            db = self.hermes_state_db()
            self.log(f"Hermes state DB: {db} exists={db.exists()}")
            return 0
        if agent == "opencode":
            db = self.opencode_db_path()
            self.log(f"OpenCode DB: {db} exists={db.exists()}")
            self.log("OpenCode conversation scan uses `opencode export <session-id>` first, then read-only SQLite supplement/fallback.")
            return 0
        qoder_paths = [
            self.qoder_home(),
            expand_path("~/.qoder"),
            Path(os.environ.get("APPDATA", "")) / "Qoder" / "User" / "globalStorage" / "state.vscdb",
        ]
        self.log("Qoder conversation scan is not enabled by default because its local state.vscdb schema is not stable.")
        for path in qoder_paths:
            self.log(f"- probe: {path} exists={path.exists()}")
        return 0

    def cmd_conversations_scan(self, agent: str, target_date: str | None = None, all_dates: bool = False) -> int:
        if agent == "all":
            status = 0
            for name in ("codex", "claude", "openclaw", "hermes-agent", "opencode", "qoder"):
                result = self.cmd_conversations_scan(name, target_date=target_date, all_dates=all_dates)
                status = status or result
            return status
        if agent == "codex":
            return self.cmd_conversations_scan_codex(target_date=target_date, all_dates=all_dates)
        if agent == "claude":
            return self.cmd_conversations_scan_claude(target_date=target_date, all_dates=all_dates)
        if agent == "openclaw":
            return self.cmd_conversations_scan_openclaw(target_date=target_date, all_dates=all_dates)
        if agent == "hermes-agent":
            return self.cmd_conversations_scan_hermes(target_date=target_date, all_dates=all_dates)
        if agent == "opencode":
            return self.cmd_conversations_scan_opencode(target_date=target_date, all_dates=all_dates)
        if agent == "qoder":
            return self.cmd_conversations_probe(agent)
        self.log(f"ERROR conversation scan is not implemented for: {agent}")
        return 1

    def cmd_ingest(self, agent: str, text: str) -> int:
        if agent not in ADAPTER_NAMES:
            self.log(f"ERROR unknown agent: {agent}")
            return 1
        text = text.strip()
        if not text:
            self.log("ERROR ingest text is empty")
            return 1

        now = datetime.now()
        day = now.date().isoformat()
        base = self.agent_dir(agent)
        daily_dir = base / "handoffs"
        daily_dir.mkdir(parents=True, exist_ok=True)
        daily_path = daily_dir / f"{day}.md"
        summary = extract_summary(text, limit=360)
        header = f"## {now.replace(microsecond=0).isoformat()} {agent} ingest"
        prefix = "\n".join([header, "", "### Summary", "", summary, "", "### Original Context", ""])
        block = prefix + text.rstrip() + "\n\n"
        if daily_path.exists():
            old = daily_path.read_text(encoding="utf-8", errors="replace")
            daily_path.write_text(old.rstrip() + "\n\n" + block, encoding="utf-8")
            start_line = len(old.splitlines()) + 2
        else:
            daily_path.write_text(f"# {agent} daily {day}\n\n" + block, encoding="utf-8")
            start_line = 3

        rel = self.vault_rel(daily_path)
        original_start_line = start_line + len(prefix.splitlines())
        anchor = f"line {original_start_line}-{start_line + len(block.splitlines()) - 1}"
        title = title_from_ingest(text, agent)
        indexed_body = ingest_index_body(summary, rel, anchor)
        candidate = self.build_agent_ingest_memory(agent, title, indexed_body, rel, anchor)
        candidate["summary"] = summary
        candidate["excerpt"] = indexed_body
        reason = noise_reason_for_text(text)
        if reason:
            self.log(f"Stored agent daily only; not indexed reason={reason}: {rel}")
        else:
            memory_id, action = self.add_or_merge(candidate)
            self.store.save()
            self.log(f"Ingest indexed: {memory_id} [{candidate.get('stage')}] action={action} {title}")

        self.refresh_derived_outputs()
        self.log(f"Agent ingest stored: {rel}")
        return 0

    def cmd_candidates(self, agent: str | None = None) -> int:
        rows = []
        for memory_id, memory in self.store.memories().items():
            if agent and self.memory_agent(memory) != agent:
                continue
            if memory.get("candidate_origin") or memory.get("source_type") in {"agent_ingest", "openclaw_distilled"}:
                rows.append((memory_id, memory))
        rows.sort(key=lambda item: (str(item[1].get("source_agent", "")), str(item[1].get("stage", "")), item[0]))
        self.log(f"Candidate memories: {len(rows)}")
        for memory_id, memory in rows:
            self.log(
                f"- {memory_id} [{memory.get('stage')}] agent={self.memory_agent(memory)} "
                f"origin={memory.get('candidate_origin')} {memory.get('title')}"
            )
        return 0

    def cmd_handoff(self, agent: str) -> int:
        if agent not in ADAPTER_NAMES:
            self.log(f"ERROR unknown agent: {agent}")
            return 1
        profile = self.load_or_build_profile()
        context = self.build_agent_context(profile)
        if CONFIG["LEGACY_CONTEXT_ENABLED"]:
            self.write_agent_context(agent, profile=profile, context=context)
        self.write_shared_layer(profile=profile, context=context)
        self.write_path_map()
        self.write_obsidian_surfaces(profile=profile, context=context)
        text = self.adapter_markdown(context, agent)
        self.log(text)
        return 0

    def cmd_context_brief(self) -> int:
        profile = self.read_user_profile()
        if profile is None:
            self.log(f"Profile not found or invalid: {self.vault_rel(self.profile_path())}")
            self.log("Run `python scripts/main.py profile build` or `python scripts/main.py context export all`.")
            return 1
        context = self.build_agent_context(profile)
        text = self.adapter_markdown(context, "brief")
        self.log(text)
        return 0

    def cmd_context_doctor(self) -> int:
        profile = self.read_user_profile()
        if profile is None:
            profile = {
                "_meta": {"generated_at": None},
                "summary": {},
                "profile_brief": "",
            }
        context = self.build_agent_context(profile)
        issues = []
        if not self.profile_path().exists():
            issues.append("missing user_profile.json")
        elif not self.read_user_profile():
            issues.append("invalid user_profile.json")
        if CONFIG["LEGACY_CONTEXT_ENABLED"] and not (self.vault_path / CONTEXT_DIR).exists():
            issues.append("missing legacy _context directory")
        if not (self.vault_path / MEMORY_DASHBOARD_FILE).exists():
            issues.append("missing Obsidian memory dashboard")
        if not (self.vault_path / MEMORY_PAGES_DIR).exists():
            issues.append("missing Obsidian memory pages directory")
        if not (self.vault_path / AGENTS_DIR).exists():
            issues.append("missing Sources directory")
        if not (self.vault_path / SHARED_DIR).exists():
            issues.append("missing .memory-sync/shared directory")
        if not (self.vault_path / SHARED_CONTEXT_DIR).exists():
            issues.append("missing Context directory")
        else:
            for adapter in ADAPTER_NAMES:
                if not (self.vault_path / SHARED_CONTEXT_DIR / f"{adapter}.md").exists():
                    issues.append(f"missing shared context adapter: {adapter}")
        if not (self.vault_path / SHARED_AGENT_SKILLS_JSON).exists():
            issues.append("missing shared agent skill inventory")
        for rel in ("AGENTS.md", "USER.md"):
            if not (self.openclaw_path / rel).exists():
                issues.append(f"missing OpenClaw rule/profile source: {rel}")
        if not (self.vault_path / PERSONAL_KNOWLEDGE_DIR / "openclaw" / "MEMORY.md").exists():
            issues.append("missing Personal Agent Knowledge copy of OpenClaw MEMORY.md")
        existing_rule_agents = {
            str(item["agent"])
            for item in self.agent_knowledge_sources()
            if Path(item["path"]).exists() and Path(item["path"]).is_file()
        }
        for adapter in ADAPTER_NAMES:
            if adapter not in existing_rule_agents and self.agent_memories(adapter):
                issues.append(f"no persistent rule/profile source found for {adapter}; add one or configure MEMORY_SYNC_PROJECT_ROOTS/MEMORY_SYNC_AGENT_KNOWLEDGE_FILES")
        if len(profile.get("summary", {}).get("communication_style", [])) == 0:
            issues.append("communication_style has no signals")
        if len(profile.get("summary", {}).get("active_projects", [])) == 0:
            issues.append("active_projects has no signals")
        stale_at = parse_time(profile.get("_meta", {}).get("generated_at"))
        if stale_at and datetime.now() - stale_at > timedelta(days=7):
            issues.append("profile older than 7 days")
        noisy_glossary = [
            str(item.get("label"))
            for item in profile.get("summary", {}).get("domain_glossary", [])
            if is_low_signal_profile_label(str(item.get("label", "")))
        ]
        if noisy_glossary:
            issues.append("domain_glossary still has low-signal labels: " + ", ".join(noisy_glossary[:5]))
        s1_snapshot = [item.get("id") for item in context.get("memory_snapshot", []) if item.get("stage") == "S1"]
        if s1_snapshot:
            issues.append("shared context snapshot contains S1 memories: " + ", ".join(str(item) for item in s1_snapshot[:5]))
        if issues:
            self.log("Context doctor issues:")
            for issue in issues:
                self.log(f"- {issue}")
        else:
            self.log("Context doctor: OK")
        return 0

    def cmd_autopilot(self) -> int:
        self.log("Autopilot start")
        if self.review_mode() == "agent":
            return self.prepare_agent_review("autopilot")
        result = self.cmd_sync()
        if result != 0:
            return result
        status = self.cmd_status()
        if status != 0:
            return status
        if CONFIG["GIT_SYNC_ENABLED"]:
            return self.cmd_git_sync()
        self.log("Git sync skipped; set GIT_SYNC_ENABLED=true to include it in autopilot.")
        return 0


def usage() -> None:
    print("Memory Sync")
    print("")
    print("Usage:")
    print("  python scripts/main.py sync")
    print("  python scripts/main.py search <keyword>")
    print("  python scripts/main.py diagnose <text>")
    print("  python scripts/main.py ingest <agent> [--stdin|--file path|--project path|text]")
    print("  python scripts/main.py conversations scan [codex|claude|openclaw|opencode|hermes-agent|qoder|all] [--date YYYY-MM-DD|--all]")
    print("  python scripts/main.py review prepare")
    print("  python scripts/main.py review apply <decisions.json> [pack.json]")
    print("  python scripts/main.py handoff <agent>")
    print("  python scripts/main.py candidates [agent]")
    print("  python scripts/main.py trigger check <text>")
    print("  python scripts/main.py trigger hit <text>")
    print("  python scripts/main.py index clean")
    print("  python scripts/main.py profile build")
    print("  python scripts/main.py profile show")
    print(f"  python scripts/main.py context export [{CONTEXT_ADAPTER_LIST}]")
    print("  python scripts/main.py context brief")
    print("  python scripts/main.py context doctor")
    print("  python scripts/main.py skills sync")
    print("  python scripts/main.py git sync")
    print("  python scripts/main.py status")
    print("  python scripts/main.py autopilot")


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if not args or args[0] in {"help", "-h", "--help"}:
        usage()
        return 0

    command = args[0]
    try:
        app = MemorySync()
    except ValueError as exc:
        print(f"ERROR {exc}")
        return 1

    if command == "sync":
        if len(args) != 1:
            print("ERROR sync takes no extra arguments")
            return 1
        return app.cmd_sync()
    if command == "search":
        if len(args) < 2:
            print("ERROR search requires a keyword")
            return 1
        return app.cmd_search(" ".join(args[1:]))
    if command == "diagnose":
        if len(args) < 2:
            print("ERROR diagnose requires text")
            return 1
        return app.cmd_diagnose(" ".join(args[1:]))
    if command == "ingest":
        if len(args) < 2:
            print("ERROR ingest requires: <agent> [--stdin|--file path|text]")
            return 1
        agent = args[1]
        if agent not in ADAPTER_NAMES:
            print(f"ERROR unknown agent: {agent}")
            return 1
        try:
            text = app.read_ingest_input(args[2:])
        except ValueError as exc:
            print(f"ERROR {exc}")
            return 1
        return app.cmd_ingest(agent, text)
    if command == "conversations":
        if len(args) < 3 or args[1] != "scan":
            print(f"ERROR conversations requires: scan <{CONTEXT_ADAPTER_LIST}> [--date YYYY-MM-DD|--all]")
            return 1
        agent = args[2]
        if agent != "all" and agent not in ADAPTER_NAMES:
            print(f"ERROR unknown agent: {agent}")
            return 1
        target_date: str | None = None
        all_dates = False
        index = 3
        while index < len(args):
            if args[index] == "--all":
                all_dates = True
                index += 1
            elif args[index] == "--date":
                if index + 1 >= len(args):
                    print("ERROR --date requires YYYY-MM-DD")
                    return 1
                target_date = args[index + 1]
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", target_date):
                    print("ERROR --date must be YYYY-MM-DD")
                    return 1
                index += 2
            else:
                print(f"ERROR unknown conversations option: {args[index]}")
                return 1
        if all_dates and target_date:
            print("ERROR use either --date or --all, not both")
            return 1
        return app.cmd_conversations_scan(agent, target_date=target_date, all_dates=all_dates)
    if command == "review":
        if len(args) < 2 or args[1] not in {"prepare", "apply"}:
            print("ERROR review requires: prepare or apply <decisions.json> [pack.json]")
            return 1
        if args[1] == "prepare":
            if len(args) != 2:
                print("ERROR review prepare takes no extra arguments")
                return 1
            return app.cmd_review_prepare()
        if len(args) not in {3, 4}:
            print("ERROR review apply requires: <decisions.json> [pack.json]")
            return 1
        decisions_path = expand_path(args[2])
        pack_path = expand_path(args[3]) if len(args) == 4 else None
        return app.cmd_review_apply(decisions_path, pack_path)
    if command == "handoff":
        if len(args) != 2:
            print("ERROR handoff requires: <agent>")
            return 1
        return app.cmd_handoff(args[1])
    if command == "candidates":
        if len(args) > 2:
            print("ERROR candidates accepts at most one agent")
            return 1
        agent = args[1] if len(args) == 2 else None
        if agent is not None and agent not in ADAPTER_NAMES:
            print(f"ERROR unknown agent: {agent}")
            return 1
        return app.cmd_candidates(agent)
    if command == "trigger":
        if len(args) < 3 or args[1] not in {"check", "hit"}:
            print("ERROR trigger requires: check <text> or hit <text>")
            return 1
        text = " ".join(args[2:])
        if args[1] == "check":
            return app.cmd_trigger_check(text)
        return app.cmd_trigger_hit(text)
    if command == "git":
        if len(args) != 2 or args[1] != "sync":
            print("ERROR git requires: sync")
            return 1
        return app.cmd_git_sync()
    if command == "index":
        if len(args) != 2 or args[1] != "clean":
            print("ERROR index requires: clean")
            return 1
        return app.cmd_index_clean()
    if command == "profile":
        if len(args) != 2 or args[1] not in {"build", "show"}:
            print("ERROR profile requires: build or show")
            return 1
        if args[1] == "build":
            return app.cmd_profile_build()
        return app.cmd_profile_show()
    if command == "context":
        if len(args) < 2 or args[1] not in {"export", "brief", "doctor"}:
            print("ERROR context requires: export [adapter], brief, or doctor")
            return 1
        if args[1] == "export":
            adapter = args[2] if len(args) == 3 else "all"
            if adapter != "all" and adapter not in ADAPTER_NAMES:
                print(f"ERROR unknown adapter: {adapter}")
                return 1
            return app.cmd_context_export(adapter)
        if len(args) != 2:
            print(f"ERROR context {args[1]} takes no extra arguments")
            return 1
        if args[1] == "brief":
            return app.cmd_context_brief()
        return app.cmd_context_doctor()
    if command == "skills":
        if len(args) != 2 or args[1] != "sync":
            print("ERROR skills requires: sync")
            return 1
        return app.cmd_skills_sync()
    if command == "status":
        if len(args) != 1:
            print("ERROR status takes no extra arguments")
            return 1
        return app.cmd_status()
    if command == "autopilot":
        if len(args) != 1:
            print("ERROR autopilot takes no extra arguments")
            return 1
        return app.cmd_autopilot()

    print(f"ERROR unknown command: {command}")
    usage()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
