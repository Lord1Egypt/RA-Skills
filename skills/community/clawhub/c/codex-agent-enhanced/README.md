# Codex Agent — 让 OpenClaw 替你操作 Codex 🧠

**[English](README_EN.md)** | 中文

> 你躺在床上说一句话，OpenClaw 帮你写提示词、启动 Codex、检查质量、汇报结果。全程自动，无需守着。

**这是一个 [OpenClaw](https://github.com/openclaw/openclaw) 专用 Skill。** 需要 OpenClaw 作为 AI agent 运行时，通过 OpenClaw 的 agent 唤醒、消息投递、cron 等能力驱动整个工作流。

## 它是什么？

一句话：**OpenClaw 代替用户操作 Codex CLI**。

Codex 是 OpenAI 的终端编程工具，很强，但需要你坐在电脑前盯着它——写提示词、等输出、审批命令、检查结果。这个 skill 让 OpenClaw 替你做这些事。

核心机制：**`codex exec` + notify hook**。

- **Exec 模式**：`codex exec --full-auto` 非交互式执行，适合 Agent 编程调用
- **Notify Hook**：Codex 完成任务时自动触发脚本，通知用户（Telegram）+ 唤醒 OpenClaw 处理

## 完全体 Codex

普通用法：你手动写提示词丢给 Codex，Codex 只知道你告诉它的东西。

OpenClaw 在发任务给 Codex 之前，会：

1. **识别本机环境**：当前装了哪些 MCP server（Exa 搜索、Chrome 控制等）、哪些 Skills、哪些模型可用
2. **根据任务选模型**：简单 bug 用快模型，架构设计用强模型，代码搜索用 code 专用模型
3. **设计提示词**：不是转发用户原话，而是基于知识库 + 提示词模式库，针对任务类型构造最优提示词——告诉 Codex 它能用什么工具、该怎么分步骤、输出什么格式
4. **开启合适的 feature flags**：比如 `multi_agent`、`web_search`、`shell_snapshot` 等，按需启用

这意味着 Codex 每次收到的都是一个**充分利用本机全部能力**的精心设计的任务，而不是用户随手写的一句话。

## 解决什么问题？

正常用 Codex 的流程：

```
你坐在电脑前 → 打开终端 → 想提示词 → 启动 Codex → 盯着输出 →
审批命令 → 不满意就重来 → 满意了收工
```

用了这个 skill：

```
你躺在床上 → 在 Telegram 里说"帮我给这个项目加个 XX 功能" →
OpenClaw 开 Codex 干活 → 中间过程自己处理 → 完事了 Telegram 通知你 →
不满意？说一句就继续改
```

**核心价值：用户当老板，OpenClaw 当员工，Codex 当工具。**

## 工作流程

```
1. 用户下任务（Telegram / 终端 / 任何渠道）
     ↓
2. OpenClaw 理解需求，追问不清楚的地方
     ↓
3. OpenClaw 设计提示词，选择执行模式，和用户确认
     ↓
4. OpenClaw 执行 `codex exec --full-auto`
     ↓
5. Codex 干活，notify hook 触发：
   ├── 📱 Telegram 通知用户（实时推送）
   └── 📄 更新项目状态文件（由 Cron 巡检推进）
     ↓
6. Cron 定时唤醒主会话（每 10 分钟）：
   ├─ review_pending → 检查输出质量
   │   ├─ 满意 → 汇报用户，清空任务
   │   └─ 不满意 → 发后续指令继续改
   └─ blocked → message.send 通知用户
     ↓
7. 用户收到最终结果
```

中间过程 OpenClaw 全权处理，但**每一步都会同步发送到 Telegram**——任务完成、输出内容，用户在手机上实时可见。你可以选择不管（让 OpenClaw 自主处理），也可以随时插话干预。
## 技术原理：Exec + Notify Hook

### Exec 模式：非交互式执行

```bash
# 基础用法
OPENCLAW_AGENT_NAME=main codex exec --full-auto "在 src/utils.ts 添加日期格式化函数"

# 指定工作目录
OPENCLAW_AGENT_NAME=main codex exec --full-auto -C /path/to/project "重构这个目录的代码"

# 指定模型和推理强度
OPENCLAW_AGENT_NAME=main codex exec --full-auto -m gpt-5.2 -c 'model_reasoning_effort="xhigh"' "任务描述"

# 附带图片
OPENCLAW_AGENT_NAME=main codex exec --full-auto -i screenshot.png "根据图片实现这个 UI"

# 启用网页搜索
OPENCLAW_AGENT_NAME=main codex exec --full-auto --search "查找最佳实践并应用到当前项目"
```

### Notify Hook：任务完成自动通知

Codex 配置 `~/.codex/config.toml`：

```toml
notify = ["python3", "/root/.openclaw/skills/codex-agent/hooks/on_complete.py"]
```

触发流程：
```
Codex 完成 turn → on_complete.py
                  ├── 📱 Telegram 通知用户（Codex 完整回复内容）
                  └── 🤖 openclaw agent 唤醒（OpenClaw 自动检查输出）
```

用户在 Telegram 上能看到 Codex 每次回复的完整内容，相当于实时监控。

### 审批处理

`--full-auto` 模式下，Codex 自主判断是否批准命令。如遇方向性问题或需要用户决策，OpenClaw 会主动询问。

## 两种执行模式

| 模式 | 谁审批 | 适用场景 |
|------|--------|---------|
| **Codex 自动** (`--full-auto`) | Codex 自己判断 | 常规开发，省心 |
| **人工审批** (默认) | Codex 弹出审批提示 | 敏感操作，需要把关 |

## 知识库：OpenClaw 真正理解 Codex

OpenClaw 不是盲目转发命令。它维护一套 Codex 知识库：

| 文件 | 内容 |
|------|------|
| `features.md` | 30+ feature flags、斜杠命令、CLI 子命令 |
| `config_schema.md` | config.toml 完整字段定义 |
| `capabilities.md` | 本机 MCP/Skills/模型能力 |
| `prompting_patterns.md` | 提示词模式库（按任务类型） |
| `UPDATE_PROTOCOL.md` | 5 级数据源更新协议 |
| `changelog.md` | 版本变更 + 实测发现 |

知识库会过时，所以有更新协议：版本变更 / 超 7 天 / 手动触发时，按 CLI 自省 → Schema → GitHub → 官方文档 → 社区的优先级更新。

## 文件结构

```
codex-agent/
├── SKILL.md                    # OpenClaw 工作流指令（给 OpenClaw 读的）
├── README.md                   # 本文件（给人读的）
│
├── hooks/
│   └── on_complete.py          # Codex 完成 → Telegram + OpenClaw 唤醒
│
├── knowledge/                  # Codex 知识库（6 文件）
│   ├── features.md
│   ├── config_schema.md
│   ├── capabilities.md
│   ├── prompting_patterns.md
│   ├── UPDATE_PROTOCOL.md
│   └── changelog.md
│
├── workflows/
│   ├── standard_task.md        # 标准任务流程
│   └── knowledge_update.md     # 知识库更新流程
│
├── references/
│   └── codex-cli-reference.md  # CLI 命令参考
│
└── state/
    ├── version.txt             # 当前 Codex 版本
    └── last_updated.txt        # 知识库最后更新日期
```

## 快速开始

详细的安装步骤见 **[INSTALL.md](INSTALL.md)**（7 步，约 5 分钟）。

或者，把下面这段话直接发给你的 OpenClaw，它会自动帮你完成配置：

> 请帮我安装和配置 codex-agent skill。
> 先读一遍完整的安装指南 `~/.openclaw/workspace/skills/codex-agent/INSTALL.md`，然后按照步骤帮我完成配置。
> 如果还没有这个文件，先从 https://github.com/dztabel-happy/codex-agent 克隆到 `~/.openclaw/workspace/skills/codex-agent/`，再读 INSTALL.md 执行。

配置完成后，在 Telegram 里对 OpenClaw 说一句话就能用：

> "用 Codex 帮我在 /path/to/project 实现 XX 功能"

## 更新

已安装的用户更新到最新版本：

```bash
cd ~/.openclaw/workspace/skills/codex-agent
git pull
```

更新日志见 **[CHANGELOG.md](CHANGELOG.md)**。

## 前置条件

- [OpenClaw](https://github.com/openclaw/openclaw) 已安装并运行
- [Codex CLI](https://github.com/openai/codex) 已安装
- Telegram 已配置为 OpenClaw 消息通道
- ⚠️ **OpenClaw session 自动重置必须关闭或调大**（默认每天重置会丢失 Codex 任务上下文，详见 [INSTALL.md](INSTALL.md#第四步配置-openclaw-session-重置)）

## 踩过的坑

| 问题 | 解决 |
|------|------|
| OpenClaw 默认每天重置 session，长任务上下文丢失 | 关闭自动重置（见前置配置） |
| Codex notify 不覆盖审批等待 | 已移除，--full-auto 模式自主判断 |
| `--full-auto` 与 shell alias 冲突报错 | 检查 `~/.bashrc` / `~/.zshrc` 是否有 codex alias |
| Codex memories 不工作 | `disable_response_storage = true` + custom provider 不兼容，不启用 |
| notify payload 缺少字段文档 | `turn-id` 和 `cwd` 是实测发现的 |

## 未来计划

- [ ] 复制模式到 Claude Code / OpenCode agent
- [ ] 补充更多提示词模式（代码审查、架构设计）
- [ ] 支持审批等待检测（如需要）

---

## 📋 配置指南

**重要**：codex-agent 是一个通用 skill，所有路径和参数都需要根据你的环境配置。

### 快速配置

1. **阅读配置模板**：`docs/CONFIG_TEMPLATE.md`
2. **复制并修改**：根据你的项目调整路径和参数
3. **设置环境变量**：在调用 codex exec 前设置

### 核心配置项

| 配置项 | 说明 | 是否必需 |
|--------|------|----------|
| `OPENCLAW_AGENT_NAME` | Agent 名称（选择 bot 账号） | ✅ 必需 |
| `OPENCLAW_AGENT_CHAT_ID` | Telegram Chat ID | ✅ 必需 |
| `OPENCLAW_PROJECT_STATE_FILE` | 项目状态文件路径 | ⚠️ Cron 模式必需 |
| `OPENCLAW_PROJECT_TASK_ID` | 任务 ID | ⚠️ Cron 模式必需 |

### Cron 配置

使用 Cron 巡检模式时，需要：
1. 创建 Cron Job 配置（参考 `docs/CONFIG_TEMPLATE.md`）
2. 替换占位符（`<YOUR_AGENT_ID>` / `<WAKER_PROMPT_PATH>`）
3. 执行 `openclaw cron add <配置文件>`

---

## 🚀 快速开始

### 方式 A：自动配置（推荐）

```bash
# 进入 skill 目录
cd /root/.openclaw/skills/codex-agent

# 简单模式（仅 Telegram 通知）
./scripts/setup.sh simple

# Cron 巡检模式（完整工作流）
./scripts/setup.sh cron
```

### 方式 B：手动配置

1. 复制 `.env.example` 为 `.env`
2. 编辑 `.env` 填入你的配置
3. 执行 `source .env`
4. 按照 `docs/CONFIG_TEMPLATE.md` 配置 Codex 和 Cron

---
