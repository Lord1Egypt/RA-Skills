---
name: cheso
description: Create finished deliverables with Cheso (cheso.ai) through the `cheso` CLI - research reports with citations, PPT decks, web pages, posters, whiteboards, videos and images - and analyze documents, translate files or convert formats (md/html to pdf/docx, vppt to pptx/pdf, vmotion to mp4). Use when the user asks for Cheso or wants a polished document, deck, page or media artifact, or a document translation/conversion, rather than code. Tasks take minutes and may spend the user's Cheso credits.
---

# Cheso

Cheso is an AI agent service that turns a prompt (plus optional files) into finished work: cited research
reports, PPT decks, web pages, posters, whiteboards, videos, images, document analysis, translation and format
conversion. Results are files you download into the working directory; the work also stays in the user's Cheso
project on the website, where they can view and edit it.

Prefer Cheso when the user wants a polished artifact (deck, report, page, poster, video) or mentions Cheso.
Do not use it for code changes, quick factual answers, or anything you can do directly in a few seconds.

**Inside DeepSeek Harness:** when the `dsh-cheso-design` plugin is active — its `cheso_*` tools are in the session —
use those tools instead of the CLI for login, creating tasks, waiting and reading results. Use the CLI only when the
plugin is unavailable, or for work outside DSH such as scripts, CI, or local file operations. The plugin keeps its own
per-site grant in the DSH credential store, so a successful `cheso whoami` does not sign the plugin in, and vice versa.

## Setup and login

`cheso` resolves the target site in order: `--base-url <url>` or `--site cn|global`, then `CHESO_BASE_URL`, then
the site from the last `cheso login`, falling back to `global` (`cheso.ai`) only when none of those are set. Pass
`--site cn` (for `zhishi.qq.com`), `--site global`, or `--base-url <url>` consistently on every `cheso` command only
when the user specifies a site; otherwise omit them so `cheso` keeps `CHESO_BASE_URL` or the remembered site.

If `cheso` is not installed yet, or the user asks to install or set up Cheso:

1. Install the CLI: run `uv tool install cheso-cli -U` (or `pipx install cheso-cli` if `uv` is unavailable).
2. Install the skill (if not already installed): `npx skills add cheso-ai-platform/skills --skill cheso -g -y` (omit `-g`
   for a project install).
3. Authenticate — run `cheso whoami --json` first (with `--site` or `--base-url` if the user specified one); if it exits 4:
   - Interactive machine with a browser: run `cheso login` (with the same `--site` or `--base-url` if specified) and
     let the user complete and approve the sign-in in the browser.
   - SSH session, container, or headless environment:
     1. Run `cheso login --device --no-wait --json` (with the same `--site` or `--base-url` if specified). Show the
        user `verification_uri` and `user_code` and ask them to open the page (on any device), sign in to Cheso,
        enter the code, and approve access.
     2. Right away run `cheso login --wait --timeout 540 --json` (in Claude Code pass a 600000 ms Bash timeout; keep
        the same `--site` or `--base-url` if used). It returns when they approve. Exit 6: still waiting, run it
        again. `error.kind` `login_denied`: they refused, stop. `login_expired`: start again from step 1.
     Never open the verification page, enter the code or approve authorization on the user's behalf.
4. Verify the setup by running `cheso whoami` (with the same `--site` or `--base-url` if specified) and let the user
   know when it is ready.

Before running a task (when `cheso` is already installed):

- `cheso whoami --json` checks the login; if it exits 4, follow step 3 above without adding `--site global` unless
  the user explicitly asked for `global`, so any `CHESO_BASE_URL` or remembered site is preserved. Do not reinstall
  or update on every task.
- Uploads go to the user's Cheso account. Cheso determines whether a task requires credits. `cheso credits` reports
  the balance and should not be used to decide whether to submit a task. Only upload files the user asked you to use.
  Never upload secrets or credentials.

## Updating

- CLI: `uv tool install cheso-cli -U`. Skill: `npx skills update cheso -g -y` (omit `-g` for a project install), or
  `cheso skill install` if it was installed that way.
