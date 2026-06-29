#!/usr/bin/env python3
"""
分区策略推荐器 — Partition Advisor
分析表 DDL 和查询模式，自动推荐最优分区和聚簇策略。
支持 BigQuery / Snowflake / Redshift / StarRocks / ClickHouse / Databricks。
"""

import argparse
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Tuple

# ── 平台分区能力矩阵 ──────────────────────────────────────────────

PLATFORM_CAPABILITIES = {
    "bigquery": {
        "partition_types": ["time_unit", "ingestion_time", "integer_range"],
        "time_granularity": ["HOUR", "DAY", "MONTH", "YEAR"],
        "max_partitions": 4000,
        "supports_clustering": True,
        "max_cluster_cols": 4,
        "clustering_cardinality_advice": "每组 ~50k-500k 行最佳",
        "partition_pruning": "自动分区裁剪",
        "cost_model": "按扫描字节计费，分区裁剪可大幅降低成本",
        "partition_syntax": "PARTITION BY {strategy}",
        "cluster_syntax": "CLUSTER BY {cols}",
        "best_practices": [
            "常用 WHERE 过滤列作为分区键",
            "高基数列不适合分区（如 user_id）",
            "分区粒度 = DAY 最常用",
            "搭配 CLUSTER BY 对高基数列排序",
        ],
    },
    "snowflake": {
        "partition_types": ["auto_micro_partition"],
        "time_granularity": ["AUTO"],
        "max_partitions": "无限制（自动微分区）",
        "supports_clustering": True,
        "max_cluster_cols": 4,
        "clustering_cardinality_advice": "中-高基数列效果好",
        "partition_pruning": "自动微分区裁剪",
        "cost_model": "按 credit 计费，聚簇可减少扫描微分区数",
        "partition_syntax": "自动管理，无需显式分区",
        "cluster_syntax": "CLUSTER BY ({cols})",
        "best_practices": [
            "Snowflake 自动管理微分区，无需手动分区",
            "对高基数列使用 CLUSTER BY 加速过滤和 JOIN",
            "对常用 JOIN 键聚簇",
            "定期检查聚簇深度 (SYSTEM$CLUSTERING_INFORMATION)",
        ],
    },
    "redshift": {
        "partition_types": ["distribution", "sort"],
        "time_granularity": ["DISTKEY + SORTKEY"],
        "max_partitions": "无限制",
        "supports_clustering": True,
        "max_cluster_cols": "复合 SORTKEY 最大 8 列",
        "clustering_cardinality_advice": "DISTKEY 低基数，SORTKEY 常用范围过滤",
        "partition_pruning": "SORTKEY 范围扫描",
        "cost_model": "按节点小时计费",
        "partition_syntax": "DISTKEY({col})",
        "cluster_syntax": "SORTKEY({cols})",
        "best_practices": [
            "DISTKEY 选择 JOIN 频繁的列，避免数据倾斜",
            "SORTKEY 选择 WHERE 范围过滤列（通常日期列第一）",
            "复合 SORTKEY 按过滤频率排序",
            "定期运行 VACUUM 和 ANALYZE",
        ],
    },
    "starrocks": {
        "partition_types": ["range", "list"],
        "time_granularity": ["HOUR", "DAY", "MONTH", "YEAR"],
        "max_partitions": 1024,
        "supports_clustering": False,
        "max_cluster_cols": 0,
        "clustering_cardinality_advice": "",
        "partition_pruning": "分区裁剪 + 分桶裁剪",
        "cost_model": "开源免费",
        "partition_syntax": "PARTITION BY RANGE({col})",
        "cluster_syntax": "DISTRIBUTED BY HASH({cols}) BUCKETS N",
        "best_practices": [
            "按日期 RANGE 分区",
            "分桶键选择高基数、分布均匀的列",
            "分区粒度 MONTH 最常用",
            "动态分区自动管理",
        ],
    },
    "clickhouse": {
        "partition_types": ["range", "list"],
        "time_granularity": ["MONTH", "DAY", "HOUR"],
        "max_partitions": "建议 < 1000",
        "supports_clustering": True,
        "max_cluster_cols": "无限制",
        "clustering_cardinality_advice": "主键即排序键",
        "partition_pruning": "分区裁剪 + 主键索引",
        "cost_model": "开源免费",
        "partition_syntax": "PARTITION BY {expr}",
        "cluster_syntax": "ORDER BY ({cols})",
        "best_practices": [
            "分区粒度 MONTH 最常用",
            "主键（ORDER BY）按查询频率排序",
            "避免过多分区（<1000）",
            "使用 TTL 自动清理旧数据",
        ],
    },
    "databricks": {
        "partition_types": ["range"],
        "time_granularity": ["YEAR", "MONTH", "DAY"],
        "max_partitions": "建议 < 10000",
        "supports_clustering": True,
        "max_cluster_cols": 4,
        "clustering_cardinality_advice": "高基数列不宜过多",
        "partition_pruning": "分区裁剪 + Z-Ordering",
        "cost_model": "按 DBU 计费",
        "partition_syntax": "PARTITIONED BY ({col})",
        "cluster_syntax": "CLUSTER BY ({cols})",
        "best_practices": [
            "分区基数适中 (100-10000)",
            "Delta Lake Z-Ordering 加速多维过滤",
            "OPTIMIZE 命令维护聚簇",
            "避免小文件问题",
        ],
    },
}

