#!/usr/bin/env python3
"""
数据质量检查引擎 — Data Quality Checker
支持 6 大质量维度的自动化规则生成，输出 Great Expectations / SQL / dbt test / Soda 格式。
"""

import argparse
import json
import os
import sys
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Any

# ── 质量维度定义 ──────────────────────────────────────────────────

QUALITY_DIMENSIONS = {
    "completeness": {
        "name": "完整性 (Completeness)",
        "description": "检查必填字段是否为空",
        "severity": "CRITICAL",
        "checks": ["not_null", "missing_rate", "row_count_check"],
        "default_threshold": {"not_null_pct": 99.0, "missing_max_pct": 1.0},
    },
    "uniqueness": {
        "name": "唯一性 (Uniqueness)",
        "description": "检查主键/业务键是否唯一",
        "severity": "CRITICAL",
        "checks": ["unique", "duplicate_count", "pk_composite_unique"],
        "default_threshold": {"unique_pct": 100.0, "max_duplicates": 0},
    },
    "validity": {
        "name": "有效性 (Validity)",
        "description": "检查数据格式/范围是否符合业务规则",
        "severity": "HIGH",
        "checks": ["regex_match", "range_check", "enum_values", "date_format", "email_format"],
        "default_threshold": {"valid_pct": 95.0},
    },
    "consistency": {
        "name": "一致性 (Consistency)",
        "description": "检查跨表/跨系统数据是否一致",
        "severity": "HIGH",
        "checks": ["referential_integrity", "cross_table_match", "aggregate_consistency"],
        "default_threshold": {"match_pct": 98.0},
    },
    "timeliness": {
        "name": "及时性 (Timeliness)",
        "description": "检查数据是否按时到达",
        "severity": "MEDIUM",
        "checks": ["freshness_check", "max_delay", "expected_arrival"],
        "default_threshold": {"max_delay_hours": 4, "on_time_pct": 99.0},
    },
    "accuracy": {
        "name": "准确性 (Accuracy)",
        "description": "检查数据是否反映真实业务值",
        "severity": "HIGH",
        "checks": ["statistical_outlier", "zscore_check", "variance_from_avg", "sum_check"],
        "default_threshold": {"zscore_threshold": 3.0, "deviation_pct": 10.0},
    },
    "freshness": {
        "name": "新鲜度 (Freshness)",
        "description": "检查数据最新更新时间",
        "severity": "MEDIUM",
        "checks": ["max_data_age", "stale_partition_check", "no_new_data_alert"],
        "default_threshold": {"max_age_hours": 24, "empty_partitions": 0},
    },
    "volume": {
        "name": "数据量 (Volume)",
        "description": "检查数据量是否异常波动",
        "severity": "MEDIUM",
        "checks": ["row_count_anomaly", "volume_change_pct", "zero_row_check"],
        "default_threshold": {"anomaly_threshold_pct": 50, "min_rows": 1},
    },
    "custom": {
        "name": "自定义 (Custom SQL)",
        "description": "用户自定义 SQL 检查",
        "severity": "HIGH",
        "checks": ["custom_sql"],
        "default_threshold": {},
    },
}

def parse_args():
    parser = argparse.ArgumentParser(description="数据质量检查引擎")
    parser.add_argument("--table", type=str, required=True,
                        help="目标表名 (schema.table)")
    parser.add_argument("--platform", type=str, default="bigquery",
                        choices=["bigquery", "snowflake", "redshift", "starrocks", "clickhouse", "databricks", "postgres"])
    parser.add_argument("--checks", type=str, default="completeness,uniqueness,validity",
                        help="检查类型，逗号分隔")
    parser.add_argument("--format", type=str, default="sql",
                        choices=["great_expectations", "sql", "dbt_test", "soda"])
    parser.add_argument("--threshold-file", type=str, default=None,
                        help="阈值配置文件 (YAML)")
    parser.add_argument("--output", type=str, default="dq_checks/",
                        help="输出目录")
    parser.add_argument("--columns", type=str, default=None,
                        help="指定检查列，逗号分隔（默认全部）")
    parser.add_argument("--pk-column", type=str, default="id",
                        help="主键列名")
    parser.add_argument("--date-column", type=str, default="created_at",
                        help="日期列名")
    return parser.parse_args()


def load_thresholds(file_path: str | None) -> dict:
    """加载阈值配置文件."""
    thresholds = {}
    if file_path and os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            thresholds = yaml.safe_load(f) or {}
    return thresholds