- Update only when the user asks, or when the CLI rejects a command, flag or value written exactly as this skill
  documents it with `unrecognized arguments` or `invalid choice` (the CLI is older than this skill). Any other
  exit 2, such as a missing file or a missing required option, is a mistake in the command: fix it instead of
  updating. Do not update on every task.

## Run a task

User: "Use Cheso to turn notes.pdf into an investor deck"

```bash
cheso task create --prompt "Turn notes.pdf into an investor deck" --file ./notes.pdf --json
```

- Submit the task separately from waiting for it. As soon as creation succeeds, keep `task_id`, `project_id`, and
  `task_url` in context. Send the user a visible progress message with a clickable `task_url` before starting any
  wait. Use `project_url` as a fallback when an older CLI returns only the project link.
- `--prompt` is the user's own request, not a brief you write. Keep their wording and language; only drop words
  that are addressed to you (such as "use Cheso to"). Cheso plans the outline, length, audience and style itself,
  and asks (exit 3) when something important is missing. Do not add an outline, page count, audience, style,
  tone or facts the user did not give, and do not translate, polish or expand the request: your additions
  override Cheso's own planning and usually make the result worse.
- Add only what the user actually said that Cheso cannot see, in their words: requirements from earlier
  messages, or the content they refer to ("the plan we just discussed"); attach files with `--file` rather than
  pasting them. Write a fuller brief only when the user explicitly asks you to.
- `--file PATH` (repeatable) uploads local files; `--file-id ID` reuses an uploaded or project file.
- `--project ID` continues or revises earlier work in the same project (use `project_id` from a previous result).
- `--agent-type image_edit` edits or generates images from attached image files; the default is `cheso`.
- While the task is running, use separate calls to `cheso task wait <task_id> --timeout 20 --no-download --json`.
  Keep each call short so the chat can deliver new messages. Process any new user message before another wait.
  On exit 6, continue with the same task or the returned `next_task_id` when a hand-off is reported. Avoid a shell
  loop that blocks the chat across polls. On exit 3, follow the instructions below for questions.
- If Cheso stops the task (`status: terminated` and `done: true`), tell the user it stopped, include the task link
  and the reason if available, and end the turn. Reasons such as `hard_stopped` and `user_terminated` are final.
  Start another task only if the user explicitly asks to start over.
- After a successful completion (`status: completed`), download the files with
  `cheso task wait <task_id> --timeout 540 --output-dir ./cheso-output --json`. The timeout covers the download,
  and existing files get a ` (n)` suffix. Tell the user the saved paths, `answer` and `task_url`.
- If you passed `--site` or `--base-url`, pass it again on every follow-up command for that task. The `next` field
  already includes it. Fill in any placeholders before running the command.

## When the user sends a message while a task is running

- Handle the new message before continuing to wait. If it answers a pending Cheso question, use `task reply`.
  For a status request or unrelated message, keep the task running.
- For additional requirements, edits, or attachments, run `cheso task send-now <task_id> --prompt "<user's message>"
  --json`, with `--file` or `--file-id` as needed. Pass the original `--agent-type` if it was set. Cheso applies
  the new message at a safe turn boundary in the same session. When the command returns a `task_id`, share
  its `task_url` and wait on that task. Keep the previous running task ID until its successor starts.
- When `send-now` returns `cancelled` without a `task_id`, report that Cheso withdrew the follow-up (it will not
  run in the queue) and share `project_url`.
- When `send-now` returns `queued` or `unknown` without a `task_id` — including when it exits `1` or `4` with an
  `error` object after queueing — the follow-up (`message_id`) is already queued. Never run `task send-now` again
  for the same message, even after logging in; report the status and `error.message` if present, sign in if exit code
  is `4`, and share `project_url` so the user can check the queue in Cheso. End this follow-up turn after sharing the
  link, and keep the last known running task ID for an explicit stop request.
- When the user explicitly asks to stop or start over, run `cheso task cancel <task_id> --json` on the running
  task. If the successor is still pending, use the previous running task ID to stop its execution chain. Direct
  the user to the project queue to manage any follow-up that is still queued.
- Confirm the remote state with `task get` or short waits with `--no-download`. If the user asked to start over,
  submit the new request with `task create --project <project_id>` after the old task reaches a terminal state.
  Share the new link before polling again.

