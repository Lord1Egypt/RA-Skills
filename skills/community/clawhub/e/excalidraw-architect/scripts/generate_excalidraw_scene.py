#!/usr/bin/env python3
"""
Generate Excalidraw element JSON from a compact architecture spec.

Usage:
  python scripts/generate_excalidraw_scene.py --spec spec.json --out elements.json

Spec format (example):
{
  "title": "多租户外贸线索架构",
  "subtitle": "第一层：采集到 Raw Data Pool",
  "nodes": [
    {"id":"src", "x":40, "y":160, "w":360, "h":220, "title":"线索来源", "body":"Google Maps\\nReddit\\nFacebook"},
    {"id":"collector", "x":480, "y":160, "w":360, "h":220, "title":"采集层", "body":"Gosom Worker\\nReddit/Facebook Bot"},
    {"id":"raw", "x":920, "y":160, "w":420, "h":260, "title":"Raw Data Pool", "body":"tenant_id 分区"}
  ],
  "edges": [
    {"from":"src", "to":"collector"},
    {"from":"collector", "to":"raw"}
  ]
}
"""

import argparse
import json
import time
from pathlib import Path


def text_size(text: str, font_size: int):
    lines = (text or "").split("\n")
    max_len = max((len(x) for x in lines), default=1)
    width = max(100, round(max_len * font_size * 0.58))
    height = max(24, round(len(lines) * font_size * 1.35))
    return width, height


def base_element(eid, etype, x, y, w, h, seed, version, nonce, bg="#ffffff"):
    return {
        "id": eid,
        "type": etype,
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": "#1f2937",
        "backgroundColor": bg,
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 3},
        "seed": seed,
        "version": version,
        "versionNonce": nonce,
        "isDeleted": False,
        "boundElements": [],
        "updated": int(time.time() * 1000),
        "link": None,
        "locked": False,
    }


def make_text(eid, x, y, text, font_size, seed, version, nonce, color="#111827"):
    w, h = text_size(text, font_size)
    t = base_element(eid, "text", x, y, w, h, seed, version, nonce, bg="transparent")
    t.update(
        {
            "strokeColor": color,
            "backgroundColor": "transparent",
            "strokeWidth": 1,
            "roundness": None,
            "boundElements": None,
            "text": text,
            "fontSize": font_size,
            "fontFamily": 1,
            "textAlign": "center",
            "verticalAlign": "middle",
            "containerId": None,
            "originalText": text,
            "lineHeight": 1.25,
            "baseline": round(font_size * 0.9),
            "autoResize": True,
        }
    )
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="Path to spec.json")
    ap.add_argument("--out", required=True, help="Path to output elements JSON")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])

    seed = 1000
    version = 1
    nonce = 5000

    elements = []

    # Title
    title = spec.get("title")
    subtitle = spec.get("subtitle")
    if title:
        elements.append(make_text("title", 700, 20, title, 30, seed, version, nonce, color="#0f172a"))
        seed += 1; version += 1; nonce += 1
    if subtitle:
        elements.append(make_text("subtitle", 700, 70, subtitle, 18, seed, version, nonce, color="#475569"))
        seed += 1; version += 1; nonce += 1

    node_map = {}

    # Blocks + labels
    for i, n in enumerate(nodes, start=1):
        nid = n["id"]
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        fill = n.get("fill", "#ffffff")
        rect = base_element(f"{nid}-rect", "rectangle", x, y, w, h, seed, version, nonce, bg=fill)
        elements.append(rect)
        seed += 1; version += 1; nonce += 1

        title_txt = n.get("title", "")
        body_txt = n.get("body", "")
        if title_txt:
            elements.append(make_text(f"{nid}-title", x + w / 2 - 80, y + 14, title_txt, 20, seed, version, nonce))
            seed += 1; version += 1; nonce += 1
        if body_txt:
            elements.append(make_text(f"{nid}-body", x + w / 2 - 110, y + 60, body_txt, 16, seed, version, nonce, color="#374151"))
            seed += 1; version += 1; nonce += 1

        node_map[nid] = n

    # Arrows
    for i, e in enumerate(edges, start=1):
        s = node_map[e["from"]]
        t = node_map[e["to"]]
        sx = s["x"] + s["w"]
        sy = s["y"] + s["h"] / 2
        ex = t["x"]
        ey = t["y"] + t["h"] / 2
        dx = ex - sx
        dy = ey - sy
        arr = base_element(f"edge-{i}", "arrow", sx, sy, abs(dx), abs(dy), seed, version, nonce, bg="transparent")
        arr.update(
            {
                "backgroundColor": "transparent",
                "points": [[0, 0], [dx, dy]],
                "startBinding": None,
                "endBinding": None,
                "startArrowhead": None,
                "endArrowhead": "arrow",
                "elbowed": False,
            }
        )
        elements.append(arr)
        seed += 1; version += 1; nonce += 1

    Path(args.out).write_text(json.dumps(elements, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(elements)} elements to {args.out}")


if __name__ == "__main__":
    main()
