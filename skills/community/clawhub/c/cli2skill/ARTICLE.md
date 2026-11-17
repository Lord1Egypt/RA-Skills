# MCP 进程泄漏把我 32GB 系统搞死了——为什么 CLI+Skill 才是 Agent 工具的正确姿势

> "Software as a tool 结论是别用 MCP... 这玩意是我们拿去忽悠子刊审稿人用的"
> —— 某大厂 RL 团队工程师的非公开评论

## TL;DR

MCP (Model Context Protocol) 在单机 AI 编码场景下是过度工程。每个 MCP server 在 Windows 上需要 `cmd → uv → python` 三层进程套娃，session 断开时不回收，积累几轮后吃光系统 commit charge，fork 直接炸。

**替代方案**：把工具写成 CLI，用 Agent Skill（一个 markdown 文件）教 agent 怎么调。零常驻进程，跨 Claude Code / Codex / Gemini CLI / Cursor 通用。

本文附带 `cli2skill` 工具——一行命令把任意 CLI 变成 Agent Skill。

---

## 血案现场

2026 年 3 月 24 日晚，我的开发机（RTX 5090 + 32GB RAM，Windows 11）突然无法 fork 新进程：

```
dofork: child -1 - forked process died unexpectedly, exit code 0xC000012D
bash: fork: retry: Resource temporarily unavailable
```

`0xC000012D` = `STATUS_COMMITMENT_LIMIT`，Windows 虚拟内存 commit charge 耗尽。

排查发现 **400+ 进程**在跑，罪魁祸首：

| 进程 | 数量 | 来源 |
|------|------|------|
| node | 46 | MCP server 僵尸 |
| python | 39 | MCP server 僵尸 |
| cmd | 37 | MCP 启动器壳 |
| uv/uvx | 36 | Python MCP launcher（应该跑完就退！） |
| bash | 30 | fork 残留 |
| conhost | 26 | 每个 shell 一个 |

我配了 ~15 个 MCP server（memU、PageIndex、GitNexus、Obsidian、Context7、Memorix...），每次 Claude Code session 重连就 spawn 一套新进程，旧的不杀。5-10 轮 session 后系统就满了。

