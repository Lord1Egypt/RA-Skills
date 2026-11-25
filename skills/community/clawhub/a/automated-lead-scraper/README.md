# Automated Lead Scraper — Agent Skill

Turns a list of company website URLs into a CSV of **publicly listed business contact emails**. Checkpointed (resume after interruption), polite (delays, ≤4 concurrent, stops on 429/403/503), website-only. Designed for skill-capable agents (Claude Code, Codex, Cursor, …) but fully usable by hand.

## Install
Requires **Node.js ≥ 18**.
```bash
cd skills/automated-lead-scraper
npm install
```
To use as an agent skill, copy/symlink this folder to your agent's skills directory (e.g. `~/.claude/skills/automated-lead-scraper/`). The agent reads `SKILL.md`.

## Quick start
```bash
# 1. validate + clean a URL list (CSV with a url column, or .txt one per line)
node scripts/validate-input.js examples/sample-input.csv --write-clean runs/demo/input.csv

# 2. scrape (plain output; add > runs/demo/run.log 2>&1 to log)
node scripts/email-scraper.js --workdir runs/demo

# 3. summary: completed / blocked / errors / pending
node scripts/summarize-run.js --workdir runs/demo
```
Interrupted? Re-run the **same** step-2 command to resume. Start over (old files archived, not deleted): add `--fresh`.

## CLI reference
| Command | Purpose |
|---|---|
| `node scripts/email-scraper.js [--workdir DIR] [--input FILE] [--concurrency 1-4] [--fresh] [--fancy]` | Run / resume |
| `node scripts/email-scraper.js --selftest` | Offline checks of email normalization (baseline 7/8, see notes) |
| `node scripts/validate-input.js FILE [--write-clean OUT.csv] [--force]` | Validate / clean URLs |
| `node scripts/summarize-run.js [--workdir DIR] [--json]` | Run summary |
| `npm test` | Offline end-to-end test suite (local fake sites; no internet needed) |

Exit codes: `0` ok · `2` input problem · `1` unexpected error.

## Input format
CSV with a header column named `url`, `website`, `link`, `domain` or `site`:
```csv
url
https://example.com
https://example.org
```
Bare domains are fine when you go through `validate-input.js` (it adds `https://`).

## Output files (in the workdir)
`output.csv` (results), `suspicious.csv` (typo-looking emails, flagged not fixed), `cache.json` (checkpoint). Column details: `references/output-columns.md`.

## Supported systems
Linux and macOS (Linux tested), Windows (paths and commands are cross-platform Node; **not tested on Windows**). No browser, no native modules.

## Limitations
- Static HTML only — emails rendered by JavaScript or hidden behind forms are not found.
- Does not read robots.txt; you are responsible for site terms and email law (CAN-SPAM, GDPR/PECR, CASL).
- Facebook search/login from the original project is intentionally **not** included (see `references/adaptation-notes.md`).
- Original-logic quirks kept as-is (blacklist substring matching may drop addresses like `jsmith@…`; selftest baseline 7/8). Details in the adaptation notes.
- ~12 s per URL average → 1000 URLs ≈ 3–4 h.

## Troubleshooting
See `references/troubleshooting.md`.

## License
MIT (add your own LICENSE file before publishing).
