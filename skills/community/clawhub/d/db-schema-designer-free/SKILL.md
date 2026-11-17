---
slug: db-schema-designer-free
name: db-schema-designer-free
version: 1.0.0
displayName: 数据库Schema设计器(免费版)
summary: 面向开发者的轻量级数据库Schema设计助手,支持SQLite软Schema与三层演进,快速落地灵活数据存储方案。
license: Proprietary
edition: free
description: '数据库Schema设计器(免费版)是一套面向独立开发者与小团队的轻量级数据库建模工具,聚焦"主干硬、尾巴软"的软Schema设计哲学,帮助用户在需求不确定阶段快速构建可演进的数据库结构。核心能力:

  - 提供原始层、软字段层、业务视图层三层建模方法论

  - 内置个人知识库、政策信息收集、财务报表收集等场景模板

  - 支持JSON软字段存储与键值对索引混合策略

  - 提供中文全文检索的基础实现思路(FTS5+LIKE回退)


  适用场景:

  - 个人知识库与碎片信息归档

  - 政策、新闻、报表等结构化信息收集

  - 表单问卷数据的多形...'
tags:
- 数据库
- 建模
- 知识库
- SQLite
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L2-标准级"
pricing_model: per_use
suggested_price: "19.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "设计,UI/UX,创意"
---
# 数据库Schema设计器(免费版)

一套可复用的"软Schema"设计方法:主干硬、尾巴软,三层演进。安装后,Agent可据此指导用户真正构建出灵活可演进的数据库结构,适配需求频繁变化的早期阶段。

## 概述

在数据建模实践中,最大的痛点不是"如何写SQL",而是"需求还没定型时怎么建表"。传统硬Schema要求字段提前确定,一旦业务变化就需要执行ALTER TABLE,迁移成本高、风险大。本Skill提供一套"软Schema"设计方法论,通过"原始层+软字段层+业务视图层"三层结构,让数据库能够在保持主干稳定的同时,灵活承载多变的字段需求。

免费版聚焦核心建模能力,适合个人开发者与小型项目快速上手。

## 核心能力

### 三层模型

| 层级 | 作用 | 典型做法 |
|---|---|----|
| **原始层** | 不丢信息、可追溯 | 整条记录原样存,加哈希去重、来源标记、版本号 |
| **软字段层** | 灵活查询 | JSON存结构化结果;键值对表按key查询、聚合 |
| **业务视图层** | 高频查询、报表 | 物化表/视图,按需建索引 |

**输入**: 用户提供三层模型所需的指令和必要参数。
**处理**: 解析三层模型的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回三层模型的响应数据,包含状态码、结果和日志。

### 三条核心心法

1. **主干硬、尾巴软** — 固定列只放:谁、何时、从哪来、类型;其余进JSON/键值对。
2. **先全量保留,再按需提键** — 原始数据完整落库;需要查询统计时再写入键值对或业务表。
3. **分层演进** — 原始层 → 软字段层 → 业务视图层;缺什么再补什么,避免过度设计。

**输入**: 用户提供三条核心心法所需的指令和必要参数。
**处理**: 解析三条核心心法的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回三条核心心法的响应数据,包含状态码、结果和日志。

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：面向开发者的轻量、级数据库、Schema、设计助手、SQLite、与三层演进、快速落地灵活数据、存储方案、数据库、设计器、免费版、是一套面向独立开、发者与小团队的轻、量级数据库建模工、主干硬、尾巴软、设计哲学、帮助用户在需求不、确定阶段快速构建、可演进的数据库结、核心能力、提供原始层、软字段层、业务视图层三层建、模方法论、内置个人知识库、政策信息收集、财务报表收集等场、景模板、JSON、软字段存储与键值、对索引混合策略、提供中文全文检索、的基础实现思路、FTS、LIKE等。

## 使用场景

### 场景1:个人知识库搭建

用户意图: "我想做一个个人知识库,收藏微信文章、网页片段、读书笔记。"

