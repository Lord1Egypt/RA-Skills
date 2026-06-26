#!/usr/bin/env python3
"""Generate semantic YAML from in-memory table metadata."""

from __future__ import annotations

import os
from typing import Any, Dict, List, Set, Tuple

import yaml


def normalize_database_type(db_type: str) -> str:
    """Normalize database type token for YAML output."""
    value = str(db_type or "").strip().lower()
    if value in {"mysql"}:
        return "mysql"
    if value in {"postgresql", "postgres", "psql"}:
        return "postgresql"
    if value in {"sqlserver", "sql_server", "mssql"}:
        return "sql_server"
    if value in {"oracle"}:
        return "oracle"
    raise ValueError("UNSUPPORTED_DATABASE_TYPE")


def map_column_type(sql_type: str) -> str:
    """Map SQL-like type to strict YAML type tokens."""
    raw = str(sql_type or "").upper()
    if raw in {"TEXT", "NUMBER", "DATE", "BOOLEAN"}:
        return raw
    value = raw.lower()
    if any(t in value for t in ["int", "integer", "bigint", "smallint", "tinyint", "decimal", "numeric", "float", "double", "real"]):
        return "NUMBER"
    if any(t in value for t in ["date", "time", "datetime", "timestamp"]):
        return "DATE"
    if any(t in value for t in ["bool", "boolean", "bit"]):
        return "BOOLEAN"
    return "TEXT"


def _clean_ai_context(ai_ctx: Dict[str, Any], fallback_name: str) -> Dict[str, Any]:
    if not isinstance(ai_ctx, dict):
        ai_ctx = {}
    cleaned: Dict[str, Any] = {"ai_name": ai_ctx.get("ai_name", fallback_name)}
    optional_keys = [
        "property",
        "ai_type",
        "value_list",
        "is_default",
        "weight",
        "synonyms",
        "default_datetime_field",
        "instructions",
    ]
    for key in optional_keys:
        if key in ai_ctx and ai_ctx[key] is not None:
            cleaned[key] = ai_ctx[key]
    return cleaned


def _normalize_field(field: Dict[str, Any]) -> Dict[str, Any]:
    ai_ctx = field.get("ai_context", {}) if isinstance(field.get("ai_context"), dict) else {}
    field_name = field.get("name", "")
    field_desc = field.get("description", field.get("comment", "")) or field_name

    result = {
        "name": field_name,
        "type": map_column_type(field.get("type", "TEXT")),
        "description": field_desc,
        "primary_key": bool(field.get("primary_key", False)),
        "ai_context": _clean_ai_context(ai_ctx, field_desc),
    }
    if "num_format" in field and isinstance(field.get("num_format"), dict):
        result["num_format"] = field["num_format"]
    return result


def _normalize_dataset(table_name: str, table_info: Dict[str, Any]) -> Dict[str, Any]:
    table_desc = table_info.get("description", table_info.get("comment", "")) or table_name.split(".")[-1]
    table_ai_ctx = table_info.get("ai_context", {}) if isinstance(table_info.get("ai_context"), dict) else {}
    fields_raw = table_info.get("fields")
    if fields_raw is None:
        fields_raw = table_info.get("columns", [])
    fields = [_normalize_field(f) for f in fields_raw if isinstance(f, dict)]

    return {
        "name": str(table_info.get("name", table_name)).split(".")[-1],
        "source": table_name,
        "description": table_desc,
        "ai_context": _clean_ai_context(table_ai_ctx, table_desc),
        "fields": fields,
    }


