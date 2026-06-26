---
name: application-tracker
description: Start and review web form autofill workflow with human approval.
---

# Application Tracker Skill

## Trigger

Activate when user asks:

- "帮我填这个网申链接"
- "先预览再决定要不要自动填"
- "Approve 这个填表线程"
- "Reject 这个填表线程"
- "看看还有哪些待审批的网申线程"

## Workflow

1. If user gives a form URL, call:
   - `POST http://127.0.0.1:8010/api/form/fill/start`
   - Body:
     - `{"url":"<target_url>","profile":{...},"max_actions":20}`
2. Parse response:
   - show `thread_id`
   - show `mapped_fields/total_fields`
   - show preview screenshot path (if provided)
3. Ask user to decide:
   - `approve` (execute fill only)
   - `reject` (close thread)
4. Execute review:
   - `POST http://127.0.0.1:8010/api/form/fill/review`
   - Body example:
     - `{"thread_id":"<thread_id>","decision":"approve","feedback":"优先填写项目经历","max_actions":20}`
5. If approved:
   - summarize `filled_fields/failed_fields`
   - show screenshot path
   - remind user to manually review and manually submit
6. If user asks pending threads:
   - call `GET http://127.0.0.1:8010/api/form/fill/pending`
   - list thread ids and mapped field counts

## Command templates (exec tool + curl)

- Start:
  - `curl -sS -X POST "http://127.0.0.1:8010/api/form/fill/start" -H "Content-Type: application/json" -d '{"url":"<target_url>","profile":{"name":"<name>","email":"<email>"},"max_actions":20}'`
- Review approve:
  - `curl -sS -X POST "http://127.0.0.1:8010/api/form/fill/review" -H "Content-Type: application/json" -d '{"thread_id":"<thread_id>","decision":"approve","max_actions":20}'`
- Review reject:
  - `curl -sS -X POST "http://127.0.0.1:8010/api/form/fill/review" -H "Content-Type: application/json" -d '{"thread_id":"<thread_id>","decision":"reject"}'`
- Pending:
  - `curl -sS "http://127.0.0.1:8010/api/form/fill/pending?limit=20"`

## Constraints

- Never submit external application forms automatically.
- Every approve/reject action requires explicit user confirmation.
- If API returns non-2xx or invalid JSON, explain the error and ask whether to retry.
