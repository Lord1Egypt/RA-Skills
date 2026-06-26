# arXiv XHS Daily Operations

## Inputs

- arXiv feed categories: configurable in `config/topics.json` (default: `cs.AI`, `cs.CL`)
- Topic configuration: `config/topics.json`

The fetcher first tries local-today papers. If none are available yet because arXiv has not rolled over, it falls back to the latest available announcement day in that category.

## Outputs

For each run, the skill writes into:

- `data/<topic>/<date>/raw/`
- `data/<topic>/<date>/processed/`

Key files:

- `papers.json`
- `matched_papers.json`
- `notes.md`
- `post_draft.json`
- `cover.png`
- `publish_result.txt` when publishing

Current default cover style is a light-background research card with custom typography.

## Environment

Publishing uses:

- `MCPORTER_CONFIG_PATH`

If unset, scripts default to:

- `/Users/ailor/.openclaw/workspace/config/mcporter.json`

## Typical Commands

Dry run:

```bash
cd /path/to/skills/arxiv-xhs-daily
python3 scripts/run_daily.py --topic diffusion_llm --dry-run
```

Publish:

```bash
cd /path/to/skills/arxiv-xhs-daily
python3 scripts/run_daily.py --topic diffusion_llm --publish
```

## Adding Topics

Add a new topic entry with:

- `display_name`
- `keywords`
- `negative_keywords`
- `post_title_prefix`
- `post_hashtags`
- `default_cover_image`
- `max_matches`

This is the main migration / extension interface. If you want other paper directions, add new topic keys such as:

- `llm_safety`
- `agent_memory`
- `test_time_scaling`
- `multi_agent`
- `diffusion_reasoning`

## Changing arXiv Domains

To survey other arXiv slices, edit:

- `sources.categories`

Examples:

- `cs.LG`
- `cs.IR`
- `stat.ML`
- `cs.CV`
- `cs.RO`

You can mix multiple categories in one run.

## Scheduling

Cron example:

```bash
30 9 * * * cd /path/to/skills/arxiv-xhs-daily && MCPORTER_CONFIG_PATH=/path/to/mcporter.json /usr/bin/python3 scripts/run_daily.py --topic diffusion_llm --publish >> /path/to/skills/arxiv-xhs-daily/data/logs/diffusion_llm.log 2>&1
```
