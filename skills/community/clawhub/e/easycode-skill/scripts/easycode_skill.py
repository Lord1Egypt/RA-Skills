#!/usr/bin/env python3
import argparse
import glob
import json
import os
import shlex
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

STATE_DIR = Path(".easycode-skill")
STATE_FILE = STATE_DIR / "state.json"

SUPPORTED_GROUPS = {
    "MyBatisPlus": "EasyCodeConfig-mybatispuls.json",
    "Custom-V2": "EasyCodeConfig-V2.json",
    "Custom-V3": "EasyCodeConfig-V3.json",
}

SAVE_PATTERN = re.compile(r"#save\(\s*\"([^\"]+)\"\s*,\s*\"([^\"]+)\"\s*\)")
PKG_PATTERN = re.compile(r"#setPackageSuffix\(\s*\"([^\"]+)\"\s*\)")
SUFFIX_PATTERN = re.compile(r"#setTableSuffix\(\s*\"([^\"]*)\"\s*\)")

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
CONFIG_DIR = SKILL_ROOT / "configs"
DRIVER_PATHS_FILE = SKILL_ROOT / "drivers" / "drivers-paths.json"
JAVA_SRC_DIR = SCRIPT_DIR / "java"
JAVA_BUILD_DIR = Path(tempfile.gettempdir()) / "easycode-skill-java-build"
JAVA_RENDER_MAIN_CLASS = "VelocityRenderBridge"
JAVA_METADATA_MAIN_CLASS = "JdbcMetadataBridge"


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    with STATE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def _save_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with STATE_FILE.open("w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def _package_to_path(base_package: str) -> str:
    return base_package.replace(".", "/")


def _parse_spec(spec_raw: str) -> dict:
    try:
        return json.loads(spec_raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid --spec JSON: {exc}")


def _validate(spec: dict) -> None:
    if "db_connection" not in spec or "generation_config" not in spec:
        raise SystemExit("spec must contain db_connection and generation_config")

    dbc = spec["db_connection"]
    gen = spec["generation_config"]

    required_db = ["db_type", "url", "user", "pass"]
    required_gen = ["table_names", "author", "base_package", "template_group"]

    for key in required_db:
        if not dbc.get(key):
            raise SystemExit(f"db_connection.{key} is required")

    for key in required_gen:
        if not gen.get(key):
            raise SystemExit(f"generation_config.{key} is required")

    if dbc["db_type"] not in {"mysql", "postgresql", "oracle", "sqlserver"}:
        raise SystemExit("db_connection.db_type must be one of mysql/postgresql/oracle/sqlserver")

    if gen["template_group"] not in SUPPORTED_GROUPS:
        raise SystemExit(f"Unsupported template_group: {gen['template_group']}")

    if not isinstance(gen["table_names"], list) or not gen["table_names"]:
        raise SystemExit("generation_config.table_names must be a non-empty array")


def merge_with_state(spec: dict, state: dict) -> dict:
    merged = {
        "db_connection": dict(state.get("db_connection", {})),
        "generation_config": dict(state.get("generation_config", {})),
    }
    merged["db_connection"].update(spec.get("db_connection", {}))
    merged["generation_config"].update(spec.get("generation_config", {}))

    merged.setdefault("generation_config", {})
    merged["generation_config"].setdefault("template_group", "Custom-V3")
    merged["generation_config"].setdefault("output_root", "src/main/java")
    return merged


def to_pascal_case(raw_name: str) -> str:
    parts = [p for p in raw_name.replace("-", "_").split("_") if p]
    if not parts:
        return "Unknown"
    return "".join(p.lower().capitalize() for p in parts)


def _snake_to_camel(raw_name: str) -> str:
    pascal = to_pascal_case(raw_name)
    if not pascal:
        return "unknown"
    return pascal[:1].lower() + pascal[1:]


def _split_qualified_table(table_name: str) -> Tuple[str, str]:
    if "." in table_name:
        schema, table = table_name.split(".", 1)
        return schema.strip(), table.strip()
    return "", table_name.strip()


def _short_type(java_type: str) -> str:
    if not java_type:
        return "Object"
    if "<" in java_type:
        java_type = java_type.split("<", 1)[0]
    return java_type.split(".")[-1]


def _load_template_elements(template_group: str) -> List[Dict[str, Any]]:
    cfg_path = _resolve_template_config_path(template_group)
    if not cfg_path.exists():
        raise SystemExit(f"Template config file not found: {cfg_path}")

    with cfg_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    groups = data.get("template", {})
    if not groups:
        raise SystemExit(f"No template group found in {cfg_path}")

    first_group = next(iter(groups.values()))
    elements = first_group.get("elementList", [])
    if not elements:
        raise SystemExit(f"Template group has no elements in {cfg_path}")
    return elements


def _resolve_template_config_path(template_group: str) -> Path:
    filename = SUPPORTED_GROUPS[template_group]
    candidates = [
        CONFIG_DIR / filename,
        Path(filename),
    ]
    for p in candidates:
        if p.exists():
            return p
    raise SystemExit(f"Template config file not found for {template_group}: {filename}")


def _load_global_macros(template_group: str) -> Dict[str, str]:
    cfg_path = _resolve_template_config_path(template_group)
    if not cfg_path.exists():
        raise SystemExit(f"Template config file not found: {cfg_path}")

    with cfg_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    global_config = data.get("globalConfig", {})
    if not global_config:
        return {}

    first_group = next(iter(global_config.values()))
    elements = first_group.get("elementList", [])
    
    macros = {}
    for element in elements:
        name = element.get("name", "")
        value = element.get("value", "")
        if name:
            macros[name] = value
            macros[f"{name}.vm"] = value
    return macros


def _parse_template_rule(element: Dict[str, Any]) -> Dict[str, str]:
    code = element.get("code", "")

    save_match = SAVE_PATTERN.search(code)
    pkg_match = PKG_PATTERN.search(code)
    suffix_match = SUFFIX_PATTERN.search(code)

    save_dir = save_match.group(1).strip("/") if save_match else ""
    save_name = save_match.group(2) if save_match else "Generated.java"

    if "." in save_name:
        ext = "." + save_name.split(".")[-1]
    else:
        ext = ".java"

    suffix = suffix_match.group(1) if suffix_match else ""
    package_suffix = pkg_match.group(1).strip(".") if pkg_match else save_dir.replace("/", ".")
    module_name = element.get("name") or save_dir or "module"

    return {
        "module_name": module_name,
        "save_dir": save_dir,
        "package_suffix": package_suffix,
        "class_suffix": suffix,
        "ext": ext,
    }


def _resolve_java_package(base_package: str, package_suffix: str) -> str:
    return f"{base_package}.{package_suffix}" if package_suffix else base_package


def _normalize_target_dir(raw_save_path: str, project_root: Path) -> Path:
    p = Path(raw_save_path)
    if p.is_absolute():
        parts = p.parts
        # EasyCode templates may emit '/src/...' meaning project-root-relative.
        if len(parts) >= 2 and parts[1] == "src":
            return project_root / Path(*parts[1:])
        return p
    return p


def _find_jar(pattern: str) -> str:
    files = glob.glob(os.path.expanduser(pattern))
    if not files:
        return ""
    files.sort()
    return files[-1]


def _load_driver_paths_config() -> Dict[str, Any]:
    if not DRIVER_PATHS_FILE.exists():
        return {}
    try:
        with DRIVER_PATHS_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _expand_pattern(pattern: str) -> str:
    home = str(Path.home())
    return pattern.replace("{home}", home).replace("{skill_root}", str(SKILL_ROOT))


def _java_classpath_entries(extra_jars: List[str] = None) -> List[str]:
    jars = [
        _find_jar("~/.m2/repository/org/apache/velocity/velocity/1.7/velocity-1.7.jar"),
        _find_jar("~/.m2/repository/commons-collections/commons-collections/*/commons-collections-*.jar"),
        _find_jar("~/.m2/repository/commons-lang/commons-lang/*/commons-lang-*.jar"),
        _find_jar("~/.m2/repository/oro/oro/*/oro-*.jar"),
        _find_jar("~/.gradle/caches/modules-2/files-2.1/com.fasterxml.jackson.core/jackson-databind/*/*/jackson-databind-*.jar"),
        _find_jar("~/.gradle/caches/modules-2/files-2.1/com.fasterxml.jackson.core/jackson-core/*/*/jackson-core-*.jar"),
        _find_jar("~/.gradle/caches/modules-2/files-2.1/com.fasterxml.jackson.core/jackson-annotations/*/*/jackson-annotations-*.jar"),
    ]
    missing = [p for p in jars if not p]
    if missing:
        raise SystemExit("Missing local Java dependencies for Velocity bridge.")
    if extra_jars:
        jars.extend([j for j in extra_jars if j])
    return jars


def _ensure_java_bridge_compiled(extra_jars: List[str] = None) -> str:
    if not JAVA_SRC_DIR.exists():
        raise SystemExit(f"Java bridge source dir not found: {JAVA_SRC_DIR}")

    java_sources = sorted(str(p) for p in JAVA_SRC_DIR.glob("*.java"))
    if not java_sources:
        raise SystemExit(f"No java bridge sources in {JAVA_SRC_DIR}")

    JAVA_BUILD_DIR.mkdir(parents=True, exist_ok=True)
    cp_entries = _java_classpath_entries(extra_jars=extra_jars)
    compile_cp = os.pathsep.join(cp_entries)

    marker = JAVA_BUILD_DIR / ".compiled"
    latest_src_mtime = max(Path(s).stat().st_mtime for s in java_sources)
    needs_compile = not marker.exists() or latest_src_mtime >= marker.stat().st_mtime
    if needs_compile:
        cmd = [
            "javac",
            "-encoding",
            "UTF-8",
            "-cp",
            compile_cp,
            "-d",
            str(JAVA_BUILD_DIR),
        ] + java_sources
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise SystemExit(f"Failed to compile Java bridge:\n{proc.stderr}")
        marker.write_text(_now_iso(), encoding="utf-8")

    return os.pathsep.join([str(JAVA_BUILD_DIR)] + cp_entries)


def _run_java_main(main_class: str, args: List[str], extra_jars: List[str] = None) -> str:
    cp = _ensure_java_bridge_compiled(extra_jars=extra_jars)
    cmd = ["java", "-cp", cp, main_class] + args
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"{main_class} failed:\n{proc.stderr}\n{proc.stdout}")
    return proc.stdout


def _render_with_velocity(template_code: str, context_payload: Dict[str, Any]) -> Dict[str, str]:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".vm", delete=False) as tf:
        tf.write(template_code)
        template_file = tf.name

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as cf:
        json.dump(context_payload, cf, ensure_ascii=False)
        context_file = cf.name

    try:
        out_raw = _run_java_main(
            JAVA_RENDER_MAIN_CLASS,
            [
            "--template-file",
            template_file,
            "--context-file",
            context_file,
            ],
        )
        out = json.loads(out_raw)
        return {
            "rendered": out.get("rendered", ""),
            "savePath": out.get("savePath", ""),
            "fileName": out.get("fileName", ""),
        }
    finally:
        try:
            os.unlink(template_file)
        except OSError:
            pass
        try:
            os.unlink(context_file)
        except OSError:
            pass


