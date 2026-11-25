"""Deterministic question handoff derived from canonical semantic assets.

This offline control never grants runtime permission or invents a query plan.
"""
import copy
import hashlib
import json


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def plan_dependencies(plan):
    """Declared references only, shared by authoring, impact and package closure."""
    if not isinstance(plan, dict):
        raise ValueError("query_plan must be an object")
    ids = []
    for key in ("dataset_id",):
        if key in plan:
            if not isinstance(plan[key], str) or not plan[key]:
                raise ValueError(key + " must be a stable ID")
            ids.append(plan[key])
    for key in ("column_ids", "grain_ids", "relation_ids", "mapping_ids", "rule_ids"):
        values = plan.get(key, [])
        if not isinstance(values, list) or any(not isinstance(x, str) or not x for x in values):
            raise ValueError(key + " must be stable IDs")
        ids.extend(values)
    filters = plan.get("filters", [])
    if not isinstance(filters, list) or any(not isinstance(f, dict) for f in filters):
        raise ValueError("filters must be objects")
    aggregation = plan.get("aggregation", {})
    if not isinstance(aggregation, dict):
        raise ValueError("aggregation must be an object")
    for item in filters + [aggregation]:
        if "field_id" in item:
            if not isinstance(item["field_id"], str) or not item["field_id"]:
                raise ValueError("field_id must be a stable ID")
            ids.append(item["field_id"])
    return list(dict.fromkeys(ids))


def redirect_plan(plan, removed, survivor):
    """Rewrite declared identity references after an explicit same-kind merge."""
    if plan.get("dataset_id") == removed:
        plan["dataset_id"] = survivor
    for key in ("column_ids", "grain_ids", "relation_ids", "mapping_ids", "rule_ids"):
        if key in plan:
            plan[key] = list(dict.fromkeys(survivor if x == removed else x for x in plan[key]))
    for binding in plan.get("filters", []) + [plan.get("aggregation", {})]:
        if binding.get("field_id") == removed:
            binding["field_id"] = survivor


def derive_control(package, *, preview=False):
    """No source/model/task text can set executable, freshness or authorization."""
    task = package.task_record["request"]
    blockers, gaps = [], []
    def block(code, message, **values):
        item = {"code": code, "message": message, **values}
        if item not in blockers:
            blockers.append(item)
    roots = [package._resolve(aid) for aid in task["asset_ids"]]
    assets, seen_gaps, offset = [], set(), 0
    while True:
        context = package.context(roots, intent=task["intent"], as_of=task.get("as_of"),
                                  limit=500, offset=offset, detail="summary")
        assets.extend(context["assets"])
        for gap in context.get("gaps", []):
            if gap["code"] == "CONTEXT_TRUNCATED":
                continue
            key = digest(gap)
            if key not in seen_gaps:
                gaps.append(gap); seen_gaps.add(key)
        if context.get("next_offset") is None:
            break
        offset = context["next_offset"]
    index = {a["id"]: package.index[a["id"]] for a in assets}
    candidates = [a for a in index.values() if "query_plan" in a.get("properties", {})]
    plans = [a for a in candidates if a["id"] in roots and a["kind"] == "metric"]
    plan = None
    owner = None
    if task["intent"] != "explain":
        if len(plans) != 1:
            block("NO_PLAN" if not plans else "AMBIGUOUS_PLAN", "Select exactly one metric with a reviewed query_plan / 请明确一个带查询约定的指标")
        else:
            owner = plans[0]
            plan = copy.deepcopy(owner["properties"]["query_plan"])
            _check_plan(plan, owner, index, package, block)
        if package.manifest["draft"] and not preview:
            block("DRAFT_PACKAGE", "Draft knowledge cannot authorize execution / 草稿不可作为执行依据")
        for gap in gaps:
            if gap["code"] not in {"NO_DATA_CONNECTOR", "NO_ACTION_EXECUTOR"}:
                block("KNOWLEDGE_GAP", gap.get("message", gap["code"]), gap=gap)
        # A static endpoint ID, even in confirmed source text, is not an executor handshake.
        block("NO_EXECUTOR", "No runtime authorization or executor is bound / 尚无已验证的执行器与运行时授权")
        block("FRESHNESS_UNVERIFIED", "Offline files cannot prove current definitions or catalog / 离线包无法证明口径与目录仍为最新")
        if task["intent"] == "act":
            block("ACTION_UNSUPPORTED", "Query control does not authorize business actions / 问数控制单不授权业务操作")
    columns = []
    for aid in plan.get("column_ids", []) if isinstance(plan, dict) else []:
        resolved = package.redirects.get(aid, aid)
        asset = index.get(resolved)
        if asset:
            columns.append({"field_id": resolved, "name": asset["name"],
                            "column": asset.get("properties", {}).get("column"),
                            "value_type": asset.get("properties", {}).get("value_type")})
    result = {"format_version": "query-control/1.0", "snapshot_id": package.manifest["snapshot_id"],
        "model_sha256": package.manifest["model_sha256"], "task_sha256": digest(package.task_record),
        "scenario_id": task["id"], "question": task["question"], "intent": task["intent"],
        "as_of": task.get("as_of"), "scope": copy.deepcopy(task["scope"]), "root_ids": roots,
        "required_asset_ids": sorted(index), "metric_id": owner["id"] if owner else None,
        "plan": plan, "column_bindings": columns,
        "rules": [{"asset_id": a["id"], "condition": a.get("properties", {}).get("condition"),
                   "requirement": a.get("properties", {}).get("requirement")} for a in index.values() if a["kind"] == "rule"],
        "decision": "explain_only" if task["intent"] == "explain" else "blocked",
        "plan_status": "not_requested" if task["intent"] == "explain" else "incomplete" if any(b["code"] not in {"NO_EXECUTOR", "FRESHNESS_UNVERIFIED"} for b in blockers) else "declared",
        "blockers": blockers, "gaps": gaps, "freshness": "unknown_offline", "executor": None,
        "answer_verified": False, "question_coverage": "not_verified", "authorization_granted": False,
        "boundary": "A reviewed plan is not runtime permission. Never infer joins, SQL, freshness or missing facts from this file."}
    result["control_sha256"] = digest(result)
    return result


