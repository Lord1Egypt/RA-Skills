#!/usr/bin/env python3
"""
ETL 管道模板生成器 — ETL Pipeline Builder
生成 dbt / Airflow / 自定义 SQL 格式的 ETL/ELT 管道模板。
支持增量加载、CDC、错误处理和重试逻辑。
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, List

SOURCE_TYPES = ["mysql", "postgresql", "oracle", "sqlserver", "mongodb", "kafka", "api", "s3", "bigquery", "snowflake"]
TARGET_PLATFORMS = ["bigquery", "snowflake", "redshift", "starrocks", "clickhouse", "databricks", "postgres"]
ORCHESTRATORS = ["airflow", "dbt", "dagster", "prefect", "custom"]
CDC_METHODS = ["timestamp", "binlog", "trigger", "full_refresh", "change_table"]


def parse_args():
    parser = argparse.ArgumentParser(description="ETL 管道模板生成器")
    parser.add_argument("--source-type", type=str, default="mysql",
                        choices=SOURCE_TYPES)
    parser.add_argument("--target-platform", type=str, default="bigquery",
                        choices=TARGET_PLATFORMS)
    parser.add_argument("--mode", type=str, default="incremental",
                        choices=["full", "incremental", "cdc", "snapshot"])
    parser.add_argument("--cdc-method", type=str, default="timestamp",
                        choices=CDC_METHODS)
    parser.add_argument("--orchestrator", type=str, default="airflow",
                        choices=ORCHESTRATORS)
    parser.add_argument("--output", type=str, default="pipelines/")
    parser.add_argument("--pipeline-name", type=str, default="etl_pipeline",
                        help="管道名称")
    parser.add_argument("--source-table", type=str, default="source_table",
                        help="源表名")
    parser.add_argument("--target-table", type=str, default="target_table",
                        help="目标表名")
    return parser.parse_args()


def generate_dbt_template(args) -> str:
    """生成 dbt 模型模板."""
    mode = args.mode
    target = args.target_table
    source = args.source_table

    config_block = ""
    if mode == "incremental":
        config_block = """{{
  config(
    materialized='incremental',
    unique_key='id',
    partition_by={{'field': 'created_at', 'data_type': 'timestamp'}},
    cluster_by=['id'],
    incremental_strategy='merge'
  )
}}"""
    elif mode == "snapshot":
        config_block = """{{
  config(
    materialized='snapshot',
    unique_key='id',
    strategy='timestamp',
    updated_at='updated_at'
  )
}}"""
    else:
        config_block = """{{
  config(
    materialized='table',
    partition_by={{'field': 'created_at', 'data_type': 'timestamp'}}
  )
}}"""

    incremental_filter = ""
    if mode == "incremental":
        incremental_filter = """
{% if is_incremental() %}
  -- 增量逻辑：仅处理上次运行后新增/变更的数据
  AND updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}"""

    sql = f"""{config_block}

WITH source AS (
    SELECT * FROM {{{{ source('{args.source_type}', '{source}') }}}}
    WHERE 1=1{incremental_filter}
),

-- 数据清洗和转换
transformed AS (
    SELECT
        -- 代理键
        {{{{ dbt_utils.generate_surrogate_key(['id']) }}}} AS sk_id,
        -- 业务字段 (自定义映射)
        id,
        name,
        description,
        amount,
        status,
        -- 日期维度键
        CAST(FORMAT_DATE('%Y%m%d', created_at) AS INT64) AS fk_date_sk,
        -- SCD Type 2 追踪列
        created_at AS valid_from,
        CAST(NULL AS TIMESTAMP) AS valid_to,
        TRUE AS is_current,
        -- 审计列
        CURRENT_TIMESTAMP() AS etl_created_at,
        '{{{{ invocation_id }}}}' AS etl_batch_id,
        '{args.pipeline_name}' AS etl_pipeline_name
    FROM source
    WHERE 1=1
      -- 数据质量过滤
      AND id IS NOT NULL
      AND name IS NOT NULL
)

-- 写入目标表
SELECT * FROM transformed
"""

    # 添加 dbt 测试文件
    tests_yml = f"""version: 2