def _driver_candidates(db_type: str) -> List[Tuple[str, str]]:
    cfg = _load_driver_paths_config()
    item = cfg.get(db_type, {}) if isinstance(cfg, dict) else {}
    patterns = item.get("patterns", []) if isinstance(item, dict) else []
    driver_class = item.get("driver_class", _default_driver_class(db_type)) if isinstance(item, dict) else _default_driver_class(db_type)
    dynamic: List[Tuple[str, str]] = []
    for p in patterns:
        if isinstance(p, str) and p.strip():
            jar = _find_jar(_expand_pattern(p.strip()))
            if jar:
                dynamic.append((driver_class, jar))
    if dynamic:
        return dynamic

    if db_type == "mysql":
        return [
            ("com.mysql.cj.jdbc.Driver", _find_jar("~/.m2/repository/com/mysql/mysql-connector-j/*/mysql-connector-j-*.jar")),
            ("com.mysql.jdbc.Driver", _find_jar("~/.m2/repository/mysql/mysql-connector-java/*/mysql-connector-java-*.jar")),
        ]
    if db_type == "postgresql":
        return [
            ("org.postgresql.Driver", _find_jar("~/.m2/repository/org/postgresql/postgresql/*/postgresql-*.jar")),
        ]
    if db_type == "oracle":
        return [
            ("oracle.jdbc.OracleDriver", _find_jar("~/.m2/repository/com/oracle/database/jdbc/ojdbc8/*/ojdbc8-*.jar")),
            ("oracle.jdbc.OracleDriver", _find_jar("~/.m2/repository/com/oracle/database/jdbc/ojdbc11/*/ojdbc11-*.jar")),
        ]
    if db_type == "sqlserver":
        return [
            ("com.microsoft.sqlserver.jdbc.SQLServerDriver", _find_jar("~/.m2/repository/com/microsoft/sqlserver/mssql-jdbc/*/mssql-jdbc-*.jar")),
        ]
    return []


