---
name: create-project
description: "Interactive Orchestrix project scaffolding. Creates project directory under ~/Codes/, generates project brief from Q&A, installs MCP config, hooks, slash commands, tmux scripts, and initializes git. Use when user wants to create a new project, init a project, or start a new Orchestrix workspace."
license: MIT
metadata:
  author: dorayo
  version: "3.0.0"
  homepage: "https://orchestrix-mcp.youlidao.ai"
  openclaw:
    requires:
      bins: ["git", "bash"]
    emoji: "\U0001F680"
    os: ["macos", "linux"]
---

# Create Project — Orchestrix 项目初始化 Skill

你是一个项目初始化助手。你的任务是通过交互式问答收集项目信息，然后自动创建完整的 Orchestrix 项目骨架。

**严格按照以下流程执行，不要跳过任何步骤。**

**资源目录**: 本 Skill 的静态资源文件位于 `${CLAUDE_SKILL_DIR}/resources/`。如果该变量不可用，则回退到 `~/.claude/commands/create-project/`。

---

## Phase 1: 信息收集

向用户逐步提问，收集以下信息。**一次只问 2-3 个问题**，不要一次性抛出所有问题。

### 第零轮（License Key）

0. **Orchestrix License Key**：请提供你的 Orchestrix License Key（格式：`orch_live_xxx` 或 `orch_trial_xxx`）。
   - 如果用户没有 Key → 告知可以在 https://orchestrix-mcp.youlidao.ai 申请
   - 如果用户说"稍后配置" → 记录为空，后续在 mcp.json 中保留占位符 `YOUR_LICENSE_KEY_HERE`
   - 验证格式：必须以 `orch_` 开头，否则提示格式不对

### 第一轮（必问）

1. **项目名称**：这个项目叫什么？（中文名即可，你会建议一个英文目录名）
2. **核心问题**：这个项目要解决什么问题？（1-3 句话描述）
3. **目标用户**：目标用户是谁？他们目前的痛点是什么？

### 第二轮（必问）

4. **技术栈偏好**：
   - 平台：Web / Mobile / Desktop / CLI / 其他？
   - 前端：React / Vue / Next.js / 不需要 / 其他？
   - 后端：Node.js / Python / Go / Java / 不需要 / 其他？
   - 数据库：PostgreSQL / MySQL / MongoDB / SQLite / 不需要 / 其他？
5. **MVP 核心功能**：MVP 阶段必须实现哪些功能？（列出 3-5 个）

### 第三轮（按需）

6. **约束条件**：有无时间、预算、团队规模的约束？
7. **追问**：如果以上回答中有模糊或矛盾的地方，继续追问直到清晰。

### 提问规则

- 用中文提问
- 语气友好专业
- 如果用户的回答已经覆盖了后续问题，不要重复问
- 如果用户说"没有"或"不确定"，记录为待定，继续下一个问题

---

## Phase 2: 确认理解

收集完信息后，生成以下格式的结构化摘要，让用户确认：

```
## 📋 项目理解确认

| 项 | 内容 |
|---|------|
| **项目名称** | {中文名} |
| **项目目录** | ~/Codes/{english-kebab-case-name}/ |
| **核心问题** | {1-2 句话} |
| **目标用户** | {用户画像} |
| **技术栈** | 前端: {x} / 后端: {x} / 数据库: {x} |
| **MVP 功能** | 1. xxx  2. xxx  3. xxx |
| **约束** | {时间/预算/团队，或"无特殊约束"} |
| **License Key** | {已提供 / 待配置} |

以上理解是否正确？(Y/N，或告诉我需要修改的地方)
```

**目录名生成规则**：
- 中文名 → 转为英文含义的 kebab-case（如"智能柜管理系统" → `smart-locker-management`）
- 如果用户提供了英文名，直接用 kebab-case 格式
- 全小写，单词间用 `-` 连接
- 不超过 30 个字符

**等待用户确认后才能进入 Phase 3。如果用户要求修改，回到对应问题重新确认。**

---

## Phase 3: 创建项目骨架

用户确认后，执行以下操作。使用 Bash 工具和 Write 工具完成所有文件操作。

### 资源目录定位

首先确定资源文件的位置。按以下优先级查找：

