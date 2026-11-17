---
name: competitive-landscape
description: "Map who wins an SEO market across many competitors: recurring ranking domains, their organic footprint, winning content formats, backlinks, local pack leaders, and open gaps. Use when the user asks who ranks for a topic or market, who their SEO competitors are, or where the openings are. For a deep dive on one named competitor, use competitor-analysis instead."
---

# HarborRank Competitive Landscape

## Goal

Answer: "Who is winning this SEO market, what content is working for them, and where are the openings?"

Use this when the user wants a market-level view across several competitors. For a deep dive on one domain, use `competitor-analysis`.

## Step 0: Check connection

Before any other step, confirm the HarborRank MCP tools are loaded. Look for `get_domain_overview` or `list_leads` among your tools, including deferred tools you can load (the name may carry a prefix such as `mcp__harborrank__`). If they are there, call `whoami`: it uses no credits, confirms the user is signed in, and returns `creditsRemaining` for budgeting the run. Do not call a research tool to test the connection.

If neither tool is available, or `whoami` fails because the user is not signed in, tell the user plainly: "HarborRank isn't connected, so I can't pull live HarborRank data yet." Then tell them how to connect it:

- Claude Code with the HarborRank plugin: run `/mcp`, choose `harborrank`, and sign in.
- Claude Code without the plugin: run `claude mcp add --transport http --scope user harborrank https://app.harborrank.com/mcp`, then `/mcp` to sign in.
- Claude on the web, desktop or Cowork: open Customize, then Connectors, search for HarborRank, choose Connect, and sign in. New accounts start with a 7-day free trial.
- Cursor with the HarborRank plugin: open Cursor Settings, then MCP, and sign in to `harborrank`.
- Gemini CLI with the HarborRank extension: run `/mcp auth harborrank`.
- Other clients: add `https://app.harborrank.com/mcp` as a remote MCP server. Setup for each client is at https://harborrank.com/docs/mcp.

Tell them what happens when they connect: they sign in to HarborRank with Google or email and start a 7-day free trial. Then they come back to this conversation and say "connected", and you pick up the task where it stopped.

Do not stop there. Continue in fallback mode (below). If the user connects HarborRank mid-task, run Step 0 again and switch to the full workflow.

### Plan limits

On hosted HarborRank, research tools spend credits. New accounts start with a 7-day free trial (1,000 research credits, one project); paid plans start at $29/month with 15,000 credits. Search Console, saved keywords, rank tracker reads, and site crawls use no credits. A keyword search costs about 50 credits and a domain overview about 80. Full backlinks, lead research (`research_lead`), and Lighthouse checks need a paid plan; on Free, the backlinks tools return a preview (totals and the top 3 referring domains, about 50 credits) with an upgrade link.

- If `creditsRemaining` will not cover the planned calls, give the user the estimate and ask before spending. Use the free tools first.
- If a tool replies that a feature "is included in paid plans", tell the user once which feature needs a paid plan and pass on the upgrade link from the reply, skip that tool for the rest of the run, and finish with the other evidence. Do not retry it.
- If a tool fails for insufficient credits, stop making paid calls, tell the user, and finish with free tools and the data you already have. If `whoami` warns that credits are low, say so before a large run.
- If a HarborRank tool says the free trial hasn't started, or that credits ran out, give the user the link from that reply exactly as written, as a clickable link, and wait for them to say they're done before calling HarborRank again. Don't switch to answering without HarborRank data unless they ask you to.
- If the user asks to upgrade, change plan or buy credits, call `get_upgrade_link` (no credits) and give them the link. They pay on HarborRank by card; never say the upgrade is done until `whoami` shows the new plan.
- When `whoami` returns `mode: "self-hosted"`, there are no plan gates.

### Fallback mode (no HarborRank connection)

Use this mode only when Step 0 finds no connection. It works from web search, page reading, and files the user provides.

**Can still do**

- Run the market query set through web search and note which domains keep appearing.
- Group those domains by type: direct competitors, publishers, directories, communities, resources.
- Read the leaders' sites to identify the content formats, themes, and positioning that are working.
- Call the result directional.

**Must not estimate**

Traffic, search volume, keyword difficulty, CPC, keyword counts, rankings, backlink counts, Maps pack positions, and Q&A counts. Write `unknown` for each. A web search shows which pages appeared for a query when you searched, not their Google ranking: report it as "appeared in web search", never as a position.

**Output**

- Start with the label **Web-evidence only: no HarborRank data.**
- Name the source (URL or file) of every figure you report.
- End, after any recommended next workflow, with one sentence that names the numbers this report is missing: "Connect HarborRank (start with a 7-day free trial) to add each leader's organic footprint, traffic, and backlink strength." Do not add more sales copy than that.

## Required inputs

If the project's SEO folder has `seo-context.md` (see `seo-context`), read it first for the site, market, audience, competitors and goals, and ask only for what it doesn't cover.