def generate_sql_checks(
    table: str,
    checks: List[str],
    platform: str,
    pk_column: str,
    date_column: str,
    columns: List[str] | None,
    thresholds: dict,
) -> str:
    """生成纯 SQL 格式的数据质量检查."""

    # 平台特定函数
    platform_funcs = {
        "bigquery": {"current_ts": "CURRENT_TIMESTAMP()", "array_agg": "ARRAY_AGG", "safe_div": "SAFE_DIVIDE"},
        "snowflake": {"current_ts": "CURRENT_TIMESTAMP()", "array_agg": "ARRAY_AGG", "safe_div": "DIV0"},
        "redshift": {"current_ts": "GETDATE()", "array_agg": "LISTAGG", "safe_div": "NULLIF"},
        "postgres": {"current_ts": "NOW()", "array_agg": "ARRAY_AGG", "safe_div": "NULLIF"},
    }
    funcs = platform_funcs.get(platform, platform_funcs["bigquery"])
    ct = funcs["current_ts"]

    sql = f"""-- ============================================================
-- Data Quality Checks for: {table}
-- Platform: {platform}
-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- ============================================================

"""

    # 1. 完整性检查
    if "completeness" in checks:
        t = thresholds.get("completeness", {})
        null_pct = t.get("not_null_pct", 99.0)
        sql += f"""
-- [COMPLETENESS] Not Null Rate Check
SELECT
    '{table}' AS table_name,
    'completeness' AS check_type,
    'not_null_rate' AS check_name,
    COUNT(*) AS total_rows,
    SUM(CASE WHEN {pk_column} IS NULL THEN 1 ELSE 0 END) AS null_count,
    ROUND(100.0 * SUM(CASE WHEN {pk_column} IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS null_pct,
    CASE WHEN ROUND(100.0 * SUM(CASE WHEN {pk_column} IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) > {100 - null_pct}
         THEN 'FAIL' ELSE 'PASS' END AS status
FROM {table};
"""
        if columns:
            sql += f"""
-- [COMPLETENESS] Column-level missing rate
SELECT
"""
            col_checks = []
            for col in columns:
                col_checks.append(
                    f"    ROUND(100.0 * SUM(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS {col}_missing_pct"
                )
            sql += ",\n".join(col_checks)
            sql += f"\nFROM {table};\n"

    # 2. 唯一性检查
    if "uniqueness" in checks:
        sql += f"""
-- [UNIQUENESS] Primary Key Uniqueness
SELECT
    '{table}' AS table_name,
    'uniqueness' AS check_type,
    COUNT(*) AS total_rows,
    COUNT(DISTINCT {pk_column}) AS distinct_pks,
    COUNT(*) - COUNT(DISTINCT {pk_column}) AS duplicate_count,
    CASE WHEN COUNT(*) = COUNT(DISTINCT {pk_column})
         THEN 'PASS' ELSE 'FAIL' END AS status
FROM {table};
"""
        sql += f"""
-- [UNIQUENESS] Duplicate Detail (Top 100)
SELECT {pk_column}, COUNT(*) AS dup_count
FROM {table}
GROUP BY {pk_column}
HAVING COUNT(*) > 1
ORDER BY dup_count DESC
LIMIT 100;
"""

    # 3. 有效性检查
    if "validity" in checks:
        sql += f"""
-- [VALIDITY] Range Check Example
-- 检查数值列是否为合理范围
"""
        if columns:
            for col in columns:
                sql += f"""
-- Check: {col} IS NOT NULL AND {col} >= 0
SELECT
    '{col}' AS column_name,
    COUNT(*) AS total,
    SUM(CASE WHEN {col} < 0 OR {col} IS NULL THEN 1 ELSE 0 END) AS invalid_count,
    ROUND(100.0 * SUM(CASE WHEN {col} < 0 OR {col} IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS invalid_pct
FROM {table};
"""
        sql += f"""
-- [VALIDITY] Date Format Check
SELECT
    COUNT(*) AS total,
    SUM(CASE WHEN SAFE.PARSE_DATE('%Y-%m-%d', CAST({date_column} AS STRING)) IS NULL THEN 1 ELSE 0 END) AS invalid_date_count
FROM {table};
"""

    # 4. 及时性/新鲜度检查
    if "timeliness" in checks or "freshness" in checks:
        t = thresholds.get("timeliness", thresholds.get("freshness", {}))
        max_hours = t.get("max_delay_hours", t.get("max_age_hours", 24))
        sql += f"""
-- [TIMELINESS] Data Freshness Check
SELECT
    '{table}' AS table_name,
    'freshness' AS check_type,
    MAX({date_column}) AS latest_record,
    TIMESTAMP_DIFF({ct}, MAX({date_column}), HOUR) AS hours_since_latest,
    CASE WHEN TIMESTAMP_DIFF({ct}, MAX({date_column}), HOUR) <= {max_hours}
         THEN 'PASS' ELSE 'FAIL' END AS status
FROM {table};
"""

    # 5. 数据量检查
    if "volume" in checks:
        t = thresholds.get("volume", {})
        min_rows = t.get("min_rows", 1)
        sql += f"""
-- [VOLUME] Row Count Check
SELECT
    '{table}' AS table_name,
    'volume' AS check_type,
    COUNT(*) AS row_count,
    CASE WHEN COUNT(*) >= {min_rows} THEN 'PASS' ELSE 'FAIL' END AS status
FROM {table};
"""

    # 6. 统计异常检查
    if "accuracy" in checks:
        t = thresholds.get("accuracy", {})
        zscore_threshold = t.get("zscore_threshold", 3.0)
        if columns:
            for col in columns:
                sql += f"""
-- [ACCURACY] Z-Score Outlier Check for {col}
WITH stats AS (
    SELECT
        AVG({col}) AS mean_val,
        STDDEV({col}) AS std_val
    FROM {table}
    WHERE {col} IS NOT NULL
),
outliers AS (
    SELECT
        {pk_column},
        {col},
        ({col} - stats.mean_val) / NULLIF(stats.std_val, 0) AS z_score
    FROM {table}, stats
    WHERE {col} IS NOT NULL
      AND ABS(({col} - stats.mean_val) / NULLIF(stats.std_val, 0)) > {zscore_threshold}
)
SELECT
    COUNT(*) AS outlier_count,
    ROUND(100.0 * COUNT(*) / NULLIF((SELECT COUNT(*) FROM {table}), 0), 2) AS outlier_pct,
    CASE WHEN COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM {table}), 0) < 5.0
         THEN 'PASS' ELSE 'WARN' END AS status
FROM outliers;
"""

    return sql


