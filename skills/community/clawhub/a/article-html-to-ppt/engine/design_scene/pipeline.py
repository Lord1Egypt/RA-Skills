"""Task lifecycle: ingest → target → scene → candidate → review → delivery."""
from __future__ import annotations

import io
import copy
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from PIL import Image, ImageChops, ImageStat
from jsonschema import Draft202012Validator

from .backend import inspect_objects
from .contract import ID, SHORT, SHA, arr, enum, obj, validate, versions, walk
from .composition import composition_diagnostics
from .runtime import fonts_for, launch_worker, renderer_identity, select_isolation
from .store import (DesignError, Store, canonical, decode_image, digest, external_bytes,
                    json_bytes, normalized_png)


def now():
    return datetime.now(timezone.utc).isoformat()


def new_task(task_id, *, mode, width, height, pages=1, author="host-model",
             audience="待填写", language="zh-CN", target_software="LibreOffice"):
    pids = ["page-" + str(i + 1) for i in range(pages)]
    task = {"schema_version": "1.1" if mode == "create" else "1.0", "task_id": task_id, "author_id": author, "mode": mode,
            "audience": audience, "language": language, "target_software": target_software,
            "canvas": {"width": width, "height": height, "unit": "pt"},
            "content": {"items": [], "notes": []}, "assets": {"items": []},
            "design": {"brief": "", "references": [], "revision_budget": 3,
                       "pages": [{"page_id": p, "quality_limits": [], "accepted_differences": [],
                                  "aspect_policy": "exact", "raster_acceptances": []} for p in pids]},
            "scene": {"pages": [{"id": p, "background": "FFFFFF", "nodes": []} for p in pids]}}
    if mode != "template":
        validate(task)
    return task


def ingest(store, task, *, asset_id, data, page_ids, role, source, crop=None, tool_result=None):
    if not re.fullmatch(ID["pattern"], asset_id):
        raise DesignError("INVALID_ASSET_ID")
    if any(a["id"] == asset_id for a in task["assets"]["items"]):
        raise DesignError("ASSET_ID_EXISTS: use a new id for replacements")
    png, size = normalized_png(data, crop)
    asset = {"id": asset_id, "sha256": digest(png), "original_sha256": digest(data),
             "width": size[0], "height": size[1], "page_ids": page_ids, "role": role, "source": source}
    if crop is not None:
        asset["crop"] = crop
    if tool_result is not None:
        asset["tool_result"] = tool_result
    candidate = {**task, "assets": {"items": [*task["assets"]["items"], asset]}}
    validate(candidate)
    # Identical payloads share a content-addressed file; conflicting bytes cannot overwrite it.
    for name, payload in (("assets/" + asset["sha256"] + ".png", png),
                          ("originals/" + asset["original_sha256"] + ".image", data)):
        store.write(name, payload)
    store.put_json("task.json", candidate)
    return asset


def read_assets(store, task):
    result = {}
    total_bytes = 0
    for a in task["assets"]["items"]:
        data = store.read("assets/" + a["sha256"] + ".png")
        original = store.read("originals/" + a["original_sha256"] + ".image")
        total_bytes += len(data) + len(original)
        if total_bytes > 128 * 1024 * 1024:
            raise DesignError("TOTAL_ASSET_BYTE_LIMIT")
        if digest(data) != a["sha256"] or digest(original) != a["original_sha256"]:
            raise DesignError("ASSET_CONTENT_CHANGED")
        im = decode_image(data)
        if im.size != (a["width"], a["height"]):
            raise DesignError("ASSET_DIMENSIONS_CHANGED")
        result[a["id"]] = data
    return result


