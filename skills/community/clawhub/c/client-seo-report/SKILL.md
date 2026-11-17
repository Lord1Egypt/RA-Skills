---
name: client-seo-report
description: "Produce a monthly (or custom-period) SEO report for a client or boss: what changed in clicks, impressions and positions versus the previous period and last year, which pages and queries drove the change, rank tracker movement, conversions from organic search when Google Analytics is connected, work done this period, and the next priorities, written for a non-SEO reader and published as a shareable report link. Use when the user asks for a monthly SEO report, a client report, an SEO results summary, what changed this month, or a report for their boss. For agencies and freelancers reporting to clients and in-house marketers reporting up. To diagnose a traffic drop in depth, use seo-audit instead."
---

# HarborRank Client SEO Report

## Goal

Turn a period of Search Console, Analytics and rank tracker data into a one-page report a client or boss can read in two minutes: what changed, why (as far as the data shows), what was done, and what comes next. The reader is not an SEO. Every number has a source, and every claim about cause is labelled as evidence or inference.

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

Most of this report is free: Search Console performance and rank tracker reads use no credits. The Google Analytics tools charge a small flat amount per call: `get_analytics_report` and `get_ai_referral_traffic` about 10 credits each, `get_landing_page_performance` about 25.

- If `creditsRemaining` will not cover the planned calls, give the user the estimate and ask before spending. Use the free tools first.
- If a tool replies that a feature "is included in paid plans", tell the user once which feature needs a paid plan and pass on the upgrade link from the reply, skip that tool for the rest of the run, and finish with the other evidence. Do not retry it.
- If a tool fails for insufficient credits, stop making paid calls, tell the user, and finish with free tools and the data you already have. If `whoami` warns that credits are low, say so before a large run.
- If a HarborRank tool says the free trial hasn't started, or that credits ran out, give the user the link from that reply exactly as written, as a clickable link, and wait for them to say they're done before calling HarborRank again. Don't switch to answering without HarborRank data unless they ask you to.
- If the user asks to upgrade, change plan or buy credits, call `get_upgrade_link` (no credits) and give them the link. They pay on HarborRank by card; never say the upgrade is done until `whoami` shows the new plan.
- When `whoami` returns `mode: "self-hosted"`, there are no plan gates.

### Fallback mode (no HarborRank connection)

Use this mode only when Step 0 finds no connection. It works from web search, page reading, and files the user provides.

**Can still do**

- Build the report from the user's Search Console exports (Performance report with "Compare" dates set: Queries, Pages and Dates tabs), Google Analytics exports, and any rank tracker export they provide. Those figures are the user's own data; report them with the file as the source.
- Compile the work done this period from the SEO folder (audits, keyword files, past reports) and what the user tells you.
- Read the pages that gained or lost the most, to describe what is on them now.
- Write the summary, the change tables and the next priorities, and save the report as a file.

**Must not estimate**

Traffic, clicks, impressions, conversions, search volume, keyword difficulty, keyword counts, rankings, backlink counts, Maps pack positions, and Q&A counts. Write `unknown` for each. A web search shows which pages appeared for a query when you searched, not their Google ranking: report it as "appeared in web search", never as a position. Do not fill a missing comparison period with a guess; say which export would supply it.

**Output**

- Start with the label **Web-evidence only: no HarborRank data.**
- Name the source (URL or file) of every figure you report.
- End, after any recommended next workflow, with one sentence that names the numbers this report is missing: "Connect HarborRank (start with a 7-day free trial) to pull this report's Search Console, Google Analytics and rank tracker numbers live each month." Do not add more sales copy than that.

## Required inputs

- `projectId` (from `list_projects`)
- The reporting period (default: the last complete calendar month that ended at least 3 days ago)
- The audience (client or boss) and what they care about most, if not already in `seo-context.md`
- Work done this period, if it is not in the SEO folder

## HarborRank MCP tools

- `get_search_console_performance`: clicks, impressions, CTR and average position by `query`, `page`, `country`, `device` or `date`, for explicit `startDate`/`endDate` (Pacific Time). Up to 1,000 rows per call; paginate with `startRow` when `hasMore` is true. Data goes back 16 months. Free.
- `get_landing_page_performance`: Search Console clicks joined with Google Analytics organic sessions, engagement, key events (conversions) and revenue per landing page; also lists pages that earn Google clicks but never show up in Analytics. Needs Google Analytics connected.
- `get_analytics_report`: sessions, users, key events and revenue by channel, landing page, date and more, with optional `compareTo` (`previous_period` or `previous_year`). Needs Google Analytics connected.
- `get_ai_referral_traffic`: visits, key events and revenue from AI assistants such as ChatGPT and Perplexity, with optional `compareTo`. Needs Google Analytics connected.
- `get_rank_tracker`: without `trackerId`, lists the project's trackers; with it, the latest position and the previous check's position per keyword, desktop and mobile. Free.
- `list_share_reports`: reports already published, with links and view counts. Use it to find last period's report.
- `create_share_report`: publish the finished report as a read-only page at a shareable link (see "Shareable report" below). Only after the user agrees.

## Workflow

If the project's SEO folder has `seo-context.md`, read it first for the site, market, audience, competitors and goals; otherwise ask only what this workflow needs.

1. Call `list_projects` and pick the client's project. Read last period's report from `reports/` in the SEO folder, if there is one, so this report continues its story and checks last period's priorities.
2. Set three windows of equal length with matching weekdays, none including the last 3 days:
   - **This period:** the reporting period.
   - **Previous period:** the same number of days, shifted back by the smallest whole number of weeks that avoids overlap (28 days for a 28-day period, 35 days for a 29 to 35-day calendar month).
   - **Last year:** the same dates shifted back 364 days (52 weeks), if Search Console data reaches that far.
   Example for October 2026 (31 days): previous period August 27 to September 26, 2026; last year October 2 to November 1, 2025.
   If the client insists on calendar months, use them as the headline but say the months differ in length and weekday mix, and add clicks per day.
