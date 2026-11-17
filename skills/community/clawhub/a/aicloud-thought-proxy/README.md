# 云思客 · AIcloud‑thought‑proxy

> **[🇨🇳 阅读中文版](#中文版-zh) ｜ [🇺🇸 Read in English](#english-version-en)**

**云思客** 是一个 AI Agent 技能（Skill），通过操控你的浏览器打开指定 AI 的**网页版对话**，让网页版 AI 承担「规划步骤 / 编写代码 / 逻辑推理」等思维型工作，本地 Agent 承担「扒取代码、创建文件、运行脚本、下载资源、联网搜索」等执行型工作——从而把推理成本转移到网页版（免费额度 / 订阅会员），**节省 API tokens**。

**AIcloud‑thought‑proxy** is an AI Agent Skill that drives your browser to open a target AI's **web chat UI**, letting the web AI handle the "thinking" work (planning steps / writing code / logical reasoning) while the local Agent handles the "doing" work (scraping code, creating files, running scripts, downloading assets, web searching) — shifting inference cost onto the web tier (free quota / subscriptions) and **saving API tokens**.

<table>
<tr><th>🇨🇳 中文</th><th>🇺🇸 English</th></tr>
<tr>
<td>

- [中文版](#中文版-zh)
  - [概述](#概述-zh)
  - [核心特性](#核心特性-zh)
  - [支持哪些网页版 AI](#支持哪些网页版-ai-zh)
  - [工作原理（工作流）](#工作原理工作流-zh)
  - [浏览器内核检测](#浏览器内核检测-zh)
  - [操控工具安装（缺失时）](#操控工具安装缺失时-zh)
  - [安全与原则](#安全与原则-zh)
  - [支持的平台](#支持的平台-zh)
  - [如何安装本技能](#如何安装本技能-zh)
  - [许可证](#许可证-zh)

</td>
<td>

- [English Version](#english-version-en)
  - [Overview](#overview-en)
  - [Key Features](#key-features-en)
  - [Which Web AIs Are Supported](#which-web-ais-are-supported-en)
  - [How It Works (Workflow)](#how-it-works-workflow-en)
  - [Browser Engine Detection](#browser-engine-detection-en)
  - [Installing the Driver Tools (When Missing)](#installing-the-driver-tools-when-missing-en)
  - [Security & Principles](#security--principles-en)
  - [Supported Platforms](#supported-platforms-en)
  - [How to Install This Skill](#how-to-install-this-skill-en)
  - [License](#license-en)

</td>
</tr>
</table>

---

<a id="中文版-zh"></a>
# 中文版 🇨🇳

<a id="概述-zh"></a>
## 概述

云思客解决的核心问题是：**把"思考"外包给网页版 AI，把"执行"留在本地 Agent**。

当你在 WorkBuddy / Codex 这类 Agent 里反复让模型做大量规划、推理、写代码时，tokens 消耗很快。而 DeepSeek、Kimi、豆包、通义千问等网页版 AI 大多有免费额度或低价会员，足够承担"出方案"的工作。

云思客让 Agent 自动打开网页版 AI，你手动登录后，Agent 负责把你的需求转达给网页 AI、再把网页 AI 给出的步骤在本地电脑上执行，全程只消耗网页版的额度，几乎不花 Agent 侧的 tokens。

> 想读同一节的英文说明？→ [Jump to English: Overview](#overview-en)

<a id="核心特性-zh"></a>
## 核心特性

- **自动检测浏览器内核**：首次使用先判断你的默认浏览器是 Chromium 内核（Chrome / Edge / 360 / QQ 等）还是 Gecko 内核（Firefox），再选择对应操控通道。
- **双通道操控**：Chromium → `chrome-mcp` / BrowserSkill；Gecko → GeckoDriver + Marionette。
- **工具缺失自动安装**：若操控工具未安装，会用小白能听懂的语言引导你完成安装（Agent 侧自动装、浏览器侧给你手把手步骤）。
- **模糊语言选模型**：支持「最新模型 / 最强模型 / 专家模式 / 快速模式 / 识图」等口语化描述，自动映射到具体型号与思考模式。
- **语言跟随**：全程使用你当前使用的语言（默认简体中文），发给网页 AI 的消息也用你的语言。
- **安全协作**：绝不代填账号密码、绝不代过人机验证；你始终是「眼睛」，Agent 是「手」。

> 想读同一节的英文说明？→ [Jump to English: Key Features](#key-features-en)

<a id="支持哪些网页版-ai-zh"></a>
## 支持哪些网页版 AI

| 品牌 | 官网对话 URL | 代表型号 | 思考模式 | 联网搜索 |
|---|---|---|---|---|
| DeepSeek | https://chat.deepseek.com | DeepSeek‑V4-flash / V4-Pro | 专家模式 / 快速模式 / 识图 | 支持 |
| Kimi（月之暗面） | https://www.kimi.com | Kimi K2.7 / 探索版 | 思考模式 | 默认联网 |
| 豆包（字节） | https://www.doubao.com | 1.6 / 2.x 系列 | 深度思考 | 支持 |
| 通义千问（阿里） | https://www.qianwen.com （国内）/ https://chat.qwen.ai （国际） | Qwen3.7 / Qwen3.8‑Max 等 | 深度思考 | 支持 |
| 文心一言（百度） | https://wenxin.baidu.com | 文心 4.5 / 5.0 | 深度思考 | 支持 |
| ChatGPT（OpenAI） | https://chatgpt.com | GPT‑4o / o3 / GPT‑5 | 推理模式 | 支持（手动） |
| Claude（Anthropic） | https://claude.ai | Opus / Sonnet / Haiku | 思考 | 支持 |
| Gemini（Google） | https://gemini.google.com | 2.x Pro / Flash | 深度思考 | 默认联网 |
| Grok（xAI） | https://grok.com | Grok 3 / 4 | 思考 | 支持 |
| 智谱清言 | https://chatglm.cn | GLM‑4.5 / 5.2 | 深度思考 | 支持 |
| 腾讯元宝 | https://yuanbao.tencent.com | 混元3 / DeepSeek | 深度思考 | 支持 |
| 讯飞星火 | https://xinghuo.xfyun.cn/desk | 星火 4.0 | 深度思考 | 支持 |

> 想读同一节的英文说明？→ [Jump to English: Which Web AIs](#which-web-ais-are-supported-en)

<a id="工作原理工作流-zh"></a>
## 工作原理（工作流）

```
触发
 └─ 阶段 0：确认语言（跟随用户语言）
 └─ 阶段 1：浏览器内核检测（Chromium? Gecko?）
 └─ 阶段 1.5：操控工具就绪检查，缺失则询问自动安装
 └─ 阶段 2：选择 AI 品牌 / 型号 / 思考模式 / 联网搜索
 └─ 阶段 3：打开网页版 AI → 提示手动登录 → 人机验证 → 纯文本模式
 └─ 阶段 4：发送第一条协作协议消息，建立分工
 └─ 阶段 5：协作循环：转达需求 → 网页 AI 给步骤 → 本地执行 → 反馈闭环
```

**阶段 4 协议消息示例（简体中文）**：

> 我是来自用户电脑中的 AI agent，你负责规划步骤 / 编写代码 / 逻辑推理，我可以根据你的步骤完成扒取代码、创建文件、运行脚本、下载资源、联网搜索等等，而且完全在用户的电脑中，稍后我会给你用户的要求。

> 想读同一节的英文说明？→ [Jump to English: How It Works](#how-it-works-workflow-en)

<a id="浏览器内核检测-zh"></a>
## 浏览器内核检测

运行内置脚本即可检测系统默认浏览器内核；也支持用户手动指定浏览器路径。

```bash
python scripts/detect_browser.py                  # 自动检测默认浏览器
python scripts/detect_browser.py --browser "C:\path\to\firefox.exe"   # 手动指定
```

脚本输出 JSON，关键字段 `engine`：

- `chromium` → 通道 A（Chrome / Edge / 360 / QQ / Brave / Opera 等）
- `gecko` → 通道 B（Firefox 等）
- `unknown` → 提示用户手动指定浏览器路径

> 想读同一节的英文说明？→ [Jump to English: Browser Detection](#browser-engine-detection-en)

<a id="操控工具安装缺失时-zh"></a>
## 操控工具安装（缺失时）

**原则**：Agent 侧自动安装（经你同意）+ 浏览器侧由你手动完成（小白语言指引）。**绝不擅自安装**。

### 通道 A：Chromium → chrome-mcp（mcp-chrome）

Agent 侧（需 Node.js ≥ 18.19）：

```bash
npm install -g mcp-chrome-bridge
mcp-chrome-bridge register
# 并在 ~/.workbuddy/mcp.json 的 mcpServers 中写入 chrome-mcp-server（streamableHttp: http://127.0.0.1:12306/mcp）
```

浏览器侧（给用户的手把手步骤）：

> 我在浏览器里需要你做 4 步：
> 1. 打开 https://github.com/hangwin/mcp-chrome/releases ，下载最新的 `chrome-mcp-server-*.zip`；
> 2. 把压缩包解压到一个**固定位置**（如桌面新建"chrome-mcp"文件夹），**不要删除、不要移动**；
> 3. 地址栏输入 `chrome://extensions/`（Edge 用 `edge://extensions/`）→ 打开"开发者模式" → 点"加载已解压的扩展程序"选那个文件夹；
> 4. 点拼图图标找到"Chrome MCP Server"，点图钉固定，再点图标 → 弹窗里点 **Connect** 连接。

### 通道 B：Gecko → GeckoDriver + Marionette

Firefox 内置 Marionette，只需装一个 `geckodriver` 翻译层，**浏览器侧无需装任何插件**。

```bash
# 从 https://github.com/mozilla/geckodriver/releases 下载对应平台 zip 并解压到 PATH
geckodriver --version   # 验证
```

> 想读同一节的英文说明？→ [Jump to English: Installing Tools](#installing-the-driver-tools-when-missing-en)

<a id="安全与原则-zh"></a>
## 安全与原则

1. **语言跟随**：全程使用你的语言（默认简体中文）。
2. **不替你登录**：绝不代填账号密码 / 验证码；只负责打开登录页并提示你手动完成。
3. **人机验证交给你**：遇到验证码 / 滑块 / 行为验证，提示你手动通过，Agent 等待并轮询。
4. **你始终在场**：关键动作前向你确认；你是「眼睛」，Agent 是「手」。
5. **先检测，后行动**：首次必须先检测内核再选通道，除非你手动指定浏览器路径。

> 想读同一节的英文说明？→ [Jump to English: Security](#security--principles-en)

<a id="支持的平台-zh"></a>
## 支持的平台

- **操作系统**：Windows / macOS / Linux（检测脚本跨平台；操控工具安装各异但均有官方指南）。
- **浏览器内核**：Chromium（chrome-mcp / BrowserSkill）、Gecko（GeckoDriver + Marionette）。
- **Agent 宿主**：任何支持 MCP 连接器 / 技能系统的 Agent（如 WorkBuddy、Codex 等）。

> 想读同一节的英文说明？→ [Jump to English: Platforms](#supported-platforms-en)

<a id="如何安装本技能-zh"></a>
## 如何安装本技能

本技能以目录形式分发，结构如下：

```
aicloud-thought-proxy/
├── SKILL.md                         # 核心工作流
├── README.md                        # 本文档（中英双语）
├── LICENSE                          # MIT-0 许可证
├── scripts/detect_browser.py        # 浏览器内核检测脚本
└── references/
    ├── ai-models.md                 # AI 品牌 / 型号 / 模式目录
    ├── browser-detection.md         # 跨平台检测方法详解
    ├── tool-installation.md         # 操控工具安装指南 + 常见问题
    ├── chromium-automation.md       # chrome-mcp / BrowserSkill 操作指南
    └── gecko-automation.md          # GeckoDriver + Marionette 指南
```

**安装方式**：将整个 `aicloud-thought-proxy/` 目录放入你的 Agent 技能目录（如 `~/.workbuddy/skills/` 或项目级 `.workbuddy/skills/`），重启 Agent 即可在对话中用「云思客，用浏览器打开 deepseek 网页版…」触发。

> 想读同一节的英文说明？→ [Jump to English: How to Install](#how-to-install-this-skill-en)

<a id="许可证-zh"></a>
## 许可证

本项目以 **MIT‑0（MIT No Attribution）** 许可证开源。你可以自由使用、修改、分发，无需署名、无需保留版权声明。详见 [`LICENSE`](./LICENSE) 文件。

> 想读同一节的英文说明？→ [Jump to English: License](#license-en)

---

<a id="english-version-en"></a>
# English Version 🇺🇸

<a id="overview-en"></a>
## Overview

The core problem AIcloud‑thought‑proxy solves: **outsource "thinking" to the web AI, keep "doing" in the local Agent.**

When you repeatedly ask an Agent like WorkBuddy / Codex to plan, reason, and write lots of code, token consumption adds up fast. Meanwhile, web AIs such as DeepSeek, Kimi, Doubao, and Qwen ship free tiers or cheap subscriptions that are perfectly adequate for "producing a plan."

AIcloud‑thought‑proxy has the Agent automatically open the web AI in your browser. After you log in manually, the Agent relays your requirements to the web AI and executes the web AI's steps on your local machine — consuming only the web tier's quota and barely touching the Agent's tokens.

> 想读同一节的中文说明？→ [回到中文: 概述](#概述-zh)

<a id="key-features-en"></a>
## Key Features

- **Automatic browser‑engine detection**: on first use, it checks whether your default browser is Chromium (Chrome / Edge / 360 / QQ …) or Gecko (Firefox), then picks the matching driver channel.
- **Dual driver channels**: Chromium → `chrome-mcp` / BrowserSkill; Gecko → GeckoDriver + Marionette.
- **Auto‑install when missing**: if the driver tool isn't installed, it guides you in plain language (Agent installs its side automatically; you get step‑by‑step browser instructions).
- **Fuzzy model selection**: understands "latest / strongest / expert / fast / vision" and maps them to concrete models and thinking modes.
- **Language following**: uses your current language throughout (Simplified Chinese by default), including the messages sent to the web AI.
- **Safe collaboration**: never fills in credentials, never solves CAPTCHAs; you stay the "eyes," the Agent is the "hands."

> 想读同一节的中文说明？→ [回到中文: 核心特性](#核心特性-zh)

<a id="which-web-ais-are-supported-en"></a>
## Which Web AIs Are Supported

| Brand | Chat URL | Representative Models | Thinking Mode | Web Search |
|---|---|---|---|---|
| DeepSeek | https://chat.deepseek.com | DeepSeek‑V3 / R1 | Expert / Fast / Vision | Yes |
| Kimi (Moonshot) | https://www.kimi.com | Kimi K2 / Explore | Thinking | On by default |
| Doubao (ByteDance) | https://www.doubao.com | 1.5 / 2.x series | Deep Think | Yes |
| Qwen (Alibaba) | https://www.qianwen.com (CN) / https://chat.qwen.ai (Intl) | Qwen3 / Qwen3.8‑Max | Deep Think (QwQ) | Yes |
| Wenxin (Baidu) | https://wenxin.baidu.com | ERNIE 4.5 / 5.0 | Deep Think | Yes |
| ChatGPT (OpenAI) | https://chatgpt.com | GPT‑4o / o3 / GPT‑5 | Reasoning | Yes (manual) |
| Claude (Anthropic) | https://claude.ai | Opus / Sonnet / Haiku | Thinking | Yes |
| Gemini (Google) | https://gemini.google.com | 2.x Pro / Flash | Deep Think | On by default |
| Grok (xAI) | https://grok.com | Grok 3 / 4 | Thinking | Yes |
| Zhipu GLM | https://chatglm.cn | GLM‑4.5 / 4.6 | Deep Think | Yes |
| Tencent Yuanbao | https://yuanbao.tencent.com | Hunyuan / DeepSeek | Deep Think | Yes |
| iFlytek Spark | https://xinghuo.xfyun.cn/desk | Spark 4.0 | Deep Think | Yes |

> 想读同一节的中文说明？→ [回到中文: 支持哪些网页版 AI](#支持哪些网页版-ai-zh)

<a id="how-it-works-workflow-en"></a>
## How It Works (Workflow)

```
Trigger
 └─ Stage 0: Confirm language (follow the user's language)
 └─ Stage 1: Detect browser engine (Chromium? Gecko?)
 └─ Stage 1.5: Check driver tool; if missing, ask before auto‑installing
 └─ Stage 2: Choose AI brand / model / thinking mode / web search
 └─ Stage 3: Open web AI → prompt manual login → solve CAPTCHA → plain‑text mode
 └─ Stage 4: Send the first collaboration‑protocol message, establish the division of labor
 └─ Stage 5: Loop: relay requirement → web AI gives steps → local execution → feedback loop
```

**Stage 4 protocol message example (Simplified Chinese)**:

> 我是来自用户电脑中的 AI agent，你负责规划步骤 / 编写代码 / 逻辑推理，我可以根据你的步骤完成扒取代码、创建文件、运行脚本、下载资源、联网搜索等等，而且完全在用户的电脑中，稍后我会给你用户的要求。

> 想读同一节的中文说明？→ [回到中文: 工作原理](#工作原理工作流-zh)

<a id="browser-engine-detection-en"></a>
## Browser Engine Detection

Run the bundled script to detect the system default browser engine; a manual path can also be supplied.

```bash
python scripts/detect_browser.py                  # auto‑detect default browser
python scripts/detect_browser.py --browser "C:\path\to\firefox.exe"   # manual path
```

The script outputs JSON; the key field is `engine`:

- `chromium` → Channel A (Chrome / Edge / 360 / QQ / Brave / Opera …)
- `gecko` → Channel B (Firefox …)
- `unknown` → ask the user to specify a browser path

> 想读同一节的中文说明？→ [回到中文: 浏览器内核检测](#浏览器内核检测-zh)

<a id="installing-the-driver-tools-when-missing-en"></a>
## Installing the Driver Tools (When Missing)

**Principle**: Agent installs its side automatically (with your consent) + you complete the browser side manually (plain‑language guidance). **Never installs without asking.**

### Channel A: Chromium → chrome-mcp (mcp-chrome)

Agent side (requires Node.js ≥ 18.19):

```bash
npm install -g mcp-chrome-bridge
mcp-chrome-bridge register
# then add chrome-mcp-server to mcpServers in ~/.workbuddy/mcp.json (streamableHttp: http://127.0.0.1:12306/mcp)
```

Browser side (step‑by‑step for the user):

> 4 steps in your browser:
> 1. Open https://github.com/hangwin/mcp-chrome/releases and download the latest `chrome-mcp-server-*.zip`;
> 2. Unzip it to a **fixed location** (e.g. a "chrome-mcp" folder on your desktop) — **don't delete or move it**;
> 3. In the address bar type `chrome://extensions/` (Edge: `edge://extensions/`) → enable "Developer mode" → click "Load unpacked" and select that folder;
> 4. Click the puzzle icon, find "Chrome MCP Server," pin it, then click its icon → in the popup click **Connect**.

### Channel B: Gecko → GeckoDriver + Marionette

Firefox ships Marionette built‑in; you only need the `geckodriver` translation layer, and **no browser plugin is required.**

```bash
# Download the matching zip from https://github.com/mozilla/geckodriver/releases and unzip into PATH
geckodriver --version   # verify
```

> 想读同一节的中文说明？→ [回到中文: 操控工具安装](#操控工具安装缺失时-zh)

<a id="security--principles-en"></a>
## Security & Principles

1. **Language following**: uses your language throughout (Simplified Chinese by default).
2. **Never logs in for you**: never fills credentials / CAPTCHAs; only opens the login page and prompts you to finish manually.
3. **CAPTCHAs are yours**: on any challenge (slider / code / behavior check), it asks you to solve it and polls while waiting.
4. **You're always present**: confirms before key actions; you are the "eyes," the Agent is the "hands."
5. **Detect first, act later**: must detect the engine before choosing a channel, unless you specify a path.

> 想读同一节的中文说明？→ [回到中文: 安全与原则](#安全与原则-zh)

<a id="supported-platforms-en"></a>
## Supported Platforms

- **OS**: Windows / macOS / Linux (the detection script is cross‑platform; driver install steps vary but each has official guidance).
- **Browser engines**: Chromium (chrome-mcp / BrowserSkill), Gecko (GeckoDriver + Marionette).
- **Agent hosts**: any Agent supporting MCP connectors / a skill system (e.g. WorkBuddy, Codex, …).

> 想读同一节的中文说明？→ [回到中文: 支持的平台](#支持的平台-zh)

<a id="how-to-install-this-skill-en"></a>
## How to Install This Skill

The skill is distributed as a directory:

```
aicloud-thought-proxy/
├── SKILL.md                         # core workflow
├── README.md                        # this document (bilingual)
├── LICENSE                          # MIT-0 license
├── scripts/detect_browser.py        # browser-engine detection script
└── references/
    ├── ai-models.md                 # AI brand / model / mode catalog
    ├── browser-detection.md         # cross-platform detection details
    ├── tool-installation.md         # driver install guide + FAQ
    ├── chromium-automation.md       # chrome-mcp / BrowserSkill guide
    └── gecko-automation.md          # GeckoDriver + Marionette guide
```

**Installation**: drop the whole `aicloud-thought-proxy/` directory into your Agent's skill folder (e.g. `~/.workbuddy/skills/` or project‑level `.workbuddy/skills/`), restart the Agent, then trigger it in chat with "云思客，用浏览器打开 deepseek 网页版…" ("AIcloud, open the DeepSeek web chat…").

> 想读同一节的中文说明？→ [回到中文: 如何安装本技能](#如何安装本技能-zh)

<a id="license-en"></a>
## License

This project is open source under the **MIT‑0 (MIT No Attribution)** license. You may use, modify, and distribute it freely, with no attribution and no requirement to retain copyright notices. See the [`LICENSE`](./LICENSE) file for the full text.

> 想读同一节的中文说明？→ [回到中文: 许可证](#许可证-zh)