def generate_great_expectations(
    table: str,
    checks: List[str],
    platform: str,
    pk_column: str,
    date_column: str,
    columns: List[str] | None,
    thresholds: dict,
) -> str:
    """生成 Great Expectations suite YAML."""
    suite_name = table.replace(".", "_").replace("`", "")
    yml = f"""# Great Expectations Expectation Suite
# Generated for: {table} ({platform})
# Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

suite_name: {suite_name}_quality_suite
data_asset_type: Table

expectations:
"""
    # 完整性
    if "completeness" in checks:
        t = thresholds.get("completeness", {})
        expect_pct = t.get("not_null_pct", 99.0) / 100.0
        yml += f"""
  # === COMPLETENESS ===
  - expectation_type: expect_column_values_to_not_be_null
    kwargs:
      column: {pk_column}
      mostly: {expect_pct}
    meta:
      dimension: completeness
      severity: critical
"""
        if columns:
            for col in columns:
                yml += f"""  - expectation_type: expect_column_values_to_not_be_null
    kwargs:
      column: {col}
      mostly: {expect_pct}
    meta:
      dimension: completeness
"""

    # 唯一性
    if "uniqueness" in checks:
        yml += f"""
  # === UNIQUENESS ===
  - expectation_type: expect_column_values_to_be_unique
    kwargs:
      column: {pk_column}
    meta:
      dimension: uniqueness
      severity: critical
"""

    # 有效性
    if "validity" in checks:
        yml += f"""
  # === VALIDITY ===
  - expectation_type: expect_column_values_to_be_of_type
    kwargs:
      column: {pk_column}
      type_: varchar
      or_other_types: [int, integer]
    meta:
      dimension: validity
"""

    # 新鲜度
    if "freshness" in checks or "timeliness" in checks:
        yml += f"""
  # === FRESHNESS ===
  - expectation_type: expect_column_max_to_be_between
    kwargs:
      column: {date_column}
      min_value: "{{{{ now() - timedelta(days=1) }}}}"
      max_value: "{{{{ now() }}}}"
    meta:
      dimension: freshness
      severity: warning
"""

    # 数据量
    if "volume" in checks:
        t = thresholds.get("volume", {})
        min_rows = t.get("min_rows", 1)
        yml += f"""
  # === VOLUME ===
  - expectation_type: expect_table_row_count_to_be_between
    kwargs:
      min_value: {min_rows}
      max_value: 1000000000
    meta:
      dimension: volume
"""

    return yml


