---
name: knot-agent-editor
description: 用于查看和修改 Knot 平台智能体（Agent）配置的专业技能。当用户需要以下操作时使用：(1) 查看当前对话智能体的草稿配置，(2) 查看指定 agent_id 的草稿配置，(3) 搜索/列出名下有管理权限的 agent，(4) 查看 agent 可用的大模型列表，(5) 基于最新版本重新生成 agent 草稿，(6) 修改 agent 草稿的名称、描述、欢迎语、系统提示词或默认模型，(7) 将草稿发布为正式版本。触发关键词：修改智能体、编辑agent、更新system prompt、修改提示词、查看agent配置、查看指定agent草稿、发布agent草稿等。
---

# Knot Agent Editor

用于查看和修改 Knot 平台智能体配置的工具集。

## 脚本目录（`scripts/`）

所有能力均已封装为独立 Python 脚本，通过 `terminal` 工具调用：

| 脚本 | 功能 |
|------|------|
| `get_current_draft.py` | 查看当前对话智能体的草稿配置 |
| `get_agent_draft.py` | 查看指定 agent_id 的草稿配置 |
| `list_agents.py` | 查询名下有管理权限的 Agent 列表 |
| `list_models.py` | 查看指定 Agent 可用的大模型列表 |
| `new_draft.py` | 基于最新版本重新生成 Agent 草稿 |
| `modify_draft.py` | 修改 Agent 草稿的指定字段 |
| `publish_draft.py` | 将草稿发布为正式版本（高危） |
| `common.py` | 公共模块（认证、JWT 解析等，不直接调用） |

**脚本路径**：`{SKILL_DIR}/scripts/<script_name>.py`

---

## 功能使用说明

### 1. 查看当前对话智能体的草稿

```bash
python {SKILL_DIR}/scripts/get_current_draft.py
```

自动从 JWT 解析当前 agent_id，展示草稿的名称、描述、欢迎语、系统提示词、模型、知识库等完整配置。

**注意**：
- `is_stale=true` 表示草稿已过期，发布将覆盖最新改动，需提示用户
- `can_edit=false` 表示无编辑权限

---

### 2. 查看指定 Agent 的草稿

```bash
python {SKILL_DIR}/scripts/get_agent_draft.py <agent_id>
```

- `agent_id`：必填，目标 Agent 的 ID（可通过 `list_agents.py` 获取）
- 展示指定 Agent 草稿的名称、描述、欢迎语、系统提示词、模型、知识库等完整配置

**示例**：
```bash
python {SKILL_DIR}/scripts/get_agent_draft.py 877c45a6f2f542e0b3dadb089f6ef532
```

---

### 3. 查询名下管理的 Agent 列表

```bash
python {SKILL_DIR}/scripts/list_agents.py [--agent_id <id>] [--keyword <关键字>]
```

- `--agent_id`：可选，按 agent_id 精确查询
- `--keyword`：可选，按名称/描述关键字过滤

---

### 4. 查看 Agent 可用的大模型

```bash
python {SKILL_DIR}/scripts/list_models.py [agent_id]
```

- `agent_id`：可选，不传则使用当前对话的 agent_id
- 修改模型前先调用此脚本，获取合法的 `model_name`

---

### 5. 基于最新版本重新生成草稿

```bash
python {SKILL_DIR}/scripts/new_draft.py [agent_id]
```

- 脚本会在终端提示二次确认（输入 `yes` 执行）
- **⚠️ 会覆盖当前未发布的草稿内容**，需用户确认后再执行

---

### 6. 修改草稿字段

```bash
# 修改名称和描述
python {SKILL_DIR}/scripts/modify_draft.py --name "新名称" --desc "新描述"

# 修改系统提示词（直接传值）
python {SKILL_DIR}/scripts/modify_draft.py --system_prompt "你是一个专业助手..."

# 修改系统提示词（从文件读取，适合长提示词）
python {SKILL_DIR}/scripts/modify_draft.py --system_prompt @/path/to/prompt.txt

# 修改默认模型（model_name 从 list_models.py 获取）
python {SKILL_DIR}/scripts/modify_draft.py --model claude-3-5-sonnet

# 指定 agent_id（不指定则使用当前对话 agent）
python {SKILL_DIR}/scripts/modify_draft.py agent_xxx --name "新名称"
```

**支持的参数**：`--name`、`--desc`、`--welcome_msg`、`--system_prompt`、`--model`

**修改完成后必须提示用户**：草稿修改仅在页面调试时生效，若需正式对话生效请将草稿发布成正式版本。

---

### 7. 发布草稿（高危操作）

```bash
python {SKILL_DIR}/scripts/publish_draft.py [agent_id]
```

- 脚本会自动检查草稿是否 `is_stale`，并在终端提示二次确认（输入 `yes` 执行）
- **⚠️ 发布后所有用户的正式对话立即使用新版本**
- 若 `is_stale=true`，脚本会显示红色警告，建议先运行 `new_draft.py`
- 必须获得用户明确确认后再执行此操作

---

## 展示规范

- 展示草稿信息时，以结构化方式呈现各字段，**system_prompt 必须完整展示，不得截断**
- 展示 agent 列表时使用表格，包含 id、名称、描述、是否可编辑
- 展示模型列表时使用表格，包含 display_name、model_name、描述
- 操作成功/失败均给出明确反馈

## 详细 API 文档

见 [references/api.md](references/api.md)
