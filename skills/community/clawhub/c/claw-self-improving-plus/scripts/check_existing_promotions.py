#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("patches", help="Patch JSON from draft_patches.py")
    ap.add_argument("--base-dir", required=True, help="Workspace base dir containing target files")
    ap.add_argument("-o", "--output", help="Output JSON")
    args = ap.parse_args()

    data = load_json(Path(args.patches))
    base_dir = Path(args.base_dir)
    results = []

    for patch in data.get("patch_candidates", []):
        target = patch.get("target_file")
        entry = (patch.get("suggested_entry") or "").strip()
        path = base_dir / target if target else None
        present = False
        if path and path.exists() and entry:
            present = entry in path.read_text(encoding="utf-8")
        results.append({
            "id": patch.get("id"),
            "target_file": target,
            "already_present": present,
            "status": "duplicate-promotion" if present else "new-promotion",
        })

    report = {
        "total": len(results),
        "already_present": sum(1 for r in results if r["already_present"]),
        "results": results,
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