# ── 查询模式分析 ──────────────────────────────────────────────────

QUERY_PATTERNS = {
    "daily_report": {
        "description": "日报查询：按单日聚合",
        "filter_columns": ["date", "dt", "created_date"],
        "recommended_partition": "DAY",
        "priority": "HIGH",
    },
    "monthly_trend": {
        "description": "月度趋势：按月聚合",
        "filter_columns": ["month", "year_month"],
        "recommended_partition": "MONTH",
        "priority": "MEDIUM",
    },
    "user_lookup": {
        "description": "用户查询：按用户ID精确查找",
        "filter_columns": ["user_id", "customer_id"],
        "recommended_partition": "CLUSTER_ONLY",
        "priority": "HIGH",
    },
    "real_time": {
        "description": "实时查询：需要最新数据",
        "filter_columns": ["created_at", "event_time", "ingestion_time"],
        "recommended_partition": "HOUR",
        "priority": "HIGH",
    },
    "range_scan": {
        "description": "范围扫描：按时间段批量查询",
        "filter_columns": ["created_at", "updated_at"],
        "recommended_partition": "MONTH",
        "priority": "MEDIUM",
    },
    "full_scan": {
        "description": "全量扫描：定期全表分析",
        "filter_columns": [],
        "recommended_partition": "MONTH",
        "priority": "LOW",
    },
    "dimensional_join": {
        "description": "维度 JOIN：大表 JOIN 维度表",
        "filter_columns": ["dim_key", "category_id"],
        "recommended_partition": "CLUSTER_ONLY",
        "priority": "HIGH",
    },
}


def parse_args():
    parser = argparse.ArgumentParser(description="分区策略推荐器")
    parser.add_argument("--ddl-file", type=str, required=True,
                        help="表 DDL 文件路径")
    parser.add_argument("--query-patterns", type=str, required=True,
                        help="查询模式描述，逗号分隔: daily_report,monthly_trend,user_lookup,...")
    parser.add_argument("--platform", type=str, default="bigquery",
                        choices=list(PLATFORM_CAPABILITIES.keys()))
    parser.add_argument("--data-volume", type=str, default="1TB,100M rows",
                        help="数据量级: '10TB,500M rows'")
    parser.add_argument("--output", type=str, default="partition_advice/")
    return parser.parse_args()


def parse_ddl(file_path: str) -> dict:
    """解析 DDL 文件提取表信息和列."""
    with open(file_path, "r", encoding="utf-8") as f:
        ddl = f.read()

    table_name = "unknown_table"
    m = re.search(r'TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?(\w+\.\w+)`?', ddl, re.IGNORECASE)
    if m:
        table_name = m.group(1)

    # 解析列名和类型
    columns = []
    # 匹配列定义
    col_pattern = re.findall(r'^\s*(\w+)\s+(\w+(?:\([^)]*\))?)', ddl, re.MULTILINE)
    for col_name, col_type in col_pattern:
        if col_name.upper() not in ("PRIMARY", "PARTITION", "CLUSTER", "DISTKEY", "SORTKEY",
                                      "CREATE", "TABLE", "COMMENT", "OPTIONS", "DISTRIBUTED"):
            columns.append({"name": col_name, "type": col_type.upper()})

    return {"name": table_name, "columns": columns, "ddl": ddl}


