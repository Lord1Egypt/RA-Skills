"""Reuse independent page evidence only when semantics AND actual output match."""
from __future__ import annotations

import copy

from .store import DesignError, canonical, digest

CHECKS = ("design", "reconstruction", "content", "editability", "fonts")


def page_evidence(task, manifest):
    previews = {p["page_id"]: p for p in manifest["render"]["pages"]}
    objects = {p["page_id"]: p for p in manifest["object_inspection"]["pages"]}
    designs = {p["page_id"]: p for p in task["design"]["pages"]}
    common = {k: task[k] for k in ("task_id", "author_id", "mode", "audience", "language", "target_software", "canvas")}
    common.update(brief=task["design"]["brief"], page_order=[p["id"] for p in task["scene"]["pages"]],
                  environment=manifest["environment"], fonts=manifest["fonts"],
                  render={k: manifest["render"].get(k) for k in ("engine", "version", "path", "dpi")})
    if "review_profile" in task["design"]:
        common["review_profile"] = task["design"]["review_profile"]
    result = {}
    for page in task["scene"]["pages"]:
        pid = page["id"]
        preview = previews.get(pid)
        if not preview or pid not in objects:
            continue
        record = {"common": common, "scene": page, "design": designs[pid],
                  "content": [c for c in task["content"]["items"] if c["page_id"] == pid],
                  "notes": [n for n in task["content"]["notes"] if n["page_id"] == pid],
                  "references": [r for r in task["design"]["references"] if pid in r["page_ids"]],
                  "assets": [a for a in task["assets"]["items"] if pid in a["page_ids"]],
                  "native_objects": objects[pid], "preview_sha256": manifest["artifacts"].get(preview["file"])}
        result[pid] = digest(canonical(record))
    return result


def _page_can_inherit(assessment, pid):
    # A different page's unresolved visual issue does not revoke this page's
    # review. Global failures (fonts, render, editing, isolation) always do.
    for blocker in assessment["blockers"]:
        # Whole-deck rhythm is reviewed afresh on every candidate. An unresolved
        # deck composition does not erase independent evidence for unchanged
        # pages; review_skeleton never inherits the whole-deck approval.
        if blocker == "DECK_COMPOSITION_REVIEW_REQUIRED":
            continue
        parts = blocker.rsplit(":", 1)
        if len(parts) != 2 or parts[1] == pid or parts[0] not in {x.upper() + "_REVIEW_REQUIRED" for x in CHECKS}:
            return False
    return True


def prepare_inheritance(store, task, manifest, draft, previous):
    from .pipeline import assess, build_prefix, verify_build
    old_task, old = verify_build(store, previous["build_id"], snapshot=True)
    assessment = assess(store, old["build_id"], previous, snapshot=True)
    if old_task["task_id"] != task["task_id"] or old["build_id"] == manifest["build_id"]:
        raise DesignError("INHERITANCE_TASK_OR_BUILD_MISMATCH")
    before, after = page_evidence(old_task, old), page_evidence(task, manifest)
    old_pages = {p["page_id"]: p for p in previous["pages"]}
    inherited = []
    sha = digest(canonical(previous))
    for index, row in enumerate(draft["pages"]):
        pid = row["page_id"]
        if pid not in old_pages or not after.get(pid) or after[pid] != before.get(pid) or not _page_can_inherit(assessment, pid):
            continue
        source = copy.deepcopy(old_pages[pid])
        source["inherited_from"] = {
            "build_id": old["build_id"], "manifest_sha256": digest(store.read(build_prefix(old["build_id"]) + "manifest.json")),
            "review_sha256": sha}
        draft["pages"][index] = source
        inherited.append(pid)
    if inherited:
        store.put_json("review-evidence/" + sha + ".json", previous)
    return inherited


def verify_inheritance(store, task, manifest, review, chain, cache):
    from .pipeline import assess, build_prefix, verify_build
    current = page_evidence(task, manifest)
    for row in review["pages"]:
        source = row.get("inherited_from")
        if not source:
            continue
        if source["build_id"] in chain or len(chain) >= 10:
            raise DesignError("REVIEW_INHERITANCE_CYCLE_OR_DEPTH")
        sha = source["review_sha256"]
        if sha not in cache:
            old_review = store.json("review-evidence/" + sha + ".json")
            if digest(canonical(old_review)) != sha or old_review["build_id"] != source["build_id"]:
                raise DesignError("INHERITED_REVIEW_CHANGED")
            old_task, old = verify_build(store, source["build_id"], snapshot=True)
            assessment = assess(store, source["build_id"], old_review, snapshot=True, _chain=chain, _cache=cache)
            cache[sha] = (old_review, old_task, old, assessment)
        old_review, old_task, old, assessment = cache[sha]
        if (old["build_id"] != source["build_id"] or old_task["task_id"] != task["task_id"] or
                source["manifest_sha256"] != digest(store.read(build_prefix(old["build_id"]) + "manifest.json"))):
            raise DesignError("INHERITED_MANIFEST_CHANGED")
        pid = row["page_id"]
        old_row = next((p for p in old_review["pages"] if p["page_id"] == pid), None)
        if (not old_row or not current.get(pid) or current[pid] != page_evidence(old_task, old).get(pid)
                or not _page_can_inherit(assessment, pid)):
            raise DesignError("INHERITED_PAGE_CHANGED: " + pid)
        if {k: v for k, v in row.items() if k != "inherited_from"} != {k: v for k, v in old_row.items() if k != "inherited_from"}:
            raise DesignError("INHERITED_REVIEW_ROW_CHANGED: " + pid)


def archive_evidence(store, archive, review, seen=None):
    seen = set() if seen is None else seen
    from .pipeline import build_prefix
    for row in review["pages"]:
        source = row.get("inherited_from")
        if not source or source["review_sha256"] in seen:
            continue
        seen.add(source["review_sha256"])
        if len(seen) > 10:
            raise DesignError("REVIEW_INHERITANCE_DEPTH")
        path = "review-evidence/" + source["review_sha256"] + ".json"
        data = store.read(path)
        previous = store.json(path)
        archive.writestr(path, data)
        archive.writestr("review-evidence/" + source["review_sha256"] + "-manifest.json",
                         store.read(build_prefix(source["build_id"]) + "manifest.json"))
        archive_evidence(store, archive, previous, seen)
