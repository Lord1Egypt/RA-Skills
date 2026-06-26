#!/usr/bin/env python3
"""
Example 4: Import from PDF/DOCX/Markdown

Turn an existing document (a brief, a past report, a wiki export) into a
DeckCraft outline JSON, then render it to PPTX.

The import is heuristic — it makes a best-effort guess at page types
(cover, toc, content, table, stat_cards, etc.). You should review the
generated outline and adjust before publishing.

This script:
1. Imports a sample document (or any file path you pass as argv[1])
2. Saves the outline JSON to examples/output/
3. Renders the outline to PPTX
4. Reports how many slides of each type were generated
"""
import sys, os, subprocess, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.importers import detect_and_import
from engine import DeckEngine
from scripts.generate_ppt import PAGE_HANDLERS

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUT_DIR, exist_ok=True)

# Sample document paths (use the first one that exists, or accept argv[1])
SAMPLES = [
    "/tmp/test_doc.pdf",       # from PDF (made by fpdf2)
    "/tmp/test_doc.docx",      # from DOCX (made by python-docx)
    "/tmp/test_doc.md",        # from Markdown
]


def find_source() -> str:
    """Pick the first existing sample, or use argv[1]."""
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        return sys.argv[1]
    for s in SAMPLES:
        if os.path.isfile(s):
            return s
    print("No sample found. Create one with:")
    print("  python3 -c \"import docx; d=docx.Document(); d.add_heading('Test',0); d.save('/tmp/test_doc.docx')\"")
    sys.exit(1)


def import_and_render(source_path: str, theme: str = "business", canvas: str = "16:9"):
    """Import source → outline JSON → PPTX."""
    base = os.path.splitext(os.path.basename(source_path))[0]
    outline_path = os.path.join(OUT_DIR, f"{base}_outline.json")
    pptx_path = os.path.join(OUT_DIR, f"{base}.pptx")

    # 1. Import
    print(f"Step 1: Importing {source_path} ...")
    outline = detect_and_import(source_path, theme=theme, canvas=canvas)
    with open(outline_path, "w", encoding="utf-8") as f:
        json.dump(outline, f, indent=2, ensure_ascii=False)

    # 2. Report what we got
    pages = outline["pages"]
    type_counts = {}
    for p in pages:
        t = p.get("type", "?")
        type_counts[t] = type_counts.get(t, 0) + 1
    print(f"  ✓ {len(pages)} slides detected: "
          + ", ".join(f"{k}×{v}" for k, v in sorted(type_counts.items())))

    # 3. Render
    print(f"Step 2: Rendering to {pptx_path} ...")
    eng = DeckEngine(theme_name=theme, canvas=canvas)
    for page in pages:
        ptype = page.get("type", "content")
        handler = PAGE_HANDLERS.get(ptype)
        if handler:
            handler(eng, page)
    eng.save(pptx_path)
    print(f"  ✓ Saved {eng.slide_count} slides ({eng.prs.slide_width/914400:.1f}\" × "
          f"{eng.prs.slide_height/914400:.1f}\")")

    # 4. Run gate
    print("Step 3: Running gate check ...")
    result = subprocess.run(
        ["python3", "scripts/gate_check.py", pptx_path, "/tmp/"],
        capture_output=True, text=True,
    )
    if "GATE PASSED" in result.stdout:
        print("  ✓ Gate PASSED (100/100)")
    else:
        print("  ⚠ Gate reported issues. Check the PPTX visually.")

    print()
    print(f"Output files:")
    print(f"  - Outline: {outline_path}")
    print(f"  - PPTX:    {pptx_path}")
    print()
    print("Tip: Edit the outline JSON to fine-tune page types or content,")
    print("     then re-run generate_ppt.py to regenerate the PPTX.")


if __name__ == "__main__":
    source = find_source()
    import_and_render(source)
