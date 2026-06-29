#!/usr/bin/env python3
"""
维度建模 DDL 生成器 — Dimension Model DDL Generator
支持星型模型(Snowflake/BigQuery/Redshift/StarRocks/ClickHouse/Databricks/Postgres)
和 Data Vault 2.0 建模范式。
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ── 平台 SQL 方言配置 ──────────────────────────────────────────

PLATFORM_DIALECTS = {
    "bigquery": {
        "pk": "STRING",
        "fk": "INT64",
        "int": "INT64",
        "decimal": "NUMERIC",
        "text": "STRING",
        "date": "DATE",
        "timestamp": "TIMESTAMP",
        "boolean": "BOOL",
        "json": "JSON",
        "array": "ARRAY<STRING>",
        "scd2_struct": "STRUCT<valid_from TIMESTAMP, valid_to TIMESTAMP, is_current BOOL>",
        "auto_increment": "INT64",  # BigQuery uses GENERATE_UUID() for surrogate keys
        "surrogate_key": "GENERATE_UUID()",
        "table_comment": "OPTIONS(description=\"{comment}\")",
        "partition": "PARTITION BY DATE({col})",
        "cluster": "CLUSTER BY {cols}",
        "create_syntax": "CREATE OR REPLACE TABLE",
        "merge_syntax": "MERGE",
    },
    "snowflake": {
        "pk": "VARCHAR",
        "fk": "NUMBER",
        "int": "NUMBER",
        "decimal": "NUMBER(38,2)",
        "text": "VARCHAR(16777216)",
        "date": "DATE",
        "timestamp": "TIMESTAMP_NTZ",
        "boolean": "BOOLEAN",
        "json": "VARIANT",
        "array": "ARRAY",
        "scd2_struct": "OBJECT",
        "auto_increment": "NUMBER AUTOINCREMENT",
        "surrogate_key": "SEQ4()",
        "table_comment": "COMMENT = '{comment}'",
        "partition": "",  # Auto micro-partitions
        "cluster": "CLUSTER BY ({cols})",
        "create_syntax": "CREATE OR REPLACE TABLE",
        "merge_syntax": "MERGE INTO",
    },
    "redshift": {
        "pk": "VARCHAR(256)",
        "fk": "BIGINT",
        "int": "BIGINT",
        "decimal": "DECIMAL(18,2)",
        "text": "VARCHAR(65535)",
        "date": "DATE",
        "timestamp": "TIMESTAMP",
        "boolean": "BOOLEAN",
        "json": "SUPER",
        "array": "SUPER",
        "scd2_struct": "SUPER",
        "auto_increment": "BIGINT IDENTITY(1,1)",
        "surrogate_key": "IDENTITY(1,1)",
        "table_comment": "COMMENT ON TABLE {table} IS '{comment}'",
        "partition": "DISTKEY({col})",
        "cluster": "SORTKEY({cols})",
        "create_syntax": "CREATE TABLE IF NOT EXISTS",
        "merge_syntax": "MERGE",
    },
    "starrocks": {
        "pk": "VARCHAR",
        "fk": "BIGINT",
        "int": "BIGINT",
        "decimal": "DECIMAL(18,2)",
        "text": "STRING",
        "date": "DATE",
        "timestamp": "DATETIME",
        "boolean": "BOOLEAN",
        "json": "JSON",
        "array": "ARRAY<STRING>",
        "scd2_struct": "JSON",
        "auto_increment": "BIGINT",
        "surrogate_key": "uuid()",
        "table_comment": "COMMENT \"{comment}\"",
        "partition": "PARTITION BY RANGE({col})",
        "cluster": "",
        "create_syntax": "CREATE TABLE IF NOT EXISTS",
        "merge_syntax": "",  # Use INSERT OVERWRITE
    },
    "clickhouse": {
        "pk": "String",
        "fk": "Int64",
        "int": "Int64",
        "decimal": "Decimal(18,2)",
        "text": "String",
        "date": "Date",
        "timestamp": "DateTime",
        "boolean": "Bool",
        "json": "JSON",
        "array": "Array(String)",
        "scd2_struct": "Tuple(valid_from DateTime, valid_to DateTime, is_current UInt8)",
        "auto_increment": "Int64",
        "surrogate_key": "generateUUIDv4()",
        "table_comment": "COMMENT '{comment}'",
        "partition": "PARTITION BY toYYYYMM({col})",
        "cluster": "ORDER BY ({cols})",
        "create_syntax": "CREATE TABLE IF NOT EXISTS",
        "merge_syntax": "ALTER TABLE ... UPDATE",
    },
    "databricks": {
        "pk": "STRING",
        "fk": "BIGINT",
        "int": "BIGINT",
        "decimal": "DECIMAL(18,2)",
        "text": "STRING",
        "date": "DATE",
        "timestamp": "TIMESTAMP",
        "boolean": "BOOLEAN",
        "json": "STRING",
        "array": "ARRAY<STRING>",
        "scd2_struct": "STRUCT<valid_from: TIMESTAMP, valid_to: TIMESTAMP, is_current: BOOLEAN>",
        "auto_increment": "BIGINT",
        "surrogate_key": "uuid()",
        "table_comment": "COMMENT '{comment}'",
        "partition": "PARTITIONED BY ({col})",
        "cluster": "CLUSTER BY ({cols})",
        "create_syntax": "CREATE TABLE IF NOT EXISTS",
        "merge_syntax": "MERGE INTO",
    },
    "postgres": {
        "pk": "VARCHAR",
        "fk": "BIGINT",
        "int": "BIGINT",
        "decimal": "NUMERIC(18,2)",
        "text": "TEXT",
        "date": "DATE",
        "timestamp": "TIMESTAMPTZ",
        "boolean": "BOOLEAN",
        "json": "JSONB",
        "array": "JSONB",
        "scd2_struct": "JSONB",
        "auto_increment": "BIGSERIAL",
        "surrogate_key": "nextval('{table}_sk_seq')",
        "table_comment": "COMMENT ON TABLE {table} IS '{comment}'",
        "partition": "PARTITION BY RANGE ({col})",
        "cluster": "",
        "create_syntax": "CREATE TABLE IF NOT EXISTS",
        "merge_syntax": "INSERT ... ON CONFLICT",
    },
}

# ── SCD 策略 ─────────────────────────────────────────────────────

SCD_STRATEGIES = {
    1: {
        "name": "Type 1 — 覆盖 (Overwrite)",
        "description": "直接更新维度属性，不保留历史",
        "extra_cols": [],
        "strategy_sql": "UPDATE {table} SET {updates} WHERE {business_key} = :bk",
    },
    2: {
        "name": "Type 2 — 新增行 (Add Row)",
        "description": "新增行保留历史，通过 valid_from/valid_to 标记有效期",
        "extra_cols": [
            ("sk_id", "pk"),           # 代理键
            ("valid_from", "timestamp"),
            ("valid_to", "timestamp"),
            ("is_current", "boolean"),
        ],
        "strategy_sql": "INSERT + UPDATE is_current=0, valid_to=NOW()",
    },
    3: {
        "name": "Type 3 — 新增列 (Add Column)",
        "description": "新增列保留上一个值",
        "extra_cols": [
            ("previous_value", "text"),
            ("effective_date", "date"),
        ],
        "strategy_sql": "UPDATE {table} SET previous_value = {col}, {col} = :new_val",
    },
    "hybrid": {
        "name": "Hybrid (Type 1 + Type 2)",
        "description": "大部分属性 Type 1 覆盖，关键属性 Type 2 保留历史",
        "extra_cols": [
            ("sk_id", "pk"),
            ("valid_from", "timestamp"),
            ("valid_to", "timestamp"),
            ("is_current", "boolean"),
        ],
        "strategy_sql": "根据属性分类混合处理",
    },
}

# ── 事实表类型 ────────────────────────────────────────────────────

FACT_TYPES = {
    "transaction": "事务事实表 — 记录业务事件，粒度=单次事件",
    "periodic_snapshot": "周期快照事实表 — 按固定周期记录状态，粒度=周期+维度",
    "accumulating_snapshot": "累积快照事实表 — 记录有明确生命周期的业务流程",
    "factless": "无事实的事实表 — 记录事件发生/条件满足，无数值度量",
}


def parse_args():
    parser = argparse.ArgumentParser(description="维度建模 DDL 生成器")
    parser.add_argument("--business-domain", type=str, default="business",
                        help="业务域名称")
    parser.add_argument("--facts", type=str, required=True,
                        help="事实表定义，格式 'orders:订单事实,order_items:订单明细'")
    parser.add_argument("--dimensions", type=str, required=True,
                        help="维度表定义，格式 'dim_customer:客户,dim_product:产品'")
    parser.add_argument("--schema", type=str, default="star",
                        choices=["star", "snowflake", "vault"],
                        help="建模范式")
    parser.add_argument("--scd-type", type=str, default="2",
                        choices=["1", "2", "3", "hybrid"],
                        help="缓慢变化维度策略")
    parser.add_argument("--platform", type=str, default="bigquery",
                        choices=list(PLATFORM_DIALECTS.keys()),
                        help="目标数仓平台")
    parser.add_argument("--output", type=str, default="ddl/",
                        help="输出目录")
    parser.add_argument("--schema-name", type=str, default="dwh",
                        help="目标 schema 名称")
    parser.add_argument("--format", type=str, default="sql",
                        choices=["sql", "dbt"],
                        help="输出格式")
    return parser.parse_args()


def get_type(dialect: dict, typ: str) -> str:
    """将通用类型映射到平台特定类型."""
    return dialect.get(typ, typ.upper())


def build_dimension_ddl(
    dim_name: str,
    dim_desc: str,
    dialect: dict,
    scd_type: str,
    platform: str,
    schema_name: str,
    scd_extra_cols: list,
    output_format: str,
) -> str:
    """生成维度表 DDL."""
    table_name = dim_name if dim_name.startswith("dim_") else f"dim_{dim_name}"
    full_name = f"`{schema_name}`.`{table_name}`" if platform in ("bigquery",) else f"{schema_name}.{table_name}"

    cols = []
    # 代理键
    if scd_type in ("2", "hybrid"):
        cols.append(f"    sk_{dim_name.replace('dim_', '')}_id {get_type(dialect, 'pk')} NOT NULL,")
        cols.append(f"    -- 代理键 (Surrogate Key)")
    # 业务键
    cols.append(f"    {dim_name.replace('dim_', '')}_bk {get_type(dialect, 'pk')} NOT NULL,")
    cols.append(f"    -- 业务自然键 (Business Key)")
    # 核心属性
    cols.append(f"    {dim_name.replace('dim_', '')}_name {get_type(dialect, 'text')},")
    cols.append(f"    {dim_name.replace('dim_', '')}_code {get_type(dialect, 'text')},")
    cols.append(f"    description {get_type(dialect, 'text')},")
    # SCD 追踪列
    if scd_type in ("2", "hybrid"):
        cols.append(f"    valid_from {get_type(dialect, 'timestamp')} NOT NULL,")
        cols.append(f"    valid_to {get_type(dialect, 'timestamp')} DEFAULT '9999-12-31 23:59:59',")
        cols.append(f"    is_current {get_type(dialect, 'boolean')} DEFAULT TRUE,")
    elif scd_type == "3":
        cols.append(f"    effective_date {get_type(dialect, 'date')},")
    # 审计列
    cols.append(f"    created_at {get_type(dialect, 'timestamp')} DEFAULT CURRENT_TIMESTAMP(),")
    cols.append(f"    updated_at {get_type(dialect, 'timestamp')} DEFAULT CURRENT_TIMESTAMP(),")
    cols.append(f"    source_system {get_type(dialect, 'text')}")

    pk_col = f"sk_{dim_name.replace('dim_', '')}_id" if scd_type in ("2", "hybrid") else f"{dim_name.replace('dim_', '')}_bk"
    pk_line = f"    PRIMARY KEY ({pk_col}) NOT ENFORCED" if platform == "bigquery" else f"    PRIMARY KEY ({pk_col})"

    comment = dialect.get("table_comment", "COMMENT '{comment}'")
    if "{comment}" in comment:
        comment_line = comment.format(comment=f"维度表 — {dim_desc} | SCD Type {scd_type}")
    else:
        comment_line = comment.format(table=full_name, comment=f"维度表 — {dim_desc} | SCD Type {scd_type}")

    ddl = f"""-- ============================================================
