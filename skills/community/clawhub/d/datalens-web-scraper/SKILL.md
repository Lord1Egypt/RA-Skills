---
name: datalens
description: Use DataLens MCP tools to scrape structured data from any website open in Chrome. Triggers when the user wants to extract lists, tables, comments, products, reviews, or any repeating data from a webpage, or wants to manage active scraping jobs.
---

# DataLens Scraping Skill

## How Tool Calls Work

Every DataLens tool is invoked by running a terminal command. No MCP client configuration is required.

The `datalens-mcp-call` binary handles the MCP stdio handshake and returns the tool result as YAML/JSON to stdout.

```
run_in_terminal: datalens-mcp-call <tool_name> '<args_json>'
```

If `datalens-mcp-call` is not on PATH (e.g. not globally installed), use npx:

```
run_in_terminal: npx datalens-mcp-call <tool_name> '<args_json>'
```

## Prerequisites

1. `datalens-mcp-server` npm package installed: `npm install -g datalens-mcp-server` (or use `npx`).
2. DataLens Chrome extension installed and active in Chrome.
3. Chrome open with the target page loaded (or provide `url` in the tool args — the extension will open it).
4. Node.js ≥ 18 available in the terminal.

---

## How This Works

`datalens-mcp-call` spawns the DataLens MCP proxy as a child process, performs the MCP initialization handshake over stdio, calls the requested tool, and prints the result.

```
AI Agent
  ↓ run_in_terminal
datalens-mcp-call <tool> <args>
  ↓ stdio JSON-RPC
DataLens MCP Proxy (datalens-mcp-proxy)
  ↓ WebSocket (localhost:17373)
Chrome Extension
  ↓
Browser Tab
```

---

## Standard Scraping Workflow

Follow these steps in order. Do not skip steps or call `scrape_start` before `scrape_analyze_columns` completes.

### Step 1 — Detect tables

```bash
datalens-mcp-call scrape_detect_tables '{"url":"https://example.com","prompt":"article list"}'
```

Returns a list of detected table structures with `rootSelector`, `itemSelector`, `documentInfoPath`. Pick the best matching table and copy those three values for subsequent steps.

If the page requires login, ask the user to log in in Chrome first, then re-run this command.

### Step 2 (optional) — Inspect tree for expand buttons

```bash
datalens-mcp-call scrape_get_table_tree '{"rootSelector":"<from step 1>","itemSelector":"<from step 1>","documentInfoPath":"<from step 1>"}'
```

Use when the data has nested replies, collapsed rows, or "load more" buttons. Inspect the `_uid`-annotated tree in the output to identify expand button UIDs.

### Step 2b (optional) — Expand and re-detect

```bash
datalens-mcp-call scrape_click_expand_and_redetect '{"rootSelector":"...","itemSelector":"...","documentInfoPath":"...","expandButtonUids":[{"type":"reply","uids":["uid1","uid2"]}]}'
```

The extension clicks the buttons, waits for new content, then re-detects. Use the updated `rootSelector`/`itemSelector`/`documentInfoPath` from this output in Step 3.

### Step 3 — Analyze columns

```bash
datalens-mcp-call scrape_analyze_columns '{"rootSelector":"...","itemSelector":"...","documentInfoPath":"...","url":"https://example.com","prompt":"article list"}'
```

Calls the backend AI to identify fields, data types, and pagination. Returns a `scraperConfig` and `jobDraft`. Confirm the field list looks correct before proceeding.

### Step 4 — Start scraping

```bash
# Pass the jobDraft object returned by scrape_analyze_columns
datalens-mcp-call scrape_start '{"jobDraft":<paste jobDraft here>,"maxRecords":10}'
```

Returns a `jobId`. Use `maxRecords: 10` for a preview run first.

### Step 5 — Poll for status

```bash
datalens-mcp-call scrape_status '{"jobId":"<jobId>","waitMs":3000}'
```

Re-run until `status` is `COMPLETED`, `FAILED`, or `STOPPED`.