def image_request(task, *, page_ids=None):
    """An allowlist projection, not serialization of internal content records."""
    validate(task)
    from .targets import target_context
    all_ids = {p["id"] for p in task["scene"]["pages"]}
    selected = all_ids if page_ids is None else set(page_ids)
    if not selected or not selected <= all_ids or page_ids is not None and len(selected) != len(page_ids):
        raise DesignError("IMAGE_REQUEST_PAGE_SELECTION_INVALID")
    pages = []
    for page in task["scene"]["pages"]:
        if page["id"] not in selected:
            continue
        visible = []
        for c in task["content"]["items"]:
            if c["page_id"] != page["id"]:
                continue
            if not c["provenance"]["checked"]:
                raise DesignError("CHECK_CONTENT_BEFORE_IMAGE_REQUEST")
            visible.append({k: c[k] for k in ("id", "type", "text", "categories", "series", "cells", "required_edit") if k in c})
        refs = [r for r in task["design"]["references"] if page["id"] in r["page_ids"]]
        design = next(d for d in task["design"]["pages"] if d["page_id"] == page["id"])
        pages.append({"page_id": page["id"], "visible_content": visible,
                      "content_sha256": digest(canonical(visible)),
                      "context_sha256": digest(canonical(target_context(task, page["id"]))),
                      "references": [{"asset_id": r["asset_id"], "roles": r["roles"],
                                      "priority": r["priority"], "features": r["features"]} for r in refs],
                      "reference_features": [r["features"] for r in refs],
                      **({"composition": design["composition"]} if "composition" in design else {})})
    return copy.deepcopy({"status": ("reference_analysis_required" if task["mode"] == "recreate" else
                       "optional_image_tool_request" if task["mode"] == "create" else "image_tool_required"),
            "task_sha256": versions(task)["task"],
            "request": {"mode": task["mode"], "audience": task["audience"], "language": task["language"],
                        "canvas": task["canvas"], "visual_brief": task["design"]["brief"], "pages": pages,
                        **({"review_profile": task["design"]["review_profile"]} if "review_profile" in task["design"] else {}),
                        "instruction": "Design each complete slide using only the supplied visible content. Do not invent data or labels. Style references supply visual rules, not business content. Preserve exact facts and units. Prefer clean editable typography, flat shapes and native charts; avoid effects unsupported by the renderer. Charts and tables will be reconstructed deterministically from checked data. Review the design and reconstruction feasibility before freezing it as a target.",
                        "editable_types": ["text", "shape", "path", "chart", "table"],
                        "unsupported_effects": ["gradient", "mask", "embedded_font", "automatic_text_reflow"],
                        "asset_policy": "Standalone illustrations may remain replaceable images; complete slide images cannot substitute for editable content."},
            "generated": False})


