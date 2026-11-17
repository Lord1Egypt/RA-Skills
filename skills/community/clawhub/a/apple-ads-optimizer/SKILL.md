---
name: apple-ads-optimizer
description: Optimizes the user's Apple Ads (Search Ads) campaigns through their connected Apple Ads account - reads the last 14 days of keyword and search term reports, raises bids on keywords that convert under the target CPA (capped +30% per run), lowers or pauses keywords that spend without installs, adds converting search terms as exact keywords and wasteful ones as negatives - every change a dry run with a diff the user approves. Use when the user says "optimize my Apple Ads", "Apple Search Ads bids", "which keywords are wasting money", "add negative keywords", "harvest search terms", "lower my CPA" or sets up a weekly ads review.
argument-hint: "[campaign] [target_cpa]"
license: MIT
---

# Apple Ads optimizer

A weekly pass over Apple Ads campaigns with explicit rules: move budget toward keywords that
install under the target cost per acquisition (CPA), away from keywords and search terms that
spend without installs, and promote proven search terms to exact keywords. Every change goes
through `propose_action` (dry run, free) and is applied only after the user approves it.

## When to use

- The user runs Apple Ads for their own app and connected the Apple Ads account in AppGoat
  (https://dash.appgoat.ai/connections, provider `apple_ads`, Apple Ads Platform API). An API user
  with access to several ad accounts connects one `ad_account_id` per connection; pick the
  connection whose account runs the app's campaigns.
- Not for organic keyword research (use `aso-keywords-metadata-rewrite`) or Google Ads.

## Inputs

- `campaign` (optional): a campaign name or id. Default: every campaign with status `ENABLED`;
  ask which ones when there are more than five.
- `target_cpa` (optional): the most the user wants to pay per install, in the campaign currency.
  **Ask for it if missing**; if they don't know, suggest the median CPA of the converting keywords
  from step 3 and get a yes before using it. Also ask for the daily budget they are comfortable with.

Window: the last 14 full days (`end` = yesterday, `start` = end − 13 days, UTC).
Limits per run: at most **25 bid changes, 15 new keywords and 25 negatives** per campaign.

## Steps

Costs in AppGoat credits. Without the MCP, use the REST equivalents in [reference/api.md](reference/api.md).

1. `list_connections` {provider: "apple_ads"} - **0**. Keep `status: active`; `mode: read_only`
   can only dry-run (say so). None: send the user to https://dash.appgoat.ai/connections and stop.
2. `read_connection` {id, what: "ads", view: "campaigns"} - **1**. Campaign ids, status, app
   (adam id), countries, daily budget. Pick the campaigns.
3. Per campaign:
   - `read_connection` {id, what: "ads", view: "ad_groups", campaign_id} - **1** (ad group ids, default bids).
   - `read_connection` {id, what: "ads", view: "report", level: "keywords", campaign_id, start, end} - **1**:
     per keyword impressions, taps, installs, spend, avg CPT, avg CPA, keyword id, ad group id, bid.
   - `read_connection` {id, what: "ads", view: "report", level: "searchterms", campaign_id, start, end} - **1**:
     the search terms that triggered the ads, with the keyword that matched them.
   - `read_connection` {id, what: "ads", view: "negatives", campaign_id} - **1** (existing negatives).
   - For ad groups you will add keywords to: `read_connection` {view: "keywords", campaign_id, ad_group_id} - **1** each.
4. Optional, for search terms you cannot judge: `keyword_research` {terms: ≤ 25 terms, store:
   "apple", country: <campaign country>} - **1 per term**. Popularity 5–100 shows whether a term
   has real search volume; `include: ["top_apps"]` shows which apps win it (relevance check).
5. Apply the decision rules (no calls) and build three lists: bid changes, new exact keywords, negatives.
6. Propose them as dry runs, one action per ad group and type, with `playbook: "apple-ads-optimizer"` - **0**:
   - `propose_action` {type: "ads.keyword.bid", connection, params: {campaign_id, ad_group_id,
     keywords: [{id, bid}] or [{id, status: "PAUSED"}], max_increase: 0.3}} (status is
     `ENABLED` or `PAUSED`; `ENABLED` resumes a paused keyword)
   - `propose_action` {type: "ads.keyword.add", connection, params: {campaign_id, ad_group_id,
     keywords: [{text, match_type: "EXACT", bid}]}}
   - `propose_action` {type: "ads.negative.add", connection, params: {campaign_id, ad_group_id,
     keywords: [{text, match_type: "EXACT"}]}}
   The diffs show current → new bid per keyword; warnings flag bid jumps above `max_increase` and
   negatives that would block an enabled keyword.
7. Show the user the summary table (see Output format) with each action id and the expected effect,
   and ask which to apply ("all", "only bids", "all except negatives in ad group X").
8. `apply_action` {id} for each approved action - **1 per applied action**. `pending_approval` →
   give the user the `approve_url`; "needs approval by a person" → hand over the link, don't retry;
   "account changed" (someone edited bids meanwhile) → show the new diff, re-run step 3 for that
   ad group rather than forcing. `reject_action` {id, reason} the declined ones - **0**.
9. Report what changed and when to look again (7 days).

Budget: **~5–8 credits per campaign** to read + 1 per applied action (dry runs are free).

## Decision rules

Let `T` = target CPA. Only act on rows with enough data: **taps ≥ 10** or **spend ≥ T**.

- **Raise bid** when installs ≥ 3 and CPA ≤ 0.8 × T: new bid = current × min(1.30, T / CPA × 0.9),
  rounded to 0.05. Never more than **+30% per run**; skip keywords already at the user's max CPT.
- **Hold** when CPA is within 0.8–1.2 × T, or the data threshold is not met.
- **Lower bid** when installs ≥ 1 and CPA > 1.2 × T: new bid = current × max(0.70, T / CPA), i.e.
  at most −30% per run.
- **Pause** (`status: "PAUSED"`) when installs = 0 and spend ≥ 2 × T. Lower by 30% instead when
  installs = 0 and spend is between T and 2 × T, or when the keyword is the app's brand name.
- **Add as EXACT keyword** a search term with installs ≥ 2 and CPA ≤ T that is not already a
  keyword (any match type) in the ad group. Bid = its avg CPT × 1.1 (or the ad group default when
  the CPT is missing). Put it in the user's exact-match ad group when they have one, else the ad
  group where it converted. Skip "(low volume terms)" rows: Apple hides those terms.
- **Add as negative (EXACT, ad group level)** a search term with taps ≥ 10 and installs = 0 and
  spend ≥ T, or one that is clearly irrelevant (another product, a different meaning, a job or
  piracy query) regardless of spend. Prefer EXACT negatives; BROAD only for clearly irrelevant
  words and only with the user's explicit agreement.
- **Never negate** a term that converts (installs ≥ 1 in the window), that equals an enabled
  keyword in any ad group of the campaign, or the app's own brand. A guardrail warning about a
  blocked keyword means: drop that negative.
- **Budget:** if the proposed raises would push daily spend past the user's budget (estimate:
  current daily spend × (1 + weighted bid increase)), scale the raises down; never change campaign budgets.
