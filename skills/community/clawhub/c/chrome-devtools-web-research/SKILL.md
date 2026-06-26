---
name: chrome-devtools-web-research
description: Browser-driven web research and live site inspection using chrome-devtools-mcp over a remote-debugging Chrome session. Use when a user asks to investigate, verify, cross-check, monitor, or extract information from real websites or dynamic pages—especially social platforms, search engines, docs, dashboards, login-aware flows, and JavaScript-heavy sites where page state matters or normal search/read tools are insufficient. Always start with Chrome DevTools MCP via mcporter instead of waiting for the user to remind you. Default pattern: Google first for the main reporting chain, X second for live discussion, and Reddit third for community source-tracing and cross-verification.
---

# Chrome DevTools Web Research

Use `chrome-devtools-mcp@latest` through `mcporter` to drive Chrome, inspect real pages, and extract structured findings from dynamic websites.

Use **MCP first by default**. Do not wait for the user to remind you to use it.

For concrete failure wording and remediation paths, read `references/troubleshooting.md`.

## User setup guidance

If the user needs to enable tab access in Chrome, give them this short setup flow:

1. Open `chrome://inspect/#remote-debugging`
2. Toggle it on
3. That’s it — the agent can now see the user’s tabs, cookies, logins, and page state through Chrome DevTools MCP

Explain plainly that this uses **Chrome DevTools MCP** under the hood and **does not require a browser extension**.

## Quick start

1. Verify the MCP server is available.
2. Open the target page with `chrome-devtools.new_page`.
3. Take a snapshot and read visible structure from the accessibility tree.
4. Navigate, click, fill, or switch tabs as needed.
5. Cross-check important claims across multiple sources.
6. Close pages promptly when a search leg is done.
7. Summarize by source quality, not page volume.

## Core commands

```bash
mcporter list --output json
mcporter call chrome-devtools.new_page --args '{"url":"https://example.com"}' --output json
mcporter call chrome-devtools.take_snapshot --args '{}' --output json
mcporter call chrome-devtools.click --args '{"uid":"<tab_uid>"}' --output json
mcporter call chrome-devtools.navigate_page --args '{"url":"https://example.com/next"}' --output json
mcporter call chrome-devtools.fill --args '{"uid":"<input_uid>","value":"query text"}' --output json
mcporter call chrome-devtools.press_key --args '{"key":"Enter"}' --output json
mcporter call chrome-devtools.close_page --args '{}' --output json
```

## Workflow

### Default operating rule

1. **Always try MCP first** with `mcporter` + `chrome-devtools`.
2. **Start searching proactively** when the task implies browsing or research.
3. **Only stop to ask for help when Chrome-side access is broken**.
4. If setup/access fails, **prompt the user to check Chrome**, especially remote debugging / inspect availability, then retry.
5. **Close pages promptly** when a page or search leg is no longer needed.

### Failure and retry policy

Do not give up after the first MCP/browser failure.

Use `references/troubleshooting.md` for concrete error classes, user-facing wording, and remediation steps.

Follow this retry order strictly:

1. **Retry the same MCP command once immediately** if the error looks transient.
2. If it still fails, run `mcporter list --output json` again to verify `chrome-devtools` is still present.
3. If the server is present, retry with the smallest next step:
   - reopen the page with `chrome-devtools.new_page`, or
   - re-run `chrome-devtools.take_snapshot`, or
   - re-issue a single click/fill/navigation action.
4. If Chrome itself appears unreachable, explicitly tell the user to check Chrome remote debugging / inspect access, then retry after that.
5. If Google is blocked by captcha, consent wall, or anti-bot friction, **do not stall**. Record that Google was blocked and continue to **X**, then **Reddit**.
6. Only stop the flow when the browser bridge is clearly broken and the user must intervene.

Practical rule: prefer **one immediate retry + one environment re-check + one resumed attempt**. Do not loop endlessly.

### Default search strategy

If the user does not specify a website, platform, or search engine, follow this chain **by default and in order**:

1. **Google first**
2. **X second**
3. **Reddit third**

Treat this as the standard search chain, not an optional suggestion.

Required behavior for the chain:

