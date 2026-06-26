# DYK Command Reference

## Data files

| File | Purpose |
|------|---------|
| `~/.openclaw/dyk-facts.json` | Local cache of fetched hooks, served history, and score records |
| `~/.openclaw/dyk-prefs.json` | User tag preferences used to score and rank hooks |

## Serve a fact

```bash
python3 {baseDir}/scripts/dyk.py
```

**Fact served:**
```
Did you know that [fact]?

[URL]
```

**No facts remaining:**
```
No more facts to share today; check back tomorrow!
```

**Error:**
```
Something went wrong with the fact-fetching; please try again later.
```

## Refresh the cache

```bash
python3 {baseDir}/scripts/fetch_hooks.py
```

Fetches the latest hooks from Wikipedia and appends them to `~/.openclaw/dyk-facts.json` with `"tags": null`. No-op if a refresh isn't due yet. If it exits non-zero, stop and report the error.

## Write tags to the cache

Tagging is a two-step process: the agent reads the untagged hooks and assigns tags itself, then writes the results to a temporary JSON file and applies them to the cache using:

```bash
python3 {baseDir}/scripts/write_tags.py --json-file /tmp/dyk-tags.json
```

The JSON file must be an array of entries. `domain` is an array (a hook can belong to multiple domains); `tone` is a single string. `low_confidence` is a boolean — set to `true` if the hook's topic or style was hard to determine.

```json
[
  {"url": "https://en.wikipedia.org/wiki/Example",
   "domain": ["science"], "tone": "surprising", "low_confidence": false}
]
```

Hooks that are already tagged are skipped — safe to re-run. If it exits non-zero, report the error.

## Manage preferences

Preferences are stored in `~/.openclaw/dyk-prefs.json` and control how hooks are scored. Two dimensions are supported: `domain` (topic area) and `tone` (style/mood). Valid tag values for each are defined in `{baseDir}/references/tags.csv`.

`list`, `get`, and `set` all require the prefs file to exist — if they report "no prefs file found", run `init` first.

```bash
# Create prefs file with all tags set to neutral. Fails if already exists.
python3 {baseDir}/scripts/prefs.py init

# Show all current preferences
python3 {baseDir}/scripts/prefs.py list

# Get a single preference
python3 {baseDir}/scripts/prefs.py get domain science

# Set a preference (value: like | neutral | dislike)
python3 {baseDir}/scripts/prefs.py set domain science like
python3 {baseDir}/scripts/prefs.py set tone dark dislike
```

## Explain a fact choice

To explain why a fact was chosen, read `~/.openclaw/dyk-facts.json` and find the hook with the most recent `returned_at` timestamp. Its `served_score` field contains the exact score breakdown from the moment it was served.

To compare against facts that were not chosen, each unchosen hook has a `candidate_score` field with the same structure.

> **Warning:** `candidate_score` is overwritten on every run. It reflects the most recent evaluation and may not match what was calculated when the fact was originally passed over — for example, if preferences have changed since.

### Score fields

Both `served_score` and `candidate_score` are objects with the following fields:

| Field | What it means |
|---|---|
| `domain` | Points from the user's domain tag preferences (positive = liked tags matched, negative = disliked) |
| `tone` | Points from the user's tone tag preference |
| `repetition_penalty` | Deduction for sharing a domain tag with the previous fact |
| `freshness` | Bonus for being from the most recently fetched batch |
| `multi_link` | Bonus for having more than one source link |
| `brevity` | Bonus for being a short fact |
| `total` | Sum of all components |