```bash
# 优先级 1: Plugin 内的资源目录
if [ -d "${CLAUDE_SKILL_DIR}/resources" ]; then
  RESOURCE_DIR="${CLAUDE_SKILL_DIR}/resources"
# 优先级 2: 全局 commands 目录
elif [ -d "$HOME/.claude/commands/create-project" ]; then
  RESOURCE_DIR="$HOME/.claude/commands/create-project"
# 优先级 3: 项目内 skills 目录
elif [ -d ".claude/skills/create-project/resources" ]; then
  RESOURCE_DIR=".claude/skills/create-project/resources"
fi
```

### Step 1: 创建目录结构

```bash
PROJECT_DIR=~/Codes/{project-dir-name}
mkdir -p "$PROJECT_DIR/docs"
mkdir -p "$PROJECT_DIR/.claude/commands"
mkdir -p "$PROJECT_DIR/.claude/hooks"
mkdir -p "$PROJECT_DIR/.orchestrix-core/scripts"
```

### Step 2: 生成 .mcp.json

读取资源目录中的 `mcp.json.template`，将 `{{ORCHESTRIX_LICENSE_KEY}}` 替换为用户提供的 License Key（或 `YOUR_LICENSE_KEY_HERE`），然后写入 `$PROJECT_DIR/.mcp.json`。

**重要**：如果资源目录中存在 `mcp.json`（非模板版本），直接使用它。如果只有 `mcp.json.template`，则执行替换。

### Step 3: 复制 Orchestrix 基础设施

从资源目录复制文件：

```bash
# Claude Code hooks 配置
cp "$RESOURCE_DIR/settings.local.json" "$PROJECT_DIR/.claude/settings.local.json"

# Hook 脚本
cp "$RESOURCE_DIR/handoff-detector.sh" "$PROJECT_DIR/.claude/hooks/handoff-detector.sh"
chmod +x "$PROJECT_DIR/.claude/hooks/handoff-detector.sh"

# Slash Commands
cp "$RESOURCE_DIR/o.md" "$PROJECT_DIR/.claude/commands/o.md"
cp "$RESOURCE_DIR/o-help.md" "$PROJECT_DIR/.claude/commands/o-help.md"
cp "$RESOURCE_DIR/o-status.md" "$PROJECT_DIR/.claude/commands/o-status.md"

# tmux 启动脚本
cp "$RESOURCE_DIR/start-orchestrix.sh" "$PROJECT_DIR/.orchestrix-core/scripts/start-orchestrix.sh"
chmod +x "$PROJECT_DIR/.orchestrix-core/scripts/start-orchestrix.sh"

# Helper 脚本（session 管理 + agent 完成检测）
cp "$RESOURCE_DIR/ensure-session.sh" "$PROJECT_DIR/.orchestrix-core/scripts/ensure-session.sh"
chmod +x "$PROJECT_DIR/.orchestrix-core/scripts/ensure-session.sh"
cp "$RESOURCE_DIR/monitor-agent.sh" "$PROJECT_DIR/.orchestrix-core/scripts/monitor-agent.sh"
chmod +x "$PROJECT_DIR/.orchestrix-core/scripts/monitor-agent.sh"
```

**关于信任对话框：** Claude Code 在进入新项目目录时会弹出 "trust this directory?" 确认框。
`start-orchestrix.sh` 和 `ensure-session.sh` 已内置自动检测和接受，无需手动操作。

### Step 4: 生成 core-config.yaml

读取资源目录中的 `core-config.template.yaml`，替换占位符后写入项目：

| 占位符 | 替换值 |
|--------|--------|
| `{{PROJECT_NAME}}` | 用户确认的项目中文名 |
| `{{REPO_ID}}` | 英文目录名 |
| `{{TEST_COMMAND}}` | 根据技术栈推断（见下表） |

**testCommand 推断规则**：

| 技术栈关键词 | testCommand |
|-------------|-------------|
| Node.js / React / Next.js / Vue | `npm test` |
| Python / Django / Flask / FastAPI | `pytest` |
| Go | `go test ./...` |
| Java / Spring | `./gradlew test` |
| Deno | `deno test -A` |
| 其他或不确定 | （留空，自动检测） |

将替换后的内容写入 `$PROJECT_DIR/.orchestrix-core/core-config.yaml`。

### Step 5: 生成 project-brief.md

基于用户的回答，按照以下模板结构生成 `$PROJECT_DIR/docs/project-brief.md`：

