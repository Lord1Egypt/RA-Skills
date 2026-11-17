#!/usr/bin/env python3
"""
Archery 表去重查询脚本
查找表中基于唯一约束字段的重复数据，并生成需要删除的记录列表

使用场景：
- TiDB 老版本唯一约束必须包含分区键，导致数据重复
- MySQL 分表合并到单表后出现重复
- 数据迁移导致的重复记录
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from archery_client import ArcheryClient, ArcheryError
from cache_config import load_instances, get_instance, get_aliases

# 全局配置目录
GLOBAL_SECRETS_FILE = Path.home() / ".archery" / "config.json"
GLOBAL_CACHE_DIR = Path.home() / ".archery" / "cache"


def load_secrets() -> dict:
    """加载凭证"""
    if GLOBAL_SECRETS_FILE.exists():
        with open(GLOBAL_SECRETS_FILE) as f:
            return json.load(f)
    return {}


def get_client(timeout: int = 60) -> ArcheryClient:
    """获取已认证的客户端"""
    secrets = load_secrets()
    base_url = secrets.get("archery_base_url", "http://your-server:9123")

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
        print(">>> 登录成功", file=sys.stderr)

    return client


def analyze_duplicates(
    client: ArcheryClient,
    instance_name: str,
    db_name: str,
    table_name: str,
    unique_fields: list[str],
    date_field: str = "create_time",
    start_date: str = None,
    end_date: str = None,
    output_file: str = None,
    generate_delete: bool = True,
):
    """
    分析表中的重复数据

    Args:
        client: Archery 客户端
        instance_name: 实例名
        db_name: 数据库名
        table_name: 表名
        unique_fields: 唯一约束字段列表（不含分区键）
        date_field: 日期/时间字段（用于分区和过滤）
        start_date: 开始日期
        end_date: 结束日期
        output_file: 输出文件路径
        generate_delete: 是否生成 DELETE 语句
    """

    print(f"\n{'='*80}")
    print(f"分析表 {table_name} 的重复数据")
    print(f"{'='*80}")
    print(f"唯一约束字段: {unique_fields}")
    print(f"日期字段: {date_field}")
    print(f"时间范围: {start_date} ~ {end_date or '今天'}")

    # 1. 先获取每日数据统计
    print(f"\n>>> 统计每日数据分布...")
    unique_key_expr = "CONCAT(" + ", '|', ".join(unique_fields) + ")"

    if start_date:
        date_filter = f"WHERE {date_field} >= '{start_date}'"
        if end_date:
            date_filter += f" AND {date_field} < '{end_date}'"
    else:
        date_filter = ""

    sql_daily = f"""
    SELECT
        DATE({date_field}) as create_date,
        COUNT(*) as total_count,
        COUNT(DISTINCT {unique_key_expr}) as unique_count
    FROM {table_name}
    {date_filter}
    GROUP BY DATE({date_field})
    ORDER BY create_date
    """

    result = client.query(
        instance_name=instance_name,
        db_name=db_name,
        sql_content=sql_daily,
        limit_num=1000,
    )

    if not result.get("rows"):
        print("未找到数据")
        return

    print("\n每日数据统计:")
    print("-" * 60)

    total_dup = 0
    dates_with_dup = []

    for row in result["rows"]:
        date, total, unique = row
        dup_count = total - unique
        print(f"{date}: 总记录 {total}, 唯一组合 {unique}, 重复记录 {dup_count}")
        if dup_count > 0:
            total_dup += dup_count
            dates_with_dup.append(date)

    print(f"\n总重复记录: {total_dup}")

    if not dates_with_dup:
        print("\n✅ 没有重复数据！")
        return

    # 2. 查询需要删除的重复记录 ID
    print(f"\n>>> 查询需要删除的重复记录...")

    all_dup_records = []

    for date in dates_with_dup:
        sql_dup = f"""
        SELECT id, {', '.join(unique_fields)}, {date_field}
        FROM (
            SELECT id, {', '.join(unique_fields)}, {date_field},
                   ROW_NUMBER() OVER (PARTITION BY {', '.join(unique_fields)} ORDER BY {date_field}) as rn
            FROM {table_name}
            WHERE DATE({date_field}) = '{date}'
        ) t
        WHERE rn > 1
        ORDER BY {', '.join(unique_fields)}, {date_field}
        """

        try:
            result = client.query(
                instance_name=instance_name,
                db_name=db_name,
                sql_content=sql_dup,
                limit_num=1000,
            )

            for row in result["rows"]:
                all_dup_records.append(row)

            print(f"{date}: 找到 {len(result['rows'])} 条需删除")

        except ArcheryError as e:
            print(f"{date}: 查询失败 - {e}", file=sys.stderr)

    print(f"\n总计需删除: {len(all_dup_records)} 条")

    if not all_dup_records:
        print("\n✅ 没有需要删除的记录！")
        return

    # 3. 输出结果
    columns = ["id"] + unique_fields + [date_field]

    if output_file:
        # CSV 格式
        csv_file = output_file.replace(".sql", ".csv") if ".sql" in output_file else output_file + ".csv"
        with open(csv_file, "w") as f:
            f.write(",".join(columns) + "\n")
            for row in all_dup_records:
                f.write(",".join(str(v) for v in row) + "\n")
        print(f"\n✅ 重复记录详情已保存到: {csv_file}")

        # DELETE 语句
        if generate_delete:
            sql_file = output_file if ".sql" in output_file else output_file + ".sql"
            ids = [str(row[0]) for row in all_dup_records]

            with open(sql_file, "w") as f:
                f.write(f"-- 删除 {table_name} 表中的重复记录\n")
                f.write(f"-- 唯一约束字段: {unique_fields}\n")
                f.write(f"-- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"-- 删除记录数: {len(ids)}\n")
                f.write(f"-- 时间范围: {start_date or '最早'} ~ {end_date or '今天'}\n\n")

                # 分批 DELETE（每批 50 条）
                batch_size = 50
                for i in range(0, len(ids), batch_size):
                    batch_ids = ids[i:i + batch_size]
                    f.write(f"DELETE FROM {table_name} WHERE id IN ({','.join(batch_ids)});\n")

            print(f"✅ DELETE 语句已保存到: {sql_file}")
    else:
        # 直接输出
        print("\n需删除的记录详情 (前20条):")
        print("-" * 80)
        for row in all_dup_records[:20]:
            record = dict(zip(columns, row))
            print(f"ID: {record['id']}, {', '.join(f'{k}={v}' for k, v in record.items() if k != 'id')}")

        if len(all_dup_records) > 20:
            print(f"... 还有 {len(all_dup_records) - 20} 条")

    return all_dup_records


def main():
    cached_instances = load_instances()

    parser = argparse.ArgumentParser(
        description="Archery 表去重查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 查询表中重复数据
  %(prog)s --alias alias1 --table your_table \
    --unique-fields field1,field2 \
    --date-field create_time \
    --start-date 2026-01-01

  # 指定输出文件
  %(prog)s --alias alias1 --table your_table \
    --unique-fields field1,field2 \
    --output /tmp/duplicates.sql

  # 不生成 DELETE 语句
  %(prog)s --alias alias1 --table your_table \
    --unique-fields field1,field2 \
    --no-delete

实例别名请在 cache_config.py 中配置。
        """,
    )

    parser.add_argument("--instance", "-i", default=None, help="实例名")
    parser.add_argument("--db", "-d", default=None, help="数据库名")
    parser.add_argument("--alias", "-a", choices=get_aliases(), help="实例别名")
    parser.add_argument("--table", "-t", required=True, help="表名")
    parser.add_argument("--unique-fields", "-u", required=True, help="唯一约束字段（逗号分隔，不含分区键）")
    parser.add_argument("--date-field", default="create_time", help="日期/时间字段")
    parser.add_argument("--start-date", "-s", help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--end-date", "-e", help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--no-delete", action="store_true", help="不生成 DELETE 语句")
    parser.add_argument("--timeout", type=int, default=120, help="查询超时（秒）")

    args = parser.parse_args()

    # 处理别名
    if args.alias:
        args.instance, args.db = get_instance(args.alias)
    elif not args.instance or not args.db:
        secrets = load_secrets()
        args.instance = args.instance or secrets.get("default_instance")
        args.db = args.db or secrets.get("default_database")

    if not args.instance or not args.db:
        print("错误: 请指定实例和数据库，或使用别名", file=sys.stderr)
        return 1

    unique_fields = [f.strip() for f in args.unique_fields.split(",")]

    try:
        client = get_client(timeout=args.timeout)

        analyze_duplicates(
            client=client,
            instance_name=args.instance,
            db_name=args.db,
            table_name=args.table,
            unique_fields=unique_fields,
            date_field=args.date_field,
            start_date=args.start_date,
            end_date=args.end_date,
            output_file=args.output,
            generate_delete=not args.no_delete,
        )

        return 0

    except ArcheryError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"异常: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())