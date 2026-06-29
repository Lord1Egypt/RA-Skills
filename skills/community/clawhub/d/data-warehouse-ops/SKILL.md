---
name: data-warehouse-ops
description: "数据仓库（大数据/数仓）全生命周期运维技能。覆盖单一事实来源定义、ETL/ELT管道构建、维度建模（星型模型/雪花模型/Data Vault）、数据质量检查、分区策略、成本/性能调优、数据治理、血缘追踪、SLA监控9大模块。支持主流云数仓（BigQuery/Snowflake/Redshift/Databricks/StarRocks/ClickHouse）和开源工具链（dbt/Airflow/Great Expectations/OpenLineage/DataHub）。触发词：数据仓库、数仓、DW、ETL、ELT、维度建模、星型模型、数据质量、分区策略、数仓调优、数据治理、血缘追踪、SLA监控、数仓运维、数据管道、data warehouse、dimensional modeling、data quality、data lineage。"
agent_created: true
---

# 数据仓库运维技能 (Data Warehouse Operations)

数据仓库全生命周期运维助手，覆盖从架构设计到日常监控的完整工作流。

## 模块索引

本技能包含 9 大工作模块和配套的脚本/参考/资产资源：

| 模块 | 关键词 | 脚本 | 参考文档 |
|------|--------|------|----------|
| 1. 单一事实来源 | SSOT, 数据标准 | — | governance_framework.md |
| 2. ETL/ELT 管道 | pipeline, dbt, Airflow | etl_pipeline_builder.py | sql_templates.md |
| 3. 维度建模 | star schema, Kimball | dim_model_generator.py | dimensional_modeling.md |
| 4. 数据质量 | DQ, Great Expectations | data_quality_checker.py | data_quality_rules.md |
| 5. 分区策略 | partition, clustering | partition_advisor.py | partition_strategies.md |
| 6. 成本/性能调优 | cost, performance | cost_optimizer.py | partition_strategies.md |
| 7. 数据治理 | governance, catalog | — | governance_framework.md |
| 8. 血缘追踪 | lineage, OpenLineage | lineage_parser.py | — |
| 9. SLA 监控 | SLA, freshness, uptime | sla_monitor.py | sla_templates.md |

## 工作流程

当用户提出数仓相关需求时，按以下流程执行：

### Phase 0: 需求识别与路由

1. 分析用户输入，识别属于哪个/哪些模块
2. 如果涉及多个模块，按依赖顺序排列（先建模→再ETL→再质量→再调优→再监控）
3. 确认目标数仓平台（BigQuery/Snowflake/Redshift/StarRocks/ClickHouse/Databricks/其他）

### Phase 1: 架构设计与建模（模块1-3）

**单一事实来源 (SSOT) 定义：**
- 识别业务域的核心实体（客户/产品/订单/供应商等）
- 为每个实体定义权威数据源和 golden record 标准
- 输出 SSOT 矩阵：实体 → 源系统 → 主键 → 更新频率 → 数据Owner
- 加载 `references/governance_framework.md` 获取 SSOT 设计模板

**维度建模：**
- 使用 `scripts/dim_model_generator.py` 生成 DDL
- 支持星型模型（默认）、雪花模型、Data Vault 2.0
- 自动生成：事实表 + 维度表 + 代理键 + SCD Type 1/2/3 策略
- 指定参数：`--schema star|snowflake|vault --scd-type 2 --platform bigquery`
- 加载 `references/dimensional_modeling.md` 了解建模最佳实践

**ETL/ELT 管道设计：**
- 使用 `scripts/etl_pipeline_builder.py` 生成管道模板
- 支持 dbt/Airflow/自定义 SQL 三种输出格式
- 包含增量加载、CDC、错误处理、重试逻辑
- 加载 `references/sql_templates.md` 获取标准 SQL 模式

### Phase 2: 数据质量与治理（模块4, 7）

**数据质量检查：**
- 使用 `scripts/data_quality_checker.py` 生成检查规则
- 覆盖 6 大质量维度：完整性、唯一性、有效性、一致性、及时性、准确性
- 输出 Great Expectations suite YAML 或纯 SQL 检查脚本
- 加载 `references/data_quality_rules.md` 获取预制规则模板

