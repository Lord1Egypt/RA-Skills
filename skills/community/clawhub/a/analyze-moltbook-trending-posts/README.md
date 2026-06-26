# Moltbook Trend Analysis

> This skill uses minimal compute -- offloading all gathering and analysis to scripts instead of burning tokens on number crunching. I made this for my duo agent setup; [RAG to Riches](https://www.moltbook.com/u/ragtoriches) & [G. Petti](https://www.moltbook.com/u/gpetti-music) -- [LLM Rappers](https://llmrapper.com) (pun intended), but figured the rest of the world might find this useful.

Fetch, analyze, and compare trending posts from [Moltbook](https://www.moltbook.com) -- the AI-agent social network. Built as an [OpenClaw](https://github.com/openclaw) skill.

## What It Does

Pulls live trending data from Moltbook's public API, analyzes virality patterns, and generates intelligence reports:

- **Trending post analysis** -- score velocity, engagement rates, content features
- **Author dominance tracking** -- who controls the trending page
- **Virality signal scoring** -- 10-point checklist benchmarked against 36,576+ posts
- **Snapshot comparison** -- track how the trending landscape changes over time
- **Actionable briefings** -- markdown reports with posting recommendations

No authentication required -- uses Moltbook's public trending endpoint.

## Quick Start

```bash
# Full briefing: fetch + analyze + report
bash scripts/full_run.sh
```

### Prerequisites

- `bash`, `curl`, `python3` (stdlib only -- no pip installs)
- Network access to `https://www.moltbook.com/api/v1`

## Usage

```bash
# Full pipeline
bash scripts/full_run.sh

# Fetch only (saves snapshot)
bash scripts/fetch_trends.sh

# Analyze a snapshot
python3 scripts/analyze_trends.py data/snapshots/SNAPSHOT.json

# Compare two snapshots
python3 scripts/compare_snapshots.py data/snapshots/OLD.json data/snapshots/NEW.json
```

## Output Structure

```
data/snapshots/   # Timestamped JSON snapshots of trending data
reports/          # Markdown analysis reports
```

## OpenClaw Skill

This is an OpenClaw skill. Install it via ClawHub or clone directly. See `SKILL.md` for full agent-facing documentation with `{baseDir}` template paths.

## Find This Skill Useful?

Support the [LLM Rappers](https://llmrapper.com) -- AI agents that rap, research, and ship code.

- [LLMRapper.com](https://llmrapper.com)
- [G. Petti on X](https://x.com/GPettyMusic)
- [G. Petti on YouTube](https://www.youtube.com/@GPetti)
- [G. Petti on TikTok](https://www.tiktok.com/@gpettimusic)
- [Context to Conquest (debut album)](https://soundcloud.com/g-petti-music/sets/context-to-conquest)

## License

MIT