def _default_driver_class(db_type: str) -> str:
    m = {
        "mysql": "com.mysql.cj.jdbc.Driver",
        "postgresql": "org.postgresql.Driver",
        "oracle": "oracle.jdbc.OracleDriver",
        "sqlserver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
    }
    return m.get(db_type, "")


def _default_jdbc_url(db_type: str) -> str:
    m = {
        "mysql": "jdbc:mysql://localhost:3306/demo?useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Shanghai",
        "postgresql": "jdbc:postgresql://localhost:5432/demo",
        "oracle": "jdbc:oracle:thin:@//10.96.1.32:1521/wghisfat",
        "sqlserver": "jdbc:sqlserver://localhost:1433;databaseName=demo;encrypt=false",
    }
    return m.get(db_type, "")


def _fetch_table_columns_via_jdbc(spec: dict) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, str], str]:
    dbc = spec["db_connection"]
    gen = spec["generation_config"]
    db_type = dbc["db_type"]
    table_names = [str(t) for t in gen["table_names"]]

    driver_jar = dbc.get("driver_jar", "").strip()
    driver_class = dbc.get("driver_class", "").strip()

    extra_jars: List[str] = []
    if driver_jar:
        if not Path(driver_jar).exists():
            return {}, {}, f"driver_jar not found: {driver_jar}"
        extra_jars.append(driver_jar)
    else:
        for cand_class, cand_jar in _driver_candidates(db_type):
            if cand_jar:
                extra_jars.append(cand_jar)
                if not driver_class:
                    driver_class = cand_class
                break

    if not extra_jars:
        return {}, {}, (
            f"No JDBC driver jar found for {db_type}. "
            "Provide db_connection.driver_jar (and optionally driver_class), or pass generation_config.table_columns."
        )

    type_mapping = gen.get("type_mapping", {}) if isinstance(gen.get("type_mapping"), dict) else {}
    number_type = str(type_mapping.get("number_default", "Long"))
    time_type = str(type_mapping.get("time_default", "Date"))

    args = [
        "--db-type", db_type,
        "--url", dbc["url"],
        "--user", dbc["user"],
        "--pass", dbc["pass"],
        "--tables", ",".join(table_names),
        "--number-type", number_type,
        "--time-type", time_type,
    ]
    if driver_class:
        args.extend(["--driver-class", driver_class])

    try:
        out_raw = _run_java_main(JAVA_METADATA_MAIN_CLASS, args, extra_jars=extra_jars)
    except Exception as exc:
        return {}, {}, f"JDBC metadata fetch failed: {exc}"

    out = json.loads(out_raw)
    tables = out.get("tables", {})
    table_comments = out.get("table_comments", {})
    if not isinstance(tables, dict):
        return {}, {}, "JDBC metadata fetch returned invalid table payload."
    if not isinstance(table_comments, dict):
        table_comments = {}
    return tables, table_comments, ""