def generate_dbt_tests(
    table: str,
    checks: List[str],
    platform: str,
    pk_column: str,
    date_column: str,
    columns: List[str] | None,
    thresholds: dict,
) -> str:
    """生成 dbt test YAML."""
    model_name = table.split(".")[-1] if "." in table else table
    yml = f"""# dbt Tests for model: {model_name}
# Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

version: 2

models:
  - name: {model_name}
    description: "Data quality tests for {table}"
    columns:
"""
    yml += f"""      - name: {pk_column}
        description: "Primary key"
        tests:
          - not_null
          - unique
"""

    if "freshness" in checks or "timeliness" in checks:
        yml += f"""      - name: {date_column}
        description: "Record timestamp"
        tests:
          - not_null
"""

    if columns:
        for col in columns:
            if col == pk_column or col == date_column:
                continue
            yml += f"""      - name: {col}
        tests:
          - not_null:
              config:
                severity: warn
"""

    if "validity" in checks:
        yml += f"""
    # Custom data tests (place in tests/generic/)
    # tests:
    #   - dbt_utils.expression_is_true:
    #       expression: "amount >= 0"
"""
    return yml


def generate_soda_checks(
    table: str,
    checks: List[str],
    platform: str,
    pk_column: str,
    date_column: str,
    columns: List[str] | None,
    thresholds: dict,
) -> str:
    """生成 SodaCL 检查 YAML."""
    yml = f"""# SodaCL Checks for {table}
# Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

checks for {table}:
"""
    if "completeness" in checks:
        yml += f"""
  # Completeness
  - missing_count({pk_column}) = 0:
      name: PK must not be null
      fail: when > 0
"""

    if "uniqueness" in checks:
        yml += f"""
  # Uniqueness
  - duplicate_count({pk_column}) = 0:
      name: PK must be unique
"""

    if "freshness" in checks or "timeliness" in checks:
        yml += f"""
  # Freshness
  - freshness({date_column}) < 1d:
      name: Data must be less than 1 day old
"""

    if "volume" in checks:
        t = thresholds.get("volume", {})
        min_rows = t.get("min_rows", 1)
        yml += f"""
  # Volume
  - row_count > {min_rows}:
      name: Table must have data
"""

    if "validity" in checks:
        yml += f"""
  # Validity (customize per column)
  - invalid_count({pk_column}) = 0:
      valid_format: uuid
      name: PK must be valid format
"""

    if columns:
        for col in columns:
            if col == pk_column or col == date_column:
                continue
            yml += f"""  - missing_count({col}) < 100:
      name: {col} should have minimal nulls
"""

    return yml


def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)

    checks = [c.strip() for c in args.checks.split(",")]
    invalid = [c for c in checks if c not in QUALITY_DIMENSIONS]
    if invalid:
        print(f"⚠️  未知检查类型: {invalid}")
        print(f"可用检查类型: {list(QUALITY_DIMENSIONS.keys())}")
        checks = [c for c in checks if c in QUALITY_DIMENSIONS]

    thresholds = load_thresholds(args.threshold_file)
    # 合并默认阈值
    for dim_name, dim_info in QUALITY_DIMENSIONS.items():
        if dim_name not in thresholds:
            thresholds[dim_name] = dim_info["default_threshold"]

    columns = args.columns.split(",") if args.columns else None
    cols_clean = [c.strip() for c in columns] if columns else None

    # 生成对应格式
    generators = {
        "sql": generate_sql_checks,
        "great_expectations": generate_great_expectations,
        "dbt_test": generate_dbt_tests,
        "soda": generate_soda_checks,
    }

    ext_map = {"sql": "sql", "great_expectations": "yml", "dbt_test": "yml", "soda": "yml"}

    generator = generators[args.format]
    content = generator(
        table=args.table,
        checks=checks,
        platform=args.platform,
        pk_column=args.pk_column,
        date_column=args.date_column,
        columns=cols_clean,
        thresholds=thresholds,
    )

    ext = ext_map[args.format]
    safe_name = args.table.replace(".", "_").replace("`", "")
    output_file = os.path.join(args.output, f"{safe_name}_dq.{ext}")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ 数据质量检查已生成: {output_file}")
    print(f"📋 检查维度: {', '.join(checks)}")
    print(f"🔧 输出格式: {args.format}")
    print(f"☁️  目标平台: {args.platform}")

    # 生成摘要
    summary = {
        "table": args.table,
        "platform": args.platform,
        "format": args.format,
        "checks": checks,
        "generated_at": datetime.now().isoformat(),
        "output_file": output_file,
    }
    summary_file = os.path.join(args.output, f"{safe_name}_dq_summary.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"📄 摘要: {summary_file}")


if __name__ == "__main__":
    main()