def _check_plan(plan, owner, index, package, block):
    required = {"dataset_id", "column_ids", "grain_ids", "relation_ids", "mapping_ids", "rule_ids",
                "aggregation", "filters", "null_policy", "time_scope", "semantic_fingerprint"}
    if not isinstance(plan, dict) or set(plan) != required:
        block("INVALID_PLAN", "Query plan fields are incomplete or unsupported / 查询约定字段不完整或含未支持项")
        return
    def get(aid, kind):
        asset = index.get(package.redirects.get(aid, aid)) if isinstance(aid, str) else None
        if not asset or asset["kind"] != kind or asset["status"] != "confirmed":
            block("UNCONFIRMED_BINDING", "Binding must reference a confirmed definition of the expected kind / 绑定须引用已确认的对应类型定义", asset_id=aid)
            return None
        return asset
    dataset = get(plan["dataset_id"], "dataset")
    columns = plan["column_ids"]
    if not columns or len(columns) != len(set(columns)):
        block("COLUMNS_NOT_IN_SCOPE", "Explicit nonduplicate column IDs required / 请明确字段名单")
    if not plan["grain_ids"] or not set(plan["grain_ids"]) <= set(columns):
        block("GRAIN_UNBOUND", "Grain must reference selected fields / 粒度须绑定所选字段")
    for aid in columns:
        field = get(aid, "field")
        if field and not isinstance(field.get("properties", {}).get("column"), str):
            block("PHYSICAL_COLUMN_MISSING", "Physical column name is not declared / 尚未声明物理列名", asset_id=aid)
        if field and dataset and dataset["id"] not in [package.redirects.get(x, x) for x in field.get("refs", [])]:
            block("FIELD_DATASET_MISMATCH", "Field is not explicitly attached to this dataset / 字段未明确属于本数据集", asset_id=aid)
    for key, kind in (("rule_ids", "rule"), ("mapping_ids", "mapping"), ("relation_ids", "relation")):
        for aid in plan[key]:
            bound = get(aid, kind)
            if bound and kind == "mapping" and dataset:
                ends = [package.redirects.get(bound.get(k), bound.get(k)) for k in ("from", "to")]
                if dataset["id"] not in ends:
                    block("MAPPING_DATASET_MISMATCH", "Selected mapping must reference this dataset / 所选映射须关联本数据集", asset_id=aid)
                if bound.get("properties", {}).get("strength") == "weak":
                    block("WEAK_MAPPING", "Weak mappings are not query bindings / 弱映射不可充当查询绑定", asset_id=aid)
    if not plan["mapping_ids"]:
        block("NO_MAPPING", "Business-to-data mapping is not selected / 尚未选择业务到数据的映射")
    # Relations are retained for review, never silently compiled into joins.
    if plan["relation_ids"]:
        block("PATH_NOT_EXECUTION_VALIDATED", "Selected relations are descriptive; join keys and fanout are not validated / 已选关系仅供核对，连接键与重复放大尚未验证")
    aggregation = plan["aggregation"]
    if set(aggregation) != {"function", "field_id"} or not isinstance(aggregation.get("function"), str) or aggregation.get("function") not in {"count_distinct", "count", "sum", "min", "max"} or aggregation.get("field_id") not in columns:
        block("AGGREGATION_UNBOUND", "Unsupported or unbound aggregation / 聚合函数或字段未绑定")
    for f in plan["filters"]:
        if set(f) != {"field_id", "op", "value"} or f.get("field_id") not in columns or not isinstance(f.get("op"), str) or f.get("op") not in {"eq", "ne", "gt", "gte", "lt", "lte", "is_null", "not_null"} or isinstance(f.get("value"), (list, dict)):
            block("FILTER_UNBOUND", "Filter must bind one selected field, operator and scalar / 过滤须绑定字段、运算符与单值")
        elif (f["op"] in {"is_null", "not_null"}) != (f["value"] is None):
            block("NULL_FILTER_AMBIGUOUS", "Use explicit null operators / NULL 须使用明确空值运算符")
    if not isinstance(plan["null_policy"], str) or plan["null_policy"] not in {"exclude", "preserve"}:
        block("NULL_POLICY_MISSING", "Explicit NULL behavior is required / 请明确空值处理")
    if not isinstance(plan["time_scope"], str) or not plan["time_scope"].strip() or plan["time_scope"] != owner["properties"].get("time_scope"):
        block("TIME_SCOPE_MISMATCH", "Data window must match reviewed metric scope / 数据时间范围须与指标一致")
    if plan["semantic_fingerprint"] != semantic_fingerprint(owner):
        block("PLAN_REVIEW_STALE", "Meaning changed since plan alignment was recorded / 指标口径已变化，请重新核对绑定")


def semantic_fingerprint(asset):
    """Change detection only, never automatic proof of text-to-plan equivalence."""
    return digest({"definition": asset.get("definition"), "scope": asset.get("scope"),
        "properties": {k: v for k, v in asset.get("properties", {}).items() if k != "query_plan"}})
