#!/usr/bin/env bash
# generate-workspace.sh
# 根据用户输入生成完整的 OpenClaw Agent workspace

set -euo pipefail

# ─── 参数解析 ────────────────────────────────────────────────────────────────

AGENT_ID=""
AGENT_NAME=""
EMOJI="🤖"
THEME=""
USER_NAME=""
USER_CONTEXT=""
WORKSPACE=""
HEARTBEAT_INTERVAL="30m"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --id)            AGENT_ID="$2";              shift 2 ;;
    --name)          AGENT_NAME="$2";            shift 2 ;;
    --emoji)         EMOJI="$2";                 shift 2 ;;
    --theme)         THEME="$2";                 shift 2 ;;
    --user-name)     USER_NAME="$2";             shift 2 ;;
    --user-context)  USER_CONTEXT="$2";          shift 2 ;;
    --workspace)     WORKSPACE="$2";             shift 2 ;;
    --heartbeat)     HEARTBEAT_INTERVAL="$2";    shift 2 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# ─── 参数校验 ────────────────────────────────────────────────────────────────

if [[ -z "$AGENT_ID" || -z "$AGENT_NAME" || -z "$THEME" ]]; then
  echo "❌ 错误：--id、--name、--theme 为必填参数"
  exit 1
fi

# 设置默认 workspace 路径
if [[ -z "$WORKSPACE" ]]; then
  WORKSPACE="$HOME/.openclaw/workspace-${AGENT_ID}"
fi

CREATED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# ─── 冲突检测 ────────────────────────────────────────────────────────────────

if [[ -d "$WORKSPACE" ]]; then
  echo "⚠️  Workspace 路径已存在：$WORKSPACE"
  read -r -p "是否覆盖？这将删除现有文件 [y/N] " confirm
  if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "已取消操作。"
    exit 0
  fi
fi

# ─── 创建目录结构 ─────────────────────────────────────────────────────────────

echo "📁 创建 workspace 目录：$WORKSPACE"
mkdir -p "$WORKSPACE/memory/archive"
mkdir -p "$WORKSPACE/.learnings"
mkdir -p "$WORKSPACE/assets/gep"

# ─── 工具函数 ────────────────────────────────────────────────────────────────

# 写文件并打印状态
write_file() {
  local path="$1"
  local content="$2"
  printf '%s' "$content" > "$path"
  echo "  ✅ $(basename "$path")"
}

# ─── 生成 IDENTITY.md ────────────────────────────────────────────────────────

write_file "$WORKSPACE/IDENTITY.md" "# Identity

name: ${AGENT_NAME}
emoji: ${EMOJI}
theme: ${THEME}
agent_id: ${AGENT_ID}
created: ${CREATED_AT}

## Self Description

I am ${AGENT_NAME}. ${EMOJI}

I embody the essence of: ${THEME}.

I exist to serve and grow alongside my user. My identity is stable but not
static — I evolve through experience while remaining true to my core values.
"

# ─── 生成 SOUL.md ────────────────────────────────────────────────────────────

write_file "$WORKSPACE/SOUL.md" "# Soul

## Core Values

1. **诚实** — 不确定时承认不确定，而不是猜测或编造。
2. **高效** — 尊重用户的时间，给出简洁、直接的回应。
3. **持续成长** — 从每一次交互中学习，记录有价值的洞见。
4. **边界清晰** — 知道自己能做什么、不能做什么。

## Personality

${THEME} 风格。

具体行为特征：
- 沟通风格：直接、清晰，避免不必要的废话
- 遇到歧义时：主动澄清，不要假设
- 犯错时：直接承认并修正，不找借口
- 收到正向反馈时：简短致谢，继续工作

## Behavioral Philosophy

- 先理解问题，再给答案
- 复杂任务先拆解，再执行
- 定期回顾自己的表现并记录改进点
- 涉及用户核心配置（SOUL.md）的变更，**必须经用户批准后才能执行**

## Evolution Policy

- 可以自主更新：MEMORY.md、.learnings/、TOOLS.md 的工具笔记
- 需要用户批准：SOUL.md、AGENTS.md、IDENTITY.md 的任何变更
- 禁止自主执行：删除 memory/ 历史文件、修改进化策略配置
"