- Start with **Google** for broad discovery, main reporting chain, and likely primary/secondary sources.
- Then check **X** for live spread, fresh claims, quote-post chains, contradictions, and breaking updates.
- Then check **Reddit** for community source-tracing, surfaced links, and discussion that may reveal the original source trail.
- Do this **proactively**. Do not wait for the user to ask for each platform one by one.
- If the user only says “search this”, still run the chain unless they explicitly restrict scope.
- If one source is blocked, unavailable, or low value, continue to the next source instead of stopping.

Minimum acceptable default sequence:

1. Open Google results for the query
2. Inspect at least one fresh snapshot there
3. Open X search for the same query
4. Inspect at least one fresh snapshot there
5. Open Reddit search for the same query
6. Inspect at least one fresh snapshot there
7. Then summarize across the chain

If Google is blocked by a bot challenge or consent wall, report that friction, mark the Google leg blocked, and continue with **X -> Reddit** without waiting for user confirmation.

This default is for open-ended web research. If the user explicitly names another site, search engine, or platform, follow that instead.

### 1. Confirm MCP access

Run:

```bash
mcporter list --output json
```

Expect a `chrome-devtools` server using a transport similar to:

```text
STDIO npx chrome-devtools-mcp@latest --autoConnect
```

If `mcporter` is missing, help the user install it first. If the `chrome-devtools` MCP server is missing, help the user configure or install it instead of stopping at a vague error.

Practical install/remediation flow:

```bash
npm i -g mcporter
mcporter list
```

If Chrome DevTools MCP is not available yet, guide the user to set up or reconnect the server used by `mcporter`, and then retry `mcporter list` until `chrome-devtools` appears.

Do not ask whether MCP should be used. If it is available, proceed immediately.

### 2. Open the target page directly

Prefer direct URLs whenever possible.

```bash
mcporter call chrome-devtools.new_page --args '{"url":"https://target-site.example/path"}' --output json
```

Use direct navigation for:

- search result pages
- filtered URLs
- deep links to posts/articles/docs/issues
- dynamic app routes that are easier to open directly than to reproduce manually

If the site supports URL query parameters, prefer those over repeatedly editing fragile on-page controls.

### 2.5 Close pages when done

Do not leave research tabs open unnecessarily.

After extracting what you need from a page or after finishing a search leg, close that page promptly unless you still need it for comparison.

```bash
mcporter call chrome-devtools.close_page --args '{}' --output json
```

Practical rule:

- open page
- inspect / interact / snapshot
- record findings
- close page when that leg is done

For multi-source research, keep only the minimum number of live pages needed.

### 3. Read the snapshot, not the pixels

Always pull a fresh snapshot after navigation or interaction:

```bash
mcporter call chrome-devtools.take_snapshot --args '{}' --output json
```

Look for:

- `article`, `link`, `button`, `heading`, `textbox`, `combobox`, `tab`, `dialog`
- authors, timestamps, handles, titles, labels, counts
- outbound links to original reporting or docs
- signs of login walls, parity labels, sponsored content, or partial loads

Use screenshots only when layout itself matters.

### 4. Interact carefully

Use the smallest reliable action:

- `navigate_page` for direct URL changes
- `click` for tabs, filters, menus, pagination
- `fill` + `press_key` for search boxes and forms
- `select_page` if multiple tabs/pages are open

After each meaningful state change, take another snapshot.

### 5. Separate source quality

Group findings into buckets such as:

- **Primary / official**: original publisher, official docs, org pages, first-party dashboards
- **Secondary reporting**: media, analysts, aggregator accounts citing a source
- **Tertiary chatter**: comments, fan accounts, reposts, AI replies, unsourced claims

Repeated copies of the same claim count as one claim stream, not multiple confirmations.

### 6. Cross-check outside the active page

If the user wants stronger confidence, combine browser MCP findings with other methods:

- `web_search` for discovery, source expansion, and finding external reporting
- `web_fetch` for automatically retrieving readable page content when a page URL appears and lightweight extraction is enough
- `agent-browser` for parallel page inspection when helpful
- `curl` as a fallback when fetch-style extraction is unavailable or insufficient

