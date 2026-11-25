"""Catalog observations use the canonical graph, existing candidate review and question contracts."""
import copy
import json

from workbench.db_metadata import capture, classify, profile
from workbench.knowledge import containers, dependencies, find, meaningful, normalize_asset, uid, mark_dependents, seed_physical_drafts
from workbench.scenario_contract import basis, closure
from workbench.store import Conflict, digest, now


def asset_id(connection_id, table, column=None, fk=None):
    return "meta_" + digest([connection_id, table, column, fk])[:24]


def _objects(conn, table):
    name = table["name"]
    dataset = asset_id(conn["id"], name)
    prefix = conn["name"] + " / " + table["schema"] + "." + name
    common = {"domain": "Database structure / 数据库结构", "scope": {"connection": conn["id"], "schema": table["schema"], "table": name}, "aliases": []}
    result = [{**common, "id": dataset, "kind": "dataset", "name": prefix,
        "definition": "Observed physical table; no business ownership inferred / 已观察的物理表，不推断业务所有权",
        "refs": [], "properties": {"metadata_connection": conn["id"], "metadata_table": name,
            "primary_key": table["primary_key"], "catalog": {k: v for k, v in table.items() if k != "columns"}}}]
    for col in table["columns"]:
        result.append({**common, "id": asset_id(conn["id"], name, col["name"]), "kind": "field", "name": prefix + "." + col["name"],
            "definition": "Observed physical column / 已观察的物理字段: " + col["name"], "refs": [dataset],
            "properties": {"value_type": col["type"], "column": col["name"], "metadata_connection": conn["id"], "metadata_table": name, "catalog": col}})
    for fk in table["foreign_keys"]:
        # Selected scope never silently expands to other tables or schemas.
        target = fk["to_table"]
        same_schema = fk["to_schema"] == table["schema"]
        if target not in conn["tables"] or not same_schema or not all(fk["to_fields"]):
            result[0]["properties"].setdefault("knowledge_gaps", []).append("Foreign-key target requires explicit scope/column review / 外键目标需要明确范围或字段核对: " + target)
            continue
        result.append({**common, "id": asset_id(conn["id"], name, fk=[fk["from_fields"], target, fk["to_fields"]]),
            "kind": "relation", "name": prefix + " → " + target + " (" + ",".join(fk["from_fields"]) + ")",
            "definition": "Catalog foreign key; physical reference only / 目录声明的外键，仅表示物理引用", "refs": [],
            "from": dataset, "to": asset_id(conn["id"], target), "predicate": "foreign key / 外键", "relation_type": "physical_fk",
            "properties": {"metadata_connection": conn["id"], "metadata_table": name, "from_fields": fk["from_fields"], "to_fields": fk["to_fields"]}})
    return result


def _source(know, conn, name, table):
    sources = conn.setdefault("source_ids", {})
    if name not in sources:
        sources[name] = uid("src")
        know["sources"].append({"id": sources[name], "name": conn["name"] + " / " + name + ".catalog.json", "format": "metadata",
            "domain": "Database structure / 数据库结构", "scope": {"connection": conn["id"], "table": name}, "current_revision": 0, "revisions": []})
    source = find(know["sources"], sources[name])
    text = json.dumps({"table": name, "observation": table, "business_rows_read": 0}, ensure_ascii=False, sort_keys=True)
    fragment = {"id": "f_" + digest(text)[:24], "text": text, "location": {"type": "catalog", "table": name}}
    parsed = {"format": "metadata", "status": "complete", "warnings": [], "fragments": [fragment], "structure": {"parser_version": "metadata/1"}}
    number = source["current_revision"] + 1
    extraction = "extract_" + digest(parsed)[:20]
    source["revisions"].append({"revision": number, "sha256": digest(text), "created": now(), "parsed": parsed,
                               "current_extraction": extraction, "extractions": [{"id": extraction, "parsed": parsed}]})
    source["current_revision"] = number
    return {"source_id": source["id"], "revision": number, "extraction_id": extraction}, [
        {"source_id": source["id"], "revision": number, "extraction_id": extraction, "fragment_id": fragment["id"], "quote": text}]


