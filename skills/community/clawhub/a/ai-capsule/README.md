# AI Capsule

[中文文档](README.zh.md)

An AI agent skill that scores and ranks your daily AI news feed based on what *you* actually care about.

Tell it your role and your familiar areas — it scores every article against your profile and ranks them so the most relevant ones appear first. Nothing is filtered out: every article makes it into the digest, just in the right order. An Agent engineer and a fine-tuning researcher reading the same 40 articles will get completely different ranked digests.

Built around AI industry sources by default (HuggingFace, OpenAI, Anthropic, DeepMind, HN, Reddit…), but the source system is industry-agnostic — drop in a `sources/finance.yaml` or `sources/crypto.yaml` and it works the same way.

Works with **Claude Code** and **OpenClaw**. Any agent runtime that supports `SKILL.md` can use it.

Every day it pulls from 16 sources (HuggingFace Papers, OpenAI, Anthropic, DeepMind, Simon Willison, GitHub Trending, HN, Reddit, and more), scores each article across 7 dimensions (Relevance, Utility, Novelty, Depth, Wow, Perspective, Cross-domain), and applies a **Personal Fit** score calibrated to your background. The result is a ranked daily report where the most useful articles for *you* float to the top.

![daily report example](https://via.placeholder.com/800x400?text=daily+report+screenshot)

---

## How it works

Each article gets a **RUND+WPS** score:

| Dimension | What it measures |
|-----------|-----------------|
| R — Relevance | Does it match your tech stack? |
| U — Utility | Can you do something with it? |
| N — Novelty | Is this actually new? |
| D — Depth | Paper/source-level or blog-level? |
| W — Wow | Counter-intuitive or elegant? |
| P — Perspective | Does it shift how you think? |
| S — Cross-domain | Unexpected combination? |

A **Personal Fit (F)** multiplier then re-ranks by how close each article is to your `familiar_areas`. An Agent paper ranks higher for you than for someone who only does fine-tuning.

Action tags tell you what to do with each card:
- `TRY` — has a GitHub repo or runnable code
- `READ` — deep content worth your full attention
- `SCAN` — 30-second skim is enough

---

## Requirements

- [Claude Code](https://claude.ai/code) or [OpenClaw](https://openclaw.ai)
- Python 3.9+

---

## Installation

### Claude Code

```
/plugin marketplace add WebPudge/ai-capsule
/plugin install ai-capsule@ai-capsule
```

Then run the environment setup:

```bash
bash ~/.claude/plugins/ai-capsule/scripts/setup-env.sh
```

Then say `daily`.

### OpenClaw

```bash
openclaw skills install ai-capsule
cd ~/.openclaw/skills/ai-capsule
bash scripts/setup-env.sh
```

Then say `daily` in your OpenClaw session.

---

Claude will walk you through a short setup (role, familiar areas, output language) and write your config to `~/.ai-capsule/config.yaml`. Your data lives in `~/.ai-capsule/data/` — separate from the skill, safe across updates.

---

## Usage

Say any of these to Claude:

| What you say | What happens |
|-------------|-------------|
| `daily` | Pull today's AI news, score everything, output ranked digest |
| `reconfigure` | Re-run the setup questionnaire |
| Paste a URL | Score that single article |
| Paste article text | Score that single article |

---

## Daily digest example

Real output from a June 2026 digest — engineer profile, familiar with LLM app development / RAG / Agent frameworks:

---

### #1 ★★★★☆ 6.9/10 · [Conan — Claude Code Visual Control Panel](https://conan.sh)

🔗 [https://conan.sh](https://conan.sh)
📌 **Product Hunt Daily** · engineer · learn mode · 🎯 **TRY**
`Relevance:9` `Utility:8` `Novelty:7` `Depth:5` | `Wow:6` `Perspective:6` `Cross-domain:3`

- **Relevance:** A direct companion tool for Claude Code, immediately useful for engineers who use it heavily
- **Utility:** Downloadable macOS app, dmg available on GitHub Releases, usable today
- **Novelty:** A visual HUD for Claude Code fills a real gap — context window monitoring solves a daily pain point
- **Depth:** Product page, clear feature descriptions but no technical implementation details
- **Wow:** Context monitoring solves a real developer pain point more elegantly than expected
- **Perspective:** Visualizing runtime state as a HUD reframes the experience from "black box" to observable
- **Cross-domain:** No cross-domain inspiration

**Summary:** Native macOS app that adds a real-time HUD to Claude Code — Timeline (streaming prompt/tool call view), Context window usage monitor, Pulse throughput, Skills & MCP visualizer. $29 one-time.

**Value:** You use Claude Code heavily — Conan immediately shows how much context each conversation consumes and which tools fire how often, so you know when to /compact before the context fills up silently.

---

### #3 ★★★★☆ 7.0/10 · [Mapping SQLite result columns back to their source table.column](https://simonwillison.net/2026/Jun/13/sqlite-column-provenance/)

🔗 [https://simonwillison.net/2026/Jun/13/sqlite-column-provenance/](https://simonwillison.net/2026/Jun/13/sqlite-column-provenance/)
📌 **Simon Willison** · engineer · learn mode · 🎯 **TRY**
`Relevance:7` `Utility:8` `Novelty:7` `Depth:7` | `Wow:5` `Perspective:5` `Cross-domain:3`

- **Relevance:** SQL result provenance is a real problem in RAG and Agent tool-call workflows
- **Utility:** All three approaches include code; column_provenance.py on GitHub is ready to use
- **Novelty:** Bridging ctypes to sqlite3_column_table_name() is a trick most developers don't know
- **Depth:** Covers the rationale and tradeoffs of three approaches with working code
- **Wow:** The ctypes bypass of Python's stdlib has some elegance, though it's a known pattern
- **Perspective:** Reveals that SQLite internally computes this via SQLITE_ENABLE_COLUMN_METADATA — a hidden capability
- **Cross-domain:** No cross-domain perspective

**Summary:** Simon Willison uses Claude Code to research how to map SQL query result columns back to their source table.column. Explores three approaches — apsw, ctypes bridge to SQLite C API, and EXPLAIN analysis — with code published on GitHub.

**Value:** When your RAG Agent executes SQL and needs to explain the results, column_provenance.py lets it return "users.name from the users table" instead of a bare column name — a direct upgrade for multi-table JOIN explainability.

---

### #5 ★★★★☆ 6.9/10 · [Why AI hasn't replaced software engineers, and won't](https://simonwillison.net/2026/Jun/14/why-ai-hasnt-replaced-software-engineers/)

🔗 [https://simonwillison.net/2026/Jun/14/why-ai-hasnt-replaced-software-engineers/](https://simonwillison.net/2026/Jun/14/why-ai-hasnt-replaced-software-engineers/)
📌 **Simon Willison** · engineer · learn mode · 🎯 **READ**
`Relevance:8` `Utility:6` `Novelty:6` `Depth:7` | `Wow:6` `Perspective:8` `Cross-domain:3`

- **Relevance:** Directly addresses AI's impact on software engineers — a core concern for engineer readers
- **Utility:** Provides the NY WARN Act data as a concrete source, and the decision/verification/understanding framework
- **Novelty:** Counters the popular "threshold theory" with three specific cognitive bottlenecks
- **Depth:** Arvind Narayanan's deep analysis with academic grounding; Simon adds his own perspective
- **Wow:** No counter-intuitive finding — the three-part framework lands in expected territory
- **Perspective:** "Decision-making and accountability matter more than code input speed" reframes what engineers do
- **Cross-domain:** Pulls in labor economics data (WARN Act) to analyze a tech trend

**Summary:** Arvind Narayanan and Sayash Kappor argue that AI hasn't replaced software engineers because of three irreducible bottlenecks: decision-making and specification, verification and accountability, and deep contextual understanding. Backed by NY WARN Act filings showing zero companies attributed layoffs to AI.

**Value:** You're an AI application engineer — this piece articulates clearly why you haven't been replaced. Decision-making and verification are exactly what you do every day; use this framework to explain AI tool boundaries to PMs, managers, or clients.

---

The same 31 articles ranked for a fine-tuning researcher would look completely different — the SQLite and Agent tooling pieces above would rank lower, and model architecture or training papers would float to the top.

---

## Configuration

Config lives at `~/.ai-capsule/config.yaml` (created on first run):

```yaml
initialized: true
default_identity: engineer      # engineer | pm | researcher | learner | founder
default_purpose: learn          # learn | solve | scout
output_language: en             # en | zh | any language name
familiar_areas:
  - LLM application development
  - RAG
  - Agent frameworks
data_dir: ~/.ai-capsule/data
```

Override config path: `export AI_CAPSULE_CONFIG=/path/to/config.yaml`

### Example: LLM application engineer

```yaml
initialized: true
default_identity: engineer
default_purpose: learn
output_language: en
familiar_areas:
  - LLM application development
  - RAG
  - Agent frameworks
  - Prompt Engineering
dislikes: pure marketing content, trend articles with no code
data_dir: ~/.ai-capsule/data
```

With this config, articles about RAG retrieval strategies or Agent tool-calling rank higher than general AI industry news. A paper on speech recognition scores low on Personal Fit even if the overall quality is high — it still appears in the digest, just near the bottom.

---

## Data sources

### Built-in AI sources (16 out of the box)

**RSS (auto-fetched):** HuggingFace Papers · OpenAI Blog · Microsoft Research · Ben's Bites · Hacker News

**URL fetch:** Anthropic (3 feeds) · Google DeepMind · Meta AI · Simon Willison · Eugene Yan · Chip Huyen · Product Hunt Daily · GitHub Trending

**X/Twitter:** @Zai_org · @dotey · @_akhaliq · @omarsar0 · @karpathy (latest 5 posts each)

**Search:** Reddit LocalLLaMA

## Proxy configuration for X/Twitter

If you cannot access X/Twitter directly from your network, the `twitter-cli` tool uses `curl-cffi` which does not read system proxy settings automatically. Set the `https_proxy` environment variable:

```bash
export https_proxy=http://127.0.0.1:7890
```

Or add it to your shell profile (`~/.zshrc` / `~/.bashrc`):

```bash
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
```

`fetch.py` auto-detects `https_proxy` / `HTTPS_PROXY` and forwards it to the `twitter-cli` subprocess. If neither env var is set, it will also try common local proxy ports (ClashX 7890, Surge 6152, etc.) automatically.

### Extend to other industries

Sources are organized by industry file. Add a new industry by creating `sources/{industry}.yaml`:

```bash
# Add a source to the AI industry list
bash scripts/add-source.sh --industry ai --type rss --name "My Blog" --url https://example.com/feed

# Start a new industry (e.g. finance, crypto, security)
cp sources/ai.yaml sources/finance.yaml
# then edit sources/finance.yaml with finance-specific feeds

# Run daily digest for a specific industry
# say "daily --industry finance" to Claude
```

Four source types are supported in any industry:

| Type | Fetched by | Use for |
|------|-----------|---------|
| `rss` | `fetch.py` automatically | RSS/Atom feeds, APIs |
| `webfetch` | Agent at runtime | Blogs, leaderboards, pages without RSS |
| `tavily` | Agent at runtime | Reddit, forums, search-based discovery |
| `twitter` | `fetch.py` automatically | X/Twitter account timeline — uses twitter-cli + browser-cookie3 |

---

## Agent compatibility

Works with any agent that can fetch URLs and run Bash:

| Runtime | Fetch tool used |
|---------|----------------|
| Claude Code | `WebFetch` |
| Codex / shell agents | `curl` + python parse |
| Tavily-enabled agents | `tavily_extract` |
| OpenClaw | falls back to system Python gracefully |

---

## Project structure

```
ai-capsule/
  SKILL.md              # skill entrypoint (instructions for Claude)
  fetch.py              # RSS/API fetcher
  sources_extract.py    # source config reader
  requirements.txt
  scripts/
    setup-env.sh        # one-time Python venv setup
    add-source.sh       # add a data source
  sections/
    scoring.md          # RUND+WPS+F scoring framework
    output-format.md    # card format spec
    daily-mode.md       # daily mode execution flow
  sources/
    ai.yaml             # AI industry source list
```

User data (`~/.ai-capsule/`):
```
config.yaml             # your profile and preferences
data/
  daily-YYYY-MM-DD.md   # daily reports
  history.jsonl         # all scored articles
  dedup-titles.txt      # seen titles (prevents re-scoring)
```

---

## Privacy

**X/Twitter source:** When you add an X/Twitter data source, the daily fetch uses `browser-cookie3` to read Chrome's local SQLite cookie file on your machine. Only cookies for the `x.com` domain are extracted. These cookies are passed to `twitter-cli` as environment variables in memory — they are never written to disk, uploaded, or shared. If the cookies expire, the daily report will prompt you to re-login at x.com.

All other data sources fetch public content via RSS, HTTP requests, or search APIs. Your config and scored history are stored locally in `~/.ai-capsule/`.

## License

MIT
