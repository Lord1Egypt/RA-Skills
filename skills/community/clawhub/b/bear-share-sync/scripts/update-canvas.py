#!/usr/bin/env python3
"""update-canvas.py — Append knowledge nodes for new #share notes to a JSON Canvas file."""
import argparse
import json
import os
import sys

def load_canvas(path: str) -> dict:
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"nodes": [], "edges": []}

def save_canvas(path: str, canvas: dict):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump(canvas, f, indent=2, ensure_ascii=False)

def next_y(canvas: dict) -> int:
    if not canvas["nodes"]:
        return 0
    return max(n.get("y", 0) + n.get("height", 100) for n in canvas["nodes"]) + 200

def ensure_group(canvas: dict) -> str:
    """Find or create the 'Shared Notes' group node."""
    for n in canvas["nodes"]:
        if n.get("type") == "group" and n.get("label") == "Shared Notes":
            return n["id"]
    gid = "group-shared-notes"
    canvas["nodes"].append({
        "id": gid,
        "type": "group",
        "label": "Shared Notes",
        "x": -100,
        "y": -100,
        "width": 800,
        "height": 600,
        "color": "5"
    })
    return gid

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--canvas", required=True, help="Path to .canvas file")
    parser.add_argument("--notes", default="/dev/stdin", help="JSON file of notes (default stdin)")
    args = parser.parse_args()

    notes = json.load(open(args.notes))
    if not notes:
        print("No new notes to add.")
        return

    canvas = load_canvas(args.canvas)
    y = next_y(canvas)
    gid = ensure_group(canvas)
    existing_ids = {n["id"] for n in canvas["nodes"]}

    for i, note in enumerate(notes):
        nid = f"share-{note['id']}"
        if nid in existing_ids:
            continue
        title = note.get("title", "Untitled")
        content = note.get("content", "")
        # Truncate content for node display
        display = f"## {title}\n\n{content[:500]}"
        if len(content) > 500:
            display += "…"

        node = {
            "id": nid,
            "type": "text",
            "text": display,
            "x": 0,
            "y": y + i * 250,
            "width": 400,
            "height": 200,
            "color": "4"
        }
        canvas["nodes"].append(node)

        # Edge from group to node
        eid = f"edge-{nid}"
        canvas["edges"].append({
            "id": eid,
            "fromNode": gid,
            "fromSide": "bottom",
            "toNode": nid,
            "toSide": "top",
            "toEnd": "arrow"
        })

    # Expand group height to cover new nodes
    for n in canvas["nodes"]:
        if n["id"] == gid:
            n["height"] = max(n["height"], (len(notes)) * 250 + 200)
            break

    save_canvas(args.canvas, canvas)
    print(f"Added {len(notes)} node(s) to {args.canvas}")

if __name__ == "__main__":
    main()
