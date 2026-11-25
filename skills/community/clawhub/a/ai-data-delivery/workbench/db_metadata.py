"""Bounded catalog reads, never user SQL or business rows. Credentials stay in the host environment."""
import ipaddress
import json
import os
from pathlib import Path
import re
import socket
import sqlite3
import ssl
import time
from contextlib import closing

from workbench.store import digest


class MetadataError(ValueError):
    """A catalog diagnostic with safe, operator-facing text."""


def _driver_hint(exc):
    # PyMySQL wraps socket and certificate errors; libpq may expose only a diagnostic string.
    seen = set()
    while exc is not None and id(exc) not in seen:
        seen.add(id(exc))
        code = exc.args[0] if exc.args else None
        state = getattr(exc, "sqlstate", None) or ""
        msg = str(exc).lower()
        if isinstance(exc, ssl.SSLCertVerificationError) or "certificate verify failed" in msg or "does not match host name" in msg:
            return "[tls_certificate] Verify the trusted CA, hostname and certificate validity / 请核对受信 CA、证书有效期及连接主机名"
        if isinstance(exc, ssl.SSLError) or code == 2026 or "server does not support ssl" in msg:
            return "[tls_handshake] Check server TLS support and trusted CA, or import a schema-only DDL / 请核对服务端 TLS 与可信 CA，或导入仅结构 DDL"
        if code == 1045 or state.startswith("28") or "password authentication failed" in msg:
            return "[authentication] Check the account and its configured credential / 请核对账号及对应的凭据"
        if code in (1044, 1142, 1143) or state == "42501":
            return "[catalog_permission] Check catalog visibility for the selected tables / 请核对所选表的目录可见权限"
        if isinstance(exc, socket.gaierror):
            return "[dns] Check hostname resolution / 请核对主机名解析"
        if isinstance(exc, (TimeoutError, ConnectionRefusedError)):
            return "[endpoint] Check host, port and reachability / 请核对地址、端口和网络可达性"
        exc = getattr(exc, "original_exception", None) or exc.__cause__ or exc.__context__
    return "Check endpoint, credentials, permissions and selected tables / 请核对地址、凭据、权限及选表"


def profile(value):
    if not isinstance(value, dict):
        raise ValueError("Provide a connection profile / 请提供连接配置")
    allowed = {"id", "name", "engine", "path", "host", "port", "database", "schema", "user", "password_env", "tls_ca", "tables", "auto_indexes"}
    if set(value) - allowed:
        raise ValueError("Unknown connection setting; passwords/SQL are not accepted / 未知连接参数，不接收密码或 SQL")
    p = dict(value)
    if p.get("engine") not in {"sqlite", "postgresql", "mysql"}:
        raise ValueError("Choose SQLite, PostgreSQL or MySQL / 请选择数据库类型")
    if not isinstance(p.get("name"), str) or not p["name"].strip() or len(p["name"]) > 160:
        raise ValueError("Name this connection / 请填写连接名称，至多 160 字符")
    tables = p.get("tables")
    if not isinstance(tables, list) or not 1 <= len(tables) <= 200 or any(not isinstance(t, str) or not t or len(t) > 255 or "\x00" in t for t in tables):
        raise ValueError("Select 1–200 exact table names / 请明确选择 1–200 个表名")
    p["tables"] = sorted(set(tables))
    p.setdefault("auto_indexes", False)
    if type(p["auto_indexes"]) is not bool:
        raise ValueError("auto_indexes must be boolean / 自动索引同步须为开关")
    if p["engine"] == "sqlite":
        raw = p.get("path")
        if not isinstance(raw, str) or not raw or raw.startswith(("file:", "\\\\", "//")):
            raise ValueError("Use an explicit local database file, not a URI or network share / 请使用本机数据库文件路径")
        path = Path(raw).expanduser().resolve()
        if not path.is_file():
            raise ValueError("Database file does not exist; nothing was created / 数据库文件不存在，未创建空库")
        return {k: p[k] for k in ("name", "engine", "tables", "auto_indexes")} | {"path": str(path), **({"id": p["id"]} if "id" in p else {})}
    for key in ("host", "database", "schema", "user", "password_env"):
        if not isinstance(p.get(key), str) or not p[key] or len(p[key]) > 255 or "\x00" in p[key]:
            raise ValueError(f"Provide {key} / 请填写 {key}")
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", p["password_env"]):
        raise ValueError("Use an environment variable name, never its secret value / 请填写环境变量名称，不是密码值")
    if p["host"].startswith(('/', '\\')) or any(c in p["host"] for c in "@/?#;= "):
        raise ValueError("Use a database hostname, not a URL/DSN / 请填写数据库主机名，不是 URL 或连接串")
    p.setdefault("port", 5432 if p["engine"] == "postgresql" else 3306)
    if type(p["port"]) is not int or not 1 <= p["port"] <= 65535:
        raise ValueError("Port must be 1–65535 / 端口须为 1–65535")
    if p["engine"] == "mysql" and p["database"] != p["schema"]:
        raise ValueError("MySQL schema must equal database / MySQL 的 schema 须与数据库一致")
    if p.get("tls_ca") and (not isinstance(p["tls_ca"], str) or not Path(p["tls_ca"]).is_file()):
        raise ValueError("TLS CA file is missing / TLS CA 文件不存在")
    return {k: v for k, v in p.items() if k != "path"}


