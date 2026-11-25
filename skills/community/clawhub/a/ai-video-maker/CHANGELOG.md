# Changelog

## 2.1.4 — 2026-11-22

- Add `--platform <codex|claude|openclaw>` to `connect.mjs` and `run-workflow.mjs`, so setup commands no longer need the `AIVIDEO_AGENT_PLATFORM=...` prefix, which is POSIX-only and fails in PowerShell and cmd. The environment variable still works when the argument is absent. Not yet verified on a Windows machine.
- Document installation with `npx skills add https://aivideomaker.ai/skills/ai-video-maker.tgz` and updates with `npx skills update`. The version-free archive link always serves the latest release.

## 2.1.3 — 2026-11-21

- Check that the private credentials folder can hold a key before requesting a browser approval. An agent that cannot write `~/.aivideo-maker` (a sandbox, wrong permissions, or a saved key that cannot be replaced) is told so up front instead of after the user approved, when the issued key was lost.
- Say whether an approval already under way is kept, and name the actual cause instead of always blaming permissions.
- Make `connect.mjs --start` fail when it cannot keep the approval for the next run, instead of printing a link nothing could finish.
- Give unsafe or damaged saved credentials an error that names a way out, instead of asking to run connect again.
- Report a link or wrong kind of entry in place of the credentials folder or file as such, not as a permissions problem.
- Stop applying Unix permission checks on Windows, where files have no such modes; privacy there relies on the user profile. Not yet verified on a Windows machine.

## 2.1.2 — 2026-11-19

- Resume a pending browser approval when the connect helper is run again, including one started with `--reconnect`, so an approval given after the helper stopped is no longer lost.
- Add `connect.mjs --start` to print the approval link without waiting, for agents that cannot keep a background process.
- Keep the approval resumable after a passing network fault; only a denied, expired or already-used approval ends it.
- Poll at the normal interval when the server asks to slow down, and stop handing out a link that is about to expire.
- Return the official link for adding API credits when a new quote is unaffordable or generation fails with `INSUFFICIENT_CREDITS`, while still resuming a request that was already paid for.

## 2.1.1 — 2026-11-14

- Guide real product/social first videos after connection, preserving quote and spending approval.
- Validate product images using MiniMax imageUrl and reject the incorrect image field.
- Add intent routing, mode-specific prompting, recipes and delivery checks.
- Save optional private recovery state before submission and resume waiting without creating a task.
- Recover accepted first-video requests after their debit lowers the balance; new debits remain server-guarded.
- Distinguish terminal task failures and cancellation from retryable status-query failures.

## 2.1.0 — 2026-09-27

- Add browser-approved agent connections with expiring sessions and automatic account and quote verification.
- Recover temporary connection failures and lost responses without issuing duplicate keys.
- Preserve the approval link through signup and email verification.
- Keep hidden terminal API-key entry as an explicit `--manual` fallback.
- Distinguish installation, connection, and verification without requiring a manual chat handoff or blanket session restart.

## 2.0.0 — 2026-09-20

- Replace the public Wan 2.7 model identifier with `wan30`, backed by Alibaba Cloud's Wan 3.0 video model.
- Keep the existing Wan duration, aspect-ratio, and prompt-extension contract while expanding resolution support.
- Add Wan 3.0 480P output with pricing of 8 credits/second; 720P and 1080P use 15 and 30 credits/second.
- Preserve in-flight legacy tasks while rejecting new `wan27` requests.

## 1.0.16 — 2026-09-13

- Add a terminal connection command that validates API keys without charging and saves them privately outside the project.
- Load saved credentials automatically, with environment variables taking precedence.
- Include connection helpers in the downloadable release.

## 1.0.15 — 2026-09-06

- Rename the package to `ai-video-maker` for consistent installation and discovery.
- Add no-charge doctor and quote workflows, server-enforced spend limits, and stable idempotency.
- Add a dedicated MiniMax H3 contract with numeric 5–20 second durations, 720p/1080p output, Turbo/Base tiers, frame inputs, and reference assets.
- Validate Seedance 2.0, Wan 2.7, and HappyHorse 1.1 payloads before submission.
- Preserve task IDs and idempotency keys across polling timeouts and ambiguous responses.
- Require Node.js 20 or newer and keep machine-readable JSON on stdout.
- Synchronize package, client, registry, OpenAPI, and website version metadata.
