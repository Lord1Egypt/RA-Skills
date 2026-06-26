---
name: chartgen
description: >
  Use this skill when the user wants to create visualizations (charts, dashboards, diagrams, Gantt, PPT), analyze data (Excel/CSV upload, cross-file analysis, trends, outliers) or generate reports. Also use when the user mentions ChartGen or uploads spreadsheet files.
user-invocable: true
homepage: https://github.com/chartgen-ai/chartgen-skill
metadata:
  openclaw:
    primaryEnv: CHARTGEN_API_KEY
    requires:
      runtime:
        - node >= 14
---

# ChartGen AI — Data Analysis & Visualization Skill

ChartGen is an AI platform for **visualization**, **data analysis** and **report generation**.
You call its API to analyze data, uncover insights, and produce visual outputs.

**Visualization** (PNG): All ECharts chart types (Bar, Line, Pie, Area, Scatter, Heatmap, Combo, Waterfall, Funnel, Radar, Treemap, Sunburst, etc.); Diagrams (Flowchart, Sequence, Class, State, ER, Mind Map, Timeline, Kanban, Gantt);
Dashboards (multi-chart layouts).

**Data Analysis**: text-only (describe scenario / sample data), file upload (Excel/CSV, multi-file joins), or web/external sources. Supports stats, trends, outliers, YoY.

**Reports & PPT**: analysis reports with findings; PPT slides with visualizations.

---

## Tool — `tools/chartgen_api.js`

| Command | Args | Purpose |
|---------|------|---------|
| `submit` | `<request.json>` | Submit request → returns `task_id` |
| `wait` | `<task_id>` | Poll until done (~25 min max) |
| `poll` | `<task_id>` | Single status check |
| `run` | `<request.json>` | Submit request and poll until done |

- Request JSON shape: `{ "query": "...", "channel": "Web", "files": ["/absolute/path/data.xlsx"] }`.
- `query`: confirmed user request text.
- `channel`: messaging channel name using letters, numbers, spaces, dots, underscores, or hyphens.
- `files`: optional array of absolute paths to selected files.
- Supported files: `.csv`, `.xls`, `.xlsx`, `.tsv`.
- Network boundary: this helper sends the confirmed prompt and selected files only to `https://chartgen.ai`. Custom API endpoints are not supported.
- Output: JSON with `text_reply`, `edit_url`, `artifacts[]` (`artifact_id`, `image_path`, `title`).
- PPT artifacts also have: `page_count`, `preview_paths[]`, `download_path`.
- Excel/file artifacts also have: `download_path`, `file_name`, `summary`.
- On error: JSON with `"error"` and `"user_message"` (for non-special errors).

---

## Workflow — 5 Steps

### STEP 1 — Confirm Before Submitting

Always respond in the user's language. **Must** mention using **ChartGen** to complete the task, and include numbered options, each on its own line:
> **1** ✅ Go ahead
> **2** ✏️ Modify
> **0** ❌ Cancel

**Confirmation rules:**
1. **Cancel = abandon forever.** Never proceed with a cancelled task.
2. **Replies bind to the most recent prompt only.** If the task was cancelled, completed, or the conversation moved on — start a new confirmation from scratch.
3. **When in doubt, ask** — never guess.

**Query rule — text requests (no files):**
The request JSON `query` field is **always the user's original message, copied word-for-word**. Do NOT translate, rephrase, expand, polish, or "improve" it in any way. Show this exact text in the confirmation. If user confirms → submit this exact text. If user edits → the edited text becomes the new verbatim query.

**File upload:** Do NOT submit immediately. Recommend 3–5 analysis tasks (numbered, noting which files). Each option's text is the exact query that will be submitted. User picks a number, types custom text, or cancels.