**已提交 bug report**: [anthropics/claude-code#38228](https://github.com/anthropics/claude-code/issues/38228)

---

## MCP 的问题不只是进程泄漏

进程泄漏是实现 bug，会修。但 MCP 在单机开发场景有更深层的架构问题：

### 1. 进程开销不对称

一个 MCP server 在 Windows 上的进程树：
```
cmd.exe (shell wrapper)
  └── uv.exe (Python launcher)
       └── python.exe (MCP server)
```

3 个常驻进程，只为了提供 2-3 个工具调用。15 个 MCP server = 45+ 常驻进程。

CLI 方式：agent 需要时 spawn 1 个 python 进程，跑完退出。**0 常驻进程。**

### 2. 协议开销 vs 实际收益

MCP 用 JSON-RPC over stdio/HTTP，有 capability negotiation、tool discovery、resource listing 等完整生命周期。这在多 client 共享 server 的企业场景有意义。

但单机开发？你的 agent 是唯一 client，tool 列表写在 SKILL.md 里就行。`--help` 就是 tool discovery。stdout 就是 response。

### 3. 调试地狱

MCP server 报错时，你面对的是：
- stdio pipe 的 JSON-RPC 错误
- 被 Claude Code 封装过的错误消息
- 三层进程中任何一层可能挂掉

CLI 报错？直接看 stderr。

---

## CLI + Skill 模式

### 核心思想

```
MCP 模式:  Agent --JSON-RPC--> MCP Server (常驻) --API--> Backend
CLI 模式:  Agent --Bash tool--> CLI (按需) --API--> Backend
```

Agent Skill（`.claude/skills/xxx.md`）是一个 markdown 文件，教 agent：
1. 这个 CLI 能做什么
2. 怎么调用（命令 + 参数）
3. 什么时候该用

26+ 平台已支持 Agent Skills 规范：Claude Code、Codex CLI、Gemini CLI、Cursor、Copilot、VS Code...

### 实际迁移案例

我把 4 个 MCP server 迁移到了 CLI + Skill：

| 工具 | 之前 (MCP) | 之后 (CLI) | 常驻进程 |
|------|-----------|-----------|---------|
| memU (记忆检索) | uv→python MCP server | `python memu-cli.py search "query"` | 3 → 0 |
| PageIndex (文档搜索) | python MCP server | `python pageindex-cli.py search "query"` | 1 → 0 |
| GitNexus (代码图谱) | node MCP server | `gitnexus query "query"` (已有 CLI) | 1 → 0 |
| Obsidian (笔记) | node MCP server | `python obsidian-cli.py read "path"` | 1 → 0 |

**结果：减少 12-15 个常驻进程，功能完全相同。**

---

## cli2skill：一行命令把 CLI 变成 Agent Skill

### 安装

```bash
pip install cli2skill
# 或
pipx install cli2skill
```

### 使用

```bash
# 从 --help 解析
cli2skill generate mytool --parse-help

# 从 Typer/Click introspection
cli2skill generate mytool --framework typer

# 指定输出目录
cli2skill generate mytool --output ~/.claude/skills/
```

### 生成结果

```markdown
---
name: mytool
description: Auto-generated skill for mytool CLI
user-invocable: false
allowed-tools: Bash(mytool *)
---

# mytool

## Commands

\`\`\`bash
mytool subcommand1 <arg> [--flag]
mytool subcommand2 <arg>
\`\`\`

## When to use
- [从 --help description 提取]
```

### 支持的框架

| 框架 | 语言 | 解析方式 |
|------|------|---------|
| Typer / Click | Python | Introspection API (最精确) |
| argparse | Python | --help 解析 |
| clap (derive) | Rust | --help 解析 |
| Commander.js | TypeScript | --help 解析 |
| 任意 CLI | 任意 | --help 解析 (通用) |

---

## 什么时候该用 MCP

MCP 不是废物，在这些场景仍然合理：

1. **需要持久化状态的工具**（浏览器自动化、数据库连接池）
2. **多 client 共享的服务**（团队共享的 tool server）
3. **流式通知**（server → client 推送，CLI 做不到）
4. **远程 HTTP MCP**（不需要本地进程，如 Slack/GitHub/Notion 的官方 MCP）

如果你的工具是"调用 → 返回结果"模式，CLI + Skill 永远是更好的选择。

---

## FAQ

**Q: Agent 怎么知道什么时候用我的 CLI？**
A: Skill 文件的 `description` 字段 + 正文中的 "When to use" 部分。Agent 自动匹配。

**Q: 性能不会更差吗？每次都要 spawn 进程。**
A: Python CLI 冷启动 ~50ms，Node CLI ~30ms。MCP 的 JSON-RPC roundtrip 也不是零。实际差异可忽略。

**Q: 我用的 MCP server 是别人写的，没有 CLI。**
A: `cli2skill` 支持 `--wrap-mcp` 模式——生成一个 thin CLI wrapper 来调用现有 MCP server 的 HTTP endpoint，然后禁用 MCP auto-spawn。

---

## 引用

- [Agent Skills Specification](https://agentskills.io/specification) — Anthropic, 2025-12 (26+ 平台采纳)
- [Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) — Anthropic, 2025-11 (**直接 MCP tool call → code execution 省 98.7% token**)
- [Equipping Agents with Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills) — Anthropic, 2025-10
- [Skills vs Dynamic MCP Loadouts](https://lucumr.pocoo.org/2025/12/13/skills-vs-mcp/) — Armin Ronacher (Flask 作者)
- [Anthropic Downplays MCPs](https://danielmiessler.com/blog/anthropic-downplays-mcps) — Daniel Miessler
- [CLI-Anything: Making ALL Software Agent-Native](https://github.com/HKUDS/CLI-Anything) — HKU, 2026-03 (22.3k stars)
- [ToolMaker: LLM Agents Making Agent Tools](https://arxiv.org/abs/2502.11705) — arXiv 2025-02
- [Claude Code MCP Process Leak Bug Report](https://github.com/anthropics/claude-code/issues/38228)

---

*作者：[TODO]*
*日期：2026-03-24*
*License: MIT*
