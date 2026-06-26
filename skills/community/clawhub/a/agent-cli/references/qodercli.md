---
name: qoder-cli-core
version: 1.0.0
description: Qoder CLI（qodercli）使用规范（凝练版，适用于 Agent 调用）
author: workspace
---

# Qoder CLI 核心操作

## 1. TUI（默认）

在任意项目根目录执行：

```bash
qodercli
```

通过自然语言对话；也可用斜杠命令与多种输入模式。

---

## 2. 输入模式（在 TUI 内）

| 前缀 | 作用 |
| :--- | :--- |
| （默认）`>` | 对话模式：普通文本与 CLI 对话 |
| `!` | Bash：直接跑 shell |
| `/` | 斜杠：内置命令 |
| `#` | 记忆：追加到项目 `AGENTS.md` |
| `\` + 回车 | 多行输入 |

注意：`>` / `!` / `/` 等是 **qodercli 界面内** 的语义；**不要**在系统 shell 里单独输入 `>`（会被当成重定向）。

---

## 3. 内置工具

Grep、Read、Write、Bash 等：读文件、搜目录、写文件、执行命令（以当前版本为准）。

---

## 4. 常用斜杠命令

| 命令 | 作用 |
| :--- | :--- |
| `/login` `/logout` | 登录 / 退出账号 |
| `/help` | TUI 帮助 |
| `/init` | 初始化或更新项目 `AGENTS.md` |
| `/memory` | 编辑 `AGENTS.md`（用户级/项目级可选） |
| `/quest` | 基于 Spec 的任务委派 |
| `/review` | 本地改动评审 |
| `/resume` | 会话列表与恢复 |
| `/clear` `/compact` | 清上下文 / 压缩总结上下文 |
| `/usage` | 账户与 Credits |
| `/status` | 版本、模型、连通性、工具状态 |
| `/config` | 系统配置 |
| `/agents` | 子 Agent 管理 |
| `/bashes` | 后台 Bash 任务 |
| `/release-notes` | 更新日志 |
| `/vim` | 外部编辑器编辑输入 |
| `/feedback` | 反馈问题 |
| `/quit` | 退出 TUI |

---

## 5. 启动参数（TUI / 通用）

| 参数 | 说明 |
| :--- | :--- |
| `-w <dir>` | 工作区目录 |
| `-c` | 继续上次会话 |
| `-r <id>` | 恢复指定会话 |
| `--allowed-tools` | 仅允许列出工具（如 `READ,WRITE`） |
| `--disallowed-tools` | 禁止列出工具 |
| `--max-turns` | 最大对话轮数 |
| `--yolo` | 跳过权限检查（慎用） |

---

## 6. Print（非交互）

```bash
qodercli --print
```

配合输出格式（如 `text` / `json` / `stream-json`）使用；适合脚本与自动化。

| 参数 | 说明 |
| :--- | :--- |
| `-p` | 非交互跑一轮 Agent（示例：`qodercli -p "hi"`，具体以 `--help` 为准） |
| `--output-format` | `text` / `json` / `stream-json` 等 |

---

## 7. MCP

添加（示例：Playwright）：

```bash
qodercli mcp add playwright -- npx -y @playwright/mcp@latest
```

管理：

```bash
qodercli mcp list
qodercli mcp remove playwright
```

* `-t`：stdio / sse / streamable-http（stdio 常在 TUI 启动时拉起）  
* `-s`：用户级或项目级范围  

配置文件位置：

* 用户或项目：`~/.qoder.json`  
* 项目（可提交）：`${project}/.mcp.json`  

推荐（按需安装）：

```bash
qodercli mcp add context7 -- npx -y @upstash/context7-mcp@latest
qodercli mcp add deepwiki -- npx -y mcp-deepwiki@latest
qodercli mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```

---

## 8. 权限（Permission）

配置文件（优先级从低到高）：

```
~/.qoder/settings.json
${project}/.qoder/settings.json
${project}/.qoder/settings.local.json   # 建议 .gitignore
```

策略：`allow` / `deny` / `ask`；可与 `Read` / `Edit` / `WebFetch` / `Bash` 等规则组合。项目目录外默认偏保守（常为 Ask）。

**Read / Edit**：gitignore 风格路径；支持绝对路径、`~/`、`./` 相对路径。

**WebFetch**：`WebFetch(domain:example.com)`

**Bash**：精确或前缀匹配，如 `Bash(npm run build)`、`Bash(npm run test:*)`。

---

## 9. Worktree（并行任务）

依赖本机可用 **Git**。

| 命令 | 作用 |
| :--- | :--- |
| `qodercli --worktree "任务描述"` | 新建并进入 worktree 任务（默认进容器内 TUI） |
| `qodercli jobs --worktree` | 列出任务 |
| `qodercli rm <jobId>` | 删除任务（不可恢复） |

可选：`-p` 非交互跑完即停；`--branch` 指定分支；其余 Agent 参数会透传。

---

## 10. Memory（`AGENTS.md`）

加载位置：

```
~/.qoder/AGENTS.md          # 用户级，所有项目
${project}/AGENTS.md       # 项目级
```

* `/init`：自动生成/更新项目 `AGENTS.md`  
* TUI 内 `#`：记忆编辑模式  
* `/memory`：选用户级或项目级记忆文件  