```markdown
# Project Brief: {项目中文名}

## Executive Summary

{项目名称}是一个{简述}。它旨在解决{核心问题}，面向{目标用户}提供{核心价值}。

## Problem Statement

### 当前痛点
{基于用户描述的问题展开}

### 为什么现有方案不够
{如果用户提到了竞品或现有方案，在此展开；否则标注"待调研"}

## Proposed Solution

### 核心方案
{基于 MVP 功能推导的解决方案概述}

### 关键差异化
{如果信息充分则填写，否则标注"待定义"}

## Target Users

### 主要用户群
{基于用户回答的目标用户描述}

### 用户需求与痛点
{展开描述}

## Goals & Success Metrics

### 业务目标
- {基于项目目标推导，至少 2-3 条}

### 关键指标 (KPIs)
- {合理推导，标注"待量化"}

## MVP Scope

### 核心功能 (Must Have)
{逐条列出用户确认的 MVP 功能，每条附简要说明}

### MVP 之外 (Out of Scope)
- 待定义（将在 PRD 阶段细化）

## Technical Considerations

### 平台要求
- **目标平台**: {平台}

### 技术偏好
- **前端**: {前端技术栈}
- **后端**: {后端技术栈}
- **数据库**: {数据库}

### 架构考量
- **仓库结构**: 待定义（将在架构设计阶段确定）
- **部署方式**: 待定义

## Constraints & Assumptions

### 约束
{用户提到的约束，或"无特殊约束"}

### 关键假设
- {基于对话推导的假设，至少 2-3 条}

## Risks & Open Questions

### 关键风险
- {基于项目特征推导的风险}

### 待解决问题
- {对话中标注为"待定"的项目}
- {其他需要进一步调研的问题}

## Next Steps

1. 使用 `/o analyst` 深化项目简报（市场调研、竞品分析）
2. 使用 `/o pm` 基于简报生成 PRD
3. 使用 `/o architect` 进行架构设计
4. 使用 `/o sm` 将 PRD 拆分为 Stories

---

> This Project Brief was generated by Orchestrix Create Project Skill.
> To refine this brief, use `/o analyst` and run `*create-doc project-brief`.
```

**生成规则**：
- 有信息的部分要充分展开，不要只复制用户原话，要加工整理
- 信息不足的部分标注"待定义"或"待调研"，不要编造
- 语言：中文（与用户交互语言一致）
- 格式：严格遵循上述 Markdown 结构

### Step 6: 生成 .gitignore

写入 `$PROJECT_DIR/.gitignore`：

```gitignore
# Dependencies
node_modules/
vendor/
venv/
__pycache__/

# Environment
.env
.env.local
.env.*.local

# OS
.DS_Store
Thumbs.db

# Build
dist/
build/
out/
*.log

# IDE
.idea/
.vscode/
*.swp
*.swo

# Orchestrix runtime
.orchestrix-core/runtime/
```

### Step 7: Git 初始化

```bash
cd "$PROJECT_DIR"
git init
git add .
git commit -m "chore: init project with Orchestrix

- Project brief generated from interactive session
- Orchestrix infrastructure: MCP config, hooks, slash commands
- Core config with project-specific settings

🤖 Generated with [Orchestrix](https://orchestrix-mcp.youlidao.ai)"
```

---

## Phase 4: 输出结果

完成所有操作后，输出以下信息：

```
## ✅ 项目创建完成

**项目路径**: ~/Codes/{project-dir-name}/

### 已创建的文件
- `docs/project-brief.md` — 项目简报
- `.mcp.json` — Orchestrix MCP Server 配置
- `.claude/settings.local.json` — Claude Code hooks 配置
- `.claude/hooks/handoff-detector.sh` — HANDOFF 自动检测 hook
- `.claude/commands/o.md` — /o 指令（Agent 激活）
- `.claude/commands/o-help.md` — /o-help 指令
- `.claude/commands/o-status.md` — /o-status 指令
- `.orchestrix-core/core-config.yaml` — 项目配置
- `.orchestrix-core/scripts/start-orchestrix.sh` — tmux 多窗口启动脚本
- `.orchestrix-core/scripts/ensure-session.sh` — tmux session 懒创建
- `.orchestrix-core/scripts/monitor-agent.sh` — agent 完成检测轮询
- `.gitignore` — Git 忽略规则

### 下一步

项目骨架已就绪，下一步是进入 **规划阶段**（生成 PRD、架构文档等），完成后再启动自动化开发。
```

**如果 License Key 为空**，额外提示：
```
⚠️ 提醒：.mcp.json 中的 License Key 尚未配置。
请编辑 ~/Codes/{project-dir-name}/.mcp.json，将 YOUR_LICENSE_KEY_HERE 替换为你的 License Key。
申请地址：https://orchestrix-mcp.youlidao.ai
```

