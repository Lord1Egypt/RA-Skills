# OpenClaw 帶來的隨想

<span style="color:red">Disclaimer</span>: 
- A complete **personal** opinion with no guarantee of accuracy, and the situation is constantly changing.
- 沒有經過 AI 潤色
- 本文只是針對一些個人體會和踩過的坑，並且嘗試覆蓋一些通用的 topic

[TOC]

## Future Predictions
#### Long-term
- Less human required. Entry-level engineer layoff, in Silicon Valley
    - eg. Less employee > less office > less janitor > less printer to rent...
- Impact on US Stock Market: less revenue > lower stock value!
- 2025, 2026, then 2027

#### Short-term
- Writing code = labor work (搬機上架，接線還得人來). 
- **角色變換**: Developer vs Builder/ Orchestrator
    - Orchestrator **prompt** example > https://x.com/94vanAI/status/2029321553167458358
- **技能**: 
    - English vs other languages. 所有基礎 large language model 都是使用英語做初始訓練
    - 人類自然語言與機器交互

## What is OpenClaw
- 需要你告訴用什麼大腦 (brain= model) 和用什麼方式 (method= `skills`)，然後，它去執行 (task execution)
- Assitant - Hub - Middleware
- Configuration > `~/.openclaw/openclaw.json`
- Middleware
- Tools

#### Tools > plugin, skills, automation, and more
- Tools > https://docs.openclaw.ai/tools
- Plugin
    - `openclaw plugins list`.  eg, `openclaw plugins install @openclaw/voice-call`
    - Official plugins > https://docs.openclaw.ai/tools/plugin#available-plugins-official
