#!/usr/bin/env python3
"""dbq 配置管理 —— 路径常量 / 密码解析 / 环境配置加载 / 连接获取。"""

from __future__ import annotations

import json as _json_mod
import os
import re
import subprocess
import sys
from pathlib import Path

# ── 路径常量 ─────────────────────────────────────────────────

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"
ENV_FILE = ASSETS_DIR / ".env"
LOG_DIR = SKILL_DIR / "logs"

DEFAULT_ENV = os.environ.get("DB_QUERY_DEFAULT_ENV", "dev")

# ── 配置模板（内嵌，不依赖 assets/ 目录文件）─────────────────
# ClawHub 安全策略不收录 .yaml / .env 文件，模板内容内嵌到代码中，
# 通过 --init-config 命令生成，无需 cp -n assets/*.example

_CONFIG_TEMPLATES = {
    "connections.dev.yaml": r"""# 开发环境数据库连接配置
# ⚠️  三种密码管理方式（值字段支持 ${VAR} 占位符）:
#   1. 不写 password 字段 → 通过 Keychain/.env/环境变量 约定查找 DB_PWD_DEV_{ALIAS}
#   2. password: ${MY_SHARED_PASS} → 从 assets/.env 或环境变量中解析（多库共用推荐）
#   3. password: ${ENV_VAR} → 直接引用父进程环境变量
#
# 查询: python scripts/query.py sqlite_test "SELECT 1"

connections:
  # --- SQLite 默认测试连接（零依赖，开箱即用）─────────
  sqlite_test:
    type: sqlite
    path: ":memory:"
    readonly: false

  # --- 方式 1: 不写 password，靠脚本自动查找 ───
  # recharge_db:
  #   type: mysql
  #   host: 10.18.122.60
  #   port: 3306
  #   user: readonly_dev
  #   database: recharge
  #   charset: utf8mb4
  #   connect_timeout: 10
  #   readonly: true

  # --- 方式 2: ${VAR} 占位，多库共享密码（推荐） ───
  # recharge_db:
  #   type: mysql
  #   host: 10.18.122.60
  #   port: 3306
  #   user: readonly
  #   password: ${PWD_DEV}
  #   database: recharge
  #
  # pay_db:
  #   type: mysql
  #   host: 10.18.122.60
  #   port: 3306
  #   user: readonly
  #   password: ${PWD_DEV}
  #   database: pay
""",

    "connections.test.yaml": r"""# 测试环境数据库连接配置
# 用法同 connections.dev.yaml

connections:
  # recharge_db:
  #   type: mysql
  #   host: 10.18.122.61
  #   port: 3306
  #   user: readonly
  #   password: ${PWD_TEST}
  #   database: recharge
  #
  # pay_db:
  #   type: mysql
  #   host: 10.18.122.61
  #   port: 3306
  #   user: readonly
  #   password: ${PWD_TEST}
  #   database: pay
""",

    "connections.prod.yaml": r"""# 生产环境数据库连接配置（独立文件，建议 chmod 600）
# 用法同 connections.dev.yaml

connections:
  # recharge_db:
  #   type: mysql
  #   host: 10.19.xx.xx
  #   port: 3306
  #   user: readonly
  #   password: ${PWD_PROD}
  #   database: recharge
  #
  # pay_db:
  #   type: mysql
  #   host: 10.19.xx.xx
  #   port: 3306
  #   user: readonly
  #   password: ${PWD_PROD}
  #   database: pay
""",

    ".env": r"""# 数据库密码配置文件
# ⚠️  包含敏感信息，不要提交到 Git！
# 编辑填入实际密码后: chmod 600 .env
#
# 两种使用方式:
#
# --- 方式 1: 按约定命名（脚本自动查找） ---
# 规则: DB_PWD_{ENV}_{ALIAS大写短横换下划线}
# DB_PWD_DEV_RECHARGE_DB=dev_password_here
# DB_PWD_TEST_RECHARGE_DB=test_password_here
#
# --- 方式 2: 自定义变量名 + YAML ${VAR} 引用（多库共享推荐） ---
# PWD_DEV=shared_dev_password
# PWD_TEST=shared_test_password
# PWD_PROD=shared_prod_password
# 在 connections.{env}.yaml 中用 password: ${PWD_PROD} 引用
""",
}


def _handle_init_config():
    """生成配置模板文件到 assets/ 目录，已存在则跳过。"""
    created, skipped = [], []
    for filename, content in _CONFIG_TEMPLATES.items():
        target = ASSETS_DIR / filename
        if target.exists():
            skipped.append(filename)
        else:
            target.write_text(content, encoding="utf-8")
            created.append(filename)
            # prod 配置自动设置 600 权限
            if "prod" in filename:
                try:
                    target.chmod(0o600)
                except OSError:
                    pass

    if created:
        print(f"✅ 已创建 {len(created)} 个配置文件:")
        for f in created:
            print(f"   assets/{f}")
    if skipped:
        print(f"⏭️  跳过 {len(skipped)} 个（已存在）:")
        for f in skipped:
            print(f"   assets/{f}")
    print("\n下一步: 编辑 assets/connections.dev.yaml 填入你的数据库连接信息。")
    print("密码管理: Keychain 自动查找 > .env 文件 > 环境变量")


def _config_file_for(env: str) -> Path:
    """env → connections.{env}.yaml"""
    return ASSETS_DIR / f"connections.{env}.yaml"


# ── YAML 依赖检查 ───────────────────────────────────────────

try:
    import yaml
except ImportError:
    yaml = None