- Changes compound: one run per week, and never re-raise a keyword raised in the last 7 days
  (check `get_action` history or ask).

## Output format

```markdown
# Apple Ads optimizer: <campaign> (<country>) - <start> → <end>, target CPA <T> <cur>

Spend <s> · installs <i> · CPA <c> · <k> keywords, <n> search terms with data

| Change | Ad group | Item | Now | Proposed | Why (14 d) | Action |
|---|---|---|---|---|---|---|
| Raise bid | Exact | habit tracker [EXACT] | 1.00 | 1.30 (+30%) | 14 installs, CPA 1.80 | act_… |
| Pause | Broad | free planner [BROAD] | 0.90 | paused | 0 installs, spend 11.20 | act_… |
| Add keyword | Exact | streak app [EXACT] | – | 0.85 | search term: 4 installs, CPA 2.10 | act_… |
| Negative | Broad | planner printable [EXACT] | – | negative | 22 taps, 0 installs | act_… |

Guardrail warnings: <none | list>.
Reply "apply all", "only bids", or name rows to skip.
```

Run report: what was applied, what waits for approval (links), and "Re-run in 7 days; the bid
changes need about a week of data." Credits used: <sum>.

## Automate it

Weekly proposals that a person approves in the dashboard. The run calls `apply_action` once per
action, which submits it for approval (or applies it when the org has a Studio auto-apply rule for
the type); nothing changes in Apple Ads until someone approves it at https://dash.appgoat.ai/approvals.

GitHub Action (`.github/workflows/appgoat-apple-ads.yml`, secrets `ANTHROPIC_API_KEY`, `APPGOAT_API_KEY`):

```yaml
name: AppGoat Apple Ads optimizer
on:
  schedule:
    - cron: "0 6 * * 1"
  workflow_dispatch:
permissions:
  contents: read
jobs:
  ads:
    runs-on: ubuntu-latest
    steps:
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
            Use the apple-ads-optimizer skill for all enabled campaigns with target CPA <amount> <currency>
            and daily budget <amount>. This is an unattended run: instead of asking in step 7, call apply_action
            once for every proposed action without guardrail warnings (this submits it for approval in the
            dashboard) and reject_action the others with the reason. Never call apply_action with force.
          claude_args: |
            --mcp-config ${{ runner.temp }}/appgoat-mcp.json
            --allowedTools mcp__appgoat__list_connections,mcp__appgoat__read_connection,mcp__appgoat__keyword_research,mcp__appgoat__propose_action,mcp__appgoat__apply_action,mcp__appgoat__reject_action,mcp__appgoat__get_action
```

Claude Code routine:

```text
/schedule mondays 08:00 - Run the apple-ads-optimizer playbook for my enabled Apple Ads campaigns, target CPA <amount>. Submit the proposed changes for approval (apply_action once each) and send me the summary table and the approvals link.
```
