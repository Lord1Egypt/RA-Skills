---
name: data-query
description: 通用自然语言转SQL与可视化页面生成技能。当用户使用自然语言查询数据，或需要生成带图表的数据看板页面时调用本技能。技能基于挂载的知识库上下文直接生成SQL，验证后生成可部署的HTML图表页面。
---

# data-query 技能

## 技能概述

本技能提供自然语言转 SQL（NL→SQL）能力，并支持生成基于 ECharts 的可视化 HTML 页面。

**核心能力：**
- 将自然语言问题转换为准确的 SQL 查询
- 验证 SQL 可执行性后返回结果
- 生成可嵌入的 HTML 图表页面

**典型触发场景：**
- 用户问："某项目的延期任务有哪些？"
- 用户问："帮我统计一下这个项目的风险分布"
- 用户说："生成一个资源负载分析页面"

---

# 🚨 核心原则一：前置配置检查（必须首先执行）

**使用本技能前，必须立刻执行此检查。配置缺失时，停止一切操作，提示用户补充。**

**配置文件位置：** `skills/data-query/config.json`

### 必需配置

| 配置项 | 路径 | 说明 | 缺失后果 |
|--------|------|------|----------|
| API 验证账号 | `security.apiAuth.username` | 系统账号，用于验证 SQL | ❌ 无法验证 SQL |
| API 验证密码 | `security.apiAuth.password` | 系统密码，用于验证 SQL | ❌ 无法验证 SQL |
| 数据库类型 | `db.type` | `mysql` / `dm` / `oracle` | ⚠️ 无法确定方言规则 |

### 根据 db.type 显示相关配置

**当 `db.type = dm` 时：**

| 配置项 | 路径 | 说明 | 缺失后果 |
|--------|------|------|----------|
| 达梦主机 | `db.host` | 达梦数据库地址 | ❌ 无法连接达梦 |
| 达梦端口 | `db.port` | 达梦端口，默认 5236/5237 | ❌ 无法连接达梦 |
| 达梦数据库名 | `db.database` | 数据库实例名 | ⚠️ 可能连接失败 |
| 达梦用户名 | `db.user` | 数据库用户名 | ❌ 无法连接达梦 |
| 达梦密码 | `db.password` | 数据库密码 | ❌ 无法连接达梦 |

**当 `db.type = oracle` 时：**

| 配置项 | 路径 | 说明 | 缺失后果 |
|--------|------|------|----------|
| Oracle 主机 | `oracle.host` | Oracle 数据库地址 | ❌ 无法连接 Oracle |
| Oracle 端口 | `oracle.port` | Oracle 端口，默认 1521 | ❌ 无法连接 Oracle |
| Oracle 服务名 | `oracle.serviceName` | 数据库服务名 | ❌ 无法连接 Oracle |
| Oracle 用户名 | `oracle.user` | 数据库用户名 | ❌ 无法连接 Oracle |
| Oracle 密码 | `oracle.password` | 数据库密码 | ❌ 无法连接 Oracle |

**API 配置：**

| 配置项 | 路径 | 说明 | 缺失后果 |
|--------|------|------|----------|
| API Base URL | `api.base` | Dashboard 服务地址 | ❌ 无法调用 API 验证 |
| 登录密码加密 | `api.loginPasswordEncrypt` | 密码是否加密 | ⚠️ 可能登录失败 |

### 缺失时提示模板

配置缺失时，按以下格式提示用户，并直接帮用户设置：

```
⚠️ 技能配置不完整

配置文件：skills/data-query/config.json

缺失项：
  ❌ security.apiAuth.username — API 验证账号
  ❌ security.apiAuth.password — API 验证密码

请提供：
  1. 系统账号（用于验证 SQL）：______
  2. 系统密码：______

我将直接帮你写入配置文件。
```

### 校验规则

使用技能时，我会按以下顺序检查：

1. **检查 `security.apiAuth`** — 缺失则提示用户提供，我直接写入配置文件
2. **检查 `db.type`** — 缺失则无法确定方言，提示用户提供
3. **根据 db.type 检查对应数据库连接** — 缺失则提示用户提供，我直接写入
4. **检查 `api.base`** — 缺失则提示用户提供，我直接写入

**注意：** `verifyLimit`（重试次数）、`workspace` 为可选，不影响核心功能。

---

## 工作流程

### ⚠️ 必读：数据库方言规范

**生成 SQL 前，必须先读取对应数据库的规范文档：**

| 数据库 | 规范文档位置 |
|--------|------------|
| 达梦 DM | `skills/data-query/database_specs/dialect/DM.md` |
| MySQL | `skills/data-query/database_specs/dialect/MySQL.md` |
| Oracle | `skills/data-query/database_specs/dialect/Oracle.md` |
| **ShardingSphere 路由** | `skills/data-query/database_specs/sharding/ROUTING_RULES.md` |
| **ShardingSphere BUG** | `knowledge/shared/sharding/KNOWN_BUGS.md` |
| **分片表分布** | `knowledge/shared/sharding/TABLE_DISTRIBUTION.md` |

**达梦关键规范（必须遵守）：**
- ❌ 禁用 `TO_CHAR(date, 'YYYY-MM')` → ✅ 用 `SUBSTR(CAST(date AS VARCHAR), 1, 7)`
- ❌ 禁用 `GROUP BY + COUNT(*)` 在 ShardingSphere 下 → ✅ 返回原始数据，前端聚合
- ❌ 分片键上禁止使用函数

### ⚠️ 两套 SQL 必须同步

Cockpit 页面存在**两套 SQL**，修改时必须同时更新：

| 对象 | 用途 | 怎么改 |
|------|------|--------|
| `ENCRYPTED_SQL[key].ciphertext` | 后端实际执行 | 重新加密后替换 |
| `SQL_PLAIN[key]` | 前端参数校验 | 明文替换 |
| `CHART_CONFIG[id].scope` | 参数注入逻辑 | 按需调整 |

**修改步骤：**
1. 确定正确 SQL → 2. 用 `encrypt_for_page.js` 加密 → 3. 同时更新 ENCRYPTED_SQL 和 SQL_PLAIN → 4. 用 `src/verify/index.js` 验证

### 流程一：NL→SQL 查询（预览）

**输出**：无文件，直接返回 JSON 结果

```
用户自然语言问题
    ↓
主 agent 直接生成 SQL（基于知识库，不调用外部 LLM）
    ↓
调用 src/verify/index.js verify() 验证 SQL 可执行性（unified 模式：DB + API）
    ↓
返回 SQL + 查询结果给用户预览
```

### 流程二：生成单图表 HTML 页面

**输出路径**：`{workspace}/nl2sql_output/{chartTitle}_{timestamp}.html`

```
用户需求（图表类型 + 数据描述）
    ↓
步骤1：主 agent 直接生成 SQL（基于知识库）
步骤2：调用 src/verify/index.js verify() 验证 SQL（unified 模式）
步骤3：调用 src/security/encryptSql.js 对 SQL 进行 AES-256-CBC 加密
步骤4：填充 html_page_template.html 模板
       替换占位符: {{ENCRYPTED_SQL}}、{{IV}}、{{JWT_TOKEN}}、{{CHART_TITLE}} 等
    ↓
输出完整的 HTML 文件 → {workspace}/nl2sql_output/{chartTitle}_{timestamp}.html
```

### 流程三：生成驾驶舱 HTML 页面

驾驶舱是多图表聚合页面，包含 KPI 指标卡、多种 ECharts 图表、项目列表侧边栏和视图切换（仪表盘/看板/甘特图）。

**输出路径**：两个文件（归集在一起）
- 本地预览版：`{workspace}/nl2sql_output/cockpit_preview.html`（CDN URLs）
- 部署版：`{workspace}/nl2sql_output/cockpit.html`（CDN→本地相对路径，供部署使用）