- Skills via `clawhub` (https://github.com/openclaw/clawhub)
    - eg, `clawhub list` and `clawhub install ddg-web-search`
    - up to 20260307, ~5700 in **community** with high-quality (active) ~3000, at ClawHub.ai
    - My published skill > https://clawhub.ai/dashboard
    - See below for more info
- Automation
- Media

#### Skills

Skills are organized into approximately 28 categories to help users find specific functionalities: 

- Developer Tools: Includes GitHub integration, Linear project management, and automated coding agents (543+ skills).
- AI & LLMs: Tools for specialized models, prompt engineering, and consciousness frameworks (287+ skills).
- Search & Research: Specialized scrapers using Playwright and academic research tools (253+ skills).
- Social & Communication: Email infrastructure via AgentMail and social network integrations for agents (189+ skills).

> Ref > [opencaw how many skills in clawhub community](https://www.google.com/search?client=firefox-b-d&q=openclaw+how+many+skills+in+clawhub+community+totally&udm=50&fbs=ADc_l-aN0CWEZBOHjofHoaMMDiKpaEWjvZ2Py1XXV8d8KvlI3tR7kVu8a3MULVA9bsoO0mCCFiZoMv28ux3eOJ39Q_ixnRJO66C0xBAUoovRT1WiWVOtT4zjXe0lj3elvwDB5I8j6nJU6_mGZR00yYVVXi0fynqC7IsJwxu75Hxrqk_uB71U5DlQaov6BIAokHa5B21TVygnT9xQ6xIiei68IJ0H8mD_Ag&ved=2ahUKEwiI3Myo1YyTAxXEcvUHHcbwLOoQ0NsOegQIAxAB&aep=10&ntc=1&mstk=AUtExfCrekwiaH57ZI9BScPsriN0hKaP_o-E4Y8tFYtKZ4nsTntS_dyOpJt43nXshZ8CmwTBlz2TDZ6hjNu-NAl1x5kxH1VzzGWitjzQCVNGUSCqL75UJE8MxqELw6WOS9h8dDHK636a0dLsIUJsZFJ1ZmSzb6nC9YONZiki5ZYUwZZ0Dy7AOjxAJNNKRFmuSrqtwsTnUbNylWAz63QjTkMXm1z3B2PtzKqNNuZNEXIWmwMZ7yv5f9g1RTOUtBVKiJip-S-OF5HcK8U98o8MDTEEBKuKLAIK5AYRfLIQiR72AUcEb-gWSf4ftPWIhWXlBK6nMvg7nHtcmNNjig&csuir=1&mtid=qoOrabyQCMTl1e8PxuGz0Q4)

#### Personalization Configuration/ 個性化配置
- Location: `~/.openclaw/workspace`
- Customization > https://www.reddit.com/r/openclaw/comments/1r6rnq2/memory_fix_you_all_want/

md | func
-- | --
`SOUL.md` | who are you?
`AGENTS.md` | working preference, eg, memory management
`USER.md` | who are you helping?

## 小結

#### 具體可以幹什麼？
- 這個清單應該很長
- Human work, eg. phone call, copy & paste, multi-tasks
- ...

#### 有些特點
- Switching model(s) > `openclaw config get agents.defaults.models`
- 所有 conversations 無邊界 for **Vector Search**
- **Local** and **Persistent** storage > `.openclaw/agents/main/sessions/`

#### Unique (獨到) Tech & Business Model
- 平臺? eg, OpenAI, 豆包 - bill with API usage


#### Model Selection
- 完全個人體驗和喜好，且模型世界變化快速多端！

model | reason of choosing
-- | --
OpenAI | absolute leading model. `4o-mini` is cheap with 1/4 token usage
Gemini | free tier at AI studio. I personally use its commandline coding
Claude | **best** for reasoning, inference and coding
Qwen | 感覺國內評價最好的。個人沒有用過


#### 踩過的坑/ Issues I got
- 26.03.02 Milestone Release > [https://www.reddit.com/r/openclaw/...after updating_to_openclaw_202632_your_agent/](https://www.reddit.com/r/openclaw/comments/1rlg0ki/psa_after_updating_to_openclaw_202632_your_agent/)
- `openclaw doctor --fix` 可以 smartly fix 很多配置錯誤。但是，backup your `~/.openclaw/openclaw.json` before running. Run `openclaw doctor` without `--fix` first
- Different and weird search behaviors from **Telegram**, **WhatsApp** & **Discord**? Eg, search "can you search web to find hotel price comparison in asakusa/ 淺草, tokyo japan"

---

## 引申觀察

#### 標準/ standardization
- 提問：為什麼我們需要關注這個？
- **原則**: 最小計算單元
- **Linux** and daemon control, in `command line` (standard `$SHELL`)
    - eg, `systemctl --user start openclaw-gateway.service`
- Markdown in `md` file
- Configuration and Data: **`json`** - **descriptive** and **declarative**, as well as **`yaml`**
- Package Mgmt:
    - `node` and `npm`
    - `homebrew` on macOS and Linux


#### Security (永遠的話題)

- Protect all of your API keys - `chmod 700 .openclaw/credentials/` 
- Channel > `openclaw channels list`
- Network: `openclaw gateway` with proxy, eg. `openclaw tui`
- 永遠的話題。這個可以成為一個有償服務！

---

## Architecture Overview Recap/ 框架的不同視角

OpenClaw is designed as a modular, layered, and self-hosted AI agentic framework that connects messaging apps (Telegram, Slack, Discord, etc.) to Large Language Models (LLMs) and local tools. 
The architecture can be understood through its core structural layers, often described as a four-layer stack. 

#### Core Architectural Layers

- **Model Layer (the Brain)**: Acts as a stochastic CPU, processing instructions, reasoning, and generating responses.
- **Memory Layer (the State)**: Manages context, storing conversations on disk as JSONL files (short-term) and using vector search for long-term recall.
- **Tool Layer (the Muscles)**: Bridges agent reasoning and real-world action, allowing the AI to interface with APIs, file systems, and external services.
- **Orchestrator Layer (the Hub)**: The central Gateway service that manages session routing, message processing, and tool execution. 

#### Functional "Workspace" Layers 
Another perspective on OpenClaw's architecture focuses on its configuration-driven, "Workspace-First" design: 

- `AGENTS.md`: Serves as the primary configuration file for defining an AI agent's purpose, behavior, and operational instructions.
- `SOUL.md`: Defines the agent's purpose, personality, and behavioral rules.
- `TOOLS.md`: Specifies the capabilities and tools available to the agent.
- `IDENTITY.md`: Personalizes the agent for the user.
- `HEARTBEAT.md`: Configures the agent's automatic execution, such as scheduled tasks and monitoring. 

#### Operational Flow Layers
When a user interacts with OpenClaw, the message passes through these operational stages: 

- **Channels**: The messaging interface (Telegram, WhatsApp).
- **Gateway**: Receives messages and manages connections.
- **Agent/ Session**: The AI processes the request, loading relevant context.
- **Tools/ Skills**: The agent performs tasks (e.g., browsing, coding) and returns a response. 

OpenClaw is often described as a "self-hosted gateway" that operates as a long-running Node.js service on your machine, distinguishing it from browser-based AI tools

---

## Appendix/ 後續

#### Extra Read
func briefing | url 
-- | -- 
Awesome Skills (分類) | https://github.com/VoltAgent/awesome-openclaw-skills
多稿合并：从手动比稿到一键 Skill | https://x.com/dotey/status/2029443721637327027 | 
1 person companies | [https://www.reddit.com/r/AgentsOfAI/./1person_companies_arent_far_away/](https://www.reddit.com/r/AgentsOfAI/comments/1rhuflt/1person_companies_arent_far_away/) 
`sqlite3` for vector | https://www.pingcap.com/blog/local-first-rag-using-sqlite-ai-agent-memory-openclaw/
`firecrawl`: web scraping | https://www.firecrawl.dev/blog/openclaw-firecrawl-guide
Market investment | https://x.com/xingpt/status/2025219080421277813
Tools & Skills tutorial | https://yu-wenhao.com/en/blog/openclaw-tools-skills-tutorial/

#### `json` vs `jsonl`

Structural Differences
Feature | 	JSON	 |JSONL (JSON Lines / NDJSON)
-- | -- | --
Overall Structure	| A single JSON object or a single array of objects, requiring proper nesting and commas.	| Multiple, independent JSON objects separated by newline characters (\n).
File Validity	| The entire file is a single, valid JSON document.	| The file as a whole is not a single valid JSON document in the standard sense, but each individual line is.
Example	| `[{"id": 1}, {"id": 2}]`	| `{"id": 1}\n{"id": 2}\n`

--- 

## Answers

- Skill stack and investment > human resource and technical strategy. 
- 換一種方式：我們做什麼，和不做什麼？比如，IaaS 都是租賃。這個又引申一個問題：我們的價值點 value proposition 和 技術**卡位**
- Operation automation flow. 假設我們使用類似 ansible 和 terraform 來做自動化流程 (流水線，如變更)，我們必須關注 compute element，如前面提到的 `yaml`, `json` 和 `markdown`。這些都涵蓋在 GitOps 之下。在如，使用 Docker 和 Kubernetes (本身即是 compute element)，使用 `helm` (所有配置都使用 `yaml` 實現) 做調度 (orchestrating)。這些在規模化生產的狀態下，是完全無法避免 (unavoidable) 和繞開的！
- l.cncf.io 對我來說，就像 bible 描述“最小的計算單元” (compute element)