class MetadataService:
    def __init__(self, knowledge):
        self.knowledge = knowledge

    def connect(self, req):
        def apply(doc, sem, know, db):
            config = profile(req.get("connection"))
            if config.get("id"):
                raise ValueError("Create a new connection for a different endpoint or scope / 更换地址或选表范围请新建连接，避免身份串接")
            if config["engine"] == "sqlite" and config["path"] == str(self.knowledge.store.path.resolve()):
                raise ValueError("Do not connect the workbench's own project database / 不可把工作台项目库当作业务来源")
            conn = {**config, "id": uid("connection"), "created": now(), "dirty_asset_ids": [], "projected": {}, "asset_tables": {}}
            know.setdefault("connections", []).append(conn)
            return {"connection": conn, "connected": False, "next_step": "Scan metadata / 读取元数据"}
        return self.knowledge._write(req, "登记只读元数据连接", apply)

    def scan(self, req):
        def apply(doc, sem, know, db):
            if type(req.get("seed_draft", False)) is not bool:
                raise ValueError("seed_draft must be boolean")
            if req.get("seed_draft") and sem["assets"]:
                raise ValueError("Draft initialization requires an empty graph / 初始草稿仅用于空图；已有模型请按候选核对变化")
            conn = find(know.get("connections", []), req.get("connection_id"), "连接")
            observed = capture({k: v for k, v in conn.items() if k in {"id", "name", "engine", "path", "host", "port", "database", "schema", "user", "password_env", "tls_ca", "tables", "auto_indexes"}})
            if self.knowledge.progress:
                self.knowledge.progress("catalog_observed", selected=len(conn["tables"]), business_rows_read=0)
            previous = conn.get("snapshot")
            if type(req.get("refresh_review", False)) is not bool:
                raise ValueError("refresh_review must be boolean / 重新生成候选须为开关")
            if previous and previous["fingerprint"] == observed["fingerprint"] and not req.get("refresh_review") and not req.get("seed_draft"):
                return {"status": "unchanged", "connection_id": conn["id"], "fingerprint": observed["fingerprint"], "business_rows_read": 0}
            if not previous and any(t is None for t in observed["tables"].values()):
                raise ValueError("Initial selected tables are missing or invisible; check exact names and permissions / 首次选表存在缺失或不可见项，请核对名称和权限")
            scan = {"id": uid("scan"), "connection_id": conn["id"], "created": now(), "fingerprint": observed["fingerprint"],
                    "changes": [], "group_ids": [], "automatic_asset_ids": [], "changed_asset_ids": [], "affected_questions": [], "business_rows_read": 0}
            candidates, source_refs = [], []
            current = {a["id"]: a for a in sem["assets"]}
            unresolved = [g for g in know["groups"] if g.get("metadata_connection") == conn["id"] and not g.get("superseded_by") and g["status"] != "accepted"]
            hold_proposals = any(g['status'] == 'rejected' for g in unresolved) and not req.get('refresh_review')
            scan['requires_explicit_refresh'] = bool(hold_proposals)
            carry = {conn["asset_tables"][c["target_id"]] for g in unresolved for c in g["candidates"] if c["target_id"] in conn["asset_tables"]}
            if req.get('refresh_review'):
                carry.update(conn['asset_tables'][aid] for aid in conn['dirty_asset_ids'] if aid in conn['asset_tables'])
            for name, table in observed["tables"].items():
                old = previous["tables"].get(name) if previous else None
                if previous and digest(old) == digest(table) and name not in carry:
                    continue
                code, equivalent = classify(old, table)
                old_ids = {aid for aid, tab in conn["asset_tables"].items() if tab == name and aid in current}
                ref, evidence = _source(know, conn, name, table)
                source_refs.append(ref)
                fresh = _objects(conn, table) if table else []
                for a in fresh:
                    a["evidence"] = evidence
                new_ids = {a["id"] for a in fresh}
                conn["asset_tables"].update({aid: name for aid in new_ids})
                changed = old_ids | new_ids
                scan["changed_asset_ids"].extend(sorted(changed))
                untouched_projection = old_ids and all(aid in current and current[aid]["status"] == "confirmed" and
                    digest(meaningful(current[aid])) == conn["projected"].get(aid) for aid in old_ids)
                automatic = bool(name not in carry and conn["auto_indexes"] and code == "nonunique_index_only" and untouched_projection)
                scan["changes"].append({"table": name, "classification": code, "automatic": automatic,
                    "reason": "Mechanical index metadata only / 仅机械同步非唯一索引元数据" if automatic else "Review meaning, mapping and identity; absence may mean permission loss / 核对含义、映射和身份；不可见不一定是删除",
                    "before": old, "after": table})
                for a in fresh:
                    if automatic:
                        a = normalize_asset(a, confirm=True)
                        a.update(confirmed_by="policy:nonunique-index-only", confirmed_at=now(), updated=now())
                        current[a["id"]] = a
                        conn["projected"][a["id"]] = digest(meaningful(a))
                        scan["automatic_asset_ids"].append(a["id"])
                    else:
                        candidates.append({"op": "upsert", "asset": a})
                for aid in sorted(old_ids - new_ids):
                    candidates.append({"op": "retire", "target_id": aid, "reason": "Missing in current catalog; confirm identity and visibility / 当前目录不可见，请确认身份与可见权限"})
                if not automatic:
                    for aid in old_ids:
                        if current[aid]["status"] == "confirmed":
                            current[aid]["status"] = "needs_review"
                            current[aid]["review_reason"] = "Database metadata changed / 数据库结构已变化"
            sem["assets"] = list(current.values())
            mark_dependents(sem["assets"], scan["changed_asset_ids"])
            # Old scan proposals based on superseded source revisions remain historical, never auto-accepted.
            for group in unresolved if not hold_proposals else []:
                group["status"], group["superseded_by"] = "stale", scan["id"]
            if candidates and not hold_proposals:
                batch = {"id": uid("batch"), "status": "review", "sources": source_refs, "base_revision": req["revision"], "created": now()}
                know["batches"].append(batch)
                scan["group_ids"] = self.knowledge._add_groups([{"summary": "Review database structure changes / 核对数据库结构变化", "candidates": candidates}], batch, sem, know)
                for gid in scan["group_ids"]:
                    group = find(know["groups"], gid)
                    group["metadata_connection"] = conn["id"]
                    for c in group["candidates"]:
                        if c["op"] == "upsert":
                            conn["projected"][c["target_id"]] = digest(meaningful(c["asset"]))
            conn["snapshot"] = observed
            conn["dirty_asset_ids"] = sorted(set(conn["dirty_asset_ids"]) | set(scan["changed_asset_ids"]))
            for q in know["scenarios"]:
                paths = closure(sem, q["asset_ids"])
                hits = set(paths) & set(conn["dirty_asset_ids"])
                if hits:
                    scan["affected_questions"].append({"id": q["id"], "title": q["title"], "paths": [paths[x] for x in sorted(hits)]})
            know.setdefault("metadata_scans", []).append(scan)
            seeded = seed_physical_drafts(sem, know, scan["group_ids"]) if req.get("seed_draft") else None
            return {"status": "draft_ready" if seeded else "review_required" if candidates else "automatically_adjusted", "scan": scan,
                    **({"seeded": seeded} if seeded else {})}
        return self.knowledge._write(req, "读取数据库结构变化", apply, "scan")

    def regress(self, req):
        def apply(doc, sem, know, db):
            conn = find(know.get("connections", []), req.get("connection_id"), "连接")
            fresh(conn)
            results = []
            for q in know["scenarios"]:
                if not set(closure(sem, q["asset_ids"])) & set(conn["dirty_asset_ids"]):
                    continue
                checked = self.knowledge.scenario_check({"scenario_id": q["id"], "limit": 500})
                a, reader = checked["acceptance"], checked["reader"]
                expected_gaps = set(q.get("acceptance", {}).get("required_gap_codes", [])) | {"NO_DATA_CONNECTOR", "NO_ACTION_EXECUTOR"}
                unexpected = [g for g in reader.get("context", {}).get("gaps", []) if g["code"] not in expected_gaps]
                passed = a["context_contract"]["status"] == "passed" and not unexpected and not reader.get("error") and not reader.get("identity_issues") and all(c["status"] == "passed" for c in a["cases"])
                results.append({"scenario_id": q["id"], "title": q["title"], "basis_fingerprint": a["basis_fingerprint"],
                    "status": "passed" if passed else "blocked", "check": checked, "unexpected_gaps": unexpected})
            report = {"id": uid("regression"), "connection_id": conn["id"], "fingerprint": conn["snapshot"]["fingerprint"],
                "created": now(), "status": "passed" if results and all(r["status"] == "passed" for r in results) else "not_applicable" if not results else "blocked",
                "results": results, "answer_verified": False, "boundary": "Declared context and recorded examples only; no business query / 仅核对声明上下文与已有样例记录，未查询业务数据"}
            know.setdefault("metadata_regressions", []).append(report)
            return {"regression": report}
        return self.knowledge._write(req, "回归受影响业务问题", apply)


