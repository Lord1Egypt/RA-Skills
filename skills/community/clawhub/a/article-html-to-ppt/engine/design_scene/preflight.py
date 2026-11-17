"""Small real-office font probes, cached by glyphs, font bytes and renderer."""
from __future__ import annotations

import re
import uuid
from pathlib import Path

from .contract import walk
from .runtime import CODE_ROOT, find_tool, fonts_for, launch_worker, renderer_identity, run_process, select_isolation
from .store import DesignError, Store, canonical, digest


def font_samples(task):
    content = {c["id"]: c for c in task["content"]["items"]}
    faces = {}

    def add(font, text):
        key = (font["family"], bool(font.get("bold")), bool(font.get("italic")))
        faces.setdefault(key, set()).update(c for c in text if not c.isspace())

    for page in task["scene"]["pages"]:
        for node, *_ in walk(page["nodes"]):
            if "font" not in node:
                continue
            item = content.get(node.get("content_id"), {})
            if item.get("type") == "text":
                text = item["text"]
                spans = node.get("spans", [])
                covered = set()
                for s in spans:
                    add(s["font"], text[s["start"]:s["end"]])
                    covered.update(range(s["start"], s["end"]))
                add(node["font"], "".join(c for i, c in enumerate(text) if i not in covered))
            elif item.get("type") == "table":
                add(node["font"], " ".join(x for row in item["cells"] for x in row))
                add({**node["font"], "bold": True}, " ".join(item["cells"][0]))
            elif item.get("type") == "chart":
                add(node["font"], " ".join(item["categories"]) + "0123456789.-%" + " ".join(s["name"] for s in item["series"]))
    samples = []
    for (family, bold, italic), chars in sorted(faces.items()):
        if chars:
            samples.append({"family": family, "bold": bold, "italic": italic,
                            "text": "".join(sorted(chars))[:160], "untested_glyphs": max(0, len(chars) - 160)})
    if len(samples) > 60:
        raise DesignError("FONT_PROBE_FACE_LIMIT: probe representative subsets (maximum 60 faces)")
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
        key = digest(canonical({"samples": samples, "fonts": fonts_for(task), "renderer": renderer_identity(),
                                "isolation": mode,
                                "inspection_tools": {x: digest(Path(find_tool(x)).read_bytes())
                                                     for x in ("pdffonts", "pdftotext")}}))
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
            listing = run_process([find_tool("pdffonts"), "-f", str(i), "-l", str(i), str(stage / "deck.pdf")], cwd=stage, timeout=15)
            actual = [line.split()[0] for line in listing.splitlines()[2:] if line.strip()]
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