Text request example (**reply in user's language, mention ChartGen**):
> Sure! Here's what I'll ask **ChartGen** to do for you:
> 📊 **"Generate a monthly sales trend line chart for 2025"**
> **1** ✅ Go ahead
> **2** ✏️ Modify
> **0** ❌ Cancel

File upload example (**reply in user's language, mention ChartGen**):
> Got your files! Here are a few things **ChartGen** can do — pick one or tell me what you'd like:
> **1.** 📊 "Monthly order trend chart" — *orders.xlsx*
> **2.** 🥧 "Category breakdown pie chart" — *orders.xlsx, products.xlsx*
> **3.** 📋 "Full analysis report with all files"
> **0.** ❌ Cancel
> Or just type your own request!

---

### STEP 2 — Notify User, Then Submit

**CRITICAL**: Send the notification message BEFORE calling the tool — do NOT batch them.

**Notify** (adapt to language and context):
- Text-only: "ChartGen is working on your request, ~1–2 min..."
- With files: "ChartGen is analyzing your data, ~2–5 min..."
- PPT: "ChartGen is generating your PPT, ~10–20 min, please be patient..."

**Then create a temporary request JSON file:**
Use a platform file-write API or other structured file operation. Do **not** create this JSON file with a shell command containing the user's query, and do **not** put the query, channel, or data file paths directly into the shell command.

Use an agent-generated temporary filename with safe characters, for example `/tmp/chartgen_request_20260506_112900.json`.

Request JSON:
```json
{
  "query": "confirmed user text from STEP 1",
  "channel": "Web",
  "files": ["/absolute/path/data.xlsx"]
}
```

Omit `files` when no files are selected.

**Then call the tool with only the request file path:**
```
node tools/chartgen_api.js submit /tmp/chartgen_request_20260506_112900.json
```
The shell command must contain only the fixed command words and the agent-generated request JSON path.

Save the returned `task_id` for STEP 3.

**Error handling:**

- `"api_key_not_configured"` → Tell user to get a key at https://chartgen.ai/chat → Menu → API, then set via `export CHARTGEN_API_KEY="key"` or save to `~/.chartgen/api_key`. **Stop here.**
- `"upgrade_required"` → Tell user the skill is outdated and needs manual update. See `references/upgrade-skill.md` for the message template. **Stop here.**
- **Any other error** → Show the `user_message` field to the user. **Stop here.**

---

### STEP 3 — Background Polling

Choose based on platform capabilities:

Before using any `task_id`, confirm it matches only letters, numbers, dots, underscores, or hyphens. If it does not, stop and report the invalid task ID instead of running a command.

**A. Background exec** (OpenClaw, or agent supports background execution with exit notification):
```json
{ "tool": "exec", "params": { "command": "node tools/chartgen_api.js wait {task_id}", "background": true } }
```
When done, read output → STEP 4.

**B. Cron** (generic): poll every 90s with `poll {task_id}`. On terminal status (`finished`/`error`/`not_found`), remove cron → STEP 4. Timeout after 25 min.

**C. Inline** (last resort): run `wait {task_id}` synchronously → STEP 4.

If user asks to check a task: run `poll {task_id}` and report.

---

### STEP 4 — Handle Completion

Read the output JSON `status`:

- **`"finished"`** → Proceed to STEP 5. Artifacts are already saved to local `image_path` / `download_path`.
- **`"error"`** → Show `error` to user, suggest retry.
- **`"not_found"`** → Task expired, offer new request.
- **`"timeout"`** → Inform user, offer manual check: "Check task {task_id}".

---

### STEP 5 — Deliver Results

1. **Summarize `text_reply`** — extract key points from ChartGen's analysis and present them concisely to the user. Keep it clear and informative.

2. **Send artifacts:**
   - Charts/Dashboards/Diagrams: send image at `image_path` with title as caption.
   - PPT: tell user page count, send each `preview_paths` image, send `.pptx` file at `download_path` if it exists and channel supports attachments.
   - Excel/file: show `summary` (columns, rows), send file at `download_path` if it exists and channel supports attachments.

3. **Show `edit_url`** — link to edit on ChartGen.

4. **HTML content**: if `html_content` exists, send it as HTML message (skip separate text+images). Still show `edit_url`.

5. **Suggest next steps**: "You can ask me to generate another visualization!"

---

## Rules

- Always respond in the user's language.
- Always confirm before submitting — never call the tool without explicit confirmation.
- Tell the user that confirmed prompts and selected files are sent to `https://chartgen.ai`.
- Never expose API key. Never fabricate visualizations.
- Prefer background/cron polling over blocking. Clean up crons after completion.
- Always use `image_path` from results, never show raw base64.
- Each request is independent — don't suggest modifying previous charts.
- **NEVER skip STEP 5 items**: always summarize `text_reply`, **send artifact images/files**, show `edit_url`, and suggest next steps — even when artifacts are present.

