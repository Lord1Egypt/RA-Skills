#!/usr/bin/env python3
"""Build a synthetic 'three months old' Agent Home for s4 end-to-end tests.

The builder writes only generated fixture data.  It deliberately avoids real
user names, company names, project names, session bodies, and credentials.
The generated tree is created in a temporary directory by the tests; this
builder file is safe to include in the published package.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

SKILL_COUNT = 30
SESSION_COUNT = 100
OLD_SESSION_COUNT = 40

TRIGGER_WORDS = [
    "整理收件箱",
    "生成周报",
    "会议纪要",
    "合同校对",
    "排期检查",
    "发票归档",
    "需求梳理",
    "测试用例",
    "发布清单",
    "数据校对",
    "目录整理",
    "表格合并",
    "文档摘要",
    "邮件草稿",
    "行程规划",
    "预算复核",
    "物料盘点",
    "进度跟踪",
    "风险登记",
    "知识检索",
    "读书笔记",
    "术语统一",
    "链接检查",
    "图片命名",
    "备份核对",
    "版本对比",
    "日志排查",
    "接口联调",
    "季度复盘",
    "生成月报",
]

AMBIGUOUS_TRIGGER = "整理房间"


def _write(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")


def _write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _utime(path: Path, timestamp: float) -> None:
    os.utime(path, (timestamp, timestamp))


def build(root: Path, now: Optional[datetime] = None) -> Dict[str, Any]:
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    current = now or datetime.now(timezone.utc)
    old_ts = (current - timedelta(days=120)).timestamp()
    recent_ts = (current - timedelta(days=3)).timestamp()

    _write(
        root / "AGENTS.md",
        "# Synthetic Agent Home\n\n"
        "This is generated fixture data for Agent Slim regression tests.\n"
        "Read rules/index.md before changing anything.\n",
    )
    _write(
        root / "config.toml",
        "[plugins.'active-helper@fixture-market']\n"
        "enabled = true\n\n"
        "[plugins.'legacy-helper@fixture-market']\n"
        "enabled = false\n",
    )
    _write(
        root / "plugins/cache/fixture-market/active-helper/1.0.0/.mcp.json",
        json.dumps(
            {"mcpServers": {"fixture-tools": {"tools": {"lookup": {}, "summarize": {}}}}},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    )
    _write(
        root / "plugins/cache/fixture-market/active-helper/1.0.0/.app.json",
        json.dumps({"apps": {"fixture-app": {"enabled": True}}}, ensure_ascii=False, indent=2) + "\n",
    )
    _write(
        root / "plugins/cache/fixture-market/active-helper/1.0.0/skills/plugin-skill/SKILL.md",
        "---\n"
        "name: plugin-skill\n"
        "description: Synthetic enabled plugin skill used to prove plugin inventory.\n"
        "version: 1.0.0\n"
        "triggers: [插件能力]\n"
        "---\n\n"
        "# Plugin Skill\n\nUse the plugin lookup tool when the plugin trigger matches.\n",
    )

    memory_lines = [
        "# Synthetic Memory Summary\n",
        "\n",
        "This generated summary simulates an Agent used for three months. "
        "It contains no real user, project, company, or session content.\n",
    ]
    for index in range(3000):
        memory_lines.append(
            "- fixture-memory-{:04d}: generated record retained for aging-agent size checks.\n".format(index)
        )
    memory_text = "".join(memory_lines)
    _write(root / "memories/memory_summary.md", memory_text)

    resident = "# Resident Rule\n\nKeep synthetic fixture changes reversible.\n"
    _write(root / "rules/resident.md", resident)
    _write(root / "rules/duplicate-a.md", resident)
    _write(root / "rules/duplicate-b.md", resident)
    _write(
        root / "rules/conditional.md",
        "# Conditional Rule\n\nLoad this synthetic rule only for fixture regression.\n",
    )
    _write(
        root / "rules/index.md",
        "# Rule Index\n\n"
        "- [resident.md](resident.md)\n"
        "- [conditional.md](conditional.md)\n"
        "- [duplicate-a.md](duplicate-a.md)\n"
        "- [duplicate-b.md](duplicate-b.md)\n",
    )

    old_session = "sessions/2026/03/session-000.jsonl"
    for index in range(SESSION_COUNT):
        if index < OLD_SESSION_COUNT:
            month = "03"
            rel = "sessions/2026/{}/session-{:03d}.jsonl".format(month, index)
        else:
            month = "09"
            rel = "sessions/2026/{}/session-{:03d}.jsonl".format(month, index)
        path = root / rel
        _write(
            path,
            json.dumps(
                {
                    "fixtureSession": index,
                    "recordType": "synthetic-metadata-only",
                    "note": "Audit must not read this body.",
                },
                ensure_ascii=False,
            )
            + "\n",
        )
        _utime(path, old_ts if index < OLD_SESSION_COUNT else recent_ts)

    for index in range(3):
        rel = "archived_sessions/archive-{:03d}.jsonl.zst".format(index)
        path = root / rel
        _write_bytes(path, ("synthetic archived metadata {}\n".format(index)).encode("utf-8"))
        _utime(path, old_ts)

    backup_a = b"SYNTHETIC-BACKUP-PAYLOAD-v1\n" * 8
    _write_bytes(root / "backups/snapshot-a.zip", backup_a)
    _write_bytes(root / "backups/snapshot-b.zip", backup_a)
    _write_bytes(root / "backups/snapshot-c.zip", b"SYNTHETIC-BACKUP-PAYLOAD-v2\n" * 8)
    _utime(root / "backups/snapshot-a.zip", old_ts)
    _utime(root / "backups/snapshot-b.zip", old_ts + 10)
    _utime(root / "backups/snapshot-c.zip", old_ts + 20)

    _write(root / "log/codex.log", "synthetic log line; no request or response body\n" * 10)
    _write_bytes(root / "state.db", b"SYNTHETIC-DATABASE-METADATA-ONLY\n")

    for index, trigger in enumerate(TRIGGER_WORDS, 1):
        name = "skill-{:02d}".format(index)
        skill_dir = root / "skills" / name
        if index == 29:
            body_reference = "This skill intentionally has an unreferenced warm file for quarantine testing.\n"
        elif index == 28:
            body_reference = "Read [large](references/large.md) only for a synthetic large-file review.\n"
        else:
            body_reference = "Read [guide](references/guide.md) when the trigger matches.\n"
        _write(
            skill_dir / "SKILL.md",
            "---\n"
            "name: {name}\n"
            "description: Synthetic skill {index:02d} for the three-month aging fixture; trigger '{trigger}'.\n"
            "version: 1.0.0\n"
            "triggers: [{trigger}, 场景{index:02d}]\n"
            "---\n\n"
            "# {name}\n\n"
            "{body_reference}".format(
                name=name,
                index=index,
                trigger=trigger,
                body_reference=body_reference,
            ),
        )
        if index == 29:
            _write(skill_dir / "references/orphan.md", "# Orphan Reference\n\nSynthetic unreferenced warm content.\n")
        elif index == 28:
            _write(
                skill_dir / "references/large.md",
                "# Large Warm File\n\n" + ("synthetic on-demand line\n" * 1200),
            )
        else:
            _write(skill_dir / "references/guide.md", "# Guide\n\nSynthetic reference for {}.\n".format(name))

    _write(
        root / "skills/.usage.json",
        json.dumps(
            {
                "skill-01": {"lastUsedAt": "2026-09-01T00:00:00Z", "count": 12},
                "skill-30": {"lastUsedAt": "2026-10-01T00:00:00Z", "count": 4},
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    )

    return {
        "skillCount": SKILL_COUNT,
        "pluginSkillCount": 1,
        "sessionCount": SESSION_COUNT,
        "oldSessionCount": OLD_SESSION_COUNT,
        "memoryBytes": len(memory_text.encode("utf-8")),
        "triggerWords": list(TRIGGER_WORDS),
        "ambiguousTrigger": AMBIGUOUS_TRIGGER,
        "orphanFile": "skills/skill-29/references/orphan.md",
        "largeFile": "skills/skill-28/references/large.md",
        "oldSession": old_session,
        "backupDuplicates": ["backups/snapshot-a.zip", "backups/snapshot-b.zip"],
        "disabledPlugin": "legacy-helper@fixture-market",
        "activePlugin": "active-helper@fixture-market",
    }
