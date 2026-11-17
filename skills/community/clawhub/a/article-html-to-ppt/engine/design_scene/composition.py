"""Declared composition diagnostics; never infer visual quality or approval."""
from __future__ import annotations

from collections import Counter

from .contract import walk


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