def _endpoint(p):
    addresses = socket.getaddrinfo(p["host"], p["port"], type=socket.SOCK_STREAM)
    ips = [ipaddress.ip_address(a[4][0].split('%')[0]) for a in addresses]
    ips = [getattr(a, 'ipv4_mapped', None) or a for a in ips]
    if not ips or any(a.is_link_local or a.is_multicast or a.is_unspecified or str(a) == 'fd00:ec2::254' for a in ips):
        raise MetadataError("Database endpoint is not allowed / 不允许连接该数据库地址")
    secret = os.environ.get(p["password_env"])
    if not secret:
        raise MetadataError("Credential environment variable is unset; set it before starting the host / 凭据环境变量未设置，请在启动宿主前设置")
    local = p["host"].lower() in {"localhost", "127.0.0.1", "::1"} and all(a.is_loopback for a in ips)
    return secret, local


def _rows(cursor):
    columns = [d[0] for d in cursor.description]
    data = cursor.fetchmany(20001)
    if len(data) > 20000:
        raise MetadataError("Catalog result exceeded the limit; narrow the selected tables / 元数据超限，请缩小选表范围")
    return [dict(zip(columns, row)) for row in data]


def _budget(tables, deadline):
    if time.monotonic() > deadline:
        raise MetadataError("Catalog capture timed out; narrow the selection / 元数据读取超时，请缩小选表范围")
    if any(t and len(t['columns']) > 2000 for t in tables.values()) or len(json.dumps(tables, ensure_ascii=False).encode()) > 8 * 1024 * 1024:
        raise MetadataError("Schema exceeds capture limits; narrow the selection / 元数据超限，请缩小选择")


