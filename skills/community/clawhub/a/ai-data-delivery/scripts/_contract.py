"""Shared local contract utilities. No network calls or business decisions."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile

import yaml


def _missing(path):
    print(f"错误：输入文件不存在：{path}\n"
          f"检查路径拼写；相对路径以当前工作目录为基准。", file=sys.stderr)
    sys.exit(2)


def top_shape_error(m):
    """模型顶层结构校验：返回错误消息或 None。

    datasets/metrics 等写错型别（映射当列表）是最高频的手写/生成错误，
    各消费方在深入处理前先调用本函数，把堆栈变成可操作提示。
    """
    if not isinstance(m, dict):
        return "模型必须是 YAML mapping"
    for key, want, hint in (
            ("datasets", list, "列表，每项一个数据集（含 name 字段）；若按表名写成了映射，"
                               "请改为列表并把键名写进各项的 name 字段"),
            ("relationships", list, "列表，每项含 from/to/join_key"),
            ("concepts", list, "列表，每项含 name"),
            ("metrics", list, "列表，每项含 id/name；若按指标名写成了映射，请改为列表"),
            ("ontology", dict, "mapping（含 entities/relations 子键）")):
        val = m.get(key)
        if val is not None and not isinstance(val, want):
            got = {list: "列表", dict: "mapping"}.get(want, str(want))
            return f"模型结构错误：{key} 应为{got}，当前是 {type(val).__name__}。{hint}"
    return None


def load(path):
    """读取 YAML 输入；文件缺失/非法时给可操作报错（exit 2），不抛堆栈。"""
    p = Path(path)
    if not p.is_file():
        _missing(path)
    try:
        with open(p, encoding="utf-8-sig") as stream:
            return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(f"错误：输入文件不是合法 YAML：{path}\n{exc}", file=sys.stderr)
        sys.exit(2)


def digest(path):
    if not Path(path).is_file():
        _missing(path)
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def object_digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     default=str).encode()).hexdigest()


def minimal_env(extra=None):
    """白名单环境：仅保留子进程运行必需项，不透传可能含凭据的变量（CI token 等）。"""
    keep = ("PATH", "SystemRoot", "SYSTEMROOT", "WINDIR", "TEMP", "TMP",
            "HOME", "USERPROFILE", "LANG", "LC_ALL")
    env = {k: os.environ[k] for k in keep if k in os.environ}
    env["PYTHONIOENCODING"] = "utf-8"
    if extra:
        env.update(extra)
    return env


def guard_endpoint(url, allow_remote=False):
    """无网络策略检查；实际传输仍须经 _network 校验解析结果并固定连接 IP。"""
    from _network import validate_url
    validate_url(url, allow_remote)


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def write(path, value):
    """Atomic replacement of one artifact, including Unicode paths on Windows."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = (json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n"
               if path.suffix == ".json" else
               yaml.safe_dump(value, allow_unicode=True, sort_keys=False))
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".delivery-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def quote(name):
    if not isinstance(name, str) or not name or "\x00" in name:
        raise ValueError("invalid SQL identifier")
    return '"' + name.replace('"', '""') + '"'


def readonly(path):
    uri = Path(path).resolve().as_uri() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.execute("PRAGMA query_only=ON")
    return conn


def snapshot(path):
    """Read a consistent SQLite snapshot (including committed WAL contents)."""
    source = readonly(path)
    conn = sqlite3.connect(":memory:")
    try:
        source.backup(conn)
    finally:
        source.close()
    conn.execute("PRAGMA query_only=ON")
    fingerprint = hashlib.sha256()
    for statement in conn.iterdump():
        fingerprint.update(statement.encode("utf-8"))
        fingerprint.update(b"\n")
    return conn, fingerprint.hexdigest()


def evidence(model, cases=None, mode="static", **extra):
    return {"schema_version": "1.0", "created_at": now(), "mode": mode,
            "model_sha256": digest(model) if model else None,
            "cases_sha256": digest(cases) if cases else None, **extra}


def fields(ds):
    return {field["name"] for field in ds.get("fields", [])}


def keys(value):
    return [value] if isinstance(value, str) else list(value or [])


def relation_keys(rel):
    # Existing consumers use join_key_from/join_key_to for asymmetric keys.
    # Retain those declarations instead of falling back to a same-name key.
    for canonical, legacy in (("from_columns", "join_key_from"), ("to_columns", "join_key_to")):
        if canonical in rel and legacy in rel and keys(rel[canonical]) != keys(rel[legacy]):
            raise ValueError(f"conflicting {canonical}/{legacy}; confirm the intended mapping")
    left = keys(rel.get("from_columns", rel.get("join_key_from", rel.get("join_key"))))
    right = keys(rel.get("to_columns", rel.get("join_key_to", rel.get("join_key"))))
    if not left or len(left) != len(right) or len(set(left)) != len(left) or len(set(right)) != len(right):
        raise ValueError("关系需等长、不重复的 from_columns/to_columns（或同名 join_key）")
    return left, right


def relation_id(rel):
    return rel.get("id") or f"{rel.get('from')}->{rel.get('to')}:{','.join(keys(rel.get('join_key')))}"


# ---------- ontology 段（声明式事实清单；不做推理，只做静态对账） ----------

MAPPINGS = {"equi_key", "weak", "derived", "semantic_only"}


def ontology(model):
    ont = model.get("ontology") or {}
    return ont if isinstance(ont, dict) else {}


def ont_entities(model):
    return ontology(model).get("entities", []) or []


def ont_relations(model):
    return ontology(model).get("relations", []) or []


def ont_relation_id(rel):
    return rel.get("id") or f"{rel.get('from')}->{rel.get('to')}:{rel.get('predicate')}"


def ont_entity_id(entity):
    """本体实体的稳定身份：uid 优先（重命名后可追踪），缺省回退 name。"""
    return entity.get("uid") or entity.get("name")


EVIDENCE_SOURCES = {"user_provided", "data_observed", "model_inferred", "owner_confirmed"}


def evidence_source(obj):
    """元素级证据来源分级：用户提供/数据观测/模型推断/责任人确认。无声明返回 None。"""
    source = (obj.get("evidence") or {}).get("source")
    return source if source in EVIDENCE_SOURCES else None


def get_path(obj, dotted):
    """Walk a dotted collection path like 'ontology.entities'."""
    for part in dotted.split("."):
        if not isinstance(obj, dict):
            return []
        obj = obj.get(part, [])
    return obj


def binding_errors(report, model, cases=None, max_age_hours=24):
    if not isinstance(report, dict) or not isinstance(report.get('evidence'), dict):
        return ['report must be an object with evidence bindings; raw reconcile_paths lists are not evidence reports. Use a model-bound run_eval report for acceptance.']
    ev = report.get("evidence", {})
    errors = []
    if ev.get("model_sha256") != digest(model):
        errors.append("missing/stale model binding")
    if cases and ev.get("cases_sha256") != digest(cases):
        errors.append("missing/stale cases binding")
    try:
        age = dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(ev["created_at"])
        if not 0 <= age.total_seconds() <= max_age_hours * 3600:
            errors.append("expired/future evidence")
    except (KeyError, ValueError, TypeError):
        errors.append("missing/invalid evidence timestamp")
    return errors
