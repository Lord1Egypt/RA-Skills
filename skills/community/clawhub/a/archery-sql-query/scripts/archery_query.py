#!/usr/bin/env python3
"""
Archery 快速查询脚本（项目级）
支持实例别名缓存，自动管理配置
"""

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from archery_client import ArcheryClient, ArcheryError
from cache_config import load_instances, get_instance, get_aliases, save_instances, save_tables_to_cache

# 默认配置
DEFAULT_BASE_URL = "http://your-archery-server:9123"

# 全局配置目录（唯一位置）
GLOBAL_CACHE_DIR = Path.home() / ".archery" / "cache"
GLOBAL_SECRETS_FILE = Path.home() / ".archery" / "config.json"
SESSION_FILE = GLOBAL_CACHE_DIR / "session.json"

# 查询模板
QUERY_TEMPLATES = {
    "failed_records": {
        "desc": "查询失败的记录",
        "sql": "SELECT * FROM your_table WHERE status != 'success' ORDER BY id DESC LIMIT {limit}",
        "default_params": {"limit": 20},
    },
    "recent_records": {
        "desc": "查询最近的记录",
        "sql": "SELECT * FROM your_table ORDER BY id DESC LIMIT {limit}",
        "default_params": {"limit": 20},
    },
    "by_field": {
        "desc": "按字段查询",
        "sql": "SELECT * FROM your_table WHERE your_field = '{value}' LIMIT {limit}",
        "default_params": {"limit": 5},
        "required_params": ["value"],
    },
}


def load_secrets() -> dict:
    """加载凭证和配置"""
    if GLOBAL_SECRETS_FILE.exists():
        with open(GLOBAL_SECRETS_FILE) as f:
            return json.load(f)

    return {
        "archery_username": "",
        "archery_password": "",
        "archery_base_url": DEFAULT_BASE_URL,
    }


def get_secrets_file() -> Path:
    """获取配置文件路径"""
    return GLOBAL_SECRETS_FILE


def get_base_url() -> str:
    """获取 Archery Base URL"""
    secrets = load_secrets()
    return secrets.get("archery_base_url", DEFAULT_BASE_URL)


def get_client(timeout: int = 60) -> ArcheryClient:
    """获取已认证的客户端"""
    secrets = load_secrets()
    base_url = get_base_url()

    if not secrets.get("archery_username") or not secrets.get("archery_password"):
        raise ArcheryError(
            f"请先配置凭证文件: {GLOBAL_SECRETS_FILE}\n\n"
            f"配置示例:\n"
            f"  {{\n"
            f"    \"archery_username\": \"your_username\",\n"
            f"    \"archery_password\": \"your_password\",\n"
            f"    \"archery_base_url\": \"http://your-server:9123\"\n"
            f"  }}\n"
        )

    client = ArcheryClient(
        base_url=base_url,
        timeout=timeout,
        session_file=str(SESSION_FILE),
    )

    try:
        client.load_session()
    except Exception:
        pass

    try:
        client.ensure_session()
    except ArcheryError:
        print(">>> 登录中...", file=sys.stderr)
        client.login(
            username=secrets["archery_username"],
            password=secrets["archery_password"],
        )
        print(">>> 登录成功", file=sys.stderr)

    return client


def format_output(result: dict, format: str = "table") -> str:
    """格式化输出结果"""
    if not result.get("rows"):
        return "未找到数据"

    rows = result["rows"]
    columns = result.get("column_list", [])

    if format == "json":
        output = []
        for row in rows:
            output.append(dict(zip(columns, row)))
        return json.dumps(output, indent=2, ensure_ascii=False)

    # table 格式
    lines = []
    col_widths = [len(str(col)) for col in columns]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)[:50]))

    header = " | ".join(str(col).ljust(col_widths[i]) for i, col in enumerate(columns))
    lines.append(header)
    lines.append("-" * len(header))

    for row in rows[:20]:
        cells = []
        for i, val in enumerate(row):
            val_str = str(val) if val is not None else "NULL"
            if len(val_str) > 50:
                val_str = val_str[:47] + "..."
            cells.append(val_str.ljust(col_widths[i]))
        lines.append(" | ".join(cells))

    if len(rows) > 20:
        lines.append(f"... 还有 {len(rows) - 20} 行")

    lines.append(f"\n共 {len(rows)} 行，耗时 {result.get('query_time', 0):.2f}s")

    return "\n".join(lines)