-- 维度表: {full_name}
-- 描述: {dim_desc}
-- SCD 策略: {SCD_STRATEGIES[scd_type]['name']}
-- 平台: {platform}
-- ============================================================

{dialect['create_syntax']} {full_name} (
{chr(10).join(cols)}
{pk_line}
)
{comment_line};
"""
    return ddl


def build_fact_ddl(
    fact_name: str,
    fact_desc: str,
    dimensions: list,
    dialect: dict,
    platform: str,
    schema_name: str,
    output_format: str,
) -> str:
    """生成事实表 DDL."""
    table_name = fact_name if fact_name.startswith("fact_") else f"fact_{fact_name}"
    full_name = f"`{schema_name}`.`{table_name}`" if platform in ("bigquery",) else f"{schema_name}.{table_name}"

    cols = []
    cols.append(f"    -- 维度外键")
    for dim in dimensions:
        dim_clean = dim.replace("dim_", "")
        cols.append(f"    fk_{dim_clean}_sk {get_type(dialect, 'fk')} NOT NULL,")

    cols.append(f"    -- 日期维度")
    cols.append(f"    fk_date_sk {get_type(dialect, 'fk')} NOT NULL,")

    cols.append(f"    -- 度量值 (Measures)")
    cols.append(f"    quantity {get_type(dialect, 'int')} DEFAULT 0,")
    cols.append(f"    unit_price {get_type(dialect, 'decimal')},")
    cols.append(f"    total_amount {get_type(dialect, 'decimal')},")
    cols.append(f"    discount_amount {get_type(dialect, 'decimal')} DEFAULT 0,")
    cols.append(f"    net_amount {get_type(dialect, 'decimal')},")

    cols.append(f"    -- 审计列")
    cols.append(f"    created_at {get_type(dialect, 'timestamp')} DEFAULT CURRENT_TIMESTAMP(),")
    cols.append(f"    source_batch_id {get_type(dialect, 'text')},")
    cols.append(f"    etl_job_id {get_type(dialect, 'text')}")

    # 分区和聚簇
    partition_clause = ""
    cluster_clause = ""
    if platform == "bigquery":
        partition_clause = f"\nPARTITION BY DATE(fk_date_sk)"
        cluster_clause = f"\nCLUSTER BY fk_{dimensions[0].replace('dim_', '')}_sk" if dimensions else ""
    elif platform == "clickhouse":
        partition_clause = f"\nPARTITION BY toYYYYMM(created_at)"
        cluster_clause = f"\nORDER BY (fk_date_sk)" if dimensions else ""
    elif platform == "starrocks":
        partition_clause = f"\nPARTITION BY RANGE(fk_date_sk)"

    comment = dialect.get("table_comment", "COMMENT '{comment}'")
    if "{comment}" in comment:
        comment_line = comment.format(comment=fact_desc)
    else:
        comment_line = comment.format(table=full_name, comment=fact_desc)

    ddl = f"""-- ============================================================
