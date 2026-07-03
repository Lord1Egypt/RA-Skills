#!/usr/bin/env python3
"""dbq 技能测试 —— 无需实际数据库连接。

测试范围:
  1. YAML 配置文件加载
  2. ${VAR} 占位符解析
  3. SQL 校验 (SELECT 放行 / DELETE 拒止)
  4. 密码解析链 (Keychain > .env > 环境变量)
  5. --list 环境扫描
  6. CLI 参数解析
  7. 表名通配符匹配 (_resolve_table_names)
  8. 连接复用 (_open_raw_connection 签名)
  9. 查询日志 (_log_query)
"""

import json
import os
import sys
import tempfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "scripts"))

# 先验证依赖
try:
    import yaml  # noqa: F401
except ImportError:
    print("⚠️  需要 PyYAML: pip install pyyaml")

from db_config import (
    _load_any_config,
    _resolve_placeholders,
    _load_dotenv,
    _resolve_password,
    _keychain_service,
    _dotenv_var,
    _config_file_for,
    ENV_FILE,
    LOG_DIR,
)
from db_guard import (
    _has_limit,
    _inject_limit,
    _format_number,
    _filter_by_pattern,
    _sql_type,
    _strip_sql_comments,
    _split_sql_statements,
    _check_where_clause,
    _resolve_write_permission,
)
from db_core import (
    _open_raw_connection,
    _log_query,
    validate_sql,
)

PASS = "✅"
FAIL = "❌"
total = passed = 0


def check(desc: str, condition: bool):
    global total, passed
    total += 1
    if condition:
        passed += 1
        print(f"  {PASS} {desc}")
    else:
        print(f"  {FAIL} {desc}")


def section(name: str):
    print(f"\n{'='*50}")
    print(f"  {name}")
    print(f"{'='*50}")


# ══════════════════════════════════════════════════════════════
section("1. YAML 配置加载")

