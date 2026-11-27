"""Small real-office font probes, cached by glyphs, font bytes and renderer."""
from __future__ import annotations

import re
import uuid
from pathlib import Path

from .contract import walk
from .runtime import CODE_ROOT, find_tool, fonts_for, launch_worker, renderer_identity, run_process, select_isolation
from .store import DesignError, Store, canonical, digest


def _east_asian(c):
    o = ord(c)
    return (0x2E80 <= o <= 0x9FFF or 0xAC00 <= o <= 0xD7AF or 0xF900 <= o <= 0xFAFF or
            0xFE30 <= o <= 0xFE4F or 0xFF00 <= o <= 0xFFEF or 0x20000 <= o <= 0x2FA1F)


def _page_fonts(pdf, page, stage):
    """Fonts actually used by text on one page.

    LibreOffice shares font resources across pages, so ``pdffonts -f/-l`` lists every font of the document.
    ``pdftohtml -xml`` attributes each text run to a subset prefix (e.g. ``BAAAAA+``); keep only those.
    """
    listing = run_process([find_tool("pdffonts"), "-f", str(page), "-l", str(page), str(pdf)], cwd=stage, timeout=15)
    names = [line.split()[0] for line in listing.splitlines()[2:] if line.strip()]
    tool = find_tool("pdftohtml")
    if tool:
        xml = run_process([tool, "-xml", "-i", "-stdout", "-q", "-f", str(page), "-l", str(page), str(pdf)], cwd=stage, timeout=30)
        used = set(re.findall(r'family="([A-Z]{6})\+', xml))
        if used:
            names = [n for n in names if n.split("+", 1)[0] in used or "+" not in n]
    return names


def _glyph_priority(char):
    """Test rare non-ASCII symbols (arrows, warnings, subscripts) before common ASCII/CJK glyphs."""
    code = ord(char)
    if code > 127 and not _east_asian(char):
        return (0, code)
    if _east_asian(char):
        return (1, code)
    return (2, code)


MAX_PROBE_PAGES = 60
GLYPHS_PER_PAGE = 240


def _format_literals(fmt):
    """Extract quoted literals and non-ASCII/currency/unit symbols from an Excel number format."""
    if not fmt:
        return ""
    quoted = "".join(re.findall(r'"([^"]*)"', fmt))
    stripped = re.sub(r'"[^"]*"', "", fmt)
    symbols = "".join(ch for ch in stripped if ord(ch) > 127 or ch in "$¥€£₩%+-.,/:()[]")
    return quoted + symbols


