---
name: ai-video-maker
description: Generate, quote, monitor, retrieve, and cancel AI videos through the AI Video Maker API. Use when a user asks an agent to create text-to-video, image-to-video, frame-guided, or reference-guided video; estimate video cost before spending; check API setup or balance; resume an existing generation; or automate AI Video Maker workflows.
---

# AI Video Maker

Create videos through a guarded API workflow that validates inputs, quotes the charge, obtains spending approval, submits exactly once with an idempotency key, polls safely, and returns the output URL with its retention deadline.

## Required setup

- Use Node.js 20 or newer.
- Resolve the installed path, then run `node "$SKILL_ROOT/scripts/connect.mjs"` on the agent's computer. It verifies an existing saved connection or secret environment key; otherwise it prints a browser approval URL and comparison code, waits up to 10 minutes, saves the credential privately, and checks the account and a sample quote without spending credits.
- Show the approval URL as **Connect AI Video Maker** and the comparison code. Ask the user to open it and approve the matching code. Keep the helper running and wait for its completion using the host's background-process tools; do not ask the user to run a terminal command or reply “Connected.” Never approve the browser request on the user's behalf.
- Use `--reconnect` only when a new connection or account is needed. `AIVIDEO_API_KEY` in the agent's secret environment takes precedence; the helper will not silently replace it.
- If browser connection is unavailable, offer `node "$SKILL_ROOT/scripts/connect.mjs" --manual` in the user's own terminal. It hides key entry and saves it outside the project at `~/.aivideo-maker/credentials.json` (directory 0700, file 0600). Create a key at `https://aivideomaker.ai/app/settings/account/api-keys`.
- Resolve this `SKILL.md` file's parent directory to an absolute `SKILL_ROOT`. Never assume the shell's current directory is the skill directory.
- Set `AIVIDEO_AGENT_PLATFORM` to `openclaw`, `claude`, `codex`, or the current client name.

Run commands as:

```bash
node "$SKILL_ROOT/scripts/run-workflow.mjs" <arguments>
```

Claude Code may set `SKILL_ROOT="$CLAUDE_SKILL_DIR"`. In other clients, resolve the installed `ai-video-maker` directory and use its absolute path.

## Setup communication

Report installation, connection, and verification separately. While approval is pending, say “Installed. Connect your account to finish setup.” After the helper succeeds, report “Connected and verified. No credits spent,” plus the returned balance and sample quote. Do not claim success if account or quote verification failed. A timeout or cancellation means setup remains incomplete; offer a new link only when needed. Keep checksums, local paths, and internal security instructions out of the main setup message unless troubleshooting requires them. Setup does not authorize video generation.

## Safe workflow

1. Run `--action doctor` before the first paid request. Report key validity, balance, configured limits, and supported models.
2. Collect the required model inputs. If the user did not choose a model, recommend `minimax` for MiniMax H3. Ask only for missing inputs that materially change the output or price.
3. Run `--action quote --model <model> --payload '<json>'`. Show credits and list-price USD before submission.
4. Obtain confirmation when the user has not already authorized this generation or a sufficient spending budget.
5. Run the generation with `--maxCredits <approved_credit_limit>`. The client creates an idempotency key automatically; preserve it with the task ID.
6. Poll with backoff. Never create a replacement task after a timeout or ambiguous response. Resume the returned task with `getStatus` or `getTask`.
7. Return the task ID, final status, credits charged, output URL, and the 24-hour retention warning. Tell the user to save the output promptly.

## First-video onboarding

When the user asks to try the skill or create a first sample, use `minimax`, 5 seconds, `720p`, `tier=turbo`, and `aspectRatio=16:9` unless they specify different settings. Use their prompt, or offer the candle example in [references/examples.md](references/examples.md) when they only want a test. Do not turn an installation or setup request into permission to generate.

- Run doctor and quote first. Report the actual remaining balance and quoted credits; never assume introductory credits are still available.
- The first sample normally quotes 15 credits. Existing credits can cover it without a purchase; do not direct users to buy a pack when the quote says it is affordable.
- If setup fails, check the Node version, resolved skill path, and whether the saved connection or `AIVIDEO_API_KEY` is available on the agent's computer. Retry verification using the saved connection; use browser reconnect for an invalid key. Never ask them to paste the key into chat. A host may need a new session to discover a newly installed skill, but the helper can verify credentials in the current task.
- Finish by returning the playable output link and task ID. A local timeout is a reason to resume polling, not to buy more credits or generate again.

## Commands

```bash
# Validate setup without charging
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action doctor

# Quote without charging
node "$SKILL_ROOT/scripts/run-workflow.mjs" --action quote --model minimax --payload '{"content":"A cinematic candle","duration":5,"resolution":"720p","tier":"turbo"}'

# Generate after approval; maxCredits is enforced locally and by the API
node "$SKILL_ROOT/scripts/run-workflow.mjs" --model minimax --maxCredits 15 --payload '{"content":"A cinematic candle","duration":5,"resolution":"720p","tier":"turbo"}'

# Resume or retrieve an existing paid task
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