3. For each window, call `get_search_console_performance` with explicit `startDate` and `endDate`: once with `dimensions: ["date"]` for totals, once with `["page"]`, once with `["query"]`. Compute the change in clicks, impressions, CTR and average position.
4. Find the drivers: the 5 pages and 5 queries with the largest click gains and losses versus the previous period. For each, note what moved (impressions, position or CTR) using the classification in `seo-audit` Workflow B step 4.
5. If Google Analytics is connected, call `get_landing_page_performance` for this period to tie organic clicks to key events and revenue per page. For the period totals, call `get_analytics_report` with `dimensions: ["sessionDefaultChannelGroup"]`, `metrics: ["sessions", "keyEvents", "totalRevenue"]` and the Organic Search filter. `compareTo` shifts by exact days or a calendar year, so it only matches weekdays for a 28-day period; otherwise call once per window with explicit dates. Add `get_ai_referral_traffic` with `compareTo` if AI visits matter to this client. Report any page in `pagesMissingFromAnalytics` as a tracking problem, not a traffic one.
6. Call `get_rank_tracker` to list trackers, then with each `trackerId`. Its previous position is the previous check, not the start of the period; for month-over-month movement, compare with the positions in last period's report.
7. List the work done this period with dates: pages published or changed, fixes shipped, links earned. Match each item to the data only where the timing and the pages line up.
8. Separate what changed from why. A change is evidence when the numbers show it. A cause is inference unless something confirms it (a fix on that exact page before the gain, a tracked keyword moving on that page). Write "likely" or "consistent with" for inferences, and say when the data does not explain a change.
9. Pick the next priorities: 3 at most, each tied to a finding in this report.
10. Draft the report and show it to the user before saving or sharing.

## Output format

One page, plain language, no SEO jargon without a short gloss ("average position, where the site shows up in Google results, 1 is the top").

- **Summary:** three lines. What happened to organic search this period, the main reason as far as the data shows, and the one thing to do next.
- **Headline numbers:**

| Metric | This period | Previous period | Change | Same period last year | Change |
| ------ | ----------: | --------------: | -----: | --------------------: | -----: |

  Rows: clicks, impressions, CTR, average position, and organic sessions and key events when Analytics is connected.
- **What drove it:** the top gaining and losing pages and queries, each with what moved and the likely cause, labelled evidence or inference.
- **Rankings:** tracked keywords that moved most, up and down.
- **Work done this period:** dated list.
- **Next priorities:** up to 3, each with the reason from this report.
- **Notes on the data:** windows used, the 3-day lag, Analytics thresholding or sampling if the tool flagged it, and anything not checked.

- **Next workflow:** end with one recommended next workflow, the reason for it, and the input it starts from. If clicks fell on specific pages, recommend `seo-audit` (traffic-drop diagnosis) on those pages. If a competitor took the lost queries, recommend `competitor-analysis` on that domain. Otherwise recommend `keyword-research` on the striking-distance queries (positions 5 to 20) from this period.
- **Check back:** end with one dated follow-up: the date (the first business day on or after the 4th of the month after the next period ends, written out, for example "Friday, December 4") and the exact question to ask then: "Write the <month> SEO report for <domain>." Say in one line why it needs that wait: the period has to end and Search Console needs about 3 days to finish its data, and the Search Console and rank tracker reads use no credits. Add it to the `Follow-ups` list in the SEO folder's `README.md` (create the list if it is missing) so the next session finds it. One follow-up only; don't add reminders or repeat it. If scheduled tasks are available (Cowork and the Claude apps on paid plans), offer once to make this a monthly scheduled task instead, named for the site, so the report drafts itself; the user reviews and confirms the schedule.
- **Where the output goes:** the report as `reports/<domain>-<YYYY-MM>.md` (or `reports/<domain>-<start>-to-<end>.md` for a custom period). Save it in the project's SEO folder (see `seo-project-setup`); if there is none, ask once whether to create one or where to save instead. If the user prefers a doc or a sheet and a docs or spreadsheet tool is available, put reports in a doc and tables in a sheet instead. Tell the user where it was saved.
- **Shareable report:** once the work is done, offer one time to publish it as a shareable report with `create_share_report`: a read-only page at a link the user can send to a client, a boss or a teammate, no sign-in needed. Write it from this output: the summary first, then next priorities, then the supporting tables. The title is up to 120 characters (for example "SEO report for acme.com, October 2026"); the body is Markdown up to 50,000 characters, and images and raw HTML do not render. Publish only after the user says yes, and leave out their Search Console and Google Analytics numbers unless they agree to share them; without that agreement, describe changes in words and percentages they approve. Give them the link; `delete_share_report` removes it. A workspace can publish 30 reports a day.

## Guardrails

- Never invent a number. Every figure comes from a tool result or a file the user provided; write `unknown` otherwise.
- Never take credit for a change the data does not support. If clicks rose sitewide before any work shipped, say so.
- Do not blame a Google update or seasonality without evidence: check last year's same period first.
- Compare windows of equal length and matching weekdays, and leave out the last 3 days of Search Console data. Search Console dates are Pacific Time.
- Average position across many queries can move because the query mix changed. Check the query table before calling it a ranking change.
- A small change on a small number is noise. Do not headline a change of a few clicks as a trend; say the numbers are too small to read.
- Keep agency pricing, upsells and internal notes out of the report; put them in a message to the user.
- Anyone with a share link can read the report. Confirm the title and content with the user before publishing, and never include a client's private contact details or account data.