> ⚠️ **不得覆盖模板**：`templates/cockpit_current.html` 是模板文件，生成结果必须保存到 `nl2sql_output/`，不得覆盖模板。

```
用户需求：生成项目驾驶舱
    ↓
步骤0：resolveCockpitTemplate() 解析模板
       ├─ cockpit_current.html 存在 → 使用用户当前版本
       ├─ cockpit_current.html 不存在 → 使用技能基线模板
       └─ regenerate=true → 强制重新生成并存档旧版本
    ↓
步骤1：resolveDomain() × N 生成 sqlMap + spec（自动进化）
       └─ 或由主 agent 直接构造（显式配置格式）
    ↓
步骤2：verify() × N 验证（source=unified：DB 直连 + API 端到端同时验证）
   > agent 全程参与：验证失败 → 返回错误信息给 agent → agent 决定是否重新生成 SQL → 重试验证（最多 3 次，全失败则停止）
   > ⚠️ **前置条件**：params 数量必须与 SQL 中 `?` 总数完全匹配；禁止 `?` 出现在表达式中
    ↓
步骤3：parseSqlMap() → buildChartConfig() 生成图表配置
    ↓
步骤4：encryptSql() 加密所有 SQL
    ↓
步骤5：注入 cockpit_current.html → 输出 HTML（不修改模板文件）
    ↓
步骤6（可选）：applyTweak() 应用局部微调 → 写回 cockpit_current.html（供下次生成使用）
    ↓
步骤7：**完整性校验** — src/generate/page.js 内置 `src/generate/validate_page.js`，自动完成以下 6 项检查 + auto-fix
    ↓
步骤8：**HTML 端到端验证** — src/generate/page.js 内置 `src/verify/index.js` 的 `batchVerifyHtml()`，解析 HTML 中所有加密 SQL，调后端 API 验证全部通过后才写入文件；失败则删除文件并退出
    ↓
步骤9：输出两个文件
  - nl2sql_output/cockpit_preview.html（预览版，保留 CDN URLs）
  - nl2sql_output/cockpit.html（部署版，CDN→本地相对路径）
  - [deploy=true] 同时拷贝到 acm_www/static/cockpit.html
```

**sqlMap 新格式（显式配置，v2）：**

sqlMap 每个条目使用显式 spec，不再依赖 key 名称推断类型。

```javascript
const { generateCockpitChart } = require('{skillDir}/src/generate/page.js');

const sqlMap = {
  // ── sidebar：左侧项目列表，不进 CHART_CONFIG ──────────────────
  'projectList': {
    sql: 'SELECT p.ID, p.NAME, p.COMPLETE_PCT, p.STATUS FROM wsd_plan_project p WHERE p.DEL = 0 AND p.STATUS = \'active\'',
    type: 'sidebar',     // 显式声明为 sidebar
    title: '项目列表'
  },

  // ── KPI 类型图表 ───────────────────────────────────────────────
  'kpi_progress': {
    sql: 'SELECT ID, NAME, COMPLETE_PCT, PLAN_SUM, ACT_SUM FROM wsd_plan_project WHERE ID = ? AND DEL = 0',
    type: 'kpi',
    title: '项目进度',
    scope: 'project',
    spec: {
      kpiType: 'avg_percent',
      valueField: 'COMPLETE_PCT',
      unit: '%',
      thresholds: { green: 80, orange: 60 }
    }
  },

  'kpi_health': {
    sql: 'SELECT COUNT(CASE WHEN FEEDBACK_STATUS = \'2\' AND ACT_END_TIME <= PLAN_END_TIME THEN 1 END) * 100.0 / NULLIF(COUNT(*),0) AS health_score FROM wsd_plan_task WHERE PROJECT_ID = ? AND DEL = 0',
    type: 'kpi',
    title: '任务健康度',
    scope: 'project',
    spec: {
      kpiType: 'health_score',
      valueField: 'health_score',
      unit: '分',
      thresholds: { green: 80, orange: 60 }
    }
  },

  // ── chart 类型图表 ──────────────────────────────────────────────
  'riskHeatmap': {
    sql: 'SELECT PROBABILITY_LEVEL, AFTERMATH_LEVEL, COUNT(*) AS count FROM wsd_risk_register WHERE PROJECT_ID = ? AND IS_CLOSE = \'N\' GROUP BY PROBABILITY_LEVEL, AFTERMATH_LEVEL',
    type: 'chart',
    title: '风险四象限',
    scope: 'project',
    spec: {
      chartType: 'scatter',
      xAxis: 'aftermath_level',
      yAxis: 'probability_level',
      valueField: 'count',
      width: 'full'
    }
  },

  'milestone': {
    sql: 'SELECT t.TASK_NAME, t.PLAN_START_TIME, t.PLAN_END_TIME, t.ACT_END_TIME, t.FEEDBACK_STATUS, u.USER_NAME FROM wsd_plan_task t LEFT JOIN wsd_sys_user u ON t.USER_ID = u.ID WHERE t.PROJECT_ID = ? AND t.TASK_TYPE IN (2,3) AND t.DEL = 0 ORDER BY t.PLAN_END_TIME',
    type: 'chart',
    title: '里程碑节点',
    scope: 'project',
    spec: {
      chartType: 'timeline',
      startField: 'plan_start_time',
      endField: 'plan_end_time',
      labelField: 'task_name',
      width: 'full'
    }
  },

  'resourceLoad': {
    sql: 'SELECT r.ORG_ID, o.ORG_NAME, SUM(t.BUDGET_QTY)/8 AS plan_days, COUNT(DISTINCT r.ID) * ? AS capacity_days, SUM(t.BUDGET_QTY)/8 / (COUNT(DISTINCT r.ID) * ?) * 100 AS load_rate FROM wsd_plan_taskrsrc t JOIN wsd_rsrc_user r ON t.RSRC_ID = r.ID LEFT JOIN wsd_sys_org o ON r.ORG_ID = o.ID WHERE r.ORG_ID IS NOT NULL AND t.PLAN_START_TIME >= ? AND t.PLAN_START_TIME <= ? GROUP BY r.ORG_ID, o.ORG_NAME',
    type: 'chart',
    title: '资源负载分布',
    scope: 'global',    // 全局统计，不需要 projectId
    spec: {
      chartType: 'bar',
      xAxis: 'org_name',
      yAxis: 'load_rate',
      valueField: 'plan_days'
    }
  },

  'kanban': {
    sql: 'SELECT t.ID, t.TASK_NAME, t.STATUS, t.FEEDBACK_STATUS, t.COMPLETE_PCT, t.PLAN_END_TIME, u.USER_NAME AS assignee_name FROM wsd_plan_task t LEFT JOIN wsd_sys_user u ON t.USER_ID = u.ID WHERE t.PROJECT_ID = ? AND t.DEL = 0 ORDER BY t.PLAN_END_TIME',
    type: 'chart',
    title: '任务看板',
    scope: 'project',
    spec: {
      chartType: 'kanban',
      kanbanColumns: [
        { status: 'EDIT',      title: '待开始',  color: '#999' },
        { status: 'APPROVAL',  title: '审批中',  color: '#faad14' },
        { status: 'CONFIRM',   title: '进行中',  color: '#1890ff' },
        { status: 'RELEASE',   title: '已发布',  color: '#52c41a' }
      ]
    }
  }
};

const html = await generateCockpitChart(sqlMap, {
  title: '项目驾驶舱',
  projectId: 61,
  verify: true
});
```

**sqlMap 旧格式兼容**：条目为纯字符串时，内部自动推断 spec 作为兜底。

**ChartSpec 字段说明**：