---

## 11. Subagent

定义文件：

* `~/.qoder/agents/<name>.md`（用户级）  
* `${project}/agents/<name>.md`（项目级）  

需含 **frontmatter**：`name`、`description`、`tools`，正文为 system prompt。

创建：`/agents` → Tab 选 User/Project → Create new agent。

使用：TUI 内 `/agent` 查看；可显式写「使用 xxx subagent」或依赖模型隐式调度、多步串联。

---

## 12. 自定义斜杠命令（`.md`）

路径：

* `~/.qoder/commands/*.md`（用户级）  
* `${project}/.qoder/commands/*.md`（项目级）  

示例文件名 `quest.md`：frontmatter 里 `description`，正文为要执行的提示词；TUI 内输入 `/quest` 触发。

---

## 14. 模型管理

### 模型分类

Qoder CLI 提供 **三大类模型**：

| 类别 | 说明 | 适用场景 |
|------|------|----------|
| **分级模型** (Tiered) | 5 个等级，混合模型策略 | 日常使用（默认） |
| **前沿模型** (Frontier) | 最新 SOTA，限时免费 | 体验最新能力 |
| **自定义模型** (Custom) | 连接自己的 provider | 个人付费账户专享 |

### 分级模型详情

| 等级 | Credit 消耗 | 适用场景 |
|------|-----------|----------|
| `lite` | 免费 | 简单问答、轻量任务 |
| `efficient` | 低 | 日常编码、代码补全 |
| `auto` | 标准 | 复杂任务、多步推理（**默认**） |
| `performance` | 高 | 棘手工程问题、大代码库 |
| `ultimate` | 最高 | 极致性能、最佳结果 |

### 切换模型

```bash
# 命令行指定（仅当前会话，不持久化）
qodercli --model lite
qodercli --model efficient
qodercli --model auto
qodercli --model performance
qodercli --model ultimate

# TUI 内永久切换（配置保存到 ~/.qoder.json）
qodercli
# 然后输入 /model，↑↓选择，Enter 确认
```

### 检查当前模型

```bash
# 方法 1: TUI 内查看
qodercli
# 输入 /model 查看当前选中的模型等级

# 方法 2: 查看配置文件
cat ~/.qoder/settings.json | grep -i model

# 方法 3: 查看账户与 Credits 状态
qodercli /usage
```

### 添加自定义模型

1. TUI 内输入 `/model`
2. 切换到 **Custom** 标签页
3. 选择 `Add custom model...`
4. 按提示选择 Provider → Model Type → Model
5. 输入 API key 并完成验证

**注意**：自定义模型需个人付费账户（Pro/Pro+/Ultra），Teams 账户不支持。

---

## 15. 速查

* 完整索引：<https://docs.qoder.com/llms.txt>  
* 自动化优先用 **Print / `-p`**，避免在无 TTY 环境强开 TUI。  
