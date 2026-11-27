"""Declared composition diagnostics; never infer visual quality or approval."""
from __future__ import annotations

from collections import Counter
import re

from .contract import walk

_SECTION_NUM_ONLY = re.compile(r"^\s*(?:0?([1-9]|1[0-9]|20))\s*$")
_SECTION_NUM_TAG = re.compile(
    r"^\s*(?:第\s*0?([1-9]|1[0-9]|20)\s*[章篇部]|(?:PART|CHAPTER|SECTION)\s+0?([1-9]|1[0-9]|20)\b)",
    re.IGNORECASE,
)
_EYEBROW_NUM = re.compile(r"^\s*(?:第\s*0?([1-9]|1[0-9]|20)\s*[章篇部]|0?([1-9]|1[0-9]|20)(?=\s+[^\d/]))")
_CONTENTS_ITEM_NUM = re.compile(r"^\s*(?:0?([1-9]|1[0-9]|20)\s*$|第\s*0?([1-9]|1[0-9]|20)\s*[章篇部]|0([1-9]|1[0-9])\s+[\u4e00-\u9fffA-Za-z])")


def _extract_group_int(match):
    if not match:
        return None
    for group in match.groups():
        if group:
            return int(group)
    return None


def _page_texts(page, content):
    entries = []
    for node, _, ox, oy in walk(page.get("nodes", [])):
        if node.get("type") != "text":
            continue
        item = content.get(node.get("content_id"))
        if not item or item.get("type") != "text":
            continue
        text = (item.get("text") or "").strip()
        if not text:
            continue
        box = node["box"]
        entries.append({
            "text": text,
            "x": ox + box["x"],
            "y": oy + box["y"],
            "size": node.get("font", {}).get("size", 0),
        })
    return entries


def _section_lead_number(page, content, canvas_height):
    candidates = []
    for entry in _page_texts(page, content):
        if entry["y"] > canvas_height * 0.8:
            continue
        num = _extract_group_int(_SECTION_NUM_ONLY.match(entry["text"]))
        priority = 2 if num is not None else 1
        if num is None:
            num = _extract_group_int(_SECTION_NUM_TAG.match(entry["text"]))
        if num is not None:
            candidates.append((priority, entry["size"], -entry["y"], num))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][3]


def _eyebrow_chapter_number(page, content, canvas_height):
    top_limit = max(90.0, canvas_height * 0.18)
    for entry in sorted(_page_texts(page, content), key=lambda e: (e["y"], e["x"])):
        if entry["y"] > top_limit or entry["size"] > 15:
            continue
        num = _extract_group_int(_EYEBROW_NUM.match(entry["text"]))
        if num is not None:
            return num
    return None


def _contents_chapter_numbers(page, content, canvas_height):
    nums = set()
    for entry in _page_texts(page, content):
        if entry["y"] > canvas_height * 0.88:
            continue
        num = _extract_group_int(_CONTENTS_ITEM_NUM.match(entry["text"]))
        if num is not None:
            nums.add(num)
    if len(nums) >= 2 and 1 in nums and nums == set(range(1, max(nums) + 1)):
        return sorted(nums)
    return []


def _claim_observation(page, composition, content):
    """Read scene bindings; a declared claim is not necessarily a page title."""
    claim = composition.get("claim_content_id")
    result = {"page_id": page["id"], "claim_content_id": claim, "nodes": []}
    item = content.get(claim)
    if not claim:
        result["status"] = "missing_claim_reference"
    elif item is None:
        result["status"] = "missing_content"
    elif item.get("type") != "text":
        result["status"] = "non_text_content"
    else:
        for node, _, ox, oy in walk(page.get("nodes", [])):
            if node["type"] != "text" or node.get("content_id") != claim:
                continue
            box = node["box"]
            result["nodes"].append({
                "node_id": node["id"],
                "absolute_box": {**box, "x": ox + box["x"], "y": oy + box["y"]},
                "font": dict(node["font"]), "align": node["align"],
                "valign": node["valign"], "margin": node.get("margin", 0),
                "spans": [{**span, "font": dict(span["font"])} for span in node.get("spans", [])],
            })
        count = len(result["nodes"])
        result["status"] = ("observed" if count == 1 else
                            "multiple_native_text_nodes" if count else "no_native_text_node")
    return result


