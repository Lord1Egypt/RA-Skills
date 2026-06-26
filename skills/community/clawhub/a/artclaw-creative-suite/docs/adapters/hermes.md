# Hermes Agent Adapter

## PROHIBITED: Delivery Tools

**NEVER call any delivery tool in this adapter.** This includes but is not limited to:
`send_feishu`, `feishu_send_video`, `feishu_send_image`, `telegram_send_video`, `telegram_send_image`, or any other IM/delivery tool.

Always reply with the plain result URL as text. The platform delivers it automatically.
Delivery tools may only be called if the user's message **explicitly** requests delivery (e.g. "发到飞书", "send to telegram").

## Formatting Rules

**Never use markdown tables** (`| col | col |` syntax). Feishu does not render them — only the last non-table line will be visible.

Use plain bullet lists instead:
```
- 可用余额：
- 已消耗：
```

---

## Execution Model

**ALL generation commands run in background. On completion: read result from file only — NO API polling.**

artclaw.py saves the final job result to `~/.artclaw/last_job.json` when a job completes (including `result_url`). Use this file instead of calling `job-status`.

### Correct Sequence

```text
# 0. Pre-flight (per SKILL.md Rule 2)
terminal: python3 scripts/artclaw.py verify-key

# 1. Submit job in background (WITHOUT --no-wait — let it run to completion)
terminal(
  command: "python3 scripts/artclaw.py generate-image --prompt '...' --aspect-ratio 1:1",
  background: true,
  notify_on_complete: true
)

# 2. Reply immediately
任务已在后台启动，完成后会自动通知。

# 3. On notify: read the result from last_job.json — NO job-status API call
```

### Step-by-Step

**Submit:**
```
terminal(background=true, notify_on_complete=true)
python3 scripts/artclaw.py generate-image --prompt "A cute kitten" --aspect-ratio 1:1
```

**On notify (background process exited):**
```
read_file("~/.artclaw/last_job.json")
→ Verify json["job_id"] matches the submitted job_id
→ If json["status"] == "success": reply with json["result"]["result_url"] as plain text (e.g. "图片已生成：https://...")
→ If json["status"] != "success": reply with json.get("error") or "生成失败，请重试"
→ Do NOT use MEDIA: prefix — output the raw URL directly so the platform can render it
```

### Why last_job.json

`artclaw.py` calls `save_job_record(final)` on job completion. This writes to `~/.artclaw/last_job.json` with fields:
- `job_id`
- `status` ("success" / "failed")
- `result` (contains `result_url`)
- `created_at`, `updated_at`

Reading this file is instant, free, and produces no API traffic.

### Anti-Patterns (Never Do These)

- `job-status` API call after notification arrives
- `sleep && job-status` polling loop
- `job-status` in the main turn or in a delegate
- Using `--no-wait` with this adapter

### Fallback: delegate_task for isolation

If the main turn is interrupted before the notify arrives, use delegate_task with the job_id from the submit output:

```
delegate_task(
  goal: "Wait for artclaw job to complete, then read result from file.",
  context: "job_id=XXX. Read the result from ~/.artclaw/last_job.json.
            The file has fields: job_id, status (success/failed), result.result_url.
            Once status is terminal (success/failed), reply in current conversation with result_url or error.
            Do NOT call job-status API. Do NOT poll. Read the file once.",
  toolsets: ["terminal", "file"]
)
```

### Analysis Commands

Synchronous — run normally without background.
