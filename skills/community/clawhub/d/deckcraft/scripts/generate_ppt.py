#!/usr/bin/env python3
"""
DeckCraft v5 — CLI entry point for generating PPTX from outline JSON.

Usage:
    python3 generate_ppt.py -i outline.json -o output.pptx
    python3 generate_ppt.py -i outline.json -o output.pptx --theme tech --canvas 9:16
    python3 generate_ppt.py -i outline.json              # output defaults to input basename + .pptx

The outline JSON schema is documented in examples/03_from_outline_json.py and
SKILL.md. See also PAGE_HANDLERS below for the full type → method mapping.
"""
import sys, os, json, argparse
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import DeckEngine
from engine.constants import CANVAS_PRESETS, THEMES


# ── Outline schema → DeckEngine method mapping ─────────────────────
# To add a new page type, add it here AND mirror the schema in your outline JSON.

PAGE_HANDLERS = {
    "cover": lambda e, p: e.cover(
        title=p.get("title", ""), subtitle=p.get("subtitle", ""),
        author=p.get("author", ""), date=p.get("date", ""),
        image_path=p.get("image"),
    ),
    "closing": lambda e, p: e.closing(
        title=p.get("title", "Thank You"),
        message=p.get("message", ""),
        contact=p.get("contact", ""),
    ),
    "toc": lambda e, p: e.toc(items=p.get("items", [])),
    "section": lambda e, p: e.section_divider(
        section_title=p.get("title", ""),
        section_number=p.get("number"),
        subtitle=p.get("subtitle", ""),
    ),
    "content": lambda e, p: e.content(
        title=p.get("title", ""),
        bullets=p.get("content", p.get("bullets", [])),
        key_point=p.get("key_point", ""),
        image_path=p.get("image"),
        page_num=p.get("page_num"),
    ),
    "content_with_icon": lambda e, p: e.content_with_icon(
        title=p.get("title", ""), items=p.get("items", []),
        page_num=p.get("page_num"),
    ),
    "two-col": lambda e, p: e.two_col(
        title=p.get("title", ""),
        left_title=p.get("left_title", "A"),
        left_items=p.get("left_content", []),
        right_title=p.get("right_title", "B"),
        right_items=p.get("right_content", []),
        page_num=p.get("page_num"),
    ),
    "vs_compare": lambda e, p: e.vs_compare(
        title=p.get("title", ""),
        left_title=p.get("left_title", "A"),
        right_title=p.get("right_title", "B"),
        rows=p.get("rows", []),
        page_num=p.get("page_num"),
    ),
    "table": lambda e, p: e.table(
        title=p.get("title", ""),
        headers=p.get("headers", []),
        rows=p.get("rows", []),
        insights=p.get("insights"),
        page_num=p.get("page_num"),
    ),
    "stat_cards": lambda e, p: e.stat_cards(
        title=p.get("title", ""), stats=p.get("stats", []),
        page_num=p.get("page_num"),
    ),
    "chart_bar": lambda e, p: e.chart_bar(
        title=p.get("title", ""),
        data=p.get("data", [[]]),
        labels=p.get("labels", []),
        series_names=p.get("series_names"),
        orientation=p.get("orientation", "vertical"),
        page_num=p.get("page_num"),
    ),
    "chart_pie": lambda e, p: e.chart_pie(
        title=p.get("title", ""),
        data=p.get("data", []),
        labels=p.get("labels", []),
        donut=p.get("donut", True),
        page_num=p.get("page_num"),
    ),
    "chart_line": lambda e, p: e.chart_line(
        title=p.get("title", ""),
        data=p.get("data", [[]]),
        labels=p.get("labels", []),
        series_names=p.get("series_names"),
        fill_area=p.get("fill_area", False),
        page_num=p.get("page_num"),
    ),
    "chart_gauge": lambda e, p: e.chart_gauge(
        title=p.get("title", ""),
        value=p.get("value", 0),
        max_value=p.get("max_value", 100),
        label=p.get("label", ""),
        page_num=p.get("page_num"),
    ),
    "timeline": lambda e, p: e.timeline(
        title=p.get("title", ""),
        milestones=p.get("milestones", []),
        page_num=p.get("page_num"),
    ),
    "process_flow": lambda e, p: e.process_flow(
        title=p.get("title", ""),
        steps=p.get("steps", []),
        page_num=p.get("page_num"),
    ),
    "matrix_2x2": lambda e, p: e.matrix_2x2(
        title=p.get("title", ""),
        quadrants=p.get("quadrants", []),
        page_num=p.get("page_num"),
    ),
    "quote": lambda e, p: e.quote(
        title=p.get("title", ""),
        quote_text=p.get("quote_text", ""),
        attribution=p.get("attribution", ""),
        page_num=p.get("page_num"),
    ),
    "image_full": lambda e, p: e.image_full(
        title=p.get("title", ""),
        image_path=p.get("image", ""),
        caption=p.get("caption", ""),
        page_num=p.get("page_num"),
    ),
    "image_split": lambda e, p: e.image_split(
        title=p.get("title", ""),
        image_path=p.get("image", ""),
        bullets=p.get("content", []),
        image_side=p.get("image_side", "right"),
        page_num=p.get("page_num"),
    ),
    "kpi_dashboard": lambda e, p: e.kpi_dashboard(
        title=p.get("title", ""),
        kpis=p.get("kpis", []),
        page_num=p.get("page_num"),
    ),
    "team_grid": lambda e, p: e.team_grid(
        title=p.get("title", ""),
        members=p.get("members", []),
        page_num=p.get("page_num"),
    ),
    "checklist": lambda e, p: e.checklist(
        title=p.get("title", ""),
        items=p.get("items", []),
        checked=p.get("checked"),
        page_num=p.get("page_num"),
    ),
    "summary": lambda e, p: e.summary(
        title=p.get("title", ""),
        key_points=p.get("content", p.get("key_points", [])),
        conclusion=p.get("conclusion", ""),
        page_num=p.get("page_num"),
    ),
}


