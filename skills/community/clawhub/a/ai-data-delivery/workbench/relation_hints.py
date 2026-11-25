"""Suggest narrowly supported relationship leads from current physical metadata."""
from collections import defaultdict
import re

from scripts.ingest_ddl import CREATE_RE, IDENTIFIER, identifier, strip_comments


KEY_NAMES = {"id", "code", "key", "uuid", "no", "number"}
SCOPE_FIELDS = {"tenant_id", "tenant_code", "org_id", "organization_id", "company_id"}
AUDIT_NAMES = {"created_by", "updated_by", "modified_by", "deleted_by", "approved_by", "owner_id"}
ROLE_PREFIXES = ("parent_", "supervisor_", "manager_", "previous_", "next_")
ORGANIZATION_NAMES = {"org", "organization", "organisation", "机构", "组织"}


def _tokens(name):
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return re.sub(r"[^\w]+", "_", name.casefold()).strip("_")


def _table_names(name):
    if name.endswith("ies") and len(name) > 3:
        return {name, name[:-3] + "y"}
    if name.endswith("s") and not name.endswith(("ss", "us")):
        return {name, name[:-1]}
    return {name}


def _parent_comment(comment, aliases):
    normalized = _tokens(comment)
    # A generic "parent ID" or a remark about a different entity has no direction evidence.
    targets = aliases | ORGANIZATION_NAMES if aliases & ORGANIZATION_NAMES else aliases
    if aliases & ORGANIZATION_NAMES and normalized in {"上级机构", "上级机构id", "上级机构_id", "上级机构编号",
                                                        "上级组织", "上级组织id", "上级组织_id", "上级组织编号"}:
        return True
    return any(normalized in {f"parent_{target}", f"parent_{target}_id", f"parent_{target}_identifier"}
               for target in targets)


def _column_type(asset):
    value = re.sub(r"\s*([(),])\s*", r"\1", asset["properties"].get("value_type", "").casefold())
    value = " ".join(value.split())
    return {"integer": "int", "int4": "int", "int8": "bigint"}.get(value, value)


def _current_evidence(asset, sources):
    for evidence in asset.get("evidence", []):
        source = sources.get(evidence.get("source_id"), {})
        if source.get("format") not in {"ddl", "metadata"}:
            continue
        current = source.get("revisions", [])[-1:]
        extraction = current[0].get("current_extraction") if current else None
        if (evidence.get("revision") == source.get("current_revision") and evidence.get("fragment_id")
                and evidence.get("extraction_id", extraction) == extraction):
            return evidence
    return None


def _locator(evidence):
    return {key: evidence[key] for key in ("source_id", "revision", "extraction_id", "fragment_id") if key in evidence}


def _column(asset, evidence):
    return {"id": asset["id"], "name": asset["properties"]["column"], "type": asset["properties"].get("value_type", ""),
            "evidence": _locator(evidence)}


def _ddl_tables(sources):
    tables = {}
    for source in sources:
        if source.get("format") != "ddl":
            continue
        revision = next((r for r in source["revisions"] if r["revision"] == source["current_revision"]), {})
        parsed = revision.get("parsed", {})
        fragments = {fragment["id"]: fragment["text"] for fragment in parsed.get("fragments", [])}
        for table in parsed.get("structure", {}).get("tables", []):
            fragment_id = table["fragment_id"]
            match = CREATE_RE.search(strip_comments(fragments.get(fragment_id, "")))
            if match:
                names = tuple(identifier(part) for part in re.findall(IDENTIFIER, match.group(1)))
                tables[(source["id"], fragment_id)] = (table, names[:-1], names[-1])
    return tables