def classify_columns(columns: list) -> dict:
    """将列分类为维度键、度量值、时间列等."""
    classified = {
        "time_columns": [],
        "key_columns": [],
        "measure_columns": [],
        "text_columns": [],
        "other": [],
    }

    for col in columns:
        name = col["name"].lower()
        typ = col["type"].upper()

        # 时间列
        if any(kw in name for kw in ["date", "time", "dt", "created", "updated", "timestamp",
                                       "event_time", "ingestion", "etl"]):
            classified["time_columns"].append(col)
        elif any(kw in typ for kw in ["DATE", "TIME", "TIMESTAMP", "DATETIME"]):
            classified["time_columns"].append(col)
        # 键列
        elif any(kw in name for kw in ["id", "key", "sk", "bk", "pk", "fk"]):
            classified["key_columns"].append(col)
        # 度量列
        elif any(kw in typ for kw in ["INT", "NUMERIC", "DECIMAL", "FLOAT", "DOUBLE", "NUMBER", "BIGINT"]):
            classified["measure_columns"].append(col)
        # 文本列
        elif any(kw in typ for kw in ["STRING", "VARCHAR", "TEXT", "CHAR"]):
            classified["text_columns"].append(col)
        else:
            classified["other"].append(col)

    return classified


def recommend_strategy(
    classified: dict,
    query_patterns: list,
    platform: str,
    data_volume: str,
) -> dict:
    """生成分区和聚簇推荐策略."""
    caps = PLATFORM_CAPABILITIES[platform]
    patterns = [p.strip() for p in query_patterns if p.strip() in QUERY_PATTERNS]
    pattern_data = [QUERY_PATTERNS[p] for p in patterns]

    # 选择分区列
    partition_col = None
    partition_granularity = "MONTH"  # 默认
    cluster_cols = []

    time_cols = classified["time_columns"]
    key_cols = classified["key_columns"]

    # 分区列推荐逻辑
    if time_cols:
        # 优先选择 created_at / event_time 类列
        priority_time = [c for c in time_cols
                         if any(kw in c["name"].lower()
                                for kw in ["created", "event_time", "dt", "date"])]
        partition_col = (priority_time or time_cols)[0]

        # 根据查询模式选择粒度
        if any(p.get("recommended_partition") == "HOUR" for p in pattern_data):
            partition_granularity = "HOUR"
        elif any(p.get("recommended_partition") == "DAY" for p in pattern_data):
            partition_granularity = "DAY"
        elif any(p.get("recommended_partition") == "MONTH" for p in pattern_data):
            partition_granularity = "MONTH"
    elif platform == "snowflake":
        partition_col = None  # Snowflake 自动管理
    elif platform == "redshift":
        # Redshift DISTKEY 选 JOIN 频率最高的列
        partition_col = key_cols[0] if key_cols else None

    # 聚簇列推荐
    # 高基数列适合聚簇
    if key_cols:
        cluster_cols.append(key_cols[0]["name"])
    # 文本列中 category/type/status 等适合聚簇
    text_cols = classified["text_columns"]
    for col in text_cols:
        if any(kw in col["name"].lower() for kw in ["category", "type", "status", "region", "country"]):
            cluster_cols.append(col["name"])
            break

    # 查询模式驱动的聚簇
    for p in pattern_data:
        if p.get("recommended_partition") == "CLUSTER_ONLY":
            for col in p.get("filter_columns", []):
                if col not in cluster_cols:
                    cluster_cols.append(col)

    # 平台特定调整
    max_cluster = caps.get("max_cluster_cols", 4)
    if isinstance(max_cluster, int):
        cluster_cols = cluster_cols[:max_cluster]

    # 生成 DDL 建议
    ddl_suggestions = _generate_ddl(
        platform, partition_col, partition_granularity, cluster_cols, caps
    )

    # 风险提示
    risks = _identify_risks(classified, partition_col, platform, caps)

    return {
        "platform": platform,
        "table_analysis": {
            "total_columns": sum(len(v) for v in classified.values()),
            "time_columns": [c["name"] for c in time_cols],
            "key_columns": [c["name"] for c in key_cols],
        },
        "query_patterns_considered": patterns,
        "recommendation": {
            "partition_column": partition_col["name"] if partition_col else "N/A (auto-managed)",
            "partition_granularity": partition_granularity,
            "cluster_columns": cluster_cols,
            "ddl_example": ddl_suggestions,
        },
        "cost_impact": _estimate_cost_impact(classified, partition_col, platform),
        "risks": risks,
        "best_practices": caps["best_practices"],
    }


