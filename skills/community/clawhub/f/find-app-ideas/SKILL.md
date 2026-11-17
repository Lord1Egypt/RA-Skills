---
name: find-app-ideas
description: Finds underserved App Store / Google Play niches with live AppGoat data - search demand (keyword popularity) against weak supply (low ratings, abandoned incumbents, few strong apps) - and returns a ranked shortlist of app ideas with evidence and user pain points. Use when the user says "find me an app idea", "what app should I build", "underserved niches", "app opportunities in <category>", "is there demand for a <type> app" or wants to validate an idea before building.
argument-hint: "[niche] [store] [country]"
license: MIT
---

# Find app ideas

Turns "what should I build?" into a ranked shortlist of niches where people search a lot and the
existing apps are weak. Each pick comes with the numbers behind it and what users of the current
apps complain about, so the idea has a wedge.

Everything is built from the public read tools (charts, keyword research, apps, search, reviews),
so it runs on every plan.

## When to use

- The user has no idea yet, or a broad area ("health", "something for teachers").
- The user has an idea and wants to know if there is demand and room ("validate a habit tracker for ADHD").
- Not for improving an existing app (use `app-audit-lite` or `aso-keywords-metadata-rewrite`).

## Inputs

- `niche` (optional): a seed area or idea, e.g. `habit tracker`, `plant care`, `finance for couples`.
  Without it, start from the charts (step 1).
- `store` (optional, default `apple`): `apple` or `play`. Run once per store; demand differs.
- `country` (optional, default `us`).

Ask at most one question before starting: whether the user has constraints (solo dev, no backend,
paid vs free). Otherwise assume a solo developer shipping in 4–8 weeks.

## Steps

Costs in AppGoat credits; watch the footer of each tool result. Without the MCP, use the REST
equivalents in [reference/api.md](reference/api.md).

1. **Seeds.**
   - With `niche`: write 8–10 seed terms a user would type into the store (2–3 words, no brand names).
   - Without `niche`: `get_charts` {store, country, chart: "free", category} and {chart: "grossing"} for
     4 categories (Apple genre ids: 6013 Health & Fitness, 6007 Productivity, 6017 Education,
     6012 Lifestyle; Play: HEALTH_AND_FITNESS, PRODUCTIVITY, EDUCATION, LIFESTYLE) - 8 calls, **8 credits**.
     Take apps with `is_new` or `delta` ≥ 10 and the grossing apps outside the top 20 free; derive
     8–10 seed terms from what they do.
2. **Expand.** `keyword_research` {terms: 5 seeds, store, country, include: ["related", "suggestions"]},
   twice for 10 seeds - **5 per seed, 50 credits**. Collect related terms and suggestions.
3. **Measure candidates.** Pick the 25 most specific candidate terms (prefer 2–4 words that describe
   a job, e.g. "adhd planner", not "planner"). `keyword_research` {terms: 25 terms, store, country,
   include: ["top_apps"]} - **1 per keyword, 25 credits**. Terms that come back `pending` are being
   measured: call again with just those after a minute (charged again only for those).
4. **Check supply.** For the 8 best terms by the demand rule below: `get_app` {app: <app_id>, store,
   country} for the top 3 `top_apps` of each - **~24 credits** - to read `updated_at`, rating,
   ratings_count, price, has_iap. Optionally `search_apps` {q: term, store, limit: 20} - **1 each** -
   to count how many apps target it directly by title.
5. **Find the wedge.** For the 5 best niches: `get_reviews` {app: <top incumbent>, store, country,
   rating: "1-2", limit: 100} for the top 2 incumbents - **~10 credits**. Group complaints into themes.
6. **Rank and write up** (no calls).

Budget: about **150–200 credits** per run (up to ~250 with refreshes and re-measured pending terms).
Stop early if `credits_remaining` falls below the remaining budget and tell the user.

## Decision rules