| 字段 | 位置 | 类型 | 说明 |
|------|------|------|------|
| `type` | entry | string | `kpi` / `chart` / `sidebar` / `table` |
| `scope` | entry | string | `project`（需 projectId）/ `global`（不需要）|
| `sql` | entry | string | SQL 查询语句 |
| `title` | entry | string | 图表标题 |
| `spec.chartType` | spec | string | `bar`/`line`/`pie`/`scatter`/`timeline`/`kanban`/`gantt`/`number` |
| `spec.kpiType` | spec | string | `health_score`/`count`/`avg_percent`/`sum_money`/`ratio_percent` |
| `spec.valueField` | spec | string | 值字段名（SQL 结果中的列名）|
| `spec.unit` | spec | string | 单位：`%`/`分`/`项`/`元` |
| `spec.thresholds` | spec | object | 颜色阈值：`{ green, orange }` |
| `spec.xAxis` | spec | string | X 轴字段（热力图：aftermath_level）|
| `spec.yAxis` | spec | string | Y 轴字段（热力图：probability_level）|
| `spec.width` | spec | string | `third`（1/3宽）/`half`（半宽）/`full`（全宽）|
| `spec.kanbanColumns` | spec | array | 看板列定义：`[{ status, title, color }]` |
| `spec.startField` | spec | string | 时间线开始字段 |
| `spec.endField` | spec | string | 时间线结束字段 |
| `spec.params` | spec | array | 额外业务参数（追加到 projectId 之后的位置），如 `['2024-01-01', '2024-12-31']` |
| `paramsCount` | entry | number | **（推荐声明）** 声明该 SQL 需要的参数总数（含 projectId），生成器据此校验 `?` 占位符数量，提前发现 params 不匹配问题。例：`scope=project` 的 SQL 含 2 个 `?`，则 `paramsCount: 3`（1 个 projectId + 2 个额外参数）|

### params 校验机制（前端运行时）

**问题背景**：前端生成的 SQL 含 `?` 占位符，但 `params` 数组经常为空或不完整，导致后端报 "parameter not found" 错误。

**根本解决方案**：技能在生成 HTML 时同时注入两个常量：

| 常量 | 内容 | 用途 |
|------|------|------|
| `ENCRYPTED_SQL` | AES-256-CBC 加密后的 SQL | 传给后端 execute 接口 |
| `SQL_PLAIN` | 明文 SQL（与 ENCRYPTED_SQL key 一一对应）| 供前端 `buildParams` 运行时校验 `?` 数量 |

`buildParams` 在每次发请求前做以下校验：
- **ERROR**：SQL 有 `?` 但 `params=[]` → 控制台立即报错，指明具体图表和原因
- **WARN**：`params.length > SQL中?数量` → 控制台警告，多余参数被忽略
- **WARN**：`scope=project` 但 `currentProjectId=null` → 控制台警告，图表数据无法加载

**生成者规范**：sqlMap 条目应声明 `paramsCount`，与 SQL 中 `?` 数量精确匹配，从源头消除歧义。


**Schema 源码**：`src/generate/chartSpecSchema.js`

**输出文件：** `{outputPath}/cockpit_{timestamp}.html`
## 核心知识库文件（必须读取）

| 文件 | 路径 | 用途 |
|------|------|------|
| 字段映射 | `knowledge/{dbType}/field_mapping.json` | 字段→中文名、枚举值映射 |
| KPI公式 | `knowledge/shared/kpi_formulas.json` | KPI计算公式（挣值、进度偏差等）|
| KPI规格 | `knowledge/shared/kpi_spec_schema.json` | KPI结构化渲染规范（类型、阈值、颜色）|
| 安全规则 | `knowledge/shared/sql_generation_rules.md` | SQL生成铁律（必读！）|
| 知识库扫描 | `scripts/scanner.js` | 自动进化引擎（域→表→SQL+spec）|

## 达梦数据库知识库生成

技能支持两种方案生成达梦数据库知识库：

### 方案一：驱动方案（自动连接数据库）

自动连接达梦数据库，查询系统表生成知识库。

**要求**：
- Linux/Windows: 安装 dmPython 驱动 (`pip install dmPython`)
- macOS: 安装 pyodbc + 达梦 ODBC 驱动

**使用**：
```bash
# 设置环境变量
export DB_TYPE=dm
export DB_HOST=192.168.1.100
export DB_PORT=5236
export DB_NAME=ACM
export DB_USER=SYSDBA
export DB_PASSWORD=password

# 生成知识库
cd scripts/knowledge
python generate.py
```

### 方案二：转换方案（无需驱动，推荐）

通过导出的表结构文件（SQL/CSV/JSON）转换生成知识库，**无需安装任何数据库驱动**。

**适用场景**：
- 无法安装驱动的环境（如 macOS、受限服务器）
- 离线环境
- 快速部署

**使用方法**：

```bash
cd scripts/knowledge

# 只转换表结构（生成 tables.json）
python3 convert_knowledge.py --input /path/to/structure.sql

# 转换表结构并生成字段映射（生成 tables.json + field_mapping.json）
python3 convert_knowledge.py --input /path/to/structure.sql --mapping

# 同时导入字典数据
python3 convert_knowledge.py --input /path/to/structure.sql --mapping --dict /path/to/dict.csv

# 强制覆盖现有文件
python3 convert_knowledge.py --input /path/to/structure.sql --mapping --force

# 合并多个文件
python3 convert_knowledge.py --inputs file1.sql file2.sql --mapping --force
```

**支持的输入格式**：
| 格式 | 说明 | 示例来源 |
|------|------|---------|
| `.sql` | 达梦 CREATE TABLE 脚本 | DM Manager 导出 |
| `.csv` | 表结构 CSV 文件 | DM Manager 导出 |
| `.json` | 自定义 JSON 格式 | 其他工具导出 |

**输出文件**（自动覆盖）：
- `knowledge/dm/tables.json` - 表结构信息
- `knowledge/dm/field_mapping.json` - 字段映射和枚举值

**Python 接口**（供 agent 调用）：
```python
import sys
sys.path.append('.')
from scripts.knowledge.convert_knowledge import convert

# 只转换表结构
result = convert('/path/to/structure.sql')

# 转换表结构并生成字段映射
result = convert('/path/to/structure.sql', generate_mapping=True)

# 同时导入字典数据
result = convert('/path/to/structure.sql', generate_mapping=True, dict_file='/path/to/dict.csv')

if result['success']:
    print(f"✅ 转换成功: {result['tables_count']} 个表")
    if 'field_count' in result:
        print(f"   字段映射: {result['field_count']} 个字段")
else:
    print(f"❌ 转换失败: {result['message']}")
```

---

## 多数据库支持

技能支持 MySQL、Oracle、达梦（DM）三种数据库的 SQL 生成，通过 `DB_TYPE` 环境变量配置。

### 配置方式

| 环境变量 | 可选值 | 默认值 | 说明 |
|---------|-------|-------|------|
| `DB_TYPE` | `mysql` / `oracle` / `dm` | `mysql` | 目标数据库类型 |
| `DB_HOST` | IP/域名 | `192.168.3.25` | 数据库地址 |
| `DB_PORT` | 端口号 | `3306` | 数据库端口 |
| `DB_NAME` | 库名 | `acm_cloud_acm` | 数据库名称 |
| `DB_USER` | 用户名 | `root` | 数据库用户 |
| `DB_PASSWORD` | 密码 | `Wisdom83248380` | 数据库密码 |
| `ORACLE_HOST` | IP/域名 | `192.168.3.25` | Oracle 主机 |
| `ORACLE_PORT` | 端口号 | `1521` | Oracle 端口 |
| `ORACLE_SERVICE` | 服务名 | `orcl` | Oracle 服务名 |
| `ORACLE_USER` | 用户名 | `acm` | Oracle 用户 |
| `ORACLE_PASSWORD` | 密码 | `acm` | Oracle 密码 |

### 方言差异说明

