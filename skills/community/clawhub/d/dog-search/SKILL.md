---
name: dog-search
description: >
  Search Google via the ScrapingDog API using the bundled search.py CLI script.
  Use this skill whenever the user wants to search the web, look something up on Google,
  run a search query, find results for a topic, or do any kind of web/Google search —
  even if they don't explicitly say "use ScrapingDog" or "run search.py".
  Requires SCRAPINGDOG_API_KEY to be set in the environment.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPINGDOG_API_KEY
      bins:
        - python
    primaryEnv: SCRAPINGDOG_API_KEY
---

# dog-search

Run Google searches from the command line using the ScrapingDog API.

## Setup

Requires the `SCRAPINGDOG_API_KEY` environment variable to be set:

```bash
export SCRAPINGDOG_API_KEY=your_key_here
```

Install the dependency if not already present:

```bash
pip install requests
```

## Script location

The search script is bundled at: `scripts/search.py` (relative to this SKILL.md).

When using this skill, resolve the absolute path to `scripts/search.py` from the skill directory and run it with `python`.

## Usage

```bash
python scripts/search.py "your query"

python scripts/search.py "your query" --country uk --lang en
python scripts/search.py "your query" --json
```

## Arguments

| Argument | Default | Description |
|---|---|---|
| `query` | required | The search query string |
| `--country` | us | Country code (us, uk, de, fr, ...) |
| `--lang` | en | Language code (en, fr, de, ...) |
| `--json` | off | Print raw JSON response instead of formatted output |

## Workflow

1. Check that `SCRAPINGDOG_API_KEY` is set in the environment. If not, tell the user to set it and stop.
2. Resolve the path to `scripts/search.py` relative to this skill's directory.
3. Run the script with `python scripts/search.py "<query>"` plus any relevant flags.
4. Parse and present the results clearly to the user.

## Output format (default)

```
  Results for: "your query"

  ────────────────────────────────────────────────────────────

  [1] Result Title
      https://example.com/page
      Snippet describing the result...

  ────────────────────────────────────────────────────────────
  10 result(s)
```

## Error handling

- Missing API key → script exits with a clear message; tell the user to set `SCRAPINGDOG_API_KEY`
- HTTP error → script prints the status code and response body
- No results → script prints "No results found."
