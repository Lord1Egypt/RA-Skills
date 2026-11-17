#!/usr/bin/env python3
"""Package a conversation handoff into a small zip for transfer."""

import argparse
import datetime
import zipfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot-dir", default="conversation-output")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    snapshot_dir = Path(args.snapshot_dir)
    snapshot = snapshot_dir / "conversation-snapshot.md"
    index = snapshot_dir / "routing-index.md"
    if not snapshot.exists():
        raise SystemExit("SNAPSHOT_NOT_FOUND")
    if not index.exists():
        raise SystemExit("ROUTING_INDEX_NOT_FOUND")

    if args.output:
        output = Path(args.output)
    else:
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        output = Path(f"skill-architect-handoff-{stamp}.zip")
    output.parent.mkdir(parents=True, exist_ok=True)

    files = [snapshot, index]
    skills_dir = snapshot_dir / "skills"
    if skills_dir.exists():
        files.extend(sorted(p for p in skills_dir.rglob("SKILL.md") if p.is_file()))
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "README.md",
            "# Skill Package\n\n"
            "- `conversation-snapshot.md`：对话快照\n"
            "- `routing-index.md`：话题路由\n"
            "- `skills/`：按话题拆分的技能包\n\n"
            "导入命令：\n\n"
            "```bash\n"
            "python3 scripts/import_conversation_handoff.py --source <zip> --dest imported-conversation-output --topic <问题>\n"
            "```\n",
        )
        for path in files:
            zf.write(path, path.relative_to(snapshot_dir).as_posix())

    print(f"output={output}")
    print(f"files={len(files) + 1}")
    print("EXPORT_CONVERSATION_HANDOFF_OK")


if __name__ == "__main__":
    main()