models:
  - name: {target}
    description: "ETL pipeline {args.pipeline_name}"
    columns:
      - name: sk_id
        tests:
          - unique
          - not_null
      - name: id
        tests:
          - not_null
      - name: name
        tests:
          - not_null
      - name: etl_batch_id
        tests:
          - not_null
    data_tests:
      - dbt_utils.expression_is_true:
          expression: "amount >= 0"
          config:
            severity: warn
"""

    return f"-- dbt Model: {target}\n-- Source: {source} ({args.source_type})\n{sql}\n\n-- tests/{target}_tests.yml\n{tests_yml}"


def generate_airflow_template(args) -> str:
    """生成 Airflow DAG 模板."""
    dag_id = args.pipeline_name.replace(" ", "_").lower()
    mode = args.mode

    incremental_logic = ""
    if mode in ("incremental", "cdc"):
        incremental_logic = """
    # 获取上次成功运行的时间戳
    last_success = get_last_success_timestamp('{{ dag.dag_id }}', '{{ task.task_id }}')
    if last_success:
        sql += f" AND updated_at > '{last_success}'"
"""

    python_code = f'''"""
Airflow DAG: {args.pipeline_name}
Source: {args.source_type} -> Target: {args.target_platform}
Mode: {args.mode}
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.{args.target_platform}.operators.{args.target_platform} import (
    {args.target_platform.capitalize()}Operator,
)
from airflow.providers.{args.source_type}.hooks.{args.source_type} import {args.source_type.capitalize()}Hook
from airflow.models import Variable
import logging

logger = logging.getLogger(__name__)

default_args = {{
    "owner": "data_engineering",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 1),
    "email_on_failure": True,
    "email_on_retry": False,
    "email": ["data-team@company.com"],
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(hours=1),
    "execution_timeout": timedelta(hours=2),
    "sla": timedelta(hours=4),
}}


def extract_data(**context):
    """从 {args.source_type} 抽取数据."""
    hook = {args.source_type.capitalize()}Hook({args.source_type}_conn_id="{args.source_type}_default")
    sql = """
        SELECT *
        FROM {args.source_table}
        WHERE 1=1
    """{incremental_logic}

    df = hook.get_pandas_df(sql)
    context["ti"].xcom_push(key="extracted_data", value=df.to_json())
    logger.info(f"Extracted {{len(df)}} rows")
    return len(df)


def transform_data(**context):
    """数据清洗和转换."""
    import pandas as pd

    ti = context["ti"]
    json_data = ti.xcom_pull(key="extracted_data", task_ids="extract")
    df = pd.read_json(json_data)

    # 数据质量检查
    initial_count = len(df)
    df = df.dropna(subset=["id", "name"])  # 移除关键列为空的行
    logger.info(f"Quality filter: {initial_count} -> {{len(df)}} rows")

    # 添加审计列
    df["etl_created_at"] = datetime.now()
    df["etl_batch_id"] = context["dag_run"].run_id
    df["etl_pipeline_name"] = "{args.pipeline_name}"

    ti.xcom_push(key="transformed_data", value=df.to_json())
    logger.info(f"Transformed {{len(df)}} rows")
    return len(df)


def load_data(**context):
    """加载数据到 {args.target_platform}."""
    import pandas as pd

    ti = context["ti"]
    json_data = ti.xcom_pull(key="transformed_data", task_ids="transform")
    df = pd.read_json(json_data)

    hook = {args.target_platform.capitalize()}Hook({args.target_platform}_conn_id="{args.target_platform}_default")

    # 写入目标表
    hook.run(f"TRUNCATE TABLE staging.{args.target_table}")

    # 批量写入
    hook.insert_rows(
        table=f"staging.{args.target_table}",
        rows=df.values.tolist(),
        target_fields=df.columns.tolist(),
    )

    # 合并到最终表
    merge_sql = f"""
        MERGE INTO dwh.{args.target_table} T
        USING staging.{args.target_table} S
        ON T.id = S.id
        WHEN MATCHED THEN UPDATE SET
            T.name = S.name,
            T.amount = S.amount,
            T.updated_at = CURRENT_TIMESTAMP()
        WHEN NOT MATCHED THEN INSERT
            (id, name, amount, created_at, etl_batch_id)
        VALUES
            (S.id, S.name, S.amount, CURRENT_TIMESTAMP(), S.etl_batch_id)
    """
    hook.run(merge_sql)
    logger.info(f"Loaded {{len(df)}} rows")


