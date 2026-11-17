# Fleece — Credit Card Research & Redemption

## Project Overview

**Fleece** is a credit card research and award redemption toolkit. Tagline: "Find the best card for deal saviors."

It has two surfaces:
1. **Streamlit chatbot** (`fleece.py`) — conversational AI assistant backed by OpenAI
2. **CLI** (`cli.py`) — 13 commands for card research, wallet analysis, MCC lookup, spending profile, and award redemption

Published on PyPI as [`fleece-cli`](https://pypi.org/project/fleece-cli/) · current version **0.4.0**

---

## Tech Stack

| Layer | Technology |
|---|---|
| Chatbot frontend | Streamlit |
| Chatbot LLM | OpenAI (gpt-3.5-turbo, gpt-4, gpt-4o) via LangChain |
| Chatbot memory | ConversationEntityMemory |
| CLI framework | Typer |
| Live research | Brave Search API |
| Card portfolio | SQLite (`fleece.db`) via `db.py` |
| MCC dataset | Bundled `mcc_codes.jsonl` (981 codes, offline) |
| Redemption URLs | `pointsyeah.py` (pure stdlib, no deps) |
| Language | Python 3.11+ |

---

## CLI Commands

### Research (requires `BRAVE_API_KEY`)
| Command | Description |
|---|---|
| `fleece card "<name>"` | Full card report — fees, welcome offer, rates, credits, benefits |
| `fleece rates "<name>"` | Earning rates by spend category |
| `fleece partners "<name>"` | Transfer partners, ratios, timing |
| `fleece credits "<name>"` | Statement credits and perks |
| `fleece news "<name>"` | Recent changes (past month, freshness-filtered) |
| `fleece compare "<A>" "<B>"` | Side-by-side comparison |
| `fleece wallet` | Portfolio analysis — coverage, overlaps, gaps, next-card suggestions |
| `fleece roi "<name>"` | First-year ROI estimate by spend profile |
| `fleece recommend "<profile>"` | Card recommendations for a spending profile |

### Redemption & Profile (no API key needed — work fully offline)
| Command | Description |
|---|---|
| `fleece mcc <code>` | Offline MCC code lookup (981 codes bundled). Add `--wallet` to cross-reference saved cards |
| `fleece flights <ORIGIN> <DEST> --date <YYYY-MM-DD>` | PointsYeah award flight search URL |
| `fleece hotels "<location>" --checkin <date> --checkout <date>` | PointsYeah award hotel search URL |
| `fleece profile show` | Display spending profile |
| `fleece profile set <field> <value>` | Set a profile field |
| `fleece profile unset <field>` | Clear a profile field |
| `fleece profile fields` | List all 10 profile fields |

All commands support `--json` for agent-friendly output and `-` to read arguments from stdin.

### BRAVE_API_KEY
Optional at startup — checked only when a research command actually runs. `mcc`, `flights`, `hotels`, and `profile` work with no key set.

### Spending Profile
Stored in `fleece.db` (table: `profile`). Fields: `dining_monthly`, `groceries_monthly`, `travel_monthly`, `gas_monthly`, `other_monthly`, `annual_fee_tolerance`, `points_programs`, `home_airport`, `goal`, `preferences`.

Once set, profile context is automatically injected into:
- `fleece roi` — pulls spend values when flags not passed
- `fleece wallet` — tailors gap analysis to the user's actual spend
- `fleece recommend` — prepends profile context to the search query

---

## Key Files

| File | Purpose |
|---|---|
| `cli.py` | Main CLI entry point (Typer app) |
| `fleece.py` | Streamlit chatbot app |
| `db.py` | SQLite helpers for card portfolio and spending profile (`fleece.db`) |
| `pointsyeah.py` | PointsYeah URL generation (pure stdlib, merged from archived `pointsyeah-cli`) |
| `mcc_codes.jsonl` | Bundled MCC dataset (981 codes, source: greggles/mcc-codes) |
| `tools/brave_client.py` | Brave Search API client |
| `tools/credit_card_tools.py` | LangChain tools for the chatbot |
| `pyproject.toml` | Package config — hatchling build, `fleece` entry point |
| `install.sh` | Installs skills for Claude Code, OpenClaw, Gemini CLI, Copilot, Cursor, Windsurf |
| `SKILL.md` | Root-level skill file for `npx skills add chenyuan99/fleece` (skills.sh registry) |
| `skills/fleece/SKILL.md` | skills.sh directory structure copy |
| `GEMINI.md` | Gemini CLI project context |
| `.github/copilot-instructions.md` | GitHub Copilot instructions |
| `.cursor/rules/fleece.mdc` | Cursor IDE rule |
| `.windsurfrules` | Windsurf rules |

---

## Agent Skills

### Universal install (55+ agents) — recommended
```bash
npx skills add chenyuan99/fleece
```
Installs to Claude Code, Cursor, GitHub Copilot, Gemini CLI, Windsurf, Cline, Codex, Warp, Kiro, Continue, Junie, and more in one command. Requires a valid `SKILL.md` at `skills/fleece/SKILL.md` in the repo root (already present).

### Claude Code (`/.claude/skills/`)
13 slash commands installed via `bash install.sh --claude`:

**Research:** `/fleece-card` `/fleece-rates` `/fleece-partners` `/fleece-credits` `/fleece-news` `/fleece-compare` `/fleece-wallet` `/fleece-roi` `/fleece-recommend`

**Redemption:** `/fleece-mcc` `/fleece-flights` `/fleece-hotels`

**Profile:** `/fleece-profile`

### Platform-specific install flags
| Flag | Platform | File installed |
|---|---|---|
| `--claude` | Claude Code | `.claude/skills/fleece-*.md` |
| `--agents` | OpenClaw / Codex | `.agents/skills/fleece/SKILL.md` |
| `--gemini` | Gemini CLI | `GEMINI.md` |
| `--copilot` | GitHub Copilot | `.github/copilot-instructions.md` |
| `--cursor` | Cursor | `.cursor/rules/fleece.mdc` |
| `--windsurf` | Windsurf | `.windsurfrules` |
| `--all` | All of the above | — |

### ClawHub / OpenClaw (`/.agents/skills/fleece/SKILL.md`)
Published on ClawHub as `fleece@1.6.0`. Install via `clawhub install fleece` or `bash install.sh --agents`.

### skills.sh / Vercel Agent Skills Registry
`SKILL.md` at repo root and `skills/fleece/SKILL.md` enable `npx skills add chenyuan99/fleece`. Installs to 55+ agents in one command.

> **IMPORTANT:** The frontmatter `description` field must never contain embedded quotes — they silently break YAML parsing in both ClawHub's vector indexer and the skills.sh CLI. Always use plain unquoted text.

---

## CI/CD

| Workflow | Trigger | Action |
|---|---|---|
| `publish.yml` | Push `v*` tag | Build and publish to PyPI via OIDC trusted publishing |
| `publish-skills.yml` | Push to `main` touching `.agents/skills/` or `.claude/skills/` | Publish to ClawHub via `CLAWHUB_TOKEN` secret |

GitHub environment `pypi` is required for the PyPI workflow (OIDC).

---

## Landing Page

`docs/` is served as GitHub Pages at **https://getfleece.io/**.

Contains `index.html`, `sitemap.xml`, `robots.txt`. Submitted to Google Search Console. JSON-LD structured data included.

SEO notes tracked in `docs/SEO.md`.

---

## Infrastructure Notes

- **Databricks**: No resources available. Do not suggest Databricks solutions until provisioned.
- **pointsyeah-cli**: Archived. All functionality merged into fleece (`pointsyeah.py`, `fleece flights`, `fleece hotels`).

---

## Development Notes

- Author: Yuan Chen
- Created: March 16, 2025
- Chatbot uses custom CSS styling (`style.css`)
- OpenAI API key entered via Streamlit sidebar — not stored

---

## Git Workflow

**Always ask before pushing.** Do not run `git push` without explicit user confirmation. Commits are fine, but pushing to remote requires approval each time.
