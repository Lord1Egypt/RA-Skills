# data-query 技能

自然语言转 SQL 与可视化页面生成技能。

## 目录结构

```
data-query/
├── SKILL.md                          # 技能定义文档（必读）
├── README.md                          # 本文件
├── CHANGES.md                        # 变更记录
├── .gitignore
│
├── scripts/                           # 脚本工具
│   ├── encrypt_for_page.js            # SQL 加密工具（生成页面前使用）
│   ├── scanner.js                    # 知识库扫描引擎
│   ├── knowledge/                    # 知识库生成脚本
│   │   ├── generate.py
│   │   ├── convert_knowledge.py
│   │   └── requirements.txt
│   └── ...
│
├── database_specs/                   # 数据库通用能力
│   ├── dialect/                     # 方言语法（按数据库类型）
│   │   ├── DM.md                   # 达梦方言
│   │   ├── MySQL.md                 # MySQL 方言
│   │   └── Oracle.md                # Oracle 方言
│   └── sharding/                     # ShardingSphere 通用配置
│       └── ROUTING_RULES.md         # 分片路由规则
│
├── knowledge/                        # ACM 项目专属知识
│   ├── dm/                          # 达梦数据库（ACM 表结构）
│   │   ├── tables.json
│   │   ├── dm_ddl.sql
│   │   └── field_mapping.json
│   ├── mysql/                       # MySQL 数据库（ACM 表结构）
│   │   ├── tables.json
│   │   └── field_mapping.json
│   ├── oracle/                      # Oracle 数据库（ACM 表结构）
│   │   ├── tables.json
│   │   └── field_mapping.json
│   └── shared/                      # ACM 共享知识
│       ├── sql_generation_rules.md   # SQL 生成铁律
│       ├── kpi_spec_schema.json      # KPI 规范 Schema
│       ├── kpi_formulas.json        # KPI 计算公式
│       ├── evolved_domains.json      # 已进化域
│       └── sharding/                # ShardingSphere 经验
│           ├── KNOWN_BUGS.md        # 已知 BUG 及规避方案
│           └── TABLE_DISTRIBUTION.md # 表分片分布
│
└── templates/                        # HTML 模板
```

### 知识分类原则

| 内容 | 归属 | 说明 |
|------|------|------|
| 方言语法（TO_CHAR禁用等） | `database_specs/dialect/` | 通用能力，大模型预训练知识 |
| ShardingSphere 路由配置 | `database_specs/sharding/` | 通用中间件知识 |
| ACM 表结构、DDL | `knowledge/{db}/` | ACM 项目专属 |
| ShardingSphere BUG、表分布 | `knowledge/shared/sharding/` | ACM 系统经验总结 |

## 核心能力

- **NL→SQL 查询**：将自然语言问题转换为准确的 SQL 查询，验证后返回结果
- **驾驶舱生成**：基于 ECharts 生成可嵌入的 HTML 图表页面（单图表 + 多图表驾驶舱）
- **显式配置**：sqlMap 使用声明式 spec，不再依赖 key 名称推断图表类型
- **自动进化**：用户需求超出预定义时，从知识库动态生成 SQL + spec

## 快速开始

### SQL 加密（生成页面前必须）

```bash
# 加密单条 SQL
node scripts/encrypt_for_page.js "SELECT * FROM WSD_PLAN_PROJECT WHERE DEL=0" projectList

# 交互模式
node scripts/encrypt_for_page.js --interactive
```

### SQL 验证

`page.js` 生成时默认使用 **unified 模式**（DB 直连 + API 端到端同时验证），无需单独调用验证工具。

如需单独验证 SQL：

```bash
# MySQL 直连验证
node src/verify/index.js --sql "SELECT * FROM wsd_plan_task LIMIT 3" --source db

# HTTP API 验证
node src/verify/index.js --sql "SELECT * FROM wsd_plan_task LIMIT 3" --source api

# 同时使用两者
node src/verify/index.js --sql "SELECT * FROM wsd_plan_task LIMIT 3" --source unified
```

### 生成驾驶舱页面

```javascript
const { generateCockpitChart } = require('./src/generate/page.js');

const sqlMap = {
  'kpi_health': {
    sql: 'SELECT ...',
    type: 'kpi',
    spec: { kpiType: 'health_score', valueField: 'health_score', unit: '分' }
  },
  'riskHeatmap': {
    sql: 'SELECT PROBABILITY_LEVEL, AFTERMATH_LEVEL FROM wsd_risk_register ...',
    type: 'chart',
    spec: { chartType: 'scatter', xAxis: 'aftermath_level', yAxis: 'probability_level' }
  }
};

const html = await generateCockpitChart(sqlMap, { title: '项目驾驶舱', verify: true });
```

## 生成 SQL 前必读规范

| 数据库 | 规范文档 |
|--------|---------|
| 达梦 DM | `database_specs/dialect/DM.md` |
| MySQL | `database_specs/dialect/MySQL.md` |
| Oracle | `database_specs/dialect/Oracle.md` |
| ShardingSphere 路由 | `database_specs/sharding/ROUTING_RULES.md` |
| ShardingSphere BUG | `knowledge/shared/sharding/KNOWN_BUGS.md` |
| 分片表分布 | `knowledge/shared/sharding/TABLE_DISTRIBUTION.md` |

## 依赖

### Node.js 依赖

```bash
cd scripts && npm install
```

### Python 依赖（知识库生成）

```bash
cd scripts/knowledge && pip3 install -r requirements.txt
```

## 变更记录

详见 `CHANGES.md`
