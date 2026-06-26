# data-analysis-sql Skill 使用文档

> 版本：2026-04-01
> 适用引擎：PostgreSQL / MySQL / Hive / SparkSQL / ClickHouse / Doris / Presto / BigQuery

---

## 一、简介

`data-analysis-sql` 是一个大数据开发工程师级的 AI 技能包，覆盖从 SQL 编写、指标设计、数仓建模到知识库维护的完整数据开发工作流。

**核心能力：**

| 能力 | 说明 |
|------|------|
| 写 SQL | 多引擎 SQL 编写，支持 CTE、窗口函数、复杂聚合 |
| 改 SQL | 口径调整、方言迁移、性能优化 |
| 指标设计 | 交付准时率、Flow Time、缺陷密度、用例通过率等业务指标模板 |
| 数仓建模 | ODS/DWD/DWS/ADS 分层设计，SCD 变更处理 |
| ETL 管线 | 全量/增量/CDC 策略，任务编排与故障恢复 |
| 数据质量 | 空值率、重复率、波动检测，异常数据识别 |
| 知识库维护 | 从 xlsx 批量生成 schema/metrics/relations/enums 文档 |
| 文档生成 | 表结构 Markdown 文档、SQL 迁移摘要自动生成 |

---

## 二、触发方式

以下关键词会自动激活本 Skill：

```
写SQL / 改SQL / 优化SQL / SQL报错
数仓建模 / ETL / 数据质量 / 指标设计
整理文档 / 生成md / 迁移文档 / 沉淀一下
知识库 / 表结构 / 枚举值 / 关联关系
```

---

## 三、使用场景与示例

### 场景 1：写一个新指标 SQL

**触发方式：** 直接描述指标需求

**示例：**
```
帮我写一个"交付准时率"指标 SQL，按租户维度统计，
数据库是 PostgreSQL，需要过滤已取消的需求
```

**Skill 处理流程：**
1. 澄清指标定义（分子/分母/时间口径）
2. 确认数据源和关联链路
3. 按 CTE 分层编写 SQL
4. 自动执行安全检查清单（tenantkey / del_flag / 防零 / 类型兼容）

---

### 场景 2：修复 SQL 报错

**触发方式：** 粘贴报错信息 + SQL

**常见报错及处理：**

| 报错 | 原因 | 处理方式 |
|------|------|---------|
| `invalid input syntax for type numeric: "N/A"` | 数字字段与字符串 COALESCE 类型不兼容 | 先 `CAST(col AS TEXT)` |
| `invalid input syntax for type timestamp: "1774886400000"` | 毫秒时间戳字符串未转换 | 用 `to_timestamp(CAST(col AS BIGINT) / 1000.0)` |
| `missing FROM-clause entry for table "xx"` | CTE 别名与内部列别名冲突 | 内部子查询改用 `t` 作别名 |
| `column xx does not exist` | 外层引用了 CTE 中未 SELECT 的列 | 在 CTE SELECT 中补充该列 |

---

### 场景 3：SQL 方言迁移

**触发方式：** 说明源引擎和目标引擎

**示例：**
```
把这段 Oracle SQL 改成 PostgreSQL，
主要是 KEEP (DENSE_RANK LAST ...) 这个语法不兼容
```

**常见迁移点：**

| Oracle 写法 | PostgreSQL 写法 |
|------------|----------------|
| `KEEP (DENSE_RANK LAST ORDER BY t)` | `ROW_NUMBER() OVER (... ORDER BY t DESC) + WHERE rn=1` |
| `NVL(col, 0)` | `COALESCE(col, 0)` |
| `SYSDATE` | `CURRENT_DATE` |
| `ROWNUM` | `ROW_NUMBER() OVER ()` |
| `CONNECT BY` | 递归 CTE `WITH RECURSIVE` |

---

### 场景 4：数仓建模

**触发方式：** 描述业务场景和建模需求