# ── 密码解析 ────────────────────────────────────────────────
# 优先级: macOS Keychain > .env 文件 > 父进程环境变量
# Keychain 条目: service=dbq/{env}/{alias}
# .env 变量名:   DB_PWD_{ENV}_{ALIAS}  (全大写，短横换下划线)

def _keychain_service(env: str, alias: str) -> str:
    return f"dbq/{env}/{alias}"


def _dotenv_var(env: str, alias: str) -> str:
    raw = f"{env}_{alias}".upper().replace("-", "_")
    return f"DB_PWD_{raw}"


def _load_dotenv(path: Path) -> dict:
    """解析 .env 文件为 dict"""
    env = {}
    if not path.exists():
        return env
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            k, _, v = line.partition("=")
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            env[k] = v
    return env


def _resolve_password(env: str, alias: str) -> str:
    """按优先级获取密码"""
    service = _keychain_service(env, alias)
    env_var = _dotenv_var(env, alias)

    # 1 — macOS Keychain
    if sys.platform == "darwin":
        try:
            result = subprocess.run(
                [
                    "security", "find-generic-password",
                    "-a", "dbq",
                    "-s", service,
                    "-w",
                ],
                capture_output=True, text=True, timeout=5,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    # 2 — .env 文件
    dotenv = _load_dotenv(ENV_FILE)
    if env_var in dotenv:
        return dotenv[env_var]

    # 3 — 父进程环境变量
    if env_var in os.environ:
        return os.environ[env_var]

    raise RuntimeError(
        f"无法获取 [{alias}] ({env} 环境) 的密码。请通过以下任一方式配置:\n"
        f"  1. Keychain: security add-generic-password -a dbq -s {service} -w '密码'\n"
        f"  2. assets/.env: {env_var}=密码\n"
        f"  3. 环境变量: export {env_var}=密码"
    )


# ── 环境配置加载 ────────────────────────────────────────────

def _resolve_placeholders(data):
    """递归替换数据中所有字符串值里的 ${VAR} 占位符。

    查找顺序: .env 文件 → 父进程环境变量
    未找到的占位符保持原样并打印警告。
    """
    dotenv = _load_dotenv(ENV_FILE)

    def _replace(val):
        if not isinstance(val, str):
            return val

        def _lookup(match):
            var = match.group(1)
            if var in dotenv:
                return dotenv[var]
            if var in os.environ:
                return os.environ[var]
            print(
                f"[WARN] 占位符 ${{{var}}} 在 .env 和环境变量中均未找到，保持原样",
                file=sys.stderr,
            )
            return match.group(0)
        return re.sub(r"\$\{(\w+)\}", _lookup, val)

    return _walk_replace(data, _replace)


def _walk_replace(data, fn):
    """递归遍历 dict/list，对每个字符串值应用 fn"""
    if isinstance(data, dict):
        return {k: _walk_replace(v, fn) for k, v in data.items()}
    elif isinstance(data, list):
        return [_walk_replace(v, fn) for v in data]
    else:
        return fn(data)


def _load_yaml_file(path: Path) -> dict:
    if yaml is None:
        raise ImportError(
            "需要 PyYAML 来读取 YAML 配置。请安装: pip install pyyaml"
        )
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _load_json_file(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return _json_mod.load(f) or {}


def _load_any_config(path: Path) -> dict:
    """加载 YAML 或 JSON 配置文件"""
    if not path.exists():
        raise FileNotFoundError(f"配置文件不存在: {path}")
    suffix = path.suffix.lower()
    if suffix in (".yaml", ".yml"):
        return _load_yaml_file(path)
    elif suffix == ".json":
        return _load_json_file(path)
    raise ValueError(f"不支持的配置格式: {suffix}")


def load_env_config(env: str, config_override: str | None = None) -> dict:
    """加载环境的连接配置，返回 connections 字典。

    1. --config 指定 → 加载该文件
    2. --env dev|test|prod → connections.{env}.yaml

    加载后会对所有值进行 ${VAR} 占位符替换，优先查 .env 文件，其次查环境变量。
    """
    if config_override:
        path = Path(config_override)
        if not path.is_absolute():
            path = ASSETS_DIR / path
    else:
        path = _config_file_for(env)

    if not path.exists():
        if config_override:
            raise FileNotFoundError(f"配置文件不存在: {path}")
        raise FileNotFoundError(
            f"环境 [{env}] 配置文件不存在: {path.name}\n"
            f"请从 assets/{path.stem}.example 复制并编辑。"
        )
    config = _load_any_config(path)
    connections = config.get("connections", {})
    return _resolve_placeholders(connections)


# ── 连接获取 ────────────────────────────────────────────────

def get_connection(db_alias: str, env: str, config_override: str | None = None) -> dict:
    """获取单个数据库连接信息（含密码注入）"""
    connections = load_env_config(env, config_override)
    if db_alias not in connections:
        available = list(connections.keys())
        raise ValueError(
            f"未找到数据库别名 [{db_alias}] ({env} 环境)\n"
            f"可用别名: {', '.join(available) if available else '(无)'}"
        )
    conn = dict(connections[db_alias])  # 浅拷贝，避免污染缓存
    db_type = conn.get("type", "").lower()
    if db_type in ("sqlite", "sqlite3"):
        # SQLite 只需要 type + path，默认 :memory:
        conn.setdefault("path", ":memory:")
    else:
        required = ["type", "host", "port", "user", "database"]
        missing = [k for k in required if k not in conn]
        if missing:
            raise ValueError(
                f"数据库 {db_alias} 配置不完整，缺少字段: {', '.join(missing)}"
            )
        # 密码: YAML 中已解析的 ${VAR} 优先，否则走约定查找
        if not conn.get("password"):
            conn["password"] = _resolve_password(env, db_alias)
    return conn
