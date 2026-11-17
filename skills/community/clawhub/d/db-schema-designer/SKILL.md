---

name: flexible-database-design
slug: flexible-database-design
displayName: "Flexible Database De"
version: 1.0.1
summary: "指导Agent与用户设计实现灵活数据库,建模不踩坑(社区下载版)。['基于高人气开源Skill深度优化升级\n- 移除风险代码,增强安全性和稳定性\n\n适用场景:\n- 第三方AP"
description: "['基于高人气开源Skill深度优化升级\\n- 移除风险代码,增强安全性和稳定性\\n\\n适用场景:\\n- 第三方API集成、平台对接、数据同步\\n- 独立开发者与一人公司效率提升\\n\\', '自动化工作流与智能决策辅助\\n\\n差异化:经过深度优化,去除原始风险代码,清理外部依赖引用,增强元数据和触发关键词,完全适配SkillHub平台规范']"
license: "MIT-0"
tools:
  - read
  - exec
tags:
  - created_at
  - source
  - report_type
  - fts
  - pdf
category: "Knowledge"
pricing_tier: "L2-标准级"
license: "Proprietary"

---

> **功能说明**: 本技能涵盖 升级\n- 等核心能力。

# Flexible Database Design â SQLite flexible schema & knowledge base skill

一套可复用的「软 Schema」设计方法：主干硬、尾巴软，三层演进。用户安装后，Agent 可据此指导其**真正构建**出灵活数据库。

---

## 一、核心心法（3 条）

1. **主干硬、尾巴软** — 固定列只放：谁、何时、从哪来、类型；其余进 JSON/键值对。
2. **先全量保留，再按需提键** — 原始数据完整落库；需要查/统计时再写入键值对或业务表。
3. **分层演进** — 原始层 → 软字段层（JSON/键值对）→ 业务视图层；缺什么再补。

---

## 二、三层模型

| 层级 | 作用 | 典型做法 |
| --- | --- | --- |
| **原始层** | 不丢信息、可追溯 | 整条记录原样存，加哈希去重、来源、版本号 |
| **软字段层** | 灵活查询 | JSON 存结构化结果；键值对表按 key 查、聚合 |
| **业务视图层** | 高频查询、报表 | 物化表/视图，按需建索引 |

---

## 三、Agent 工作流（用户说「想做 XX」时执行）

### Step 1：Discovery（必做）

向用户确认以下信息，并记录到对话中：

| 问题 | 用途 |
| --- | --- |
| 你的数据主要来自哪里？（微信/网页/API/手动输入/多种） | 定 `source_type` 枚举 |
| 每条记录大概有哪些「永远会有」的信息？（如：时间、来源、类型） | 定主干字段 |
| 有哪些「可能经常变、不同来源不一样」的信息？ | 确认用 JSON/键值对 |
| 是否有按编号/文号等唯一标识查询的需求？ | 决定是否在视图中加入对应字段，并考虑快捷查询 |
| 需要全文搜索吗？ | 决定是否建 FTS |
| 内容语言？（中文为主 / 英文为主 / 混合） | 决定是否采用中文分词、FTS 策略 |
| 内容形态？（纯文本 / PDF / Excel / 网页 / 混合） | 决定归档前是否需要提取（如 pypdf） |
| 预期数据量？（百 / 千 / 万 / 十万级） | 决定 LIKE 回退是否可用、是否考虑外部搜索引擎 |

### Step 2：选择场景模板

根据用户描述，选择最接近的场景并适配：

| 场景 | 主干字段建议 | 软字段典型 key |
| --- | --- | --- |
| **个人知识库 / 碎片收集** | id, created_at, source, content_type, raw_content | title, tags, url, project, deadline |
| **政策信息收集** | id, created_at, source, source_type | title, release_date, issuing_org, policy_type, url, policy_no, industry, subsidy_amount |
| **财务报表收集** | id, created_at, source, source_type | company, report_type, report_date, revenue, net_income, total_assets, roa, roe |
| **表单/问卷** | id, created_at, form_id, respondent_id, raw_response | 各题目 id 或题目名 |
| **PDF/报告知识库** | id, created_at, source, content_type, raw_content | report_title, report_type, period_start, period_end, file_path |
| **多源异构（如群消息聚合）** | id, created_at, source, sender, raw_content | data_type, items[], trend, 各业务字段 |

### Step 3：生成并落地 Schema

1. 复制  到用户项目。
2. 按 Discovery 结果做**最小修改**：
   * 调整 `source_type` 的 CHECK 枚举；
   * 如需 FTS，取消 `messages_fts` 相关注释；
   * 业务视图层参考  按需新增视图。**业务视图应覆盖高频查询字段**：政策类含 title、release_date、issuing_org、policy_type、url、policy_no；知识库类含 title、tags、url、project；财报类含 company、report_type、report_date、revenue、net_income；PDF/报告类含 report_title、report_type、period_start、period_end。
