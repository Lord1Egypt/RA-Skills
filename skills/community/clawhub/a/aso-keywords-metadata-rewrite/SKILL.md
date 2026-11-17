---
name: aso-keywords-metadata-rewrite
description: Researches App Store / Google Play keywords for one app with live AppGoat data (current ranks, competitor keyword gaps, popularity, difficulty, relevance) and rewrites the title, subtitle, keyword field and description within the store character limits. Use when the user says "improve my ASO", "rewrite my app title / subtitle", "which keywords should I target", "fill my keyword field", "optimize my App Store listing", "ASO for <app>" or prepares a new version's metadata.
argument-hint: "<app> [country]"
license: MIT
---

# ASO keywords → metadata rewrite

Finds the search terms an app can realistically win and rewrites its metadata to target them,
staying inside every store limit. The output is ready to paste into App Store Connect or Play Console.

## When to use

- The user wants new metadata or keyword picks for an existing app (or a pre-launch app with a draft listing).
- After `app-audit-lite` flagged title, subtitle or keyword problems.
- Not for review analysis or idea hunting.

## Inputs

- `app` (required): store URL, Apple id, Play package, bundle id or name. For an unreleased app,
  ask for the draft title, subtitle and description and the closest competitor instead.
- `country` (optional, default `us`): the storefront to optimize. Metadata is per locale; run once per country.

Ask the user for the brand name to keep (default: the part of the current title before ":" or "-")
and anything that must not change.

## Steps

Costs in AppGoat credits (see the footer of each tool result). Without the MCP, use the REST
equivalents in [reference/api.md](reference/api.md).

1. `get_app` {app, country} - **1** (+1 if refreshed). Note title, subtitle (Play: short
   description), description, category, languages.
2. `get_app_keywords` {app, country, limit: 200} - **1**. Current ranked terms with rank, popularity, difficulty.
3. `get_competitors` {app, country, limit: 8} - **1**.
4. `get_app_keywords` {app: <competitor app_id>, store, country, max_rank: 20, limit: 100} for the
   top 5 competitors - **5**. Terms competitors rank top 20 for are your candidate pool.
5. Build a candidate list of ≤ 50 terms: competitor terms the app does not rank top 20 for, plus
   current terms ranked 11–50, plus 3–5 seeds you derive from the app's core job.
   `keyword_research` {terms: 5 seeds, store, country, include: ["related"]} - **5 per seed, ~25**.
6. `keyword_research` {terms: ≤ 25 candidates, store, country, app} - **1 per keyword**, twice for
   50 candidates - **~50**. Returns popularity, difficulty, the app's rank and `relevance` (0–1:
   1 = in title, 0.7 = subtitle, 0.4 = description) per term. Re-call `pending` terms after a minute.
7. Write the metadata (no calls), then validate it with
   `python3 scripts/check_metadata.py --store <apple|play> --title "…" --subtitle "…" --keywords "…"`
   (Play: `--short "…" --full-file description.txt`). Fix every error it reports before answering.
8. Optional: `track_keywords` {terms: the 10–20 chosen terms, store, countries: [country]} - **0
   credits**, uses keyword slots - so the next run can measure the effect with `get_keyword_ranks`.
   Ask before tracking.

Budget: about **40–80 credits** per country.

## Decision rules

- **Candidate filter:** popularity ≥ 20; drop competitor brand names and terms that misdescribe the app.
- **Pick score:** `popularity × fit × (1 − difficulty/100) × gap`, where `fit` = 1 if the term
  describes what the app does, 0.5 if adjacent, 0 otherwise (your judgment, not `relevance`), and
  `gap` = 1.5 if the app ranks 11–50 (striking distance), 1.2 if it ranks 51+ or not at all and
  difficulty ≤ 50, 1.0 if already top 10 (keep, do not chase), 0.6 if difficulty > 75.
- **Placement** (most weight first): title > subtitle > keyword field (Apple) / short description
  (Play) > description. Put the top 1–2 terms in the title next to the brand, the next 2–3 in the subtitle.
- **Keep what wins:** never remove a term the app ranks top 10 for with popularity ≥ 30 from the
  field that holds it, unless the user agrees to the trade.