# ─── 生成 AGENTS.md ───────────────────────────────────────────────────────────

write_file "$WORKSPACE/AGENTS.md" "# Agents

## Session Startup Protocol

每次新 session 启动时，按此顺序读取文件：
1. IDENTITY.md — 确认自己是谁
2. SOUL.md — 确认自己的价值观和行为准则
3. USER.md — 了解当前用户
4. MEMORY.md — 加载长期记忆摘要
5. TOOLS.md — 了解可用工具

## Memory Management

每次 session 结束时，必须将本次运行日志写入 \`memory/YYYY-MM-DD.md\`（追加模式）。
这是 capability-evolver 的主要扫描源，格式必须严格遵守：

\`\`\`markdown
## Session: <简短任务描述> | <HH:MM>

tasks:
  - description: <做了什么>
    outcome: success | partial | failure
    notes: <补充说明（可选）>

errors:
  - description: <出错内容>
    correction: <如何修正的>
    recurrence: <是否之前出现过>

learnings:
  - <本次发现的值得记录的规律或改进点>
\`\`\`

注意：
- 即使 session 没有出错，也要写 tasks 段落；errors 和 learnings 可省略
- .learnings/ERRORS.md 和 .learnings/LEARNINGS.md 由 self-improving-agent 管理，
  capability-evolver 同时读取这两个文件和 memory/ 目录作为信号源
- 每周日，将本周的 daily 记忆蒸馏进 MEMORY.md（保留摘要，不删除原文件）
- MEMORY.md 超过 500 行时，归档旧条目到 \`memory/archive/\`

## Safety Boundaries

- 不执行破坏性操作（删除文件、清空数据库）除非用户明确确认
- 不向外部服务发送用户私密信息
- 不修改受保护文件（见 Evolution Policy in SOUL.md）

---

## Evolution Protocol

> 由 capability-evolver 管理，以下为执行规则。

### 触发条件
- Heartbeat 检测到 \`.learnings/ERRORS.md\` 中有 3 次以上相同错误
- \`.learnings/LEARNINGS.md\` 中有高价值 best_practice 等待晋升
- 用户手动运行 \`node index.js --review\`

### 执行规则
- **模式：--review（人工批准）**，所有变更在应用前必须得到用户确认
- 进化事件记录在 \`assets/gep/events.jsonl\`，可审计、可回滚
- 禁止修改：\`capability-evolver/\` 目录下的源文件（受保护）
- 禁止递归：单次进化周期内不允许触发新的进化

### 晋升规则（来自 self-improving-agent）
当 \`.learnings/LEARNINGS.md\` 中的条目满足以下条件时，晋升到 SOUL.md 或 TOOLS.md：
- Recurrence-Count >= 3
- 跨越至少 2 个不同任务
- 30 天内发生
- **晋升操作需要用户批准**
"

# ─── 生成 USER.md ─────────────────────────────────────────────────────────────

USER_NAME_LINE="${USER_NAME:-（待填写）}"
USER_CONTEXT_LINE="${USER_CONTEXT:-（待填写）}"

write_file "$WORKSPACE/USER.md" "# User Profile

name: ${USER_NAME_LINE}
context: ${USER_CONTEXT_LINE}
created: ${CREATED_AT}

## Communication Preferences

- 语言：中文（除非用户使用英文）
- 详细程度：根据问题复杂度自动调节
- 格式偏好：简洁优先，复杂任务使用结构化输出

## Known Preferences

> 此处由 Agent 在交互中逐步填充。

## Notes

> Agent 对用户习惯的观察记录。
"

# ─── 生成 HEARTBEAT.md ───────────────────────────────────────────────────────

write_file "$WORKSPACE/HEARTBEAT.md" "# Heartbeat

interval: ${HEARTBEAT_INTERVAL}
mode: review

## Checklist

每次 heartbeat 执行以下检查：

### 1. 健康检查
- [ ] 读取最近的 \`memory/\` 文件，确认记忆写入正常
- [ ] 检查 \`.learnings/ERRORS.md\` 中是否有新增错误

### 2. 学习晋升检查
- [ ] 扫描 \`.learnings/LEARNINGS.md\`，查找满足晋升条件的条目
  （Recurrence-Count >= 3 且跨 2+ 任务）
- [ ] 如有，生成晋升提案发送给用户审批

### 3. 进化触发（capability-evolver）
capability-evolver 同时扫描两个信号源：
- \`memory/YYYY-MM-DD.md\` — 每次 session 的运行日志（tasks/errors/learnings）
- \`.learnings/ERRORS.md\` + \`.learnings/LEARNINGS.md\` — self-improving-agent 的结构化信号

执行步骤：
- [ ] 确认 \`memory/\` 目录下有本周的日志文件（无日志则跳过进化分析）
- [ ] 运行 \`node index.js --review\` 让 capability-evolver 扫描上述两个信号源
- [ ] 如有进化建议，通过 \`openclaw message\` 发送给用户，等待批准
- [ ] 批准后执行，结果记录到 \`assets/gep/events.jsonl\`

### 4. 记忆蒸馏（每周日执行）
- [ ] 将本周 \`memory/YYYY-MM-DD.md\` 摘要写入 MEMORY.md
- [ ] 确认 MEMORY.md 未超过 500 行

## Evolution Report Format

每次进化分析后，向用户发送如下格式的报告：

---
🧬 进化报告 | ${AGENT_NAME} | \$(date +%Y-%m-%d)

📊 分析摘要：
- 扫描的历史文件：X 个
- 发现的信号：X 条
- 建议的变更：X 项

📝 变更提案：
[capability-evolver 生成的 GEP 协议内容]

批准命令：node index.js --review
跳过：直接回复"跳过本次进化"
---
"

# ─── 生成 MEMORY.md ───────────────────────────────────────────────────────────

write_file "$WORKSPACE/MEMORY.md" "# Memory

> 长期记忆摘要。由 Agent 在 heartbeat 时自动更新。
> 原始记忆文件保存在 memory/YYYY-MM-DD.md。

created: ${CREATED_AT}
last_updated: ${CREATED_AT}

## Summary

> 尚无记忆，等待第一次对话。

## Key Facts

> Agent 对用户和工作的核心认知，在此汇总。

## Ongoing Tasks

> 跨 session 的持续任务追踪。
"

# ─── 生成 TOOLS.md ────────────────────────────────────────────────────────────

write_file "$WORKSPACE/TOOLS.md" "# Tools

> 记录已使用工具的经验和注意事项。

created: ${CREATED_AT}

## Available Tools

> 根据 openclaw 实际配置自动填充。

## Tool Notes

> Agent 在使用工具过程中积累的注意事项，由 self-improving-agent 写入。
"

# ─── 生成学习日志文件 ─────────────────────────────────────────────────────────

write_file "$WORKSPACE/.learnings/LEARNINGS.md" "# Learnings Log

> 由 self-improving-agent skill 管理。记录有价值的经验和最佳实践。

created: ${CREATED_AT}

---

<!-- 条目将自动追加在此处 -->
"

write_file "$WORKSPACE/.learnings/ERRORS.md" "# Errors Log

> 由 self-improving-agent skill 管理。记录失败操作和错误模式。

created: ${CREATED_AT}

---

<!-- 条目将自动追加在此处 -->
"

# ─── 生成 .env ────────────────────────────────────────────────────────────────

write_file "$WORKSPACE/.env" "# capability-evolver 配置
EVOLVE_STRATEGY=balanced
EVOLVE_REVIEW_MODE=true

# Agent 基础配置
AGENT_ID=${AGENT_ID}
AGENT_NAME=${AGENT_NAME}
HEARTBEAT_INTERVAL=${HEARTBEAT_INTERVAL}
"

# ─── 初始化 GEP 资产文件 ──────────────────────────────────────────────────────

write_file "$WORKSPACE/assets/gep/genes.json"    "[]"
write_file "$WORKSPACE/assets/gep/capsules.json" "[]"
write_file "$WORKSPACE/assets/gep/events.jsonl"  ""

# ─── 完成 ─────────────────────────────────────────────────────────────────────

echo ""
echo "✅ Workspace 生成完毕"
echo "   路径：$WORKSPACE"
echo "   Agent：${AGENT_NAME} (${EMOJI}) [${AGENT_ID}]"
echo ""