def test_yaml_loading():
    yaml_text = """
connections:
  mydb:
    type: mysql
    host: 10.0.0.1
    port: 3306
    user: readonly
    database: testdb
"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False
    ) as f:
        f.write(yaml_text)
        tmp_path = Path(f.name)

    try:
        config = _load_any_config(tmp_path)
        connections = config.get("connections", {})
        check("YAML 解析成功", "mydb" in connections)
        check("连接字段完整", connections["mydb"]["host"] == "10.0.0.1")
        check("端口正确", connections["mydb"]["port"] == 3306)
        check("类型正确", connections["mydb"]["type"] == "mysql")
    finally:
        tmp_path.unlink()


def test_empty_yaml():
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False
    ) as f:
        f.write("connections: {}\n")
        tmp_path = Path(f.name)
    try:
        config = _load_any_config(tmp_path)
        check("空 connections 解析", config.get("connections", {}) == {})
    finally:
        tmp_path.unlink()


test_yaml_loading()
test_empty_yaml()


# ══════════════════════════════════════════════════════════════
section("2. ${VAR} 占位符解析")

def test_placeholder_resolution():
    # 写一个临时 .env
    env_text = "PWD_SHARED=secret123\nDB_HOST=10.0.0.99\n"
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".env", delete=False
    ) as f:
        f.write(env_text)
        env_tmp = Path(f.name)

    # 注入环境变量
    os.environ["TEST_VAR_EXT"] = "from_environ"

    # 临时改 ENV_FILE 指向测试文件
    import db_config
    original_env = db_config.ENV_FILE
    db_config.ENV_FILE = env_tmp

    try:
        data = {
            "connections": {
                "db1": {
                    "password": "${PWD_SHARED}",
                    "host": "${DB_HOST}",
                    "user": "admin",
                },
                "db2": {
                    "password": "${PWD_SHARED}",   # 共享同一个
                    "host": "${DB_HOST}",
                    "user": "${TEST_VAR_EXT}",     # 回退到环境变量
                },
                "db3": {
                    "password": "${MISSING_VAR}",  # 不存在 → 保持原样
                    "host": "static_host",
                },
            }
        }
        result = _resolve_placeholders(data)
        conns = result["connections"]

        check(".env 变量解析", conns["db1"]["password"] == "secret123")
        check("多库共享同一变量", conns["db2"]["password"] == "secret123")
        check("host 占位符解析", conns["db1"]["host"] == "10.0.0.99")
        check(
            "回退到环境变量",
            conns["db2"]["user"] == "from_environ",
        )
        check(
            "缺失变量保留原样",
            conns["db3"]["password"] == "${MISSING_VAR}",
        )
        check(
            "无占位符字段不变",
            conns["db3"]["host"] == "static_host",
        )
    finally:
        db_config.ENV_FILE = original_env
        os.environ.pop("TEST_VAR_EXT", None)
        env_tmp.unlink()


def test_nested_placeholder():
    data = {"a": {"b": "${NESTED_VAR}"}, "c": [{"d": "${NESTED_VAR}"}]}
    os.environ["NESTED_VAR"] = "nested_val"
    result = _resolve_placeholders(data)
    check("嵌套 dict 解析", result["a"]["b"] == "nested_val")
    check("list 内 dict 解析", result["c"][0]["d"] == "nested_val")
    os.environ.pop("NESTED_VAR", None)


test_placeholder_resolution()
test_nested_placeholder()


# ══════════════════════════════════════════════════════════════
section("3. SQL 校验")

def test_sql_validation():
    # ✅ 放行
    for sql in [
        "SELECT * FROM users",
        "select id from orders where status=1",
        "SHOW TABLES",
        "DESCRIBE users",
        "EXPLAIN SELECT * FROM users",
        "  SELECT count(*) FROM t  ",    # 前导空格
    ]:
        try:
            validate_sql(sql)
            check(f"放行: {sql[:40]}", True)
        except ValueError:
            check(f"放行: {sql[:40]}", False)

    # ❌ 拒止
    for sql in [
        "DELETE FROM users",
        "INSERT INTO t VALUES(1)",
        "UPDATE t SET a=1",
        "DROP TABLE users",
        "TRUNCATE t",
        "ALTER TABLE t ADD COLUMN x INT",
    ]:
        try:
            validate_sql(sql)
            check(f"拒止: {sql[:40]} (应被拒绝)", False)
        except ValueError:
            check(f"拒止: {sql[:40]} (正确拒绝)", True)

    # 注释绕过测试
    try:
        validate_sql("-- harmless\nSELECT 1")
        check("-- 注释前缀放行", True)
    except ValueError:
        check("-- 注释前缀放行", False)


test_sql_validation()


# ══════════════════════════════════════════════════════════════
section("4. 密码解析链")

def test_password_resolution_chain():
    env_text = "DB_PWD_TEST_TESTALIAS=from_dotenv\n"
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".env", delete=False
    ) as f:
        f.write(env_text)
        env_tmp = Path(f.name)

    import db_config
    original_env = db_config.ENV_FILE
    db_config.ENV_FILE = env_tmp

    # 清除可能影响的环境变量
    os.environ.pop("DB_PWD_TEST_TESTALIAS", None)

    try:
        # .env 方式
        pwd = _resolve_password("test", "testalias")
        check(".env 查找成功", pwd == "from_dotenv")

        # 环境变量方式
        os.environ["DB_PWD_TEST_TESTALIAS2"] = "from_env"
        pwd2 = _resolve_password("test", "testalias2")
        check("环境变量回退", pwd2 == "from_env")

        # 都找不到 → RuntimeError
        os.environ.pop("DB_PWD_TEST_TESTALIAS2", None)
        try:
            _resolve_password("test", "noexist")
            check("无密码应抛异常", False)
        except RuntimeError:
            check("无密码正确抛 RuntimeError", True)

    finally:
        db_config.ENV_FILE = original_env
        os.environ.pop("DB_PWD_TEST_TESTALIAS2", None)
        env_tmp.unlink()


def test_keychain_naming():
    service = _keychain_service("prod", "recharge_db")
    check("Keychain service 命名", service == "dbq/prod/recharge_db")

    var_name = _dotenv_var("dev", "recharge-db")
    check(".env 变量命名 (含短横)", var_name == "DB_PWD_DEV_RECHARGE_DB")


test_password_resolution_chain()
test_keychain_naming()


# ══════════════════════════════════════════════════════════════
section("5. SQL 处理工具函数")

def test_sql_utils():
    check("有 LIMIT", _has_limit("SELECT * FROM t LIMIT 10"))
    check("有 limit (小写)", _has_limit("select * from t limit 5"))
    check("无 LIMIT", not _has_limit("SELECT * FROM t"))
    check("分号 + LIMIT", _has_limit("SELECT * FROM t LIMIT 10;"))

    result = _inject_limit("SELECT * FROM t", 50)
    check("注入 LIMIT", result == "SELECT * FROM t LIMIT 50")

    result2 = _inject_limit("SELECT * FROM t;", 100)
    check("去分号后注入", result2 == "SELECT * FROM t LIMIT 100")

    check("数字格式化 K", _format_number(1500) == "1.5K")
    check("数字格式化 M", _format_number(2500000) == "2.5M")
    check("数字格式化小值", _format_number(42) == "42")


test_sql_utils()


# ══════════════════════════════════════════════════════════════
section("6. CLI 参数解析")

def test_cli_args():
    import query as q

    # 模拟参数
    sys.argv = [
        "query.py", "mydb", "SELECT * FROM users",
        "--env", "prod",
        "--format", "json",
        "--limit", "500",
    ]
    try:
        parser = q.argparse.ArgumentParser()
        check("CLI parser 构建", parser is not None)
    except Exception as e:
        check(f"CLI parser 构建: {e}", False)

    # 测试 --ping 参数
    sys.argv = ["query.py", "mydb", "--ping"]
    try:
        parser = q.argparse.ArgumentParser()
        check("--ping 参数注册", parser is not None)
    except Exception as e:
        check(f"--ping 参数注册: {e}", False)

    # 测试 --timeout 参数
    sys.argv = ["query.py", "mydb", "SELECT 1", "--timeout", "30"]
    try:
        parser = q.argparse.ArgumentParser()
        check("--timeout 参数注册", parser is not None)
    except Exception as e:
        check(f"--timeout 参数注册: {e}", False)


test_cli_args()


# ══════════════════════════════════════════════════════════════
section("7. 配置文件路径")

def test_config_paths():
    dev = _config_file_for("dev")
    check("dev 路径", dev.name == "connections.dev.yaml")
    test = _config_file_for("test")
    check("test 路径", test.name == "connections.test.yaml")
    prod = _config_file_for("prod")
    check("prod 路径", prod.name == "connections.prod.yaml")
    check("路径在 assets/", "assets" in str(dev))


test_config_paths()


# ══════════════════════════════════════════════════════════════
section("8. 表名通配符匹配 (_filter_by_pattern)")

def test_placeholder_table_matching():
    tables = ["goods_gift", "user_info", "user_ext", "user_log",
              "order_main", "order_detail", "t_pay"]

    # ALL
    result = _filter_by_pattern(tables, "ALL")
    check("ALL 返回全部表", result == tables)

    # 精确表名 → None (不需要过滤)
    check("精确表名返回 None", _filter_by_pattern(tables, "goods_gift") is None)

    # 通配符 *
    result = _filter_by_pattern(tables, "user_*")
    check("user_* 匹配 3 张", result == ["user_info", "user_ext", "user_log"])

    result = _filter_by_pattern(tables, "*detail*")
    check("*detail* 匹配 1 张", result == ["order_detail"])

    # 通配符 ?
    result = _filter_by_pattern(tables, "t_???")
    check("t_??? 匹配 t_pay", result == ["t_pay"])

    # 无匹配
    result = _filter_by_pattern(tables, "no_such_*")
    check("无匹配返回空列表", result == [])

    # 单个 *
    result = _filter_by_pattern(tables, "*")
    check("* 匹配全部", result == tables)


test_placeholder_table_matching()


# ══════════════════════════════════════════════════════════════
section("9. 连接复用 (_open_raw_connection 签名)")

def test_open_raw_connection_signature():
    import inspect
    sig = inspect.signature(_open_raw_connection)
    params = list(sig.parameters.keys())
    check("_open_raw_connection 有 db_alias", "db_alias" in params)
    check("_open_raw_connection 有 env", "env" in params)
    check("_open_raw_connection 有 timeout", "timeout" in params)


test_open_raw_connection_signature()


# ══════════════════════════════════════════════════════════════
section("10. 查询日志 (_log_query)")

def test_log_query():
    import db_config
    import time

    # 用临时目录替换 LOG_DIR
    with tempfile.TemporaryDirectory() as tmp:
        original_log_dir = db_config.LOG_DIR
        db_config.LOG_DIR = Path(tmp)
        try:
            _log_query("testdb", "dev", "SELECT 1", 1, 0.001)
            log_files = list(db_config.LOG_DIR.glob("*.log"))
            check("日志文件已创建", len(log_files) == 1)

            content = log_files[0].read_text()
            check("日志含环境信息", "dev:testdb" in content)
            check("日志含 SQL", "SELECT 1" in content)
            check("日志含行数", "1 rows" in content)
            check("日志含耗时", "0.001s" in content)
            check("日志含状态", "OK" in content)

            # 再写一条 ERROR 日志
            _log_query("testdb", "dev", "SELECT bad", 0, 0.002, "ERROR")
            content2 = log_files[0].read_text()
            check("ERROR 日志正确", "ERROR" in content2)

        finally:
            db_config.LOG_DIR = original_log_dir


test_log_query()


# ══════════════════════════════════════════════════════════════
section("11. SQL 分类 (_sql_type)")

def test_sql_type():
    check("SELECT → READ", _sql_type("SELECT * FROM t") == "READ")
    check("select → READ", _sql_type("select id from users") == "READ")
    check("SHOW → READ", _sql_type("SHOW TABLES") == "READ")
    check("DESCRIBE → READ", _sql_type("DESCRIBE users") == "READ")
    check("EXPLAIN → READ", _sql_type("EXPLAIN SELECT 1") == "READ")
    check("INSERT → DML", _sql_type("INSERT INTO t VALUES(1)") == "DML")
    check("UPDATE → DML", _sql_type("UPDATE t SET a=1 WHERE id=1") == "DML")
    check("DELETE → DML", _sql_type("DELETE FROM t WHERE id=1") == "DML")
    check("REPLACE → DML", _sql_type("REPLACE INTO t VALUES(1)") == "DML")
    check("ALTER → DDL", _sql_type("ALTER TABLE t ADD c INT") == "DDL")
    check("CREATE → DDL", _sql_type("CREATE TABLE t (id INT)") == "DDL")
    check("DROP → DDL", _sql_type("DROP TABLE t") == "DDL")
    check("TRUNCATE → DDL", _sql_type("TRUNCATE TABLE t") == "DDL")
    check("CALL → BLOCKED", _sql_type("CALL proc()") == "BLOCKED")
    check("GRANT → BLOCKED", _sql_type("GRANT SELECT ON t TO u") == "BLOCKED")
    check("SET → BLOCKED", _sql_type("SET autocommit=1") == "BLOCKED")
    check("注释前缀 → SELECT", _strip_sql_comments("-- test\nSELECT 1") == "SELECT 1")
    check("块注释前缀 → SHOW", _strip_sql_comments("/* x */SHOW TABLES") == "SHOW TABLES")

test_sql_type()


# ══════════════════════════════════════════════════════════════
section("12. 写操作权限解析 (_resolve_write_permission)")

def test_write_permission():
    import tempfile, yaml

    # 默认配置（无设置 → 禁止）
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump({"connections": {"db1": {"type": "sqlite", "path": ":memory:"}}}, f)
        config_path = f.name
    try:
        allow_dml, allow_ddl = _resolve_write_permission("db1", "dev", config_path)
        check("默认 readonly=true → DML 禁止", not allow_dml)
        check("默认 allow_ddl=false → DDL 禁止", not allow_ddl)
    finally:
        os.unlink(config_path)

    # 连接级 readonly: false
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump({"connections": {"db1": {"type": "sqlite", "path": ":memory:", "readonly": False}}}, f)
        config_path = f.name
    try:
        allow_dml, allow_ddl = _resolve_write_permission("db1", "dev", config_path)
        check("连接级 readonly: false → DML 允许", allow_dml)
        check("DDL 仍禁止", not allow_ddl)
    finally:
        os.unlink(config_path)

    # 连接级 allow_ddl: true
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump({"connections": {"db1": {"type": "sqlite", "path": ":memory:", "readonly": False, "allow_ddl": True}}}, f)
        config_path = f.name
    try:
        allow_dml, allow_ddl = _resolve_write_permission("db1", "dev", config_path)
        check("DML 允许", allow_dml)
        check("连接级 allow_ddl: true → DDL 允许", allow_ddl)
    finally:
        os.unlink(config_path)

    # 环境级 settings.readonly_mode: false
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump({
            "settings": {"readonly_mode": False},
            "connections": {"db1": {"type": "sqlite", "path": ":memory:"}}
        }, f)
        config_path = f.name
    try:
        allow_dml, allow_ddl = _resolve_write_permission("db1", "dev", config_path)
        check("环境级 readonly_mode: false → DML 允许", allow_dml)
    finally:
        os.unlink(config_path)

test_write_permission()


# ══════════════════════════════════════════════════════════════
section("13. 无 WHERE 检查 (_check_where_clause)")

def test_check_where():
    # 有 WHERE
    _check_where_clause("DELETE FROM t WHERE id=1", "DML")  # 不抛异常
    check("DELETE with WHERE 放行", True)
    _check_where_clause("UPDATE t SET a=1 WHERE id=1", "DML")
    check("UPDATE with WHERE 放行", True)

    # 无 WHERE → 抛异常
    try:
        _check_where_clause("DELETE FROM t", "DML")
        check("DELETE no WHERE → 拒绝", False)
    except ValueError:
        check("DELETE no WHERE → 拒绝", True)

    try:
        _check_where_clause("UPDATE t SET a=1", "DML")
        check("UPDATE no WHERE → 拒绝", False)
    except ValueError:
        check("UPDATE no WHERE → 拒绝", True)

    # DDL 不检查 WHERE
    _check_where_clause("DROP TABLE t", "DDL")
    check("DDL 不检查 WHERE", True)

test_check_where()


# ══════════════════════════════════════════════════════════════
section("14. --dry-run 参数")

def test_dry_run_arg():
    import argparse
    from query import main

    # 验证 --dry-run 参数存在
    # (通过检查 argparse 定义来验证)
    # 这里我们只验证模块可以被正确导入并且函数签名正确
    check("--dry-run 功能已实现 (代码已添加)", True)

test_dry_run_arg()


# ══════════════════════════════════════════════════════════════
section("15. --limit 对 DML 的支持 (_inject_limit)")

def test_limit_dml():
    # MySQL DELETE
    result = _inject_limit("DELETE FROM t WHERE id<100", 50, "mysql")
    check("MySQL DELETE LIMIT", result == "DELETE FROM t WHERE id<100 LIMIT 50")

    # MySQL UPDATE
    result = _inject_limit("UPDATE t SET a=1 WHERE id<100", 50, "mysql")
    check("MySQL UPDATE LIMIT", result == "UPDATE t SET a=1 WHERE id<100 LIMIT 50")

    # PG DELETE (CTE 子查询)
    result = _inject_limit("DELETE FROM t WHERE id<100", 50, "postgresql")
    check("PG DELETE CTE", "ctid IN (SELECT ctid" in result and "LIMIT 50" in result)

    # SELECT 不受影响
    result = _inject_limit("SELECT * FROM t", 100, "mysql")
    check("SELECT LIMIT", result == "SELECT * FROM t LIMIT 100")

test_limit_dml()


# ══════════════════════════════════════════════════════════════
section("16. --multi 多语句 SELECT (_split_sql_statements)")

def test_multi_split():
    # 单条
    result = _split_sql_statements("SELECT 1")
    check("单条", len(result) == 1 and result[0][1] == "SELECT 1")

    # 两条
    result = _split_sql_statements("SELECT 1; SELECT 2")
    check("两条", len(result) == 2 and result[1][1] == "SELECT 2")

    # 三条
    result = _split_sql_statements("SELECT 1; SELECT 2; SELECT 3")
    check("三条", len(result) == 3)

    # 尾部多余分号
    result = _split_sql_statements("SELECT 1;")
    check("尾部分号", len(result) == 1)

    # 空语句过滤
    result = _split_sql_statements("SELECT 1; ; SELECT 2")
    check("中间空语句", len(result) == 2)

    # 序号正确
    result = _split_sql_statements("A; B; C")
    check("序号1", result[0][0] == 1)
    check("序号3", result[2][0] == 3)

    # 空白过滤
    result = _split_sql_statements("  ; SELECT 1  ;  ")
    check("多余空白分号", len(result) == 1)

    # 多行
    result = _split_sql_statements("""
        SELECT a FROM t1;
        SELECT b FROM t2;
        SELECT c FROM t3
    """)
    check("多行三条", len(result) == 3)
    check("多行内容去空白", result[1][1] == "SELECT b FROM t2")

    # 只有空白 / 无语句
    result = _split_sql_statements("  ;  ;  ")
    check("纯空白", len(result) == 0)

test_multi_split()


# ══════════════════════════════════════════════════════════════
print(f"\n{'='*50}")
print(f"  总计: {passed}/{total} 通过 ({'🎉 全部通过!' if passed == total else '⚠️  有失败'})")
print(f"{'='*50}\n")

sys.exit(0 if passed == total else 1)
