"""Question contracts, local review evidence and source-to-question impact.

These checks describe declared context, not a proof that a business answer is true.
"""
import copy
import hashlib
import json

from workbench.semantic_package import asset_dependencies


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def closure(sem, roots):
    index = {a["id"]: a for a in sem["assets"]}
    redirects = sem.get("redirects", {})
    paths, pending = {}, [(aid, [aid]) for aid in roots]
    while pending:
        raw, path = pending.pop(0)
        aid = redirects.get(raw, raw)
        if aid in paths:
            continue
        paths[aid] = path if raw == aid else path + [aid]
        if aid in index:
            pending.extend((ref, paths[aid] + [ref]) for ref in asset_dependencies(index[aid], include_execution=True))
    return paths


def validate_acceptance(value, known_ids):
    if not isinstance(value, dict) or set(value) - {"required_asset_ids", "required_gap_codes", "cases"}:
        raise ValueError("Invalid acceptance criteria / 验收条件格式无效")
    result = {"required_asset_ids": [], "required_gap_codes": [], "cases": [], **copy.deepcopy(value)}
    for key in ("required_asset_ids", "required_gap_codes"):
        items = result[key]
        if not isinstance(items, list) or len(items) > 200 or any(not isinstance(x, str) or not x.strip() for x in items):
            raise ValueError("Invalid acceptance list / 验收条件须为非空文字列表")
        result[key] = list(dict.fromkeys(items))
    if set(result["required_asset_ids"]) - set(known_ids):
        raise ValueError("Required definition is missing / 预期包含的定义不存在")
    cases = result["cases"]
    if not isinstance(cases, list) or len(cases) > 50:
        raise ValueError("At most 50 acceptance examples / 验收样例至多 50 项")
    seen = set()
    for case in cases:
        if not isinstance(case, dict) or set(case) != {"id", "expectation"}:
            raise ValueError("Each example needs an ID and expectation / 样例需要身份和预期")
        if not isinstance(case["id"], str) or not case["id"] or len(case["id"]) > 160 or case["id"] in seen:
            raise ValueError("Invalid or repeated example ID / 样例身份无效或重复")
        if not isinstance(case["expectation"], str) or not case["expectation"].strip() or len(case["expectation"]) > 4000:
            raise ValueError("Write an expected result / 请填写样例预期结果，至多 4000 字符")
        seen.add(case["id"])
    return result


def basis(scenario, sem, know):
    """Ignore unrelated edits and display titles; include dependency meaning and source heads."""
    ids = closure(sem, scenario["asset_ids"])
    assets = [a for a in sem["assets"] if a["id"] in ids]
    sources = {e.get("source_id") for a in assets for e in a.get("evidence", [])}
    heads = [{"id": s["id"], "revision": s["current_revision"],
              "sha256": s["revisions"][-1]["sha256"],
              "extraction": s["revisions"][-1].get("current_extraction")}
             for s in know["sources"] if s["id"] in sources]
    return fingerprint({"question": {k: scenario.get(k) for k in
        ("question", "intent", "asset_ids", "domain", "scope", "as_of", "acceptance", "acceptance_notes")},
        "assets": sorted(assets, key=lambda a: a["id"]), "sources": sorted(heads, key=lambda s: s["id"]),
        "paths": ids})


