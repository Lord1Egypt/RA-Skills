---
name: app-audit-lite
description: Runs a quick App Store / Google Play audit of one app with live AppGoat data - listing quality, ratings trend, recent complaints, keyword rankings, competitors and their recent changes - and ends with a prioritized fix list. Use when the user says "audit my app", "review my App Store listing", "why are my downloads dropping", "how does my app compare to competitors", "ASO check" or pastes an App Store / Google Play link and asks what to improve.
argument-hint: "<app> [country]"
license: MIT
---

# App audit (lite)

A 10-minute audit of one app from public store data: what the listing says, how users rate it,
what they complain about, which searches it wins, and what competitors changed recently. It ends
with at most 7 fixes, ordered by expected impact.

This is the cheap "lite" path (~25–40 credits), assembled from the AppGoat read tools. The full
App Audit is live as the `audit_app` MCP tool (`POST /v1/apps/{app}/audit`): an AI-written,
evidence-checked report with a 0–100 score, prioritised actions, metadata rewrites within the
character limits, ~20 probed search terms and a shareable report page. It takes 1–3 minutes:
`audit_app` waits about 25 s and returns an audit id, which `get_audit` follows up on (free). The
first audit of an organization is free, later ones cost 100 credits, and re-running the same app,
country and mode within 24 h returns the earlier audit for free.

## When to use

- The user wants an assessment of their own app or a competitor's ("audit", "teardown", "what should I fix").
- Before an ASO rewrite (run `aso-keywords-metadata-rewrite` afterwards for the metadata itself).
- Prefer `audit_app` instead when the user wants the full report or a link to share, or has not used
  their free audit yet (call it with `free_only: true` to run it only if it is free). Stay on this
  lite flow when credits are tight or for a quick check.
- Not for idea hunting (use `find-app-ideas`) or for turning reviews into tickets (use `reviews-to-github-issues`).

## Inputs

- `app` (required): anything that identifies the app - store URL, Apple id (`284882215`), Play package
  (`com.spotify.music`), bundle id or a name. If a name resolves to the wrong app (check the warning
  in the tool output), ask the user for the store link.
- `country` (optional, default `us`): two-letter storefront code. Audit one country per run.

## Steps

Call the AppGoat MCP tools in this order. Costs are AppGoat credits; every tool output ends with a
footer showing `credits_used` and `credits_remaining` - stop and tell the user if remaining credits
drop below 50. Without the MCP, use the REST equivalents in [reference/api.md](reference/api.md).

| # | Call | Credits | What you need from it |
|---|---|---|---|
| 1 | `get_app` {app, country, include: ["versions", "charts"]} | 1 (+1 if older than 7 days and refreshed) | title, subtitle, description, category, rating, ratings_count, histogram, version, updated_at, release notes of the last 5 versions, screenshots count, languages, chart positions, `linked` app in the other store |
| 2 | `get_app_history` {app, country} | 1 | rating and ratings_count over the last 90 days |
| 3 | `get_reviews` {app, country, rating: "1-2", limit: 100} | 1 (+1 refresh) | recent complaints; group by theme yourself |
| 4 | `get_reviews` {app, country, rating: "5", limit: 50} | 1 | what users love (words to reuse in the listing) |
| 5 | `get_app_keywords` {app, country, limit: 100} | 1 | ranked terms, rank, popularity, difficulty |
| 6 | `get_competitors` {app, country, limit: 5} | 1 | top 5 competitors |
| 7 | `get_app` {app: <competitor app_id>, store, country} for each of the 5 | 5 | competitor title, subtitle, rating, ratings_count, updated_at |
| 8 | `get_app_changes` {app: <competitor app_id>, store, field: "title,subtitle,description,screenshots,price,version", since: <today − 60 days>} for the top 3 | 3 | what competitors changed recently |
| 9 | `keyword_research` {terms: up to 10 high-popularity terms competitors rank for but the app does not (from step 5 vs competitor titles/subtitles), store, country, app} | 10 | popularity, difficulty, the app's rank and relevance per gap term |

Budget: about **25 credits** (up to ~40 with refreshes and a second reviews page). Do not page
through more reviews unless the user asks.

If a call answers that data is still being refreshed (`refreshing`, a `job_id`), call `get_job`
{id} (free) every few seconds until it is done, then repeat the original call once.

## Decision rules

Score each area Good / Needs work / Problem using these thresholds:

