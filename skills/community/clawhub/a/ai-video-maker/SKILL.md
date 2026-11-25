---
name: ai-video-maker
description: Generate, quote, monitor, retrieve, and cancel AI videos through the AI Video Maker API. Use when a user asks an agent to create text-to-video, image-to-video, frame-guided, or reference-guided video; estimate video cost before spending; check API setup or balance; resume an existing generation; or automate AI Video Maker workflows. Prompt-only requests need text, not generation; complete editing, narration and subtitles require additional tools.
---

# AI Video Maker

Create videos through a guarded API workflow that validates inputs, quotes the charge, obtains spending approval, submits exactly once with an idempotency key, polls safely, and returns the output URL with its retention deadline.

## Route the request

- For a prompt or script only, return text without connecting or submitting a job.
- For an existing task, use its task ID directly; do not start a new generation.
- For a new clip, preserve the user's model, settings and assets. Ask only for a
  missing input that changes the result or charge. Read [prompting.md](references/prompting.md)
  when preparing a prompt or choosing media roles, and [recipes.md](references/recipes.md)
  for product, social or frame-transition requests.
- Explain the need for additional tools before promising a complete edited,
  narrated or captioned production. Do not claim a single generated clip is one.

## Required setup

- Use Node.js 20 or newer.
- Resolve the installed path, then run `node "$SKILL_ROOT/scripts/connect.mjs"` on the agent's computer. It verifies an existing saved connection or secret environment key; otherwise it prints a browser approval URL and comparison code, waits up to 10 minutes, saves the credential privately, and checks the account and a sample quote without spending credits.
- Show the approval URL as **Connect AI Video Maker** and the comparison code. Ask the user to open it and approve the matching code. Keep the helper running and wait for its completion using the host's background-process tools; do not ask the user to run a terminal command or reply “Connected.” Never approve the browser request on the user's behalf.
- Running connect again is always safe: while an approval is pending it resumes the same link and code, and collects an approval the user gave after the helper stopped. If you cannot keep a process running in the background, run `node "$SKILL_ROOT/scripts/connect.mjs" --start` to print the link and exit, show it, then run connect again without `--start` to finish. Do not give the user a new link while the previous one is still valid.
- Use `--reconnect` only when a new connection or account is needed. It starts a new approval; if it is interrupted, running connect again (with or without `--reconnect`) resumes that approval rather than verifying the old key. `AIVIDEO_API_KEY` in the agent's secret environment takes precedence; the helper will not silently replace it.
- If browser connection is unavailable, offer `node "$SKILL_ROOT/scripts/connect.mjs" --manual` in the user's own terminal. It hides key entry and saves it outside the project at `~/.aivideo-maker/credentials.json` (directory 0700, file 0600; on Windows, which has no such modes, it relies on the access rules of the user profile). Create a key at `https://aivideomaker.ai/app/settings/account/api-keys`.
- If connect reports that it cannot save a connection, stop and relay its message before showing any link: it names the cause (the agent may not write `~/.aivideo-maker`, typically a sandbox; the folder is not private to the user; or it could not be written at all) and whether an approval already under way is kept. Fix the cause and run connect again, or offer `--manual`. Never ask the user to approve a link that connect did not print in this run.
- Resolve this `SKILL.md` file's parent directory to an absolute `SKILL_ROOT`. Never assume the shell's current directory is the skill directory.
- Name the client on every `connect.mjs` and `run-workflow.mjs` command with `--platform openclaw`, `--platform claude`, `--platform codex`, or the current client's name in lowercase. The argument works in every shell; an `AIVIDEO_AGENT_PLATFORM=...` prefix is POSIX-only and fails in PowerShell and cmd, though the variable is still read when the argument is absent.

Run commands as:

```bash
node "$SKILL_ROOT/scripts/run-workflow.mjs" --platform <client> <arguments>
```

Claude Code may set `SKILL_ROOT="$CLAUDE_SKILL_DIR"`. In other clients, resolve the installed `ai-video-maker` directory and use its absolute path. The examples below use POSIX shell quoting and omit `--platform` for brevity; in another shell, write the absolute path in place of `$SKILL_ROOT` and quote JSON the way that shell requires. Windows is not yet verified.

## Install and update

