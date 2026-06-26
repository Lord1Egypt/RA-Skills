---
name: data-pipeline-toolkit
description: 快速构建ETL数据管道 — 提取(APIs/数据库/文件)、转换(清洗/过滤/聚合)、加载(数据仓库)，支持定时调度和监控告警。
version: 1.0.0
author: yesong-Hue
tags: [ETL, 数据管道, 数据集成, 自动化, 调度]
readme: |
  # 数据管道工具箱

  快速构建企业级ETL数据管道。

  ## 核心功能

  - Extract：支持APIs、数据库、CSV/JSON/Parquet文件、S3等
  - Transform：清洗、过滤、聚合、关联
  - Load：PostgreSQL/MySQL、Snowflake/BigQuery、S3等
  - 定时调度：Cron或事件驱动
  - 监控告警：失败自动通知

  ## 安装

  ```bash
  clawhub install data-pipeline-toolkit
  ```

  ## 适用场景

  - 数据工程师：快速搭建数据管道
  - 运营人员：自动化数据汇总报表
  - 开发者：定时同步第三方API数据

  ## 相关资源

  更多AI技能包和工具，请访问：[AI智造工坊](http://ai.qnitgroup.com)
---

# 数据管道工具箱

> 快速构建ETL数据管道：提取 → 转换 → 加载 → 调度

## 核心功能

1. **多源提取** — REST APIs、GraphQL、SQL数据库、CSV/JSON/Parquet文件、S3/云存储、Kafka/SQS
2. **数据转换** — 清洗、过滤、聚合、关联、跨表Join
3. **多目标加载** — PostgreSQL/MySQL、Snowflake/BigQuery、S3、数据仓库
4. **定时调度** — Cron任务或事件触发
5. **监控告警** — 失败自动通知，可视化运行状态

## 快速开始

```bash
# 创建数据管道
./pipeline.sh create my-pipeline

# 添加数据源
./pipeline.sh extract my-pipeline api --url https://api.example.com/data

# 添加转换规则
./pipeline.sh transform my-pipeline filter "status == 'active'"
./pipeline.sh transform my-pipeline aggregate "group by category, sum(amount)"

# 添加目标存储
./pipeline.sh load my-pipeline postgres --connection $DATABASE_URL

# 运行管道
./pipeline.sh run my-pipeline
```

## 支持的数据源

| 类型 | 具体来源 |
|------|----------|
| APIs | REST API, GraphQL, 内部服务 |
| 数据库 | PostgreSQL, MySQL, MongoDB, SQL Server |
| 文件 | CSV, JSON, Parquet, Excel |
| 云存储 | AWS S3, Google Cloud Storage |
| 消息队列 | Kafka, AWS SQS |

## 支持的目标存储

| 类型 | 具体目标 |
|------|----------|
| 数据库 | PostgreSQL, MySQL, BigQuery, Snowflake |
| 数据仓库 | ClickHouse, DuckDB, TimescaleDB |
| 文件存储 | S3, GCS, 本地文件 |
| API | 第三方API回传 |

## 典型使用场景

### 场景1：每日销售数据汇总

```bash
# 从CRM API提取昨日销售数据
./pipeline.sh extract daily-sales api \
  --url "https://crm.example.com/api/orders?date=yesterday"

# 转换：按产品分类汇总
./pipeline.sh transform daily-sales aggregate \
  --group-by "product_category" \
  --sum "quantity,amount"

# 加载到数据仓库
./pipeline.sh load daily-sales bigquery \
  --project "my-project" --dataset "sales" --table "daily_summary"

# 设置每日定时任务
./pipeline.sh schedule daily-sales "0 6 * * *"
```

### 场景2：用户行为数据同步

```bash
# 从日志文件提取
./pipeline.sh extract user-logs file --path "/var/logs/app/*.json"

# 清洗和转换
./pipeline.sh transform user-logs filter "event_type != 'heartbeat'"
./pipeline.sh transform user-logs add-column "timestamp:parse_timestamp(time)"

# 加载到ClickHouse
./pipeline.sh load user-logs clickhouse --connection $CH_URL
```

## 监控与告警

### 查看运行状态

```bash
./pipeline.sh status my-pipeline
# 输出：
# Status: ✅ Running
# Last Run: 2026-05-05 06:00:00
# Duration: 45s
# Records Processed: 12,847
# Errors: 0
```

### 配置告警

```bash
# 失败时发送邮件
./pipeline.sh alert my-pipeline email --to admin@example.com

# 失败时发送飞书消息
./pipeline.sh alert my-pipeline webhook --url "https://open.feishu.cn/..."
```

## 推荐资源

- **ShadowAI API（数据管道配套）**: https://referer.shadowai.xyz/r/1056448

---

*由 AI智造工坊 (http://ai.qnitgroup.com) 整理发布 | 安装源: ClawHub*