def _fit_target(im, size, background):
    ratio = min(size[0] / im.width, size[1] / im.height)
    scaled = im.convert("RGB").resize((max(1, round(im.width * ratio)), max(1, round(im.height * ratio))), Image.Resampling.LANCZOS)
    result = Image.new("RGB", size, "#" + background)
    result.paste(scaled, ((size[0] - scaled.width) // 2, (size[1] - scaled.height) // 2))
    return result


def comparisons(store, prefix, task, preview, assets):
    """Produce a real-target/real-preview pair and per-region diagnostic error.

    No metric is interpreted as design quality or automatic approval.
    """
    out = []
    designs = {p["page_id"]: p for p in task["design"]["pages"]}
    scenes = {p["id"]: p for p in task["scene"]["pages"]}
    for page in preview["pages"]:
        pid = page["page_id"]
        target_id = designs[pid].get("target_asset_id")
        if not target_id:
            continue
        actual = decode_image(store.read(prefix + page["file"])).convert("RGB")
        target = _fit_target(decode_image(assets[target_id]), actual.size, scenes[pid]["background"])
        pair = Image.new("RGB", (actual.width * 2, actual.height), "white")
        pair.paste(target, (0, 0))
        pair.paste(actual, (actual.width, 0))
        b = io.BytesIO()
        pair.save(b, format="PNG")
        name = "compare-" + pid + ".png"
        store.write(prefix + name, b.getvalue(), exclusive=True)
        diff = ImageChops.difference(actual, target)
        regions = []
        sx, sy = actual.width / task["canvas"]["width"], actual.height / task["canvas"]["height"]
        for n, _, ox, oy in walk(scenes[pid]["nodes"]):
            box = n["box"]
            crop = (round((ox + box["x"]) * sx), round((oy + box["y"]) * sy),
                    round((ox + box["x"] + box["width"]) * sx), round((oy + box["y"] + box["height"]) * sy))
            if crop[2] > crop[0] and crop[3] > crop[1]:
                regions.append({"node_id": n["id"], "mean_absolute_rgb_error": round(sum(ImageStat.Stat(diff.crop(crop)).mean) / 3, 4)})
        out.append({"page_id": pid, "file": name, "left": "approved_target", "right": "actual_pptx_render",
                    "mean_absolute_rgb_error": round(sum(ImageStat.Stat(diff).mean) / 3, 4), "regions": regions,
                    "approval": "not_inferred_from_metric"})
    return out


def build(root, *, isolation="auto", preview=True, parent_build=None, require_os_isolation=False):
    requested_isolation = isolation
    isolation = select_isolation(isolation)
    with Store(root) as store:
        task = store.json("task.json")
        check = validate(task, complete=True)
        assets = read_assets(store, task)
        revision = 0
        if parent_build:
            parent = store.json(build_prefix(parent_build) + "manifest.json")
            if parent["task_id"] != task["task_id"]:
                raise DesignError("PARENT_TASK_MISMATCH")
            revision = parent["revision"] + 1
            if revision > task["design"]["revision_budget"]:
                raise DesignError("REVISION_BUDGET_EXHAUSTED: retain unresolved differences")
        bid = "build-" + uuid.uuid4().hex
        prefix = build_prefix(bid)
        store.put_json(prefix + "task.json", task, exclusive=True)
        for a in task["assets"]["items"]:
            store.write(prefix + "assets/" + a["sha256"] + ".png", assets[a["id"]])
        report = {"build_id": bid, "task_id": task["task_id"], "created_at": now(), "revision": revision,
                  "parent_build": parent_build, "inputs": versions(task), "environment": renderer_identity(),
                  "fonts": fonts_for(task),
                  "isolation": {"requested": requested_isolation, "mode": isolation, "verified": False},
                  "delivery_policy": {"require_os_isolation": bool(require_os_isolation)},
                  "validation": check, "status": "build_failed", "artifacts": {}}
        if task["design"].get("review_profile") or any("composition" in p for p in task["design"]["pages"]):
            report["composition_diagnostics"] = composition_diagnostics(task)
        try:
            if require_os_isolation and isolation == "host":
                raise DesignError("OS_ISOLATION_REQUIRED: no verified OS sandbox selected; worker was not started")
            launch_worker(store.root / prefix, isolation=isolation, preview=preview)
            report["isolation"]["verified"] = isolation == "macos"
            pptx = store.read(prefix + "deck.pptx")
            report["object_inspection"] = inspect_objects(pptx, task)
            report["render"] = store.json(prefix + "render.json")
            report["comparisons"] = comparisons(store, prefix, task, report["render"], assets)
            names = ["task.json", "deck.pptx", "objects.json", "render.json"]
            if report["render"]["status"] == "passed":
                names.append("deck.pdf")
                names.extend(p["file"] for p in report["render"]["pages"])
            names.extend(p["file"] for p in report["comparisons"])
            names.extend("assets/" + a["sha256"] + ".png" for a in task["assets"]["items"])
            report["artifacts"] = {n: digest(store.read(prefix + n)) for n in names}
            from .incremental import page_evidence
            report["page_evidence"] = page_evidence(task, report)
            previous = {}
            if parent_build:
                old_task = store.json(build_prefix(parent_build) + "task.json")
                previous = page_evidence(old_task, parent)
            report["changed_pages"] = [p["id"] for p in task["scene"]["pages"]
                                       if not report["page_evidence"].get(p["id"]) or
                                       report["page_evidence"].get(p["id"]) != previous.get(p["id"])]
            report["design_origins"] = [{"page_id": d["page_id"],
                                        "kind": "external_target" if d.get("target_asset_id") else "programmatic_preview",
                                        "target_asset_id": d.get("target_asset_id"),
                                        "scene_sha256": report["inputs"]["scene"]} for d in task["design"]["pages"]]
            report["status"] = "candidate_unreviewed" if report["render"]["status"] == "passed" else "render_incomplete"
            if task["mode"] == "draft":
                report["status"] = "draft"
        except (DesignError, OSError) as exc:
            report["error"] = str(exc)
        store.put_json(prefix + "manifest.json", report, exclusive=True)
        return report


def build_prefix(bid):
    if not re.fullmatch(r"build-[0-9a-f]{32}", bid):
        raise DesignError("INVALID_BUILD_ID")
    return "builds/" + bid + "/"


def verify_build(store, bid, *, snapshot=False):
    prefix = build_prefix(bid)
    manifest = store.json(prefix + "manifest.json")
    task = store.json(prefix + "task.json" if snapshot else "task.json")
    validate(task, complete=True)
    if manifest["inputs"] != versions(task):
        raise DesignError("REVIEW_STALE_INPUTS")
    read_assets(store, task)
    if manifest["environment"] != renderer_identity() or manifest["fonts"] != fonts_for(task):
        raise DesignError("REVIEW_STALE_RENDERER_OR_FONTS")
    for name, expected in manifest["artifacts"].items():
        if digest(store.read(prefix + name)) != expected:
            raise DesignError(f"REVIEW_STALE_ARTIFACT: {name}")
    if manifest["status"] not in {"candidate_unreviewed", "draft", "render_incomplete"}:
        raise DesignError("BUILD_NOT_REVIEWABLE")
    inspect_objects(store.read(prefix + "deck.pptx"), task)
    return task, manifest


REVIEW_SCHEMA = obj({
    "build_id": ID, "manifest_sha256": SHA,
    "reviewer": obj({"id": SHORT, "method": enum("human", "independent_multimodal"), "environment": SHORT}),
    "pages": arr(obj({"page_id": ID, "design": enum("pass", "revise", "reject"),
                      "reconstruction": enum("pass", "revise", "reject", "not_applicable"),
                      "content": enum("pass", "revise", "reject"), "editability": enum("pass", "revise", "reject"),
                      "fonts": enum("pass", "revise", "reject"), "observations": arr(SHORT, 50, 1),
                      "observed_node_ids": arr(ID, 500, 1), "accepted_differences": arr(SHORT, 50),
                      "inherited_from": obj({"build_id": ID, "manifest_sha256": SHA, "review_sha256": SHA})},
                     ["page_id", "design", "reconstruction", "content", "editability", "fonts", "observations",
                      "observed_node_ids", "accepted_differences"]), 60, 1),
    "target_software": obj({"name": SHORT, "version": SHORT, "status": enum("pass", "not_tested", "fail"),
                            "actions": arr(SHORT, 100)}),
    "deck_composition": obj({"status": enum("pass", "revise", "reject"),
                             "observations": arr(SHORT, 50, 1),
                             "reviewed_page_ids": arr(ID, 60, 1)}),
}, ["build_id", "manifest_sha256", "reviewer", "pages", "target_software"])


def review_skeleton(store, bid):
    task, manifest = verify_build(store, bid)
    result = {"build_id": bid, "manifest_sha256": digest(store.read(build_prefix(bid) + "manifest.json")),
            "reviewer": {"id": "REPLACE_WITH_INDEPENDENT_REVIEWER", "method": "human", "environment": "填写实际审阅环境"},
            "pages": [{"page_id": p["id"], **{k: "revise" for k in ("design", "content", "editability", "fonts")},
                       "reconstruction": "revise" if next(d for d in task["design"]["pages"] if d["page_id"] == p["id"]).get("target_asset_id") else "not_applicable",
                       "observations": [], "observed_node_ids": [], "accepted_differences": []} for p in task["scene"]["pages"]],
            "target_software": {"name": task["target_software"], "version": "待验证", "status": "not_tested", "actions": []}}
    if task["design"].get("review_profile") == "decorative_business":
        result["deck_composition"] = {"status": "revise", "observations": [], "reviewed_page_ids": []}
    return result


def assess(store, bid, review, *, require_os_isolation=False, snapshot=False, _chain=(), _cache=None):
    task, manifest = verify_build(store, bid, snapshot=snapshot)
    errors = list(Draft202012Validator(REVIEW_SCHEMA).iter_errors(review))
    if errors:
        location = "/".join(str(part) for part in errors[0].absolute_path) or "$"
        raise DesignError("REVIEW_SCHEMA_INVALID: " + location + ": " + errors[0].message[:300])
    if review["build_id"] != bid or review["manifest_sha256"] != digest(store.read(build_prefix(bid) + "manifest.json")):
        raise DesignError("REVIEW_STALE_MANIFEST")
    if review["reviewer"]["id"] in {task["author_id"], "REPLACE_WITH_INDEPENDENT_REVIEWER"}:
        raise DesignError("INDEPENDENT_REVIEW_REQUIRED")
    reviewed = {p["page_id"]: p for p in review["pages"]}
    pages = task["scene"]["pages"]
    if len(reviewed) != len(review["pages"]) or set(reviewed) != {p["id"] for p in pages}:
        raise DesignError("REVIEW_PAGE_COVERAGE_MISMATCH")
    from .incremental import verify_inheritance
    verify_inheritance(store, task, manifest, review, (*_chain, bid), {} if _cache is None else _cache)
    blockers = []
    deck = review.get("deck_composition")
    if task["design"].get("review_profile") == "decorative_business" and deck is None:
        blockers.append("DECK_COMPOSITION_REVIEW_REQUIRED")
    if deck is not None:
        if any(not observation.strip() for observation in deck["observations"]):
            raise DesignError("DECK_COMPOSITION_OBSERVATIONS_REQUIRED")
        page_ids = {p["id"] for p in pages}
        observed = deck["reviewed_page_ids"]
        if len(observed) != len(set(observed)) or set(observed) != page_ids:
            raise DesignError("DECK_COMPOSITION_PAGE_COVERAGE_MISMATCH")
        if deck["status"] != "pass":
            blockers.append("DECK_COMPOSITION_REVIEW_REQUIRED")
    if manifest["status"] == "draft":
        blockers.append("DRAFT_NOT_FINAL")
    if manifest["render"]["status"] != "passed":
        blockers.append("ACTUAL_RENDER_REQUIRED")
    # Old manifests keep their original strict policy. New builds bind their
    # explicit policy into the hash-reviewed manifest. Callers may strengthen it.
    strict = require_os_isolation or manifest.get("delivery_policy", {"require_os_isolation": True})["require_os_isolation"]
    isolation = manifest["isolation"]
    if isolation["mode"] not in {"host", "macos"} or (isolation["mode"] == "host" and isolation["verified"]):
        raise DesignError("ISOLATION_RECORD_INVALID")
    warnings = [] if isolation["verified"] else ["OS_ISOLATION_NOT_VERIFIED"]
    if strict and not isolation["verified"]:
        blockers.append("OS_ISOLATION_NOT_VERIFIED")
    if any(f["status"] != "matched" for f in manifest["fonts"]):
        blockers.append("FONT_ENVIRONMENT_UNRESOLVED")
    for page in pages:
        r = reviewed[page["id"]]
        design = next(d for d in task["design"]["pages"] if d["page_id"] == page["id"])
        if set(r["accepted_differences"]) != set(design["accepted_differences"]):
            blockers.append("DIFFERENCES_NOT_APPROVED_IN_DESIGN:" + page["id"])
        nodes = {n["id"] for n, *_ in walk(page["nodes"])}
        if not set(r["observed_node_ids"]) <= nodes:
            raise DesignError("REVIEW_UNKNOWN_OBJECT")
        # Each editable content object needs concrete review, not a page-count proxy.
        required = {n["id"] for n, *_ in walk(page["nodes"]) if n.get("content_id")}
        if not required <= set(r["observed_node_ids"]):
            blockers.append("OBJECT_REVIEW_INCOMPLETE:" + page["id"])
        for check in ("design", "reconstruction", "content", "editability", "fonts"):
            expected = "not_applicable" if check == "reconstruction" and not design.get("target_asset_id") else "pass"
            if r[check] != expected:
                blockers.append(check.upper() + "_REVIEW_REQUIRED:" + page["id"])
    target = review["target_software"]
    if target["name"] != task["target_software"] or target["status"] != "pass" or not target["actions"]:
        blockers.append("TARGET_SOFTWARE_EDIT_TEST_REQUIRED")
    return {"status": "final_delivery_ready" if not blockers else "revision_required", "build_id": bid,
            "blockers": blockers, "warnings": warnings,
            "execution": {"mode": isolation["mode"], "os_isolation_verified": isolation["verified"]},
            "delivery_policy": {"require_os_isolation": bool(strict)},
            "review_sha256": digest(canonical(review)), "checked_at": now()}


def deliver(store, bid, review, *, require_os_isolation=False):
    result = assess(store, bid, review, require_os_isolation=require_os_isolation)
    if result["blockers"]:
        return result
    task, manifest = verify_build(store, bid)
    prefix = build_prefix(bid)
    buf = io.BytesIO()
    with ZipFile(buf, "w", ZIP_DEFLATED) as z:
        for name in manifest["artifacts"]:
            z.writestr(name, store.read(prefix + name))
        originals = {a["original_sha256"] for a in task["assets"]["items"]}
        for sha in originals:
            z.writestr("originals/" + sha + ".image", store.read("originals/" + sha + ".image"))
        z.writestr("manifest.json", store.read(prefix + "manifest.json"))
        z.writestr("review.json", json_bytes(review))
        z.writestr("acceptance.json", json_bytes(result))
        from .incremental import archive_evidence
        archive_evidence(store, z, review)
        notes = ["# PPT Smith 交付说明", "", "预览来自交付 PPTX 的真实 LibreOffice 渲染。",
                 "目标软件：" + task["target_software"],
                 "运行模式：" + result["execution"]["mode"],
                 "OS 隔离：" + ("已验证" if result["execution"]["os_isolation_verified"] else "未验证；本地 host 执行，交付通过仅代表 PPT 质量验收通过"),
                 "强制 OS 隔离策略：" + str(result["delivery_policy"]["require_os_isolation"]),
                 "", "## 逐页对应与编辑边界", ""]
        for page, design in zip(task["scene"]["pages"], sorted(task["design"]["pages"], key=lambda d: next(i for i,p in enumerate(task["scene"]["pages"]) if p["id"] == d["page_id"]))):
            origin = design.get('target_asset_id', '程序设计预览；无外部还原目标，不声明复刻保真')
            notes.append(f"- {page['id']}：{origin}；质量限制 {design['quality_limits']}；已接受差异 {design['accepted_differences']}。")
            notes.extend(f"  - {n['id']}：{n['role']}" for n, *_ in walk(page["nodes"]))
        notes += ["", "图片仅可替换；不等于恢复内部文字、路径或图表数据。字体未嵌入，跨设备需复验。", "",
                  "平台安全审核和不同软件兼容性属于独立验证范围。"]
        z.writestr("交付说明.md", "\n".join(notes).encode("utf-8"))
    name = "deliveries/" + bid + ".zip"
    store.write(name, buf.getvalue(), exclusive=True)
    return {**result, "delivery": name, "sha256": digest(buf.getvalue())}