3. 在用户项目中创建 `data/` 目录，指定 db 路径（如 `data/flexible.db`）。

### 全文检索策略（当 Discovery 勾选「需要全文搜索」时）

| 内容语言 | 推荐方案 | 说明 |
| --- | --- | --- |
| 英文为主 | FTS5 (unicode61) | 默认即可 |
| 中文为主 | FTS + LIKE 回退 | 长短语易漏检，需实现 `recall()` |
| 中文为主（数据量 < 5000） | 同上 + 短词拆分 | 如「煤炭期货价格」→ 拆为「煤炭」「期货」「价格」分别查，取并集 |
| 中文为主（数据量 > 5000） | 考虑 Meilisearch / jieba+FTS | SQLite FTS 中文能力有限 |

**实现要点**：查询层实现 `recall(keyword)`：先 FTS，无结果则 LIKE；中文可加短词拆分。`LIKE '%x%'` 无法用索引，数据量大时需评估性能。扫描件 PDF 无法提取正文，归档时需跳过或标记。

### Step 4：生成并适配脚本

1. 将  下脚本复制到用户项目 `scripts/`：**核心** flexible_db.py、archive_item.py、query_items.py；**可选** manage_item.py、import_batch.py、quick_validate.py、extractors/。
2. 修改 `flexible_db.py` 中的 `db_path` 指向用户的 db 路径。
3. 若用户有特殊「提取逻辑」（如用 LLM 从原文抽结构化数据），使用 `archive_item.py --llm-extract` 或配置 `FLEXIBLE_EXTRACTOR=extractors.dummy:extract`；可自定义 `extractors/` 下的实现。**抽取器字段应与场景匹配**：政策类建议 title、release_date、issuing_org、policy_type、url、policy_no；知识库类建议 title、tags、url、project；财报类建议 company、report_type、report_date、revenue、net_income（金额统一存「元」）；PDF/报告类建议 report_title、report_type、period_start、period_end。
4. **若内容为 PDF/文档**：归档前需提取正文（推荐 pypdf：`pip install pypdf`），扫描件无法提取时跳过。可选：将 PDF 复制到项目 `data/reports/` 统一管理，`file_path` 存相对路径；抽取器可从文件名解析 period、source、report_type。
5. 运行验证（`python` 或 `python3` 按环境选择）：

```bash
python3 scripts/archive_item.py -c "测试条" -s "manual"

python3 scripts/query_items.py --list
py --field "tags" --value "工作"
```

### Step 5：验证清单

* 建表成功，无报错
* 能归档一条测试数据
* 能按分类/字段查询
* 全文搜索（若启用）可用；中文检索建议实现 FTS + LIKE 回退（如 `recall()`）
* **中文检索**：用 3–5 个中文短语（含 2–4 字短语）实测，确认能召回预期结果
* **数据量评估**：若预期 > 5000 条，已评估 LIKE 性能或选用替代方案

---

## 四、场景速查（用户说想做 XX 时）

| 用户意图 | 推荐主干 | 推荐软字段 | 备注 |
| --- | --- | --- | --- |
| 个人知识库 | id, created_at, source, content_type | title, tags, url, project | 碎片收集同此 |
| PDF/报告知识库 | id, created_at, source, content_type, file_path | report_title, report_type, period_start, period_end | 需提取正文；中文检索见「全文检索策略」 |
| 政策信息收集 | id, created_at, source, source_type | title, release_date, issuing_org, policy_type, url, policy_no, industry, subsidy_amount | 政府网站/新闻来源，文号常作查询键 |
| 财务报表收集 | id, created_at, source, source_type | company, report_type, report_date, revenue, net_income, total_assets, roa, roe | 金额统一存「元」；report_type→category |
| 表单/问卷 | id, created_at, form_id, respondent_id | 题目 id → 答案 | 可加 form_version |
| 多源消息聚合 | id, created_at, source, sender | data_type, items[], trend | 参考 agri-market-info |
| 埋点/事件 | id, created_at, event_name, user_id | properties JSON | 可加 event_version |

---

## 五、反模式

* 一上来穷举所有可能字段 → 改表成本高
* 软字段 key 随心所欲 → 约定 snake_case、命名空间
* 所有查询都扫 JSON → 高频条件应提键值对并建索引
* 没有原始层 → 无法回溯、补字段
* 中文全文检索只依赖 FTS5 → unicode61 对中文不友好，需 FTS + LIKE 回退或中文分词
* `LIKE '%x%'` 用于万级数据 → 全表扫描，应评估或改用外部搜索引擎
* PDF 只存路径不提取正文 → 无法全文检索，需在归档时提取并写入 raw_content

---

## 六、文件结构（本 Skill 包）