-- 事实表: {full_name}
-- 描述: {fact_desc}
-- 类型: Transaction Fact
-- 粒度: 每笔交易一行
-- 平台: {platform}
-- ============================================================

{dialect['create_syntax']} {full_name} (
{chr(10).join(cols)}
)
{partition_clause}{cluster_clause};
{comment_line}
"""
    return ddl


def build_date_dimension_ddl(dialect: dict, platform: str, schema_name: str) -> str:
    """生成日期维度表 DDL."""
    full_name = f"`{schema_name}`.`dim_date`" if platform in ("bigquery",) else f"{schema_name}.dim_date"

    comment = dialect.get("table_comment", "COMMENT '{comment}'")
    if "{comment}" in comment:
        comment_line = comment.format(comment="日期维度表 — 覆盖10年日期范围")
    else:
        comment_line = comment.format(table=full_name, comment="日期维度表 — 覆盖10年日期范围")

    ddl = f"""-- ============================================================
-- 日期维度表: {full_name}
-- 描述: 标准日期维度，覆盖10年日期范围
-- ============================================================

{dialect['create_syntax']} {full_name} (
    date_sk           {get_type(dialect, 'fk')} NOT NULL,      -- 日期代理键 (YYYYMMDD)
    full_date         {get_type(dialect, 'date')} NOT NULL,    -- 完整日期
    year              {get_type(dialect, 'int')},              -- 年份
    quarter           {get_type(dialect, 'int')},              -- 季度 (1-4)
    quarter_name      {get_type(dialect, 'text')},             -- Q1/Q2/Q3/Q4
    month             {get_type(dialect, 'int')},              -- 月份 (1-12)
    month_name        {get_type(dialect, 'text')},             -- 月份名称
    month_abbr        {get_type(dialect, 'text')},             -- 月份缩写
    week_of_year      {get_type(dialect, 'int')},              -- ISO 周数
    day_of_week       {get_type(dialect, 'int')},              -- 星期几 (1-7)
    day_name          {get_type(dialect, 'text')},             -- 星期名称
    day_name_abbr     {get_type(dialect, 'text')},             -- 星期缩写
    is_weekend        {get_type(dialect, 'boolean')},          -- 是否周末
    is_holiday        {get_type(dialect, 'boolean')},          -- 是否节假日
    fiscal_year       {get_type(dialect, 'int')},              -- 财年
    fiscal_quarter    {get_type(dialect, 'int')},              -- 财季
    PRIMARY KEY (date_sk) NOT ENFORCED
)
{comment_line};
"""
    return ddl


def build_vault_ddl(
    business_domain: str,
    facts: list,
    dimensions: list,
    dialect: dict,
    platform: str,
    schema_name: str,
) -> str:
    """生成 Data Vault 2.0 模型 DDL."""
    ddl = f"""-- ============================================================
