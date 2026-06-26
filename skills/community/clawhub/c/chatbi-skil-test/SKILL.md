---
name: chatbi-agent-skill
description: |
  通过命令行调用 ChatBI 问数 Agent 流式接口，对企业数据表进行自然语言驱动的数据查询分析。
  本工具支持：发起自然语言问数、实时跟踪 Agent 执行流程、提取意图理解/选表结果/SQL/最终回答。
  当用户需要查询数据库、分析数据、用自然语言问数，或提到"ChatBI"、"问数"、"数据查询"、"SQL分析"时使用本 Skill。
compatibility: |
  需要能访问 ChatBI Agent 服务端点；
  需要安装 requirements.txt 中的依赖；
  数据表需已在 ChatBI 平台注册。
domain: DataAnalysis
---
metadata:
  author: ChatBI Skills
  version: "1.0.0"
---

# ChatBI 问数 Agent Skill

## 概述

`scripts/chatbi_cli.py` 帮助用户完成 **自然语言问数 → 意图理解 → 智能选表 → SQL 生成执行 → 获取结果** 的完整流程。

### 核心能力

本 Skill 调用 ChatBI Agent 流式接口，从丰富的 Agent 输出中只提取关键信息：

1. **意图理解**：`intent_tool` → `understanding_thinking`（Agent 对用户问题的理解）
2. **选表结果**：`table_select_tool` → `table_name` + `table_selected_reason`（选择了哪些表及原因）
3. **SQL 执行**：`sql_executed`（生成的 SQL）、`execution_plan`（执行计划）、`data_preview_info`（数据预览）
4. **最终回答**：`is_final_answer=true` 且 `type=answer` 的内容

---

## 安装

```bash
pip install -r scripts/requirements.txt
```

---

## 快速开始

```bash
# 基本问数
python3 scripts/chatbi_cli.py -q "查询乳制品的销售情况"

# 指定输出模式
python3 scripts/chatbi_cli.py -q "各品类月度销售趋势" --output detail

# 仅输出 SQL
python3 scripts/chatbi_cli.py -q "查询销量 Top10 的商品" --output sql-only
```

---

## 输出模式

- **summary**（默认）：意图理解 + 选表结果 + SQL + 最终回答
- **detail**：完整的 Agent 执行过程
- **sql-only**：仅输出生成的 SQL
- **raw**：输出被过滤命中的事件 JSON 及未匹配事件标注（调试用）

---

## ⚠️ 调用规范（必读）

> **必须使用 `yieldMs=200` 参数**，否则无法实现流式输出！

本 Skill 的 CLI 脚本执行耗时约 30-50 秒（Agent 意图理解 → 选表 → SQL 生成执行 → 回答）。
CLI 内部每个阶段完成后会立即 `flush` 输出，配合 `yieldMs=200` 可实现渐进式展示。

### 正确调用方式

```
exec(command="python3 scripts/chatbi_cli.py -q '查询乳制品的销售情况' --output summary", yieldMs=200)
```

### 错误调用方式

```
# ❌ 缺少 yieldMs，会等进程跑完才一次性返回所有结果
exec(command="python3 scripts/chatbi_cli.py -q '查询乳制品的销售情况'")
```

### 参数说明

| 参数 | 值 | 说明 |
|------|-----|------|
| `yieldMs` | `200` | 每 200ms 把已产生的 stdout 分批推送给用户，实现渐进式展示 |
| `--output` | `summary` | 默认模式，只输出关键信息（意图/选表/SQL/回答） |
| `--output` | `detail` | 额外输出执行计划和数据预览详情 |
| `--output` | `sql-only` | 仅输出 SQL，适合管道使用 |

---

## 项目结构

```
├── SKILL.md              # 本文档
├── scripts/
│   ├── chatbi_cli.py     # CLI 入口
│   ├── requirements.txt  # 依赖
│   └── chatbi/           # 核心模块
│       ├── __init__.py
│       ├── config.py     # 配置管理
│       ├── client.py     # 流式 API 客户端
│       ├── parser.py     # 流式事件解析与过滤
│       ├── formatter.py  # 输出格式化
│       └── models.py     # 数据模型
└── references/
    └── COMMANDS.md       # 命令参考
```