def relation_hints(assets, sources, asset_id=None, limit=20, offset=0):
    """Return paged, ephemeral leads over a single graph snapshot."""
    if not 1 <= limit <= 100 or offset < 0:
        raise ValueError("Use a limit between 1 and 100 and a nonnegative offset / 请使用 1–100 条上限及非负偏移")
    active = {a["id"]: a for a in assets if a["status"] in {"draft", "confirmed"}}
    if asset_id is not None and (asset_id not in active or active[asset_id]["kind"] != "dataset"):
        raise ValueError("Select an active dataset ID / 请选择有效的数据表资产 ID")
    source_by_id = {s["id"]: s for s in sources}
    ddl_tables = _ddl_tables(sources)
    physical = {i: e for i, a in active.items() if (e := _current_evidence(a, source_by_id))}
    tables = {i: a for i, a in active.items() if i in physical and a["kind"] == "dataset"}
    fields = defaultdict(lambda: defaultdict(list))
    for i, field in active.items():
        if field["kind"] != "field" or i not in physical or not field["properties"].get("column"):
            continue
        for parent in field.get("refs", []):
            if parent in tables and physical[parent]["source_id"] == physical[i]["source_id"]:
                fields[parent][_tokens(field["properties"]["column"])].append(field)

    namespaces, declared, target_keys, documented_parents = {}, {}, defaultdict(list), {}
    for i, table in tables.items():
        prop = table["properties"]
        catalog = prop.get("catalog", {})
        evidence = physical[i]
        ddl, schema, bare = ddl_tables.get((evidence["source_id"], evidence["fragment_id"]),
                                           ({}, (catalog.get("schema", ""),), prop.get("metadata_table")))
        if not bare:
            continue
        declared[i] = {_tokens(column) for fk in [*ddl.get("foreign_keys", []), *catalog.get("foreign_keys", [])]
                       for column in fk.get("from_columns", fk.get("from_fields", []))}
        namespaces[i] = (prop.get("metadata_connection") or physical[i]["source_id"], schema)
        name = _tokens(bare)
        aliases = _table_names(name)
        if name.startswith("t_") and len(name) > 2:
            aliases |= _table_names(name[2:])
        key = [_tokens(k) for k in ddl.get("pk_guess", catalog.get("primary_key", []))]
        if not key or len(set(key)) != len(key) or any(len(fields[i][k]) != 1 for k in key):
            continue
        specific = [k for k in key if k not in SCOPE_FIELDS]
        if len(specific) != 1:
            continue
        anchor = specific[0]
        if anchor == "id" and len(fields[i].get("parent_id", ())) == 1:
            parent = fields[i]["parent_id"][0]
            column = parent["properties"]["column"]
            ddl_comment = next((c.get("comment") for c in ddl.get("columns", []) if c["name"] == column), None)
            comment = ddl_comment or parent["properties"].get("catalog", {}).get("comment")
            comment_evidence = physical[parent["id"]]
            if not comment:
                table_comment = ddl.get("comment") or catalog.get("comment") or ""
                entry = re.fullmatch(r"\s*parent_id\s*[:：=]\s*(.+?)\s*", table_comment, re.IGNORECASE)
                if entry and _parent_comment(entry[1], aliases):
                    comment = entry[1]
                    comment_evidence = physical[i]
            if comment and _parent_comment(comment, aliases):
                documented_parents[i] = (key, anchor, comment, _locator(comment_evidence))
        for alias in aliases:
            prefix = alias + "_"
            suffix = anchor.removeprefix(prefix)
            if suffix in KEY_NAMES or anchor.startswith(prefix):
                candidate = anchor if anchor.startswith(prefix) else prefix + anchor
                target_keys[(namespaces[i], candidate)].append((i, key, anchor))

    existing = {(a.get("from"), tuple(sorted(_tokens(x) for x in a["properties"].get("from_fields", []))))
                for a in active.values() if a["kind"] == "relation"}
    hints = []
    for i in namespaces:
        for name, matches in fields[i].items():
            if (len(matches) != 1 or name in declared[i] or name in AUDIT_NAMES or name in SCOPE_FIELDS
                    or name.startswith(("external_", "ext_", "audit_"))):
                continue
            origin = matches[0]
            origin_type = _column_type(origin)
            if not origin_type:
                continue
            candidates = {target: (key, anchor) for target, key, anchor in target_keys.get((namespaces[i], name), ()) if target != i}
            parent = documented_parents.get(i) if name == "parent_id" else None
            if parent:
                candidates[i] = parent[:2]
            for prefix in ROLE_PREFIXES:
                if name.startswith(prefix):
                    for target, key, anchor in target_keys.get((namespaces[i], name.removeprefix(prefix)), ()):
                        if target == i:
                            candidates[target] = (key, anchor)
            # Naming ambiguity remains unresolved even when only one type matches.
            if len(candidates) != 1:
                continue
            target, (key, anchor) = next(iter(candidates.items()))
            mapping = {k: name if k == anchor else k for k in key}
            if (i, tuple(sorted(mapping.values()))) in existing:
                continue
            if any(len(fields[i].get(left, ())) != 1 for left in mapping.values()):
                continue
            pairs = [(fields[i][left][0], fields[target][right][0]) for right, left in mapping.items()]
            if any(not _column_type(left) or _column_type(left) != _column_type(right) for left, right in pairs):
                continue
            if asset_id is not None and asset_id not in {i, target}:
                continue
            hints.append({"from": i, "from_name": tables[i]["name"], "to": target, "to_name": tables[target]["name"],
                          "basis": ("documented_parent_column_and_compatible_primary_key" if parent
                                    else "table_qualified_column_and_compatible_primary_key"),
                          **({"hierarchy_comment": parent[2], "hierarchy_evidence": parent[3]} if parent else {}),
                          "target_key_evidence": _locator(physical[target]),
                          "columns": [{"from": _column(left, physical[left["id"]]), "to": _column(right, physical[right["id"]])}
                                      for left, right in pairs]})
    hints.sort(key=lambda hint: (hint["from_name"], hint["to_name"], tuple(pair["from"]["name"] for pair in hint["columns"]),
                                 hint["from"], hint["to"]))
    return {"status": "review_only", "business_rows_read": 0, "total": len(hints), "offset": offset,
            "hints": hints[offset:offset + limit], "next_offset": offset + limit if offset + limit < len(hints) else None,
            "limitations": ["Name, primary-key shape, declared type and explicit hierarchy comments only / 仅核对字段命名、主键结构、声明类型和明确的层级注释",
                            "Verify actual key coverage, tenant scope, cardinality and business meaning before saving a relation / 保存关系前需另行核实键覆盖、租户范围、基数与业务含义",
                            "Only current source-linked physical assets and supported key patterns are considered / 仅检查具有当前来源的物理资产及受支持的键模式"]}
