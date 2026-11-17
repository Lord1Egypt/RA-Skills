#!/usr/bin/env python3
"""Prepare a summarized long conversation for import into the current dialog."""

import argparse
import zipfile
from pathlib import Path

from find_conversation_handoff import candidates, last_answer_text


def safe_extract(source, dest):
    dest = dest.resolve()
    with zipfile.ZipFile(source) as zf:
        for member in zf.infolist():
            target = (dest / member.filename).resolve()
            if not target.is_relative_to(dest):
                raise SystemExit("UNSAFE_ZIP_PATH")
        zf.extractall(dest)


def print_import(snapshot, topic):
    index = snapshot.parent / "routing-index.md"
    print(f"snapshot={snapshot}")
    print(f"index={index}")
    print(f"last_answer={last_answer_text(snapshot)}")

    packs_dir = snapshot.parent / "skills"
    if packs_dir.exists():
        packs = sorted(packs_dir.rglob("SKILL.md"))
        print(f"packs={len(packs)}")
        if topic:
            matched = [p for p in packs if topic.lower() in str(p).lower()]
            if matched:
                print(f"matching_pack={matched[0]}")
            else:
                print("matching_pack=NOT_FOUND")
    else:
        print("packs=0")

    print("IMPORT_CURRENT_DIALOG_READY")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--search-base", default="")
    parser.add_argument("--source", default="")
    parser.add_argument("--dest", default="imported-conversation-output")
    parser.add_argument("--topic", default="")
    args = parser.parse_args()

    if args.source:
        source = Path(args.source)
        if not source.exists():
            raise SystemExit("SOURCE_NOT_FOUND")
        if source.suffix.lower() == ".zip":
            dest = Path(args.dest)
            dest.mkdir(parents=True, exist_ok=True)
            safe_extract(source, dest)
            snapshots = sorted(dest.rglob("conversation-snapshot.md"))
            if not snapshots:
                raise SystemExit("SOURCE_HAS_NO_SNAPSHOT")
            snapshot = snapshots[0]
        else:
            snapshot = source / "conversation-snapshot.md"
            if not snapshot.exists():
                raise SystemExit("SOURCE_HAS_NO_SNAPSHOT")
        print_import(snapshot, args.topic)
        return

    latest = candidates(args.search_base)
    if not latest:
        print("CONVERSATION_HANDOFF_NOT_FOUND")
        raise SystemExit(1)

    snapshot = latest[0]
    print_import(snapshot, args.topic)


if __name__ == "__main__":
    main()