def main():
    # 从缓存加载实例别名
    cached_instances = load_instances()
    
    parser = argparse.ArgumentParser(
        description="Archery 快速查询工具（项目级）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用别名查询（需先配置实例别名）
  %(prog)s --alias alias1 "SELECT * FROM your_table LIMIT 5"

  # 指定实例和数据库
  %(prog)s --instance "your-instance" --db "your-db" "SELECT ..."

  # 使用模板
  %(prog)s --template failed_records --params limit=10

实例别名请在 cache_config.py 或 instances.json 中配置。
        """,
    )

    parser.add_argument("sql", nargs="?", help="SQL 查询语句")
    parser.add_argument("--instance", "-i", default=None, help="实例名")
    parser.add_argument("--db", "-d", default=None, help="数据库名")
    parser.add_argument("--alias", "-a", choices=get_aliases(), help="实例别名（从缓存）")
    parser.add_argument("--limit", "-l", type=int, default=100, help="返回行数限制")
    parser.add_argument("--format", "-f", choices=["table", "json"], default="table", help="输出格式")
    parser.add_argument("--timeout", "-t", type=int, default=60, help="查询超时时间")
    parser.add_argument("--template", choices=QUERY_TEMPLATES.keys(), help="使用查询模板")
    parser.add_argument("--params", help="模板参数（格式: key=value,key2=value2）")
    parser.add_argument("--desc", metavar="TABLE", help="查看表结构")
    parser.add_argument("--list-dbs", action="store_true", help="列出数据库")
    parser.add_argument("--list-tables", metavar="DB", help="列出表")

    args = parser.parse_args()

    try:
        # 处理别名
        if args.alias:
            instance_name, db_name = get_instance(args.alias)
            args.instance = instance_name
            args.db = db_name

        # 从配置获取默认值
        if not args.instance or not args.db:
            secrets = load_secrets()
            args.instance = args.instance or secrets.get("default_instance", "your-instance")
            args.db = args.db or secrets.get("default_database", "your-database")

        # 自动缓存实例配置（当直接使用 --instance 和 --db 时）
        # 检查是否已存在该配置，避免重复添加
        if args.instance and args.db and not args.alias:
            cached_instances = load_instances()
            existing_key = None
            for key, value in cached_instances.items():
                if isinstance(value, list) and len(value) == 2:
                    if value[0] == args.instance and value[1] == args.db:
                        existing_key = key
                        break

            if not existing_key:
                # 静默添加到缓存
                cache_key = f"{args.instance}|{args.db}"
                cached_instances[cache_key] = [args.instance, args.db]
                save_instances(cached_instances)

        client = get_client(timeout=args.timeout)

        if args.list_dbs:
            dbs = client.list_resources(
                instance_name=args.instance,
                db_name="",
                resource_type="database",
            )
            print("\n".join(dbs))
            return 0

        if args.list_tables:
            tables = client.list_resources(
                instance_name=args.instance,
                db_name=args.list_tables,
                resource_type="table",
            )

            # 保存到缓存
            save_tables_to_cache(args.instance, args.list_tables, tables)

            print(f"\n数据库 {args.list_tables} 中的表 ({len(tables)} 个):")
            for table in sorted(tables):
                print(f"  - {table}")
            return 0

        if args.desc:
            result = client.query(
                instance_name=args.instance,
                db_name=args.db,
                sql_content=f"SHOW COLUMNS FROM {args.desc}",
                limit_num=100,
            )
            print(format_output(result, args.format))
            return 0

        if args.template:
            template = QUERY_TEMPLATES[args.template]
            params = template["default_params"].copy()

            if args.params:
                for param in args.params.split(","):
                    key, value = param.split("=")
                    params[key.strip()] = value.strip()

            sql = template["sql"].format(**params)
            print(f">>> 模板: {template['desc']}", file=sys.stderr)
            print(f">>> SQL: {sql}", file=sys.stderr)

            result = client.query(
                instance_name=args.instance,
                db_name=args.db,
                sql_content=sql,
                limit_num=args.limit,
            )

            print(format_output(result, args.format))
            return 0

        if args.sql:
            result = client.query(
                instance_name=args.instance,
                db_name=args.db,
                sql_content=args.sql,
                limit_num=args.limit,
            )

            print(format_output(result, args.format))
            return 0

        parser.print_help()
        return 1

    except ArcheryError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"异常: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
