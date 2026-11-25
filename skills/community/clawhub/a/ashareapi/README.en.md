<div align="center">

<a href="https://ashareapi.com/en/"><img src="https://ashareapi.com/icon-512.png" width="88" height="88" alt="ashareapi"></a>

# ashareapi — Official Agent Skill for the A-Share Data API

Drop it into a skills directory an AI Agent client reads (**the common one**: `~/.claude/skills/ashareapi/` — read by Claude Code / opencode / Cursor / Antigravity / DeepSeek Harness; other clients are listed under "Client directories" below), and the AI Agent immediately knows how to fetch A-share data: which endpoint to call, how to fill the parameters, what unit each field is in, and what to do on errors — **no prompting, no doc reading, no made-up numbers**. Covers **102 endpoints / 94 MCP tools**; the free endpoints need no key at all.

![version](https://img.shields.io/badge/skill-0.3.1-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Works with 45+ agent clients** (open-standard Agent Skills) — mainstream clients work out of the box:

![Claude Code](https://img.shields.io/badge/Claude%20Code-supported-D97757?logo=claude&logoColor=white)
![Cursor](https://img.shields.io/badge/Cursor-supported-000000?logo=cursor&logoColor=white)
![Codex](https://img.shields.io/badge/Codex-supported-000000)
![opencode](https://img.shields.io/badge/opencode-supported-211E1E?logo=opencode&logoColor=white)
![VS Code / GitHub Copilot](https://img.shields.io/badge/VS%20Code%20%2F%20Copilot-supported-007ACC?logo=githubcopilot&logoColor=white)
![Antigravity (Google)](https://img.shields.io/badge/Antigravity%20%28Google%29-supported-4285F4?logo=google&logoColor=white)
![DeepSeek](https://img.shields.io/badge/DeepSeek-supported-4D6BFE?logo=deepseek&logoColor=white)
![WorkBuddy](https://img.shields.io/badge/WorkBuddy-supported-4B6BFB)

[中文](README.md) · **English**

[Website](https://ashareapi.com/en/) · [Docs](https://ashareapi.com/en/docs/) · [Endpoint list](https://ashareapi.com/en/endpoints/) · [MCP](https://ashareapi.com/en/mcp/) · [Changelog](https://ashareapi.com/en/changelog/)

[Source](https://github.com/ashareapi/ashareapi-skill) · [Issues](https://github.com/ashareapi/ashareapi-skill/issues)

</div>

---

## What this is

An **A-share data Agent Skill**: a set of operating instructions written for an AI Agent, plus reference documents loaded on demand. Once installed, when the agent answers questions like "how much is this stock right now" or "screen for stocks with PE<20 and ROE>15", it **knows which endpoint to call and how to read the response** — instead of making things up.

**10 endpoints need no key** (usable right after installation — 7 data endpoints + 1 doc search + 2 utility endpoints): `/v1/quote` · `/v1/kline` · `/v1/hot` · `/v1/market-overview` · `/v1/changedist` · `/v1/models` · `/v1/trade-calendar` · `/v1/wiki` · `/v1/health` · `/v1/challenge`. The rest need a key ([get one](https://ashareapi.com/en/pricing/) from ¥9.9).

## Why use it

- **It ships a decision tree**: the agent finds the endpoint by task ("how much now" → `quote`; "recent trend" → `kline`; "which sectors are rising" → `sector`)
- **All four must-know semantics are spelled out**: units (lots / yuan / percent) · numbers are strings · date formats · response structures — without these, whatever the AI Agent computes is wrong
- **Errors and rate limits are covered too**: the difference between 401 / 429 / `ok:false` / empty results, and how to raise your quota when the anonymous limit is hit
- **Intraday data is never cached**: every call fetches fresh · `minute` gives 242 points for the day · `auction` covers 9:15–9:25 (about 150 points)
- **10 years of K-line history**: from 2016-08-08; `kline-full` returns all of it at once (about 2,500 bars); daily / weekly / monthly / quarterly / yearly plus `m1`–`m120`
- **Whole market in one call**: `market-kline` returns every A-share (5,000+) for one trading day — no 5,000-request loop
- **L2 microstructure, 7 endpoints**: market-wide net-flow ranking with **5,568 stocks in one call** · Dragon-Tiger seats down to **broker-branch level** · large-order four directions / order-queue add-cancel / 100-day history
- **Batch endpoints, 9 of them**: quote / K-line / snapshot / financials / technical / chip / shareholders / money flow / company profile — **150 stocks in about 2 seconds**
- **One key, five markets**: A-shares + on-exchange ETFs (1,716) + Hong Kong + US + futures & forex (65 instruments)
- **Quant in one place**: 87 factors + 29 strategies + 25 playbooks + backtests (single / portfolio / batch) + portfolio weight optimisation
- **No charge on failures**: empty results, fetch failures, wrong codes — none of these are billed (billing counts actual returned rows only)
- **10 endpoints need no key**: `quote` / `kline` / `hot` / `market-overview` / `changedist` / `models` / `trade-calendar` / `wiki` + `health` / `challenge`
- **Automatic source failover**: 70 data sources back each other up; if one has a problem it switches to the next, and **your quota is not charged**
- **No data ≠ failure**: "the market genuinely has no data" (e.g. a suspended stock) is returned separately from "the fetch failed" — the agent will not mistake a suspension for an outage
- **Fixed conventions, no post-processing**: K-lines are always **forward-adjusted (qfq)** (there is no `adjust` parameter), so there is no double-adjustment
- **Code format is forgiving**: `sh600667` / `600667.SH` / `600667` all work (normalised automatically)
- **Pure files, no server**: copy one folder into your skills directory — no URL to configure, no service to start
- **Loaded on demand, so it does not eat context**: the 4 reference files are read only when needed, not dumped into the AI Agent all at once

## Installation

**① Hand it to the AI Agent** (the easiest — copy this line and send it):

> Please install this ashareapi Agent Skill for me: download `https://ashareapi.com/ashareapi-skill.zip` and extract it into the client's skills directory (e.g. `~/.claude/skills/`). When done, confirm the directory contains `ashareapi/SKILL.md` and `ashareapi/references/`.

**② One command** (macOS / Linux / WSL — replace `~/.claude/skills` with your client's directory):

```bash
mkdir -p ~/.claude/skills && cd ~/.claude/skills && curl -sL https://ashareapi.com/ashareapi-skill.zip -o s.zip && unzip -oq s.zip && rm s.zip
```

Windows (PowerShell):

```powershell
iwr https://ashareapi.com/ashareapi-skill.zip -OutFile s.zip; Expand-Archive s.zip -DestinationPath "$env:USERPROFILE\.claude\skills" -Force; rm s.zip
```

**③ Manually**: download the zip from <https://ashareapi.com/en/skill/> and extract it into your skills directory:

```bash
unzip ashareapi-skill.zip -d ~/.claude/skills/     # Claude Code
```

**Restart your client after installing.** You can also clone this repo and put `SKILL.md` plus `references/` into `skills/ashareapi/`.

### Client directories

**8 mainstream clients** (paths checked against official docs):

| Client | Global (all projects) | In-project (committed to git) |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| opencode | `~/.config/opencode/skills/` | `.opencode/skills/` |
| Cursor | `~/.claude/skills/` | `.cursor/skills/` |
| Codex (OpenAI) | `~/.codex/skills/` | `.codex/skills/` |
| Antigravity (Google) | `~/.gemini/antigravity/skills/` | `.agents/skills/` |
| VS Code / GitHub Copilot | `~/.copilot/skills/` | `.github/skills/` |
| WorkBuddy | — | `.workbuddy/skills/` |
| DeepSeek Harness | `~/.dsh/skills/` | `.dsh/skills/` |

> Not sure which one to use? `.claude/skills/` and `.agents/skills/` are "universal directories" that Claude Code / opencode / Cursor / Antigravity / DeepSeek Harness can all read.

**The other 40 clients** (installation paths follow each vendor's official docs):

Junie (JetBrains) · OpenHands · Goose (Block) · Amp · Kiro (AWS) · TRAE · Command Code · Roo Code · Cline · Factory (Droids) · Deep Code · Mistral AI Vibe · Letta · Mux (Coder) · Emdash · OpenClaw · Hermes Agent · Qodo · Tabnine · Snowflake Cortex Code · Databricks Genie Code · Spring AI · Laravel Boost · Pulumi Neo · Superconductor · Ona · pi · VT Code · fast-agent · bub · nanobot · ZeroClaw · Autohand Code CLI · Firebender · Vita · Agentman · Workshop · Piebald · Google AI Edge Gallery · Claude (claude.ai)

> Full list with per-vendor doc links: <https://agentskills.io/clients>

## Contents

| File | Description |
|---|---|
| [`SKILL.md`](SKILL.md) | Main entry: how to decide whether a key is needed · finding the endpoint by task (decision tree) · the four must-know semantics · errors and rate limits |
| [`references/endpoints.md`](references/endpoints.md) | **Complete parameters and response fields** for all 102 endpoints |
| [`references/fields.md`](references/fields.md) | Field units and meanings (**read before doing any arithmetic**) |
| [`references/errors.md`](references/errors.md) | Handling 401 / 429 / `ok:false` / empty results |
| [`references/sdk.md`](references/sdk.md) | Read this when you need to write Python / Node.js code |

## Version

**Current version: `0.3.1`** — version history and how to update: see [`SKILL.md`](SKILL.md) §9.

> ⚠️ **The API itself never needs updating** — endpoints are always current (the service evolves server-side); what needs updating is **this skill's reference files**.

## Related

**Official SDKs**: Python `pip install ashareapi` · Node.js / TypeScript `npm install ashareapi`

**MCP server**: `https://api.ashareapi.com/mcp` ([configuration guide](https://ashareapi.com/en/mcp/))

## License

MIT · Data is for research reference only and is not investment advice
