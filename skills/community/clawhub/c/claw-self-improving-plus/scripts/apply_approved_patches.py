#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


TARGETS = {"SOUL.md", "AGENTS.md", "TOOLS.md", "MEMORY.md"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def insert_after_anchor(text: str, anchor: str, entry: str):
    if anchor not in text:
        return None
    idx = text.index(anchor) + len(anchor)
    tail = text[idx:]
    insert_at = idx + 1 if tail.startswith("\n") else idx
    insertion = entry.rstrip() + "\n"
    return text[:insert_at] + insertion + text[insert_at:]


def append_entry(text: str, entry: str):
    if text and not text.endswith("\n"):
        text += "\n"
    return text + entry.rstrip() + "\n"


def validate_patch(patch: dict):
    target = patch.get("target_file")
    if target not in TARGETS:
        return f"target_file not allowed: {target}"
    if not patch.get("approved"):
        return "not approved"
    if not (patch.get("suggested_entry") or (patch.get("old_text") is not None and patch.get("new_text") is not None)):
        return "no applicable patch content"
    return None


def apply_patch(base_dir: Path, patch: dict, dry_run: bool = False):
    error = validate_patch(patch)
    if error:
        return {"id": patch.get("id"), "status": "skipped" if error == "not approved" else "error", "reason": error}

    path = base_dir / patch["target_file"]
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() and not dry_run:
        path.write_text("", encoding="utf-8")

    text = path.read_text(encoding="utf-8") if path.exists() else ""
    old_text = patch.get("old_text")
    new_text = patch.get("new_text")
    suggested_entry = patch.get("suggested_entry")
    anchor = patch.get("anchor")
    insert_mode = patch.get("insert_mode", "append")

    if suggested_entry and suggested_entry in text:
        return {"id": patch.get("id"), "status": "skipped", "reason": "entry already present", "target": str(path)}

    if old_text is not None and new_text is not None:
        if old_text not in text:
            return {"id": patch.get("id"), "status": "error", "reason": "old_text not found", "target": str(path)}
        updated = text.replace(old_text, new_text, 1)
        if not dry_run:
            path.write_text(updated, encoding="utf-8")
        return {"id": patch.get("id"), "status": "applied", "mode": "replace", "target": str(path), "dry_run": dry_run}

    if suggested_entry and insert_mode == "after-anchor" and anchor:
        updated = insert_after_anchor(text, anchor, suggested_entry)
        if updated is None:
            return {"id": patch.get("id"), "status": "error", "reason": f"anchor not found: {anchor}", "target": str(path)}
        if not dry_run:
            path.write_text(updated, encoding="utf-8")
        return {"id": patch.get("id"), "status": "applied", "mode": "after-anchor", "target": str(path), "anchor": anchor, "dry_run": dry_run}

    if suggested_entry:
        updated = append_entry(text, suggested_entry)
        if not dry_run:
            path.write_text(updated, encoding="utf-8")
        return {"id": patch.get("id"), "status": "applied", "mode": "append", "target": str(path), "dry_run": dry_run}

    return {"id": patch.get("id"), "status": "error", "reason": "no applicable patch content", "target": str(path)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("patches", help="Path to JSON file from draft_patches.py")
    ap.add_argument("--base-dir", required=True, help="Workspace root containing SOUL.md/AGENTS.md/etc")
    ap.add_argument("-o", "--output", help="Write apply report JSON")
    ap.add_argument("--dry-run", action="store_true", help="Validate and simulate without writing files")
    args = ap.parse_args()

    data = load_json(Path(args.patches))
    patches = data.get("patch_candidates", [])
    base_dir = Path(args.base_dir)
    results = [apply_patch(base_dir, patch, dry_run=args.dry_run) for patch in patches]
    report = {
        "total": len(patches),
        "applied": sum(1 for r in results if r.get("status") == "applied"),
        "errors": sum(1 for r in results if r.get("status") == "error"),
        "dry_run": args.dry_run,
        "results": results,
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
