# 🗄️ File to Database

![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.1.0-green)
![Platform](https://img.shields.io/badge/platform-OpenClaw%20%7C%20Claude%20Code%20%7C%20Cursor%20%7C%20Codex%20%7C%20Gemini%20CLI-purple)
![ClawHub](https://img.shields.io/badge/ClawHub-draft-yellow)

**[English](README.md)** | **中文**

把原始数据文件（CSV / Excel / JSON / JSONL / TSV）变成一套经过验证的数据库——之后还能继续用自然语言操作它：查询、插入、更新、删除，带安全门槛、审计日志，每次变更后自动交付可视化包。

**7 份参考文档**固化完整工程循环。**6 种文件格式**支持。**0 依赖**（纯 Python 标准库；xlsx 可选装 openpyxl）。

**解决的痛点**："把文件发给 Cursor 让它建库"只能用一次——每个新项目都要重新交代设计规则，Agent 每次猜的外键和索引都不一样，而且 DDL 生成完就不管了。File to Database 三个问题全解：设计方法论固化在 `references/methodology.md`（换文件即换风格），每次生成的 schema 严格遵循它，运行模式让 Agent 在建库之后继续当数据库的自然语言操作员。

## 目录

<details>
<summary>点击展开</summary>

- [工作原理](#工作原理)
- [分阶段循环](#分阶段循环)
- [运行模式（建库之后）](#运行模式建库之后)
- [工程化加固](#工程化加固)
- [非数据文件（意图分流）](#非数据文件意图分流)
- [可插拔方法论](#可插拔方法论)
- [安装](#安装)
- [快速开始](#快速开始)
- [全链路实测](#全链路实测)
- [文件结构](#文件结构)
- [兼容性](#兼容性)
- [许可](#许可)

</details>

## 工作原理

```
数据文件 ──▶ infer_schema.py ──▶ 列画像
                                      │
           detect_relations.py ◀──────┘
                    │
                    ▼
          methodology.md（你的规则）
                    │
                    ▼
      schema.sql + ERD + seed + 迁移脚本
                    │
                    ▼
      约束反向测试 + EXPLAIN 验证
```

1. **画像** — `infer_schema.py` 扫描每个文件：类型推断（int/float/bool/date/uuid/text，90% 投票制）、空值率、基数、唯一性、最长值、样本值。
2. **关系发现** — `detect_relations.py` 找主键候选（完全唯一列）和外键候选（名称匹配 + 值集包含），每个都带置信度和裁决：`adopt` / `ask_user` / `ignore`。
3. **建模** — Agent 按你的方法论执行：默认 3NF，只为点名查询反范式化，约束落 DDL 不留应用层。
4. **交付** — `schema.sql`、Mermaid ERD、`seed.py`、可回滚迁移。
5. **验证** — 约束反向测试（插入应被拒绝的行，断言报错）+ `EXPLAIN` 关键查询确认索引命中。

## 运行模式（建库之后）

Skill 不止于 DDL。库建好之后，Agent 成为它的**自然语言操作员**：意图识别 → SQL 生成 → 安全执行 → 人话汇报。

```
"在订单表里加一条，用户是 Alice，金额 59"
    → 参数化 INSERT → 执行
    → "已添加 1 条订单（Alice，¥59）。"

"删掉所有过期的订阅"
    → 先 SELECT 预览受影响行数（12 行）
    → 超过 5 行门槛，等用户确认后才 DELETE
    → "已删除 12 条过期订阅，备份在 /tmp/backup_xxx.csv"
```

完整规则见 `references/operations.md`：触发条件（实体+操作词、数据疑问、变更动词、隐式指代）、SQL 生成规则、安全门槛（UPDATE/DELETE 必须预览行数；超过 5 行或无 WHERE 必须确认）、报错翻译（unique 冲突 → "这条记录已经存在"）、汇报模板（先结论后数据再提示下一步）。

## 分阶段循环

每个阶段都留下可检查的产物，正确性靠测试和执行计划，不靠人眼读生成的 SQL：

| 阶段 | 产物 | 完成标准 |
|---|---|---|
| 1. 扫描 | `profiles.json` | 每个文件都有画像，歧义列已标记 |
| 2. 关系 | 带证据的外键清单 | 低置信候选必须问用户，绝不静默选择 |
| 3. 建模 | 决策记录 | 开放问题列出来问用户 |
| 4. 交付 | DDL + ERD + seed | 每个索引注明服务的查询 |
| 5. 验证 | 测试输出 | 约束测试全过，EXPLAIN 命中计划索引 |

## 可插拔方法论

`references/methodology.md` 是本 Skill 的灵魂。内置版本固化了 Cursor 社区的分阶段循环：约束进数据库、查询驱动索引、expand-and-contract 迁移，以及固定的两问询点模式（画像后 + 建模前——带证据的选择题，不出开放题）。想强制执行你自己的规范——比如"一律用代理键 + 软删除"——改那一个文件即可，Skill 启动时读取并逐条执行，不用改代码。

## 工程化加固

`references/engineering.md` 补齐真实数据工程师的流程，按个人场景裁剪：

- **迁移账本**——带 checksum 的 `.applied.json`；乱序或被改过的历史迁移立即报错停下；交付前实际演练一次回滚
- **数据质量门**——seed 后自动断言（行数、主键空值、外键悬空、值域漂移）；失败停止并列出问题行样本
- **增量导入**——文件更新了绝不重建：画像 diff → 结构变化走新迁移 / 新行 UPSERT（主键冲突默认跳到 `skipped.csv`）
- **安全**——凭证只走环境变量（不进代码/报告/聊天）、SQLite 0600 / PG 最小权限 / Supabase RLS、PII 列标记 + 快照掩码、每次写操作记 `audit.log` 随交付包发送
- **诚实边界**——生产部署、监控、压测、容量规划：生成配置和脚本，但不假装执行

## 非数据文件（意图分流）

发来一本 PDF 教材、PPTX、图片？Skill 既不强行建库也不拒绝：`references/intake.md` 按用户意图分流——抽取成结构化 JSONL（带页码可回溯 + 10 条抽样人工核对）→ 走标准管道；或仅阅读总结不建库；或"你是不是发错文件了？"文件类型决定能力边界，用户意图决定工作流。

## 全链路实测

用三种格式自编数据（CSV / JSONL）全盘测试，故意埋入脏数据（悬空外键）：

- 类型推断全列正确；FK 检测器抓到悬空引用并降置信度 → 触发问询
- 质量门：脏行被外键拦截，隔离到 `skipped.csv`
- 约束反向测试：重复主键 / 非法数量 / 删除被引用商品——全部正确拒绝
- 运行模式：NL 查询、UPDATE 预览 → 行数门槛 → 执行 → 审计日志、报错翻译人话
- 测试中抓到 2 个真实 bug（SQLite 每连接 FK pragma；seed 事务边界）并修复——已固化进 `references/engineering.md` §4.5

## 安装

```bash
# ClawHub
clawhub install file-to-database-skill

# 或从源码
git clone https://github.com/Thomaszhou22/file-to-database-skill.git
cp -r file-to-database-skill ~/.openclaw/skills/
```

需要 Python 3.8+（纯标准库）。`.xlsx` 支持可选装 `openpyxl`。

## 快速开始

```bash
# 1. 给文件画像
python3 scripts/infer_schema.py --input ./data/ --out profiles.json

# 2. 发现关系
python3 scripts/detect_relations.py --profiles profiles.json --out relations.json

# 3. 对 Agent 说："按照 skill 方法论把 ./data 建成数据库"
```

之后 Agent（OpenClaw / Claude Code / Cursor）接手：建模、DDL、ERD、seed、验证。

## 文件结构

```
file-to-database-skill/
├── SKILL.md                        # 入口：分阶段循环 + 运行模式 + 工程加固
├── references/
│   ├── methodology.md              # ⭐ 可插拔设计方法论 + 问询点模式
│   ├── operations.md               # ⭐ 运行模式：NL 意图 → SQL → 安全执行 → 人话汇报 + 可视化交付
│   ├── engineering.md              # 迁移账本、质量门、增量导入、权限安全
│   ├── intake.md                   # 非数据文件（PDF/PPTX 等）：先意图分流再动
│   ├── output-format.md            # 交付物布局 & 报告模板
│   └── other-engines.md            # MySQL / SQLite / MongoDB / Supabase 差异
└── scripts/
    ├── infer_schema.py             # 列级画像（CSV/TSV/JSON/JSONL/xlsx）
    └── detect_relations.py         # 主外键候选检测（带置信度三档裁决）
```

## 兼容性

| 环境 | 状态 |
|---|---|
| OpenClaw | ✅ 主要目标 |
| Claude Code | ✅ 放入 `~/.claude/skills/` |
| Cursor | ✅ 作为 Project Rule + 终端跑脚本 |
| Codex CLI | ✅ 放入 `~/.codex/skills/` 或通过 AGENTS.md 引用 |
| Gemini CLI | ✅ 在 GEMINI.md 中引用 SKILL.md；脚本可独立运行 |
| 任意 LLM Agent | ✅ 脚本可独立运行（任何能读文件、跑 Python 的 Agent） |

## 许可

MIT