def _sqlite(p):
    path = Path(p["path"])
    if not path.is_file():
        raise MetadataError("Database file is missing / 数据库文件不存在")
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True, timeout=5)) as db:
        db.execute("PRAGMA query_only=ON")
        db.execute("PRAGMA trusted_schema=OFF")
        deadline = time.monotonic() + 10
        db.set_progress_handler(lambda: int(time.monotonic() > deadline), 1000)
        def authorize(action, a, b, database, trigger):
            if action == sqlite3.SQLITE_READ:
                return sqlite3.SQLITE_OK if a in {"sqlite_master", "sqlite_schema"} or a.startswith("pragma_") else sqlite3.SQLITE_DENY
            if action in {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_TRANSACTION, sqlite3.SQLITE_FUNCTION}:
                return sqlite3.SQLITE_OK if action != sqlite3.SQLITE_FUNCTION or (b or "").lower() != "load_extension" else sqlite3.SQLITE_DENY
            if action == sqlite3.SQLITE_PRAGMA and a in {"table_xinfo", "foreign_key_list", "index_list", "index_xinfo"}:
                return sqlite3.SQLITE_OK
            return sqlite3.SQLITE_DENY
        db.set_authorizer(authorize)
        db.execute("BEGIN")
        tables = {}
        for name in p["tables"]:
            _budget(tables, deadline)
            row = db.execute("SELECT type, sql FROM sqlite_schema WHERE name=? AND type IN ('table','view')", (name,)).fetchone()
            if not row:
                tables[name] = None
                continue
            if row[0] != "table" or re.match(r"(?is)^\s*CREATE\s+VIRTUAL\s+TABLE\b", row[1] or ""):
                raise MetadataError("Only ordinary base tables are supported / 当前只接入普通基础表")
            columns = _rows(db.execute("SELECT * FROM pragma_table_xinfo(?)", (name,)))
            fks = _rows(db.execute("SELECT * FROM pragma_foreign_key_list(?)", (name,)))
            indexes = []
            for idx in _rows(db.execute("SELECT * FROM pragma_index_list(?)", (name,))):
                detail = _rows(db.execute("SELECT * FROM pragma_index_xinfo(?)", (idx["name"],)))
                sql = db.execute("SELECT sql FROM sqlite_schema WHERE type='index' AND name=?", (idx["name"],)).fetchone()
                indexes.append({"name": idx["name"], "unique": bool(idx["unique"]), "origin": idx["origin"],
                                "definition": sql[0] if sql else None, "columns": detail})
            grouped = {}
            for fk in fks:
                group = grouped.setdefault(fk["id"], {"from_fields": [], "to_fields": [], "to_table": fk["table"], "to_schema": "main", "on_update": fk["on_update"], "on_delete": fk["on_delete"]})
                group["from_fields"].append(fk["from"])
                group["to_fields"].append(fk["to"])
            tables[name] = {"name": name, "schema": "main", "definition": row[1],
                "columns": [{"name": c["name"], "type": c["type"] or "untyped", "nullable": not bool(c["notnull"]),
                             "default": c["dflt_value"], "ordinal": c["cid"], "generated": c["hidden"], "pk_position": c["pk"]} for c in columns],
                "primary_key": [c["name"] for c in sorted(columns, key=lambda c: c["pk"]) if c["pk"]],
                "foreign_keys": list(grouped.values()), "indexes": sorted(indexes, key=lambda i: i["name"])}
        _budget(tables, deadline)
        return tables