def _generate_ddl(
    platform: str,
    partition_col: dict | None,
    granularity: str,
    cluster_cols: list,
    caps: dict,
) -> str:
    """生成分区 DDL 示例."""
    lines = []

    if platform == "bigquery":
        if partition_col:
            col_name = partition_col["name"]
            if any(kw in partition_col["type"].upper() for kw in ["INT", "NUMERIC", "BIGINT"]):
                lines.append(f"PARTITION BY RANGE_BUCKET({col_name}, GENERATE_ARRAY(0, 1000000, 1000))")
            else:
                lines.append(f"PARTITION BY DATE({col_name})")
        if cluster_cols:
            lines.append(f"CLUSTER BY {', '.join(cluster_cols)}")

    elif platform == "snowflake":
        if cluster_cols:
            lines.append(f"CLUSTER BY ({', '.join(cluster_cols)})")
        lines.insert(0, "-- Snowflake 自动管理微分区，以下为聚簇建议")

    elif platform == "redshift":
        if partition_col and not cluster_cols:
            lines.append(f"DISTKEY({partition_col['name']})")
        if cluster_cols:
            lines.append(f"COMPOUND SORTKEY({', '.join(cluster_cols)})")

    elif platform == "starrocks":
        if partition_col:
            col_name = partition_col["name"]
            if granularity in ("HOUR", "DAY", "MONTH", "YEAR"):
                lines.append(f"PARTITION BY RANGE({col_name}) (")
                lines.append(f"    PARTITION p_default VALUES LESS THAN MAXVALUE")
                lines.append(f")")
        if cluster_cols:
            lines.append(f"DISTRIBUTED BY HASH({cluster_cols[0]}) BUCKETS 32")

    elif platform == "clickhouse":
        if partition_col:
            col_name = partition_col["name"]
            lines.append(f"PARTITION BY toYYYYMM({col_name})")
        if cluster_cols:
            lines.append(f"ORDER BY ({', '.join(cluster_cols)})")

    elif platform == "databricks":
        if partition_col:
            col_name = partition_col["name"]
            if granularity in ("YEAR", "MONTH", "DAY"):
                fn = {"YEAR": "year", "MONTH": "month", "DAY": "date"}[granularity]
                lines.append(f"PARTITIONED BY ({fn}({col_name}))")
        if cluster_cols:
            lines.append(f"-- 使用 OPTIMIZE ... ZORDER BY ({', '.join(cluster_cols)})")

    return "\n".join(lines) if lines else "-- 当前平台无需显式分区声明"


def _identify_risks(
    classified: dict,
    partition_col: dict | None,
    platform: str,
    caps: dict,
) -> list:
    """识别分区策略风险."""
    risks = []

    # 分区列未找到
    if not partition_col and platform not in ("snowflake",):
        risks.append({
            "level": "WARNING",
            "message": "未找到合适的分区列，查询性能可能受影响",
            "suggestion": "建议添加 created_at 或 dt 类型的日期列",
        })

    # 高基数列用做分区
    if partition_col and "id" in partition_col["name"].lower() and platform != "snowflake":
        risks.append({
            "level": "CRITICAL",
            "message": f"高基数键列 {partition_col['name']} 不应用作分区键",
            "suggestion": "使用聚簇(CLUSTER BY)代替分区，或选用日期列",
        })

    # Snowflake 聚簇建议
    if platform == "snowflake" and not caps.get("supports_clustering"):
        risks.append({
            "level": "INFO",
            "message": "Snowflake 自动微分区已足够，聚簇可选",
        })

    return risks


