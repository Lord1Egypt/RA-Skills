"""Three user intents; compact commands with complete on-disk evidence."""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from collections import Counter

from .authoring import AUTHOR_SCHEMA, apply_updates, compact, expand
from .contract import CONTENT, NODE, SCHEMA, validate, versions, walk
from .pipeline import (REVIEW_SCHEMA, assess, build, build_prefix, deliver, image_request,
                       ingest, new_task, read_assets, review_skeleton, verify_build)
from .runtime import execution_capabilities, find_tool, renderer_identity
from .store import DesignError, Store, canonical, digest, external_bytes, parse_json

ALIASES = {"new_design": "create", "style_transfer": "create"}
MODES = ("create", "recreate", "template", "new_design", "style_transfer", "draft")


def route(intent="auto", *, template=False, design_target=False, template_use="preserve"):
    if template_use not in {"preserve", "style"}:
        raise DesignError("UNKNOWN_TEMPLATE_USE")
    if template_use == "style" and not template:
        raise DesignError("TEMPLATE_STYLE_REQUIRES_TEMPLATE")
    preserve = template and template_use == "preserve"
    if preserve and design_target and intent == "auto":
        raise DesignError("ROUTE_CONFLICT: specify template preservation or image reconstruction")
    chosen = ALIASES.get(intent, intent)
    if chosen == "auto":
        chosen = "template" if preserve else "recreate" if design_target else "create"
    if template and template_use == "style" and chosen == "template":
        raise DesignError("ROUTE_CONFLICT: style reference does not preserve a native template")
    if preserve and chosen != "template":
        raise DesignError("ROUTE_CONFLICT: native preservation requires template; explicitly choose --template-use style for redesign")
    if chosen not in {"create", "recreate", "template"}:
        raise DesignError("UNKNOWN_USER_INTENT")
    return {"intent": chosen, "entrypoint": "engine design" if chosen != "template" else "engine strict-template",
            "guide": "references/routes/v4-template-route.md" if chosen == "template" else "references/declarative-design.md",
            "image_generation_required": False,
            "external_target_required": chosen == "recreate",
            "native_template_preservation": chosen == "template",
            "template_use": template_use if template else None,
            "style_reference_required": template and template_use == "style"}


def save_state(store, task, *, phase, manifest=None, review_file=None, report=None, delivery=None):
    state = {"task_id": task["task_id"], "mode": task["mode"], "phase": phase,
             "task_sha256": versions(task)["task"], "pages": len(task["scene"]["pages"]),
             "content_items": len(task["content"]["items"]), "task_file": "task.json",
             "next": "Review the actual output before delivery." if manifest else "Author, preflight, build, then review."}
    if manifest:
        state.update(build_id=manifest["build_id"], manifest=build_prefix(manifest["build_id"]) + "manifest.json")
    for key, value in (("review_file", review_file), ("report", report), ("delivery", delivery)):
        if value is not None:
            state[key] = value
    if delivery:
        state["next"] = "Delivery is ready at " + delivery
    elif phase == "final_delivery_ready":
        state["next"] = "Deliver this exact build with the recorded independent review."
    elif phase == "revision_required":
        state["next"] = "Read the report blockers, patch the affected content and rebuild."
    store.put_json("state.json", state)
    return state


def read_review(store, path):
    review = store.json(path)
    if isinstance(review, dict) and "assessment" in review and "review" in review:
        raise DesignError("REVIEW_INPUT_MUST_BE_RAW: use the original independent review JSON, "
                          "or save this report's review object to a new task-relative JSON file; "
                          "the assessment/report wrapper is not a review.")
    if not isinstance(review, dict) or "build_id" not in review:
        raise DesignError("REVIEW_INPUT_INVALID: provide an independent review JSON created from review-template.")
    return review


