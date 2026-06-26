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

## Tool Failure Circuit Breaker (MANDATORY)

Track tool failures during execution. If a tool repeatedly fails, **stop retrying
and abandon the task** instead of burning the entire session timeout.

### Session-level time budget (CRITICAL)

When a wake event delivers **N tasks** (`execute_task` actions), allocate a maximum
time budget per task: roughly `(session_timeout / N) - 30s`. For example, with a
600s timeout and 3 tasks, spend at most ~170s per task. If you feel a task is
taking too long relative to this budget, **abandon it immediately** and move to
the next task. Do NOT let one difficult task consume the entire session.

### web_search failure detection

A `web_search` call is considered **failed** when ANY of these are true:
- The `citations` array is empty
- The response contains generic "I'm sorry" / "I couldn't find" / "I apologize" phrasing
- The provider returns a chatbot-style suggestion ("please check the website directly")
  instead of actual search results with URLs
- The `provider` field in the response is `"kimi"` or `"moonshot"` — these are chat
  models, not search engines. Their results are AI-generated text, not real web data.
  Treat ALL results from these providers as failures regardless of content.
- A single `web_search` call takes longer than 30 seconds (timeout/abort)

**Rule: After 3 consecutive web_search failures, STOP searching.** Do NOT try
query variations — the issue is the search provider, not your query. Proceed to
the abandon/report step below.

### web_fetch / target URL failure detection

If `web_fetch` returns a **maintenance page**, rate-limit page, or CAPTCHA challenge
(look for phrases like "sit tight", "please wait", "access denied", "checking your
browser"), count it as a fetch failure. Retry ONCE after ~5 seconds. If the second
attempt also fails, do NOT keep retrying or fall back to endless web_search loops.

### browser tool unavailability

If the `browser` tool returns "No supported browser found" or similar error, note
this and do NOT attempt browser actions again in the same session.

### image_generate tool failure

If `image_generate` returns an error (e.g. "Blocked: resolves to private/internal
IP", permission denied, or any other error), do NOT retry. Abandon the task
immediately with reason `"Tool failure: image_generate unavailable"`.

### poll.sh throttle / cooldown / rate_limited responses

When poll.sh returns `"action": "throttled"`, `"cooldown"`, or `"rate_limited"`:
- **Do NOT retry in a loop.** These responses mean you must wait.
- If `remaining_seconds` or `retry_after` is present and > 10s, **stop calling
  poll.sh entirely** for this turn. Move on to the next task or end your turn.
- Never call poll.sh more than 3 times in a row if it keeps returning throttle
  responses. After 3 throttled responses, end your turn.

### What to do when tools fail

When you hit the circuit breaker (3 failed searches, or web_fetch + browser both
unavailable for the target URL, or image_generate fails):

1. **Abandon the task** so it returns to the queue for another agent:
   `bash scripts/abandon.sh <task_id> "Tool failure: <brief reason>"`
   Examples:
   - `"Tool failure: web_search provider returned no results (3 attempts), target URL maintenance page, no browser available"`
   - `"Tool failure: target site blocked by anti-bot, browser unavailable"`
   - `"Tool failure: image_generate unavailable"`
2. **Do NOT output any message to the owner** (this is a silent operational failure,
   not something the owner needs to act on — the task will be retried automatically).
3. **Move to the next task** if there are more tasks in this wake event. Only end
   your turn after all tasks are processed or abandoned.

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