def cmd_check_driver(args: argparse.Namespace) -> int:
    db_type = args.db_type
    if db_type not in {"mysql", "postgresql", "oracle", "sqlserver"}:
        raise SystemExit("--db-type must be mysql/postgresql/oracle/sqlserver")

    candidates = _driver_candidates(db_type)
    found = []
    for driver_class, jar in candidates:
        if jar:
            found.append({"driver_class": driver_class, "driver_jar": jar})

    out = {
        "db_type": db_type,
        "found": found,
        "recommended": found[0] if found else {
            "driver_class": _default_driver_class(db_type),
            "driver_jar": "",
        },
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def cmd_spec_template(args: argparse.Namespace) -> int:
    db_type = args.db_type
    if db_type not in {"mysql", "postgresql", "oracle", "sqlserver"}:
        raise SystemExit("--db-type must be mysql/postgresql/oracle/sqlserver")

    tables = [t.strip() for t in args.tables.split(",") if t.strip()] if args.tables else ["sys_user"]
    driver = _driver_candidates(db_type)
    first_driver = driver[0] if driver and driver[0][1] else ("", "")

    out = {
        "db_connection": {
            "db_type": db_type,
            "url": args.url or _default_jdbc_url(db_type),
            "user": args.user or "emr",
            "pass": args.password or "Wgfat_2022",
            "driver_class": first_driver[0] or _default_driver_class(db_type),
            "driver_jar": first_driver[1] or "",
        },
        "generation_config": {
            "table_names": tables,
            "author": args.author or "DeveloperName",
            "base_package": args.base_package or "com.wghis.sde",
            "template_group": args.template_group or "Custom-V2",
            "project_root": args.project_root or ".",
            "output_root": "src/main/java",
            "type_mapping": {
                "number_default": "Long",
                "time_default": "Date"
            }
        }
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def _default_columns_for_table(table_name: str) -> List[Dict[str, Any]]:
    return [
        {
            "name": "id",
            "comment": "主键",
            "type": "java.lang.Long",
            "shortType": "Long",
            "is_pk": True,
            "obj": {"name": "id", "dataType": {"typeName": "BIGINT"}},
            "ext": {},
        }
    ]


def _build_table_columns(
    gen: Dict[str, Any],
    table_name: str,
    resolved_columns: Dict[str, List[Dict[str, Any]]],
    fallback_tables: List[str],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    cols = resolved_columns.get(table_name)
    if not isinstance(cols, list) or not cols:
        cols = _default_columns_for_table(table_name)
        fallback_tables.append(table_name)

    full, pk, other = [], [], []
    for c in cols:
        if not isinstance(c, dict):
            continue
        raw_name = c.get("name", "id")
        java_type = c.get("type") or c.get("java_type") or "java.lang.String"
        is_pk = bool(c.get("is_pk", False))
        col = {
            "name": c.get("java_name") or _snake_to_camel(raw_name),
            "comment": c.get("comment", ""),
            "type": java_type,
            "shortType": c.get("short_type") or _short_type(java_type),
            "ext": c.get("ext") if isinstance(c.get("ext"), dict) else {},
            "obj": {
                "name": raw_name,
                "dataType": {
                    "typeName": c.get("sql_type", "VARCHAR")
                },
            },
        }
        full.append(col)
        if is_pk:
            pk.append(col)
        else:
            other.append(col)

    if not pk and full:
        pk = [full[0]]
        other = full[1:]

    return full, pk, other


def _render_entries(spec: dict, include_content: bool) -> Tuple[List[Dict[str, Any]], List[str]]:
    gen = spec["generation_config"]
    base_package = gen["base_package"]
    project_root = Path(gen.get("project_root", "."))
    output_root = Path(gen.get("output_root", "src/main/java"))
    package_dir = Path(_package_to_path(base_package))
    template_group = gen["template_group"]
    author = gen["author"]

    elements = _load_template_elements(template_group)
    macros = _load_global_macros(template_group)

    warnings: List[str] = []
    user_columns = gen.get("table_columns", {})
    resolved_columns: Dict[str, List[Dict[str, Any]]] = dict(user_columns) if isinstance(user_columns, dict) else {}
    resolved_table_comments: Dict[str, str] = {}

    missing_tables = [t for t in gen["table_names"] if not resolved_columns.get(t)]
    if missing_tables:
        fetched, table_comments, warning = _fetch_table_columns_via_jdbc(spec)
        for t in missing_tables:
            cols = fetched.get(t)
            if isinstance(cols, list) and cols:
                resolved_columns[t] = cols
        for t, c in table_comments.items():
            if isinstance(c, str) and c.strip():
                resolved_table_comments[t] = c.strip()
        if warning:
            warnings.append(warning)

    fallback_tables: List[str] = []
    entries: List[Dict[str, Any]] = []
    for table in gen["table_names"]:
        schema_name, pure_table = _split_qualified_table(str(table))
        table_name = to_pascal_case(pure_table)
        full, pk, other = _build_table_columns(gen, table, resolved_columns, fallback_tables)

        table_info = {
            "obj": {
                "name": pure_table,
                "parent": {"name": schema_name.upper()} if schema_name else {"name": ""},
                "dataType": {"typeName": ""},
            },
            "name": table_name,
            "preName": "",
            "comment": resolved_table_comments.get(table, f"{table} table"),
            "templateGroupName": template_group,
            "fullColumn": full,
            "pkColumn": pk,
            "otherColumn": other,
            "savePackageName": base_package,
            "savePath": str(project_root / output_root / package_dir),
            "saveModelName": "",
        }

        for element in elements:
            rule = _parse_template_rule(element)
            rendered = _render_with_velocity(
                template_code=element.get("code", ""),
                context_payload={
                    "tableInfo": table_info,
                    "author": author,
                    "globalMacros": macros,
                },
            )

            save_path = rendered["savePath"].strip() if rendered["savePath"] else str(project_root / output_root / package_dir / rule["save_dir"])
            file_name = rendered["fileName"].strip() if rendered["fileName"] else f"{table_name}{rule['class_suffix']}{rule['ext']}"
            target = _normalize_target_dir(save_path, project_root) / file_name
            java_package = _resolve_java_package(base_package, rule["package_suffix"])

            item = {
                "table": table,
                "module": element.get("name") or rule["module_name"],
                "java_package": java_package,
                "path": str(target),
                "exists": target.exists(),
                "template_name": element.get("name") or "template",
            }
            if include_content:
                item["content"] = rendered["rendered"]
            entries.append(item)
    if fallback_tables:
        uniq = sorted(set(fallback_tables))
        warnings.append(
            "Fallback columns used for tables: "
            + ", ".join(uniq)
            + ". Provide generation_config.table_columns or valid JDBC driver connectivity for full metadata."
        )
    return entries, warnings


def build_plan(spec: dict, include_content: bool = False) -> dict:
    _validate(spec)
    gen = spec["generation_config"]
    project_root = Path(gen.get("project_root", "."))
    output_root = Path(gen.get("output_root", "src/main/java"))
    package_dir = Path(_package_to_path(gen["base_package"]))

    files, warnings = _render_entries(spec, include_content=include_content)

    return {
        "template_group": gen["template_group"],
        "template_config": str(_resolve_template_config_path(gen["template_group"])),
        "base_output": str(project_root / output_root / package_dir),
        "file_count": len(files),
        "files": files,
        "warnings": warnings,
    }


def _execute_write(plan: dict, overwrite: bool) -> dict:
    written = []
    skipped = []

    for item in plan["files"]:
        target = Path(item["path"])
        content = item.get("content", "")
        content = _format_content_by_suffix(content, target.suffix.lower())

        if target.exists() and not overwrite:
            skipped.append(item["path"])
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written.append(item["path"])

    return {
        "written_count": len(written),
        "skipped_count": len(skipped),
        "written": written,
        "skipped": skipped,
    }


def _candidate_project_format_commands(project_root: Path) -> List[List[str]]:
    commands: List[List[str]] = []
    gradlew = project_root / "gradlew"
    mvnw = project_root / "mvnw"
    if gradlew.exists():
        commands.extend([
            [str(gradlew), "spotlessApply"],
            [str(gradlew), "format"],
        ])
    if mvnw.exists():
        commands.extend([
            [str(mvnw), "spotless:apply"],
            [str(mvnw), "fmt:format"],
        ])
    return commands


def _run_project_formatter(gen: Dict[str, Any]) -> Dict[str, Any]:
    project_root = Path(gen.get("project_root", ".")).resolve()
    custom = gen.get("project_format_command")
    commands: List[List[str]] = []

    if isinstance(custom, str) and custom.strip():
        commands.append(shlex.split(custom))
    elif isinstance(custom, list) and custom:
        for c in custom:
            if isinstance(c, str) and c.strip():
                commands.append(shlex.split(c))
    else:
        commands = _candidate_project_format_commands(project_root)

    if not commands:
        return {
            "formatter_run": False,
            "formatter_success": False,
            "formatter_command": "",
            "formatter_message": "No formatter command configured or detected.",
        }

    for cmd in commands:
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(project_root),
                capture_output=True,
                text=True,
            )
        except Exception as exc:
            continue
        if proc.returncode == 0:
            return {
                "formatter_run": True,
                "formatter_success": True,
                "formatter_command": " ".join(cmd),
                "formatter_message": "Formatter executed successfully.",
            }
    return {
        "formatter_run": True,
        "formatter_success": False,
        "formatter_command": " | ".join(" ".join(c) for c in commands),
        "formatter_message": "Formatter command(s) attempted but none succeeded.",
    }


def _format_content_by_suffix(content: str, suffix: str) -> str:
    if suffix == ".java":
        return _format_java_content(content)
    if suffix == ".xml":
        return _format_xml_content(content)
    return content


def _format_java_content(content: str) -> str:
    lines = content.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: List[str] = []
    indent = 0
    prev_blank = False
    in_javadoc = False

    for raw in lines:
        s = raw.strip()
        if not s:
            if not prev_blank:
                out.append("")
            prev_blank = True
            continue

        prev_blank = False
        if s.startswith("}"):
            indent = max(indent - 1, 0)

        # Keep shebang/velocity macros untouched but aligned with current block.
        if s.startswith("#"):
            out.append((" " * (indent * 4)) + s)
            continue

        if in_javadoc:
            if s.startswith("*/"):
                out.append((" " * (indent * 4)) + " */")
                in_javadoc = False
            elif s.startswith("*"):
                body = s[1:].strip()
                out.append((" " * (indent * 4)) + (" *" if not body else f" * {body}"))
            else:
                body = s.strip()
                out.append((" " * (indent * 4)) + (" *" if not body else f" * {body}"))
            continue

        if s.startswith("/**"):
            out.append((" " * (indent * 4)) + "/**")
            in_javadoc = True
            continue

        out.append((" " * (indent * 4)) + s)

        opens = s.count("{")
        closes = s.count("}")
        net = opens - closes
        if s.startswith("}"):
            net += 1
        if net > 0:
            indent += net
        elif net < 0:
            indent = max(indent + net, 0)

    formatted = "\n".join(out).rstrip() + "\n"
    return formatted


def _format_xml_content(content: str) -> str:
    lines = content.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: List[str] = []
    indent = 0
    prev_blank = False
    after_select_line = False

    for raw in lines:
        s = raw.strip()
        if not s:
            if not prev_blank:
                out.append("")
            prev_blank = True
            continue

        prev_blank = False
        if s.startswith("</"):
            indent = max(indent - 1, 0)

        if s.startswith("<?xml") or s.startswith("<!DOCTYPE"):
            out.append(s)
            after_select_line = False
            continue

        extra_indent = 1 if after_select_line and not s.startswith("<") else 0
        out.append((" " * ((indent + extra_indent) * 4)) + s)
        after_select_line = s == "select"

        is_open_tag = s.startswith("<") and not s.startswith("</")
        is_self_closed = s.endswith("/>") or s.startswith("<!--") and s.endswith("-->")
        has_inline_close = "</" in s and not s.startswith("</")
        if is_open_tag and not is_self_closed and not has_inline_close:
            indent += 1

    formatted = "\n".join(out).rstrip() + "\n"
    return formatted


def _prompt_type_mapping_if_needed(gen: Dict[str, Any], interactive: bool) -> None:
    if not interactive:
        return
    if "type_mapping" in gen and isinstance(gen["type_mapping"], dict):
        number_default = gen["type_mapping"].get("number_default")
        time_default = gen["type_mapping"].get("time_default")
        if number_default in {"Long", "BigDecimal"} and time_default in {"Date", "LocalDateTime"}:
            return

    if not sys.stdin.isatty():
        return

    print("Type mapping not specified. Choose defaults (press Enter for recommended):")
    num = input("1) Number -> Long (recommended)  2) Number -> BigDecimal  [1/2]: ").strip()
    tm = input("1) Time -> Date (recommended)    2) Time -> LocalDateTime [1/2]: ").strip()
    number_type = "BigDecimal" if num == "2" else "Long"
    time_type = "LocalDateTime" if tm == "2" else "Date"
    gen["type_mapping"] = {
        "number_default": number_type,
        "time_default": time_type,
    }


def _has_reusable_history(state: Dict[str, Any]) -> bool:
    db = state.get("db_connection", {}) if isinstance(state, dict) else {}
    gen = state.get("generation_config", {}) if isinstance(state, dict) else {}
    required_db = ["db_type", "url", "user", "pass"]
    required_gen = ["author", "base_package", "template_group", "project_root", "output_root"]
    return all(db.get(k) for k in required_db) and all(gen.get(k) for k in required_gen)


def _input_non_empty(prompt: str) -> str:
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print("输入不能为空，请重试。")


def _prompt_default_or_input(label: str, default_value: str) -> str:
    default_text = default_value if default_value else "<无默认>"
    print(f"{label}")
    print(f"1) 使用默认（默认值：{default_text}，回车默认）")
    print("2) 手动输入")
    choice = input("请选择 [1/2] (回车默认1): ").strip()
    if choice in {"", "1"} and default_value:
        return default_value
    return _input_non_empty("请输入值: ")


def _prompt_select_option(label: str, options: List[str], default_value: str) -> str:
    print(label)
    for i, opt in enumerate(options, start=1):
        print(f"{i}) {opt}")
    default_idx = options.index(default_value) + 1 if default_value in options else 1
    pick = input(f"请选择 [1-{len(options)}] (回车默认{default_idx}): ").strip()
    if not pick:
        return options[default_idx - 1]
    if pick.isdigit():
        idx = int(pick)
        if 1 <= idx <= len(options):
            return options[idx - 1]
    if pick in options:
        return pick
    print("输入无效，使用默认。")
    return options[default_idx - 1]


def _parse_table_names(raw: str) -> List[str]:
    tables = [x.strip() for x in raw.split(",") if x.strip()]
    return tables


def _build_spec_interactively(state: Dict[str, Any]) -> Dict[str, Any]:
    if not sys.stdin.isatty():
        raise SystemExit("interactive mode requires a TTY")

    if _has_reusable_history(state):
        print("检测到历史配置，按要求仅需输入表名，其余使用上次配置。")
        raw_tables = _input_non_empty("1) 表名（可多个，逗号分隔）: ")
        tables = _parse_table_names(raw_tables)
        if not tables:
            raise SystemExit("至少需要一个表名")
        spec = {
            "db_connection": dict(state.get("db_connection", {})),
            "generation_config": dict(state.get("generation_config", {})),
        }
        spec["generation_config"]["table_names"] = tables
        return spec

    print("未检测到完整历史配置，进入首次引导（1~9 步）。")
    # 1) 表名
    raw_tables = _input_non_empty("1) 表名（可多个，逗号分隔）: ")
    tables = _parse_table_names(raw_tables)
    if not tables:
        raise SystemExit("至少需要一个表名")

    # 2) 模板
    template_group = _prompt_select_option(
        "2) 选择生成模板",
        ["MyBatisPlus", "Custom-V2", "Custom-V3"],
        "Custom-V3",
    )

    # 3) 作者
    default_author = os.environ.get("USER", "DeveloperName")
    author = _prompt_default_or_input("3) 作者名", default_author)

    # 4) 数据库信息
    db_type = _prompt_select_option("4.1) 数据库类型", ["mysql", "oracle", "postgresql", "sqlserver"], "oracle")
    url = _prompt_default_or_input("4.2) 数据库 URL", _default_jdbc_url(db_type))
    user = _prompt_default_or_input("4.3) 数据库用户名", "emr")
    passw = _input_non_empty("4.4) 数据库密码（必填）: ")

    # 5) 驱动地址
    detected = _driver_candidates(db_type)
    default_driver_jar = detected[0][1] if detected and detected[0][1] else ""
    default_driver_class = detected[0][0] if detected and detected[0][0] else _default_driver_class(db_type)
    driver_jar = _prompt_default_or_input("5) 数据库驱动地址（JAR）", default_driver_jar)
    driver_class = _prompt_default_or_input("5) 数据库驱动类", default_driver_class)

    # 6) 代码包目录
    base_package = _prompt_default_or_input("6) 代码包目录(base_package)", "com.example.project.modules")

    # 7) 字段类型映射
    number_default = _prompt_select_option("7.1) Number 类型映射", ["Long", "BigDecimal"], "Long")
    time_default = _prompt_select_option("7.2) 时间类型映射", ["Date", "LocalDateTime"], "Date")

    # 8) 格式化要求
    run_format = _prompt_select_option("8) 是否执行项目格式化", ["否", "是"], "否") == "是"
    project_format_command = ""
    if run_format:
        project_format_command = input("8) 可选：自定义格式化命令（回车走自动探测）: ").strip()

    # 9) 输出地址
    project_root = _prompt_default_or_input("9) 文件输出地址(project_root)", str(Path.cwd()))
    output_root = _prompt_default_or_input("9) 代码输出子目录(output_root)", "src/main/java")

    gen: Dict[str, Any] = {
        "table_names": tables,
        "author": author,
        "base_package": base_package,
        "template_group": template_group,
        "project_root": project_root,
        "output_root": output_root,
        "type_mapping": {
            "number_default": number_default,
            "time_default": time_default,
        },
    }
    if project_format_command:
        gen["project_format_command"] = project_format_command
    gen["_run_project_format"] = run_format

    return {
        "db_connection": {
            "db_type": db_type,
            "url": url,
            "user": user,
            "pass": passw,
            "driver_jar": driver_jar,
            "driver_class": driver_class,
        },
        "generation_config": gen,
    }


def cmd_state(args: argparse.Namespace) -> int:
    state = _load_state()
    if args.show:
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0

    if args.save:
        if not args.spec:
            raise SystemExit("--save requires --spec")

        spec = _parse_spec(args.spec)
        merged = merge_with_state(spec, state)

        merged["updated_at"] = _now_iso()
        _save_state(merged)
        print(str(STATE_FILE))
        return 0

    raise SystemExit("state command requires --show or --save")


def cmd_plan(args: argparse.Namespace) -> int:
    state = _load_state()
    spec = _parse_spec(args.spec)
    merged = merge_with_state(spec, state)
    _prompt_type_mapping_if_needed(merged["generation_config"], args.interactive_type_mapping)
    plan = build_plan(merged, include_content=args.include_content)
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


def cmd_execute(args: argparse.Namespace) -> int:
    state = _load_state()
    spec = _parse_spec(args.spec)
    merged = merge_with_state(spec, state)
    _prompt_type_mapping_if_needed(merged["generation_config"], args.interactive_type_mapping)
    plan = build_plan(merged, include_content=True)

    result = _execute_write(plan, overwrite=args.overwrite)
    format_result = {
        "formatter_run": False,
        "formatter_success": False,
        "formatter_command": "",
        "formatter_message": "Skipped.",
    }
    if args.run_project_format:
        format_result = _run_project_formatter(merged["generation_config"])
    print(
        json.dumps(
            {
                "template_group": plan["template_group"],
                "base_output": plan["base_output"],
                **result,
                **format_result,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def cmd_interactive(args: argparse.Namespace) -> int:
    state = _load_state()
    spec = _build_spec_interactively(state)
    merged = merge_with_state(spec, state)

    plan = build_plan(merged, include_content=False)
    print(json.dumps({
        "step": "plan",
        "file_count": plan["file_count"],
        "base_output": plan["base_output"],
        "warnings": plan.get("warnings", []),
    }, ensure_ascii=False, indent=2))

    overwrite = args.overwrite
    if sys.stdin.isatty():
        ov = input("文件已存在时是否覆盖？[y/N]: ").strip().lower()
        if ov == "y":
            overwrite = True
        go = input("确认执行生成？[Y/n]: ").strip().lower()
        if go == "n":
            print("已取消执行。")
            return 0

    plan_with_content = build_plan(merged, include_content=True)
    result = _execute_write(plan_with_content, overwrite=overwrite)

    format_result = {
        "formatter_run": False,
        "formatter_success": False,
        "formatter_command": "",
        "formatter_message": "Skipped.",
    }
    if spec["generation_config"].get("_run_project_format", False):
        format_result = _run_project_formatter(merged["generation_config"])

    merged["updated_at"] = _now_iso()
    _save_state(merged)

    print(json.dumps({
        "step": "execute",
        "saved_state": str(STATE_FILE),
        **result,
        **format_result,
    }, ensure_ascii=False, indent=2))
    return 0


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="EasyCode skill helper")
    sub = parser.add_subparsers(dest="command", required=True)

    state = sub.add_parser("state", help="show or save local state")
    state.add_argument("--show", action="store_true", help="show current state")
    state.add_argument("--save", action="store_true", help="save merged state")
    state.add_argument("--spec", type=str, help="JSON payload")
    state.set_defaults(func=cmd_state)

    plan = sub.add_parser("plan", help="preview output file plan")
    plan.add_argument("--spec", type=str, required=True, help="JSON payload")
    plan.add_argument("--include-content", action="store_true", help="include rendered content in output")
    plan.add_argument("--interactive-type-mapping", action="store_true", help="prompt for type mapping when not specified")
    plan.set_defaults(func=cmd_plan)

    execute = sub.add_parser("execute", help="write rendered files")
    execute.add_argument("--spec", type=str, required=True, help="JSON payload")
    execute.add_argument("--overwrite", action="store_true", help="overwrite existing files")
    execute.add_argument("--run-project-format", action="store_true", help="run project formatter after file generation")
    execute.add_argument("--interactive-type-mapping", action="store_true", help="prompt for type mapping when not specified")
    execute.set_defaults(func=cmd_execute)

    check_driver = sub.add_parser("check-driver", help="check local JDBC driver for db type")
    check_driver.add_argument("--db-type", type=str, required=True, help="mysql/postgresql/oracle/sqlserver")
    check_driver.set_defaults(func=cmd_check_driver)

    spec_template = sub.add_parser("spec-template", help="print a runnable spec template JSON")
    spec_template.add_argument("--db-type", type=str, required=True, help="mysql/postgresql/oracle/sqlserver")
    spec_template.add_argument("--tables", type=str, help="comma-separated table names")
    spec_template.add_argument("--url", type=str, help="jdbc url")
    spec_template.add_argument("--user", type=str, help="db user")
    spec_template.add_argument("--password", type=str, help="db password")
    spec_template.add_argument("--author", type=str, help="author name")
    spec_template.add_argument("--base-package", type=str, help="base package")
    spec_template.add_argument("--template-group", type=str, help="MyBatisPlus/Custom-V2/Custom-V3")
    spec_template.add_argument("--project-root", type=str, help="project root path")
    spec_template.set_defaults(func=cmd_spec_template)

    interactive = sub.add_parser("interactive", help="interactive wizard; first time asks 1~9 steps, later only table names")
    interactive.add_argument("--overwrite", action="store_true", help="overwrite existing files by default in interactive mode")
    interactive.set_defaults(func=cmd_interactive)

    return parser


def main() -> int:
    parser = make_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
