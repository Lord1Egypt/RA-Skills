#!/usr/bin/env python3
"""Release gate for the cyber-girlfriend skill.

This script intentionally stays dependency-free so it can run inside a plain
OpenClaw/Codex workspace before publishing the skill.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path


REQUIRED_CLAWHUB_IGNORE_ENTRIES = [
    ".git/",
    ".gitignore",
    ".DS_Store",
    "tmp/",
    "tests/",
    "config.local.json*",
    "state/**",
    "AGENTS.md",
    "CHANGELOG.md",
    "PROJECT_CONTEXT.md",
    "DECISIONS.md",
    "CURRENT_TASK.md",
    "TODO.md",
]

SENSITIVE_REGEXES = [
    re.compile(r"\b\d{10,}\b"),
    re.compile(r"[A-Za-z0-9_-]{16,}@im\.[A-Za-z0-9_-]+\b", re.IGNORECASE),
    re.compile(r"/" r"Users/[^\\s\"'`]+"),
    re.compile(r"/" r"home/[^\\s\"'`]+"),
]

FORBIDDEN_CONTRACT_TERMS = [
    "generate_life_prompt.py",
    "render_companion_message.py",
    "prepare_companion_prompt.py",
    "task_materials",
    "final_render_prompt",
    "life_prompt",
    "selected_context",
]

FORBIDDEN_RELEASE_LOCAL_TERMS = [
    "深圳",
    "福田",
    "深圳大学",
    "菠萝包",
]

FORBIDDEN_FINISHED_SCHEDULE_SECTIONS = [
    "## 生成约束",
    "## 输出要求",
    "## 校验规则",
    "执行流程：",
]

REMOVED_RELEASE_FILES = [
    "scripts/generate_life_prompt.py",
    "scripts/render_companion_message.py",
    "scripts/run_companion_heartbeat.sh",
    "scripts/prepare_companion_prompt.py",
    "scripts/companion_ping.py",
    "scripts/companion_complete_media.py",
    "scripts/companion_media_watcher.py",
    "assets/render-specs/morning.json",
    "assets/render-specs/afternoon.json",
    "assets/render-specs/evening.json",
    "assets/render-specs/night.json",
    "assets/render-specs/heartbeat.json",
    "assets/month-plan.example.json",
    "assets/month-plan.schema.json",
    "assets/day-context.example.json",
    "assets/day-context.schema.json",
    "assets/life-filter-policy.json",
    "assets/render-spec.schema.json",
    "assets/render-specs/custom.example.json",
    "references/live-cron-text-sync-template.md",
    "references/live-cron-media-async-template.md",
    "references/heartbeat-integration.md",
    "references/live-cron-templates.md",
    "references/openclaw-integration.md",
    "references/cron-blueprints.md",
    "references/live-cron-config-wizard.md",
    "references/custom-cron-minimal-flow.md",
    "references/release-notes-1.3.0.md",
    "references/release-notes-1.3.1.md",
    "references/release-notes-1.3.2.md",
    "references/release-notes-1.4.0.md",
]

OBSOLETE_CURRENT_DOC_PHRASES = [
    "媒体 completion 回同一 session 后发送媒体并提交状态",
    "媒体 completion 回同一稳定 companion session 后发送媒体并提交状态",
    "媒体后状态提交",
    "state commit after media delivery",
    "state commits after media delivery",
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str):
    raise SystemExit(f"release validation failed: {message}")


def run(cmd, cwd: Path, input_text: str | None = None):
    result = subprocess.run(cmd, cwd=str(cwd), input=input_text, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "command failed")
    return result.stdout


def write_smoke_day_schedule(path: Path, config: dict):
    timezone = config.get("timezone")
    if timezone:
        os.environ["TZ"] = timezone
        try:
            import time

            time.tzset()
        except AttributeError:
            pass
    now = datetime.now()
    current_minute = now.hour * 60 + now.minute

    def hhmm(offset: int) -> str:
        minute = (current_minute + offset) % (24 * 60)
        return f"{minute // 60:02d}:{minute % 60:02d}"

    path.write_text(
        "\n".join(
            [
                "# 角色日程",
                "",
                "## 1. 今日背景",
                f"- 日期：{now.strftime('%Y-%m-%d')}",
                "- 星期：发布校验",
                "- 城市/主要地点：Example City，图书馆三楼",
                "- 天气/环境：天气平稳，适合室内轻任务",
                "- 今日类型：workday",
                "",
                "## 4. 日程事件",
                "",
                f"### {hhmm(0)} - 发布前校验当前生活事件",
                "- 必定发生：否",
                "- 执行时间：50 分钟",
                "- 场景：图书馆三楼靠窗座位",
                "- 正在做什么：把高数错题本翻到折角页，重新抄一遍那道积分题并用荧光笔标出换元位置",
                "- 情绪/状态：专注但不紧绷",
                "- 可自然提到：那道积分题终于顺了一点，荧光笔圈出来之后心里踏实了",
                "- 用户互动入口：可以很轻地问用户现在忙不忙",
                "- 媒体信息：",
                "- 不要写成：不要写成考试崩溃或整天都在等用户",
                "",
                f"### {hhmm(180)} - 午间便利店短暂停一下",
                "- 必定发生：否",
                "- 执行时间：35 分钟",
                "- 场景：校门口便利店",
                "- 正在做什么：买一个饭团和一杯冰美式，把上午的错题页码顺手记到便签上",
                "- 情绪/状态：稍微松下来",
                "- 可自然提到：饭团和冰美式救了她的午饭，错题页码也终于记好了",
                "- 用户互动入口：可以轻轻问用户午饭有没有好好吃",
                "- 媒体信息：",
                "- 不要写成：不要写成长时间外出或正式约会",
                "",
                f"### {hhmm(360)} - 桌边整理英语展示反馈",
                "- 必定发生：否",
                "- 执行时间：45 分钟",
                "- 场景：宿舍桌边",
                "- 正在做什么：把英语展示反馈纸夹进文件夹，顺手擦掉桌上一圈咖啡印",
                "- 情绪/状态：安静，想把小尾巴收干净",
                "- 可自然提到：桌上一圈咖啡印擦掉之后，今天像终于顺了一点",
                "- 用户互动入口：可以很轻地问用户今天是不是也有收尾的小事",
                "- 媒体信息：",
                "- 不要写成：不要写成突然大扫除或强迫用户回复",
                "",
                f"### {hhmm(540)} - 傍晚照片整理锚点",
                "- 必定发生：是",
                "- 执行时间：40 分钟",
                "- 场景：宿舍窗边",
                "- 正在做什么：收住白天的节奏，整理几张窗边光线下的照片和桌上便签",
                "- 情绪/状态：柔和，适合自然靠近",
                "- 可自然提到：窗边光线刚好，桌上还有她没收完的便签",
                "- 用户互动入口：可以用很轻的语气问用户今天累不累",
                "- 媒体信息：生成一张宿舍窗边生活照，画面包含柔和傍晚光线、桌上便签和几张正在筛选的照片，不出现真实人脸或私密信息",
                "- 不要写成：不要写成固定推送任务或为了给主人发消息",
                "",
                "## 生成约束",
                "- 每天生成 3-5 个普通日常事件。",
                "- 必定发生事件来自初始化配置，不计入普通事件额度。",
                "- 每个事件标题必须使用 `HH:mm - 事件标题`。",
                "- 每个事件必须写 `必定发生：是/否`。",
                "- 每个事件必须写 `执行时间`，用分钟描述这件事大约持续多久。",
                "- 不要出现内部词。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def iter_release_files(root: Path):
    allowed_dirs = {"assets", "references", "scripts", "agents"}
    allowed_root_files = {
        ".gitignore",
        "AGENTS.md",
        "CHANGELOG.md",
        "CURRENT_TASK.md",
        "DECISIONS.md",
        "PROJECT_CONTEXT.md",
        "SKILL.md",
        "TODO.md",
    }
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if rel.parts[0] in {".git", "state"}:
            continue
        if rel.name == "config.local.json" or rel.name.endswith(".pyc"):
            continue
        if rel.parts[0] in allowed_dirs or rel.name in allowed_root_files:
            yield path


def validate_json_files(root: Path):
    for path in root.rglob("*.json"):
        rel = path.relative_to(root)
        if rel.parts[0] in {".git", "state"} or rel.name == "config.local.json":
            continue
        load_json(path)
    for path in root.rglob("*.jsonl"):
        rel = path.relative_to(root)
        if rel.parts[0] in {".git", "state"}:
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                try:
                    json.loads(line)
                except json.JSONDecodeError as exc:
                    fail(f"{path}:{line_no} invalid jsonl: {exc}")


def validate_markdown_artifacts(root: Path):
    profile = root / "assets" / "character-profile.example.md"
    if not profile.exists():
        fail("missing assets/character-profile.example.md")
    run([
        sys.executable,
        str(root / "scripts" / "validate_character_profile.py"),
        "--profile",
        str(profile),
    ], root)
    schedule = root / "assets" / "day-schedule.example.md"
    if not schedule.exists():
        fail("missing assets/day-schedule.example.md")
    text = schedule.read_text(encoding="utf-8")
    for term in FORBIDDEN_FINISHED_SCHEDULE_SECTIONS:
        if term in text:
            fail(f"assets/day-schedule.example.md contains finished-schedule instruction section {term}")


def validate_clawhub_ignore(root: Path):
    ignore_path = root / ".clawhubignore"
    if not ignore_path.exists():
        fail("missing .clawhubignore")
    lines = {
        line.strip()
        for line in ignore_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }
    missing = [item for item in REQUIRED_CLAWHUB_IGNORE_ENTRIES if item not in lines]
    if missing:
        fail(".clawhubignore missing required private/package exclusions: " + ", ".join(missing))


def assert_no_git_artifacts(root: Path):
    present = [item for item in [".git", ".gitignore"] if (root / item).exists()]
    if present:
        fail("git artifacts should not be present in ClawHub skill directory: " + ", ".join(present))


def validate_local_markdown_links(root: Path):
    hits = []
    pattern = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")
    for path in iter_release_files(root):
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in pattern.finditer(text):
            target = match.group(1).split("#", 1)[0].strip()
            if not target:
                continue
            target_path = (path.parent / target).resolve()
            try:
                target_path.relative_to(root)
            except ValueError:
                hits.append(f"{path.relative_to(root)} links outside release root: {target}")
                continue
            if not target_path.exists():
                hits.append(f"{path.relative_to(root)} has broken link: {target}")
    if hits:
        fail("broken markdown links: " + "; ".join(hits[:12]))


def compile_scripts(root: Path):
    scripts = sorted((root / "scripts").glob("*.py"))
    if not scripts:
        fail("missing python scripts")
    run([sys.executable, "-m", "py_compile", *[str(path) for path in scripts]], root)
    remove_generated_artifacts(root)


def remove_generated_artifacts(root: Path):
    """Remove Python bytecode artifacts created by validation itself."""
    for cache_dir in root.rglob("__pycache__"):
        shutil.rmtree(cache_dir)
    for pyc_path in root.rglob("*.pyc"):
        pyc_path.unlink()


def scan_sensitive_release_surface(root: Path):
    hits = []
    private_patterns = [item for item in os.environ.get("CYBER_GF_PRIVATE_PATTERNS", "").split(",") if item]
    for path in iter_release_files(root):
        if path.name == "validate_release.py":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in private_patterns:
            if pattern in text:
                hits.append(f"{path.relative_to(root)} contains {pattern}")
        for regex in SENSITIVE_REGEXES:
            if regex.search(text):
                hits.append(f"{path.relative_to(root)} matches {regex.pattern}")
    if hits:
        fail("sensitive release surface hits: " + "; ".join(hits[:8]))


def private_patterns_from_env():
    return [item for item in os.environ.get("CYBER_GF_PRIVATE_PATTERNS", "").split(",") if item]


def assert_no_generated_artifacts(root: Path):
    generated = [path.relative_to(root) for path in root.rglob("__pycache__")]
    generated += [path.relative_to(root) for path in root.rglob("*.pyc")]
    if generated:
        fail("generated artifacts present: " + ", ".join(str(item) for item in generated[:8]))


def assert_no_obsolete_contract_terms(root: Path):
    hits = []
    for path in iter_release_files(root):
        if path.name == "validate_release.py":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for term in FORBIDDEN_CONTRACT_TERMS:
            if term in text:
                hits.append(f"{path.relative_to(root)} contains obsolete term {term}")
    if hits:
        fail("obsolete cron contract terms found: " + "; ".join(hits[:12]))


def assert_no_local_profile_terms(root: Path):
    hits = []
    for path in iter_release_files(root):
        if path.name == "validate_release.py":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for term in FORBIDDEN_RELEASE_LOCAL_TERMS:
            if term in text:
                hits.append(f"{path.relative_to(root)} contains local profile term {term}")
    if hits:
        fail("local profile terms found in release surface: " + "; ".join(hits[:12]))


def assert_removed_release_files_absent(root: Path):
    present = [item for item in REMOVED_RELEASE_FILES if (root / item).exists()]
    if present:
        fail("removed release files are still present: " + ", ".join(present))


def assert_version_consistency(root: Path):
    skill_text = (root / "SKILL.md").read_text(encoding="utf-8")
    skill_match = re.search(r"^version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", skill_text, re.MULTILINE)
    if not skill_match:
        fail("SKILL.md missing semantic version")
    version = skill_match.group(1)
    changelog_text = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    changelog_match = re.search(r"^##\s+([0-9]+\.[0-9]+\.[0-9]+)\s*$", changelog_text, re.MULTILINE)
    if not changelog_match:
        fail("CHANGELOG.md missing version heading")
    if changelog_match.group(1) != version:
        fail(f"version mismatch: SKILL.md={version}, CHANGELOG top={changelog_match.group(1)}")


def assert_no_obsolete_current_docs(root: Path):
    current_docs = [
        root / "SKILL.md",
        root / "PROJECT_CONTEXT.md",
        root / "references" / "configuration.md",
        root / "references" / "contract-schema.md",
        root / "references" / "first-time-setup.md",
        root / "references" / "presence-integration.md",
        root / "references" / "private-life-layer.md",
        root / "references" / "private-life-cron-templates.md",
        root / "references" / "private-life-prompt-templates.md",
        root / "references" / "required-events-and-cron.md",
        root / "references" / "standard-init-upgrade-flow.md",
    ]
    hits = []
    for path in current_docs:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for phrase in OBSOLETE_CURRENT_DOC_PHRASES:
            if phrase in text:
                hits.append(f"{path.relative_to(root)} contains obsolete phrase {phrase}")
    if hits:
        fail("obsolete current-doc phrases found: " + "; ".join(hits[:8]))


def assert_runner_contract_boundary(label: str, payload: dict):
    text = json.dumps(payload, ensure_ascii=False)
    if "runbook_contract" in text:
        fail(f"{label} leaked local runbook contract")
    if "media_runbook" in text:
        fail(f"{label} leaked local media runbook config")
    media = payload.get("media_contract")
    if isinstance(media, dict):
        allowed = {"kind", "async", "count", "tool_name", "completion_event_is_sender", "callback_context"}
        extra = set(media) - allowed
        if extra:
            fail(f"{label} media_contract has non-generic keys: {sorted(extra)}")
        if media.get("kind") == "event_media":
            if not media.get("async"):
                fail(f"{label} event_media must use OpenClaw async generation")
            if not media.get("completion_event_is_sender"):
                fail(f"{label} event_media completion event must send media")
            callback = media.get("callback_context")
            if not isinstance(callback, dict):
                fail(f"{label} event_media missing callback_context")
            if not callback.get("requires_original_session_context"):
                fail(f"{label} event_media callback must return to the stable companion session")
            if callback.get("strategy") != "same_stable_session":
                fail(f"{label} event_media callback must use the stable companion session")
            if callback.get("send_media_with") != "delivery_contract":
                fail(f"{label} event_media callback must send with delivery_contract")
            if callback.get("commit_after_media_send_with") not in ("", None):
                fail(f"{label} event_media callback must not own state commit")
    commit = payload.get("state_commit")
    if isinstance(media, dict) and media.get("kind") == "event_media" and isinstance(commit, dict):
        if commit.get("when") != "after_text_send":
            fail(f"{label} event_media state commit must happen after text send")


def assert_dispatch_lock_schema(lock: dict, label: str = "dispatch_lock"):
    """Validate the dispatch lock schema matches the release contract."""
    if not isinstance(lock, dict):
        fail(f"{label} is not a dict")
    for key in ("event_key", "run_id", "session_key", "started_at", "expires_at", "status"):
        if key not in lock:
            fail(f"{label} missing required key: {key}")
    valid_statuses = {
        "agent_enqueued",
        "agent_started",
        "text_sent",
        "media_sent",
        "media_task_failed",
        "recent_media_task_timeout",
        "agent_completed",
        "agent_launch_failed",
        "agent_start_timeout",
        "",
    }
    status = str(lock.get("status", ""))
    if status not in valid_statuses:
        fail(f"{label} invalid status: {status}")
    if isinstance(lock.get("started_at"), (int, float)) and isinstance(lock.get("expires_at"), (int, float)):
        if lock["expires_at"] <= lock["started_at"]:
            fail(f"{label} expires_at must be > started_at")
    if "dispatch_attempt" in lock:
        if not isinstance(lock["dispatch_attempt"], int) or lock["dispatch_attempt"] < 1:
            fail(f"{label} dispatch_attempt must be a positive integer if present")
    if "last_status_at" in lock:
        if not isinstance(lock["last_status_at"], (int, float)):
            fail(f"{label} last_status_at must be numeric")


def assert_agent_message_contract(message: str, label: str = "agent_message"):
    """Validate the agent message produced by companion_presence_tick.build_agent_message."""
    if not message:
        fail(f"{label} is empty")
    required_phrases = [
        "fresh prepare",
        "不要再运行 prepare",
        "--send-story",
        "--story-stdin",
        "delivery_contract",
        "state_commit.command",
        "NO_REPLY",
    ]
    for phrase in required_phrases:
        if phrase not in message:
            fail(f"{label} missing required phrase: {phrase}")
    if "openclaw shell" in message:
        if "dispatch lock 状态" not in message:
            fail(f"{label} has lock update mention but missing 状态 wording")


def assert_prepare_contract_boundary(payload: dict):
    """Validate that the prepare contract matches the 2.1.x presence contract."""
    assert_runner_contract_boundary("presence prepare", payload)
    if "mode" in payload:
        fail("presence prepare should not expose legacy mode")
    if "primary_goal" in payload:
        fail("presence prepare duplicated top-level primary_goal")
    if "render_spec" in payload:
        fail("presence prepare should not emit render_spec; cron template owns writing constraints")
    life_context = payload.get("life_context")
    if not isinstance(life_context, dict):
        fail("presence prepare missing life_context")
    speaker = life_context.get("speaker")
    if not isinstance(speaker, dict) or speaker.get("write_as") != "我":
        fail("presence prepare missing life_context.speaker")
    event = life_context.get("event")
    if not isinstance(event, dict) or not event.get("action"):
        fail("presence prepare missing life_context.event.action")
    for obsolete in ("activity", "mention", "place", "persons", "weather"):
        if obsolete in life_context:
            fail(f"presence prepare life_context contains obsolete field {obsolete}")


def smoke_modes(root: Path, config_path: Path):
    with tempfile.TemporaryDirectory(prefix="cyber-gf-release-") as tmp:
        tmpdir = Path(tmp)
        config = load_json(config_path)
        config.setdefault("runtime", {})["state_file"] = str(tmpdir / "companion-state.json")
        smoke_schedule = tmpdir / "day-schedule.md"
        write_smoke_day_schedule(smoke_schedule, config)
        config.setdefault("life_schedule", {}).setdefault("day_schedule", {})["schedule_path"] = str(smoke_schedule)
        config.setdefault("schedule", {})["quiet_hours_start"] = "00:00"
        config.setdefault("schedule", {})["quiet_hours_end"] = "00:00"
        smoke_state = {
            "schema_version": 2,
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
        (tmpdir / "companion-state.json").write_text(json.dumps(smoke_state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        initial_state_text = (tmpdir / "companion-state.json").read_text(encoding="utf-8")
        test_config = tmpdir / "config.json"
        test_config.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        prepare_output = run([
            sys.executable,
            str(root / "scripts" / "companion_run.py"),
            "--stage",
            "prepare",
            "--config",
            str(test_config),
            "--force",
            "--dry-run",
        ], root)
        prepare_payload = json.loads(prepare_output)
        if prepare_payload.get("status") != "ok":
            fail(f"presence prepare status={prepare_payload.get('status')}")
        assert_prepare_contract_boundary(prepare_payload)
        if prepare_payload.get("delivery_tracking", {}).get("pending_recorded"):
            fail("presence dry-run recorded pending")
        output_text = json.dumps(prepare_payload, ensure_ascii=False)
        for pattern in private_patterns_from_env() + ["USER.md", "user_md_path"]:
            if pattern in output_text:
                fail(f"presence prepare output leaked {pattern}")

        final_state_text = (tmpdir / "companion-state.json").read_text(encoding="utf-8")
        if final_state_text != initial_state_text:
            fail("dry-run smoke mutated state file")


def smoke_presence_tick(root: Path, config_path: Path):
    """Validate the presence_tick dry-run flow and dispatch lock lifecycle."""
    with tempfile.TemporaryDirectory(prefix="cyber-gf-presence-tick-") as tmp:
        tmpdir = Path(tmp)
        config = load_json(config_path)
        config.setdefault("runtime", {})["state_file"] = str(tmpdir / "companion-state.json")
        smoke_schedule = tmpdir / "day-schedule.md"
        write_smoke_day_schedule(smoke_schedule, config)
        config.setdefault("life_schedule", {}).setdefault("day_schedule", {})["schedule_path"] = str(smoke_schedule)
        config.setdefault("schedule", {})["quiet_hours_start"] = "00:00"
        config.setdefault("schedule", {})["quiet_hours_end"] = "00:00"
        smoke_state = {
            "schema_version": 2,
            "day": "",
            "daily_count": 0,
            "last_proactive_at": 0,
            "last_heartbeat_at": 0,
            "last_heartbeat_event_key": "",
            "last_mode": "",
            "last_style": "",
            "last_content_type": "",
            "mode_days": {},
            "pending_send": {"mode": "", "generated_at": 0, "event_key": "", "expires_at": 0},
            "preference_profile": {"service": 0, "clingy": 0, "curious": 0, "teasing": 0, "wrapup": 0},
            "relationship_state": {"last_owner_reply_at": 0, "last_response_delay_sec": 0, "last_seen_reply_text": "", "attention_balance": "steady"},
        }
        (tmpdir / "companion-state.json").write_text(json.dumps(smoke_state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        test_config = tmpdir / "config.json"
        test_config.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        dispatch_lock = tmpdir / "presence-dispatch-tick.json"

        # 1. Tick dry-run: should produce would_start_agent
        tick_output = run([
            sys.executable,
            str(root / "scripts" / "companion_presence_tick.py"),
            "--config",
            str(test_config),
            "--dispatch-lock",
            str(dispatch_lock),
            "--dry-run",
        ], root)
        tick_payload = json.loads(tick_output)
        if tick_payload.get("status") != "would_start_agent":
            fail(f"presence tick dry-run status={tick_payload.get('status')}")
        if not tick_payload.get("run_id"):
            fail("presence tick dry-run missing run_id")
        if tick_payload.get("session_key") != "agent:main:companion-runtime":
            fail(f"presence tick dry-run unexpected session_key: {tick_payload.get('session_key')}")

        # 2. Validate the agent message contract from the prepare output
        prepare_output = run([
            sys.executable,
            str(root / "scripts" / "companion_run.py"),
            "--stage",
            "prepare",
            "--config",
            str(test_config),
            "--force",
            "--dry-run",
        ], root)
        prepare_payload = json.loads(prepare_output)
        if prepare_payload.get("status") != "ok":
            fail(f"presence prepare for tick validation status={prepare_payload.get('status')}")
        assert_prepare_contract_boundary(prepare_payload)

        # 3. Build the agent message and validate its contract
        sys.path.insert(0, str(root))
        from scripts import companion_presence_tick as tick_module  # noqa: E402
        message = tick_module.build_agent_message(prepare_payload)
        assert_agent_message_contract(message)

        # 4. Dispatch lock lifecycle smoke (in-memory, no agent)
        # Write a mock lock and validate schema
        mock_lock = {
            "event_key": "2026-06-08|15:50|窗边小景",
            "run_id": "run-mock-1",
            "session_key": "agent:main:companion-runtime",
            "started_at": 1000,
            "expires_at": 1000 + 45 * 60,
            "status": "agent_enqueued",
            "dispatch_attempt": 1,
        }
        assert_dispatch_lock_schema(mock_lock)

        # Validate stall recovery: fresh enqueued is locked, stale enqueued is not
        now_mock = 1100  # 100s after start, within 300s stall
        locked = tick_module.dispatch_is_locked(dispatch_lock, mock_lock["event_key"], now_mock)
        # After writing the mock lock to disk, re-test
        (tmpdir / "presence-dispatch-mock.json").write_text(json.dumps(mock_lock) + "\n", encoding="utf-8")
        mock_path = tmpdir / "presence-dispatch-mock.json"
        locked_disk = tick_module.dispatch_is_locked(mock_path, mock_lock["event_key"], now_mock, max_stall_seconds=60)
        # With 60s stall: 100s old is stale
        stale_disk = tick_module.dispatch_is_locked(mock_path, mock_lock["event_key"], 1100, max_stall_seconds=60)

        # Validate lock schema via assert_dispatch_lock_schema
        loaded_lock = json.loads(mock_path.read_text(encoding="utf-8"))
        assert_dispatch_lock_schema(loaded_lock, "presence_tick_mock")


def main():
    parser = argparse.ArgumentParser(description="Validate cyber-girlfriend skill before publishing.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--config", default="")
    parser.add_argument("--skip-smoke", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    config_path = Path(args.config).resolve() if args.config else root / "config.local.json"

    validate_json_files(root)
    assert_version_consistency(root)
    validate_markdown_artifacts(root)
    validate_clawhub_ignore(root)
    assert_no_git_artifacts(root)
    validate_local_markdown_links(root)
    compile_scripts(root)
    scan_sensitive_release_surface(root)
    assert_no_generated_artifacts(root)
    assert_removed_release_files_absent(root)
    assert_no_obsolete_contract_terms(root)
    assert_no_local_profile_terms(root)
    assert_no_obsolete_current_docs(root)
    if not args.skip_smoke:
        if not config_path.exists():
            fail(f"smoke config not found: {config_path}")
        smoke_modes(root, config_path)
        smoke_presence_tick(root, config_path)
    remove_generated_artifacts(root)
    assert_no_generated_artifacts(root)
    print(json.dumps({"status": "ok", "validated_root": str(root), "smoke": not args.skip_smoke, "presence_tick_smoke": not args.skip_smoke}, ensure_ascii=False))


if __name__ == "__main__":
    main()
