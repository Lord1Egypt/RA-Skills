#!/usr/bin/env python3
"""
Build the index of draw.io NATIVE shapes (vector stencils that ship with
diagrams.net), so the .drawio output can use first-class draw.io shapes instead
of embedded SVG images.

Sources (from the jgraph/drawio repo):
  * stencils/aws4.xml   -> AWS shapes   -> style "shape=mxgraph.aws4.<name>"
  * stencils/gcp2.xml   -> GCP shapes   -> style "shape=mxgraph.gcp2.<name>"
  * stencils/azure.xml  -> Azure shapes -> style "shape=mxgraph.azure.<name>"
  * js/.../Sidebar-AWS4.js -> the per-category fillColor for each AWS service
    (AWS stencils inherit the style color, so we need it; the official AWS
    resourceIcon look is a colored rounded square behind a white glyph).

GCP stencils are self-colored; Azure stencils are monochrome (we give them a
default Azure blue). The draw.io shape key is the package name + the stencil's
`name` lowercased with spaces -> underscores.

Output: references/drawio-shape-index.json  (small — names + colors only, NOT
the stencil geometry, so the skill stays lightweight).

Usage (defaults fetch from GitHub):
    python build_drawio_shape_index.py
    python build_drawio_shape_index.py --local /tmp   # use pre-downloaded files
"""
import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "references" / "drawio-shape-index.json"
RAW = "https://raw.githubusercontent.com/jgraph/drawio/dev/src/main/webapp"
STENCILS = {  # provider -> (stencil path, mxgraph package, default fill or None)
    "aws":   ("stencils/aws4.xml",  "mxgraph.aws4",  None),
    "gcp":   ("stencils/gcp2.xml",  "mxgraph.gcp2",  None),       # self-colored
    "azure": ("stencils/azure.xml", "mxgraph.azure", "#0078D4"),  # monochrome
}
AWS_SIDEBAR = "js/diagramly/sidebar/Sidebar-AWS4.js"
AWS_DEFAULT = "#232F3E"  # AWS "general" squid-ink, used when no category color


def slurp(rel, local):
    if local:
        return Path(local, Path(rel).name).read_text("utf-8", "replace")
    return urllib.request.urlopen(f"{RAW}/{rel}", timeout=60).read().decode("utf-8", "replace")


def shape_names(xml):
    return re.findall(r'<shape\b[^>]*\bname="([^"]+)"', xml)


def aws_color_map(js):
    """name(with underscores) -> category color, by walking the sidebar in order."""
    events = []
    for m in re.finditer(r"fillColor=#([0-9A-Fa-f]{6})", js):
        events.append((m.start(), "c", m.group(1)))
    for m in re.finditer(r"resIcon='\s*\+\s*gn\s*\+\s*'\.([a-z0-9_]+)", js):
        events.append((m.start(), "s", m.group(1)))
    for m in re.finditer(r"createVertexTemplateEntry\(\s*n\d?\s*\+\s*'([a-z0-9_]+);", js):
        tok = m.group(1)
        if tok not in ("resourceIcon", "group", "groupCenter", "productIcon"):
            events.append((m.start(), "s", tok))
    events.sort()
    cur, out = AWS_DEFAULT.lstrip("#"), {}
    for _, t, v in events:
        if t == "c":
            cur = v
        else:
            out.setdefault(v, "#" + cur)
    return out


def tokens(name):
    base = re.sub(r"[^a-z0-9 ]", " ", name.lower())
    return f"{base} {base.replace(' ', '')}".strip()


def build(local=None):
    aws_colors = aws_color_map(slurp(AWS_SIDEBAR, local))
    index = []
    for provider, (path, pkg, default_fill) in STENCILS.items():
        xml = slurp(path, local)
        seen = set()
        for raw_name in shape_names(xml):
            key_name = raw_name.lower().replace(" ", "_")
            if key_name in seen:
                continue
            seen.add(key_name)
            entry = {
                "shape_provider": provider,
                "name": raw_name,
                "key": f"{pkg}.{key_name}",
                "search": tokens(raw_name),
            }
            if provider == "aws":
                entry["color"] = aws_colors.get(key_name, AWS_DEFAULT)
            elif default_fill:
                entry["color"] = default_fill
            index.append(entry)
    OUT.write_text(json.dumps(index, ensure_ascii=False))
    by = {}
    for e in index:
        by[e["shape_provider"]] = by.get(e["shape_provider"], 0) + 1
    print(f"Wrote {len(index)} draw.io shapes -> {OUT}")
    print("By provider:", by)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", help="dir with pre-downloaded stencil XML + sidebar JS")
    build(ap.parse_args().local)


if __name__ == "__main__":
    main()