def fresh(conn):
    if not conn.get("snapshot"):
        raise ValueError("Scan metadata first / 请先读取元数据")
    config = {k: v for k, v in conn.items() if k in {"id", "name", "engine", "path", "host", "port", "database", "schema", "user", "password_env", "tls_ca", "tables", "auto_indexes"}}
    if capture(config)["fingerprint"] != conn["snapshot"]["fingerprint"]:
        raise Conflict("Database structure changed again; scan before review/regression/publication / 数据库结构再次变化，请先扫描，再核对、回归和发布")


def guard_publication(sem, know, included):
    for conn in know.get("connections", []):
        physical = set(conn["asset_tables"])
        if not physical & included:
            continue
        fresh(conn)
        for group in know["groups"]:
            if group.get("metadata_connection") == conn["id"] and not group.get("superseded_by") and group["status"] != "accepted" and any(c["target_id"] in included for c in group["candidates"]):
                raise ValueError("Review the pending database change group before publication / 请先核对待处理的数据库变化候选组")
        dirty = set(conn["dirty_asset_ids"]) & included
        if not dirty:
            continue
        required = [q for q in know["scenarios"] if set(closure(sem, q["asset_ids"])) & dirty]
        reports = [r for r in know.get("metadata_regressions", []) if r["connection_id"] == conn["id"] and r["fingerprint"] == conn["snapshot"]["fingerprint"]]
        for q in required:
            result = next((x for r in reversed(reports) for x in r["results"] if x["scenario_id"] == q["id"]), None)
            if not result or result["status"] != "passed" or result["basis_fingerprint"] != basis(q, sem, know):
                raise ValueError("Recheck the affected question before publication / 请先回归受影响问题: " + q["title"])


def published(know, included):
    for conn in know.get("connections", []):
        conn["dirty_asset_ids"] = sorted(set(conn["dirty_asset_ids"]) - included)


def regression_view(sem, know):
    """Expose current applicability without rewriting historical observations."""
    questions = {q['id']: q for q in know['scenarios']}
    fingerprints = {c['id']: c.get('snapshot', {}).get('fingerprint') for c in know.get('connections', [])}
    views = copy.deepcopy(know.get('metadata_regressions', []))
    for report in views:
        stale = report['fingerprint'] != fingerprints.get(report['connection_id'])
        for result in report['results']:
            q = questions.get(result['scenario_id'])
            result['current_status'] = 'stale' if stale or not q or result['basis_fingerprint'] != basis(q, sem, know) else result['status']
        report['current_status'] = 'stale' if stale or any(r['current_status'] == 'stale' for r in report['results']) else report['status']
    return views
