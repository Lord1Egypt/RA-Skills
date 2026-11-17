#!/usr/bin/env python3
"""Persistent, scoped semantic onboarding: init → propose → apply → export.

v0.0.7：init 支持 --pack 冷启动模板包（把 starter_packs 的本体声明合并进模型再开会话）；
gap 增加 suggestion（候选项+依据，由宿主 Agent 生成、脚本存证）与 state_label（三态标签）；status/export 输出清零报告。"""
import argparse
import copy
import json
from pathlib import Path
import sys

from _contract import (digest, get_path, keys, load, now, object_digest,
                       ont_entity_id, relation_id, write)

COLLECTIONS = {"dataset": ("datasets", "name"), "metric": ("metrics", "id"),
               "relationship": ("relationships", "id"), "concept": ("concepts", "term"),
               "ontology_entity": ("ontology.entities", "name"),
               "ontology_relation": ("ontology.relations", "id")}


def target(model, scope, ref):
    if ref == "scope":
        return scope
    if ref == "model":
        return model
    kind, name = ref.split(":", 1)
    collection, key = COLLECTIONS[kind]
    matches = [obj for obj in get_path(model, collection)
               if obj.get(key) == name or (kind == 'ontology_entity' and obj.get('uid') == name)]
    if len(matches) != 1:
        raise ValueError(f"missing or ambiguous object {ref}")
    return matches[0]


def get_value(obj, prop):
    for part in prop.split("."):
        if not isinstance(obj, dict):
            return None
        obj = obj.get(part)
    return obj


def set_value(obj, prop, value):
    parts = prop.split(".")
    if any(not p or p.startswith("_") for p in parts) or parts[0] in {"id", "name", "term"}:
        raise ValueError("identity/private properties cannot be edited by a gap answer")
    for part in parts[:-1]:
        if part not in obj:
            obj[part] = {}
        if not isinstance(obj[part], dict):
            raise ValueError("property path is not an object")
        obj = obj[part]
    obj[parts[-1]] = value


def merge_packs(model, pack_paths):
    """冷启动：把模板包的本体声明合并进模型。按 uid/name/id 去重，已有对象不覆盖。"""
    applied = []
    for path in pack_paths:
        pack = load(path)
        meta = pack.get("pack") or {}
        ont = (pack.get("ontology") or {})
        if not isinstance(ont, dict) or not (ont.get("entities") or ont.get("relations")):
            raise ValueError(f"pack {path} 缺少 ontology.entities/relations")
        target_ont = model.setdefault("ontology", {})
        entities = target_ont.setdefault("entities", [])
        relations = target_ont.setdefault("relations", [])
        seen_ent = {ont_entity_id(e) for e in entities} | {e.get("name") for e in entities}
        seen_rel = {r.get("id") for r in relations if r.get("id")} | \
                   {f"{r.get('from')}->{r.get('to')}:{r.get('predicate')}" for r in relations}
        ent_added = rel_added = 0
        for e in ont.get("entities") or []:
            if e.get("name") in seen_ent or (e.get("uid") and e["uid"] in seen_ent):
                continue
            entities.append(copy.deepcopy(e))
            seen_ent.add(e.get("name"))
            if e.get("uid"):
                seen_ent.add(e["uid"])
            ent_added += 1
        for r in ont.get("relations") or []:
            rid = r.get("id") or f"{r.get('from')}->{r.get('to')}:{r.get('predicate')}"
            if rid in seen_rel:
                continue
            relations.append(copy.deepcopy(r))
            seen_rel.add(rid)
            rel_added += 1
        applied.append({"pack": str(path), "id": meta.get("id"), "name": meta.get("name"),
                        "entities_added": ent_added, "relations_added": rel_added})
    return applied


STATE_LABELS = {"pending": "[待确认]", "candidate": "[候选·推断]",
                "confirmed": "[已确认]", "deferred": "[暂缓]", "rejected": "[已否决]"}


