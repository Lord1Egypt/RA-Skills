#!/usr/bin/env python3
"""打印 cad-scan 结果首屏（证据坐标/置信度/复核原因）。仅供 scripts/demo.sh 使用。"""
import json, sys

def walk(c, depth=0):
    out = []
    if isinstance(c, list):
        for x in c:
            out += walk(x, depth + 1)
    elif isinstance(c, dict):
        for k, v in c.items():
            if isinstance(v, dict):
                if k in ("members", "walls", "beams", "columns", "slabs", "spec", "evidence") and v:
                    out += [(k, str(v))[:200] for _ in [0]][0:1]
                else:
                    out += walk(v, depth + 1)
            elif k in ("name", "text", "kind", "value", "confidence", "review_reason", "layer", "id", "source_id"):
                out.append((k, str(v)[:120]))
    return out

def main(path):
    import pyboot
    pyboot.ensure_utf8_io()
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    shown = 0
    for k, v in d.items():
        if shown >= 14:
            break
        if isinstance(v, (dict, list)):
            rows = walk(v)[:8]
            if not rows:
                continue
            print(f"## {k}")
            for kk, vv in rows:
                print(f"  - {kk}: {vv}")
                shown += 1
        else:
            print(f"## {k}: {str(v)[:160]}")
            shown += 1

if __name__ == "__main__":
    main(sys.argv[1])