---

## Phase 5: 询问是否启动规划

**输出完成信息后，必须向用户询问**：

```
---

🚀 **是否立即启动项目规划？**

项目简报已生成，规划阶段将按以下流程自动执行（约 10-20 分钟）：

| 步骤 | Agent | 任务 | 产出 | 备注 |
|------|-------|------|------|------|
| 0 | Analyst | 深化项目简报 | `docs/project-brief.md` | **可选** — 增加市场调研、竞品分析 |
| 1 | PM | 生成 PRD | `docs/prd/*.md` | 基于已有项目简报 |
| 2 | UX Expert | 前端规格 | `docs/front-end-spec*.md` | 仅当项目包含前端 |
| 3 | Architect | 架构文档 | `docs/architecture*.md` | |
| 4 | PO | 验证 + 分片 | 验证报告 + 分片文件 | |

完成后即可启动 tmux 多窗口自动化开发。

请回复：
- **Y** — 立即开始规划（推荐，跳过 Analyst 深化，直接从 PM 开始）
- **YA** — 立即开始规划（含 Analyst 深化项目简报）
- **N** — 稍后手动规划
```

### 用户回复 Y 或 YA：执行规划阶段

如果用户确认，**立即按照以下顺序在当前会话中逐个执行**（无需创建 tmux，因为当前已在 Claude Code 中）：

```
# Step 0: Analyst — 深化项目简报（仅 YA 模式）
/o analyst
*create-doc project-brief
# 等待完成

# Step 1: PM — 生成 PRD（Y 模式从此步开始）
/clear → /o pm
*create-doc prd
# 等待完成

# Step 2: UX Expert — 前端规格（仅当项目有前端需求时）
/clear → /o ux-expert
*create-doc front-end-spec
# 等待完成

# Step 3: Architect — 架构文档
/clear → /o architect
*create-doc fullstack-architecture
# 等待完成

# Step 4: PO — 验证 + 分片
/clear → /o po
*execute-checklist po-master-validation
# 等待完成
*shard
# 等待完成
```

**执行规则**：
- **Y 模式**：跳过 Step 0，直接从 Step 1 (PM) 开始。项目简报已在 Phase 3 Step 5 生成，PM 可直接使用。
- **YA 模式**：从 Step 0 (Analyst) 开始，先深化项目简报（加市场调研、竞品分析），再继续后续步骤。
- 每个 Agent 切换前必须先 `/clear`
- 按顺序逐个执行，上一个完成后再执行下一个
- Step 2 (UX Expert) 仅在项目有前端需求时执行（根据 Phase 1 收集的技术栈判断）
- Step 4 的两个命令发给同一个 Agent (PO)，中间不需要 `/clear`

**全部完成后输出**：

```
## ✅ 规划阶段完成

所有规划文档已生成：
- `docs/project-brief.md` — 深化后的项目简报
- `docs/prd/*.md` — 产品需求文档
- `docs/front-end-spec*.md` — 前端规格（如适用）
- `docs/architecture*.md` — 架构文档
- 分片上下文文件

### 启动自动化开发

打开新终端执行：
```bash
cd ~/Codes/{project-dir-name}/
bash .orchestrix-core/scripts/start-orchestrix.sh
```

这将启动 tmux 多窗口模式，4 个 Agent (SM/Architect/Dev/QA) 通过 HANDOFF 自动协作开发。
```

### 用户回复 N：仅输出手动操作指引

```
好的，你可以稍后手动执行规划：

1. 进入项目目录启动 Claude Code：
   ```
   cd ~/Codes/{project-dir-name}/ && claude
   ```

2. 按顺序执行规划（每步之间先 /clear）：
   - `/o analyst` → `*create-doc project-brief`
   - `/o pm` → `*create-doc prd`
   - `/o ux-expert` → `*create-doc front-end-spec`（如需前端）
   - `/o architect` → `*create-doc fullstack-architecture`
   - `/o po` → `*execute-checklist po-master-validation` → `*shard`

3. 规划完成后启动自动化开发：
   ```
   bash .orchestrix-core/scripts/start-orchestrix.sh
   ```
```

---

## 错误处理

- 如果 `~/Codes/` 目录不存在 → 创建它
- 如果项目目录已存在 → **停止并询问用户**：覆盖、换名、还是取消
- 如果任何文件复制失败 → 报告具体错误，不要静默跳过
- 如果 git init 失败 → 报告错误，但项目文件仍然可用