- **Demand:** popularity ≥ 30 (5–100 scale). Popularity ≥ 50 with difficulty ≥ 70 is a "big but
  crowded" market: keep it only if supply is weak.
- **Difficulty:** ≤ 55 to be a candidate; ≤ 35 is "easy".
- **Weak supply** (at least one must hold):
  - median rating of the top 10 < 4.3, or
  - ≥ 3 of the top 10 not updated in 12 months, or
  - ≤ 2 of the top 10 have the term (or a close variant) in their title, or
  - the top 3 average < 5,000 ratings (Apple) / < 100k installs (Play).
- **Monetization signal:** at least one top-10 app has IAP or is paid, or the term's apps appear in
  the grossing chart. Without it, label the idea "hobby / growth only".
- **Idea score** (rank by it): `popularity × (1 − difficulty/100) × supply_weakness`, where
  `supply_weakness` = 1 + 0.25 per weak-supply condition met (max 2).
- **Wedge:** a pick needs a complaint theme mentioned in ≥ 5 of the incumbents' 1–2★ reviews, or a
  missing feature named in ≥ 3. No wedge: drop it to the "watch" list.
- Exclude: regulated or high-liability niches (medical diagnosis, lending, gambling), anything that
  depends on another company's private API, and terms that are mostly a brand name.
- Return 3–5 picks. If fewer qualify, say so and show the near misses with the rule they failed.

## Output format

```markdown
# App ideas: <niche or "chart scan"> (<store>, <country>) - <date>

| # | Idea | Key term | Popularity | Difficulty | Top-10 median ★ | Stale incumbents | Score |
|---|---|---|---|---|---|---|---|
| 1 | ADHD-friendly habit tracker | adhd habit tracker | 41 | 28 | 4.1 | 4 of 10 | 39.4 |

## 1. <Idea>
- **Demand:** <term> (pop 41), <term 2> (pop 33), related: <terms>
- **Supply:** top apps <name (4.0★, updated 2024-11)>, …; only 1 of 10 has the term in its title.
- **Wedge:** users complain about <theme> ("<≤ 120-char quote>", 2★) and <theme>.
- **Money:** <who charges what>.
- **MVP in one line:** <scope a solo dev can ship in 4-8 weeks>.
- **Launch keywords:** title "<≤ 30 chars>", subtitle "<≤ 30 chars>".

## Near misses
- <term>: popularity 58 but difficulty 81 and top apps average 4.7★.

_Credits used: <sum of the footers>._

**Automate this →** re-run monthly to see new movers; once you pick one, track its keywords with
`track_keywords` and run `aso-keywords-metadata-rewrite` before launch.
```

## Automate it

A monthly scan that opens an issue with new picks.

GitHub Action (`.github/workflows/appgoat-ideas.yml`, secrets `ANTHROPIC_API_KEY`, `APPGOAT_API_KEY`):

```yaml
name: AppGoat app ideas
on:
  schedule:
    - cron: "0 8 1 * *"
  workflow_dispatch:
    inputs:
      niche:
        description: Seed niche (optional)
        required: false
permissions:
  contents: read
  issues: write
jobs:
  ideas:
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
            Use the find-app-ideas skill with niche "${{ inputs.niche }}" (empty = chart scan), store apple, country us.
            Open one GitHub issue titled "App ideas <YYYY-MM>" with the report as the body (gh issue create).
          claude_args: |
            --mcp-config ${{ runner.temp }}/appgoat-mcp.json
            --allowedTools mcp__appgoat__get_charts,mcp__appgoat__keyword_research,mcp__appgoat__get_app,mcp__appgoat__search_apps,mcp__appgoat__get_reviews,mcp__appgoat__get_job,Bash(gh issue create:*)
```

Claude Code routine:

```text
/schedule monthly on the 1st at 09:00 - Run the find-app-ideas playbook for the niche "<niche>" on the App Store, US. Compare with last month's picks (in ideas/), highlight new entries and dropped ones, and save the report as ideas/<YYYY-MM>.md.
```
