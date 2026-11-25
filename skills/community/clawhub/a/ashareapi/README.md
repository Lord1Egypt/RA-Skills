<div align="center">

<a href="https://ashareapi.com"><img src="https://ashareapi.com/icon-512.png" width="88" height="88" alt="ashareapi"></a>

# ashareapi — A股数据 API 官方 Agent Skill

装进 AI Agent 客户端能读到的 skills 目录（**通用位置**：`~/.claude/skills/ashareapi/`，Claude Code / opencode / Cursor / Antigravity / DeepSeek Harness 都能读；其余客户端见下方「客户端目录」），AI Agent 立刻知道怎么取 A 股数据：该调哪个端点、参数怎么填、字段什么单位、出错怎么办 —— **不用教它、不用翻文档、不会编数字**。覆盖 **102 个端点 / 94 个 MCP 工具**，免费端点连 Key 都不用。

![version](https://img.shields.io/badge/skill-0.3.1-blue)
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

**10 个端点无需 Key**（装上就能调，7 个数据端点 + 1 个文档检索 + 2 个工具端点）：`/v1/quote` · `/v1/kline` · `/v1/hot` · `/v1/market-overview` · `/v1/changedist` · `/v1/models` · `/v1/trade-calendar` · `/v1/wiki` · `/v1/health` · `/v1/challenge`。其余端点需要 Key（[获取](https://ashareapi.com/pricing)，¥9.9 起）。

## 为什么用它

- **有决策树，Agent 不用猜**：按任务直接找端点（「现在多少钱」→ `quote`；「最近走势」→ `kline`；「哪些板块在涨」→ `sector`）
- **四个必知语义写全**：单位（手 / 元 / 百分数）· 数字是字符串 · 日期格式 · 返回结构 —— 不写这些，AI Agent 算出来就是错的
- **错误与限流也写了**：401 / 429 / `ok:false` / 空结果的区别，以及匿名超限怎么提额
- **盘中数据不缓存**：每次调用都重新取 · `minute` 分时（当日 242 点）· `auction` 集合竞价分时（9:15–9:25，约 150 点）
- **K 线 10 年历史**：2016-08-08 起，`kline-full` 一次拿全（约 2,500 根）；日 / 周 / 月 / 季 / 年 + 分钟线 `m1`–`m120`
- **全市场一次拿**：`market-kline` 一次返回某交易日**全部 A 股（5,000+ 只）**的日线 —— 不用循环 5,000 次
- **L2 微观结构 7 个端点**：全市场主力净额榜**一次 5,568 只** · 龙虎榜席位穿透到**营业部级** · 大单四方向 / 挂撤单队列 / 100 日历史大单
- **批量端点 9 个**：行情 / K 线 / 快照 / 财务 / 技术 / 筹码 / 股东 / 资金流 / 公司简况，**一次 150 只约 2 秒**
- **一个 Key 覆盖 5 个市场**：A 股 + 场内 ETF（1,716 只）+ 港股 + 美股 + 期货外汇（65 个品种）
- **量化五位一体**：87 因子 + 29 策略 + 25 方法论 + 回测（单标的 / 组合 / 批量）+ 组合权重优化
- **不该扣的就不扣**：空结果、取数失败、代码传错 —— 都**不计费**（按实际返回只数计）
- **10 个端点免 Key**：`quote` / `kline` / `hot` / `market-overview` / `changedist` / `models` / `trade-calendar` / `wiki` + `health` / `challenge`
- **多源自动切换**：70 个数据源互为备份，某个源出问题会自动换下一个，且**不扣调用次数**
- **无数据 ≠ 失败**：停牌这类「市场真没数据」和「取数失败」分开返回 —— Agent 不会把停牌误判成故障
- **口径固定，不用二次处理**：K 线固定**前复权**（没有 `adjust` 参数），不会二次复权
- **代码格式容错**：`sh600667` / `600667.SH` / `600667` 都认（自动补市场前缀）
- **纯文件，零服务**：一个文件夹复制进 skills 目录即可 —— 不用配 URL、不用起服务
- **按需加载，不占上下文**：4 个参考文件用到才读，不一次性灌给 AI Agent

## 安装

**① 交给 AI Agent**（最省事 —— 复制这句话发给它）：

> 帮我安装 ashareapi 这个 Agent Skill：把 `https://ashareapi.com/ashareapi-skill.zip` 下载并解压到客户端的 skills 目录（例如 `~/.claude/skills/`），装好后确认目录里是 `ashareapi/SKILL.md` 和 `ashareapi/references/`。

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
| [`references/endpoints.md`](references/endpoints.md) | 102 个端点的**完整参数与返回字段** |
| [`references/fields.md`](references/fields.md) | 字段单位与含义（**算数前必读**）|
| [`references/errors.md`](references/errors.md) | 401 / 429 / `ok:false` / 空结果的处理 |
| [`references/sdk.md`](references/sdk.md) | 要写 Python / Node.js 代码时看 |

## 版本

**当前版本：`0.3.1`** —— 版本记录与更新方法见 [`SKILL.md`](SKILL.md) §九。

> ⚠️ **API 本身不需要更新** —— 端点永远是最新的（服务端演进）；需要更新的是**这份说明**。

## 相关

**官方 SDK**：Python `pip install ashareapi` · Node.js / TypeScript `npm install ashareapi`

**MCP 服务器**：`https://api.ashareapi.com/mcp`（[配置说明](https://ashareapi.com/mcp)）

## License

MIT · 数据仅供研究参考，不构成投资建议
