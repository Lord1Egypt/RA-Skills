#!/usr/bin/env python3
"""
数据库表快速查找工具
支持模糊搜索表名、字段名，查看表结构

使用示例：
    # 搜索表名
    python3 table_finder.py --search "record"

    # 查看表结构
from cache_config import load_instance_cache, get_instance

from cache_config import load_instance_cache, get_instance

    python3 table_finder.py --desc your_table

    # 搜索字段名
    python3 table_finder.py --field "status"

    # 列出所有表
    python3 table_finder.py --list

    # 刷新缓存
    python3 table_finder.py --refresh
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from difflib import SequenceMatcher

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from archery_client import ArcheryClient, ArcheryError
from cache_config import get_tables_from_cache, save_tables_to_cache, clear_table_cache

# 全局配置目录
GLOBAL_SECRETS_FILE = Path.home() / ".archery" / "config.json"
GLOBAL_CACHE_DIR = Path.home() / ".archery" / "cache"


def load_secrets() -> dict:
    """加载凭证"""
    if GLOBAL_SECRETS_FILE.exists():
        with open(GLOBAL_SECRETS_FILE) as f:
            return json.load(f)
    return {}


def get_client(timeout: int = 30) -> ArcheryClient:
    """获取客户端"""
    secrets = load_secrets()
    base_url = secrets.get("archery_base_url", "http://your-archery-server:9123")

    if not secrets.get("archery_username"):
        raise ArcheryError(f"请先配置凭证文件: {GLOBAL_SECRETS_FILE}")

    client = ArcheryClient(
        base_url=base_url,
        timeout=timeout,
        session_file=str(GLOBAL_CACHE_DIR / "session.json"),
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

    return client


def get_tables(client: ArcheryClient, instance: str, database: str, use_cache: bool = True) -> List[str]:
    """获取表列表（带缓存）"""
    # 检查缓存
    if use_cache:
        cached_tables = get_tables_from_cache(instance, database)
        if cached_tables:
            return cached_tables

    # 查询数据库
    tables = client.list_resources(
        instance_name=instance,
        db_name=database,
        resource_type="table",
    )

    # 保存缓存
    if use_cache:
        save_tables_to_cache(instance, database, tables)

    return tables


def get_table_columns(client: ArcheryClient, instance: str, database: str, table: str) -> List[Dict]:
    """获取表字段列表"""
    result = client.query(
        instance_name=instance,
        db_name=database,
        sql_content=f"SHOW COLUMNS FROM {table}",
        limit_num=200,
    )

    columns = []
    if result.get("rows"):
        for row in result["rows"]:
            columns.append({
                "field": row[0],
                "type": row[1],
                "null": row[2] if len(row) > 2 else "",
                "key": row[3] if len(row) > 3 else "",
                "default": row[4] if len(row) > 4 else "",
            })

    return columns


def fuzzy_search(keyword: str, items: List[str], threshold: float = 0.3) -> List[tuple]:
    """模糊搜索"""
    results = []
    keyword_lower = keyword.lower()

    for item in items:
        item_lower = item.lower()

        # 包含匹配
        if keyword_lower in item_lower:
            results.append((item, 1.0))
        # 模糊匹配
        else:
            ratio = SequenceMatcher(None, keyword_lower, item_lower).ratio()
            if ratio >= threshold:
                results.append((item, ratio))

    # 按匹配度排序
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def search_tables(client: ArcheryClient, instance: str, database: str, keyword: str):
    """搜索表名"""
    print(f">>> 搜索表名: '{keyword}'\n", file=sys.stderr)

    tables = get_tables(client, instance, database)
    matches = fuzzy_search(keyword, tables)

    if not matches:
        print("未找到匹配的表")
        return

    print(f"找到 {len(matches)} 个匹配的表:\n")
    for i, (table, score) in enumerate(matches[:30], 1):
        score_str = f"[{score:.0%}]" if score < 1.0 else ""
        print(f"{i:3}. {table:40} {score_str}")

    if len(matches) > 30:
        print(f"\n... 还有 {len(matches) - 30} 个表")


def search_fields(client: ArcheryClient, instance: str, database: str, field_name: str):
    """搜索字段名"""
    print(f">>> 搜索字段名: '{field_name}'\n", file=sys.stderr)

    tables = get_tables(client, instance, database)
    found = []

    print("正在扫描表字段...", file=sys.stderr)
    for i, table in enumerate(tables[:100], 1):  # 限制扫描前100个表
        if i % 10 == 0:
            print(f"  进度: {i}/{len(tables[:100])}", file=sys.stderr)

        try:
            columns = get_table_columns(client, instance, database, table)
            for col in columns:
                if field_name.lower() in col["field"].lower():
                    found.append({
                        "table": table,
                        "field": col["field"],
                        "type": col["type"],
                    })
        except Exception:
            pass

    if not found:
        print("未找到匹配的字段")
        return

    print(f"\n找到 {len(found)} 个匹配的字段:\n")
    print(f"{'表名':<40} {'字段名':<30} {'类型':<20}")
    print("-" * 90)

    for item in found[:50]:
        print(f"{item['table']:<40} {item['field']:<30} {item['type']:<20}")

    if len(found) > 50:
        print(f"\n... 还有 {len(found) - 50} 个字段")


def describe_table(client: ArcheryClient, instance: str, database: str, table: str):
    """查看表结构"""
    print(f">>> 表结构: {table}\n", file=sys.stderr)

    columns = get_table_columns(client, instance, database, table)

    if not columns:
        print("表不存在或无权限访问")
        return

    print(f"字段总数: {len(columns)}\n")
    print(f"{'字段名':<35} {'类型':<20} {'允许空':<8} {'键':<8}")
    print("-" * 80)

    for col in columns:
        print(f"{col['field']:<35} {col['type']:<20} {col['null']:<8} {col['key']:<8}")

    # 统计索引
    keys = [col for col in columns if col["key"]]
    if keys:
        print(f"\n索引字段: {', '.join(col['field'] for col in keys)}")


def list_all_tables(client: ArcheryClient, instance: str, database: str):
    """列出所有表"""
    tables = get_tables(client, instance, database)

    print(f"\n数据库 {database} 中的表 ({len(tables)} 个):\n")

    # 按前缀分组
    groups = {}
    for table in sorted(tables):
        # 提取前缀（下划线前的部分）
        prefix = table.split("_")[0] if "_" in table else table[:3]
        if prefix not in groups:
            groups[prefix] = []
        groups[prefix].append(table)

    for prefix in sorted(groups.keys()):
        print(f"\n【{prefix}】({len(groups[prefix])} 个)")
        for table in groups[prefix][:10]:
            print(f"  - {table}")
        if len(groups[prefix]) > 10:
            print(f"  ... 还有 {len(groups[prefix]) - 10} 个")


def main():
    parser = argparse.ArgumentParser(
        description="数据库表快速查找工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 搜索表名
  %(prog)s --search "record"

  # 查看表结构
  %(prog)s --desc your_table

  # 搜索字段名
  %(prog)s --field "status"

  # 列出所有表
  %(prog)s --list

  # 指定实例和数据库
  %(prog)s --instance "your-instance" --db "your-db" --search "table"

  # 刷新缓存
  %(prog)s --refresh
        """,
    )

    parser.add_argument("--instance", "-i", default=None, help="实例名")
    parser.add_argument("--db", "-d", default=None, help="数据库名")
    parser.add_argument("--search", "-s", help="搜索表名（模糊匹配）")
    parser.add_argument("--field", "-f", help="搜索字段名")
    parser.add_argument("--desc", help="查看表结构")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有表")
    parser.add_argument("--refresh", "-r", action="store_true", help="刷新缓存")
    parser.add_argument("--timeout", "-t", type=int, default=30, help="超时时间（秒）")

    args = parser.parse_args()

    # 检查参数
    if not any([args.search, args.field, args.desc, args.list, args.refresh]):
        parser.print_help()
        return 1

    try:
        # 刷新缓存
        if args.refresh:
            clear_table_cache()
            return 0

        # 获取客户端
        client = get_client(timeout=args.timeout)

        # 从配置获取默认实例和数据库
        if not args.instance or not args.db:
            secrets = load_secrets()
            args.instance = args.instance or secrets.get("default_instance", "your-instance")
            args.db = args.db or secrets.get("default_database", "your-database")

        # 执行操作
        if args.list:
            list_all_tables(client, args.instance, args.db)

        elif args.search:
            search_tables(client, args.instance, args.db, args.search)

        elif args.field:
            search_fields(client, args.instance, args.db, args.field)

        elif args.desc:
            describe_table(client, args.instance, args.db, args.desc)

        return 0

    except ArcheryError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"异常: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