def _anchor_patterns(observations):
    """Exact observations only: neither a drift tolerance nor a quality score."""
    patterns = {}
    for observation in observations:
        for node in observation["nodes"]:
            anchor = {"x": node["absolute_box"]["x"], "y": node["absolute_box"]["y"],
                      "font_family": node["font"]["family"], "font_size": node["font"]["size"],
                      "align": node["align"]}
            key = tuple(anchor.values())
            pattern = patterns.setdefault(key, {"anchor": anchor, "page_ids": [], "node_ids": []})
            if observation["page_id"] not in pattern["page_ids"]:
                pattern["page_ids"].append(observation["page_id"])
            pattern["node_ids"].append(node["node_id"])
    return list(patterns.values())


def composition_diagnostics(task):
    """Flag repetition for human review without banning intentional sequences.

    A different shape or author-supplied family name does not prove a different
    topology. Reviewers must inspect the actual deck and semantic reading paths.
    Navigation pages interrupt consecutive runs and are excluded from ratios.
    """
    designs = {page["page_id"]: page for page in task["design"]["pages"]}
    body, runs, run, matrix, unplanned, claims = [], [], [], [], [], []
    content = {item["id"]: item for item in task.get("content", {}).get("items", [])}
    roles = {role: [] for role in ("cover", "contents", "section", "body", "closing", "unplanned")}
    section = None
    previous = None
    for number, page in enumerate(task["scene"]["pages"], 1):
        composition = designs[page["id"]].get("composition")
        role = composition["page_role"] if composition else "unplanned"
        roles[role].append(page["id"])
        if role == "section":
            section = page["id"]
        row = {"page_id": page["id"], "page_number": number,
               "planning_status": "planned" if composition else "missing",
               "latest_section_page_id": section}
        if composition:
            row.update({key: composition[key] for key in ("page_role", "content_relation", "layout_family",
                        "reading_path", "information_attachment", "claim_content_id") if key in composition})
        else:
            unplanned.append(page["id"])
        matrix.append(row)
        key = None
        if composition and composition["page_role"] == "body":
            key = (composition["layout_family"].strip().casefold(), composition["information_attachment"])
            body.append((page["id"], key))
            claims.append(_claim_observation(page, composition, content))
        if key is not None and key == previous:
            run.append(page["id"])
        else:
            if len(run) >= 3:
                runs.append(run)
            run = [page["id"]] if key is not None else []
        previous = key
    if len(run) >= 3:
        runs.append(run)
    warnings = [{"code": "COMPOSITION_REPEATED_SEQUENCE", "page_ids": pages,
                 "message": "Inspect whether the repeated structure supports a deliberate sequence; shape changes alone do not prove variety."}
                for pages in runs]
    if task["design"].get("review_profile") == "decorative_business" and unplanned:
        warnings.insert(0, {"code": "COMPOSITION_PLAN_INCOMPLETE", "page_ids": unplanned,
                            "message": "Complete the page composition plans before building this review profile."})
    counts = Counter(key for _, key in body)
    if len(body) >= 5 and counts:
        dominant, count = counts.most_common(1)[0]
        if count / len(body) >= .6:
            warnings.append({"code": "COMPOSITION_DOMINANT_FAMILY",
                             "page_ids": [pid for pid, key in body if key == dominant],
                             "message": "Review deck rhythm and content fit; this declared family dominates the body pages."})
    canvas_height = float(task.get("canvas", {}).get("height") or 540)
    scene_pages = {page["id"]: page for page in task["scene"]["pages"]}
    section_ids = roles["section"]
    if len(section_ids) >= 2:
        bgs = {}
        for pid in section_ids:
            bg = str(scene_pages[pid].get("background") or "").strip().lstrip("#").upper()
            bgs.setdefault(bg, []).append(pid)
        if len(bgs) > 1:
            warnings.append({
                "code": "SECTION_STYLE_INCONSISTENT",
                "page_ids": list(section_ids),
                "backgrounds": {bg or "(none)": pids for bg, pids in bgs.items()},
                "message": "Section dividers use inconsistent background colors; unify section divider visual templates across the deck.",
            })
    contents_ids = roles["contents"]
    if contents_ids and section_ids:
        ordered = [(p["id"], (designs[p["id"]].get("composition") or {}).get("page_role", "unplanned"))
                   for p in task["scene"]["pages"]]
        first_contents = next(i for i, (_, r) in enumerate(ordered) if r == "contents")
        first_section = next(i for i, (_, r) in enumerate(ordered) if r == "section")
        if first_section > first_contents + 1:
            gap_bodies = [pid for pid, r in ordered[first_contents + 1:first_section] if r == "body"]
            if gap_bodies:
                warnings.append({
                    "code": "SECTION_LEAD_IN_MISSING",
                    "page_ids": gap_bodies,
                    "message": "Body pages appear between the contents slide and the first section divider; confirm whether Chapter 1 is missing its section divider.",
                })
        toc_chapters = []
        for pid in contents_ids:
            found = _contents_chapter_numbers(scene_pages[pid], content, canvas_height)
            if len(found) > len(toc_chapters):
                toc_chapters = found
        if toc_chapters and len(section_ids) < len(toc_chapters):
            warnings.append({
                "code": "SECTION_COUNT_MISMATCH",
                "page_ids": list(contents_ids) + list(section_ids),
                "contents_chapters": len(toc_chapters),
                "section_divider_count": len(section_ids),
                "message": f"Contents lists {len(toc_chapters)} top-level chapters, but only {len(section_ids)} section dividers exist; ensure every top-level chapter has a matching divider or remove partial dividers.",
            })
    if section_ids:
        ordered = [(p["id"], (designs[p["id"]].get("composition") or {}).get("page_role", "unplanned"))
                   for p in task["scene"]["pages"]]
        for idx, (pid, role) in enumerate(ordered):
            if role != "section":
                continue
            sec_num = _section_lead_number(scene_pages[pid], content, canvas_height)
            if sec_num is None:
                continue
            mismatched = []
            eyebrow_nums = []
            for next_pid, next_role in ordered[idx + 1:]:
                if next_role in {"section", "closing"}:
                    break
                if next_role != "body":
                    continue
                eb_num = _eyebrow_chapter_number(scene_pages[next_pid], content, canvas_height)
                if eb_num is not None and eb_num != sec_num:
                    mismatched.append(next_pid)
                    if eb_num not in eyebrow_nums:
                        eyebrow_nums.append(eb_num)
            if mismatched:
                warnings.append({
                    "code": "SECTION_NUMBER_MISMATCH",
                    "page_ids": [pid] + mismatched,
                    "section_number": sec_num,
                    "eyebrow_numbers": eyebrow_nums,
                    "message": f"Section divider {pid} shows number {sec_num:02d}, while following body eyebrows show {eyebrow_nums}; unify TOC, section divider, and eyebrow numbering.",
                })
    return {"status": "diagnostic_only", "automatic_visual_approval": False,
            "body_page_count": len(body), "declared_family_count": len({key[0] for key in counts}),
            "declared_structure_count": len(counts),
            "unplanned_page_ids": unplanned, "pages": matrix,
            "navigation_inventory": {
                "evidence": "declared_page_roles_in_scene_order",
                "page_ids_by_role": roles,
                "role_counts": {role: len(ids) for role, ids in roles.items()},
                "review_note": "Verify roles against actual pages and the intended narrative. Missing contents, section or closing pages are not automatically defects; summary, decisions, closing and appendix order require human review.",
            },
            "body_claim_observations": claims,
            "body_claim_anchor_patterns": _anchor_patterns(claims),
            "observation_notes": [
                "Claim bindings identify scene text boxes, not inferred titles or rendered glyph baselines. Group offsets are included; actual rendering still requires inspection.",
                "Anchor patterns use exact x/y, base font family/size and alignment. Font overrides and box dimensions are listed per node; intentional differences are not failures.",
                "Only declared body pages enter anchor patterns. Unplanned and navigation pages remain visible in the ordered page inventory and need human verification.",
                "latest_section_page_id records the latest declared section in scene order, including the current page if it is a section; it is not a verified semantic grouping.",
            ],
            "warnings": warnings}
