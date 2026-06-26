## Full Workflow Details

### Step 1: Login Check
- Open `https://i.alibaba.com/` in the browser tool.
- If the URL redirects to `https://login.alibaba.com/...` → user is not logged in.
  - Prompt: *"Please log in to Alibaba International Station. Once you have completed login, press Enter to continue.*"
  - Poll the page until the URL no longer redirects (i.e., the main dashboard loads).
- If no redirect occurs, proceed directly.

### Step 2: Retrieve Business Data (Summary)
Execute in the browser console:
```js
(async () => {
  const url = 'https://crm.alibaba.com/crmlogin/aisales/dingwukong/diagnoseData.json';
  const r = await fetch(url, {method: 'POST', credentials: 'include'});
  if (!r.ok) throw new Error(`HTTP error: ${r.status}`);
  return await r.json();
})()
```
Expected JSON fields (important):
- `encryptedReportId` – token for constructing the weekly report link.
- `values.receipt` – token required for the detailed report API.
- `values.weekDiagnose` – array of diagnostic objects, each containing `scope`, `diagnoseTitle`, `diagnoseSummary`.
- `values.indicatorList` – metric list for the overview table.
- `maTaskList` – merchant task list (title & description).
- `diagnoseSummary` – free‑text diagnostic summary.

### Step 3: Data Validation (Silent)
1. If the entire response is `{}` or `null` → **CRITICAL**: No data available. Abort workflow with fallback message.
2. Missing/empty `encryptedReportId` → abort.
3. Missing/empty `values.receipt` → abort.
4. Non‑critical missing fields:
   - Missing `weekDiagnose` → note *"Business diagnostics not included for this period"* and continue.
   - Both `diagnoseTitle` and `diagnoseSummary` empty → skip that diagnostic entry.

**Fallback message** (displayed on abort):
```
Sorry, no business data is available for the current account in the Alibaba Weekly Report system. Analysis cannot be performed at this time.

**Expert Tip:** If you can see data in your backend, provide a screenshot or list key metrics (Exposure, Clicks, Inquiries, etc.) and I will give a manual diagnostic.
```

### Step 4: Structured Summary Display
Render four sections **in a single response** after validation passes.

#### 4.1 Store Data Overview
Create a Markdown table from `values.indicatorList`:
| Metric | This Week | WoW Change | vs. Industry Avg |
|---|---|---|---|
| {name} | {value} | {cycleCRC || '-'} | {valueVsAvg || '-'} |
If `cycleCRC` or `valueVsAvg` missing, show `-`.

#### 4.2 Diagnostic Summary
Print `values.diagnoseSummary` verbatim.

#### 4.3 Merchant Tasks
Iterate `maTaskList`, strip HTML tags from `desc`, and output:
- **{title}**\n  {desc cleaned}

#### 4.4 Weekly Report Link
Construct URL:
```
https://crm.alibaba.com/crmagent/crm-grow/luyou/report-render.html?id={encryptedReportId}&dateScope=week&isDownload=false
```
Display as a clickable Markdown link.

### Step 5: Full Report Retrieval
If Step 3 validation succeeded, use `values.receipt` to call the detailed report API:
```js
(async () => {
  const receipt = '<receipt from Step 2>';
  const url = 'https://crm.alibaba.com/crmlogin/aisales/dingwukong/queryWeekReportAllData.json';
  const r = await fetch(url, {
    method: 'POST',
    credentials: 'include',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: `receipt=${receipt}`
  });
  if (!r.ok) throw new Error(`HTTP error: ${r.status}`);
  return await r.json();
})()
```
#### Validation (Silent)
- Empty/null response or missing `data` → announce *"Sorry, unable to retrieve full report data at this time. Please try again later."* and stop.
- Missing module data → skip that module, continue processing others.

#### Module Mapping
The response groups data by `reportPageCode`. Key modules:
- `STORE_DATA_OVERVIEW`
- `STORE_INFRASTRUCTURE_SITUATION`
- `STORE_DIAGNOSIS`
- `OPPORTUNITY_STAR_LEVEL_DATA_OVERVIEW`
- `TRADE_STAR_LEVEL_DATA_OVERVIEW`
- `ACTION_SUGGESTION`
- `PRODUCT_DATA_OVERVIEW`
- `EXPOSURE_TOP10_PRODUCT_DATA`
- `CATEGORY_EXPANSION_SUGGESTION`
- `BUYER_DISTRIBUTION_DATA`
- `P4P_PLAN_OPTIMIZ_SUGGESTION`
- `P4P_SEARCH_WORD_OPTIMIZ_SUGGESTION`
- `FLOW_SOURCE_CHANNEL_ANALYSIS`
- `STORE_DETAIL_12_MONTHS`
- `STORE_COMMUNICATION_CONVERSION_OVERVIEW`
- `STORE_ACCOUNT_DATA_OVERVIEW`
- `EMPLOYEE_MANAGEMENT`

For field definitions, see `reference/weekly_report_data_explanation.md` (outside the scope of this skill).

#### Post‑Retrieval Behavior
After a successful call, output only:
```
Full data analysis complete. Feel free to ask me any questions about your store data!
```
Then **wait for user queries**. When a question arrives, consult the stored full‑report JSON and answer using the appropriate module, formatting tables or bullet lists as needed. Do **not** proactively dump the whole JSON.

### Exception & Edge Cases
| Situation | Signal | Action |
|---|---|---|
| Not logged in (redirect) | URL changes to `login.alibaba.com` | Prompt login, poll until success |
| API error / non‑200 HTTP | fetch throws or `!r.ok` | Show *"System busy, please retry later"* and retry after 10 s |
| System busy page | Page contains "System busy" | Inform user and abort |
| Timeout waiting for report | >30 polling attempts (≈5 min) | Notify timeout and abort |
| Empty data / missing critical fields | Checks in Step 3 | Show fallback message and stop |
| Missing optional modules | Absent `reportPageCode` entries | Skip those modules silently |

---

## Operational Standards
- **Privacy**: Only access data for the logged‑in Alibaba account; never store or transmit it elsewhere.
- **Rate Limiting**: Do not call the APIs more than once per minute for the same user to avoid throttling.
- **Formatting**: All user‑facing output must be Markdown; use tables for metrics and bullet lists for tasks.
- **User Interaction**: After the initial summary, the skill becomes passive, awaiting explicit user questions.