| 语法 | MySQL | Oracle | 达梦 |
|------|-------|--------|------|
| 标识符引号 | `\`field\`` | `"field"` | `"field"` |
| 分页 | `LIMIT offset, count` | 三层 ROWNUM 子查询 | `LIMIT count OFFSET offset` |
| 字符串拼接 | `CONCAT(a, b)` / `a \|\| b` | `a \|\| b` | `a \|\| b` |
| 当前时间 | `NOW()` | `SYSDATE` | `SYSTIMESTAMP` |
| NULL 替换 | `IFNULL(a, b)` | `NVL(a, b)` | `IFNULL(a, b)` |
| 日期减法 | `DATE_SUB(col, INTERVAL n DAY)` | `col - n` | `col - n` |
| **日期转字符串** | `DATE_FORMAT(col, '%Y-%m')` | `TO_CHAR(col, 'YYYY-MM')` | **`SUBSTR(CAST(col AS VARCHAR), 1, 7)`** ⚠️ |
| **GROUP BY + COUNT(*)** | ✅ | ✅ | ⚠️ ShardingSphere 归并 bug，前端聚合 |

> ⚠️ **达梦特别警示**：
> - `TO_CHAR` 在达梦中**不适用**于日期格式转换，必须用 `SUBSTR(CAST(... AS VARCHAR), 1, 7)`
> - `GROUP BY + COUNT(*)` 在 ShardingSphere 分片下有归并 bug，应返回原始数据由前端聚合

### 使用示例

```bash
# MySQL（默认）
DB_TYPE=mysql node src/verify/index.js "SELECT * FROM wsd_plan_task LIMIT 3"

# Oracle
DB_TYPE=oracle node src/verify/index.js "SELECT * FROM wsd_plan_task WHERE ROWNUM <= 3"

# 达梦
DB_TYPE=dm node src/verify/index.js "SELECT * FROM wsd_plan_task LIMIT 3 OFFSET 0"
```

### 生成脚本时的数据库指定

```bash
# 指定 Oracle 重新生成知识库
DB_TYPE=oracle python3 scripts/knowledge/generate.py --apply --target tables
```

### 内部 Dialect 架构

`src/core/dialect.js` 封装了所有数据库特定语法：

```javascript
const { createDialect } = require('./core/dialect.js');
const dialect = createDialect('oracle');

dialect.quote('field_name');           // "field_name"
dialect.applyPagination(sql, 0, 20);    // Oracle 三层分页
dialect.stripPagination(sql);          // 还原为 base SQL
dialect.limit('SELECT * FROM t', 0, 3);  // LIMIT 3
```

## 输入参数

### 必需参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `question` | string | 用户的自然语言问题（中文） |
| `projectId` | number | 项目上下文ID |

### 可选参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `epsId` | number | EPS上下文ID |
| `chartType` | string | 图表类型：`line`/`bar`/`pie`/`heatmap`/`table` |
| `chartTitle` | string | 图表标题 |
| `outputPath` | string | HTML输出路径（默认 `./nl2sql_output/`）|

### 鉴权说明

**JWT 获取方式：**
```
POST /api/auth/jwt/token
Body: { "userName": "admin@wisdomidata", "password": "<加密后的密码>" }
```

**密码加密方式（AES-128-CBC）：**
```javascript
// 加密算法见 acm_www/utils/AesUtil.js
const encryptedPassword = AesUtil.aesEncrypt('123456');
// 结果如: "fGs/2dJVyyTryPB4pNB8nQ=="
```

**请求头格式（重要！）：**
```
Authorization: <JWT字符串>
```
⚠️ 注意：是直接 `Authorization: <JWT>`，不是 `Authorization: Bearer <JWT>`！

**Token 缓存要求（重要！）**
生成的 HTML 页面必须内置 token 缓存机制，确保：
- 页面生命周期内只请求一次 token
- 后续请求复用缓存的 token，避免重复调用
- 使用 Promise 缓存防止并发请求时产生多个 token 请求

```javascript
// 正确示例
let jwtToken = null;
let tokenPromise = null;

async function getToken() {
    if (jwtToken) return jwtToken;
    if (tokenPromise) return tokenPromise;  // 防止并发请求时产生多个 token 请求
    tokenPromise = fetch(...).then(r => r.json()).then(d => jwtToken = d.data).finally(() => tokenPromise = null);
    return tokenPromise;
}
```

后端通过 `HttpClientUtil.getLoginUserVo().getTenantId()` 从 Gateway 设置的请求头中获取租户ID，无需客户端传入。

### 输入方式

**方式1：直接提问**
```
用户：请帮我查一下A项目延期未完成的任务有哪些？
→ question="A项目的延期未完成任务有哪些"
```

**方式2：生成图表页面**
```
用户：请帮我生成一个风险热力图页面
→ chartType="heatmap", chartTitle="风险热力图", question="项目风险四象限分布"
```

### 动态参数传递

前端调用 `executeQuery` 时，通过 `params` 数组传递动态参数：

```javascript
// 无参数
executeQuery('staticSql')

// 有参数（按顺序对应 SQL 中的 ?）
executeQuery('dynamicSql', [projectId])
executeQuery('dateRangeSql', ['2026-01-01', '2026-03-27'])

// 动态日期示例
const today = new Date().toISOString().split('T')[0]  // '2026-03-27'
const startOfYear = today.substring(0, 4) + '-01-01'    // '2026-01-01'
executeQuery('resourceLoad', [startOfYear, today])
```

**注意**：
- SQL 中 `?` 的数量必须与 params 数组长度一致
- 参数顺序对应 SQL 中 `?` 的出现顺序

### 查询模式：单项目 vs 全局

SQL 分为两种模式，生成前必须先判断用户需求属于哪种：

| 模式 | 特征关键词 | 典型问题 | projectId 参数 |
|------|-----------|---------|---------------|
| **单项目** | "某项目"、"这个项目"、"项目61" | "项目61的延期任务有哪些" | 必须传入 |
| **全局/跨项目** | "全部项目"、"所有任务"、"公司级"、"全公司"、"本月汇总" | "本月全公司延期任务有哪些"、"查询所有延期未完成的任务" | 不需要 projectId |

**识别规则（优先级从高到低）**：

1. 显式指定项目名称/ID → 单项目
2. 包含"全部"、"所有"、"全局"、"公司级"、"本月"、"本季"、"本年" → 全局
3. 无明确范围修饰词 → 默认单项目（需 projectId）

**全局查询 SQL 示例**：

```sql
-- 查询全公司延期未完成的任务（无 projectId 过滤）
SELECT t.ID, t.TASK_NAME, t.STATUS, t.FEEDBACK_STATUS, t.PLAN_END_TIME,
       p.NAME AS project_name, u.USER_NAME AS assignee_name
FROM wsd_plan_task t
LEFT JOIN wsd_plan_project p ON t.PROJECT_ID = p.ID AND p.DEL = 0
LEFT JOIN wsd_sys_user u ON u.ID = t.USER_ID
WHERE t.DEL = 0
  AND t.FEEDBACK_STATUS IN ('0', '1')
  AND t.PLAN_END_TIME < CURDATE()
ORDER BY t.PLAN_END_TIME
LIMIT 20

-- 按组织统计本月延期任务数（GROUP BY org）
SELECT o.ORG_NAME, COUNT(*) AS delayed_count
FROM wsd_plan_task t
JOIN wsd_sys_org o ON t.ORG_ID = o.ID
WHERE t.DEL = 0
  AND t.FEEDBACK_STATUS IN ('0', '1')
  AND t.PLAN_END_TIME >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
GROUP BY o.ORG_NAME, o.ID
ORDER BY delayed_count DESC

-- EPS级汇总（wsd_plan_project.PARENT_ID = epsId）
SELECT p.ID, p.NAME, COUNT(t.ID) AS task_count,
       SUM(CASE WHEN t.FEEDBACK_STATUS = '2' THEN 1 ELSE 0 END) AS completed_count
FROM wsd_plan_project p
LEFT JOIN wsd_plan_task t ON t.PROJECT_ID = p.ID AND t.DEL = 0
WHERE p.DEL = 0 AND p.PARENT_ID = ?
GROUP BY p.ID, p.NAME
```