def gap_view(gap):
    view = dict(gap)
    source, state = gap.get("source"), gap.get("state")
    if state == "candidate" and source == "supplied_input":
        view["state_label"] = "[候选·来自材料]"
    else:
        view["state_label"] = STATE_LABELS.get(state, f"[{state}]")
    if gap.get("candidate") is not None:
        view.setdefault("suggestion", {
            "value": gap["candidate"],
            "basis": "来自现有模型或输入材料；可原样采纳（confirmed + value=建议值），修改后采纳，或 rejected 并说明理由",
            "adopt_hint": "按 AI 建议：decision 填 state=confirmed、value=建议值、actor/role/basis 如实"})
    return view


def clearance(session):
    """待确认清零报告：发布前 pending/candidate 必须清零。"""
    counts = {}
    for g in session["gaps"]:
        counts[g["state"]] = counts.get(g["state"], 0) + 1
    outstanding = counts.get("pending", 0) + counts.get("candidate", 0)
    return {"counts": counts, "outstanding": outstanding,
            "ready_for_validation": outstanding == 0 and not blockers(session)}


def new_session(model, scope, source_hash, pack_paths=()):
    model, scope = copy.deepcopy(model), copy.deepcopy(scope)
    packs_applied = merge_packs(model, pack_paths) if pack_paths else []
    if not scope.get("id") or not scope.get("question") or not scope.get("datasets"):
        raise ValueError("scope requires id, question, datasets (explicit current use case)")
    for rel in model.get("relationships", []):
        rel.setdefault("id", relation_id(rel))
    requirements = []
    has_ontology = bool(model.get("ontology"))
    for name in scope["datasets"]:
        ref = "dataset:" + name
        ds = target(model, scope, ref)
        # 先业务后物理：先确认业务对象与属性，再谈表、键与粒度
        if has_ontology:
            if not ds.get("ontology_ref"):
                requirements.append({"object": ref, "property": "ontology_ref", "owner_role": "fde",
                                     "question": "该数据集承载哪个业务对象（ontology 实体）？没有对应实体请先在 ontology 段声明。"})
            else:
                try:
                    entity = target(model, scope, "ontology_entity:" + ds["ontology_ref"])
                    if not entity.get("attributes"):
                        requirements.append({"object": "ontology_entity:" + ds["ontology_ref"],
                                             "property": "attributes", "owner_role": "business_owner",
                                             "question": "该业务对象的关键业务属性（不依赖具体表）有哪些？给出 name、value_type 及含义。"})
                except ValueError:
                    pass  # 悬空 ontology_ref 由 check_model E14 报告
        for prop, role, question in [
            ("grain", "business_owner", "一行代表什么业务事实？"),
            ("primary_key", "data_owner", "哪个字段或复合键唯一标识该粒度？"),
            ("fields", "data_owner", "有哪些可提供字段？请给出 name、role 及已知含义。"),
            ("source", "data_owner", "已存在或待建设的物理表/视图是什么？"),
            ("temporal.kind", "data_owner", "是 current、event 还是 snapshot 数据？")]:
            if not get_value(ds, prop):
                requirements.append({"object": ref, "property": prop, "owner_role": role, "question": question})
    for mid in scope.get("metrics", []):
        ref = "metric:" + mid
        metric = target(model, scope, ref)
        for prop, role, question in [
            ("dataset", "fde", "指标从哪个已声明数据集计算？"),
            ("caliber.note", "business_owner", "计算范围、包含/排除、时间和单位口径是什么？"),
            ("unit", "business_owner", "结果单位是什么？百分比以小数还是百分数呈现？"),
            ("time_field", "business_owner", "指标使用哪个业务时间字段？")]:
            if prop == 'time_field' and (scope.get('time_requirement') or metric.get('time_requirement')) == 'current':
                continue  # 已明确只问当前状态；不能为了填表而制造时间字段。
            if not get_value(metric, prop):
                requirements.append({"object": ref, "property": prop, "owner_role": role, "question": question})
        if not metric.get("expr") and not (metric.get("numerator") and metric.get("denominator")):
            requirements.append({"object": ref, "property": "expr", "owner_role": "fde", "question": "按已确认口径，完整的单表计算表达式是什么？"})
    requirements.extend(scope.get("required", []))
    gaps = {}
    for requirement in requirements:
        ref, prop = requirement["object"], requirement["property"]
        obj = target(model, scope, ref)
        gid = "G-" + object_digest([scope["id"], ref, prop])[:12]
        candidate = requirement.get("candidate", get_value(obj, prop))
        gaps[gid] = {"id": gid, "object": ref, "property": prop,
                     "question": requirement["question"], "owner_role": requirement.get("owner_role", "business_owner"),
                     "blocking_use_cases": [scope["id"]], "state": "candidate" if candidate is not None else "pending",
                     "candidate": candidate, "evidence_refs": requirement.get("evidence_refs", []),
                     "source": "supplied_input" if candidate == get_value(obj, prop) else "proposal"}
    return {"schema_version": "1.0", "revision": 0, "created_at": now(),
            "source_model_sha256": source_hash, "model": model, "scope": scope,
            "packs_applied": packs_applied,
            "gaps": list(gaps.values()), "decisions": []}


