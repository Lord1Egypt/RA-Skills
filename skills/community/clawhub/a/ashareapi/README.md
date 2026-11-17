<div align="center">

<a href="https://ashareapi.com"><img src="https://ashareapi.com/icon-512.png" width="88" height="88" alt="ashareapi"></a>

# ashareapi — A股数据 API 官方 Agent Skill

给 **AI Agent** 读的 A 股接口说明书 —— 装进 skills 目录即用：Agent 由此知道**该调哪个端点、参数怎么填、字段什么单位、错了怎么处理**（40 个端点 / 31 个 MCP 工具）。

![version](https://img.shields.io/badge/skill-0.2.8-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**支持 45+ 家 Agent 客户端**（开放标准 Agent Skills）—— 主流客户端开箱即用：

![Claude Code](https://img.shields.io/badge/Claude%20Code-supported-D97757?logo=claude&logoColor=white)
![Cursor](https://img.shields.io/badge/Cursor-supported-000000?logo=cursor&logoColor=white)
![Codex](https://img.shields.io/badge/Codex-supported-000000)
![opencode](https://img.shields.io/badge/opencode-supported-211E1E?logo=opencode&logoColor=white)
![VS Code / GitHub Copilot](https://img.shields.io/badge/VS%20Code%20%2F%20Copilot-supported-007ACC?logo=githubcopilot&logoColor=white)
![Antigravity (Google)](https://img.shields.io/badge/Antigravity%20%28Google%29-supported-4285F4?logo=google&logoColor=white)
![DeepSeek](https://img.shields.io/badge/DeepSeek-supported-4D6BFE?logo=deepseek&logoColor=white)
![WorkBuddy](https://img.shields.io/badge/WorkBuddy-supported-4B6BFB)

**中文** · [English](README.en.md)

[官网](https://ashareapi.com) · [文档](https://ashareapi.com/docs/) · [端点清单](https://ashareapi.com/endpoints/) · [MCP 接入](https://ashareapi.com/mcp) · [更新日志](https://ashareapi.com/changelog)

[GitHub 源码](https://github.com/ashareapi/ashareapi-skill) · [问题反馈 Issues](https://github.com/ashareapi/ashareapi-skill/issues)

</div>

---

## 这是什么

一份 **A股数据 Agent Skill**：一段写给 AI Agent 的操作说明 + 按需加载的参考文档。装好之后，Agent 在回答"某只股票现在多少钱""帮我筛 PE<20 且 ROE>15 的股票"这类问题时，会**知道去调哪个端点、怎么读返回值**，而不是凭印象编。

**5 个端点无需 Key**（装上就能调）：`/v1/quote` · `/v1/kline` · `/v1/hot` · `/v1/market-overview` · `/v1/changedist`。其余端点需要 Key（[获取](https://ashareapi.com/pricing)，¥9.9 起）。

## 为什么用它

- **给 AI「知识」，不是「工具」**：MCP 让 Agent 自己去调工具；Skill 让 Agent **知道**该调哪个端点、字段什么单位、出错怎么办。两者并列，可以同时装
- **有决策树**：Agent 按任务找端点（「现在多少钱」→ `quote`；「最近走势」→ `kline`；「哪些板块在涨」→ `sector`）
- **四个必知语义写全**：单位（手 / 元 / 百分数）· 数字是字符串 · 日期格式 · 返回结构 —— 不写这些，AI 算出来就是错的
- **错误与限流也写了**：401 / 429 / `ok:false` / 空结果的区别，以及匿名超限怎么提额
- **按需加载，不占上下文**：4 个参考文件用到才读，不一次性灌给 AI
- **纯文件，没有服务端**：一个文件夹复制进 skills 目录就行 —— 不用配 URL、不用起服务

## 安装

**① 交给你的 AI Agent**（最省事 —— 复制这句话发给它）：

> 帮我安装 ashareapi 这个 Agent Skill：把 `https://ashareapi.com/ashareapi-skill.zip` 下载并解压到你的 skills 目录（例如 `~/.claude/skills/`），装好后确认目录里是 `ashareapi/SKILL.md` 和 `ashareapi/references/`。

**② 一条命令**（macOS / Linux / WSL —— 把 `~/.claude/skills` 换成你客户端的目录）：

```bash
mkdir -p ~/.claude/skills && cd ~/.claude/skills && curl -sL https://ashareapi.com/ashareapi-skill.zip -o s.zip && unzip -oq s.zip && rm s.zip
```

Windows（PowerShell）：

```powershell
iwr https://ashareapi.com/ashareapi-skill.zip -OutFile s.zip; Expand-Archive s.zip -DestinationPath "$env:USERPROFILE\.claude\skills" -Force; rm s.zip
```

**③ 手动**：在 <https://ashareapi.com/skill> 下载 zip，解压到 skills 目录：

```bash
unzip ashareapi-skill.zip -d ~/.claude/skills/     # Claude Code
```

**装完重启客户端**。也可以直接 clone 本仓，把 `SKILL.md` 与 `references/` 放进 `skills/ashareapi/`。

### 客户端目录

**8 家主流客户端**（路径已核对官方文档）：

| 客户端 | 全局（所有项目） | 项目内（提交 git） |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| opencode | `~/.config/opencode/skills/` | `.opencode/skills/` |
| Cursor | `~/.claude/skills/` | `.cursor/skills/` |
| Codex (OpenAI) | `~/.codex/skills/` | `.codex/skills/` |
| Antigravity (Google) | `~/.gemini/antigravity/skills/` | `.agents/skills/` |
| VS Code / GitHub Copilot | `~/.copilot/skills/` | `.github/skills/` |
| WorkBuddy | — | `.workbuddy/skills/` |
| DeepSeek Harness | `~/.dsh/skills/` | `.dsh/skills/` |

> 不确定用哪个？`.claude/skills/` 与 `.agents/skills/` 是「通用目录」，Claude Code / opencode / Cursor / Antigravity / DeepSeek Harness 都能读到。

**其余 40 家**（安装路径以各家官方文档为准）：

Junie (JetBrains) · OpenHands · Goose (Block) · Amp · Kiro (AWS) · TRAE (字节) · Command Code · Roo Code · Cline · Factory (Droids) · Deep Code · Mistral AI Vibe · Letta · Mux (Coder) · Emdash · OpenClaw · Hermes Agent · Qodo · Tabnine · Snowflake Cortex Code · Databricks Genie Code · Spring AI · Laravel Boost · Pulumi Neo · Superconductor · Ona · pi · VT Code · fast-agent · bub · nanobot · ZeroClaw · Autohand Code CLI · Firebender · Vita · Agentman · Workshop · Piebald · Google AI Edge Gallery · Claude (claude.ai)

> 完整名单与各家文档链接：<https://agentskills.io/clients>

## 内容

| 文件 | 说明 |
|---|---|
| [`SKILL.md`](SKILL.md) | 主入口：怎么判断要不要 Key · 按任务找端点（决策树）· 四个必知语义 · 错误与限流 |
| [`references/endpoints.md`](references/endpoints.md) | 40 个端点的**完整参数与返回字段** |
| [`references/fields.md`](references/fields.md) | 字段单位与含义（**算数前必读**）|
| [`references/errors.md`](references/errors.md) | 401 / 429 / `ok:false` / 空结果的处理 |
| [`references/sdk.md`](references/sdk.md) | 要写 Python / Node.js 代码时看 |

## 版本

**当前版本：`0.2.8`** —— 版本记录与更新方法见 [`SKILL.md`](SKILL.md) §九。

> ⚠️ **API 本身不需要更新** —— 端点永远是最新的（服务端演进）；需要更新的是**这份说明**。

## 相关

**官方 SDK**：Python `pip install ashareapi` · Node.js / TypeScript `npm install ashareapi`

**MCP 服务器**：`https://api.ashareapi.com/mcp`（[配置说明](https://ashareapi.com/mcp)）

## License

MIT · 数据仅供研究参考，不构成投资建议