**cockpit sqlMap 中的全局 SQL 标记**：

当驾驶舱需要包含全局数据（如"公司风险TOP10"）时，sqlMap 条目标记 `scope: 'global'`，表示不注入 projectId：

```javascript
const sqlMap = {
  // 项目级看板（需要 projectId）
  'kanban': {
    sql: 'SELECT t.ID, t.TASK_NAME, ... FROM wsd_plan_task t WHERE t.PROJECT_ID = ? AND t.DEL = 0 ...',
    scope: 'project'  // 默认
  },
  // 全局统计（不需要 projectId）
  'companyRiskCount': {
    sql: 'SELECT risk_level, COUNT(*) FROM wsd_risk_register WHERE IS_CLOSE = \'N\' GROUP BY risk_level',
    scope: 'global'
  }
};
```

## 自动进化流程（推荐）

当用户的业务需求在 sqlMap 中没有预定义时，使用 `knowledgeBaseScanner.js` 从知识库动态生成完整的 sqlMap 条目（SQL + 显式 spec）。

### 自动化入口

```javascript
const { resolveDomain } = require('{skillDir}/scripts/scanner.js');

// 用户需求："帮我生成项目驾驶舱，重点关注任务延期和资源负载"
const domain1 = '任务延期情况';
const domain2 = '资源负载分布';

const result1 = resolveDomain(domain1, { projectId: 61 });
const result2 = resolveDomain(domain2, { projectId: 61 });

if (!result1.found) {
  // 返回明确提示，让用户知道哪些不支持
  return { supported: false, suggestion: result1.suggestion };
}

// 合并到 sqlMap
const sqlMap = {
  ...(result1.found ? { [result1.entry.key]: result1.entry } : {}),
  ...(result2.found ? { [result2.entry.key]: result2.entry } : {}),
};

// 调用 cockpit 生成器
const { generateCockpitChart } = require('{skillDir}/src/generate/page.js');
const html = await generateCockpitChart(sqlMap, { projectId: 61, verify: true });
```

### resolveDomain 内部流程

```
用户业务域描述（如"任务延期情况"）
    ↓
classifyDomain()
    ├── DOMAIN_TABLE_MAP 精确/模糊匹配 → 表名
    └── 匹配失败 → searchTables() 扫描 tables.json
    ↓
getTableSchema() → 读取表字段结构
    ↓
inferSpecFromDomain() → 推断 type / chartType / kpiType / thresholds
    ↓
buildSQL() → 生成 SQL（自动 JOIN、WHERE、LIMIT）
    ↓
返回完整 entry: { key, sql, type, title, scope, spec }
```

### 域 → 表 映射（DOMAIN_TABLE_MAP）

| 域关键词 | 表 | 说明 |
|---------|-----|------|
| 任务/延期/task | wsd_plan_task | 任务主表 |
| 项目/project | wsd_plan_project | 项目主表 |
| 风险/risk | wsd_risk_register | 风险登记台账 |
| 资源/负载/resource | wsd_plan_taskrsrc | 资源分配表 |
| 里程碑/milestone | wsd_plan_task (task_type IN 2,3) | 里程碑是任务子集 |
| 会议/meeting | wsd_comu_meeting | 会议表 |
| 交付物/deliverable | wsd_plan_delvassign | 交付物表 |

### spec 推断规则

| 域关键词 | type | chartType/kpiType | 说明 |
|---------|------|-------------------|------|
| 健康度/health | kpi | health_score | 健康度评分 |
| 风险数/风险敞口 | kpi | count | 风险项数计数 |
| 完成率指标 | kpi | avg_percent | 完成率百分比 |
| 热力/四象限 | chart | scatter | 风险热力图 |
| 时间线/里程碑 | chart | timeline | 里程碑时间线 |
| 看板/kanban | chart | kanban | 任务看板 |
| 甘特/gantt | chart | gantt | 甘特图 |
| 资源负载 | chart | bar | 部门资源柱图 |
| 占比/分布/pie | chart | pie | 饼图 |
| 趋势/trend | chart | line | 趋势折线图 |

### 未知域处理（found: false）

```javascript
const r = resolveDomain('XYZ业务域', {});
if (!r.found) {
  // r.suggestion 包含原因
  // 仍然可以尝试 searchTables(keyword) 手动查找相关表
  const alternatives = searchTables('XYZ关键词');
  if (alternatives.length > 0) {
    // 可以让用户选择对应的表
  }
}
```

### 手动扩展 DOMAIN_TABLE_MAP

如需支持新的业务域，在 `knowledgeBaseScanner.js` 的 `DOMAIN_TABLE_MAP` 中添加：

```javascript
const DOMAIN_TABLE_MAP = {
  // ... 现有映射
  '设备保修期': { table: 'wsd_equip_warranty', comment: '设备保修' },
  '采购合同':   { table: 'wsd_bud_contract',   comment: '合同' },
};
```

**说明**：`knowledgeBaseScanner.js` 同时扫描 `tables.json`，即使不在 `DOMAIN_TABLE_MAP` 中，也可以通过关键词搜索定位到对应表（searchTables 支持表名/表注释/字段名搜索）。

### auto-evolution 持久化

`resolveDomain()` 首次推理成功时会自动将新条目写入 `knowledge/shared/evolved_domains.json`，下次相同域请求直接命中，无需重新推理。

如需清除沉淀记录，删除 `knowledge/shared/evolved_domains.json` 即可（技能会重新初始化为空对象）。

## SQL 生成方法

### 主 agent 直接生成（不调用外部 LLM）

主 agent 基于知识库上下文直接生成 SQL：

1. **读取安全规则**（sql_generation_rules.md）— 了解铁律
2. **读取字段映射**（field_mapping.json）— 了解字段名和枚举值
3. **读取 KPI 公式**（kpi_formulas.json）— 了解健康度、挣值等计算逻辑
4. **生成 SQL** — 根据用户问题结合知识库上下文构造查询
5. **验证 SQL** — 调用 `src/verify/index.js` 的 `verify()` 确认可执行（默认 unified 模式：DB + API 同时验证）
6. **返回结果** — 输出 SQL 和查询结果

### 何时使用动态参数

**核心原则**：
- 凡是**前端需要动态传入**的值，一律用 `?` 占位
- 凡是**用户意图包含动态时间**（今天、本月、本年），用 `?` 占位
- 静态的枚举值、确定的项目ID，可直接写死

| 场景 | 示例 | SQL 写法 |
|------|------|---------|
| 用户说"当前" | "截至今天的计划工时" | `WHERE plan_time >= ?` |
| 用户说"本月" | "本月风险分布" | `WHERE create_time >= ?` |
| 用户选择项目 | 项目下任务统计 | `WHERE project_id = ?` |
| 前端需动态计算 | 当前日期范围 | `AND plan_time >= ? AND plan_time <= ?` |

**常见错误**：
- ❌ `WHERE create_time >= '2026-01-01'` — 硬编码日期，不灵活
- ✅ `WHERE create_time >= ?` — 前端传参，动态适配

### SQL 生成示例

**问题：** 某项目的延期未完成任务有哪些？

**生成的 SQL：**
```sql
SELECT t.id, t.task_name, t.status, t.feedback_status, t.plan_end_time,
       u.user_name AS assignee_name, t.complete_pct
FROM wsd_plan_task t
LEFT JOIN wsd_sys_user u ON u.id = t.user_id
WHERE t.project_id = ?
  AND t.DEL = 0
  AND t.feedback_status IN ('0', '1')
  AND t.plan_end_time < CURDATE()
ORDER BY t.plan_end_time
LIMIT 20
```