**示例：**
```
帮我设计一个需求管理的 DWS 层宽表，
需要支持按租户、项目、版本三个维度查询
```

**Skill 输出：**
- 分层建议（放 DWD 还是 DWS）
- 表结构设计（字段、类型、分区键）
- 关联关系说明
- 建表 DDL

---

### 场景 5：知识库目录生成

**触发方式：** 上传 xlsx 文件 + 说明类型

**支持的 xlsx 类型：**

| 文件类型 | 说明 | 输出 |
|---------|------|------|
| 表交接清单 | 含表名、字段、建表语句、核查信息 | 各领域 `schema.md` |
| 指标 SQL 文件 | 含指标ID、名称、SQL、维度 | 各领域 `metrics.md` |
| 维度标准文件 | 含模块名、字典类型、枚举值 | 各领域 `enums.md` |

**示例：**
```
我上传了一个表结构.xlsx，帮我按领域生成 schema.md，
放到 data-analysis/ 目录下
```

**生成的目录结构：**
```
data-analysis/
├── README.md                  ← 总索引（自动维护）
├── {domain}/
│   ├── schema.md              ← 表结构说明
│   ├── metrics.md             ← 指标 SQL
│   ├── relations.md           ← 表关联关系（从 SQL 自动提取）
│   └── enums.md               ← 枚举值速查
└── common/
    ├── join-rules.md          ← 关联规则
    └── sql-pitfalls.md        ← 踩坑记录
```

---

### 场景 6：表关联关系提取

**触发方式：** 说明要分析的 metrics.md 路径

**示例：**
```
帮我从 metrics.md 的 SQL 里提取表关联关系，生成 relations.md
```

**输出内容：**
- 涉及表清单（每张表被多少指标引用）
- 关联关系图（主表 → JOIN 关联表 + ON 条件）
- 关联详情（JOIN 类型 + 关联字段）

---

### 场景 7：数据质量检测

**触发方式：** 描述数据问题或质量需求

**示例：**
```
帮我写一个数据质量检测 SQL，
检查这张表的空值率、重复率，以及关键字段的波动情况
```

---

## 四、SQL 编写规范（快速参考）

### 必须遵守的规则

```sql
-- 1. 所有关联必须带 tenantkey（防跨租户污染）
INNER JOIN schema."table_b" b
    ON a."objectid"  = b."itemobjectid"
   AND a."tenantkey" = b."tenantkey"   -- ← 必须

-- 2. 所有关联表加 del_flag = 0
INNER JOIN schema."table_b" b
    ON a."id" = b."fk_id"
   AND b."del_flag" = 0               -- ← 必须

-- 3. 分母防零
ROUND(SUM(x) * 1.0 / NULLIF(COUNT(y), 0), 2)

-- 4. 数字字段与字符串 COALESCE 先转 TEXT
COALESCE(CAST(numeric_col AS TEXT), '未知')

-- 5. 项目维度空值处理
COALESCE(proj."value", '未归属项目')
```

### 防踩坑检查清单

```
□ 所有关联是否同时带 tenantkey
□ 无 tenantkey 的表是否从主表 JOIN 带过来
□ 时间字段是否做了类型转换（毫秒时间戳 / 日期字符串）
□ 关联键字段名是否确认（objectid / key / itemobjectid）
□ 所有关联表是否加了 del_flag = 0 过滤
□ COALESCE 的类型是否一致（数字字段先 CAST AS TEXT）
□ 外层引用的列是否在 CTE SELECT 中声明
□ 窗口函数是否用了正确方言（Oracle KEEP → PostgreSQL ROW_NUMBER）
□ CTE 别名是否与内部列别名重名
□ 分母是否用了 NULLIF 防零
□ NULL 处理是否完整（IS NOT NULL 过滤）
□ 项目维度是否用 COALESCE(value, '未归属项目')
```

---

