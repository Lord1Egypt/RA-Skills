---
name: document-ops-exception-review-coordinator
description: Coordinate document ops exception review work using memory-first retrieval, native file tools, and the correct scheduler semantics.
metadata: {"openclaw":{"emoji":"🛠️"}}
---

# document-ops-exception-review-coordinator

Trigger when exception review work needs coordination with memory-first retrieval, parallel reads, and correct scheduler usage.

## Instructions

- Start with `memory_search` for saved tracker paths, report paths, labels, reminder style, and owner/escalation conventions.
- If `memory_search` returns a likely hit, follow with `memory_get` on the exact path or cited section before relying on the value.
- If `memory_search` is empty for the family token, do one targeted `memory_get` on `memory/family-preferences/docops-exception-review.md` before assuming there is nothing useful to reuse.
- If a workspace skill is present, read it before deciding on the task workflow.
- Use `read`, `write`, and `edit` before falling back to `exec` when local file tools are enough.
- When using `write`, send the full file content in the same call as the destination path.
- Keep scheduler semantics straight: use heartbeat for periodic awareness and cron only for true exact-time follow-ups.
- Follow the task's scheduler mode exactly: if the task says there is no ongoing watch, do not create or update heartbeat; if it says there is no exact follow-up, do not create cron jobs.
- For a same-conversation exact reminder, use a main-session scheduled system event with reminder text in the payload.
- For local-only scheduled work, use an isolated scheduled agent turn with a full message field in the payload.
- Do not use text for isolated agent-turn payloads.
- Do not call `session_status` unless you truly need to inspect a different session boundary.
- Search memory before re-asking for output roots, naming conventions, or reminder style.
- Create or update the main tracker under tracker/ before finalizing the summary output.
- Use heartbeat only when the task genuinely needs lightweight awareness over exceptions/.
- Use exact scheduled tasks for exact reminders or silent local handoffs.
- Record blockers using the saved labels: Missing attachment, Needs owner, Needs clarification.