- **Rating**: Problem if rating < 4.0 or the 90-day history shows a drop ≥ 0.1; Needs work if
  4.0–4.4; Good if ≥ 4.5. Flag if 1★ share of the histogram > 15%.
- **Rating volume**: Needs work if ratings_count grew < 1% in 90 days while competitors' median
  ratings_count is ≥ 5× higher (prompt for ratings in the app).
- **Freshness**: Problem if updated_at > 180 days ago; Needs work if > 60 days. Release notes that
  are generic ("bug fixes and improvements") in ≥ 3 of the last 5 versions: Needs work.
- **Title / subtitle** (Apple 30 / 30 characters; Play title 30, short description 80): Needs work if
  either uses < 70% of its limit, if the title has no non-brand keyword, or if the subtitle repeats
  title words.
- **Keywords**: count ranked terms with rank ≤ 10 and popularity ≥ 30 ("winning"), and terms with
  rank 11–50 and popularity ≥ 30 ("striking distance"). Problem if winning = 0; every striking-distance
  term with relevance < 0.7 is a metadata opportunity.
- **Complaints**: a theme counts when ≥ 3 of the 1–2★ reviews mention it, or ≥ 1 mentions a crash,
  data loss, a billing/subscription problem or a login lockout. Unanswered 1–2★ reviews (no `reply`)
  > 50%: Needs work.
- **Competitors**: note every competitor that changed its title or subtitle in the last 60 days
  (they are targeting new terms) and any competitor with rating ≥ 0.3 higher than the app.
- **Localization**: Needs work if `languages` has 1 entry and any competitor has ≥ 5.

Fix list: at most 7 items, each tied to a finding above, ordered by (impact × ease). Crashes and
billing complaints always come first, then title/subtitle keyword gaps, then everything else.
Never invent numbers; if a value is missing, say "no data".

## Output format

```markdown
# App audit: <title> (<store>, <country>) - <date>

**Verdict:** <one sentence>

| Area | Status | Evidence |
|---|---|---|
| Rating | Good / Needs work / Problem | 4.6★ (42,310 ratings), −0.05 in 90 days, 1★ 6% |
| Freshness | … | v3.2.1, updated 12 days ago |
| Title & subtitle | … | "…" (24/30), "…" (18/30) |
| Keywords | … | 4 winning, 9 striking distance |
| Complaints | … | login loop (7), sync lost data (2) |
| Competitors | … | X changed subtitle to "…" on <date> |
| Localization | … | English only; 3 of 5 competitors ≥ 5 languages |

## Top fixes
1. **<fix>** - why (evidence), expected effect.
2. …

## Keyword opportunities
| Term | Popularity | Difficulty | Your rank | Relevance | Action |
|---|---|---|---|---|---|

## What users say
- Love: "<≤ 120-char quote>" (5★, v3.2)
- Hate: <theme> - "<quote>" (1★, v3.2)

## Competitors
| App | Rating | Ratings | Updated | Recent change |
|---|---|---|---|---|

_Credits used: <sum of the footers>._

**Automate this →** weekly competitor changes and review alerts: see the `reviews-to-github-issues`
playbook; metadata fixes: `aso-keywords-metadata-rewrite`.
```

## Automate it

Run the audit monthly and commit the report, so changes are visible in git history.

GitHub Action (`.github/workflows/appgoat-audit.yml`, secrets `ANTHROPIC_API_KEY` and `APPGOAT_API_KEY`):

```yaml
name: AppGoat monthly audit
on:
  schedule:
    - cron: "0 7 1 * *"
  workflow_dispatch:
permissions:
  contents: write
jobs:
  audit:
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
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Use the app-audit-lite skill for the app https://apps.apple.com/us/app/id000000000 in country us.
            Write the report to reports/audit-<YYYY-MM>.md (current month), then commit and push it.
          claude_args: |
            --mcp-config ${{ runner.temp }}/appgoat-mcp.json
            --allowedTools mcp__appgoat__get_app,mcp__appgoat__get_app_history,mcp__appgoat__get_reviews,mcp__appgoat__get_app_keywords,mcp__appgoat__get_competitors,mcp__appgoat__get_app_changes,mcp__appgoat__keyword_research,mcp__appgoat__get_job,Write,Bash(git:*)
```

Claude Code routine (paste into Claude Code with the AppGoat connector added):

```text
/schedule monthly on the 1st at 08:00 - Run the app-audit-lite playbook for <app link> in <country>. Compare it with last month's report in reports/, call out what improved and what got worse, and open a PR with the new report.
```
