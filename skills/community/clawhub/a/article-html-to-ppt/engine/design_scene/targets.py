"""Content-locked external design targets; never a rendering/self-review shortcut."""
from __future__ import annotations

import copy

from .store import DesignError, canonical, digest


def visible_content(task, page_id):
    return [{k: c[k] for k in ("id", "type", "text", "categories", "series", "cells", "required_edit") if k in c}
            for c in task["content"]["items"] if c["page_id"] == page_id]


def target_context(task, page_id):
    refs = [r for r in task["design"]["references"] if page_id in r["page_ids"] and "style" in r["roles"]]
    ids = {r["asset_id"] for r in refs}
    result = {"brief": task["design"]["brief"], "canvas": task["canvas"], "references": refs,
              "assets": [{k: a[k] for k in ("id", "sha256", "original_sha256")}
                         for a in task["assets"]["items"] if a["id"] in ids]}
    # Omit absent optional fields so old frozen targets retain their hashes.
    if "review_profile" in task["design"]:
        result["review_profile"] = task["design"]["review_profile"]
    design = next(p for p in task["design"]["pages"] if p["page_id"] == page_id)
    if "composition" in design:
        result["composition"] = design["composition"]
    return copy.deepcopy(result)


def freeze_generated_target(task, request, *, page_id, asset_id, confirmed_by):
    """Host confirms a reviewed image, checking the exact requested content and style."""
    from .contract import validate
    validate(task)
    requested = next((p for p in request.get("request", {}).get("pages", [])
                      if p.get("page_id") == page_id), None)
    if not requested or request.get("generated") is not False:
        raise DesignError("GENERATED_TARGET_REQUEST_REQUIRED")
    content_hash = digest(canonical(visible_content(task, page_id)))
    context_hash = digest(canonical(target_context(task, page_id)))
    if requested.get("content_sha256") != content_hash or requested.get("context_sha256") != context_hash:
        raise DesignError("STALE_IMAGE_REQUEST: regenerate or explicitly revise the requested design")
    asset = next((a for a in task["assets"]["items"] if a["id"] == asset_id), None)
    if not asset or "tool_result" not in asset or asset["role"] != "target" or page_id not in asset["page_ids"]:
        raise DesignError("ACTUAL_IMAGE_TARGET_REQUIRED")
    if asset["tool_result"].get("request_sha256") != digest(canonical(request)):
        raise DesignError("IMAGE_TARGET_REQUEST_MISMATCH: receipt must identify this exact request")
    if not isinstance(confirmed_by, str) or not confirmed_by.strip():
        raise DesignError("TARGET_CONFIRMATION_REQUIRED")
    candidate = copy.deepcopy(task)
    page = next(p for p in candidate["design"]["pages"] if p["page_id"] == page_id)
    page.update(target_asset_id=asset_id, target_kind="generated", confirmed_by=confirmed_by,
                target_content_sha256=content_hash, target_context_sha256=context_hash)
    validate(candidate)
    return candidate
