<div align="center">

# 🌐 DeepSeek Web Search

### The web-search superpower that's *already inside* DeepSeek's API.

**Ask a question → DeepSeek's own server-side agents browse the live web → you get a cited, synthesized answer.**

No third-party search engine. No extra API keys. No plumbing.

One standard `SKILL.md` + one script — instant web search in any modern AI harness.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Node](https://img.shields.io/badge/Node-%3E%3D18-brightgreen)](https://nodejs.org/)
[![DeepSeek](https://img.shields.io/badge/Powered%20by-DeepSeek%20Responses%20API-purple)](https://platform.deepseek.com)
[![Harnesses](https://img.shields.io/badge/Works%20in-Claude%20Code%20%E2%80%A2%20Codex%20%E2%80%A2%20Gemini%20CLI%20%E2%80%A2%20Copilot%20CLI-lightgrey)]()

**English** · [简体中文](README.zh-CN.md)

</div>

---

## ⚡ The One-Line Pitch

**DeepSeek officially built web search into their API.** Using the `Responses`-format endpoint with `deepseek-v4-flash`, you just declare a `web_search` tool in the request — and DeepSeek's server-side **agent** takes over: it searches, opens pages, re-searches, cross-checks, and hands you a **synthesized, source-backed answer**. Not a link dump. A finished answer.

This skill packages that power into the universal `SKILL.md` format, so any harness — Claude Code, Codex, Gemini CLI, Copilot CLI, and more — can load it and browse the web instantly.

---

## 😮 Why This Is a Big Deal

Every other "web search" setup is a plumbing project:

| | The traditional way | DeepSeek Web Search |
|---|---|---|
| **Search engine** | Sign up for Bing / Brave / Serper / Tavily… | Built into the DeepSeek API — **nothing to integrate** |
| **Keys** | Generate yet another API key, wire quotas & billing | **Zero extra keys** — your existing DeepSeek key is all you need |
| **Glue code** | Write adapters to fetch results, paginate, and shape JSON | **Zero glue** — one clean HTTP call |
| **What you get back** | Raw links you must re-feed to an LLM | **A synthesized answer with sources**, ready to use |
| **Search quality** | Dumb keyword matches | **An agent that searches, opens pages, verifies, and re-searches** |

> The hidden killer feature: this is **not a simple search API**. DeepSeek's agent capability wraps your *query and the results together* — it reasons about what it finds, notices false premises in your question, and returns one coherent, grounded answer. That's the difference between "here are 10 links" and "here's what actually happened."

---

## ✨ Features

- 🔥 **First-party search** — powered by DeepSeek's official API, not a third-party wrapper
- 🤖 **Agent-grade research** — multi-round search loop (`search → open pages → re-search`) executed server-side, in a single API call
- 🎯 **Synthesized answers** — returns a coherent answer plus the source URLs consulted, not raw result spam
- 🌏 **Bilingual coverage** — handles Chinese *and* English web; answers in your language
- 🪶 **Zero dependencies** — one self-contained `search.mjs` using Node's built-in `fetch`
- 🔒 **Key stays local** — your key lives in `config.json` or `DEEPSEEK_API_KEY`; it never leaves your machine
- 📦 **Universal format** — a standards-compliant `SKILL.md` that installs anywhere, with a one-line installer

---

## 🧠 How It Works

One HTTP call to DeepSeek's Responses API:

```json
{
  "model": "deepseek-v4-flash",
  "input": "Who hosted the 2026 Winter Olympics?",
  "instructions": "You are a web search assistant. Search, open pages, and verify as needed, then give an accurate, complete, well-sourced answer.",
  "tools": [{ "type": "web_search" }],
  "tool_choice": { "type": "web_search" },
  "max_output_tokens": 8000
}
```

DeepSeek's server takes it from there:

1. 🔎 issues a `web_search_call`
2. 📄 opens the most promising pages (`open_page`)
3. 🔁 re-searches if the picture is incomplete
4. ✅ returns `output_text` — a synthesized, source-backed answer

`search.mjs` parses the response into clean `{ answer, sources }` JSON. That's the whole integration.

---

## 🚀 Installation

### Method 1 — One-line npx install (recommended)

```bash
npx github:mingzeng21/deepseek-web-search
```

That's it. No clone, no manual steps. The installer places the skill in **every supported harness** at once — `~/.claude/skills/` (Claude Code) **and** `~/.agents/skills/` (Codex · Gemini CLI · Copilot CLI) — then prompts for your DeepSeek API key (or reads `DEEPSEEK_API_KEY`) and saves it to a local `config.json`.

Target a single harness, or skip the key prompt:

```bash
npx github:mingzeng21/deepseek-web-search --claude   # Claude Code only
npx github:mingzeng21/deepseek-web-search --codex    # Codex / Gemini CLI / Copilot CLI only
npx github:mingzeng21/deepseek-web-search --skip-key # install without entering a key (configure later)
```

### Method 2 — Just ask your AI assistant

No cloning, no terminal. In **Claude Code** or **Codex**, paste the URL and say:

> Install this skill: https://github.com/mingzeng21/deepseek-web-search.git

The assistant clones the repo and drops it into the correct skills folder for you — Claude Code reads `~/.claude/skills/`, while Codex, Gemini CLI, and Copilot CLI read `~/.agents/skills/`. Restart your harness (or run `/reload-plugins` in Claude Code) and it's live.

> **Note:** `~/.agents/skills/` is the cross-runtime alias shared by Codex, Gemini CLI, and Copilot CLI — install once, use in all three.

---

## 🔑 Configuration

Get an API key at [platform.deepseek.com](https://platform.deepseek.com), then:

```bash
cp config.example.json config.json
# edit config.json and paste your key
```

Or skip the file entirely — the script also reads the environment:

```bash
export DEEPSEEK_API_KEY="sk-..."
```

---

## 💻 Usage

```bash
node ./search.mjs "Who won the 2026 Winter Olympics?" 8000
```

| Argument | Description |
|---|---|
| `query` (required) | The question to research |
| `maxOutputTokens` (optional) | Cap on answer length, default `8000` (max `16384`) |

Output — one JSON object:

```json
{
  "answer": "The 2026 Winter Olympics were held in Milan and Cortina d'Ampezzo…",
  "sources": ["https://olympics.com/…", "https://en.wikipedia.org/…"],
  "query": "Who won the 2026 Winter Olympics?",
  "model": "deepseek-v4-flash",
  "usage": { "input_tokens": 812, "output_tokens": 640, "total_tokens": 1452 },
  "engine": "deepseek-web-search"
}
```

`answer` is ready to present. `sources` are the pages the agent consulted — **always cite them** when sharing the answer.

---

## ⚙️ Requirements

- **Node.js 18+** (uses the built-in `fetch` — no dependencies)
- A **DeepSeek API key** (see [Configuration](#-configuration))

---

## 📌 Notes & Caveats

- The multi-round search runs server-side, so calls take **15–70 seconds**. That's the agent working — not a hang (the script allows up to 120s).
- `sources` are *pages consulted*, not per-claim citations. For critical facts, verify against them before trusting the answer.
- The agent can notice and correct **false premises** in your query (e.g. "2026 Paris Olympics" → the real 2026 Milan–Cortina Winter Olympics).
- When presenting results, always cite the source URLs.

---

## ❤️ Liked it?

Star the repo, share it with your team, and publish it to your favorite skill hub. DeepSeek already did the hard part — this skill just makes it one copy-paste away.

---

## 📄 License

[MIT](LICENSE) © MingZeng
