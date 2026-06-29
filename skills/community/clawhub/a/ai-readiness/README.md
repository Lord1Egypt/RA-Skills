<p align="center">
  <a href="https://ai.silverbackmarketing.com"><img src="https://ai.silverbackmarketing.com/images/ai-readiness-og.jpg" alt="AI Readiness Files — a structured kit of files that tells ChatGPT, Claude, Gemini, and Perplexity exactly who you are before they guess wrong" width="100%"></a>
</p>

# AI Readiness Skill

[![npm version](https://img.shields.io/npm/v/@silverbackmarketing/ai-readiness)](https://www.npmjs.com/package/@silverbackmarketing/ai-readiness) [![npm downloads](https://img.shields.io/npm/dm/@silverbackmarketing/ai-readiness)](https://www.npmjs.com/package/@silverbackmarketing/ai-readiness) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![MCP compatible](https://img.shields.io/badge/MCP-compatible-1a2c4e)](https://ai.silverbackmarketing.com/#mcp) [![Claude Skill](https://img.shields.io/badge/Claude-Skill-d97757)](https://ai.silverbackmarketing.com) [![Cursor compatible](https://img.shields.io/badge/Cursor-compatible-000000)](#use-via-mcp-no-install) [![OpenAI Codex compatible](https://img.shields.io/badge/OpenAI_Codex-compatible-412991)](#use-via-mcp-no-install) [![Perplexity compatible](https://img.shields.io/badge/Perplexity-compatible-20808D)](#use-via-mcp-no-install)

[![Optimizes for AI search](https://img.shields.io/badge/Optimizes_for-ChatGPT·Claude·Gemini·Perplexity-20808D)](https://ai.silverbackmarketing.com)

> Generate a complete suite of **AI readiness files** (GEO / generative engine optimization) for any website in a single command — `llms.txt`, `ai.txt`, schema, RAG indexes, and more. Install it into Claude, Cursor, Windsurf, GitHub Copilot, Gemini, or Codex with one `npx` command, or connect over MCP with no install.

**📖 Live site & full docs:** **[ai.silverbackmarketing.com](https://ai.silverbackmarketing.com)** · ⭐ Star this repo if it helps you get found by AI.

<p align="center">
  <a href="https://www.producthunt.com/products/ai-readiness-kit?embed=true&utm_source=badge-featured&utm_medium=badge&utm_campaign=badge-ai-readiness-kit" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1178266&theme=light" alt="AI Readiness Kit - The 17 files that make your site understandable to AI | Product Hunt" width="250" height="54"></a>
</p>

---

## What is the AI Readiness Kit?

The AI Readiness Kit is a free, open-source set of **17 structured files you deploy at the root of your website** — `robots.txt`, `ai.txt`, `llms.txt`, schema, RAG indexes, and more — that tell ChatGPT, Claude, Gemini, and Perplexity exactly who you are, what you offer, and how to represent you. Generate the whole set, tailored to any site, with a single command. Free forever (MIT); install with `npx` or run it over MCP with no install.

---

## Why AI readiness

When someone wants a product recommendation, a service provider, or a straight answer, they often ask ChatGPT, Claude, Gemini, or Perplexity **before** they ever visit a website. If you are not giving those systems clear, current signals, they guess — and they often guess wrong.

AI readiness files are structured files you deploy at the root of your website to tell AI systems exactly **who you are, what you offer, and where to send people**. They speak a format AI already understands (the [llmstxt.org](https://llmstxt.org) standard, Schema.org, and emerging AI-crawler conventions), so assistants stop guessing about your brand based on stale training data and start representing you accurately in their answers.

This skill researches any site, classifies its industry, and generates all of those files for you — tailored to that business — in one command.

---

## Contents

- [Install](#install)
- [Use via MCP (no install)](#use-via-mcp-no-install)
- [What It Does](#what-it-does)
- [The Files](#the-files)
- [Usage](#usage)
- [FAQ](#faq)
- [Reference Documentation](#reference-documentation)
- [PDF Guides](#pdf-guides)
- [Skill File Structure](#skill-file-structure)
- [Author & Company](#author--company)
- [License](#license)

---

## Install

### Quick install (any agent) — `npx`

```bash
# Global skill install → ~/.agents/skills/ AND ~/.claude/skills/ (default)
npx @silverbackmarketing/ai-readiness install

# AGENTS.md — the cross-agent standard (Cursor, Codex & others)
npx @silverbackmarketing/ai-readiness install --agent agents

# Both at once (recommended)
npx @silverbackmarketing/ai-readiness install --all
```

Primary targets:

| Target | Installs to |
|---|---|
| `skills` | `~/.agents/skills/ai-readiness/` **and** `~/.claude/skills/ai-readiness/` (full skill — `SKILL.md` + scripts + references) |
| `agents` | `./AGENTS.md` — the standard read by Cursor, Codex, and a growing list of agents (adds a delimited block, keeps your existing content) |
| `claude` | `~/.claude/skills/ai-readiness/` only |

For prompt-based agents, **`AGENTS.md` is the default and recommended target** — most modern agents now read it. Tool-specific files remain available if you prefer them:

| Opt-in target | Installs to |
|---|---|
| `cursor` | `./.cursor/rules/ai-readiness.mdc` |
| `windsurf` | `./.windsurf/rules/ai-readiness.md` |
| `copilot` | `./.github/copilot-instructions.md` (delimited block) |
| `gemini` | `./GEMINI.md` (delimited block) |
| `generic` | `./ai-readiness.SKILL.md` (paste into any system prompt) |

Non-Claude targets install into the current directory, so run the command from your project root. `--all` installs Claude + `AGENTS.md`. Add `--force` to overwrite, or `--dir <path>` to change the target. Shared-file installs insert a marked block and update it in place on re-run, so they never clobber your other instructions.

### Other install options

- **Claude Cowork one-click:** download and open [`ai-readiness.skill`](ai-readiness.skill).
- **Any AI, manually:** copy [`SKILL.md`](SKILL.md) into the assistant's system prompt or custom instructions.

After installing, trigger it with `/ai-readiness yoursite.com` in Claude, or just ask any agent: *"create AI readiness files for yoursite.com."*

### Use via MCP (no install)

Connect your coding agent to the hosted MCP server instead of installing the skill locally. Same workflow — research a site and generate all the files.

**Production:** `https://ai.silverbackmarketing.com/api/mcp`

Example prompts once connected:

```
Generate AI readiness files for example.com
Use ai-readiness to list all output files
Get the file spec for llms.txt from ai-readiness
```

**Cursor** — add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "ai-readiness": {
      "url": "https://ai.silverbackmarketing.com/api/mcp"
    }
  }
}
```

Refresh MCP servers, then ask: *"Use ai-readiness to generate files for example.com"*

**Claude Code** — add `.mcp.json` to your project root:

```json
{
  "mcpServers": {
    "ai-readiness": {
      "type": "http",
      "url": "https://ai.silverbackmarketing.com/api/mcp"
    }
  }
}
```

Or run:

```bash
claude mcp add --transport http ai-readiness https://ai.silverbackmarketing.com/api/mcp
```

Restart the session, run `/mcp`, then ask: *"Generate AI readiness files for mysite.com using ai-readiness"*

**VS Code / Copilot** — add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "ai-readiness": {
      "type": "http",
      "url": "https://ai.silverbackmarketing.com/api/mcp"
    }
  }
}
```

Open **MCP: List Servers**, confirm `ai-readiness` is running, then use agent mode in Copilot Chat.

**Claude Desktop** — use [mcp-remote](https://www.npmjs.com/package/mcp-remote) in `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "ai-readiness": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://ai.silverbackmarketing.com/api/mcp"]
    }
  }
}
```

Fully quit and reopen Claude Desktop after saving.

**OpenAI Codex** — add to `~/.codex/config.toml`:

```toml
[mcp_servers.ai-readiness]
url = "https://ai.silverbackmarketing.com/api/mcp"
enabled = true
```

Or run `codex mcp add ai-readiness --url https://ai.silverbackmarketing.com/api/mcp`, then `/mcp` in a session.

**Antigravity** — Agent panel → … → MCP Servers → Manage → View raw config:

```json
{
  "mcpServers": {
    "ai-readiness": {
      "serverUrl": "https://ai.silverbackmarketing.com/api/mcp"
    }
  }
}
```

Antigravity uses `serverUrl` (not `url`). Save, refresh, then try in agent mode.

**Perplexity** — two ways to use the kit:

- **Via remote MCP connector** — *requires a paid Perplexity plan; an org admin may first need to enable "Allow members to add custom connectors."* Go to **Account settings → [Connectors](https://www.perplexity.ai/account/connectors)** → click **+ Custom connector** (top-right) → select **Remote**, then fill in:

  | Field | Value |
  |---|---|
  | **Name** | `AI Readiness` |
  | **MCP Server URL** | `https://ai.silverbackmarketing.com/api/mcp` |
  | **Authentication** | `None` |
  | **Transport** | `Streamable HTTP` |

  Check the acknowledgement box, click **Add**, then click the connector card to enable it. Ask: *"Use ai-readiness to generate files for example.com."* (Full steps: Perplexity's [Adding Custom Remote Connectors](https://www.perplexity.ai/help-center/en/articles/13915507-adding-custom-remote-connectors) guide.)

- **Manual — free, works on any plan:** paste [`SKILL.md`](SKILL.md) into a thread (or attach it), then ask: *"Using these AI readiness instructions, generate AI readiness files for example.com."*

**Quick test:**

```bash
curl -X POST 'https://ai.silverbackmarketing.com/api/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":1}'
```

More client configs: [ai.silverbackmarketing.com/#mcp](https://ai.silverbackmarketing.com/#mcp)

---

## What It Does

Run `/ai-readiness yoursite.com` and the AI will research the site, classify its industry, and generate production-ready files that tell AI systems (ChatGPT, Claude, Gemini, Perplexity, and others) exactly what the site is, what it offers, and where to send users.

When deployed to a web root, these files improve how a site appears in AI-generated answers, summaries, and recommendations — a must-have for any business that wants to show up in the AI-driven web.

---

## The Files

The skill generates **18 files**. Of these, **17 deploy to your web root** across 7 categories (**16** if you omit the optional `.well-known/ai-plugin.json`); the 18th, `README.md`, is project documentation for your team. This matches the [17-file kit described on the live site](https://ai.silverbackmarketing.com/#files).

| # | File | Purpose | Deployed |
|---|------|---------|:---:|
| 1 | `ai.txt` | Primary AI identity declaration | ✅ |
| 2 | `llms.txt` | Concise LLM-readable site summary | ✅ |
| 3 | `llms-full.txt` | Comprehensive LLM knowledge base | ✅ |
| 4 | `ai-sitemap.xml` | AI-optimized sitemap | ✅ |
| 5 | `sitemap.md` | Human-readable sitemap for AI context | ✅ |
| 6 | `ai-entities.json` | Structured entity definitions | ✅ |
| 7 | `ai-intent.json` | User intent and query mappings | ✅ |
| 8 | `ai-schema.json` | Schema.org structured data | ✅ |
| 9 | `rag-index.json` | RAG retrieval knowledge base | ✅ |
| 10 | `rag-index.jsonl` | JSONL format for embedding pipelines | ✅ |
| 11 | `ai-disclosure.txt` | AI content transparency statement | ✅ |
| 12 | `training-data-policy.txt` | Data usage and training policy | ✅ |
| 13 | `.well-known/ai-plugin.json` | Plugin manifest for AI agents (optional) | ➖ |
| 14 | `structured-data-guide.md` | Implementation guide for developers | ✅ |
| 15 | `manifest.json` | Web app manifest | ✅ |
| 16 | `deployment-checklist.md` | Step-by-step deployment guide | ✅ |
| 17 | `robots.txt` | AI crawler directives | ✅ |
| 18 | `README.md` | Project documentation (not deployed) | ➖ |

---

## Usage

In Claude Cowork, type:

```
/ai-readiness yoursite.com
```

Or use natural language:

```
create AI readiness files for acmecorp.com
make my site AI-ready: hubspot.com
generate llms.txt for shopify.com
```

Claude will:
1. Run 10+ targeted searches to research the site
2. Classify the site type (SaaS, e-commerce, education, healthcare, etc.)
3. Generate all files tailored to that industry
4. Save everything to a folder named after the domain in your workspace

---

## FAQ

### Getting Started

**What are AI Readiness Files?**
They are structured files you deploy at the root of your website to tell AI systems exactly who you are, what you offer, and where to send people. They speak a format AI already understands, so assistants stop guessing about your brand based on old training data.

**Why does AI readiness matter now?**
When someone wants a product recommendation, a service provider, or a straight answer, they often ask ChatGPT, Claude, Gemini, or Perplexity before they visit a website. If you are not giving those systems clear, current signals, they guess. And they often guess wrong.

**How many files are in the kit?**
The kit includes 17 purpose-built files across 7 categories: Identity & Permissions, Content Files, Map & Navigation, Intelligence Files, Research Files, Policy Files, and Operations Files. Each one helps AI understand and represent your site more accurately. (The skill generates 18 files total — the extra one is this `README.md` for your project.)

**Where should I start?**
Start with the critical files: `robots.txt`, `ai.txt`, `llms.txt`, and `llms-full.txt`. They deliver the biggest immediate impact and are what most AI systems look for first. Then add sitemaps, intelligence JSON files, policies, and operational files using the deployment checklist.

### Identity & Permissions

**What does robots.txt do for AI?**
robots.txt sits at the front door of your website and tells automated visitors (search engines, AI bots, and scrapers) which sections they can access. For AI readiness, it includes instructions for major crawlers like GPTBot and ClaudeBot, pointing them toward your `llms.txt` and `ai-sitemap.xml` while keeping checkout, login, and admin pages off limits.

**What is ai.txt?**
ai.txt is your brand's introduction to every AI system on the internet. Where robots.txt controls access, ai.txt goes further. It covers what you sell, what you are known for, your authoritative topics, and the rules for what AI systems can and cannot do with your content.

**How is ai.txt different from robots.txt?**
robots.txt controls access: which pages bots can crawl. ai.txt controls identity: who you are, what you offer, and your ground rules for AI use of your content. Think of robots.txt as the doorman and ai.txt as the briefing document you hand a journalist before an interview.

### Content & Navigation

**What is llms.txt?**
llms.txt is a structured text file built for large language models. It gives AI a quick map of your website: company name, description, organized sections with direct links, and the most common questions your site answers. It follows the [llmstxt.org](https://llmstxt.org) standard used by ChatGPT, Claude, Gemini, and Perplexity.

**What's the difference between llms.txt and llms-full.txt?**
llms.txt is the cheat sheet: a quick summary an AI can scan in seconds. llms-full.txt is the deep dive with rich descriptions, detailed Q&A, and full category explanations. If llms.txt is a Wikipedia summary, llms-full.txt is the full article.

**Why do I need an ai-sitemap.xml?**
A regular sitemap lists pages and timestamps. The ai-sitemap adds what each page is about, its content type, and a plain-English summary. It is the difference between a paper road map and GPS with points of interest. AI crawlers can understand pages without fetching and parsing each one individually.

### Intelligence & Research

**What is ai-intent.json?**
ai-intent.json maps real user questions (the things people type into AI assistants) to the best page on your website to answer each one. Without it, AI guesses which page to recommend. With it, you give AI a direct URL for every common query.

**What are ai-entities.json and ai-schema.json for?**
ai-entities.json is a structured catalog of the important parts of your site: products, categories, services, and key concepts. It powers AI knowledge graphs. ai-schema.json uses the Schema.org standard to describe your organization in machine-readable format so search engines and AI systems can identify you without ambiguity.

**What are the RAG index files?**
rag-index.json and rag-index.jsonl are ready-made indexes of your site built for AI research and retrieval pipelines. When a user asks a question, AI first pulls the most relevant documents from this index before generating an answer, which keeps responses grounded in your actual content.

### Policies & Maintenance

**What is a training data policy?**
training-data-policy.txt sets formal rules for how AI companies can use your content, including model training, RAG indexing, and commercial use. It answers a practical question every brand should decide upfront: what are others allowed to do with your work?

**What is ai-disclosure.txt?**
ai-disclosure.txt is a public transparency report explaining how your organization uses AI, whether for content generation, recommendations, or customer interactions. It builds trust by answering those questions before someone has to ask.

**How often should I update my AI readiness files?**
It depends on the file. Update `llms.txt` and sitemaps monthly or when your site structure changes. Refresh `ai.txt` and `llms-full.txt` quarterly or when products change. Review policy files annually. The `manifest.json` file lists recommended update frequencies for every file in the kit.

---

## Reference Documentation

The [`references/file-specs.md`](references/file-specs.md) file contains the detailed specification for each file — required structure, key fields, and condensed examples. It is loaded automatically when the skill runs.

The [`scripts/gen_jsonl.py`](scripts/gen_jsonl.py) utility converts `rag-index.json` to `rag-index.jsonl` format for use with embedding pipelines:

```bash
python3 scripts/gen_jsonl.py rag-index.json rag-index.jsonl
```

---

## PDF Guides

The [`docs/`](docs/) folder contains PDF reference guides explaining each file in plain English and technical detail:

| Guide | Audience | Files Covered |
|-------|----------|---------------|
| [AI Readiness Guide — With Plugin](docs/ai-readiness-guide-with-plugin.pdf) | General / Non-technical | All 17 files incl. ai-plugin.json |
| [AI Readiness Guide — No Plugin](docs/ai-readiness-guide-no-plugin.pdf) | General / Non-technical | 16 files excl. ai-plugin.json |
| [Developer Reference — With Plugin](docs/ai-readiness-guide-dev-with-plugin.pdf) | Web Developers | All 17 files, compact technical format |
| [Developer Reference — No Plugin](docs/ai-readiness-guide-dev-no-plugin.pdf) | Web Developers | 16 files, compact technical format |

---

## Skill File Structure

```
ai-readiness/
├── ai-readiness.skill          ← Claude Cowork installable skill (download & open)
├── SKILL.md                    ← Raw skill definition — works in any AI assistant
├── README.md                   ← This file
├── references/
│   └── file-specs.md           ← Detailed specs for all output files
├── scripts/
│   └── gen_jsonl.py            ← JSONL generator utility
└── docs/
    ├── ai-readiness-guide-with-plugin.pdf
    ├── ai-readiness-guide-no-plugin.pdf
    ├── ai-readiness-guide-dev-with-plugin.pdf
    └── ai-readiness-guide-dev-no-plugin.pdf
```

---

## Author & Company

**Russ Wittmann** — SVP of Technology, Silverback Marketing
[LinkedIn](https://www.linkedin.com/in/russwittmann/) · [X / Twitter](https://x.com/russwittmann)

[Silverback Marketing](https://silverbackmarketing.com) is an ROI-focused digital marketing agency (founded 2007, Queen Creek, Arizona) helping businesses grow through strategy, content, and technology. This skill was built as part of Silverback's AI-readiness service offering — helping clients get found in the age of AI search.

🔗 **[ai.silverbackmarketing.com](https://ai.silverbackmarketing.com)** · [silverbackmarketing.com](https://silverbackmarketing.com)

---

## License

MIT — free to use, modify, and distribute with attribution. See [`LICENSE`](LICENSE).