def blockers(session):
    result = [{"id": g["id"], "detail": g["question"], "state": g["state"]}
              for g in session["gaps"] if g["state"] != "confirmed"]
    scope, model = session["scope"], session["model"]
    if scope.get("time_requirement") == "historical_as_of":
        for name in scope["datasets"]:
            ds = target(model, scope, "dataset:" + name)
            temporal = ds.get("temporal", {})
            if temporal.get("kind") not in {"event", "snapshot"} or not temporal.get("as_of_field"):
                result.append({"id": "history:" + name, "state": "blocked", "detail": "历史时点问题需要事件/快照及 as_of_field；现状字段不能证明过去事实"})
            elif temporal["as_of_field"] not in {f["name"] for f in ds.get("fields", [])}:
                result.append({"id": "history-field:" + name, "state": "blocked", "detail": "as_of_field 不在字段清单中"})
    return result


def proposal(session, answers):
    if answers.get("session_revision") != session["revision"]:
        raise ValueError(
            f"stale answers: answers 的 session_revision={answers.get('session_revision')!r} "
            f"与会话当前 revision={session['revision']} 不一致。"
            f"请先 guide_model.py status 查看当前 revision，"
            f"将其填入 answers 的 session_revision 字段后重试（防基于过期会话做决策）。")
    updated = copy.deepcopy(session)
    gaps = {g["id"]: g for g in updated["gaps"]}
    changes, seen = [], set()
    if not answers.get("decisions"):
        raise ValueError("no decisions supplied")
    for answer in answers["decisions"]:
        gid = answer["gap_id"]
        if gid in seen or gid not in gaps:
            raise ValueError("duplicate/unknown gap_id")
        seen.add(gid)
        gap = gaps[gid]
        state = answer.get("state")
        if state not in {"confirmed", "deferred", "rejected"}:
            raise ValueError("decision state must be confirmed/deferred/rejected")
        if not answer.get("actor") or not answer.get("basis") or answer.get("role") != gap["owner_role"]:
            raise ValueError("actor, basis and matching owner_role are required; authority must be checked by the operator")
        if gap["state"] == "confirmed" and answer.get("supersedes_revision") != gap.get("decision_revision"):
            raise ValueError("changing a confirmed answer requires supersedes_revision")
        if state == "confirmed":
            value = answer.get("value")
            if value is None or value == "" or value == [] or value == {}:
                raise ValueError("confirmed value cannot be empty")
            if gap["property"] == "temporal.kind" and value not in {"current", "event", "snapshot"}:
                raise ValueError("temporal.kind must be current/event/snapshot")
            obj = target(updated["model"], updated["scope"], gap["object"])
            changes.append({"object": gap["object"], "property": gap["property"],
                            "before": get_value(obj, gap["property"]), "after": value})
            set_value(obj, gap["property"], value)
        gap.update(state=state, decision_revision=session["revision"] + 1)
        updated["decisions"].append({**answer, "revision": session["revision"] + 1, "at": now()})
    updated["revision"] += 1
    return {"base_session_sha256": object_digest(session), "changes": changes,
            "answers": answers, "result_model_sha256": object_digest(updated["model"]),
            "remaining_blockers": blockers(updated)}