### 带动态参数的 SQL 示例

**问题**：截至今天的资源负载分布

**分析**：
- 用户说"今天" → 需要动态日期
- 资源负载按部门统计 → 不用按项目过滤
- 前端需要传入起始日期和结束日期

**生成的 SQL**：
```sql
SELECT r.ORG_ID, o.ORG_NAME as dept_name,
       COUNT(DISTINCT r.ID) as resource_count,
       SUM(t.BUDGET_QTY) / 8 as total_plan_days,
       COUNT(DISTINCT r.ID) * ? as total_capacity_days,
       SUM(t.BUDGET_QTY) / 8 / (COUNT(DISTINCT r.ID) * ?) * 100 as load_rate
FROM wsd_plan_taskrsrc t
JOIN wsd_rsrc_user r ON t.RSRC_ID = r.ID
LEFT JOIN wsd_sys_org o ON r.ORG_ID = o.ID
WHERE r.ORG_ID IS NOT NULL
  AND t.PLAN_START_TIME >= ?
  AND t.PLAN_START_TIME <= ?
GROUP BY r.ORG_ID, o.ORG_NAME
ORDER BY load_rate DESC
LIMIT 10
```

**前端调用**：
```javascript
const today = new Date()
const startOfYear = new Date(today.getFullYear() + '-01-01')
const totalDays = Math.ceil((today - startOfYear) / (1000 * 60 * 60 * 24))
const workingDays = Math.round(totalDays * 252 / 365)  // 工作日 = 总天数 × 252/365

executeQuery('resourceLoad', [workingDays, workingDays, startOfYear.toISOString().split('T')[0], today.toISOString().split('T')[0]])
// params[0] → working_days（容量公式）
// params[1] → working_days（负载率公式）
// params[2] → 起始日期
// params[3] → 结束日期
```

**资源负载算法**（2026-03-30 更新）：
```
负载率 = Y / (N × X) × 100%
  Y = 预估工时人天 = SUM(BUDGET_QTY) / 8
  N = 资源人员数量 = COUNT(DISTINCT RSRC_ID)
  X = 工作日天数 = 日期范围内总天数 × (252/365)
  阈值：<70% 空闲 / 70-90% 正常 / >90% 过载
```

## 调用脚本

### src/verify/index.js — SQL 验证（统一验证引擎）

提供三种验证模式，**默认使用 `unified`（DB 直连 + API 端到端同时验证）**：

```bash
# 默认：unified（DB 直连 + API 同时验证，以 DB 为准）
node {skillDir}/src/verify/index.js --sql "SELECT ..."

# 仅 MySQL 直连
node {skillDir}/src/verify/index.js --sql "SELECT ..." --source db

# 仅 HTTP API
node {skillDir}/src/verify/index.js --sql "SELECT ..." --source api
```

**批量 HTML 端到端验证**（Cockpit 页面生成后自动调用，无需手动）：
```javascript
const { batchVerifyHtml } = require('{skillDir}/src/verify/index.js');
const result = await batchVerifyHtml('/path/to/cockpit.html', { projectId: 61 });
// result: { passed, failed, skipped, results }
if (result.failed > 0) throw new Error('HTML 端到端验证失败');
```

**统一返回格式**：
```json
{
  "ok": true,
  "rows": 3,
  "fields": ["ID", "TASK_NAME", "PLAN_END_TIME"],
  "sampleRows": [...],
  "sources": {
    "mysql": { "ok": true, "rows": 3, "fields": [...], "error": null },
    "api":   { "ok": true, "rows": 3, "error": null }
  },
  "error": null
}
```

---

### src/security/encryptSql.js — AES-256-CBC 加密

对 SQL 进行加密，用于嵌入 HTML 页面：

```bash
node {skillDir}/src/security/encryptSql.js encrypt "SELECT * FROM ..."
```

返回：
```json
{
  "ciphertext": "a1b2c3...",
  "iv": "x9y8z7..."
}
```

**⚠️ 重要：加密逻辑不得自行重写**

加密算法为 **AES-256-CBC + HMAC-SHA256（Encrypt-then-MAC）**，实现细节在 `src/security/encryptSql.js` 中。**其他脚本需要批量加密 SQL 时，必须 require 该模块**，禁止自行实现加密逻辑。

```javascript
// ✅ 正确：从 src/security/encryptSql.js 引入
const { encrypt } = require('{skillDir}/src/security/encryptSql.js');
const { ciphertext, iv } = encrypt(sql);

// ❌ 错误：自行实现（会导致 HMAC 验签失败）
const iv = crypto.randomBytes(16);
const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
// ...
```

### src/generate/page.js — 页面生成器（流程二 + 流程三）

支持单图表和驾驶舱两种生成模式：

**单图表模式（流程二）：**
```bash
node {skillDir}/src/generate/page.js "<sql>" --title "<标题>" --type <chartType>
```

**驾驶舱模式（流程三）：**
```bash
node {skillDir}/src/generate/page.js \
  --template cockpit \
  --charts projectList.sql,kpi_health.sql,riskHeatmap.sql \
  --title "项目驾驶舱" \
  --project-id 61 \
  --output cockpit.html
```
> 注意：`--charts` 参数接收的是 SQL 文件路径，文件内容由主 agent 预先准备。

## 模板管理

### 模板文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| 单图表模板 | `skills/templates/html_page_template.html` | 技能自带，始终不变 |
| 驾驶舱基线模板 | `skills/templates/cockpit_template.html` | 首次生成后存入，布局重构时更新 |
| 驾驶舱当前模板 | `workspace/templates/cockpit_current.html` | 用户当前最新版本，实时跟随用户调整 |

**模板加载优先级**：

```
workspace/templates/cockpit_current.html   ← 优先（用户当前版本）
    ↓ 不存在时
skills/templates/cockpit_template.html    ← 降级（技能基线）
```

### 模板生命周期

| 场景 | 触发条件 | 结果 |
|------|---------|------|
| 首次生成 | 用户首次提出驾驶舱需求（附带材料）| 生成 → 存入 cockpit_current.html + cockpit_template.html |
| 数据更新 | 用户只换了数据范围/时间 | 读取 cockpit_current.html → 注入新数据 |
| 局部微调 | 用户说"左侧调窄/颜色调深" | 修改 cockpit_current.html → 下次输出即反映调整 |
| 布局重构 | 用户换了布局设计或加 `--regenerate` | 重新分析材料 → 覆盖 cockpit_current.html + cockpit_template.html |

### 🚨 模板强制规范（所有模板必须遵守）

**无论内置模板还是 regenerate 新生成的模板，无论驾驶舱还是单图表，都必须包含鉴权组件。**
这是技能层面的设计约束，不满足则生成流程报错退出。

#### 通用规范（所有模板类型）

##### 必须包含的 JS 函数

| 函数 | 说明 |
|------|------|
| `getToken()` | 三级优先级获取 token：currentToken 缓存 → sessionStorage → 弹窗登录 |
| `doLogin()` | 调用 `${API_AUTH_BASE}/jwt/token` 登录，写入 sessionStorage.setItem('token') |

##### 必须包含的 DOM / 变量

| 组件 | 说明 |
|------|------|
| `id="loginModal"` | 登录弹窗 DOM |
| `const API_AUTH_BASE = '{{API_AUTH_BASE}}'` | 认证接口变量声明 |
| CryptoJS CDN | `<script src="...crypto-js...">`，用于 AES 密码加密 |
| `sessionStorage.setItem('token', ...)` | 登录成功后必须写入 |
| `sessionStorage.getItem('token')` | getToken() 必须读取以复用 ACM token |
| `tokenPromise` 并发保护 | `if (tokenPromise) return tokenPromise` |

##### 禁止事项

