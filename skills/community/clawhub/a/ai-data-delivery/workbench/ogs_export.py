"""Offline OGS 1.1 projection of one verified semantic snapshot.

No database calls, imported query execution or writes to the canonical model.
Generated labels identify a new design; they never assert an existing DB mapping.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re

from .semantic_package import PackageError, SemanticPackage, read_package

OGS_SCHEMA = "https://neo4j.com/docs/ontology-graph-spec/1.1.0/schema.json"
NAMESPACE = "ai_data_delivery"
CARRIER_FORMAT = "ai-data-delivery/ogs-projection/1"
_TYPES = {"ANY", "BOOLEAN", "DATE", "DURATION", "FLOAT32", "FLOAT", "INTEGER8", "INTEGER16",
          "INTEGER32", "INTEGER", "LOCAL DATETIME", "LOCAL TIME", "POINT", "STRING",
          "ZONED DATETIME", "ZONED TIME", "UUID"}
_TYPES |= {f"LIST<{value}>" for value in _TYPES if value != "UUID"}
_TYPES |= {f"VECTOR<{value}>" for value in ("FLOAT", "FLOAT32", "INTEGER", "INTEGER32", "INTEGER16", "INTEGER8")}
_TYPE_ALIASES = {"str": "STRING", "int": "INTEGER", "bool": "BOOLEAN"}


def _text(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _design_id(kind, asset_id):
    # ASCII identifiers do not inherit punctuation/Unicode restrictions from a DB.
    readable = re.sub(r"[^a-zA-Z0-9_]", "_", asset_id)[:40]
    return "ADD_" + kind + "_" + readable + "_" + _hash(asset_id)[:16]


def _summary(asset, warnings):
    result = {"description": asset.get("definition", "")[:1024],
              "aliases": list(dict.fromkeys([asset["name"], *asset.get("aliases", [])]))}
    if len(asset.get("definition", "")) > 1024:
        warnings.append({"code": "NATIVE_DESCRIPTION_TRUNCATED", "asset_id": asset["id"],
                         "preserved_in": "companion.model_json"})
    return result


def export_ogs(package):
    """Return (OGS document, per-asset coverage report), without writing any file.

    Input is an explicit semantic ZIP/directory path or an already verified reader.
    Native projection is deliberately small. All original semantic JSON and the
    package's source excerpts are retained as opaque JSON strings, so JavaScript
    transports cannot round large integers in business scopes or metric metadata.
    """
    if not isinstance(package, SemanticPackage):
        package = read_package(package)
    # Re-verify when a caller supplies a reader object that it could have mutated.
    package = SemanticPackage(package._entries)
    assets = package.model["assets"]
    index = {asset["id"]: asset for asset in assets}
    redirects = package.model.get("redirects", {})
    nodes, relationships, warnings = {}, {}, []
    coverage = {a["id"]: {"asset_id": a["id"], "kind": a["kind"], "native_paths": [],
                           "preservation": "opaque_companion", "reason": "no_native_projection"} for a in assets}

    def projected(aid, path, reason):
        item = coverage[aid]
        item["native_paths"].append(path)
        item.update(preservation="native_projection_and_opaque_companion", reason=reason)

    for asset in assets:
        aid = asset["id"]
        if asset["status"] != "confirmed":
            coverage[aid]["reason"] = "not_confirmed"
        elif asset["kind"] == "entity":
            nodes[aid] = {"label": _design_id("N", aid), **_summary(asset, warnings)}
            projected(aid, ["nodes", aid], "confirmed_entity")

    for asset in assets:
        aid = asset["id"]
        if asset["status"] != "confirmed" or asset["kind"] != "relation":
            continue
        left = redirects.get(asset.get("from"), asset.get("from"))
        right = redirects.get(asset.get("to"), asset.get("to"))
        if asset.get("relation_type") == "business" and left in nodes and right in nodes:
            relationships[aid] = {"type": _design_id("R", aid), "from": {"node": left},
                                  "to": {"node": right}, **_summary(asset, warnings)}
            projected(aid, ["relationships", aid], "explicit_business_endpoints")
        elif asset.get("relation_type") == "has_attribute" and left in nodes and right in index:
            attribute = index[right]
            if attribute["kind"] != "attribute" or attribute["status"] != "confirmed":
                coverage[aid]["reason"] = "attribute_not_confirmed"
                continue
            value_type = str(attribute.get("properties", {}).get("value_type", "")).upper()
            value_type = _TYPE_ALIASES.get(value_type.lower(), value_type)
            prop = _summary(attribute, warnings)
            if value_type in _TYPES:
                prop["type"] = value_type
            else:
                warnings.append({"code": "PROPERTY_TYPE_UNMAPPED", "asset_id": right,
                                 "value_type": attribute.get("properties", {}).get("value_type"),
                                 "preserved_in": "companion.model_json"})
            # Property IDs also become proposed database names; keep them explicit.
            pid = _design_id("P", right)
            prop["name"] = pid
            nodes[left].setdefault("properties", {})[pid] = prop
            path = ["nodes", left, "properties", pid]
            projected(right, path, "explicit_has_attribute")
            projected(aid, path, "explicit_has_attribute")
        else:
            coverage[aid]["reason"] = ("physical_fk_not_business" if asset.get("relation_type") == "physical_fk"
                                       else "unsupported_relation_or_endpoints")

    model_json, sources_json = _text(package.model), _text(package.source_records)
    companion = {"format": CARRIER_FORMAT, "snapshot_id": package.manifest["snapshot_id"],
                 "source_revision": package.manifest["source_revision"],
                 "package_complete": package.manifest["complete"], "package_draft": package.manifest["draft"],
                 "model_json": model_json, "model_sha256": _hash(model_json),
                 "sources_json": sources_json, "sources_sha256": _hash(sources_json),
                 "authority": "read_only_projection_of_semantic_snapshot", "database_mapping": "not_verified"}
    document = {"schema": OGS_SCHEMA, "version": package.manifest["snapshot_id"],
                "id": "add-" + _hash(package.manifest["snapshot_id"])[:32],
                "name": "Semantic snapshot projection",
                "description": "Offline semantic projection. Generated identifiers propose a new graph design; no existing database mapping or enforcement is verified.",
                "nodes": nodes, "relationships": relationships,
                "extensions": {"custom": {NAMESPACE: companion}}}
    report = {"status": "exported_projection", "schema": OGS_SCHEMA,
              "snapshot_id": package.manifest["snapshot_id"],
              "package_complete": package.manifest["complete"], "package_draft": package.manifest["draft"],
              "native_nodes": len(nodes), "native_relationships": len(relationships),
              "native_property_placements": sum(len(node.get("properties", {})) for node in nodes.values()),
              "assets": list(coverage.values()), "warnings": warnings,
              "identifier_policy": "new_design_identifier",
              "database_mapping": "not_verified", "official_library_validation": "not_run_by_exporter",
              "source_mapping": "not_exported",
              "not_native": ["business_scope", "effective_dates", "metric_formula_and_grain", "rules",
                             "evidence", "identity_rules", "source_mappings", "permissions"],
              "preservation": {"model": "opaque_json_string", "sources": "opaque_json_string",
                               "model_sha256": companion["model_sha256"], "sources_sha256": companion["sources_sha256"]},
              "execution": {"database_connected": False, "queries_executed": False, "constraints_created": False,
                            "database_import_ready": False, "business_answer_verified": False},
              "limits": ["Custom extensions have no standard business meaning for other OGS consumers.",
                         "No keys, tenant identity, cardinalities, permissions or physical mappings are inferred.",
                         "Generic OGS/Aura conversion may discard the companion; audit each actual route.",
                         "Fingerprints prove consistency, not source authenticity or business acceptance."]}
    return document, report


def _normalise_native(document):
    result = copy.deepcopy({key: document.get(key, {}) for key in ("nodes", "relationships")})
    for node in result["nodes"].values():
        if "label" in node:
            label = node.pop("label")
            if label is not None:
                labels = node.setdefault("labels", {})
                if "identifier" in labels and labels["identifier"] != label:
                    node["label"] = label  # Conflicting shorthand must remain observable.
                else:
                    labels["identifier"] = label
    return result


def _differences(expected, actual, path=()):
    """Compare both directions; tolerate only known empty/default schema fields."""
    changes = []
    if isinstance(expected, dict) and isinstance(actual, dict):
        for key, value in expected.items():
            # OGS encoders may omit empty defaults.
            if key not in actual and value in ({}, [], None):
                continue
            if key not in actual:
                changes.append({"path": list((*path, key)), "change": "missing"})
            else:
                changes.extend(_differences(value, actual[key], (*path, key)))
        for key in set(actual) - set(expected):
            added_path = (*path, key)
            if not _sdk_empty_default(added_path, actual[key]):
                changes.append({"path": list(added_path), "change": "added"})
    elif _text(expected) != _text(actual):
        changes.append({"path": list(path), "change": "changed"})
    return changes


def _sdk_empty_default(path, value):
    # These locations name fields, not arbitrary node/property IDs. An added node
    # with an empty body remains a change, even when its ID is e.g. "properties".
    field = path[-1]
    native_item = len(path) == 3 and path[0] in {"nodes", "relationships"}
    property_field = len(path) == 5 and path[0] in {"nodes", "relationships"} and path[2] == "properties"
    label_field = len(path) == 4 and path[0] == "nodes" and path[2] == "labels"
    endpoint_field = len(path) == 4 and path[0] == "relationships" and path[2] in {"from", "to"}
    if native_item or property_field:
        if value == {} and field in {"properties", "constraints", "extensions"}:
            return True
        if value == [] and field == "aliases":
            return True
        if value == "" and field in {"description", "reference"}:
            return True
    if property_field and field == "type" and value == "ANY":
        return True  # Unspecified OGS property type defaults to ANY.
    if property_field and value is None and field in {"name", "dimension", "key", "unique", "must_exist"}:
        return True
    if label_field and ((value == [] and field in {"implied", "optional"}) or (field == "identifier" and value is None)):
        return True
    if endpoint_field and value is None and field in {"count", "min_count", "max_count"}:
        return True
    return False


def _companion(document):
    try:
        value = document["extensions"]["custom"][NAMESPACE]
        if not isinstance(value, dict) or value.get("format") != CARRIER_FORMAT:
            return None
        return value
    except (KeyError, TypeError):
        return None


def audit_roundtrip(original, returned):
    """Inspect actual conversion output; never restore it into the authoring graph.

    Compare native meaning and the opaque companion independently. The result can
    report preserved native nodes and lost evidence; passing shape validation alone
    must never hide that loss. Library-added defaults are tolerated, new graph objects
    are reported as changes. This is not a general OGS semantic-equivalence prover.
    """
    if not isinstance(original, dict) or not isinstance(returned, dict):
        raise PackageError("INVALID_INPUT", "OGS audit inputs must be JSON objects")
    for field in ("schema", "version", "id"):
        if not isinstance(original.get(field), str) or not original[field]:
            raise PackageError("INVALID_OGS_EXPORT", "Original export header is missing or invalid", field=field)
    companion = _companion(original)
    if companion is None:
        raise PackageError("INVALID_OGS_EXPORT", "Original has no ai-data-delivery companion")
    if not isinstance(companion.get("snapshot_id"), str) or not companion["snapshot_id"]:
        raise PackageError("INVALID_OGS_EXPORT", "Original companion snapshot_id is missing or invalid", field="snapshot_id")
    for field in ("model", "sources"):
        raw = companion.get(field + "_json")
        if not isinstance(raw, str) or _hash(raw) != companion.get(field + "_sha256"):
            raise PackageError("INVALID_OGS_EXPORT", "Original companion hash mismatch", field=field)
    try:
        expected, actual = _normalise_native(original), _normalise_native(returned)
        changes = _differences(expected, actual)
        changes += _differences({k: original[k] for k in ("schema", "version", "id")},
                                {k: returned[k] for k in ("schema", "version", "id") if k in returned})
    except (AttributeError, TypeError) as exc:
        raise PackageError("INVALID_INPUT", "Invalid OGS native container") from exc
    restored = _companion(returned)
    preserved, integrity = {}, {}
    for field in ("model", "sources"):
        raw = restored.get(field + "_json") if restored else None
        integrity[field] = isinstance(raw, str) and _hash(raw) == restored.get(field + "_sha256")
        preserved[field] = integrity[field] and raw == companion[field + "_json"]
    metadata_preserved = bool(restored) and not _differences(
        {k: v for k, v in companion.items() if k not in {"model_json", "sources_json"}},
        {k: v for k, v in restored.items() if k not in {"model_json", "sources_json"}})
    native_preserved = not changes
    full = native_preserved and all(preserved.values()) and metadata_preserved
    return {"status": "preserved" if full else "changed_or_lost", "snapshot_id": companion["snapshot_id"],
            "native_projection_preserved": native_preserved, "native_changes": changes,
            "companion_present": restored is not None, "companion_integrity": integrity,
            "semantic_model_preserved": preserved["model"], "source_evidence_preserved": preserved["sources"],
            "companion_metadata_preserved": metadata_preserved, "same_export_preserved": full,
            "database_import_verified": False, "business_semantics_executed": False,
            "limits": "Compares this exporter projection and payload; not arbitrary OGS equivalence or database acceptance."}