- `projectId`
- Topic, seed keywords, market/category, or user's domain
- Optional known competitors
- Optional location/language

## HarborRank MCP tools

- `research_keywords`: discover representative market queries.
- `get_keyword_metrics`: validate known query sets with volume, difficulty, intent, and trends.
- `get_serp_results`: identify recurring ranking domains across target queries.
- `find_serp_competitors`: compare domains competing across supplied keywords; use this before manual SERP counting when a keyword set is available.
- `get_domain_overview`: size organic footprint for candidate leaders.
- `get_search_console_performance`: when the user's own domain is in the comparison and Search Console is connected, anchor their position with first-party clicks/impressions/CTR rather than third-party estimates.
- `get_ranked_keywords`: find exact ranking keywords, URLs, ranks, intents, and SERP result types for leaders.
- `get_backlinks_overview`: compare backlink/referring-domain strength where relevant.
- `search_local_businesses`, `get_local_serp_results`, and `get_google_business_questions`: use for local SEO markets where proximity, Maps rankings, business categories, reviews, or Google Q&A affect who is winning.
- `create_share_report`: publish the finished work as a read-only page at a shareable link (see "Shareable report" below). Only after the user agrees.

## Workflow

1. Define the market query set:
   - Use provided keywords, or call `research_keywords` to build 5-10 representative queries.
   - Include mixed intent: informational, commercial, comparison, and tool/software terms when applicable.
   - For local SEO, include neighborhood/city/service-area queries and identify the priority locations or coordinates.
2. If the query set is already known, use `get_keyword_metrics` to validate relative demand and difficulty and `find_serp_competitors` to identify recurring domains at scale.
3. For local SEO, call `search_local_businesses` and `get_local_serp_results` for the highest-priority location(s) before synthesizing winners. Use `get_serp_results` as a complement for organic pages, not as the only local evidence.
4. Call `get_serp_results` for representative queries when live SERP composition, ranking URLs, or SERP features need inspection. Send at most 10 queries per call.
5. Identify recurring domains and group them by type:
   - Direct product competitors
   - Publishers/media
   - Marketplaces/directories
   - Communities/forums
   - Documentation/resources
6. For the strongest recurring domains, call `get_domain_overview`; default to the top 3-5 domains before expanding.
7. For direct competitors and relevant publishers, call `get_ranked_keywords`.
8. Use `get_backlinks_overview` when backlink authority appears important or the user asks why a domain is winning. On Free this returns a preview (totals and the top 3 referring domains); use it, note that the full profile needs a paid plan, and continue with SERP and domain evidence.
9. Synthesize patterns: content types, themes, SERP formats, local-pack signals, authority advantages, and underserved angles.

## Output format

Start with the market read:

- Market leaders
- Most winnable opportunity area
- Biggest barrier to ranking

Then include:

| Domain | Type | Why they matter | Organic footprint | Winning themes | Weakness/gap |
| ------ | ---- | --------------- | ----------------- | -------------- | ------------ |

Add:

- Query set used
- Content formats that are working
- Keyword/theme gaps
- Backlink or authority observations

- **Next workflow:** end with one recommended next workflow, the reason for it, and the input it starts from. Default: `competitor-analysis` on the most beatable direct competitor among the leaders, named explicitly.
- **Check back:** end with one dated follow-up: the date (today plus 30 days, written out, for example "Monday, November 9") and the exact question to ask then: "Who moved in the <market> landscape since <today's date>?" Say in one line why it needs that wait: a month of ranking changes is enough to see who is gaining. Add it to the `Follow-ups` list in the SEO folder's `README.md` (create the list if it is missing) so the next session finds it. One follow-up only; don't add reminders or repeat it. If scheduled tasks are available (Cowork and the Claude apps on paid plans), offer once to make this a weekly scheduled task instead, named for the site, so the check runs by itself; the user reviews and confirms the schedule.
- **Where the output goes:** the report as `competitors/landscape-<market-slug>-<YYYY-MM-DD>.md`. Save it in the project's SEO folder (see `seo-project-setup`); if there is none, ask once whether to create one or where to save instead. If the user prefers a doc or a sheet and a docs or spreadsheet tool is available, put reports in a doc and tables in a sheet instead. Tell the user where it was saved.
- **Shareable report:** once the work is done, offer one time to publish it as a shareable report with `create_share_report`: a read-only page at a link the user can send to a client, a boss or a teammate, no sign-in needed. Write it from this output: findings first, then next steps, then the supporting table. Publish only after the user says yes, and leave out their Search Console and Google Analytics numbers unless they agree to share them. Give them the link; `delete_share_report` removes it.

## Guardrails

- Distinguish SEO competitors from business competitors.
- Do not overstate exact traffic when HarborRank returns estimates.
- If using a small query set, call the result directional.
- Do not assume a publisher is a product competitor; label domain types clearly.
- For local markets, distinguish organic-page winners from Maps/local-pack winners.