**数据治理：**
- 加载 `references/governance_framework.md`
- 定义数据域、数据Owner、数据管家角色
- 建立数据分类分级策略（公开/内部/机密/绝密）
- 制定数据保留和归档策略

### Phase 3: 性能与成本优化（模块5-6）

**分区策略设计：**
- 使用 `scripts/partition_advisor.py` 分析表结构并推荐分区方案
- 输入：表 DDL + 查询模式描述
- 输出：平台特定的 PARTITION BY / CLUSTER BY 语句
- 加载 `references/partition_strategies.md` 了解各平台差异

**成本/性能调优：**
- 使用 `scripts/cost_optimizer.py` 分析查询成本
- 识别：全表扫描、笛卡尔积、数据倾斜、低效 JOIN
- 输出：优化建议（物化视图、聚簇键调整、谓词下推）
- 生成交互式 HTML 成本分析报告 (`assets/cost_report.html`)

### Phase 4: 血缘与监控（模块8-9）

**血缘追踪：**
- 使用 `scripts/lineage_parser.py` 解析 SQL 提取列级血缘
- 支持：INSERT...SELECT、CREATE TABLE AS、VIEW、MERGE
- 输出：DOT 格式图 + 交互式 HTML 可视化 (`assets/lineage_visualizer.html`)

**SLA 监控：**
- 使用 `scripts/sla_monitor.py` 生成监控仪表板
- 监控指标：数据新鲜度、管道运行时长、失败率、数据量波动
- 输出：HTML 仪表板 (`assets/sla_dashboard.html`)
- 加载 `references/sla_templates.md` 了解 SLA 定义标准

## 脚本使用方法

所有脚本位于 `scripts/` 目录，用 Python 3.9+ 运行。

### dim_model_generator.py — 维度建模 DDL 生成器

```bash
python scripts/dim_model_generator.py \
  --business-domain "电商订单" \
  --facts "orders:订单事实,order_items:订单明细" \
  --dimensions "customer:客户,dim_product:产品,dim_date:日期,dim_store:门店" \
  --schema star \
  --scd-type 2 \
  --platform snowflake \
  --output ddl/
```

参数说明：
- `--business-domain`: 业务域名称
- `--facts`: 事实表定义，格式 `表名:描述`
- `--dimensions`: 维度表定义，格式 `表名:描述`
- `--schema`: 建模范式 `star`(默认) | `snowflake` | `vault`
- `--scd-type`: 缓慢变化维度策略 `1` | `2` | `3` | `hybrid`
- `--platform`: 目标平台 `bigquery` | `snowflake` | `redshift` | `starrocks` | `clickhouse` | `databricks` | `postgres`
- `--output`: 输出目录

### data_quality_checker.py — 数据质量检查引擎

```bash
python scripts/data_quality_checker.py \
  --table dwh.fact_orders \
  --platform bigquery \
  --checks "completeness,uniqueness,validity,freshness" \
  --format great_expectations \
  --threshold-file dq_thresholds.yaml \
  --output dq_checks/
```

参数说明：
- `--table`: 目标表（支持 `schema.table` 格式）
- `--platform`: 目标平台
- `--checks`: 检查类型，逗号分隔。支持：completeness, uniqueness, validity, consistency, timeliness, accuracy, freshness, volume, custom
- `--format`: 输出格式 `great_expectations` | `sql` | `dbt_test` | `soda`
- `--threshold-file`: 阈值配置文件（可选）
- `--output`: 输出目录

### partition_advisor.py — 分区策略推荐器

```bash
python scripts/partition_advisor.py \
  --ddl-file ddl/fact_orders.sql \
  --query-patterns "daily_report,monthly_trend,user_lookup" \
  --platform bigquery \
  --data-volume "10TB,500M rows" \
  --output recommendations/
```

参数说明：
- `--ddl-file`: 表 DDL 文件路径
- `--query-patterns`: 查询模式描述
- `--platform`: 目标平台
- `--data-volume`: 数据量级
- `--output`: 输出目录

### cost_optimizer.py — 成本优化分析器

```bash
python scripts/cost_optimizer.py \
  --query-log queries.json \
  --platform bigquery \
  --billing-data billing.csv \
  --output optimization_report/
```

参数说明：
- `--query-log`: 查询日志（JSON 格式，含 query_text, bytes_processed, duration）
- `--platform`: 目标平台
- `--billing-data`: 账单数据（可选）
- `--output`: 输出目录