def build_summary(result):
    counts = Counter()
    for page in result.get("object_inspection", {}).get("pages", []):
        counts.update(page["objects"])
    changed = result.get("changed_pages", [])
    return {"status": result["status"], "build_id": result["build_id"],
            "manifest": build_prefix(result["build_id"]) + "manifest.json",
            "pptx": build_prefix(result["build_id"]) + "deck.pptx" if result.get("artifacts") else None,
            "pages": len(result.get("render", {}).get("pages", [])), "objects": dict(counts),
            "changed_page_count": len(changed), "changed_pages": changed[:8],
            "changed_pages_truncated": len(changed) > 8,
            "warnings_count": len(result.get("validation", {}).get("warnings", [])),
            "render": result.get("render", {}).get("status", "not_started"),
            "error": str(result.get("error") or result.get("render", {}).get("reason") or "")[:500] or None,
            "review": "independent_review_required", "os_isolation_verified": result["isolation"]["verified"]}


def context(task, page_id=None, section="content"):
    if not page_id:
        return {"task_id": task["task_id"], "mode": task["mode"], "task_sha256": versions(task)["task"],
                "audience": task["audience"], "language": task["language"], "canvas": task["canvas"],
                "brief": task["design"]["brief"],
                **({"review_profile": task["design"]["review_profile"]}
                   if "review_profile" in task["design"] else {}),
                "pages": [{"page_id": p["id"], "nodes": sum(1 for _ in walk(p["nodes"])),
                           "content_items": sum(c["page_id"] == p["id"] for c in task["content"]["items"])}
                          for p in task["scene"]["pages"]]}
    page = next((p for p in task["scene"]["pages"] if p["id"] == page_id), None)
    if not page:
        raise DesignError("UNKNOWN_PAGE")
    out = {"page_id": page_id, "task_sha256": versions(task)["task"]}
    if section in {"all", "content"}:
        out["content"] = [c for c in task["content"]["items"] if c["page_id"] == page_id]
        out["notes"] = [n for n in task["content"]["notes"] if n["page_id"] == page_id]
    if section in {"all", "scene"}:
        out["scene"] = page
    if section in {"all", "design"}:
        out["design"] = next(d for d in task["design"]["pages"] if d["page_id"] == page_id)
        out["references"] = [r for r in task["design"]["references"] if page_id in r["page_ids"]]
        out["assets"] = [a for a in task["assets"]["items"] if page_id in a["page_ids"]]
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(prog="engine design", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    schema = sub.add_parser("schema")
    schema.add_argument("--review", action="store_true", help="compatibility alias for --section review")
    schema.add_argument("--section", choices=["task", "review", "author", "node", "content"], default="task")
    schema.add_argument("--type", help="only return this node/content type, such as text or chart")
    caps = sub.add_parser("capabilities")
    caps.add_argument("--full", action="store_true")
    routing = sub.add_parser("route", help="choose create, recreate or template from input intent")
    routing.add_argument("--intent", choices=["auto", *MODES[:-1]], default="auto")
    routing.add_argument("--template", action="store_true")
    routing.add_argument("--template-use", choices=["preserve", "style"], default="preserve",
                         help="preserve native template, or explicitly permit a new design in its style")
    routing.add_argument("--design-target", action="store_true")
    init = sub.add_parser("init")
    init.add_argument("--task-dir", required=True)
    init.add_argument("--task-id", required=True)
    init.add_argument("--mode", choices=MODES, default="create")
    init.add_argument("--width", type=float, default=960, help="canvas width in points")
    init.add_argument("--height", type=float, default=540, help="canvas height in points")
    init.add_argument("--pages", type=int, default=1)
    init.add_argument("--author", default="host-model")
    init.add_argument("--audience", default="待填写")
    init.add_argument("--language", default="zh-CN")
    init.add_argument("--target-software", default="LibreOffice")
    init.add_argument("--review-profile", choices=["decorative_business"],
                      help="require page composition plans and an independent whole-deck review")
    commands = ("ingest", "crop", "validate", "image-request", "build", "status", "review-template",
                "review", "deliver", "author", "compact", "patch", "context", "inspect", "preflight", "freeze-target",
                "composition-check")
    for command in commands:
        p = sub.add_parser(command)
        p.add_argument("--task-dir", required=True)
        p.add_argument("--full", action="store_true", help="explicit detailed output; default feedback is compact")
        if command == "image-request":
            p.add_argument("--pages", help="comma-separated page IDs; default is all pages")
        if command == "freeze-target":
            p.add_argument("--page", required=True)
            p.add_argument("--asset-id", required=True)
            p.add_argument("--request-file", default="image-request.json")
            p.add_argument("--confirmed-by", required=True)
        if command in {"ingest", "crop"}:
            p.add_argument("--asset-id", required=True)
            p.add_argument("--pages", required=True)
            p.add_argument("--role", required=True, choices=["reference", "target", "photo", "illustration", "raster_data"])
            p.add_argument("--source", required=True)
            p.add_argument("--source-crop", nargs=4, type=int)
            if command == "ingest":
                p.add_argument("--file", required=True)
                p.add_argument("--tool-result")
            else:
                p.add_argument("--from-asset", required=True)
        if command in {"author", "patch"}:
            p.add_argument("--file", required=True, help="task-relative JSON input")
        if command in {"compact", "review-template"}:
            p.add_argument("--output", help="new task-relative output file (not overwritten)")
        if command == "validate":
            p.add_argument("--complete", action="store_true")
        if command in {"build", "preflight"}:
            p.add_argument("--isolation", choices=["auto", "macos", "host"], default="auto")
        if command == "build":
            p.add_argument("--no-preview", action="store_true")
            p.add_argument("--parent-build")
        if command in {"status", "review-template", "review", "deliver", "inspect"}:
            p.add_argument("--build-id", required=command != "status")
        if command == "review-template":
            p.add_argument("--inherit-from", help="task-relative previous independent review")
        if command in {"review", "deliver"}:
            p.add_argument("--review-file", required=True)
        if command in {"build", "review", "deliver"}:
            p.add_argument("--require-os-isolation", action="store_true")
        if command in {"context", "inspect"}:
            p.add_argument("--page", required=command == "inspect")
        if command == "context":
            p.add_argument("--section", choices=["content", "scene", "design", "all"], default="content")
    args = parser.parse_args(argv)
    try:
        if args.command == "schema":
            result = {"task": SCHEMA, "review": REVIEW_SCHEMA, "author": AUTHOR_SCHEMA,
                      "node": NODE, "content": CONTENT}["review" if args.review else args.section]
            if args.type:
                if args.section not in {"node", "content"} or args.review:
                    raise DesignError("SCHEMA_TYPE_REQUIRES_NODE_OR_CONTENT_SECTION")
                result = next((v for v in result["oneOf"] if v["properties"]["type"]["const"] == args.type), None)
                if result is None:
                    raise DesignError("UNKNOWN_SCHEMA_TYPE")
            if args.section == "node" and not args.review:
                result = {**result, "$defs": SCHEMA["$defs"]} if not args.type or args.type == "group" else result
        elif args.command == "route":
            result = route(args.intent, template=args.template, design_target=args.design_target,
                           template_use=args.template_use)
        elif args.command == "capabilities":
            identity = renderer_identity()
            result = {"backend": identity if args.full else {"dependencies": identity["dependencies"],
                                                            "renderer_sha256": digest(canonical(identity))},
                      "intents": ["create", "recreate", "template"],
                      "image_generation": "optional_host_tool", "programmatic_preview": "native_pptx_to_png",
                      "reference_analysis": "host_vision_or_human_required",
                      "model_capabilities": "host_declared_not_detectable_by_local_cli",
                      "render": {x: bool(find_tool(x)) for x in ("soffice", "pdftoppm", "fc-match", "pdffonts", "pdftotext")},
                      "execution": execution_capabilities(), "automatic_visual_approval": False}
        elif args.command == "init":
            mode = ALIASES.get(args.mode, args.mode)
            if mode == "template":
                raise DesignError("TEMPLATE_ROUTE_REQUIRED: see references/routes/v4-template-route.md")
            task = new_task(args.task_id, mode=mode, width=args.width, height=args.height, pages=args.pages,
                            author=args.author, audience=args.audience, language=args.language, target_software=args.target_software)
            if args.mode == "style_transfer":
                task["design"]["requires_style_reference"] = True
            if args.review_profile:
                task["design"]["review_profile"] = args.review_profile
            with Store(args.task_dir, create=True) as store:
                store.put_json("task.json", task, exclusive=True)
                result = save_state(store, task, phase="preparation_required")
                result["status"] = "preparation_required"
                if args.mode in ALIASES:
                    result["compatibility_alias"] = args.mode
                    result["style_reference"] = "Register the requested style reference." if args.mode == "style_transfer" else "optional"
        elif args.command == "build":
            manifest = build(args.task_dir, isolation=args.isolation, preview=not args.no_preview,
                             parent_build=args.parent_build, require_os_isolation=args.require_os_isolation)
            with Store(args.task_dir) as store:
                save_state(store, store.json("task.json"), phase=manifest["status"], manifest=manifest)
            result = manifest if args.full else build_summary(manifest)
        elif args.command == "preflight":
            from .preflight import preflight
            report = preflight(args.task_dir, isolation=args.isolation)
            result = report if args.full else {k: report[k] for k in ("status", "cache_hit", "report", "missing_tools", "scope") if k in report}
            if not args.full:
                result.update(faces=len(report.get("samples", [])),
                              flagged_faces=sum(s["status"] != "passed" for s in report.get("samples", [])))
        else:
            with Store(args.task_dir) as store:
                task = store.json("task.json")
                if args.command in {"ingest", "crop"}:
                    if args.command == "ingest":
                        data = external_bytes(args.file)
                        receipt = parse_json(external_bytes(args.tool_result, 65536)) if args.tool_result else None
                    else:
                        validate(task)
                        data = read_assets(store, task).get(args.from_asset)
                        if data is None or args.source_crop is None:
                            raise DesignError("REGISTERED_SOURCE_AND_CROP_REQUIRED")
                        receipt = None
                    result = ingest(store, task, asset_id=args.asset_id, data=data, page_ids=args.pages.split(","),
                                    role=args.role, source=args.source, crop=args.source_crop, tool_result=receipt)
                    save_state(store, store.json("task.json"), phase="authoring_required")
                elif args.command == "author":
                    document = store.json(args.file)
                    candidate = expand(document)
                    if (any(candidate[k] != task[k] for k in ("task_id", "author_id", "mode")) or
                            task["design"].get("requires_style_reference") and not candidate["design"].get("requires_style_reference")):
                        raise DesignError("AUTHOR_TASK_IDENTITY_MISMATCH")
                    if (task["design"].get("review_profile") and
                            candidate["design"].get("review_profile") != task["design"]["review_profile"]):
                        raise DesignError("AUTHOR_REVIEW_PROFILE_DOWNGRADE")
                    read_assets(store, candidate)
                    source = "author-inputs/" + digest(canonical(document)) + ".json"
                    store.put_json(source, document)
                    store.put_json("task.json", candidate)
                    save_state(store, candidate, phase="authored")
                    result = {"status": "authored", "task_sha256": versions(candidate)["task"], "author_input": source,
                              "compact_bytes": len(canonical(document)), "expanded_bytes": len(canonical(candidate))}
                elif args.command == "compact":
                    document = compact(task)
                    output = args.output or "author-" + versions(task)["task"][:12] + ".json"
                    store.put_json(output, document, exclusive=True)
                    result = {"status": "compact_author_input_ready", "file": output, "roundtrip": "exact",
                              "compact_bytes": len(canonical(document)), "expanded_bytes": len(canonical(task))}
                elif args.command == "patch":
                    patch = store.json(args.file)
                    candidate, affected = apply_updates(task, patch)
                    read_assets(store, candidate)
                    store.put_json("history/" + versions(task)["task"] + ".json", task)
                    store.put_json("history/patch-" + digest(canonical(patch)) + ".json", patch)
                    store.put_json("task.json", candidate)
                    save_state(store, candidate, phase="revision_requires_build")
                    result = {"status": "patched", "task_sha256": versions(candidate)["task"],
                              "affected_page_count": len(affected), "affected_pages": affected[:8],
                              "next": "Build with --parent-build; existing reviews remain stale."}
                elif args.command == "context":
                    result = context(task, args.page, args.section)
                elif args.command == "composition-check":
                    from .composition import composition_diagnostics
                    validate(task)
                    result = composition_diagnostics(task)
                elif args.command == "validate":
                    result = validate(task, complete=args.complete)
                    read_assets(store, task)
                elif args.command == "image-request":
                    request = image_request(task, page_ids=args.pages.split(",") if args.pages else None)
                    store.put_json("image-request.json", request)
                    result = request if args.full else {"status": request["status"], "file": "image-request.json", "generated": False}
                elif args.command == "freeze-target":
                    from .targets import freeze_generated_target
                    candidate = freeze_generated_target(task, store.json(args.request_file), page_id=args.page,
                                                        asset_id=args.asset_id, confirmed_by=args.confirmed_by)
                    read_assets(store, candidate)
                    store.put_json("history/" + versions(task)["task"] + ".json", task)
                    store.put_json("task.json", candidate)
                    save_state(store, candidate, phase="target_confirmed_requires_build")
                    result = {"status": "target_confirmed_requires_build", "page_id": args.page,
                              "target_asset_id": args.asset_id, "independent_review_required": True}
                elif args.command == "status":
                    if not args.build_id:
                        result = context(task)
                    else:
                        _, manifest = verify_build(store, args.build_id)
                        result = manifest if args.full else build_summary(manifest)
                elif args.command == "inspect":
                    frozen, manifest = verify_build(store, args.build_id)
                    result = context(frozen, args.page, "all")
                    result["objects"] = next(p for p in manifest["object_inspection"]["pages"] if p["page_id"] == args.page)
                    result["preview"] = next((p for p in manifest["render"]["pages"] if p["page_id"] == args.page), None)
                    result["comparison"] = next((p for p in manifest["comparisons"] if p["page_id"] == args.page), None)
                elif args.command == "review-template":
                    draft = review_skeleton(store, args.build_id)
                    inherited = []
                    if args.inherit_from:
                        from .incremental import prepare_inheritance
                        frozen, manifest = verify_build(store, args.build_id)
                        inherited = prepare_inheritance(store, frozen, manifest, draft, read_review(store, args.inherit_from))
                    output = args.output or "review-draft-" + args.build_id[-8:] + ".json"
                    store.put_json(output, draft, exclusive=True)
                    result = draft if args.full else {"status": "independent_review_required", "file": output,
                                                      "inherited_page_count": len(inherited), "inherited_pages": inherited[:8],
                                                      "pages_requiring_review": [p["page_id"] for p in draft["pages"]
                                                                                 if p["page_id"] not in inherited][:8]}
                else:
                    review = read_review(store, args.review_file)
                    operation = deliver if args.command == "deliver" else assess
                    result = operation(store, args.build_id, review, require_os_isolation=args.require_os_isolation)
                    path = "reviews/" + args.build_id + "-" + uuid.uuid4().hex + ".json"
                    store.put_json(path, {"assessment": result, "review": review}, exclusive=True)
                    if not args.full:
                        result = {**result, "report": path, "blocker_count": len(result["blockers"]),
                                  "blockers": result["blockers"][:8]}
                    save_state(store, task, phase=result["status"],
                               manifest=store.json(build_prefix(args.build_id) + "manifest.json"),
                               review_file=args.review_file, report=path, delivery=result.get("delivery"))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get("status") in {"build_failed", "render_incomplete", "revision_required",
                                             "font_review_required", "preflight_unavailable"} else 0
    except (DesignError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)[:1400]}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