- ❌ 在 `doLogin()` 的 body 中硬编码 password 字符串
- ❌ 使用字符串拼接构造 `${API_BASE}/jwt/token`（须用 `${API_AUTH_BASE}` 变量）

#### 驾驶舱模板专用

##### 占位符

| 占位符 | 说明 |
|--------|------|
| `{{ENCRYPTED_SQL}}` | AES-256-CBC 加密后的 SQL，JSON 格式（key → {ciphertext, iv}）|
| `{{SQL_PLAIN}}` | 明文 SQL（供 buildParams 运行时校验 ? 数量），JSON 格式 |
| `{{CHART_CONFIG}}` | 图表配置数组，JSON 格式 |
| `{{API_BASE}}` | API 基础路径 |
| `{{API_AUTH_BASE}}` | 认证 API 基础路径 |

##### JS 函数

| 函数 | 说明 |
|------|------|
| `executeQuery(key, params)` | 调后端 execute 接口，携带 Authorization header |
| `buildParams(cfg)` | 组装参数数组（含 ? 占位符数量校验），projectId 置于最前面 |
| `loadAllData()` | 加载所有图表数据 |

#### 单图表模板专用

##### 占位符

| 占位符 | 说明 |
|--------|------|
| `{{ENCRYPTED_SQL}}` | AES-256-CBC 加密后的 SQL |
| `{{IV}}` | AES 加密 IV |
| `{{API_BASE}}` | API 基础路径 |
| `{{API_AUTH_BASE}}` | 认证 API 基础路径 |
| `{{CHARTS_CONFIG}}` | 图表配置 |

##### JS 函数

| 函数 | 说明 |
|------|------|
| `fetchData()` | 调 API 获取数据 |

#### 校验机制

| 场景 | 校验方式 |
|------|---------|
| 内置 cockpit 模板 | `validateTemplates()` → cockpit_template.html |
| 内置单图表模板 | `validateTemplates()` → html_page_template.html |
| regenerate 驾驶舱新模板 | `validateTemplateContent(html, { type: 'cockpit' })` |
| regenerate 单图表新模板 | `validateTemplateContent(html, { type: 'single-chart' })` |

### 模板生成流程

**触发：首次生成驾驶舱 或 布局重构**

```
用户提供材料（cockpit.png + cockpit.xlsx 或详细文字描述）
    ↓
agent 分析材料
    ├─ 布局结构（顶部/左侧/右侧/中间区块）
    ├─ 组件类型（KPI gauge / ECharts 类型 / 侧边栏样式）
    └─ 样式定义（配色/字体/间距）
    ↓
生成完整 HTML（含 CSS/ECharts/鉴权逻辑 + 占位符）
    ↓
存入 workspace/templates/cockpit_current.html
同时更新 skills/templates/cockpit_template.html（基线）
↓
[deploy=true] 自动部署到 acm_www/static/（不存在时兜底到 nl2sql_output/；CDN 路径替换为本地相对路径）
```

### 局部微调

**触发：用户说"把左侧列表宽度调窄一点"**

```javascript
const html = await generateCockpitChart(sqlMap, {
    projectId: 61,
    tweak: '左侧宽度调窄',
    deploy: true  // 自动部署到 acm_www/static/（不存在时兜底到 nl2sql_output/）
});
// cockpit_current.html 被更新，下次直接生效
```

**支持的微调关键词：**

| 关键词 | 效果 |
|--------|------|
| 左侧宽度调窄 | 侧边栏宽度 → 180px |
| 左侧宽度调宽 | 侧边栏宽度 → 280px |
| KPI放大 | KPI 卡片尺寸放大 |
| KPI缩小 | KPI 卡片尺寸缩小 |
| 颜色加深 | 主色调 → `#1a3a5c` |
| 颜色调浅 | 主色调 → `#4a90d9` |
| 去掉右侧 | 隐藏右侧活动流区块 |
| 去掉顶部 | 隐藏顶部导航区块 |

**微调机制**：修改直接作用于 `cockpit_current.html`，不影响基线模板 `cockpit_template.html`。用户每次微调都实时更新同一个文件。

### src/generate/page.js 调用方式

```javascript
const { generateCockpitChart, resolveCockpitTemplate, applyTweak } = require('{skillDir}/src/generate/page.js');

// 正常使用（读取 cockpit_current.html）
const html = await generateCockpitChart(sqlMap, {
    title: '项目驾驶舱',
    projectId: 61,
    verify: true,
    deploy: true  // 生成后自动部署（兜底目录：nl2sql_output/）
});

// 局部微调（应用 tweak 并更新 cockpit_current.html）
const html2 = await generateCockpitChart(sqlMap, {
    title: '项目驾驶舱',
    projectId: 61,
    tweak: '左侧宽度调窄'
});

// 强制重新生成模板（覆盖 cockpit_current.html + 存档旧版本）
const html3 = await generateCockpitChart(sqlMap, {
    title: '项目驾驶舱',
    projectId: 61,
    regenerate: true,
    templateContent: newTemplateHtml  // 从用户新材料生成
});
```

### 占位符规范

| 占位符 | 注入内容 | 格式 |
|--------|---------|------|
| `{{PAGE_TITLE}}` | 页面标题 | 字符串 |
| `{{CHART_CONFIG}}` | 图表配置数组 | JSON 字符串 |
| `{{ENCRYPTED_SQL}}` | SQL 加密结果映射 | JSON 字符串 `{"key": {"ciphertext","iv"}}` |
| `{{DEFAULT_PROJECT_ID}}` | 默认项目 ID | 数字字符串 |
| `{{API_BASE}}` | API 基础路径 | URL 字符串 |

## 输出

### NL→SQL 预览输出

```json
{
  "sql": "SELECT t.id, t.task_name, t.status, t.feedback_status, t.plan_end_time FROM wsd_plan_task t WHERE t.project_id = ? AND t.DEL = 0 AND t.feedback_status IN ('0','1') AND t.plan_end_time < CURDATE() LIMIT 20",
  "explanation": "已根据您的问题生成SQL查询，共返回5条延期未完成的任务。延期判定条件：feedback_status IN ('0','1') 且 plan_end_time < 当前日期。",
  "data": [
    {"id": 1, "task_name": "XXX任务", "status": "RELEASE", "feedback_status": "1", "plan_end_time": "2026-03-01"},
    ...
  ],
  "total": 5,
  "ok": true
}
```

### 结构化 KPI 输出（给驾驶舱用）

KPI 数据建议返回结构化格式，前端根据 `status` 直接渲染颜色，无需二次判断：

```json
{
  "kpi_progress": {
    "value": 87.50,
    "formatted": "87.50%",
    "status": "normal",
    "trend": "+2.3%",
    "thresholds": { "warning": 80, "danger": 60 }
  },
  "kpi_health": {
    "value": 85,
    "formatted": "85",
    "status": "normal",
    "thresholds": { "warning": 80, "danger": 60 }
  },
  "kpi_risk": {
    "value": 10,
    "formatted": "10项",
    "status": "danger",
    "thresholds": { "warning": 8, "danger": 3 }
  }
}
```

**status 颜色映射**：

| status | 颜色 | 含义 | 典型阈值（健康度）|
|--------|------|------|----------------|
| `normal` | 🟢 绿色 | 正常/达标 | ≥80分 |
| `warning` | 🟡 橙色 | 轻度风险 | 60-80分 |
| `danger` | 🔴 红色 | 严重问题 | <60分 |

**SQL 层返回原始聚合值（不含 status）**，status 由驾驶舱 JS 根据 `kpi_spec_schema.json` 的阈值规则计算得出。

详细 Schema 定义见：`knowledge/shared/kpi_spec_schema.json`

### HTML 页面输出

