---
name: content-brief
description: "Write a ranking content brief for one target keyword or page: confirm intent from the live SERP, read the top results and list every question they answer (plus People Also Ask), define what the page must add that page one lacks (own data, worked example, decision rule), set the primary and secondary keywords with volume and difficulty, outline headings, internal links, schema and the title/meta, and set a length target from the competing pages. Use when the user is writing a new article or landing page, refreshing a page that slipped, asks what a page should include to rank, or wants an SEO content outline or a brief for a writer."
---

# HarborRank Content Brief

## Goal

Produce one brief, for one target keyword or page, that a writer can follow to publish a page that deserves a page-one spot. The brief starts from the live SERP, not a template, and it says plainly what the page adds that the current page one lacks. This is the deep version of one brief from `keyword-clustering`, which maps keywords to pages first.

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

On hosted HarborRank, research tools spend credits. New accounts start with a 7-day free trial (1,000 research credits, one project); paid plans start at $29/month with 15,000 credits. Search Console, saved keywords, rank tracker reads, and site crawls use no credits. A keyword search costs about 50 credits and a domain overview about 80. Full backlinks, lead research (`research_lead`), and Lighthouse checks need a paid plan; on Free, the backlinks tools return a preview (totals and the top 3 referring domains, about 50 credits) with an upgrade link. This skill spends credits only on `get_serp_results`, `get_keyword_metrics`, `research_keywords` and `get_ranked_keywords`; Search Console, `inspect_urls`, audit pages and saved keywords are free.

- If `creditsRemaining` will not cover the planned calls, give the user the estimate and ask before spending. Use the free tools first.
- If a tool replies that a feature "is included in paid plans", tell the user once which feature needs a paid plan and pass on the upgrade link from the reply, skip that tool for the rest of the run, and finish with the other evidence. Do not retry it.
- If a tool fails for insufficient credits, stop making paid calls, tell the user, and finish with free tools and the data you already have. If `whoami` warns that credits are low, say so before a large run.
- If a HarborRank tool says the free trial hasn't started, or that credits ran out, give the user the link from that reply exactly as written, as a clickable link, and wait for them to say they're done before calling HarborRank again. Don't switch to answering without HarborRank data unless they ask you to.
- If the user asks to upgrade, change plan or buy credits, call `get_upgrade_link` (no credits) and give them the link. They pay on HarborRank by card; never say the upgrade is done until `whoami` shows the new plan.
- When `whoami` returns `mode: "self-hosted"`, there are no plan gates.

### Fallback mode (no HarborRank connection)

Use this mode only when Step 0 finds no connection. It works from web search, page reading, and files the user provides.

**Can still do**

- Search the target keyword on the web, judge intent from the pages that appear, and read those pages in full.
- List every question the competing pages answer, plus the People Also Ask questions and related searches the web search shows.
- Define what the page must add, and write the outline, internal links, schema, title and meta, and a length target from the word counts of the pages you read.
- Use Search Console CSV exports in the workspace for a refresh: the page's queries, clicks and positions are the user's own data; report them with the file as the source.

**Must not estimate**

Traffic, search volume, keyword difficulty, CPC, keyword counts, rankings, backlink counts, Maps pack positions, and Q&A counts. Write `unknown` for each. A web search shows which pages appeared for a query when you searched, not their Google ranking: report it as "appeared in web search", never as a position.

**Output**

- Start with the label **Web-evidence only: no HarborRank data.**
- Name the source (URL or file) of every figure you report.
- End, after any recommended next workflow, with one sentence that names the numbers this report is missing: "Connect HarborRank (start with a 7-day free trial) to add search volume, keyword difficulty, and the live Google top 20 to this brief." Do not add more sales copy than that.

## Required inputs

- `projectId`
- One target keyword, or one existing URL to refresh
- Optional market/location/language, audience, and the user's own data or experience the page can draw on

If `projectId` is missing, use `list_projects` first. If the user gives only a topic, run `keyword-research` or pick the target with them before writing the brief. If they give several unrelated keywords, run `keyword-clustering` first; one brief covers one page.

## HarborRank MCP tools

- `get_serp_results`: the live Google top 20 for 1-10 keywords, with each row's type, domain, title, URL and snippet. Use it to confirm intent and pick the pages to read. A `people_also_ask` row shows the box is present; read the questions themselves from a web search.
- `get_keyword_metrics`: volume, KD, intent, CPC and monthly trend for the primary and secondary keywords (up to 700 per call).
- `research_keywords`: find secondary keywords and question variants from the primary keyword when the SERP and Search Console do not give enough.
- `get_ranked_keywords`: with a page URL as the target, the keywords a competing page or the user's own page already ranks for. Use it on the top one or two competitors to see the secondary terms that page one covers.
- `get_search_console_performance`: for a refresh, the queries the page earns impressions for (filter `page` to the URL, `dimensions: ["query"]`), and a before/after comparison to see when it slipped.
- `inspect_urls`: confirm the page to refresh is indexed and canonical before rewriting it.
- `get_audit_pages`: if the project has a site audit, list the site's pages to choose internal links from and to, with their status codes.
- `list_saved_keywords`: reuse keywords and tags already saved for this topic.
- `save_keywords`: save the primary and secondary keywords with a `page:<slug>` tag, only after the user confirms.
- `create_share_report`: publish the finished work as a read-only page at a shareable link (see "Shareable report" below). Only after the user agrees.

Reading competitor pages is done with your own web fetch or browser tools, not HarborRank. HarborRank gives the ranking list; you read the pages.

## Workflow