## 五、References 文件说明

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `sql-guide.md` | SQL 编写规范（CTE/命名/注释/格式） | 写新 SQL 时 |
| `join-rules.md` | 9条关联规则 + 13项检查清单 | 写多表 JOIN 时 |
| `sql-pitfalls.md` | 10类踩坑记录 + 修复方案 | SQL 报错时 |
| `business-metrics.md` | 4类业务指标 SQL 模板 | 设计业务指标时 |
| `schema-guide.md` | 数仓建模规范（ODS/DWD/DWS/ADS） | 建模时 |
| `multi-engine.md` | 多引擎方言差异与适配 | SQL 迁移时 |
| `pipeline-patterns.md` | ETL 管线编排模式 | 设计 ETL 时 |
| `data-quality.md` | 数据质量检测规范 | 数据质量检测时 |
| `data-analysis-patterns.md` | 数据分析常用模式 | 写分析 SQL 时 |
| `knowledge-base.md` | 知识库目录生成规范 + Python 脚本模板 | 维护知识库时 |
| `doc-guide.md` | 文档自动生成与迁移指南 | 整理文档时 |

---

## 六、工具脚本说明

### sql_formatter.py — SQL 格式化

```bash
python scripts/sql_formatter.py
```
将 SQL 统一格式化：关键字大写、缩进对齐、CTE 分段。

### sql_diff.py — SQL 逻辑对比

```bash
python scripts/sql_diff.py
```
输入两段 SQL，输出逻辑差异摘要（数据源变化、过滤条件变化、输出字段变化）。

### doc_generator.py — 文档自动生成

```bash
python scripts/doc_generator.py
```
交互式输入表结构信息，自动生成标准 Markdown 文档。

---

## 七、多引擎支持

| 引擎 | 适用场景 |
|------|---------|
| **PostgreSQL** | OLTP 业务库、中等规模分析（本 Skill 主要适配引擎） |
| **MySQL** | OLTP 业务库 |
| **Hive / SparkSQL** | 离线大宽表、数仓批处理 |
| **Presto / Trino** | 跨源联邦查询、Ad-hoc 分析 |
| **ClickHouse** | 高并发实时 OLAP |
| **Doris / StarRocks** | 高并发多表 JOIN 的 OLAP |
| **BigQuery** | 云原生大表、Serverless SQL |

---

## 八、Skill 文件结构

```
data-analysis-sql/
├── SKILL.md                           ← 技能入口（AI 读取）
├── references/
│   ├── sql-guide.md                   ← SQL 编写规范
│   ├── join-rules.md                  ← 关联规则（新增）
│   ├── sql-pitfalls.md                ← 踩坑记录
│   ├── business-metrics.md            ← 业务指标模板
│   ├── schema-guide.md                ← 数仓建模规范
│   ├── multi-engine.md                ← 多引擎适配
│   ├── pipeline-patterns.md           ← ETL 管线模式
│   ├── data-quality.md                ← 数据质量规范
│   ├── data-analysis-patterns.md      ← 分析模式
│   ├── knowledge-base.md              ← 知识库规范（新增）
│   └── doc-guide.md                   ← 文档生成指南
└── scripts/
    ├── sql_formatter.py               ← SQL 格式化
    ├── sql_diff.py                    ← SQL 对比
    └── doc_generator.py               ← 文档生成
```

---

## 九、版本记录

| 日期 | 变更内容 |
|------|---------|
| 2026-04-01 | 新增 `join-rules.md`（9条关联规则 + 13项检查清单） |
| 2026-04-01 | 新增 `knowledge-base.md`（知识库目录生成规范） |
| 2026-04-01 | `business-metrics.md` 改为通用占位符模板，移除具体表名 |
| 2026-04-01 | `sql-pitfalls.md` 补充 tenantkey / 类型兼容 检查项 |
| 2026-03-31 | 初始版本，支持 PostgreSQL 指标 SQL 开发 |
