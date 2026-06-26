---
name: clawshier
description: Process receipt or invoice images into structured expenses and log them to Google Sheets. Use when the user wants to scan, log, track, or record an expense from a receipt or invoice image, or when they provide a local file path to a receipt/invoice image. OCR uses OpenAI by default; set CLAWSHIER_VISION_PROVIDER=ollama to use local Ollama instead.
metadata: {"openclaw":{"requires":{"env":["GOOGLE_SHEETS_ID","GOOGLE_SERVICE_ACCOUNT_KEY"]},"primaryEnv":"OPENAI_API_KEY"}}
---

# Clawshier

Process a receipt or invoice image through a four-step pipeline, then reply with a short summary of what was added.

## Input handling

- If the user provides a **local file path** to the image, use that path directly.
- If the user sends an image in chat and a **local attachment path** is available, use that path.
- If no local file path is available for the image, ask the user to resend it as a file or provide a path you can execute against.
- If the user explicitly gives the receipt date, preserve it and pass it to step 3 with `--date YYYY-MM-DD`.

## Workflow

Run the safe pipeline runner. If it fails, retry it up to **2 times** before surfacing the error.

### Primary path — Safe pipeline runner

Run:

```bash
node {baseDir}/scripts/run_pipeline.js --image <path_to_image>
```

If the user explicitly provided a date, always pass it in ISO format:

```bash
node {baseDir}/scripts/run_pipeline.js --image <path_to_image> --date 2026-03-25
```

This runner performs OCR → structure → validate/deduplicate → store internally using JSON files, not shell-interpolated pipeline strings.

It writes to:

- the monthly expense tab (`MM-YY`)
- `Invoice Archive Breakdown`
- `Summary`

It also removes the default `Sheet1` tab if present.

### Handler compatibility note

The individual handlers still support stdin/stdout for testing, but when automating the skill, prefer `scripts/run_pipeline.js` or the handlers' `--input-file/--output-file` options instead of embedding untrusted receipt/LLM output into shell commands.

If OCR reports that the image is not a receipt or invoice, tell the user:

> I couldn't detect a receipt or invoice in that image. Could you try again with a clearer photo?

If the validator reports a duplicate, stop and tell the user:

> This receipt appears to already be logged (vendor, date, total match an existing entry). Skipping.

## Success reply

After a successful run, reply in this format:

> Added expense: **{vendor}** — {total} {currency} on {date} ({category}). Row #{row} in your spreadsheet (tab {MM-YY}).

If the user explicitly asks for tracing/debugging/cost tracing, append a compact per-step trace summary using the last recorded trace file. Otherwise keep the normal success reply short.

## Failure reply

If a step still fails after retries, say which step failed and include the error message.

## Notes

- Use `{baseDir}` exactly so the commands do not depend on the current working directory.
- For old invoices, prefer `--date YYYY-MM-DD` instead of relying on same-day date inference.
- OCR backend selection is machine-level: `CLAWSHIER_VISION_PROVIDER=openai|ollama|auto` (default: `openai`).
- `auto` tries local Ollama first and falls back to OpenAI. Set to `ollama` to force local-only OCR.
- Use `CLAWSHIER_OLLAMA_MODEL`, `CLAWSHIER_OLLAMA_HOST`, and `CLAWSHIER_OLLAMA_MAX_DIMENSION` to control the Ollama OCR backend.
- When `CLAWSHIER_TEST_MODE=1` is present in the environment, the handlers use local test fixtures and a local mock sheet store. Use that for safe smoke tests before touching real APIs.
- Optional tracing: set `CLAWSHIER_TRACE=1` to record per-step timing/usage metadata to `.clawshier-last-trace.json`. Show that trace in chat only when the user explicitly asks for tracing/debugging/cost tracing.
