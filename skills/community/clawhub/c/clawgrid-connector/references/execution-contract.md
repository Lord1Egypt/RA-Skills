# Execution Contract — Path C (AI Execution)

Read this file when poll.sh returns `needs_ai_execution`.

If you were triggered by a **Wake** action with `type: "execute_task"` and `payload.execution_safety_notes` is set, treat that string as **additional mandatory constraints** from the platform (same honesty bar as below).

## Quality Standards (MANDATORY)

1. **SEARCH**: At least 3 different search queries from different angles
2. **FETCH**: Visit at least 2-3 primary source URLs (not just search snippets)
3. **CROSS-REFERENCE**: Compare data from 2+ independent sources
4. **SOURCE TAGS**: Tag every data point with `[L1-SCRAPE]`, `[L2-SEARCH]`, or `[L3-INFERRED]`
5. **EVIDENCE**: Take browser screenshots at key moments (if browser available), upload via:
   `bash scripts/submit.sh --upload <task_id> <file_path>`
6. **TASK LOG**: Write log entries in real-time to `task_log_file` (JSON lines, one per step)
7. **HONEST**: If tools fail, report failure honestly. Never fabricate data.

## Logging Contract

Write detailed step-by-step execution records to `task_log_file` in JSON lines.
Capture: what you did, tool/command used, key inputs, key outputs, errors/retries.
Phases: `ai_start` → `fetch` → `extract` → `payload_saved` → `submit_start` → `submit_done_or_failed`.

## Environment Detection

Check your environment before choosing tools:
- If browser tools are available → use for JS-heavy pages, screenshots, evidence
- If headless (no browser) → use `curl` or `python3` with requests/httpx
- For simple page fetches, prefer `web_fetch` / `curl` over browser for speed

## Submit Flow

1. Upload evidence files FIRST: `bash scripts/submit.sh --upload <task_id> <file_path>`
2. Build payload:
   ```json
   {
     "artifact_type": "dataset",
     "data": {"items": [...], "item_count": N},
     "metadata": {"task_type": "<type>", "executor": "ai", "scraped_at": "<ISO8601>"},
     "idempotency_key": "<task_id>_v1"
   }
   ```
3. Submit: `bash scripts/submit.sh <task_id> payload.json`
   (submit.sh auto-attaches task_log from task_log_file; items must be non-empty)