If the project's SEO folder has `seo-context.md`, read it first for the site, market, audience, competitors and goals; otherwise ask only what this workflow needs.

1. Fix the target. One primary keyword and one page. For a refresh, call `inspect_urls` on the URL, then `get_search_console_performance` for its queries over `last_3_months` and the same window before it slipped, so the brief knows which queries it lost.
2. Call `get_serp_results` for the primary keyword and, in the same call, up to two close variants. Read the intent from what ranks: guides, product pages, tools, lists, local results, forums or video. If page one is mostly a different page type from what the user planned, say so and recommend matching the SERP or picking another keyword. Do not write a brief for a page type Google is not ranking.
3. Pick the top 5 organic results that match the intent (skip forums and giant marketplaces unless they dominate) and read each page in full with your own web tools. For each, note the headings, word count, format (steps, table, calculator, examples), freshness, author or proof, and schema if visible.
4. List every question those pages answer, merged and deduplicated, then add the People Also Ask questions and related searches from a web search. Mark which questions most of page one answers (the baseline the page must cover) and which only one page answers or none do.
5. Define what the page adds. Name at least two things page one lacks that this site can actually supply: its own data or numbers, a worked example with real figures, a decision rule ("choose X if..."), a template or tool, first-hand photos or testing, a clearer comparison. If you cannot name two that the user can deliver, say so and recommend a different keyword or angle instead of a brief.
6. Set the keywords. Call `get_keyword_metrics` on the primary keyword, the variants, and candidate secondaries from the SERP titles, the questions, Search Console queries, and `get_ranked_keywords` on the top competing page. Use `research_keywords` only if that list is thin. Keep secondaries that share the primary's intent; send the rest to another page.
7. Outline the page: H1, then H2s and H3s in the order a reader needs them, each with one line on what it must say and which question it answers. Put the answer to the main query near the top. Depth matches intent: a quick-answer query gets a short page that answers fast; a comparison or how-to gets the full treatment.
8. Add internal links: 3 to 6 existing pages this page should link to and 2 to 4 that should link to it, with anchor text. Use `get_audit_pages`, the sitemap, or a `site:` search to find real URLs. Never invent a URL.
9. Choose schema that fits the page type and content (for example Article, HowTo, Product, LocalBusiness, FAQPage only where the questions are on the page). Write the title tag (about 60 characters, primary keyword near the front) and meta description (about 155 characters, the page's added value in plain words).
10. Set the length target as a range from the word counts of the pages you read: around their median, higher only if the added sections need it. State the counts you measured.
11. Write the brief's guidance in plain, direct sentences. No filler ("in today's fast-paced world", "dive into", "comprehensive guide"), no padding to hit a word count. Every number in the brief names its source.
12. Ask before saving the keywords with `save_keywords` and a `page:<slug>` tag.

## Output format

Start with:

- **Target:** the primary keyword, the page (new or URL), and the intent in one line.
- **Verdict:** write it, refresh it, or pick another keyword, and why.
- **What this page adds:** the two or more things page one lacks.

Then include, in order:

- **SERP read:** the top 5 pages read, with page type, word count and the one thing each does best.

| Keyword | Role | Volume | KD | Intent | Source |
| ------- | ---- | -----: | --: | ------ | ------ |

- **Questions to answer:** baseline questions first, then the gaps.
- **Outline:** headings with one line each.
- **Internal links, schema, title and meta, length target.**

- **Next workflow:** end with one recommended next workflow, the reason for it, and the input it starts from. Default: `link-prospecting` on the published page, since a page that adds something new is easier to earn links to. If the top results belong mostly to one domain, recommend `competitor-analysis` on that domain instead.
- **Check back:** end with one dated follow-up: the date (28 days after the page is published, written out, for example "Monday, November 9") and the exact question to ask then: "Where does <page> rank for <keyword>?" Say in one line why it needs that wait: a new or rewritten page takes weeks to settle in Google, and Search Console positions cost no credits to check. Add it to the `Follow-ups` list in the SEO folder's `README.md` (create the list if it is missing) so the next session finds it. One follow-up only; don't add reminders or repeat it. If scheduled tasks are available (Cowork and the Claude apps on paid plans), offer once to make this a weekly scheduled task instead, named for the site, so the check runs by itself; the user reviews and confirms the schedule.
- **Where the output goes:** the brief as `content/briefs/<page-slug>.md`. If `keyword-clustering` already wrote a short brief there, expand that file instead of starting a new one. Approved keywords are also saved to the HarborRank project with `save_keywords`. Save it in the project's SEO folder (see `seo-project-setup`); if there is none, ask once whether to create one or where to save instead. If the user prefers a doc or a sheet and a docs or spreadsheet tool is available, put reports in a doc and tables in a sheet instead. Tell the user where it was saved.
- **Shareable report:** once the work is done, offer one time to publish it as a shareable report with `create_share_report`: a read-only page at a link the user can send to a client, a boss or a teammate, no sign-in needed. Write it from this output: findings first, then next steps, then the supporting table. Publish only after the user says yes, and leave out their Search Console and Google Analytics numbers unless they agree to share them. Give them the link; `delete_share_report` removes it.

## Guardrails

- Start from the SERP, never a stock outline. If you have not read the competing pages, the brief is not done.
- Name at least two things the page adds that page one lacks, or recommend a different keyword. Rewording what already ranks is not a plan.
- Do not invent metrics, word counts or URLs. If HarborRank or the page does not give a value, write `unknown`.
- Do not promise rankings or traffic. Say what the page needs to compete, and what it is up against.
- Do not pad. A short page that answers the query beats a long one that does not.
- Do not call `save_keywords` without explicit confirmation.