def font_samples(task):
    content = {c["id"]: c for c in task["content"]["items"]}
    faces = {}

    def add(font, text):
        # Office draws East Asian characters with the run's ea typeface; probe them with that face.
        ea = font.get("ea_family")
        for c in text:
            if c.isspace():
                continue
            family = ea if ea and _east_asian(c) else font["family"]
            faces.setdefault((family, bool(font.get("bold")), bool(font.get("italic"))), set()).add(c)

    def add_spans(text, base, spans):
        offset = 0
        for span in spans:
            add(base, text[offset:span["start"]])
            add(span["font"], text[span["start"]:span["end"]])
            offset = span["end"]
        add(base, text[offset:])

    for page in task["scene"]["pages"]:
        for node, *_ in walk(page["nodes"]):
            if "font" not in node:
                continue
            item = content.get(node.get("content_id"), {})
            if item.get("type") == "text":
                add_spans(item["text"], node["font"], node.get("spans", []))
            elif item.get("type") == "table" and "cell_styles" in node:
                for row, styles in zip(item["cells"], node["cell_styles"]):
                    for value, style in zip(row, styles):
                        add_spans(value, style.get("font", node["font"]), style.get("spans", []))
            elif item.get("type") == "table":
                add(node["font"], " ".join(x for row in item["cells"] for x in row))
                add({**node["font"], "bold": True}, " ".join(item["cells"][0]))
            elif item.get("type") == "chart":
                fmt_chars = (_format_literals(node.get("label_number_format", ""))
                             + _format_literals(node.get("axis", {}).get("number_format", "")))
                add(node["font"], " ".join(item["categories"]) + "0123456789.-%" + fmt_chars + " ".join(s["name"] for s in item["series"]))
    nonempty = [(face, sorted(chars, key=_glyph_priority)) for face, chars in sorted(faces.items()) if chars]
    if len(nonempty) > MAX_PROBE_PAGES:
        raise DesignError(f"FONT_PROBE_FACE_LIMIT: probe representative subsets (maximum {MAX_PROBE_PAGES} faces)")
    # Allocate at least one page per face, then distribute remaining page budget so long CJK decks
    # test every unique glyph instead of silently truncating at a fixed per-face cap.
    extra_pages = MAX_PROBE_PAGES - len(nonempty)
    samples = []
    for (family, bold, italic), ordered in nonempty:
        chunks_needed = max(1, (len(ordered) + GLYPHS_PER_PAGE - 1) // GLYPHS_PER_PAGE)
        extra_used = min(extra_pages, chunks_needed - 1)
        extra_pages -= extra_used
        pages_for_face = 1 + extra_used
        covered = min(len(ordered), pages_for_face * GLYPHS_PER_PAGE)
        untested = len(ordered) - covered
        for chunk_index in range(pages_for_face):
            segment = ordered[chunk_index * GLYPHS_PER_PAGE:(chunk_index + 1) * GLYPHS_PER_PAGE]
            if not segment:
                break
            samples.append({
                "family": family, "bold": bold, "italic": italic,
                "text": "".join(segment),
                "untested_glyphs": untested if chunk_index == pages_for_face - 1 else 0,
            })
    return samples


def _font_key(name):
    return re.sub(r"[^a-z0-9]", "", re.sub(r"^[A-Z]{6}\+", "", name).lower())


def preflight(root, *, isolation="auto"):
    from .pipeline import new_task
    with Store(root) as store:
        task = store.json("task.json")
        samples = font_samples(task)
        if not samples:
            raise DesignError("FONT_PROBE_NEEDS_AUTHORED_TEXT")
        needed = ("soffice", "pdftoppm", "fc-match", "pdffonts", "pdftotext")
        missing = [x for x in needed if not find_tool(x)]
        if missing:
            return {"status": "preflight_unavailable", "missing_tools": missing, "automatic_visual_approval": False}
        mode = select_isolation(isolation)
        inspection_tools = {x: digest(Path(find_tool(x)).read_bytes()) for x in ("pdffonts", "pdftotext")}
        if find_tool("pdftohtml"):
            inspection_tools["pdftohtml"] = digest(Path(find_tool("pdftohtml")).read_bytes())
        key = digest(canonical({"samples": samples, "fonts": fonts_for(task), "renderer": renderer_identity(),
                                "isolation": mode, "inspection_tools": inspection_tools}))
        cache_file = "preflight/cache-" + key + ".json"
        if (store.root / cache_file).exists():
            entry = store.json(cache_file)
            old = store.json(entry["report"])
            if digest(canonical(old)) != entry["sha256"] or old["cache_key"] != key:
                raise DesignError("FONT_PROBE_CACHE_CHANGED")
            prefix = old["report"].rsplit("/", 1)[0] + "/"
            for name, sha in old["artifacts"].items():
                if digest(store.read(prefix + name)) != sha:
                    raise DesignError("FONT_PROBE_CACHE_CHANGED")
            return {**old, "cache_hit": True}
        prefix = "preflight/font-" + key[:12] + "-" + uuid.uuid4().hex + "/"
        probe = new_task("font-preflight", mode="create", width=960, height=540, pages=len(samples), author="fixed-font-probe")
        probe["design"]["brief"] = "Internal font sample; not a presentation or visual approval."
        for page, sample in zip(probe["scene"]["pages"], samples):
            pid = page["id"]
            probe["content"]["items"].append({
                "id": "text-" + pid, "page_id": pid, "type": "text", "required_edit": "native", "text": sample["text"],
                "provenance": {"kind": "document", "source": "Glyphs from the current authored task", "checked": True, "uncertainties": []}})
            probe["content"]["notes"].append({"page_id": pid, "text": "Internal glyph/font test only."})
            page["nodes"].append({"id": "sample-" + pid, "page_id": pid, "type": "text", "role": "native_text", "z": 0,
                                  "box": {"x": 40, "y": 40, "width": 880, "height": 460},
                                  "content_id": "text-" + pid,
                                  "font": {k: sample[k] for k in ("family", "bold", "italic")},
                                  "align": "left", "valign": "top", "wrap": True})
            page["nodes"][0]["font"].update(size=20, color="17293A")
        store.put_json(prefix + "task.json", probe, exclusive=True)
        launch_worker(store.root / prefix, isolation=mode, preview=True)
        rendered = store.json(prefix + "render.json")
        if rendered["status"] != "passed":
            raise DesignError("FONT_PROBE_RENDER_FAILED: " + str(rendered.get("reason")))
        results = []
        stage = store.root / prefix
        for i, sample in enumerate(samples, 1):
            style = ("Bold" if sample["bold"] else "Regular") + (" Italic" if sample["italic"] else "")
            matched = run_process([find_tool("fc-match"), "-f", "%{postscriptname}\\n%{family}", sample["family"] + ":style=" + style],
                                  cwd=CODE_ROOT, timeout=15)
            expected, _, family_names = matched.partition("\n")
            actual = _page_fonts(stage / "deck.pdf", i, stage)
            text = run_process([find_tool("pdftotext"), "-f", str(i), "-l", str(i), str(stage / "deck.pdf"), "-"], cwd=stage, timeout=15)
            wanted = {_font_key(s) for s in expected.split(",") if s}
            fallback = [s for s in actual if _font_key(s) not in wanted]
            missing_chars = sorted(set(sample["text"]) - set(text))
            passed = bool(actual) and bool(wanted) and not fallback and not missing_chars
            results.append({**sample, "expected_postscript": expected, "fontconfig_family_names": family_names,
                            "actual_fonts": actual,
                            "unexpected_fonts": fallback, "missing_glyphs": missing_chars,
                            "status": "passed" if passed else "review_required", "preview": rendered["pages"][i - 1]["file"]})
        names = ["task.json", "deck.pptx", "deck.pdf", "render.json", "objects.json"]
        names.extend(p["file"] for p in rendered["pages"])
        report = {"status": "passed" if all(r["status"] == "passed" for r in results) else "font_review_required",
                  "cache_hit": False, "cache_key": key, "report": prefix + "report.json",
                  "samples": results, "render": rendered,
                  "artifacts": {n: digest(store.read(prefix + n)) for n in names},
                  "scope": "LibreOffice sampled glyphs; not target-software parity or visual approval"}
        if report["status"] != "passed":
            report["next_action"] = "Inspect actual fonts; try installed family aliases or select the actual font explicitly, then rerun and inspect layout."
        store.put_json(prefix + "report.json", report, exclusive=True)
        store.put_json(cache_file, {"report": report["report"], "sha256": digest(canonical(report))})
        return report