-- Data Vault 2.0 模型: {business_domain}
-- 平台: {platform}
-- ============================================================

-- Hubs (业务核心实体)
"""
    for dim in dimensions:
        dim_clean = dim.replace("dim_", "")
        hub_name = f"hub_{dim_clean}"
        ddl += f"""
CREATE TABLE {schema_name}.{hub_name} (
    {dim_clean}_hash_key {get_type(dialect, 'pk')} NOT NULL,
    {dim_clean}_bk {get_type(dialect, 'text')} NOT NULL,
    load_date {get_type(dialect, 'timestamp')} NOT NULL,
    record_source {get_type(dialect, 'text')} NOT NULL,
    PRIMARY KEY ({dim_clean}_hash_key)
);
"""
    # Links
    ddl += f"""
-- Links (关系)
"""
    for fact in facts:
        fact_clean = fact.replace("fact_", "")
        ddl += f"""
CREATE TABLE {schema_name}.lnk_{fact_clean} (
    {fact_clean}_hash_key {get_type(dialect, 'pk')} NOT NULL,
"""
        for dim in dimensions:
            dim_clean = dim.replace("dim_", "")
            ddl += f"    {dim_clean}_hash_key {get_type(dialect, 'fk')} NOT NULL,\n"
        ddl += f"""    load_date {get_type(dialect, 'timestamp')} NOT NULL,
    record_source {get_type(dialect, 'text')} NOT NULL,
    PRIMARY KEY ({fact_clean}_hash_key)
);
"""
    # Satellites
    ddl += f"""