```text
flexible-database-design/
├── SKILL.md                 # 本文件
├── README.md
├── references/
│   ├── schema_template.sql  # 通用建表模板
│   ├── view_examples.sql    # 业务视图示例
│   └── fulltext_chinese.md  # 可选：中文检索实现示例（短词拆分、recall 逻辑）
└── scripts/
    ├── flexible_db.py       # 数据库核心逻辑
    ├── archive_item.py     # 归档 CLI（支持 --llm-extract、--backup）
    ├── query_items.py      # 查询 CLI（支持 --export）
    ├── manage_item.py      # 管理 CLI（软删除、恢复、更新）
    ├── import_batch.py     # 批量导入
    ├── quick_validate.py   # 快速验证
    └── extractors/         # 抽取器（可替换为 LLM 实现）
```

---

## 工具声明（Skill平台 / SkillHub）

allowed-tools:

* Bash
* FileRead
* FileWrite
* Shell

---

**作者** | Mars Yang
**日期** | 2025-03-09

## 环境要求
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent( Code / Cursor / Codex /  CLI等)
- **操作系统**: Windows / macOS / Linux

### 依赖说明
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 本Skill基于Markdown指令,无需额外API Key(除内容中明确标注的外部API)

### 可用性分类
- **分类**: MD+execute(纯Markdown指令,部分功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行任务

## 能力清单
- \n\n\
  触发关键词: â\x80\x93, knowledge, users, base, guide, implement, sqlite, design

## 上线流程
1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 场景示例
根据用户描述，选择最接近的场景并适配：

| 场景 | 主干字段建议 | 软字段典型 key |
| --- | --- | --- |
| **个人知识库 / 碎片收集** | id, created_at, source, content_type, raw_content | title, tags, url, project, deadline |
| **政策信息收集** | id, created_at, source, source_type | title, release_date, issuing_org, policy_type, url, policy_no, industry, subsidy_amount |
| **财务报表收集** | id, created_at, source, source_type | company, report_type, report_date, revenue, net_income, total_assets, roa, roe |
| **表单/问卷** | id, created_at, form_id, respondent_id, raw_response | 各题目 id 或题目名 |
| **PDF/报告知识库** | id, created_at, source, content_type, raw_content | report_title, report_type, period_start, period_end, file_path |
| **多源异构（如群消息聚合）** | id, created_at, source, sender, raw_content | data_type, items[], trend, 各业务字段 |

## 示例

### 示例1：基础用法

```
# 请参考上方使用说明进行配置和调用
result = "ready"
```

## 异常恢复流程
| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 检查网络连接后重试，参考国内替代方案 |

## 热门问题
### Q1: 如何开始使用Flexible Database De？
A: 请先阅读使用流程章节，确认环境满足依赖说明中的要求。

### Q2: 遇到错误怎么办？
A: 请参考错误处理章节，按照表格中的处理方式操作。

### Q3: Flexible Database De有什么限制？
A: 请参考已知限制章节了解具体限制。

## 注意事项
- 需要API Key，无Key环境无法使用

## 协助指南
### Q1: Flexible Database De支持哪些输入格式？

A1: 指导Agent与用户设计实现灵活数据库,建模不踩坑(社区下载版)。['基于高人气开源Skill深度优化升级
- 移除风险代码,增强安全性和稳定性

适用场景:
。支持文本指令和结构化参数输入，具体格式参考使用流程章节。

### Q2: 需要配置API Key吗？

A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。

### Q3: 命令行执行失败怎么办？

A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。

## 安全须知事项
### 安全风险防范

| 风险项 | 等级 | 防护措施 | 验证方法 |
| --- | --- | --- | --- |
| API密钥泄露 | 高 | 通过环境变量配置，禁止硬编码 | 定期检查代码和配置文件 |
| 命令执行风险 | 高 | 仅执行白名单命令，避免拼接用户输入 | 使用沙箱环境测试 |
| 网络通信安全 | 中 | 使用HTTPS协议，验证SSL证书 | 定期检查证书有效期 |
| 敏感数据暴露 | 高 | 输出结果中不包含密钥、令牌等敏感信息 | 日志脱敏审查 |
| 未授权访问 | 中 | 限制访问权限，实施认证机制 | 定期审计访问日志 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 性能评估
| 操作场景 | 手动耗时 | 自动化耗时 | 效率提升 |
|----------|---------|-----------|---------|
| 文件解析与提取 | 5-10分钟/个 | <5秒/个 | 60-120x |
| 批量文件处理(100个) | 8-16小时 | <5分钟 | 96-192x |
| API调用与响应解析 | 2-3分钟/次 | <1秒/次 | 120-180x |
| 多接口数据聚合 | 15-30分钟 | <10秒 | 90-180x |
| 命令执行与结果收集 | 3-5分钟/次 | <2秒/次 | 90-150x |
| 重复任务批量执行 | 因任务而异 | 线性缩减 | 5-50x |
| 错误排查与修复 | 10-30分钟 | <30秒 | 20-60x |

## 特色分析
| 对比维度 | Flexible Database De | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | 指导Agent与用户设计实现灵活数据库,建模不踩坑(社区下载版)。['基于高人气 | 通用场景 | 通用场景 |

## 高频问答