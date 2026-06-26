# Anime Finder

`anime-finder` is a skill-first anime search and download helper built around one public entrypoint:

```bash
python3 scripts/workflow.py "用户原话或番名" [--episode N] [--latest-season] [--download] [--downloader ...] --json
```

The workflow now accepts raw user wording, normalizes intent, applies explicit user preferences, resolves anime identity with Bangumi when possible, searches Nyaa, ranks results, and either queues the best match or returns a magnet fallback.

## What It Optimizes For

- Better skill trigger coverage for `找番` / `追更` / `最新一集` / `最新一季第一集`
- Fewer follow-up questions through `intent + decision` output
- High-confidence auto-download when the request clearly asks to watch or download
- Explicit, local-only user preferences in `state/user_profile.json`
- Follow-up download checks like `刚才那个下载怎么样`

## Trigger Examples

These should usually trigger the skill:

- `帮我找一下 JOJO 最新一季第一集然后下载下来`
- `jojo latest season ep1 download`
- `柯南最新一集`
- `先找孤独摇滚第 3 集，别下载`
- `攻壳机动队只要磁力`
- `刚才那个下载怎么样`

More examples live in [`references/intent_examples.md`](./references/intent_examples.md).

## Public JSON Contract

`workflow.py --json` always returns:

- `status`
- `query`
- `verification`
- `search`
- `intent`
- `decision`

When a candidate exists, it also returns `best_result`.

### Status values

- `need_disambiguation`: one focused clarification is still required
- `no_results`: search completed, but nothing downloadable remained
- `ready`: a `best_result` exists and no download was executed
- `queued`: Transmission accepted the torrent, or the latest tracked task is still queryable
- `fallback_to_magnet`: a download request fell back to magnet/torrent output
- `blocked`: the workflow hit an API, local, or network blocker

### Decision fields

- `confidence`: `high` / `medium` / `low`
- `confirmation_required`: whether the agent should stop and ask exactly one question
- `autonomy_mode`: `auto_execute` / `ask_once` / `halt`
- `profile_applied`: which fields came from the persisted user profile
- `reason_codes`: machine-readable reasons behind the decision

## User Preferences

Runtime profile path:

```text
state/user_profile.json
```

Tracked template:

```text
state/user_profile.template.json
```

Current profile fields:

- `subtitle_pref`
- `resolution_order`
- `file_size_cap_gb`
- `downloader`
- `default_action`
- `auto_download_high_confidence`
- `preferred_release_groups`
- `blocked_release_groups`

Preference precedence is fixed:

```text
explicit request > CLI flags > user_profile > series_overrides defaults > built-in defaults
```

The workflow only writes profile state from explicit user wording such as `以后默认给我 1080p 简中`.

## Download Follow-Up

The workflow stores runtime download state in:

```text
state/last_download.json
```

That enables follow-up requests such as:

- `刚才那个下载怎么样`
- `有进度吗`
- `下好了没`

## Compatibility CLI

`find.sh` remains available for older usage:

```bash
./find.sh "JOJO" --latest-season --search-only
./find.sh "JOJO" 1 --latest-season
./find.sh "JOJO" 1 --latest-season --downloader cli-only
```

For agents and new integrations, prefer `workflow.py --json`.

## Project Layout

```text
anime-finder/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── references/
│   └── intent_examples.md
├── state/
│   └── user_profile.template.json
├── find.sh
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── intent.py
│   ├── workflow.py
│   ├── verify.py
│   ├── search_nyaa.py
│   └── data/
│       └── series_overrides.json
└── tests/
    ├── test_intent.py
    └── test_workflow.py
```

## Development

Static validation:

```bash
python3 -m py_compile scripts/intent.py scripts/verify.py scripts/search_nyaa.py scripts/workflow.py tests/test_intent.py tests/test_workflow.py
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" .
```

Offline tests:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

Manual smoke tests:

```bash
python3 scripts/workflow.py "帮我找一下 JOJO 最新一季第一集然后下载下来" --json
python3 scripts/workflow.py "刚才那个下载怎么样" --json
```

## Dependencies

- Required: Python 3.8+, bash
- Optional: `transmission-daemon`, `transmission-remote`

The project intentionally avoids third-party Python packages.
