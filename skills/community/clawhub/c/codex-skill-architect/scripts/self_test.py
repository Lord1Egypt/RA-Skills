#!/usr/bin/env python3
"""Self-contained smoke test for skill-architect scripts."""

import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
PYTHON = sys.executable


def run(*args, cwd):
    result = subprocess.run([PYTHON, *args], cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {args}\n{result.stdout}\n{result.stderr}")


def main():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        skill = root / "SKILL.md"
        skill.write_text(
            "# Test\n\n## Core\n- keep\n\n## Big\n- a\n- b\n\n## End\n- keep\n",
            encoding="utf-8",
        )

        run(
            str(SCRIPTS / "audit.py"),
            "--skill",
            str(skill),
            "--output",
            str(root / "audit.md"),
            cwd=root,
        )

        run(
            str(SCRIPTS / "extract.py"),
            "--skill",
            str(skill),
            "--markers",
            "## Big|## End",
            "--output",
            str(root / "extracted.md"),
            "--replace-marker",
            "## 已外移说明\n\n内容已外移。",
            cwd=root,
        )

        pack = root / "packs" / "example" / "SKILL.md"
        pack.parent.mkdir(parents=True, exist_ok=True)
        pack.write_text("# 《示例书》技能包\n\n## 1. 判断尺\n- 保持简洁。\n", encoding="utf-8")
        run(
            str(SCRIPTS / "build_index.py"),
            "--pack-dir",
            str(root / "packs"),
            "--index",
            str(root / "index.md"),
            "--root",
            str(root),
            cwd=root,
        )

        run(
            str(SCRIPTS / "validate.py"),
            "--skill",
            str(skill),
            "--index",
            str(root / "index.md"),
            "--root",
            str(root),
            cwd=root,
        )

        run(
            str(SCRIPTS / "backup.py"),
            "--skill",
            str(skill),
            "--backup",
            str(root / "backup" / "SKILL.md"),
            cwd=root,
        )
        run(
            str(SCRIPTS / "rollback.py"),
            "--skill",
            str(root / "restore" / "SKILL.md"),
            "--backup",
            str(root / "backup" / "SKILL.md"),
            cwd=root,
        )
        run(
            str(SCRIPTS / "backup.py"),
            "--skill",
            str(skill),
            "--backup",
            str(root / "backup-dir"),
            cwd=root,
        )
        run(
            str(SCRIPTS / "rollback.py"),
            "--skill",
            str(root / "restore-dir" / "SKILL.md"),
            "--backup",
            str(root / "backup-dir"),
            cwd=root,
        )

        generic = root / "generic.md"
        generic.write_text(
            "# Generic\n\n## Alpha\n- a\n\n## Beta\n- b\n\n## Tail\n- t\n",
            encoding="utf-8",
        )
        config = root / "slim-config.json"
        config.write_text(
            json.dumps(
                {
                    "sections": [
                        {
                            "start": "## Alpha",
                            "end": "## Beta",
                            "output": str(root / "packs" / "alpha" / "SKILL.md"),
                            "replace_marker": "## 已外移说明\n\n内容已外移。",
                        }
                    ]
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        run(
            str(SCRIPTS / "extract.py"),
            "--skill",
            str(generic),
            "--config",
            str(config),
            cwd=root,
        )
        run(
            str(SCRIPTS / "validate.py"),
            "--skill",
            str(generic),
            "--index",
            str(root / "index.md"),
            "--root",
            str(root),
            "--test-command",
            "python3 -c 'print(\"generic-ok\")'",
            cwd=root,
        )

        transcript = root / "conversation.md"
        transcript.write_text(
            "---\nconversation_scope: whole-dialog\n---\n\n# 对话\n\n用户：帮我分析项目延期原因\n\n结论：主要是需求变更和外部依赖延迟。\n\n助手：建议先做风险清单。\n",
            encoding="utf-8",
        )
        conversation_out = root / "conversation-output"
        run(
            str(SCRIPTS / "conversation_architect.py"),
            "--transcript",
            str(transcript),
            "--output-dir",
            str(conversation_out),
            "--skill-name",
            "conversation-test",
            cwd=root,
        )
        if not (conversation_out / "conversation-snapshot.md").exists():
            raise SystemExit("MISSING conversation snapshot")
        if not (conversation_out / "routing-index.md").exists():
            raise SystemExit("MISSING conversation routing index")
        snapshot_text = (conversation_out / "conversation-snapshot.md").read_text(encoding="utf-8")
        if "建议先做风险清单" not in snapshot_text:
            raise SystemExit("MISSING last assistant answer in snapshot")

        private = conversation_out / "private.txt"
        private.write_text("secret", encoding="utf-8")

        run(
            str(SCRIPTS / "find_conversation_handoff.py"),
            "--search-base",
            str(root),
            cwd=root,
        )
        run(
            str(SCRIPTS / "import_conversation_handoff.py"),
            "--search-base",
            str(root),
            "--topic",
            "对话",
            cwd=root,
        )
        handoff_zip = root / "handoff.zip"
        run(
            str(SCRIPTS / "export_conversation_handoff.py"),
            "--snapshot-dir",
            str(conversation_out),
            "--output",
            str(handoff_zip),
            cwd=root,
        )
        with zipfile.ZipFile(handoff_zip) as zf:
            exported_names = set(zf.namelist())
        if "private.txt" in exported_names:
            raise SystemExit("EXPORT_INCLUDED_PRIVATE_FILE")
        if "conversation-snapshot.md" not in exported_names or "routing-index.md" not in exported_names:
            raise SystemExit("EXPORT_MISSING_CORE_FILE")
        run(
            str(SCRIPTS / "import_conversation_handoff.py"),
            "--source",
            str(handoff_zip),
            "--dest",
            str(root / "imported-conversation-output"),
            "--topic",
            "对话",
            cwd=root,
        )

        evil_zip = root / "evil.zip"
        with zipfile.ZipFile(evil_zip, "w") as zf:
            zf.writestr("../escaped.txt", "bad")
        escaped = root / "escaped.txt"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "import_conversation_handoff.py"),
                "--source",
                str(evil_zip),
                "--dest",
                str(root / "unsafe-import"),
            ],
            cwd=root,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            raise SystemExit("UNSAFE_ZIP_ACCEPTED")
        if escaped.exists():
            raise SystemExit("ZIP_SLIP_WRITE_OUTSIDE_DEST")

        topic_transcript = root / "topic-only.md"
        topic_transcript.write_text(
            "---\nconversation_scope: topic\n---\n\n# 主 SKILL 任务\n\n用户：继续瘦身。\n",
            encoding="utf-8",
        )
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "conversation_architect.py"),
                "--transcript",
                str(topic_transcript),
                "--output-dir",
                str(root / "topic-output"),
                "--skill-name",
                "topic-test",
            ],
            cwd=root,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            raise SystemExit("EXPECTED FULL TRANSCRIPT SCOPE FAILURE")

        run(
            str(SCRIPTS / "check_privacy.py"),
            "--root",
            str(root),
            cwd=root,
        )

        print("SELF_TEST_OK")


if __name__ == "__main__":
    main()