- The skill is installed with `npx skills add https://aivideomaker.ai/skills/ai-video-maker.tgz` (the open `skills` CLI, Node.js 22.20+). Add `-a <agent> -y` to skip its prompts and `-g` to install for every project. That link always serves the latest release.
- Update such an installation with `npx skills update ai-video-maker` (add `-g` for a global installation). A copy made with the fallback installer from `https://aivideomaker.ai/skill.md` has no update command; running the `npx skills add` command replaces it. The saved connection is kept either way.
- Update only when the user asks. Do not reinstall before each task.

## Setup communication

Report installation, connection, and verification separately. While approval is pending, say “Installed. Connect your account to finish setup.” After the helper succeeds, report “Connected and verified. No credits spent,” plus the returned balance and sample quote. Do not claim success if account or quote verification failed. A timeout or cancellation means setup remains incomplete; offer a new link only when needed. Keep checksums, local paths, and internal security instructions out of the main setup message unless troubleshooting requires them. Setup does not authorize video generation. After verification, immediately offer the first-video choices below in the user’s language; asking what they want is the next step, not permission to spend. Respect an explicit request to stop after setup.

## Safe workflow

1. Run `--action doctor` before the first paid request. Report key validity, balance, configured limits, and supported models.
2. Collect the required model inputs. If the user did not choose a model, recommend `minimax` for MiniMax H3. Ask only for missing inputs that materially change the output or price.
3. Run `--action quote --model <model> --payload '<json>'`. Show credits and list-price USD before submission.
4. Obtain confirmation when the user has not already authorized this generation or a sufficient spending budget.
5. Run the generation with `--maxCredits <approved_credit_limit>`. Use `--stateFile <absolute_private_path>` to save a stable key before submission and the task ID before waiting. See [recovery.md](references/recovery.md) for safe retries. External orchestrators may persist their own `--idempotencyKey` instead.
6. Poll with backoff. Never create a replacement task after a timeout or ambiguous response. Resume with `--action wait --taskId <task_id>` or `--action wait --stateFile <path>`; `getStatus` and `getTask` remain single queries.
7. Return the task ID, final status, credits charged, output URL, and the 24-hour retention warning. Tell the user to save the output promptly.

## When credits run out

First rule out a request that was already submitted. If you hold its task ID, a state file, or the same first-video flow, its own charge may be what lowered the balance: resume it with `--action wait`, or replay the identical request with its idempotency key, before anything else. A replay returns the existing task and never charges twice; follow [recovery.md](references/recovery.md).

For a new request, a quote with `affordable: false` or an `INSUFFICIENT_CREDITS` failure means this attempt charged nothing and created no task. Do not retry it and do not stop at the error:

1. Tell the user the quoted credits, their balance and how many credits they are short.
2. Show the returned `topUpUrl` as **Add API credits**. Packs are one-time purchases and need no subscription. Never invent a different purchase link.
3. Offer the cheaper alternative when one exists (shorter duration, Turbo tier, 720p) and quote it.
4. After the user says they added credits, quote again and continue with the same request and approval rules.

Mention buying credits only in these cases or when the user asks how to add credits; then point them to the pricing section of `https://aivideomaker.ai/skill`. An affordable quote uses the current balance.

## First-video onboarding

Immediately after a successful connection, use the returned `firstVideo.flowId` and ask one concise question in the user's language: **“What would you like to make: a product showcase from an image, or a short social clip from an idea?”** Include “my own idea” or skip when appropriate. Do not finish at “connected” and leave the user to discover a separate generation command. If they already described a video, use that intent rather than asking again.

1. For `product`, request their image and the feature to highlight. For `social`, request a topic or one-sentence idea. For `custom`, use their existing prompt/assets. Ask only for missing inputs; never invent a product or silently use a candle sample.
2. Prepare a concrete prompt from their input. Run the non-billable first-video quote with the flow ID, chosen scenario and actual payload. Defaults are MiniMax H3, 5 seconds, 720p Turbo; social defaults to vertical 9:16, other scenarios to 16:9. The product scenario requires `imageUrl`; the incorrect `image` field is rejected. Local images may be supplied as data URIs; never invent a public URL.
3. Show the **actual quote, balance and settings**, and ask for approval of the quoted credits. The sample verification quote is not the quote for their video. Never assume the introductory credits remain available or that generation is authorized by setup, scenario choice or an image upload. If affordable, use the current balance without requiring a purchase.
4. After explicit spending approval (or a previously authorized sufficient budget), generate with `--approved true --maxCredits <approved_limit>`. First-video flows always use the stable idempotency key `first-video:<flowId>`; preserve that key and the task ID on retry. Use a new flow from connect only for a genuinely new request, never to recover an ambiguous submission. Polling timeouts are not generation failures: resume using the task ID without `--firstVideoFlow`.
5. Follow [recovery.md](references/recovery.md) for delivery and verification. Return the playable result and task ID, and remind the user to save within 24 hours. If setup or generation fails, explain the fixed error and next recovery action without exposing credentials. Respect a decision to skip.