Key status fields:

- `status`: `QUEUED` → `PREPARING` → `RUNNING` → `COMPLETED` / `FAILED` / `STOPPED`
- `scrapedCount`: rows collected so far
- `error`: present only on failure

### Step 6 — Retrieve results

**Save to file (recommended for large results):**

```bash
datalens-mcp-call scrape_export_to_file '{"jobId":"<jobId>","outputDir":"/tmp/datalens","format":"json"}'
```

Returns the saved file path.

**Inline preview (small result sets):**

```bash
datalens-mcp-call scrape_result '{"jobId":"<jobId>","limit":50}'
```

Use the `cursor` field from each response to fetch the next page.

**In-memory export:**

```bash
datalens-mcp-call scrape_export '{"jobId":"<jobId>","format":"csv"}'
```

Returns base64-encoded file content.

---

## Job Control

```bash
datalens-mcp-call scrape_pause  '{"jobId":"<jobId>"}'
datalens-mcp-call scrape_resume '{"jobId":"<jobId>"}'
datalens-mcp-call scrape_stop   '{"jobId":"<jobId>"}'
```

## Browser Tab Management

```bash
datalens-mcp-call browser_list_tabs
datalens-mcp-call browser_open_tab  '{"url":"https://example.com"}'
datalens-mcp-call browser_use_tab   '{"tabId":123}'
datalens-mcp-call browser_close_tab '{"tabId":123}'
```

Tab management is usually not needed — `scrape_detect_tables` with a `url` arg handles tab opening automatically.

---

## Agent Decision Rules

- **Never call `scrape_start` without a `jobDraft` or `scraperConfig`** from a prior `scrape_analyze_columns` response. Fabricating a scraperConfig will produce wrong results.
- **Never skip `scrape_analyze_columns`** and jump straight to `scrape_start`. The analyze step is required to build the config.
- If `scrape_detect_tables` returns an empty list, the page may need login or may be dynamically loaded. Ask the user to open the target URL in Chrome and scroll to load content, then retry.
- If `scrape_status` stays at `QUEUED` for more than 30 seconds, check that the Chrome extension is active and that a tab for the target URL is open.
- Use `maxRecords: 10` for a preview scrape to confirm the config is correct before running a full job.
- Default export format is JSON. Use CSV or XLSX when the user asks for spreadsheet output.

---

## End-to-End Example: Scrape Toutiao Headlines

```bash
# 1. Detect tables on the homepage
datalens-mcp-call scrape_detect_tables '{"url":"https://www.toutiao.com/?is_new_connect=0&is_new_user=0","prompt":"article list"}'

# 2. Analyze columns (fill in selectors from step 1 output)
datalens-mcp-call scrape_analyze_columns '{"rootSelector":"<from step 1>","itemSelector":"<from step 1>","documentInfoPath":"<from step 1>","url":"https://www.toutiao.com/?is_new_connect=0&is_new_user=0","prompt":"article list"}'

# 3. Preview run — first 10 rows (paste the full jobDraft JSON object from step 2)
datalens-mcp-call scrape_start '{"jobDraft":<paste jobDraft>,"maxRecords":10}'

# 4. Poll until status is COMPLETED
datalens-mcp-call scrape_status '{"jobId":"<jobId>","waitMs":3000}'

# 5. Save results to file
datalens-mcp-call scrape_export_to_file '{"jobId":"<jobId>","outputDir":"/tmp/datalens","format":"json"}'
```

Set `DATALENS_TIMEOUT=180000` before running if a tool call takes longer than the default 120 s:

```bash
DATALENS_TIMEOUT=180000 datalens-mcp-call scrape_analyze_columns '...'
```

---

## Debug Tools

These are for troubleshooting only. Do not use in normal scraping workflows.

```
datalens-mcp-call debug_get_logs '{"levels":["error"]}'
datalens-mcp-call debug_clear_logs '{}'
datalens-mcp-call debug_export_logs_to_file '{"outputDir":"/tmp/datalens"}'
```