def _estimate_cost_impact(
    classified: dict,
    partition_col: dict | None,
    platform: str,
) -> str:
    """估算分区策略的成本影响."""
    if platform == "bigquery":
        return "预计可减少 60-90% 的查询扫描字节量（取决于查询模式是否命中分区过滤）"
    elif platform == "snowflake":
        return "微分区自动管理，聚簇可减少 20-50% 的扫描微分区数"
    elif platform == "redshift":
        return "DISTKEY 减少跨节点数据移动，SORTKEY 加速范围查询"
    elif platform in ("starrocks", "clickhouse"):
        return "分区裁剪可跳过不相关分区，减少 70-95% 的扫描量"
    elif platform == "databricks":
        return "分区裁剪 + Z-Ordering，可减少 50-80% 的文件扫描"
    return "成本优化取决于具体查询模式"


def generate_report(result: dict, output_dir: str) -> str:
    """生成 Markdown 格式分区建议报告."""
    rec = result["recommendation"]
    md = f"""# 分区策略建议报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**目标平台**: {result['platform']}
**查询模式**: {', '.join(result['query_patterns_considered'])}

## 表分析

| 指标 | 值 |
|------|-----|
| 总列数 | {result['table_analysis']['total_columns']} |
| 时间列 | {', '.join(result['table_analysis']['time_columns']) or '无'} |
| 键列 | {', '.join(result['table_analysis']['key_columns']) or '无'} |

## 推荐策略

- **分区列**: `{rec['partition_column']}`
- **分区粒度**: `{rec['partition_granularity']}`
- **聚簇列**: `{', '.join(rec['cluster_columns']) or '无'}`

### DDL 示例

```sql
{rec['ddl_example']}
```

## 成本影响

{result['cost_impact']}

## 风险提示

"""
    for risk in result["risks"]:
        md += f"- **[{risk['level']}]** {risk['message']}\n"
        md += f"  - 建议: {risk['suggestion']}\n"

    md += f"""
## 最佳实践（{result['platform']}）

"""
    for bp in result["best_practices"]:
        md += f"- {bp}\n"

    md += """
## 后续行动

1. 在测试环境应用推荐的分区策略
2. 使用 EXPLAIN 验证查询计划是否使用分区裁剪
3. 监控查询性能变化
4. 根据实际查询模式迭代优化分区粒度
"""
    return md


def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)

    if not os.path.exists(args.ddl_file):
        print(f"❌ DDL 文件不存在: {args.ddl_file}")
        sys.exit(1)

    table_info = parse_ddl(args.ddl_file)
    classified = classify_columns(table_info["columns"])
    query_patterns = [p.strip() for p in args.query_patterns.split(",")]

    result = recommend_strategy(classified, query_patterns, args.platform, args.data_volume)

    # 保存 JSON
    table_safe = table_info["name"].replace(".", "_").replace("`", "")
    json_file = os.path.join(args.output, f"{table_safe}_partition_advice.json")
    result["table_name"] = table_info["name"]
    result["generated_at"] = datetime.now().isoformat()
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # 保存 Markdown 报告
    md_file = os.path.join(args.output, f"{table_safe}_partition_advice.md")
    report = generate_report(result, args.output)
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ 分区建议已生成")
    print(f"📄 JSON: {json_file}")
    print(f"📝 报告: {md_file}")
    print(f"")
    print(f"📊 推荐策略:")
    rec = result["recommendation"]
    print(f"   分区列: {rec['partition_column']}")
    print(f"   分区粒度: {rec['partition_granularity']}")
    print(f"   聚簇列: {', '.join(rec['cluster_columns']) or '无'}")
    print(f"   成本影响: {result['cost_impact']}")


if __name__ == "__main__":
    main()
