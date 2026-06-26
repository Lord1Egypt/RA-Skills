#!/usr/bin/env python3
"""Resolve place name via superpicky region-query and write workspace/bird.json region fields."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from bird_json_util import infer_country_code, load_doc, save_doc, workspace_bird_path


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def superpicky_skill_root() -> Path:
    env = os.environ.get("SUPERPICKY_CLI_SKILL", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return (skill_root().parent / "superpicky-cli").resolve()


def run_region_query(query: str, *, limit: int) -> List[Tuple[float, Dict[str, Any]]]:
    root = superpicky_skill_root()
    run_sh = root / "scripts" / "run.sh"
    if not run_sh.is_file():
        raise FileNotFoundError(f"missing {run_sh}; set SUPERPICKY_CLI_SKILL or install superpicky-cli skill")
    cmd = [str(run_sh), "--region-query", query, "--json", "--limit", str(limit)]
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"region-query failed ({proc.returncode}): {err}")

    rows: List[Tuple[float, Dict[str, Any]]] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        score = float(obj.get("score", 0))
        rows.append((score, obj))
    rows.sort(key=lambda x: -x[0])
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Set eBird region in workspace/bird.json from place name.",
        epilog="When called by an agent: use an absolute path for this script and for --workspace.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Absolute path to project root (contains workspace/bird.json); default cwd for local CLI only",
    )
    parser.add_argument("--location", required=True, help="Place name for region-query")
    parser.add_argument("--limit", type=int, default=15, help="Max region-query results")
    parser.add_argument(
        "--pick",
        type=int,
        default=None,
        help="0-based index into ranked results (default: 0)",
    )
    parser.add_argument(
        "--disambiguate",
        action="store_true",
        help="If set, require --pick when the top two scores are within 0.04",
    )
    args = parser.parse_args()
    ws: Path = args.workspace

    try:
        ranked = run_region_query(args.location.strip(), limit=args.limit)
    except (FileNotFoundError, RuntimeError, json.JSONDecodeError) as e:
        print(str(e), file=sys.stderr)
        return 1

    if not ranked:
        print("No region-query results.", file=sys.stderr)
        return 2

    if args.disambiguate and len(ranked) >= 2:
        s0, s1 = ranked[0][0], ranked[1][0]
        if s0 - s1 < 0.04 and args.pick is None:
            print("Ambiguous matches; choose --pick index:\n", file=sys.stderr)
            for i, (sc, r) in enumerate(ranked[:8]):
                print(
                    f"  [{i}] {r.get('code')}  {r.get('name')}  {r.get('name_cn', '')}  score={sc:.3f}",
                    file=sys.stderr,
                )
            return 3

    pick = 0 if args.pick is None else args.pick
    if pick < 0 or pick >= len(ranked):
        print(f"--pick {pick} out of range (0..{len(ranked)-1})", file=sys.stderr)
        return 4

    _score, row = ranked[pick]
    region = {
        "code": row.get("code", ""),
        "name": row.get("name", ""),
        "name_cn": row.get("name_cn", ""),
        "kind": row.get("kind", ""),
        "parent": row.get("parent", ""),
        "match_score": round(float(row.get("score", _score)), 4),
    }
    doc = load_doc(ws)
    doc["location_query"] = args.location.strip()
    doc["region"] = region
    doc["country_code"] = infer_country_code(region)
    save_doc(ws, doc)

    out_path = workspace_bird_path(ws)
    print(f"Wrote {out_path}")
    print(json.dumps({"region": region, "country_code": doc["country_code"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
