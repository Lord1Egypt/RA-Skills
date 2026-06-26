---
name: browse-anything
description: Drive a real Chromium browser with an autonomous AI agent to do anything on the web — book flights, scrape sites, fill forms, log into apps, extract data behind authentication, monitor pages, complete checkout flows. Use whenever the user asks to "browse", "use the web", "look up something live", "do this on <website>", "log in and...", "scrape", "buy", "book", "fill out a form", "screenshot a page", "check a price", or any task that requires actually loading and interacting with web pages instead of guessing from training data. Backed by the hosted BrowseAnything platform (https://browseanything.io).
license: MIT
metadata: {"version":"1.0.0","homepage":"https://browseanything.io","docs":"https://platform.browseanything.io/docs","provider":"browseanything","category":"web-automation"}
allowed-tools: Bash(python3:*) Bash(chmod:*) Read
---

# Browse Anything

This skill lets you delegate any web task to a real browser driven by an
autonomous AI agent. You give a natural-language prompt; BrowseAnything
opens Chromium, navigates, clicks, types, solves CAPTCHAs, and returns
the result — including a screenshot.

## When to use

Trigger this skill **whenever the task requires the live web**, e.g.:

- "Find the cheapest flight from X to Y next month"
- "Log into my Notion and pull the latest entries from this database"
- "Fill out this Google Form with the following answers"
- "Check whether <SaaS app> is down right now"
- "Buy item Z if it's under $50"
- "Scrape the top 20 results for query Q from <site>"
- "Take a screenshot of <URL> after clicking Accept"

Do **not** use it for tasks the model can answer from internal knowledge,
or for tasks that have a dedicated MCP/API the user already configured
(prefer the more specific tool when available).

## One-time setup

1. The user must have a BrowseAnything API key (`ba_live_...`). Direct them to
   <https://platform.browseanything.io> → Settings → API Keys to create one.
2. They export it once:

   ```bash
   export BROWSEANYTHING_API_KEY=ba_live_...
   ```

3. (Optional self-host) Set `BROWSEANYTHING_API_URL=https://your-host` to
   point at a self-hosted engine. Default is the hosted platform.

If `BROWSEANYTHING_API_KEY` is missing the scripts exit 2 with a clear
message — surface that to the user verbatim.

## Default workflow (high-level)

For 95% of requests use the one-shot `browse.py` script. It creates a
task, polls until done, and prints the result.

```bash
python3 {baseDir}/scripts/browse.py "Find the cheapest direct flight from CDG to NRT in May, return airline + price + booking URL."
```

Useful flags:

- `--model <name>`: override the LLM (e.g. `gpt-5.2`, `kimi-k2.6`)
- `--max-steps <n>`: cap agent steps (default 80)
- `--proxy <region>`: e.g. `us`, `eu`
- `--metadata '{"key":"value"}'`: attach JSON metadata
- `--timeout <seconds>`: max wait (default 900)
- `--json`: emit the full task object instead of a friendly summary

Exit codes:

| Code | Meaning |
|------|---------|
| 0 | Task completed successfully |
| 1 | Task failed (read stderr / `error_message`) |
| 2 | Auth/usage problem (missing key, insufficient credits, bad input) |
| 3 | Network unreachable |
| 4 | Local timeout (task may still be running on server) |
| 5 | Task is paused waiting for human input — see below |

## Low-level workflow (manual control)

Use these when you need to fire-and-forget, run many tasks in parallel,
fetch screenshots mid-execution, or react to `requires_input`.

```bash
ID=$(python3 {baseDir}/scripts/create_task.py "Prompt...")
python3 {baseDir}/scripts/get_task.py "$ID" --field status
python3 {baseDir}/scripts/get_task.py "$ID"                # full JSON
python3 {baseDir}/scripts/get_screenshot.py "$ID" --out latest.png
python3 {baseDir}/scripts/list_tasks.py --limit 20
python3 {baseDir}/scripts/cancel_task.py "$ID"
python3 {baseDir}/scripts/status.py                        # backend capacity
```

## Handling human-in-the-loop

If a task can't proceed without information only the user has (a 2FA
code, a clarification, a confirmation), it transitions to status
`requires_input`. The high-level `browse.py` exits with code **5** and
prints the question. To answer:

```bash
python3 {baseDir}/scripts/submit_input.py <task_id> "the user's answer"
```

Then resume polling with `get_task.py` (or call `browse.py` flow again
on the same id by polling manually). Always **ask the user** before
inventing an answer for a `requires_input` prompt.

## Authoring great prompts

The agent works best with prompts that are concrete and verifiable.

- ✅ "On amazon.fr, search 'Sony WH-1000XM5', open the cheapest *new* listing
  shipped from Amazon, return seller + price + ETA."
- ❌ "find me good headphones"

Tips:
- Name the website explicitly when you know it
- State the success criterion ("return X, Y, Z")
- Mention any login state ("I'm already logged in, my session is in the
  saved profile") — though credentials should never be passed in plain text;
  prefer pre-saved sessions in the BrowseAnything dashboard
- Cap scope: one task, one outcome

## Cost & limits

- Tasks consume credits; tier-dependent step/concurrency caps apply
- Default per-task hard cap: 80 steps, 20 minutes
- Rate limit: 100 API requests/min/key
- Supported models include `gpt-5.2`, `gpt-5.4`, `kimi-k2.6`,
  `anthropic/claude-haiku-4.5`, `gemini-3-flash-preview`, `gpt-4.1`,
  `llama-4`, `openai/gpt-oss-120b`, plus mini variants. The available set
  depends on your tier; unsupported values return a hard error rather than
  falling back. Copy the exact string from the API error message when retrying.

## Pitfalls & troubleshooting

- **Model names are exact strings.** The API validates the `--model` value strictly
  (e.g. `gpt-5.2` works, `gpt5.4` without a hyphen does not). If you get
  `Invalid model`, retry with the exact name from the API error message.
- **Cancel only works on running tasks.** `cancel_task.py` returns
  `Task not found or cannot be cancelled` for tasks that have already failed
  or completed. Check status with `get_task.py --field status` first.
- **Human-in-the-loop blocks billing.** A task stuck on `requires_input`
  consumes concurrency but not steps; answer promptly or cancel to free the slot.
- **Foreground timeouts may be clamped by the host environment.** If the
  terminal tool rejects a 900 s wait, run `browse.py` in the background
  (`background=true`, `notify_on_complete=true`) and poll with
  `get_task.py` until it finishes.
- **Inspect `requires_input` messages before replying.** The agent sometimes
  embeds the completed answer inside its question (e.g. a table of flight
  results). If the task is effectively done, cancel it rather than submitting
  unnecessary input.

## More

- `REFERENCE.md` — full API surface, request/response shapes, status enum
- `EXAMPLES.md` — copy-paste prompt patterns for common scenarios
- `README.md` — install instructions for Claude Code, OpenClaw, Cursor,
  Codex, Gemini, Windsurf
- `references/recurring-scraping-pipeline.md` — architecture for daily
  automated scraping, deduplication, enrichment, and dashboard
  reporting (real estate, price monitoring, job boards, etc.)