def validate_data(**context):
    """数据质量验证."""
    import pandas as pd

    ti = context["ti"]
    json_data = ti.xcom_pull(key="transformed_data", task_ids="transform")
    df = pd.read_json(json_data)

    errors = []
    if df["id"].duplicated().any():
        errors.append(f"{{df['id'].duplicated().sum()}} duplicate IDs found")
    if df["id"].isna().any():
        errors.append(f"{{df['id'].isna().sum()}} null IDs found")

    if errors:
        for e in errors:
            logger.error(e)
        raise ValueError("Data validation failed: " + "; ".join(errors))

    logger.info("Data validation passed")


def send_notification(**context):
    """发送通知."""
    ti = context["ti"]
    rows_extracted = ti.xcom_pull(key="extracted_data", task_ids="extract")
    rows_loaded = ti.xcom_pull(key="transformed_data", task_ids="transform")

    message = f"""
    ETL Pipeline: {args.pipeline_name}
    Status: SUCCESS
    Rows Processed: {{sum(rows_extracted or [0])}}
    Execution Time: {{datetime.now()}}
    """
    logger.info(message)


with DAG(
    dag_id="{dag_id}",
    default_args=default_args,
    description="ETL: {args.source_type} -> {args.target_platform} for {args.pipeline_name}",
    schedule_interval="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["etl", "{args.source_type}", "{args.target_platform}"],
) as dag:

    start = DummyOperator(task_id="start")

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_data,
        provide_context=True,
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_data,
        provide_context=True,
    )

    validate = PythonOperator(
        task_id="validate",
        python_callable=validate_data,
        provide_context=True,
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_data,
        provide_context=True,
    )

    notify = PythonOperator(
        task_id="notify",
        python_callable=send_notification,
        provide_context=True,
        trigger_rule="all_done",
    )

    end = DummyOperator(task_id="end")

    start >> extract >> transform >> validate >> load >> notify >> end