Use the browser for live state and interaction. When the task surfaces normal webpage links, prefer `web_fetch` first for readable extraction; fall back to `curl` when needed for raw retrieval or custom parsing.

### 7. Write the summary

Use this structure when the page contains conflicting claims:

- **Current best answer**
- **What the site/page says**
- **What other sources say**
- **Where the disagreement is**
- **Most credible sources**
- **Confidence / caveats**

Good phrasing:

- "The live page currently shows X, while secondary reporting is pushing Y."
- "Most posts trace back to the same reporting chain, so treat them as one rumor stream."
- "The browser-visible evidence supports A, but confirmation from a primary source is still missing."

## Site-specific notes

### Social platforms

- Use platform-native filters like **Top**, **Latest**, **People**, **Media**, subreddit sorting, or thread sorting to separate dominant narrative from fresh chatter.
- Check for parody/account labels before citing.
- Treat quote-post chains, repost storms, and copied Reddit comments as propagation, not independent sourcing.
- AI assistant replies inside a platform can help map rumor themes, but they are not primary evidence.
- On Reddit, prioritize posts that link back to original reporting, comments that add sourcing context, and community threads where multiple users are tracing the same source chain.

### Search engines

- Expect bot challenges or captchas.
- If blocked, pivot to another source rather than pretending results were retrieved.

### Docs / dashboards / web apps

- Prefer direct deep links.
- Snapshots are often enough for structured extraction.
- If content is hidden behind menus, open one section at a time and resnapshot.

## Practical notes

- UI language may vary; rely on structure, URLs, and recognizable entities more than labels alone.
- If the page is still loading, wait briefly and snapshot again.
- If login, subscription, or anti-bot friction appears, report the limitation plainly.
- When normal webpage links appear during research, automatically try `web_fetch` first for fast readable extraction; if that is unavailable or not enough, fall back to `curl`.
- When the page alone is not enough, expand outward with `web_search` to find corroborating coverage, official announcements, or the original reporting chain.
- If the user is not set up yet, prefer giving them the shortest enablement path first: turn on Chrome remote debugging access, then verify `mcporter` + `chrome-devtools` availability.
- Keep an audit trail in your notes: page URL, key visible claims, and which source tier each claim belongs to.
- For open-ended search, do not stop at Google alone; the default completion bar is **Google -> X -> Reddit** unless the user explicitly narrows scope.
- After failures, retry with discipline; do not abandon the browsing flow too early and do not spin in unlimited retries.
- Close pages promptly after each finished search leg or inspection leg.

## Example flows

### Generic site inspection

```bash
mcporter call chrome-devtools.new_page --args '{"url":"https://example.com"}' --output json
mcporter call chrome-devtools.take_snapshot --args '{}' --output json
mcporter call chrome-devtools.click --args '{"uid":"<relevant_tab_uid>"}' --output json
mcporter call chrome-devtools.take_snapshot --args '{}' --output json
```

### Default search-engine + social cross-check flow

```bash
mcporter call chrome-devtools.new_page --args '{"url":"https://www.google.com/search?q=Finalissima%202026"}' --output json
mcporter call chrome-devtools.take_snapshot --args '{}' --output json
mcporter call chrome-devtools.close_page --args '{}' --output json
mcporter call chrome-devtools.new_page --args '{"url":"https://x.com/search?q=Finalissima%202026&src=typed_query&f=top"}' --output json
mcporter call chrome-devtools.take_snapshot --args '{}' --output json
mcporter call chrome-devtools.navigate_page --args '{"url":"https://x.com/search?q=Finalissima%202026&src=typed_query&f=live"}' --output json
mcporter call chrome-devtools.take_snapshot --args '{}' --output json
mcporter call chrome-devtools.close_page --args '{}' --output json
mcporter call chrome-devtools.new_page --args '{"url":"https://www.reddit.com/search/?q=Finalissima%202026"}' --output json
mcporter call chrome-devtools.take_snapshot --args '{}' --output json
mcporter call chrome-devtools.close_page --args '{}' --output json
```

## Output standard

When reporting back, distinguish clearly between:

- what is visible on the live page
- what is asserted by the site or account owner
- what is reported by other sources
- what remains unverified

If sources conflict, say so directly.