### lineage_parser.py — SQL 血缘解析器

```bash
python scripts/lineage_parser.py \
  --sql-dir sql/ \
  --output lineage/
```

参数说明：
- `--sql-dir`: 包含 SQL 文件的目录
- `--sql-file`: 单个 SQL 文件（与 --sql-dir 二选一）
- `--output`: 输出目录
- `--level`: 血缘级别 `table`(默认) | `column`

### sla_monitor.py — SLA 监控仪表板生成器

```bash
python scripts/sla_monitor.py \
  --config sla_config.yaml \
  --pipeline-runs runs.csv \
  --output dashboard/
```

参数说明：
- `--config`: SLA 配置文件
- `--pipeline-runs`: 管道运行历史数据
- `--output`: 输出目录

### etl_pipeline_builder.py — ETL 管道模板生成器

```bash
python scripts/etl_pipeline_builder.py \
  --source-type mysql \
  --target-platform snowflake \
  --mode incremental \
  --cdc-method timestamp \
  --orchestrator airflow \
  --output pipelines/
```

## 参考文档索引

需要深入某个主题时加载对应文件：

| 文件 | 内容 | 使用场景 |
|------|------|----------|
| `references/dimensional_modeling.md` | Kimball 四步法、SCD策略、事实表类型、维度设计模式 | 设计维度模型时 |
| `references/data_quality_rules.md` | 6维度质量规则库、Great Expectations模板、异常检测规则 | 定义数据质量检查时 |
| `references/sql_templates.md` | ETL模式SQL、窗口函数、MERGE/UPSERT、增量加载模板 | 编写ETL逻辑时 |
| `references/partition_strategies.md` | 各平台分区对比、聚簇策略、分区裁剪最佳实践 | 设计分区方案时 |
| `references/governance_framework.md` | SSOT定义模板、数据域划分、角色职责、分类分级标准 | 制定治理策略时 |
| `references/sla_templates.md` | SLA指标定义、新鲜度等级、告警规则模板 | 建立SLA体系时 |

## 输出约定

所有可视化输出默认生成交互式 HTML 报告（使用 Chart.js + 响应式布局），包含以下特征：
- 自动适配明暗主题
- 图表可交互（缩放/筛选/导出）
- 优先使用中文标签（中国用户默认）
- 报告嵌入关键指标摘要卡片

## 平台适配说明

根据目标平台自动调整 SQL 方言：

| 特性 | BigQuery | Snowflake | Redshift | StarRocks | ClickHouse |
|------|----------|-----------|----------|-----------|------------|
| 分区语法 | `PARTITION BY DATE(timestamp)` | 自动微分区 | `DISTKEY`+`SORTKEY` | `PARTITION BY RANGE(dt)` | `PARTITION BY toYYYYMM(dt)` |
| 增量合并 | `MERGE` | `MERGE` | `MERGE`(2023+) | `INSERT OVERWRITE` | `ALTER TABLE...UPDATE` |
| 物化视图 | ✅ | ✅ | ✅(2023+) | ✅ 异步 | ✅ |
| 半结构化 | `JSON` 类型 | `VARIANT` | `SUPER` | `JSON` 类型 | `JSON` 类型 |
| UDF | SQL/JS | SQL/JS/Python/Java | SQL/Python | Java UDF | SQL |
| 成本模型 | 按扫描字节 | 按 credit | 按节点小时 | 开源免费 | 开源免费 |

## 触发词

**中文触发词**：数据仓库、数仓、DW、ETL、ELT、维度建模、星型模型、雪花模型、数据质量、分区策略、数仓调优、数据治理、血缘追踪、血缘分析、SLA监控、数仓运维、数据管道、数据新鲜度、物化视图、缓慢变化维度、SCD、代理键、一致性维度、数据目录、数据管家、golden record、事实表、维度表、数据湖、湖仓一体

**英文触发词**：data warehouse, dimensional modeling, star schema, snowflake schema, data vault, ETL pipeline, ELT pipeline, data quality, DQ checks, partition strategy, data lineage, column lineage, SLA monitoring, data freshness, data governance, data catalog, surrogate key, slowly changing dimension, fact table, dimension table, data mart, data lakehouse

当用户消息包含以上任一关键词且涉及设计/构建/优化/检查/监控操作时，激活本技能。
