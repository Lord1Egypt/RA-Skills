#!/usr/bin/env python3
"""build_outline_deck.py — render a pptxgenjs deck from a banker-memo
`slides-outline.md` (agent-produced PPT blueprint), not from a hard-coded
8-slide Python template.

Why: the v0.9.5 `build_deck.py` baked slide count + structure into Python.
Result was a data dashboard, not banker analysis. The banker-memo skill
now has the agent author a 10-15 slide outline per company, and this
script translates that outline into slide-NN.js files + compile.

Outline format (what the banker-memo prompt produces):

    ## Slide N — Title
    Title: <slide title>
    Subtitle: <optional>
    Layout: <one of: cover | divider | card-grid | table | bullets | chart>
    Key message: <one-line takeaway>
    Data used: <source refs, e.g. "analysis.md §1" or "daily_basic">

Usage:
    python3 build_outline_deck.py <deliverable_dir> <ts_code> <name_cn> <name_en>

The deliverable dir must contain slides-outline.md (from banker-memo skill).
"""
from __future__ import annotations
import json, pathlib, re, shutil, subprocess, sys


SLIDE_HEADER = re.compile(r"^##\s*Slide\s+(\d+)\s*[—\-–]\s*(.+)$", re.MULTILINE)


def parse_outline(outline_md: str) -> list[dict]:
    """Parse slides-outline.md into a list of {num, heading, title,
    subtitle, layout, key_message, data_used} dicts."""
    slides: list[dict] = []
    # Split on slide headers. The first split piece is preamble we skip.
    parts = re.split(r"(?=^##\s*Slide\s+\d+\s*[—\-–])", outline_md, flags=re.MULTILINE)
    for part in parts:
        m = SLIDE_HEADER.match(part)
        if not m:
            continue
        num = int(m.group(1))
        heading = m.group(2).strip()
        body = part[m.end():]
        fields = {"num": num, "heading": heading,
                  "title": "", "subtitle": "", "layout": "bullets",
                  "key_message": "", "data_used": ""}
        for line in body.splitlines():
            ls = line.strip()
            for key, py_key in (("Title:", "title"), ("Subtitle:", "subtitle"),
                                ("Layout:", "layout"),
                                ("Key message:", "key_message"),
                                ("Data used:", "data_used")):
                if ls.startswith(key):
                    fields[py_key] = ls[len(key):].strip()
                    break
        # Normalise layout token. Agents phrase this variably:
        #   "Rule 3 (English 44pt + Chinese subtitle)" → cover
        #   "Section Divider" in heading → divider
        #   "左右分栏 / card" → card
        lay = fields["layout"].lower()
        heading_lower = heading.lower()
        if num == 1 or "cover" in lay or "rule 3" in lay or "rule3" in lay:
            fields["layout"] = "cover"
        elif "divider" in heading_lower or "divider" in lay or "section divider" in heading_lower:
            fields["layout"] = "divider"
        elif "card" in lay or "分栏" in lay:
            fields["layout"] = "card"
        elif "table" in lay or "表" in lay:
            fields["layout"] = "table"
        elif "chart" in lay or "图" in lay:
            fields["layout"] = "chart"
        else:
            fields["layout"] = "bullets"
        slides.append(fields)
    return slides


def js_str(s: str) -> str:
    return json.dumps(s or "", ensure_ascii=False)


def render_cover(s: dict, name_en: str, ts_code: str) -> str:
    return f"""  // Rule 3: English hero + Chinese subtitle
  slide.addText({js_str(name_en)}, {{
    x: 0.7, y: 1.7, w: 8.5, h: 1.2,
    fontSize: 44, bold: true, color: theme.secondary, fontFace: 'Arial',
  }});
  slide.addText({js_str(s['title'])}, {{
    x: 0.7, y: 2.85, w: 8.5, h: 0.8,
    fontSize: 26, color: 'FFFFFF', fontFace: 'Microsoft YaHei',
  }});
  slide.addText({js_str(s.get('subtitle') or ts_code)}, {{
    x: 0.7, y: 3.65, w: 8.5, h: 0.6,
    fontSize: 18, color: theme.secondary, fontFace: 'Microsoft YaHei',
  }});
  slide.addShape(pres.ShapeType.rect, {{
    x: 0, y: 5.4, w: 10, h: 0.06,
    fill: {{ color: theme.secondary }}, line: {{ color: theme.secondary, width: 0 }},
  }});
"""


def render_divider(s: dict) -> str:
    return f"""  slide.addShape(pres.ShapeType.rect, {{
    x: 0, y: 2.2, w: 10, h: 1.4,
    fill: {{ color: theme.light }}, line: {{ color: theme.light, width: 0 }},
  }});
  slide.addText({js_str(s['title'])}, {{
    x: 0.7, y: 2.35, w: 8.5, h: 0.8,
    fontSize: 34, bold: true, color: theme.secondary, fontFace: 'Microsoft YaHei',
  }});
  slide.addText({js_str(s['subtitle'])}, {{
    x: 0.7, y: 3.0, w: 8.5, h: 0.6,
    fontSize: 16, color: 'AAAAAA', fontFace: 'Arial',
  }});
"""