-- Satellites (描述性属性)
"""
    for dim in dimensions:
        dim_clean = dim.replace("dim_", "")
        ddl += f"""
CREATE TABLE {schema_name}.sat_{dim_clean} (
    {dim_clean}_hash_key {get_type(dialect, 'fk')} NOT NULL,
    load_date {get_type(dialect, 'timestamp')} NOT NULL,
    load_end_date {get_type(dialect, 'timestamp')},
    record_source {get_type(dialect, 'text')} NOT NULL,
    {dim_clean}_name {get_type(dialect, 'text')},
    hash_diff {get_type(dialect, 'text')} NOT NULL,
    PRIMARY KEY ({dim_clean}_hash_key, load_date)
);
"""
    return ddl


def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)

    dialect = PLATFORM_DIALECTS[args.platform]
    scd_type = args.scd_type
    if scd_type.isdigit():
        scd_type = int(scd_type)

    # 解析输入
    facts = []
    for f in args.facts.split(","):
        parts = f.strip().split(":")
        if len(parts) == 2:
            facts.append((parts[0].strip(), parts[1].strip()))
        else:
            facts.append((parts[0].strip(), "事实表"))

    dimensions = []
    for d in args.dimensions.split(","):
        parts = d.strip().split(":")
        if len(parts) == 2:
            dimensions.append((parts[0].strip(), parts[1].strip()))
        else:
            dimensions.append((parts[0].strip(), "维度表"))

    dim_names = [d[0] for d in dimensions]
    scd_extra = SCD_STRATEGIES[scd_type].get("extra_cols", [])

    output_file = os.path.join(args.output, f"{args.business_domain}_ddl.sql")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"-- ============================================================\n")
        f.write(f"-- 数据仓库维度模型 DDL\n")
        f.write(f"-- 业务域: {args.business_domain}\n")
        f.write(f"-- 建模范式: {args.schema.upper()}\n")
        f.write(f"-- SCD 策略: {SCD_STRATEGIES[scd_type]['name']}\n")
        f.write(f"-- 目标平台: {args.platform}\n")
        f.write(f"-- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- ============================================================\n\n")

        if args.schema in ("star", "snowflake"):
            # 日期维度
            f.write(build_date_dimension_ddl(dialect, args.platform, args.schema_name))
            f.write("\n")

            # 维度表
            for dim_name, dim_desc in dimensions:
                f.write(build_dimension_ddl(
                    dim_name, dim_desc, dialect, scd_type,
                    args.platform, args.schema_name, scd_extra,
                    args.output_format
                ))
                f.write("\n")

            # 事实表
            for fact_name, fact_desc in facts:
                f.write(build_fact_ddl(
                    fact_name, fact_desc, dim_names, dialect,
                    args.platform, args.schema_name, args.output_format
                ))
                f.write("\n")

        elif args.schema == "vault":
            f.write(build_vault_ddl(
                args.business_domain, facts, dimensions,
                dialect, args.platform, args.schema_name
            ))

    print(f"✅ DDL 已生成: {output_file}")
    print(f"📋 包含 {len(dimensions)} 个维度表, {len(facts)} 个事实表")
    print(f"🏗️  建模范式: {args.schema.upper()}")
    print(f"📅 SCD 策略: {SCD_STRATEGIES[scd_type]['name']}")
    print(f"☁️  目标平台: {args.platform}")

    # 生成模型元数据
    meta = {
        "business_domain": args.business_domain,
        "schema": args.schema,
        "scd_type": str(scd_type),
        "platform": args.platform,
        "schema_name": args.schema_name,
        "generated_at": datetime.now().isoformat(),
        "tables": {
            "dimensions": [{"name": d[0], "description": d[1]} for d in dimensions],
            "facts": [{"name": f[0], "description": f[1]} for f in facts],
        }
    }
    meta_file = os.path.join(args.output, f"{args.business_domain}_metadata.json")
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    print(f"📄 元数据已保存: {meta_file}")


if __name__ == "__main__":
    main()