def apply_proposal(session, patch):
    patch_id = object_digest(patch)
    if patch_id in session.get("applied_patches", []):
        return session
    if object_digest(session) != patch["base_session_sha256"]:
        raise ValueError("stale patch: session changed; propose again")
    checked = proposal(session, patch["answers"])
    for key in ("changes", "result_model_sha256", "remaining_blockers"):
        if checked[key] != patch[key]:
            raise ValueError("patch differs from reviewed decisions")
    # Reconstruct from validated decisions, never trust an embedded replacement model.
    updated = copy.deepcopy(session)
    gap_index = {g["id"]: g for g in updated["gaps"]}
    for change in patch["changes"]:
        set_value(target(updated["model"], updated["scope"], change["object"]), change["property"], change["after"])
    updated["revision"] += 1
    for answer in patch["answers"]["decisions"]:
        gap_index[answer["gap_id"]].update(state=answer["state"], decision_revision=updated["revision"])
        updated["decisions"].append({**answer, "revision": updated["revision"], "at": now()})
    updated.setdefault("applied_patches", []).append(patch_id)
    return updated


def show(session):
    return {"revision": session["revision"], "scope": session["scope"]["id"],
            "status": "needs_input" if blockers(session) else "ready_for_validation",
            "clearance": clearance(session),
            "packs_applied": session.get("packs_applied", []),
            "blockers": blockers(session), "gaps": [gap_view(g) for g in session["gaps"]]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--model", required=True)
    init.add_argument("--scope", required=True)
    init.add_argument("--session", required=True)
    init.add_argument("--pack", action="append", default=[],
                      help="冷启动模板包（可重复）：先把 starter_packs 的本体声明合并进模型")
    status = sub.add_parser("status")
    status.add_argument("--session", required=True)
    propose = sub.add_parser("propose")
    propose.add_argument("--session", required=True)
    propose.add_argument("--answers", required=True)
    propose.add_argument("--patch", required=True)
    apply = sub.add_parser("apply")
    apply.add_argument("--session", required=True)
    apply.add_argument("--patch", required=True)
    export = sub.add_parser("export")
    export.add_argument("--session", required=True)
    export.add_argument("--out", required=True)
    args = ap.parse_args()
    try:
        if args.command == "init":
            if Path(args.session).exists():
                raise ValueError("session exists; resume it or use a new path")
            packs_dir = Path(__file__).resolve().parents[1] / "starter_packs"
            pack_paths = []
            for p in args.pack:
                cand = Path(p)
                if not cand.exists() and not cand.suffix:
                    alt = packs_dir / (p + ".yaml")
                    if alt.exists():
                        cand = alt
                if not cand.exists():
                    raise ValueError(f"pack 不存在：{p}（也不是 starter_packs/ 下的包名）")
                pack_paths.append(str(cand))
            session = new_session(load(args.model), load(args.scope), digest(args.model),
                                  pack_paths=pack_paths)
            write(args.session, session)
        else:
            session = load(args.session)
            if args.command == "propose":
                if Path(args.patch).resolve() == Path(args.session).resolve():
                    raise ValueError("patch must not overwrite session")
                write(args.patch, proposal(session, load(args.answers)))
            elif args.command == "apply":
                session = apply_proposal(session, load(args.patch))
                write(args.session, session)
            elif args.command == "export":
                output = Path(args.out)
                if output.exists() and any(output.iterdir()):
                    raise ValueError("export directory must be new or empty")
                write(output / "semantic.yaml", session["model"])
                write(output / "scope.json", session["scope"])
                write(output / "session.json", session)
                write(output / "gap-report.json", show(session))
                write(output / "manifest.json", {"contract": "ai-data-delivery/1.0", "status": "draft",
                      "model_version": session["model"].get("version"), "created_at": now(),
                      "scope": session["scope"]["id"], "validation": "not_run",
                      "files": [{"path": p.name, "sha256": digest(p)} for p in sorted(output.iterdir())]})
        print(json.dumps(show(session), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f"guide: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