生成完整的自包含 HTML 文件，包含：
- ECharts 5.x（CDN加载）
- 已加密的 SQL（`{{ENCRYPTED_SQL}}`）
- AES-256-CBC IV（`{{IV}}`）
- JWT 鉴权令牌（`{{JWT_TOKEN}}`）
- 指定的图表类型和配置
- 数据获取和渲染逻辑（自动携带 Authorization header 请求后端）

输出路径：`{outputPath}/{chartTitle}_{timestamp}.html`

## 图表类型与配置

| 图表类型 | 适用场景 | ECharts类型 |
|---------|---------|------------|
| `line` | 趋势图、时间序列 | line |
| `bar` | 对比图、柱状图 | bar |
| `pie` | 占比图、饼图 | pie |
| `heatmap` | 风险热力图（X/Y轴）| scatter（热力配色）|
| `table` | 明细数据列表 | 无（纯HTML表格）|

## 数值显示规范

**生成 HTML 页面时，数值字段必须遵循以下格式规范：**

| 字段类型 | 显示格式 | 示例 |
|---------|---------|------|
| 百分比字段（`_PCT`、`_RATE`、`COMPLETE`） | 2位小数 + `%` | `87.50%` |
| 金额字段（`_SUM`、`_BUDGET`、`_COST`） | 2位小数 | `¥1,234.56` |
| 比率字段（`_RATIO`） | 2位小数 + `%` | `95.00%` |
| 计数字段（`_COUNT`） | 整数（千分位分隔）| `1,234` |
| 普通数值 | 2位小数 | `123.45` |

**百分比统计规则：**
- 百分比字段统计应计算 **平均值（AVG）**，而非求和（SUM）
- 示例：`COMPLETE_PCT` 的统计应显示"平均"而非"合计"

**金额统计规则：**
- 金额字段统计应计算 **求和（SUM）**
- 示例：`PLAN_SUM` 的统计应显示"合计"

**实现参考（src/generate/page.js）：**
```javascript
const NUMERIC_FIELD_PATTERNS = [
    { pattern: /_PCT$/i, type: 'numeric', agg: 'avg' },   // 百分比→平均
    { pattern: /_RATE$/i, type: 'numeric', agg: 'avg' },   // 比率→平均
    { pattern: /COMPLETE/i, type: 'numeric', agg: 'avg' }, // 完成率→平均
    { pattern: /_SUM$/i, type: 'numeric', agg: 'sum' },    // 金额→求和
    { pattern: /_BUDGET$/i, type: 'numeric', agg: 'sum' }, // 预算→求和
    { pattern: /_COUNT$/i, type: 'numeric', agg: 'sum' },   // 计数→求和
];
```

## SQL 生成铁律

**生成 SQL 前必须遵守：**

1. **永远不猜测，先求证事实** — 字段名/列名必须对照 `tables.json` 确认实际名称，字段映射文件（如 `field_mapping.json`）中的字段名若有误，以 `tables.json` 为准
2. **只生成 SELECT 查询** — 禁止 UPDATE/DELETE/INSERT/DROP/TRUNCATE
3. **强制租户隔离** — 后端通过 `getLoginUserVo().getTenantId()` 自动注入租户ID，**Skill 生成的 SQL 不需要包含 `AND TENANT_ID = ?`**，也不需要传 tenantId 参数。`src/verify/index.js` 本地验证时不需要 `--tenant-id` 参数。
4. **强制 DEL=0** — 几乎所有表加 `AND DEL = 0`，但 `wsd_risk_register`、`wsd_base_dict`、`wsd_comu_meeting`、`wsd_comu_meetingaction`、`wsd_plan_taskrsrc` 等无 DEL 字段的表禁止加此条件
5. **参数化查询** — 
   - 前端动态值用 `?` 占位：`WHERE project_id = ?`
   - 动态日期范围用 `?` 占位：`AND plan_time >= ? AND plan_time <= ?`
   - 前端传入 params 数组替换占位符
   - 禁止字符串拼接 SQL
6. **LIMIT 限制** — 默认 20 条，最大不超过 100 条
7. **枚举值正确格式** — `feedback_status='0'`（字符串）、`status='RELEASE'`（大写）
8. **禁止字段** — 不得查询 CREATOR/PASSWORD/TOKEN 等敏感字段

**SQL 验证失败处理流程：**
```
验证失败 → 分析错误原因 → 重新生成 SQL → 再次验证 → 直至通过 → 加密嵌入
```

详细规则见：`knowledge/shared/sql_generation_rules.md`

## 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| SQL 验证失败 | 返回 `valid: false` + 错误信息，不执行 |
| 数据库连接失败 | 返回错误，不生成页面 |
| 加密失败 | 返回错误，不生成页面 |

## 目录结构

```
skills/data-query/
├── SKILL.md                       # 本文件
├── database_specs/                 # 数据库规范文档
│   ├── dialect/
│   │   ├── DM.md                  # 达梦数据库规范
│   │   ├── MySQL.md               # MySQL 数据库规范
│   │   └── Oracle.md              # Oracle 数据库规范
│   └── sharding/
│       └── ROUTING_RULES.md       # 分片路由规则
├── knowledge/                      # 知识库数据
│   ├── dm/                        # 达梦数据库
│   │   ├── field_mapping.json     # 字段映射
│   │   └── tables.json            # 表结构
│   ├── mysql/                     # MySQL 数据库
│   │   ├── field_mapping.json     # 字段映射
│   │   └── tables.json            # 表结构
│   ├── oracle/                    # Oracle 数据库
│   │   ├── field_mapping.json     # 字段映射
│   │   └── tables.json            # 表结构
│   └── shared/                    # 共享配置
│       ├── evolved_domains.json   # 自动进化域映射
│       ├── kpi_formulas.json      # KPI计算公式
│       ├── kpi_spec_schema.json   # KPI规格定义
│       ├── sql_generation_rules.md # SQL生成规则
│       └── sharding/
│           ├── KNOWN_BUGS.md      # 已知分片Bug
│           └── TABLE_DISTRIBUTION.md # 表分布
├── prompts/
│   └── nl2sql_prompt.md           # agent 提示词模板
├── scripts/                        # 独立工具（不引用 src/ 模块）
│   ├── encrypt_for_page.js        # SQL 加密工具（Node）
│   ├── scanner.js                 # 知识库扫描器（Node）
│   └── knowledge/                  # 知识库构建脚本（Python）
│       ├── convert_knowledge.py # 通用知识库转换脚本
│       ├── generate.py            # 知识库生成脚本
│       └── requirements.txt       # Python依赖
├── src/
│   ├── core/
│   │   ├── config.js              # 配置加载（读取 config.json）
│   │   ├── dialect.js             # 数据库方言封装
│   │   ├── errors.js              # 错误处理
│   │   └── validator.js           # 验证工具
│   ├── deploy/
│   │   └── index.js               # 部署（优先 acm_www/static/，兜底 nl2sql_output/）
│   ├── generate/
│   │   ├── chartSpecSchema.js     # 图表配置Schema
│   │   ├── page.js                # 页面生成器（CLI 入口）
│   │   └── validate_page.js       # HTML 完整性校验 + auto-fix
│   ├── security/
│   │   ├── encryptSql.js          # AES-256-CBC 加密核心
│   │   └── passwordEncrypt.js     # 密码加密
│   ├── templates/
│   │   ├── index.js               # 模板管理
│   │   └── validate.js            # 模板验证
│   ├── verify/
│   │   └── index.js               # SQL 验证引擎
│   └── index.js                   # 主入口
├── templates/
│   ├── html_page_template.html     # 单图表页面模板（流程二）
│   └── cockpit_template.html       # 驾驶舱页面模板（流程三）
├── .gitignore                      # Git忽略文件
├── CHANGES.md                      # 变更记录
├── README.md                       # 项目说明
├── config.json                     # 配置文件
├── package-lock.json               # NPM依赖锁定
└── package.json                    # NPM配置
```