'''

    return python_code


def generate_custom_sql_template(args) -> str:
    """生成自定义 SQL 管道模板."""
    mode = args.mode
    target_full = f"dwh.{args.target_table}"

    sql = f"""-- ============================================================
-- ETL Pipeline: {args.pipeline_name}
-- Source: {args.source_type}.{args.source_table}
-- Target: {args.target_platform}.{target_full}
-- Mode: {mode}
-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- ============================================================

"""

    if args.target_platform == "bigquery":
        # Step 1: 抽取到 Staging
        sql += f"""
-- Step 1: Extract to Staging
CREATE OR REPLACE TABLE staging.{args.target_table}_raw AS
SELECT *
FROM {args.source_table}
WHERE 1=1
"""

        if mode in ("incremental", "cdc"):
            sql += f"""  -- Incremental filter
  AND updated_at > (
    SELECT COALESCE(MAX(updated_at), TIMESTAMP('2000-01-01'))
    FROM {target_full}
  )
"""

        sql += ";\n\n"

        # Step 2: Transform
        sql += f"""
-- Step 2: Transform & Clean
CREATE OR REPLACE TABLE staging.{args.target_table}_clean AS
SELECT
    GENERATE_UUID() AS sk_id,
    id,
    name,
    description,
    CAST(amount AS NUMERIC) AS amount,
    UPPER(status) AS status,
    CAST(FORMAT_DATE('%Y%m%d', DATE(created_at)) AS INT64) AS fk_date_sk,
    created_at AS valid_from,
    CAST(NULL AS TIMESTAMP) AS valid_to,
    TRUE AS is_current,
    CURRENT_TIMESTAMP() AS etl_created_at,
    '{args.pipeline_name}' AS etl_pipeline_name
FROM staging.{args.target_table}_raw
WHERE id IS NOT NULL
  AND name IS NOT NULL
  AND amount >= 0;
"""

        # Step 3: Merge
        sql += f"""
-- Step 3: Merge into Target (SCD Type 2)
MERGE INTO {target_full} T
USING staging.{args.target_table}_clean S
ON T.id = S.id AND T.is_current = TRUE
WHEN MATCHED AND (
    T.name != S.name OR T.amount != S.amount OR T.status != S.status
) THEN
    -- Close current record
    UPDATE SET valid_to = CURRENT_TIMESTAMP(), is_current = FALSE
WHEN NOT MATCHED THEN
    INSERT (sk_id, id, name, description, amount, status, fk_date_sk,
            valid_from, valid_to, is_current, etl_created_at, etl_pipeline_name)
    VALUES (S.sk_id, S.id, S.name, S.description, S.amount, S.status, S.fk_date_sk,
            S.valid_from, S.valid_to, S.is_current, S.etl_created_at, S.etl_pipeline_name);

-- Insert new version for changed records
INSERT INTO {target_full} (sk_id, id, name, description, amount, status, fk_date_sk,
                            valid_from, valid_to, is_current, etl_created_at, etl_pipeline_name)
SELECT
    GENERATE_UUID(),
    S.id, S.name, S.description, S.amount, S.status, S.fk_date_sk,
    CURRENT_TIMESTAMP(), CAST('9999-12-31 23:59:59' AS TIMESTAMP), TRUE,
    CURRENT_TIMESTAMP(), S.etl_pipeline_name
FROM staging.{args.target_table}_clean S
INNER JOIN {target_full} T ON S.id = T.id AND T.is_current = TRUE
WHERE T.name != S.name OR T.amount != S.amount OR T.status != S.status;
"""

        # Step 4: Cleanup
        sql += f"""
-- Step 4: Cleanup Staging Tables
DROP TABLE IF EXISTS staging.{args.target_table}_raw;
DROP TABLE IF EXISTS staging.{args.target_table}_clean;
"""

        # Step 5: Quality Check
        sql += f"""
-- Step 5: Data Quality Check
SELECT
    'Completeness' AS check_type,
    COUNT(*) AS total,
    SUM(CASE WHEN id IS NULL OR name IS NULL THEN 1 ELSE 0 END) AS null_count,
    CASE WHEN SUM(CASE WHEN id IS NULL OR name IS NULL THEN 1 ELSE 0 END) = 0
         THEN 'PASS' ELSE 'FAIL' END AS status
FROM {target_full}
WHERE is_current = TRUE;

SELECT
    'Volume' AS check_type,
    COUNT(*) AS row_count,
    CASE WHEN COUNT(*) > 0 THEN 'PASS' ELSE 'FAIL' END AS status
FROM {target_full}
WHERE DATE(etl_created_at) = CURRENT_DATE();
"""

    return sql


def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)

    generators = {
        "dbt": generate_dbt_template,
        "airflow": generate_airflow_template,
        "custom": generate_custom_sql_template,
    }

    generator = generators.get(args.orchestrator, generate_custom_sql_template)
    content = generator(args)

    ext_map = {"dbt": "sql", "airflow": "py", "custom": "sql"}
    ext = ext_map.get(args.orchestrator, "sql")

    output_file = os.path.join(args.output, f"{args.pipeline_name}.{ext}")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ ETL 管道模板已生成: {output_file}")
    print(f"📋 管道名: {args.pipeline_name}")
    print(f"📥 源: {args.source_type}.{args.source_table}")
    print(f"📤 目标: {args.target_platform}.{args.target_table}")
    print(f"🔄 模式: {args.mode}")
    print(f"🔧 编排器: {args.orchestrator}")

    # 保存管道元数据
    meta = {
        "pipeline_name": args.pipeline_name,
        "source": {"type": args.source_type, "table": args.source_table},
        "target": {"platform": args.target_platform, "table": args.target_table},
        "mode": args.mode,
        "cdc_method": args.cdc_method,
        "orchestrator": args.orchestrator,
        "generated_at": datetime.now().isoformat(),
        "output_file": output_file,
    }
    meta_file = os.path.join(args.output, f"{args.pipeline_name}_metadata.json")
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    print(f"📄 元数据: {meta_file}")


if __name__ == "__main__":
    main()