def acceptance_report(scenario, sem, know, reader):
    criteria = scenario.get("acceptance", {})
    current = basis(scenario, sem, know)
    context = reader.get("context", {})
    present = set(context.get("required_asset_ids", []))
    redirects = sem.get("redirects", {})
    codes = {g["code"] for g in context.get("gaps", [])}
    checks = [{"kind": "required_asset", "expected": aid,
               "status": "passed" if redirects.get(aid, aid) in present else "failed"}
              for aid in criteria.get("required_asset_ids", [])]
    checks += [{"kind": "required_gap", "expected": code,
                "status": "passed" if code in codes else "not_verified" if context.get("truncated") else "failed"}
               for code in criteria.get("required_gap_codes", [])]
    contract_status = "not_configured" if not checks else "failed" if any(x["status"] == "failed" for x in checks) else "not_verified" if not context.get("request_complete") or any(x["status"] == "not_verified" for x in checks) else "passed"
    records = know.get("assessments", [])
    cases = []
    for case in criteria.get("cases", []):
        record = next((r for r in reversed(records) if r["scenario_id"] == scenario["id"] and r["case_id"] == case["id"]), None)
        status = "not_verified" if not record else record["outcome"] if record["basis_fingerprint"] == current else "stale"
        cases.append({**copy.deepcopy(case), "status": status, "record": copy.deepcopy(record)})
    statuses = {c["status"] for c in cases}
    status = "failed" if "failed" in statuses or contract_status == "failed" else "stale" if "stale" in statuses else "recorded_pass" if cases and statuses == {"passed"} and contract_status in {"passed", "not_configured"} and context.get("request_complete") and reader.get("decision") != "needs_review" else "not_verified"
    return {"status": status, "notes": scenario.get("acceptance_notes", ""), "basis_fingerprint": current,
            "context_contract": {"status": contract_status, "checks": checks}, "cases": cases,
            "answer_verified": False, "authority": "local_operator_record_not_independent_certification"}


def change_event(before_sem, before_know, sem, know, revision, summary):
    before = {a["id"]: a for a in before_sem["assets"]}
    after = {a["id"]: a for a in sem["assets"]}
    changed = {aid for aid in before.keys() | after.keys() if fingerprint(before.get(aid)) != fingerprint(after.get(aid))}
    source_before = {s["id"]: s for s in before_know["sources"]}
    source_after = {s["id"]: s for s in know["sources"]}
    sources = {sid for sid in source_before.keys() | source_after.keys() if fingerprint(source_before.get(sid)) != fingerprint(source_after.get(sid))}
    redirected = {key for key in before_sem.get("redirects", {}).keys() | sem.get("redirects", {}).keys()
                  if before_sem.get("redirects", {}).get(key) != sem.get("redirects", {}).get(key)}
    touched = changed | redirected | {a["id"] for a in list(before.values()) + list(after.values())
                                     if any(e.get("source_id") in sources for e in a.get("evidence", []))}
    if not changed and not sources and not redirected:
        return None
    impacted = []
    for scenario in know["scenarios"]:
        paths = {**closure(before_sem, scenario["asset_ids"]), **closure(sem, scenario["asset_ids"])}
        hits = sorted(set(paths) & touched)
        if hits:
            impacted.append({"scenario_id": scenario["id"], "title": scenario["title"],
                             "paths": [paths[aid] for aid in hits], "status": "recheck_required"})
    return {"revision": revision, "action": summary, "changed_asset_ids": sorted(changed),
            "asset_changes": [{"id": aid, "name": (after.get(aid) or before[aid])["name"],
                "kind": "added" if aid not in before else "removed" if aid not in after else "updated",
                "fields": sorted(k for k in (before.get(aid, {}).keys() | after.get(aid, {}).keys())
                                 if k not in before.get(aid, {}) or k not in after.get(aid, {}) or
                                 fingerprint(before[aid][k]) != fingerprint(after[aid][k]))} for aid in sorted(changed)],
            "source_changes": [{"id": sid, "name": (source_after.get(sid) or source_before[sid])["name"],
                "from_revision": source_before.get(sid, {}).get("current_revision"),
                "to_revision": source_after.get(sid, {}).get("current_revision"),
                "from_extraction": (source_before.get(sid, {}).get("revisions") or [{}])[-1].get("current_extraction"),
                "to_extraction": (source_after.get(sid, {}).get("revisions") or [{}])[-1].get("current_extraction")}
                for sid in sorted(sources)],
            "source_ids": sorted(sources), "redirect_ids": sorted(redirected), "impacted_questions": impacted,
            "automatic_semantic_rewrite": False}