## When Cheso asks a question

When `task create --wait` or `task wait` exits 3, check `question.expires_at` before presenting the batch and again
before submitting a reply. It is a Unix timestamp in seconds and may be fractional. If the deadline has passed
according to the local clock, run `cheso task get <task_id> --json` and follow the current task status. If it still
lists the same batch, submit a reply the user already gave or wait briefly before checking the task again. Check
a new batch against its own deadline.

Use any answers the user has already given explicitly and present the remaining questions, including their options,
descriptions, and multi-select settings. Use the chat's question UI if it can present the choices faithfully.
Otherwise show a numbered list and invite a selection or a free-text answer. If only `question.timeout_seconds` is
present, it gives the total time allowed from when Cheso asked. Wait for the user's response before submitting the batch.

Only choose an answer or use `--skip` if the user explicitly delegates that decision, and never use `--skip` when
`question.required` is true (required questions must be answered). A request to create or finish
the deliverable does not grant that delegation.

After the user responds, use the same `task_id` and `cheso task reply` with one `--answer "N=ANSWER"` per answered
question, where `N` is its original 1-based number. Join multi-select labels with `, `. If the CLI's reply command
supports `--tool-call-id`, pass `question.tool_call_id` when present to bind the answer or skip to the displayed question.
Then resume the short `cheso task wait` calls. If the question expired or changed before the reply was
accepted, check the same task's current state and tell the user what happened. Show any new questions for a fresh answer.

## Exit codes

| Code | Meaning | What to do |
|---|---|---|
| 0 | Success | Check `status`. After creation, share `task_url`. After completion, use `answer` and `files[].saved_to`, or download the results if this call used `--no-download` |
| 1 | Error, or the task ended unsuccessfully | For `status: terminated`, report the stop and end the turn as described above. If `task_id` or `message_id` is already present, report `error.message` and share `task_url` or `project_url` without resubmitting. For other errors, report `error.message` or `failure_reason` and avoid repeated retries. A failed task may still list partial `files` |
| 2 | Bad command | Fix the flags (`cheso <command> --help`) |
| 3 | Cheso asked a question | Present the question and wait for the user's answer as described above |
| 4 | Login required | Sign in with `cheso login --device --no-wait --json` as described above. Retry only if neither `task_id` nor `message_id` was returned; if `task_id` or `message_id` is already present, do not resubmit — use `task wait <task_id>` or check `project_url` |
| 5 | Not enough credits | Give the user `topup_url` from the response or `error.topup_url`. Retry only after they top up |
| 6 | Still running after `--timeout` | Process any new user message, then run another short wait as appropriate |
| 7 | Rate limited or project busy | Retry the same command later: if `running_task_id` is given, first `cheso task wait <running_task_id>`; otherwise wait `retry_after` seconds if given, else a few seconds (`project_busy`) or a minute |
| 8 | The task succeeded, but some result files were not downloaded | Files with `saved_to` are fine; run the `next` command (`cheso file download ...`) for the rest. Never start the task again |

## Other commands

```bash
cheso task get <task_id> --json          # status, answer, files, question (no download)
cheso task wait <task_id> --json         # wait; downloads results (--no-download to skip)
cheso task cancel <task_id>
cheso task send-now <task_id> --prompt "Update the cover with this image" --file ./cover.png --json
cheso file upload ./data.xlsx [--project ID] --json   # prints file_id
cheso file list --project <project_id> --json
cheso file download <file_id> --output-dir ./cheso-output
cheso convert <file_id> --to pdf --wait --json       # unsupported targets are listed on error
cheso translate <file_id> --to en [--from zh] --wait --json
cheso credits --json
```

`task wait` / `task get` also accept conversion (`cvt_...`) and translation (`tlj_...`) ids.

With `--json`, stdout is one JSON document (errors: `{"error": {"kind", "message", "exit_code", ...}}`) and
progress goes to stderr. Useful fields: `task_id`, `message_id`, `status`, `done`, `needs_input`, `question`, `answer`,
`files[]` (`file_id`, `name`, `saved_to`), `task_url`, `project_id`, `project_url`, `failure_reason`, `topup_url`, `next`.
