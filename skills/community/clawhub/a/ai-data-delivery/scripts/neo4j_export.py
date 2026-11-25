#!/usr/bin/env python3
"""Export verified semantic snapshots as Neo4j CSV + fixed Cypher; no network access."""
import argparse
import json
import os
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workbench.semantic_package import read_package
from workbench.neo4j_export import export_neo4j


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package',required=True)
    parser.add_argument('--out',required=True)
    args=parser.parse_args()
    output=Path(args.out)
    created=False
    try:
        content,manifest=export_neo4j(read_package(args.package))
        with output.open('xb') as f:
            created=True;f.write(content);f.flush();os.fsync(f.fileno())
        print(json.dumps({'status':'exported','output':str(output.resolve()),**manifest},ensure_ascii=False))
        return 0
    except (ValueError,OSError) as exc:
        if created:output.unlink(missing_ok=True)
        print(json.dumps({'status':'error','error':str(exc)},ensure_ascii=False))
        return 2


if __name__=='__main__':raise SystemExit(main())