def _extract_datasets(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    datasets: Dict[str, Dict[str, Any]] = {}
    tables = data.get("tables", {})
    if isinstance(tables, dict) and tables:
        for table_name, table_info in tables.items():
            if not isinstance(table_info, dict):
                continue
            datasets[str(table_name)] = _normalize_dataset(str(table_name), table_info)
        return datasets

    semantic_model = data.get("semantic_model", {})
    if isinstance(semantic_model, dict):
        model_datasets = semantic_model.get("datasets", [])
    elif isinstance(semantic_model, list) and semantic_model:
        model_datasets = semantic_model[0].get("datasets", [])
    else:
        model_datasets = []

    for dataset in model_datasets:
        if not isinstance(dataset, dict):
            continue
        source = str(dataset.get("source", dataset.get("name", "")))
        datasets[source] = _normalize_dataset(source, dataset)
    return datasets


def _extract_semantic_root(data: Dict[str, Any]) -> Dict[str, Any]:
    semantic_model = data.get("semantic_model", {})
    if isinstance(semantic_model, dict):
        return semantic_model
    if isinstance(semantic_model, list) and semantic_model and isinstance(semantic_model[0], dict):
        return semantic_model[0]
    return {}


def _resolve_selected_tables(all_tables: Dict[str, Dict[str, Any]], selected_tables: List[str]) -> Tuple[List[str], List[str]]:
    if not selected_tables:
        return sorted(all_tables.keys()), []

    mapping: Dict[str, str] = {}
    for full_name in all_tables.keys():
        short_name = full_name.split(".")[-1]
        mapping[full_name] = full_name
        mapping[short_name] = full_name

    resolved: List[str] = []
    missing: List[str] = []
    for name in selected_tables:
        mapped = mapping.get(name)
        if not mapped:
            missing.append(name)
            continue
        if mapped not in resolved:
            resolved.append(mapped)
    return resolved, missing


def _normalize_relationships(raw: Any, selected_sources: Set[str]) -> List[Dict[str, Any]]:
    relationships: List[Dict[str, Any]] = []
    if isinstance(raw, dict):
        for rel_name, rel in raw.items():
            if not isinstance(rel, dict):
                continue
            item = {
                "name": rel_name,
                "from": rel.get("from_table", rel.get("from", "")),
                "to": rel.get("to_table", rel.get("to", "")),
                "from_columns": rel.get("from_columns", []),
                "to_columns": rel.get("to_columns", []),
            }
            relationships.append(item)
    elif isinstance(raw, list):
        relationships = [r for r in raw if isinstance(r, dict)]

    filtered: List[Dict[str, Any]] = []
    for rel in relationships:
        from_table = rel.get("from", "")
        to_table = rel.get("to", "")
        if selected_sources and (from_table not in selected_sources or to_table not in selected_sources):
            continue
        if not rel.get("name"):
            rel["name"] = f"{from_table} to {to_table}"
        filtered.append(rel)
    return filtered


def _normalize_list_like(raw: Any) -> List[Any]:
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        if not raw:
            return []
        return list(raw.values())
    return []


def generate_yaml_content(
    topic_name: str,
    tables_data: Dict[str, Any],
    selected_tables: List[str],
    db_type: str = "",
) -> str:
    all_datasets = _extract_datasets(tables_data)
    if not all_datasets:
        raise ValueError("No usable table data found from source payload")

    target_sources, missing = _resolve_selected_tables(all_datasets, selected_tables)
    if missing:
        raise ValueError(f"TABLE_OR_SHEET_NOT_FOUND: {', '.join(missing)}")
    if not target_sources:
        raise ValueError("No table selected for YAML generation")

    semantic_root = _extract_semantic_root(tables_data)
    top_ai_ctx = tables_data.get("ai_context", {}) if isinstance(tables_data.get("ai_context"), dict) else {}
    root_ai_ctx = semantic_root.get("ai_context", {}) if isinstance(semantic_root.get("ai_context"), dict) else {}
    model_name = semantic_root.get("name") or tables_data.get("name") or topic_name
    model_desc = semantic_root.get("description") or tables_data.get("description") or topic_name
    instructions = (
        root_ai_ctx.get("instructions")
        or top_ai_ctx.get("instructions")
        or f"Use this semantic model to handle data queries and analysis related to {topic_name}."
    )
    semantic_model = {
        "name": model_name,
        "description": model_desc,
        "ai_context": {
            "instructions": instructions
        },
        "datasets": [all_datasets[source] for source in target_sources],
    }

    selected_sources = set(target_sources)
    relationships_raw = tables_data.get("relationships", semantic_root.get("relationships", []))
    metrics_raw = tables_data.get("metrics", semantic_root.get("metrics", []))
    terms_raw = tables_data.get("terms", semantic_root.get("terms", []))
    rules_raw = tables_data.get("rules", semantic_root.get("rules", []))
    semantic_model["relationships"] = _normalize_relationships(relationships_raw, selected_sources)
    semantic_model["metrics"] = _normalize_list_like(metrics_raw)
    semantic_model["terms"] = _normalize_list_like(terms_raw)
    semantic_model["rules"] = _normalize_list_like(rules_raw)

    database_type = normalize_database_type(db_type)
    config = {"version": "0.0.1", "database_type": database_type, "semantic_model": semantic_model}
    return yaml.dump(config, allow_unicode=True, default_flow_style=False, sort_keys=False, width=1000)


def generate_yaml_file(
    topic_name: str,
    tables_data: Dict[str, Any],
    selected_tables: List[str],
    output_path: str,
    db_type: str,
) -> Dict[str, Any]:
    """Generate yaml file and return metadata."""
    yaml_content = generate_yaml_content(topic_name, tables_data, selected_tables, db_type=db_type)
    os.makedirs(output_path, exist_ok=True)
    yaml_file = os.path.join(output_path, f"{topic_name}.yaml")
    with open(yaml_file, "w", encoding="utf-8") as f:
        f.write(yaml_content)
    return {
        "success": True,
        "yaml_path": os.path.abspath(yaml_file),
        "topic_name": topic_name,
        "selected_tables": selected_tables,
    }