def render_content(s: dict) -> str:
    """Generic content slide — title + key message + data-used footnote."""
    title = s["title"] or s["heading"]
    km = s["key_message"]
    du = s["data_used"]
    return f"""  slide.addText({js_str(title)}, {{
    x: 0.5, y: 0.3, w: 9, h: 0.6,
    fontSize: 24, bold: true, color: theme.secondary, fontFace: 'Microsoft YaHei',
  }});
  slide.addShape(pres.ShapeType.rect, {{
    x: 0.5, y: 1.2, w: 9, h: 3.6,
    fill: {{ color: theme.light }}, line: {{ color: theme.secondary, width: 0.5 }},
  }});
  slide.addText({js_str(km or '(see analysis.md for detail)')}, {{
    x: 0.8, y: 1.5, w: 8.4, h: 3,
    fontSize: 16, color: 'FFFFFF', fontFace: 'Microsoft YaHei', valign: 'top',
  }});
  slide.addText({js_str('Source / layout: ' + (du or 'see analysis.md'))}, {{
    x: 0.5, y: 5.25, w: 9, h: 0.3,
    fontSize: 10, italic: true, color: '888888', fontFace: 'Arial',
  }});
"""


def emit_slide_file(s: dict, name_en: str, ts_code: str) -> str:
    if s["layout"] == "cover":
        body = render_cover(s, name_en, ts_code)
    elif s["layout"] == "divider":
        body = render_divider(s)
    else:
        # card / table / bullets / chart — all render as generic content
        # slide for now; the agent's key-message is the main payload, and
        # the title reflects the slide's purpose. Future: specialise per layout.
        body = render_content(s)
    return f"""// slide-{s['num']:02d}.js — {s['layout']}
const createSlide = (pres, theme) => {{
  const slide = pres.addSlide();
  slide.background = {{ color: theme.bg }};
  slide.addShape(pres.ShapeType.rect, {{
    x: 0, y: 0, w: 10, h: 0.08,
    fill: {{ color: theme.secondary }}, line: {{ color: theme.secondary, width: 0 }},
  }});
{body}
}};

const slideConfig = {{ notes: {js_str(s['key_message'])}, title: {js_str(s['title'])} }};

module.exports = {{ createSlide, slideConfig }};
"""


def main() -> int:
    if len(sys.argv) < 5:
        sys.exit("usage: build_outline_deck.py <dir> <ts_code> <name_cn> <name_en>")
    d = pathlib.Path(sys.argv[1]).resolve()
    ts_code, name_cn, name_en = sys.argv[2], sys.argv[3], sys.argv[4]

    outline_path = d / "slides-outline.md"
    if not outline_path.exists():
        sys.exit(f"{outline_path} missing — run banker-memo skill first.")
    slides_spec = parse_outline(outline_path.read_text(encoding="utf-8"))
    if not slides_spec:
        sys.exit("parser found 0 slides in slides-outline.md; check format")
    slides_spec.sort(key=lambda s: s["num"])

    slides_dir = d / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)
    # Clean stale slide-NN.js from previous runs
    for old in slides_dir.glob("slide-*.js"):
        old.unlink()

    for s in slides_spec:
        (slides_dir / f"slide-{s['num']:02d}.js").write_text(
            emit_slide_file(s, name_en, ts_code))

    # Copy + configure compile.js from the skill template
    template_path = (pathlib.Path.home() /
                     ".openclaw/extensions/aigroup-financial-services-openclaw"
                     "/skills/cn-client-investigation/references"
                     "/compile_with_typo_gate.template.js.txt")
    template = template_path.read_text()
    slide_count = len(slides_spec)
    output_pptx = f"{ts_code.replace('.', '_').lower()}_banker_memo.pptx"
    template = (template
        .replace("const SLIDE_COUNT = 20;", f"const SLIDE_COUNT = {slide_count};")
        .replace("'presentation.pptx'", f"'{output_pptx}'")
        .replace("'2B2D42'", "'0D1829'")
        .replace("'8D99AE'", "'C9A84C'")
        .replace("'EF233C'", "'D4AF37'")
        .replace("'EDF2F4'", "'2A3A5C'")
        .replace("'FFFFFF'", "'0D1829'"))
    (slides_dir / "compile.js").write_text(template)
    (slides_dir / "package.json").write_text(json.dumps({
        "name": f"{ts_code.lower().replace('.', '-')}-banker-deck",
        "version": "0.0.1", "private": True,
        "dependencies": {"pptxgenjs": "^3.12.0"},
    }, indent=2))

    if not (slides_dir / "node_modules" / "pptxgenjs").exists():
        r = subprocess.run(["npm", "install", "--omit=dev", "--silent"],
                           cwd=str(slides_dir), capture_output=True,
                           text=True, timeout=120)
        if r.returncode != 0:
            sys.exit(f"npm install failed: {r.stderr[:500]}")

    r = subprocess.run(["node", "compile.js"], cwd=str(slides_dir),
                       capture_output=True, text=True, timeout=180)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    if r.returncode != 0:
        sys.exit(f"compile failed rc={r.returncode}")

    pptx = d / output_pptx
    print(f"OK: {pptx} ({pptx.stat().st_size} bytes, {slide_count} slides from outline)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
