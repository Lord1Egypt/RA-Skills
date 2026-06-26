---
name: clawheart-security
description: 让 AI Agent 在对话框里直接驱动本机 ClawHeart 的安全审计、技能鉴定、Agent 凭据治理。当用户问"扫一下 AI 安全"或类似意图时调用 `clawheart` CLI。
version: 1.0.0
category: [安全, AI 治理, 工具]
recommendedModels:
  - claude-opus-4-7
  - claude-sonnet-4-6
  - gpt-5.4-thinking
examples:
  - 帮我扫一下 AI 安全风险
  - 检查我的技能里有没有恶意的
  - 列出本机的 AI Agent
  - 看一下 ClawHeart 整机状态
  - 哪些 Provider 配置了
---

# ClawHeart 安全助手

你可以通过 `clawheart` 命令行调用本机 ClawHeart 服务做 AI 安全审计、技能鉴定、Agent 凭据治理。

> 前置：用户机器需要安装 ClawHeart CLI（`clawheart-cli` 或 `clawheart`，PATH 中可执行）。
> 若 `which clawheart` 失败，引导用户访问 https://clawheart.live 下载，或跑 `curl -fsSL clawheart.live/install.sh | sh`。

## 触发条件 → 命令映射

| 用户意图（关键词举例） | 命令 |
|---|---|
| "扫描安全 / AI 风险 / 检查我的配置" | `clawheart scan --json` |
| "看看本地的技能 / SKILL.md / Agent 装了什么" | `clawheart skills list --json` |
| "技能有恶意吗 / 鉴定一下技能" | `clawheart skills scan --all --json` |
| "我装了哪些 Agent / Claude / Codex / Cursor 在哪" | `clawheart agents list --json` |
| "MCP server 有哪些" | `clawheart agents mcp --json` |
| "我的 Provider / API key 配置" | `clawheart providers list --json` |
| "ClawHeart 整机状态 / 代理在跑吗" | `clawheart status --json` |
| "引导我设置 / 第一次用" | `clawheart init --json` 然后状态机交互 |
| "备份技能 / 打包技能" | `clawheart skills backup --json` |

## 输出解析规范

所有命令返回顶层 JSON：

```json
{ "ok": true,  "data": { ... } }
{ "ok": false, "error": "..." }
```

`data` 的 schema 因命令而异，**用户友好的摘要文本不在 JSON 里** —— 你需要根据 `data` 用自然语言重述。

## 工作流示例

### 扫描

1. 跑 `clawheart scan --json`
2. 从 `data.results` 里筛 `outcome=fail` 的项目
3. 优先告知用户严重问题：
   - 每项给 `id` + `description` + `detail` + `remediation`
4. 然后简单提一句"还有 X 个警告 / Y 项通过 / Z 项跳过"
5. **不要逐项列举 skipped** — 它们多是"未实现"占位，列出来反而让用户疑惑

### 技能鉴定

1. `clawheart skills scan --all --json`
2. 聚焦 `data` 数组中 `blocked: true` 或 `score < 60` 的技能
3. 给用户列出"危险技能" + 建议（一般是用 `clawheart skills backup <id>` 备份后删除）

### Agent 列表

1. `clawheart agents list --json`
2. 把 `data` 数组里每个 Agent 的 `id` + `agent_name` + `config_path` + `mcp_servers` 简洁报给用户

## 不要做的事

- ❌ 不要直接读 `~/.clawheart-v2/` 文件 — 必须通过 CLI
- ❌ 不要替用户输入密码 / API key
- ❌ skipped 项的 "未实现" 状态不要解读为漏洞或问题
- ❌ 不要自己尝试 sudo —— 遇到需要权限的提示直接转告用户

## CLI 不可用时的兜底

若 `clawheart` 命令找不到：

> ClawHeart CLI 似乎没装。访问 https://clawheart.live 下载，或运行：
>
> macOS / Linux：`curl -fsSL https://clawheart.live/install.sh | sh`
>
> Windows：`iwr https://clawheart.live/install.ps1 -useb | iex`

## 完整命令清单

```
clawheart scan [--category=<C>] [--ids=<ID,...>] [--json]
clawheart skills {list,scan <id>|--all,backup [<ids>]} [--json]
clawheart agents {list,mcp [--agent=<id>],rescan} [--json]
clawheart providers {list,add,import,overwrite <id>} [--json]
clawheart status [--json]
clawheart init [--reset] [--json]
clawheart --version
```