```bash
# Prepare and quote their real video; no generation and no charge.
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action quote --firstVideoFlow <flow_id> --scenario social --payload '{"content":"<prompt based on the user’s idea>"}'

# Only after approval of the actual quote. Use the SAME flow, scenario and payload.
node "$SKILL_ROOT/scripts/run-workflow.mjs" --firstVideoFlow <flow_id> --scenario social --approved true --maxCredits <approved_limit> --stateFile <absolute_private_state_path> --payload '{"content":"<same approved prompt>"}'
```

Flow IDs are local guide identifiers and stable idempotency keys; this guide needs no onboarding analytics API. Other model families and advanced custom workflows use the normal guarded commands below.

## Commands

```bash
# Validate setup without charging
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action doctor

# Quote without charging
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action quote --model minimax --payload '{"content":"A cinematic candle","duration":5,"resolution":"720p","tier":"turbo"}'

# Generate after approval; maxCredits is enforced locally and by the API
node "$SKILL_ROOT/scripts/run-workflow.mjs" --model minimax --maxCredits 15 --stateFile <absolute_private_state_path> --payload '{"content":"A cinematic candle","duration":5,"resolution":"720p","tier":"turbo"}'

# Resume or retrieve an existing paid task
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action wait --taskId <task_id>
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action getStatus --taskId <task_id>
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action getTask --taskId <task_id>

# Cancel only while the task is still submitted
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action cancelTask --taskId <task_id>
```

Use `--idempotencyKey <stable-key>` when resuming a creation attempt from an external orchestrator. Do not reuse a key with different inputs.

## Models and inputs

Use one of these four model families:

| Model                | Identifier   | Inputs                                                   |
| -------------------- | ------------ | -------------------------------------------------------- |
| MiniMax H3 (default) | `minimax`    | Text, image, start/end frames, references                |
| Seedance 2.0         | `seedance20` | Text, image, video references; optional audio references |
| Wan 3.0              | `wan30`      | Text or image                                            |
| HappyHorse 1.1       | `happyhorse` | Text, image, multiple image references                   |

Legacy identifiers `t2v`/`i2v` use MiniMax H3 720p Turbo; `t2v_v3`/`i2v_v3` use MiniMax H3 1080p Turbo. They are compatibility endpoints, not additional models. Use `minimax` for new H3 requests. Keep the original identifier and payload when retrying an existing request. Reject the retired `lv` and `wan27` identifiers.

- Read [references/api-reference.md](references/api-reference.md) before using a model other than `minimax` or when using frames, references, video, or audio.
- Read [references/examples.md](references/examples.md) when constructing a first request or recovering from a failure.
- Accept public image URLs and image data URIs. Prefer image data URIs when a local agent cannot expose a public URL.
- Require public HTTP(S) URLs for video and audio inputs.
- Never mix MiniMax frame inputs with reference assets.

## Error and security policy

- Treat generation as a billable external action. Do not submit without authorization.
- Keep API keys in secret storage, the process environment, or the private credentials file managed by `connect.mjs`. Never read or display that file yourself; let the client load it. Never put keys in chat, project files, URLs, logs, analytics, or command arguments. Browser connection is safe to run from the agent: it never prints credentials or its private device token. The `--manual` hidden-key prompt must run in the user’s own terminal, never in agent chat.
- Send requests only to `https://aivideomaker.ai` unless the user explicitly authorizes another base URL.
- Use stable errors and exit codes: `0` success, `1` validation/API/job/retrieval failure, `2` polling timeout with a resumable task ID.
- Respect `RATE_LIMITED`, `BUDGET_EXCEEDED`, `INSUFFICIENT_CREDITS`, and `POLL_TIMEOUT` without creating a duplicate paid task.