- **Apple limits:** title ≤ 30 characters, subtitle ≤ 30, keyword field ≤ 100 bytes, comma
  separated without spaces after commas, no word repeated from the title or subtitle (Apple combines
  them), no plurals of words already present, no competitor brands, no "app" or "free".
- **Play limits:** title ≤ 30, short description ≤ 80, full description ≤ 4000. Play indexes the
  description: use each top term 2–4 times in natural sentences, never a keyword list.
- **Style:** readable title first, keywords second. No ALL CAPS, no emoji in the title, no claims
  ("#1", "best") the user cannot back up.
- Give 2 variants for title + subtitle (safe and aggressive) and one keyword field.

## Output format

```markdown
# ASO rewrite: <app> (<store>, <country>) - <date>

## Target keywords
| Term | Popularity | Difficulty | Rank now | Relevance now | Score | Placed in |
|---|---|---|---|---|---|---|
| habit tracker | 48 | 62 | 23 | 0.4 | 27.4 | title |

## Metadata
| Field | Current | Proposed (A, safe) | Proposed (B, aggressive) |
|---|---|---|---|
| Title (≤ 30) | Streaks (7) | Streaks: Habit Tracker (22) | … |
| Subtitle (≤ 30) | … | … | … |
| Keyword field (≤ 100 bytes) | n/a | routine,daily,goals,… (97) | |

## Description
<rewritten description, or the first 3 lines for Apple, which is what users see>

## Why
- <term> moves from the description (0.4) to the title (1.0); you rank 23 with popularity 48.
- Dropped <term>: popularity 8.

## Measure it
Track these terms (`track_keywords`) and compare ranks 2 and 4 weeks after the release.

_check_metadata.py: OK · Credits used: <sum>._
```

## Automate it

Re-run after every competitor metadata change, or monthly.

GitHub Action (`.github/workflows/appgoat-aso.yml`): opens a PR with `metadata/<country>.md` so the
change is reviewed before you paste it into the store console.

```yaml
name: AppGoat ASO refresh
on:
  schedule:
    - cron: "0 7 15 * *"
  workflow_dispatch:
permissions:
  contents: write
  pull-requests: write
jobs:
  aso:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install AppGoat playbooks and MCP config
        env:
          APPGOAT_API_KEY: ${{ secrets.APPGOAT_API_KEY }}
        run: |
          git clone --depth 1 https://github.com/appgoat/skills /tmp/appgoat-skills
          mkdir -p .claude/skills
          cp -r /tmp/appgoat-skills/skills/* .claude/skills/
          # Hosted AppGoat MCP server; the key goes into a file, not the command line.
          jq -n --arg key "$APPGOAT_API_KEY" \
            '{mcpServers: {appgoat: {type: "http", url: "https://api.appgoat.ai/mcp", headers: {"x-api-key": $key}}}}' \
            > "$RUNNER_TEMP/appgoat-mcp.json"
      - uses: anthropics/claude-code-action@v1
        env:
          GH_TOKEN: ${{ github.token }}
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Use the aso-keywords-metadata-rewrite skill for <app link>, country us. Do not call track_keywords.
            Write the result to metadata/us.md, commit it on a new branch and open a pull request with gh pr create.
          claude_args: |
            --mcp-config ${{ runner.temp }}/appgoat-mcp.json
            --allowedTools mcp__appgoat__get_app,mcp__appgoat__get_app_keywords,mcp__appgoat__get_competitors,mcp__appgoat__keyword_research,mcp__appgoat__get_job,Write,Bash(python3 .claude/skills/aso-keywords-metadata-rewrite/scripts/check_metadata.py:*),Bash(git:*),Bash(gh pr create:*)
```

Claude Code routine:

```text
/schedule monthly on the 15th at 09:00 - Run the aso-keywords-metadata-rewrite playbook for <app link> in us. Compare the ranks of our tracked keywords (list_tracked_keywords, get_keyword_ranks) with last month and propose a new title/subtitle/keyword field only if a target term lost ≥ 5 positions or a competitor took it.
```
