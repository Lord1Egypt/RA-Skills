from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone

from common import dump_json, load_json, state_root


def manifest_to_map(manifest: dict) -> dict[str, dict]:
    return {item["path"]: item for item in manifest.get("files", [])}


def build_diff(old_manifest: dict, new_manifest: dict) -> dict:
    old_files = manifest_to_map(old_manifest)
    new_files = manifest_to_map(new_manifest)

    added = sorted(path for path in new_files if path not in old_files)
    removed = sorted(path for path in old_files if path not in new_files)
    changed = sorted(
        path
        for path in new_files
        if path in old_files and new_files[path]["sha256"] != old_files[path]["sha256"]
    )

    by_category = Counter()
    for path in added + removed + changed:
        by_category[path.split("/", 1)[0] if "/" in path else "_root"] += 1

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "from_generated_at": old_manifest.get("generated_at"),
        "to_generated_at": new_manifest.get("generated_at"),
        "added": added,
        "removed": removed,
        "changed": changed,
        "summary": {
            "added": len(added),
            "removed": len(removed),
            "changed": len(changed),
            "category_changes": dict(sorted(by_category.items())),
        },
    }


def render_markdown(diff: dict) -> str:
    summary = diff["summary"]
    lines = [
        "# OpenClaw Docs Diff",
        "",
        f"- Generated at: `{diff['generated_at']}`",
        f"- Added: `{summary['added']}`",
        f"- Removed: `{summary['removed']}`",
        f"- Changed: `{summary['changed']}`",
        "",
        "## Category Totals",
        "",
    ]
    for category, count in summary["category_changes"].items():
        lines.append(f"- `{category}`: {count}")
    if not summary["category_changes"]:
        lines.append("- No category-level changes detected.")

    for title, key in (("Added", "added"), ("Removed", "removed"), ("Changed", "changed")):
        lines.extend(["", f"## {title}", ""])
        items = diff[key]
        if items:
            lines.extend(f"- `{item}`" for item in items[:100])
        else:
            lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    state = state_root()
    new_manifest_path = state / "docs-manifest.json"
    old_manifest_path = state / "docs-manifest.previous.json"

    if not new_manifest_path.exists():
        print("ERROR: docs-manifest.json does not exist. Run build_knowledge.py first.")
        return 1

    new_manifest = load_json(new_manifest_path)
    old_manifest = load_json(old_manifest_path) if old_manifest_path.exists() else {"files": []}
    diff = build_diff(old_manifest, new_manifest)
    dump_json(state / "latest-diff.json", diff)
    (state / "latest-diff.md").write_text(render_markdown(diff), encoding="utf-8")
    print("Wrote latest-diff.json and latest-diff.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