def generate_from_outline(outline: dict, output_path: str,
                          theme_name: str = "business",
                          canvas: str = "16:9") -> str:
    """Generate PPTX from outline JSON using DeckEngine.

    Args:
        outline: Dict with keys 'pages' (list of page dicts) and optionally
                 'theme' and 'canvas' (overridable by CLI args).
        output_path: Path to write the .pptx file.
        theme_name: One of THEMES keys. Overridden by outline["theme"] if present.
        canvas: One of CANVAS_PRESETS keys. Overridden by outline["canvas"] if present.

    Returns:
        output_path on success.

    Raises:
        ValueError: If theme or canvas is invalid.
        KeyError: If outline is missing required 'pages' key.
    """
    # Validate theme/canvas early
    if theme_name not in THEMES:
        raise ValueError(f"Unknown theme: {theme_name!r}. Available: {list(THEMES)}")
    if canvas not in CANVAS_PRESETS:
        raise ValueError(f"Unknown canvas: {canvas!r}. Available: {list(CANVAS_PRESETS)}")

    # Allow outline to override defaults
    theme_name = outline.get("theme", theme_name)
    canvas = outline.get("canvas", canvas)

    pages = outline.get("pages")
    if not pages:
        raise ValueError("Outline has no 'pages' list (or it's empty)")

    eng = DeckEngine(theme_name=theme_name, canvas=canvas)

    skipped = []
    for i, page in enumerate(pages, 1):
        ptype = page.get("type", "content")
        handler = PAGE_HANDLERS.get(ptype)
        if handler is None:
            skipped.append((i, ptype))
            continue
        try:
            handler(eng, page)
        except (TypeError, KeyError) as e:
            raise ValueError(f"Page {i} (type={ptype!r}) has invalid fields: {e}") from e

    eng.save(output_path)
    msg = f"✓ {output_path} — {eng._slide_count} slides, {theme_name}/{canvas}"
    if skipped:
        msg += f"  (skipped {len(skipped)} unknown page types: {[t for _, t in skipped]})"
    print(msg)
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="DeckCraft v5 — Generate PPTX from outline JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available themes:  business, business_dark, tech, tech_gradient, minimal,
                   elegant, creative, green, red, ocean
Available canvases: 16:9, 9:16, 1:1, 4:3, A4, A4-portrait
                     (aliases: mobile, square, ppt)
        """,
    )
    parser.add_argument("-i", "--input", "--outline", required=True,
                        dest="outline",
                        help="Path to outline JSON file (required)")
    parser.add_argument("-o", "--output", default=None,
                        help="Output PPTX path (default: <input_basename>.pptx)")
    parser.add_argument("-t", "--theme", default="business",
                        help="Theme name (default: business, or outline['theme'])")
    parser.add_argument("-c", "--canvas", default="16:9",
                        help="Canvas preset (default: 16:9, or outline['canvas'])")
    parser.add_argument("--list-themes", action="store_true",
                        help="List all available themes and exit")
    parser.add_argument("--list-canvases", action="store_true",
                        help="List all available canvases and exit")
    parser.add_argument("--notes-file", default=None,
                        help="JSON file mapping slide numbers to speaker notes "
                             '(e.g. {"1": "Welcome everyone..."})')

    args = parser.parse_args()

    if args.list_themes:
        print("Available themes:")
        for name, theme in THEMES.items():
            print(f"  {name:18s} — {theme['name']}")
        return 0
    if args.list_canvases:
        print("Available canvases:")
        for name, (w, h, *_rest) in CANVAS_PRESETS.items():
            print(f"  {name:14s} — {w:.2f}\" × {h:.2f}\"")
        return 0

    # Resolve output path
    output_path = args.output
    if output_path is None:
        base = os.path.splitext(os.path.basename(args.outline))[0]
        output_path = f"{base}.pptx"

    # Load outline
    if not os.path.isfile(args.outline):
        print(f"ERROR: outline file not found: {args.outline}", file=sys.stderr)
        return 2
    try:
        with open(args.outline, "r", encoding="utf-8") as f:
            outline = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in {args.outline}: {e}", file=sys.stderr)
        return 2

    # Generate
    try:
        generate_from_outline(outline, output_path,
                              theme_name=args.theme, canvas=args.canvas)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    # Add speaker notes if provided
    if args.notes_file:
        if not os.path.isfile(args.notes_file):
            print(f"WARNING: Notes file not found: {args.notes_file}", file=sys.stderr)
        else:
            try:
                with open(args.notes_file, "r", encoding="utf-8") as f:
                    notes = json.load(f)
                from scripts.add_notes import add_notes
                count = add_notes(output_path, notes)
                if count >= 0:
                    print(f"  with speaker notes from {args.notes_file}")
            except (json.JSONDecodeError, Exception) as e:
                print(f"WARNING: Failed to add notes: {e}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