def _postgresql(p, password, local):
    import psycopg
    # No arbitrary DSN/options: catalog queries and transaction settings are fixed here.
    deadline = time.monotonic() + 20
    with psycopg.connect(host=p["host"], port=p["port"], dbname=p["database"], user=p["user"], password=password,
                         connect_timeout=5, sslmode="disable" if local else "verify-full",
                         **({"sslrootcert": p["tls_ca"]} if p.get("tls_ca") else {})) as db:
        db.execute("BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
        db.execute("SET LOCAL statement_timeout = '10000ms'")
        db.execute("SET LOCAL lock_timeout = '2000ms'")
        tables = {}
        for name in p["tables"]:
            _budget(tables, deadline)
            record = db.execute("SELECT c.oid,c.relkind,pg_catalog.obj_description(c.oid,'pg_class'),pg_catalog.has_table_privilege(c.oid,'SELECT') FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname=%s AND c.relname=%s", (p["schema"], name)).fetchone()
            if not record:
                tables[name] = None
                continue
            oid, kind, comment, visible = record
            if not visible:
                raise MetadataError("Selected table metadata is not authorized / 所选表缺少元数据可见权限，请由管理员处理")
            if kind not in {"r", "p"}:
                raise MetadataError("Only ordinary/partitioned base tables are supported / 当前只接入基础表")
            columns = _rows(db.execute("SELECT a.attname AS name,pg_catalog.format_type(a.atttypid,a.atttypmod) AS type,NOT a.attnotnull AS nullable,pg_catalog.pg_get_expr(d.adbin,d.adrelid) AS default,a.attnum AS ordinal,a.attgenerated AS generated,a.attidentity AS identity_mode,CASE WHEN a.attcollation=0 THEN NULL ELSE a.attcollation::regcollation::text END AS collation,pg_catalog.col_description(a.attrelid,a.attnum) AS comment FROM pg_catalog.pg_attribute a LEFT JOIN pg_catalog.pg_attrdef d ON d.adrelid=a.attrelid AND d.adnum=a.attnum WHERE a.attrelid=%s AND a.attnum>0 AND NOT a.attisdropped ORDER BY a.attnum", (oid,)))
            constraints = _rows(db.execute("SELECT c.conname AS name,c.contype AS kind,pg_catalog.pg_get_constraintdef(c.oid) AS definition,c.conkey AS keys,c.confkey AS target_keys,n.nspname AS target_schema,t.relname AS target_table,c.confrelid AS target_oid FROM pg_catalog.pg_constraint c LEFT JOIN pg_catalog.pg_class t ON t.oid=c.confrelid LEFT JOIN pg_catalog.pg_namespace n ON n.oid=t.relnamespace WHERE c.conrelid=%s ORDER BY c.conname", (oid,)))
            names = {c["ordinal"]: c["name"] for c in columns}
            fks, pk = [], []
            for c in constraints:
                if c["kind"] == "p":
                    pk = [names[k] for k in c["keys"]]
                if c["kind"] == "f":
                    targets = dict(db.execute("SELECT attnum,attname FROM pg_catalog.pg_attribute WHERE attrelid=%s AND attnum=ANY(%s)", (c["target_oid"], c["target_keys"])).fetchall())
                    fks.append({"name": c["name"], "from_fields": [names[k] for k in c["keys"]], "to_fields": [targets[k] for k in c["target_keys"]], "to_table": c["target_table"], "to_schema": c["target_schema"], "definition": c["definition"]})
            indexes = _rows(db.execute("SELECT c.relname AS name,i.indisunique AS unique,pg_catalog.pg_get_indexdef(i.indexrelid) AS definition,i.indisvalid AS valid FROM pg_catalog.pg_index i JOIN pg_catalog.pg_class c ON c.oid=i.indexrelid WHERE i.indrelid=%s ORDER BY c.relname", (oid,)))
            tables[name] = {"name": name, "schema": p["schema"], "identity_hint": oid, "comment": comment, "columns": columns,
                            "primary_key": pk, "foreign_keys": fks, "indexes": indexes, "constraints": constraints}
        _budget(tables, deadline)
        _budget(tables, deadline)
    return tables


def _mysql_capture(db, p, deadline):
    def query(sql, args):
        with db.cursor() as cursor:
            cursor.execute(sql, args)
            return _rows(cursor)
    tables = {}
    for name in p["tables"]:
        _budget(tables, deadline)
        args = (p["schema"], name)
        record = query("SELECT TABLE_TYPE AS kind,ENGINE AS engine,TABLE_COLLATION AS collation,TABLE_COMMENT AS comment FROM information_schema.TABLES WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s", args)
        if not record:
            tables[name] = None  # Absence may mean permission loss. Never auto-retire.
            continue
        if record[0]["kind"] != "BASE TABLE":
            raise MetadataError("Only base tables are supported / 当前只接入基础表")
        columns = query("SELECT COLUMN_NAME AS name,COLUMN_TYPE AS type,IS_NULLABLE AS nullable,COLUMN_DEFAULT AS default_value,ORDINAL_POSITION AS ordinal,EXTRA AS extra,GENERATION_EXPRESSION AS generated_expression,COLLATION_NAME AS collation,COLUMN_COMMENT AS comment FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s ORDER BY ORDINAL_POSITION", args)
        for c in columns:
            c["nullable"], c["default"] = c["nullable"] == "YES", c.pop("default_value")
            c["generated"] = c.pop("generated_expression")
        keys = query("SELECT CONSTRAINT_NAME AS name,COLUMN_NAME AS column_name,ORDINAL_POSITION AS ordinal,REFERENCED_TABLE_SCHEMA AS target_schema,REFERENCED_TABLE_NAME AS target_table,REFERENCED_COLUMN_NAME AS target_column FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s ORDER BY CONSTRAINT_NAME,ORDINAL_POSITION", args)
        grouped = {}
        for k in keys:
            if k["target_table"]:
                f = grouped.setdefault(k["name"], {"name": k["name"], "from_fields": [], "to_fields": [], "to_table": k["target_table"], "to_schema": k["target_schema"]})
                f["from_fields"].append(k["column_name"])
                f["to_fields"].append(k["target_column"])
        indexes = query("SELECT INDEX_NAME AS name,NON_UNIQUE AS non_unique,SEQ_IN_INDEX AS sequence,COLUMN_NAME AS column_name,COLLATION AS collation,SUB_PART AS prefix_length,INDEX_TYPE AS index_type,IS_VISIBLE AS visible,EXPRESSION AS expression FROM information_schema.STATISTICS WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s ORDER BY INDEX_NAME,SEQ_IN_INDEX", args)
        for i in indexes:
            i["unique"] = not bool(i.pop("non_unique"))
        constraints = query("SELECT tc.CONSTRAINT_NAME AS name,tc.CONSTRAINT_TYPE AS kind,cc.CHECK_CLAUSE AS definition FROM information_schema.TABLE_CONSTRAINTS tc LEFT JOIN information_schema.CHECK_CONSTRAINTS cc ON cc.CONSTRAINT_SCHEMA=tc.CONSTRAINT_SCHEMA AND cc.CONSTRAINT_NAME=tc.CONSTRAINT_NAME WHERE tc.TABLE_SCHEMA=%s AND tc.TABLE_NAME=%s ORDER BY tc.CONSTRAINT_NAME", args)
        rules = query("SELECT CONSTRAINT_NAME AS name,UPDATE_RULE AS on_update,DELETE_RULE AS on_delete FROM information_schema.REFERENTIAL_CONSTRAINTS WHERE CONSTRAINT_SCHEMA=%s AND TABLE_NAME=%s ORDER BY CONSTRAINT_NAME", args)
        tables[name] = {"name": name, "schema": p["schema"], **record[0], "columns": columns,
            "primary_key": [k["column_name"] for k in keys if k["name"] == "PRIMARY"], "foreign_keys": list(grouped.values()),
            "indexes": indexes, "constraints": constraints, "referential_actions": rules}
    _budget(tables, deadline)
    return tables


def _mysql(p, password, local):
    import pymysql
    deadline = time.monotonic() + 20
    with pymysql.connect(host=p["host"], port=p["port"], database=p["database"], user=p["user"], password=password,
        connect_timeout=5, read_timeout=10, write_timeout=10, autocommit=False, local_infile=False,
        ssl_disabled=local, ssl=None if local else ssl.create_default_context(cafile=p.get("tls_ca") or None)) as db:
        with db.cursor() as cursor:
            cursor.execute("SET SESSION MAX_EXECUTION_TIME=10000")
            cursor.execute("START TRANSACTION READ ONLY")
        first = _mysql_capture(db, p, deadline)
        second = _mysql_capture(db, p, deadline)
        if digest(first) != digest(second):
            raise MetadataError("Schema changed during capture; retry without advancing the baseline / 读取期间结构变化，请重试，未推进基线")
        return second


def capture(config):
    p = profile(config)
    try:
        if p["engine"] == "sqlite":
            tables = _sqlite(p)
        else:
            password, local = _endpoint(p)
            tables = (_postgresql if p["engine"] == "postgresql" else _mysql)(p, password, local)
        raw = json.dumps(tables, ensure_ascii=False, allow_nan=False)
        if len(raw.encode()) > 8 * 1024 * 1024 or any(t and len(t["columns"]) > 2000 for t in tables.values()):
            raise MetadataError("Schema exceeds capture limits; narrow the selection / 元数据超限，请缩小选择")
        return {"engine": p["engine"], "tables": tables, "fingerprint": digest(tables), "business_rows_read": 0}
    except ImportError as exc:
        raise ValueError("Install the pinned database drivers from requirements-connectors.txt / 请安装锁定的连接器依赖 requirements-connectors.txt") from exc
    except MetadataError:
        raise
    except Exception as exc:
        # Driver messages may contain connection secrets; do not return/log them.
        raise MetadataError("Metadata read failed / 元数据读取失败. " + _driver_hint(exc) +
                            ". Baseline unchanged / 基线未改变") from None


def classify(old, new):
    if old is None:
        return "added_or_restored", False
    if new is None:
        return "missing_or_hidden", False
    if digest(old) == digest(new):
        return "unchanged", True
    left = {k: v for k, v in old.items() if k != "indexes"}
    right = {k: v for k, v in new.items() if k != "indexes"}
    changed_indexes = [i for i in old.get("indexes", []) if i not in new.get("indexes", [])] + [i for i in new.get("indexes", []) if i not in old.get("indexes", [])]
    if digest(left) == digest(right) and changed_indexes and all(i.get("unique") is False for i in changed_indexes):
        return "nonunique_index_only", True
    return "definition_change", False
