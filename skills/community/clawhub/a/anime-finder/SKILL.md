---
name: anime-finder
description: >
  Find anime releases and handle the whole request end to end. Use when the user asks to 找番、
  追更、看最新一集、拿最新一季第一集、帮我下载、只要磁力、先找资源别下载、或者查看刚才下载怎么样；
  also use it for mixed Chinese/English wording, shorthand, aliases, and raw user utterances instead of clean titles.
---

# Anime Finder

Prefer the single workflow entrypoint and pass the raw user request when possible:

```bash
python3 "$SKILL_DIR/scripts/workflow.py" "用户原话或番名" [--episode N] [--latest-season] [--download] [--prefer-4k] [--json]
```

`find.sh` still exists, but it is compatibility glue only.

## Agent Workflow

1. Pass the user utterance into `workflow.py --json`.
2. Read top-level `status`, `intent`, and `decision` before digging into debug details.
3. If `decision.confirmation_required` is `true`, ask at most one question.
4. If `intent.action` is `status`, trust the workflow to read the last known download state; do not reconstruct it yourself.
5. If the user explicitly wants only a magnet link, pass `--downloader cli-only` or let the raw utterance express it.

## Stable Fields Worth Reading

- `status`
- `intent`
- `decision`
- `best_result`
- `verification.match` / `verification.alternatives`
- `search.search_queries`
- `search.available_seasons`
- `search.resolved_latest_season`
- `download.status`
- `summary`

## Status Rules

- `need_disambiguation`: stop and ask one focused question
- `no_results`: search finished, but nothing downloadable remained
- `ready`: `best_result` is available and no download was executed
- `queued`: Transmission accepted the torrent or the last tracked task is still queryable
- `fallback_to_magnet`: the workflow intentionally returned magnet/torrent output instead of queueing
- `blocked`: local or network blockers prevented progress

## Intent And Preference Rules

- `scripts/intent.py` is the normalization layer. It extracts `title`, `episode`, `season`, `latest_episode`, `latest_season`, `action`, quality/subtitle/downloader preferences, confidence, and missing fields.
- `scripts/data/series_overrides.json` remains the source of truth for franchises whose Bangumi names, user wording, and Nyaa season numbering drift apart.
- Runtime user preferences live in `state/user_profile.json`. Only explicit user wording should write to it. The tracked template is `state/user_profile.template.json`.
- Follow-up download queries read `state/last_download.json`; treat that file as runtime state, not repo content.

## Example Requests

- `帮我找一下 JOJO 最新一季第一集然后下载下来`
- `jojo latest season ep1`
- `先找孤独摇滚第三集，别下载`
- `攻壳机动队只要磁力`
- `刚才那个下载怎么样`

More trigger examples live in [references/intent_examples.md](./references/intent_examples.md).