推荐主干: `id, created_at, source, content_type, raw_content`
推荐软字段: `title, tags, url, project, deadline`

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 数据库Schema设计器(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```sql
CREATE TABLE knowledge_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  source TEXT NOT NULL,
  content_type TEXT NOT NULL,
  raw_content TEXT NOT NULL,
  extra JSON
);
CREATE INDEX idx_knowledge_source ON knowledge_items(source);
CREATE INDEX idx_knowledge_created ON knowledge_items(created_at DESC);
```

### 场景2:政策信息收集

用户意图: "我要收集政府补贴政策,按行业和金额筛选。"

推荐主干: `id, created_at, source, source_type`
推荐软字段: `title, release_date, issuing_org, policy_type, url, policy_no, industry, subsidy_amount`

### 场景3:财务报表归档

用户意图: "收集上市公司财报数据,要能按公司和报告期查询。"

推荐主干: `id, created_at, source, source_type`
推荐软字段: `company, report_type, report_date, revenue, net_income, total_assets, roa, roe`

> 金额字段统一存"元",避免单位混乱;`report_type`可作为业务视图的category字段。

## 不适用场景

以下场景数据库Schema设计器(免费版)不适合处理：

- 数据库架构设计决策
- NoSQL选型
- 数据仓库ETL设计

## 触发条件

需要数据库操作、SQL查询、数据存储管理时使用。不适用于非本工具能力范围的需求。

## 快速开始

### Step 1:Discovery需求澄清

Agent主动向用户确认以下信息,并记录到对话中:

| 问题 | 用途 |
|---:|---:|
| 数据主要来自哪里?(微信/网页/API/手动输入) | 定`source_type`枚举 |
| 每条记录"永远会有"的信息有哪些?(时间、来源、类型) | 定主干字段 |
| 哪些信息"可能经常变、不同来源不一样"? | 确认用JSON/键值对 |
| 是否有按编号/文号等唯一标识查询的需求? | 决定是否在视图中加入对应字段 |
| 需要全文搜索吗? | 决定是否建FTS |
| 内容语言?(中文为主/英文为主/混合) | 决定FTS策略 |
| 内容形态?(纯文本/PDF/Excel/网页/混合) | 决定是否需要提取器 |
| 预期数据量?(百/千/万/十万级) | 决定LIKE回退是否可用 |

### Step 2:选择场景模板

根据用户描述,选择最接近的场景并适配。参考"使用场景"章节的模板表。

### Step 3:生成并落地Schema

1. 复制下方"配置示例"中的建表模板到用户项目。
2. 按Discovery结果做最小修改:
   - 调整`source_type`的CHECK枚举;
   - 如需FTS,取消`messages_fts`相关注释;
   - 业务视图层按需新增视图。
3. 在用户项目中创建`data/`目录,指定db路径(如`data/flexible.db`)。

### Step 4:验证清单

- [ ] 建表成功,无报错
- [ ] 能归档一条测试数据
- [ ] 能按分类/字段查询
- [ ] 全文搜索(若启用)可用;中文检索用3-5个短语实测
- [ ] 若预期>5000条,已评估LIKE性能或选用替代方案

## 示例

### 通用建表模板

```sql
-- 原始层:全量保留
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT,
  source TEXT NOT NULL,
  source_type TEXT NOT NULL CHECK(source_type IN ('web','api','manual','file','chat')),
  content_type TEXT,
  raw_content TEXT NOT NULL,
  content_hash TEXT,
  extra JSON,
  deleted INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_items_source ON items(source);
CREATE INDEX IF NOT EXISTS idx_items_created ON items(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_items_hash ON items(content_hash);
# ...
-- 软字段层:键值对索引(高频查询字段)
CREATE TABLE IF NOT EXISTS item_kv (
  item_id INTEGER NOT NULL,
  key TEXT NOT NULL,
  value TEXT,
  PRIMARY KEY (item_id, key),
  FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_kv_key_value ON item_kv(key, value);
# ...
-- 业务视图层:按需物化(示例:知识库视图)
CREATE VIEW IF NOT EXISTS v_knowledge AS
SELECT i.id, i.created_at, i.source,
       kv_title.value AS title,
       kv_tags.value AS tags,
       kv_url.value AS url,
       kv_project.value AS project
FROM items i
LEFT JOIN item_kv kv_title ON i.id = kv_title.item_id AND kv_title.key = 'title'
LEFT JOIN item_kv kv_tags  ON i.id = kv_tags.item_id  AND kv_tags.key  = 'tags'
LEFT JOIN item_kv kv_url   ON i.id = kv_url.item_id   AND kv_url.key   = 'url'
LEFT JOIN item_kv kv_project ON i.id = kv_project.item_id AND kv_project.key = 'project'
WHERE i.deleted = 0;
# ...
-- 可选:全文检索(中文需配合LIKE回退)
-- CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
--   content, content='items', content_rowid='id'
-- );
```

### 归档一条数据

```bash
sqlite3 data/flexible.db "INSERT INTO items (source, source_type, content_type, raw_content, extra) VALUES ('manual', 'manual', 'text', '测试第一条记录', '{\"title\":\"示例\",\"tags\":\"工作\"}');"
```

### 查询数据

```bash
# 列出最近10条
sqlite3 data/flexible.db "SELECT id, created_at, source, content_type FROM items WHERE deleted=0 ORDER BY created_at DESC LIMIT 10;"
# ...
# 按字段查询
sqlite3 data/flexible.db "SELECT i.id, i.raw_content FROM items i JOIN item_kv kv ON i.id=kv.item_id WHERE kv.key='tags' AND kv.value LIKE '%工作%';"
# ...
# 统计
sqlite3 data/flexible.db "SELECT source, COUNT(*) FROM items WHERE deleted=0 GROUP BY source;"
```

## 最佳实践

### 中文全文检索策略

| 内容语言 | 推荐方案 | 说明 |
|:---:|:---:|:---:|
| 英文为主 | FTS5 (unicode61) | 默认即可 |
| 中文为主 | FTS + LIKE回退 | 长短语易漏检,需实现`recall()`函数 |
| 中文为主(数据量<5000) | 同上 + 短词拆分 | 如"煤炭期货价格"拆为"煤炭""期货""价格"分别查,取并集 |
| 中文为主(数据量>5000) | 考虑Meilisearch或jieba+FTS | SQLite FTS中文能力有限 |

**实现要点**: 查询层实现`recall(keyword)`:先FTS,无结果则LIKE;中文可加短词拆分。`LIKE '%x%'`无法用索引,数据量大时需评估性能。

### 命名规范

- 软字段key统一使用snake_case
- 多个来源的字段加命名空间前缀(如`wx_title`、`web_title`)
- 主干字段保持稳定,避免频繁ALTER
- JSON字段避免深层嵌套(建议≤3层)

### 反模式清单(必须避免)

- 一上来穷举所有可能字段 → 改表成本高
- 软字段key随心所欲 → 约定snake_case、命名空间
- 所有查询都扫JSON → 高频条件应提键值对并建索引
- 没有原始层 → 无法回溯、补字段
- 中文全文检索只依赖FTS5 → unicode61对中文不友好,需FTS+LIKE回退
- `LIKE '%x%'`用于万级数据 → 全表扫描,应评估或改用外部搜索引擎
- PDF只存路径不提取正文 → 无法全文检索,需在归档时提取并写入raw_content

## 常见问题

### Q1: 什么时候该用软Schema,什么时候该用硬Schema?

A: 需求稳定、字段明确、查询模式固定时用硬Schema;需求频繁变化、字段来源多样、查询模式未定型时用软Schema。两者不冲突,可混合使用:主干用硬Schema,扩展字段用软字段。

### Q2: JSON字段查询性能差怎么办?

A: 把高频查询字段从JSON提取到`item_kv`键值对表并建索引;低频字段保留在JSON中按需查询。数据量超过5000条时务必评估LIKE性能。

### Q3: 中文FTS检索召回率低怎么办?

A: 实现短词拆分策略,把长短语拆成2-4字短词分别查询取并集;数据量大时考虑接入jieba分词或迁移到Meilisearch。

### Q4: 如何处理重复数据?

A: 在归档时计算`content_hash`(如MD5或SHA1),写入`content_hash`字段并建唯一索引,归档前先查询hash是否存在。

### Q5: 软删除和硬删除怎么选?

A: 推荐`deleted`标记字段做软删除,定期清理可批量UPDATE;硬删除仅在数据合规要求物理删除时使用,需同步清理`item_kv`等关联表。

## 已知限制

本免费体验版限制以下高级功能:
- 不支持批量导入(单次处理≤10条)
- 不支持自定义抽取器模板(仅提供基础字段提取)
- 不支持多数据库适配(仅支持SQLite,`PostgreSQL`/MySQL需专业版)
- 不支持性能诊断与索引优化建议
- 不支持团队协作与Schema版本管理

解锁全部功能请使用专业版: db-schema-designer-pro
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+(可选,用于运行辅助脚本)
- **SQLite**: 3.35+(支持JSON1扩展)

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| sqlite3 | 数据库引擎 | 必需 | 系统自带或`pip install pysqlite3` |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |
| pypdf | Python库 | 可选 | `pip install pypdf`(PDF正文提取) |

### API Key 配置
- 本skill基于Markdown指令规范,无需额外API Key
- 如需LLM抽取器,使用Agent平台内置LLM即可

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
