---
name: data-analysis-sql
description: "大数据开发工程师级数据分析与SQL技能。(1)多数据引擎SQL编写(Hive/SparkSQL/Presto/ClickHouse/Doris/MySQL/PG/BigQuery)。(2)复杂SQL改造调试与性能优化。(3)数仓建模(ODS/DWD/DWS/ADS)维度设计/SCD变更。(4)数据探查/指标设计/ETL管线编排。(5)数据质量检测与异常分析。(6)SQL改写(方言迁移/语法适配)。(7)UDF/UDTF开发规范。(8)表结构文档自动生成与迁移支持。(9)知识库目录生成与维护(schema/metrics/relations/enums)。触发:写SQL/改SQL/数仓建模/ETL/SQL优化/数据质量/指标设计/整理文档/生成md/迁移文档/知识库"
---

# data-analysis-sql

大数据开发工程师技能，专注于数据分析、SQL 开发、数仓建模和知识库维护。

---

## 核心工作流

### 写 SQL

1. 澄清需求 — 确认指标定义、数据源、时间口径、排除逻辑、输出格式
2. 确认数据源 — 参考 `references/multi-engine.md` 选择目标引擎，参考 `references/schema-guide.md` 理解表结构
3. 分层设计 — 判断放在哪层（ODS/DWD/DWS/ADS），避免跨层直接查询
4. 编写 SQL — 按 `references/sql-guide.md` 规范编写，优先用 CTE
5. 安全检查 — 按 `references/join-rules.md` 逐项过检查清单（tenantkey / del_flag / 防零 / 类型兼容）
6. 性能评估 — 检查数据倾斜、JOIN 爆炸因子、全表扫描风险
7. 验证口径 — 与现有报表或指标交叉验证

### 改 SQL

1. 理解原 SQL 意图（画出数据流：读哪张表 → 做什么计算 → 输出什么）
2. 找到需修改的部分（口径？字段？条件？逻辑？）
3. 改完整体走查：JOIN 方向、NULL 处理、分母防零、边界日期
4. 对比旧 SQL 与新 SQL 输出差异（样本数据验证）

### 数仓建模

参考 `references/schema-guide.md`：
- 确定主题域 → 选择事实表/维度表类型 → 设计拉链/快照/累计表
- 维度退化、缓慢变化维（SCD）处理
- 命名规范、分层规范

### ETL 管线

参考 `references/pipeline-patterns.md`：
- 全量/增量/CDC 策略选择
- 任务依赖编排、故障恢复
- 数据回溯与重刷机制

### 数据质量

参考 `references/data-quality.md`：
- 空值率、重复率、波动检测
- 端到端数据探查流程
- 异常数据识别与处理

### 业务指标设计

参考 `references/business-metrics.md`：
- 指标设计标准流程（7问）
- 交付准时率、Flow Time、需求缺陷密度、用例通过率完整 SQL 模板
- 按租户/项目维度的统一扩展模式
- 指标公式模板

### SQL 踩坑修复

参考 `references/sql-pitfalls.md`：
- 时间字段毫秒时间戳处理
- 关联表无 tenantkey 的处理
- PostgreSQL ROW_NUMBER 替代 Oracle KEEP
- CTE 别名与列别名冲突解决
- del_flag 过滤遗漏检查
- 防踩坑检查清单

### 知识库目录生成与维护

参考 `references/knowledge-base.md`：
- 按领域划分目录结构（schema / metrics / relations / enums）
- 从 xlsx 批量解析表结构、指标 SQL、枚举值，生成 Markdown 文档
- 从 SQL 自动提取表关联关系，生成 relations.md
- README 总索引自动维护

### 文档自动生成与迁移

参考 `references/doc-guide.md`：
- 交互式生成表结构 Markdown 文档
- 从用户输入的表结构文本自动解析并生成文档
- SQL 摘要提取（数据源、CTE、过滤条件、输出字段）
- 完整迁移文档打包生成（表结构 + SQL 清单）
- 触发词：整理文档、生成 md、迁移文档、沉淀一下

---

## 工具脚本

| 脚本 | 用途 |
|------|------|
| `scripts/sql_formatter.py` | SQL 格式化，统一风格 |
| `scripts/sql_diff.py` | 两段 SQL 逻辑对比，输出差异摘要 |
| `scripts/doc_generator.py` | 表结构文档自动生成，支持交互式/API调用 |

---

## 多引擎参考

| 引擎 | 适用场景 | 参考 |
|------|---------|------|
| Hive / SparkSQL | 离线大宽表、数仓批处理 | references/multi-engine.md |
| Presto / Trino | 跨源联邦查询、Ad-hoc 分析 | references/multi-engine.md |
| ClickHouse | 高并发实时 OLAP，近实时写入 | references/multi-engine.md |
| Doris / StarRocks | 高并发多表 JOIN 的 OLAP | references/multi-engine.md |
| MySQL / PostgreSQL | OLTP 业务库、中等规模分析 | references/sql-guide.md |
| BigQuery | 云原生大表、Serverless SQL | references/multi-engine.md |

---

## References 索引

| 文件 | 内容 |
|------|------|
| `references/sql-guide.md` | SQL 编写规范（CTE/命名/注释/格式） |
| `references/join-rules.md` | 关联规则（tenantkey/del_flag/自定义字段/防零/ROW_NUMBER） |
| `references/sql-pitfalls.md` | 8类踩坑记录 + 防踩坑检查清单 |
| `references/business-metrics.md` | 业务指标设计模板与完整 SQL |
| `references/schema-guide.md` | 数仓建模规范（ODS/DWD/DWS/ADS） |
| `references/multi-engine.md` | 多引擎方言差异与适配 |
| `references/pipeline-patterns.md` | ETL 管线编排模式 |
| `references/data-quality.md` | 数据质量检测规范 |
| `references/data-analysis-patterns.md` | 数据分析常用模式 |
| `references/knowledge-base.md` | 知识库目录生成与维护规范 |
| `references/doc-guide.md` | 文档自动生成与迁移指南 |
