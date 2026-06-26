---
name: cyber-girlfriend
description: Build or customize an owner-only proactive companion system with a cyber-girlfriend persona, Markdown private-life context, lightweight relationship memory, and OpenClaw presence cron delivery.
version: 2.1.9
---

# Cyber Girlfriend

Use this skill when the user wants an owner-only proactive companion instead of a purely reactive assistant.

This skill gives the owner:
- proactive companion messages sent on a real schedule
- a core persona in `character-profile.md`
- daily private-life context in `day-schedule.md`
- configurable quiet hours and event-level pacing
- lightweight continuity in `life-log.jsonl`
- optional event media such as photos, audio, or video

## Quick Start

This skill is meant to be set up by an agent, not by hand.

If the user wants the default setup, the simplest path is:

> Help me set up cyber girlfriend.

The agent should then gather the minimum inputs, create or update the local files, wire the default cron jobs, and validate the install before claiming success.

## What The User Needs

For a normal install, the user only needs:
- an OpenClaw runtime
- one working delivery route to the owner
- a few persona and daily-life anchors

The user should not need to:
- hand-write JSON
- hand-write cron payloads
- manually wire runner contracts
- read every reference file before getting started

## Default Setup Shape

The recommended starter setup is:
- one daily schedule builder job that writes `day-schedule.md`
- one `companion-presence` cron that runs a deterministic tick wrapper from an isolated cron session
- 1-4 optional life anchors that are written into `day-schedule.md`

Those anchors are life facts, not guaranteed sends.

## What The Agent Sets Up

The current default active path has two small steps:
- `scripts/companion_presence_tick.py --config <CONFIG>`
- inside that wrapper, `scripts/companion_run.py --stage prepare --no-record-pending`

The wrapper reads local state through the prepare runner and exits quietly when no current event should send. Only when prepare returns `status = "ok"` does it start the stable companion session with the prepared contract. The stable session writes the first-person story, but text delivery goes through `companion_presence_tick.py --send-story --story-stdin`, which reloads the saved delivery contract from the dispatch lock, sends with the external OpenClaw CLI, and commits state only after successful text delivery. If the matched event asks for media, media generation starts after `--send-story` succeeds and finishes asynchronously. The wrapper also starts a deterministic recent-media watcher for the stable companion session, so generated media is delivered through the prepared delivery contract even if the native completion turn falls back to Codex internal UI.

The default local files are:
- `character-profile.md`
- `day-schedule.md`
- `companion-state.json`
- `life-log.jsonl`

Legacy 1.x inputs such as `persona`, `month-plan.json`, `day-context.json`, and the old multi-slot cron path are upgrade-only compatibility inputs, not the default product path.

## Hard Rules

- Never hardcode secrets.
- Keep proactive behavior owner-only unless the user explicitly wants broader scope.
- Keep runtime-specific values in `config.local.json` or environment variables, not published defaults.
- Keep the companion's core persona in `character-profile.md`; treat `config.local.json -> persona` as deprecated migration data.
- Keep presence cron payloads thin; the cron should call `companion_presence_tick.py`, not duplicate long writing instructions in runtime configuration.
- User-defined required events are life anchors, not guaranteed message sends.
- Day schedule events must keep `媒体信息`; leave it empty unless the matched event should produce photo, audio, video, or similar media.
- Final user-visible companion text must be first person from the companion's perspective.
- Do not expose internal JSON, code blocks, step names, debug output, local paths, account ids, channel ids, or session ids in owner-facing messages.
- Do not claim setup or upgrade is complete before a real validation command passes.

## Read This First For Real Setup Or Upgrade

Always read:
- [references/standard-init-upgrade-flow.md](./references/standard-init-upgrade-flow.md)
- [references/configuration.md](./references/configuration.md)
- [references/contract-schema.md](./references/contract-schema.md)

## Choose The Right Reference

- first-time setup or rebuild:
  - [references/first-time-setup.md](./references/first-time-setup.md)
  - [references/agent-first-time-qa-template.md](./references/agent-first-time-qa-template.md)
  - [references/required-events-and-cron.md](./references/required-events-and-cron.md)
- OpenClaw runtime wiring:
  - [references/presence-integration.md](./references/presence-integration.md)
- private-life layer:
  - [references/private-life-layer.md](./references/private-life-layer.md)
  - [references/private-life-cron-templates.md](./references/private-life-cron-templates.md)
  - [references/private-life-prompt-templates.md](./references/private-life-prompt-templates.md)
- custom required event anchors:
  - [references/required-events-and-cron.md](./references/required-events-and-cron.md)
- legacy upgrades:
  - [references/standard-init-upgrade-flow.md](./references/standard-init-upgrade-flow.md)
  - [references/script-contract-v2-migration.md](./references/script-contract-v2-migration.md)

## Version Notes

### 2.1.9

Version 2.1.9 makes text delivery use the same deterministic wrapper boundary as media delivery. The stable companion session must not call the runtime `message(action="send")` tool for presence text. It writes the story and calls `companion_presence_tick.py --send-story --story-stdin`; that helper loads the saved contract from `presence-dispatch.json`, sends through `openclaw message send --channel/--target/--account --message`, and then runs `state_commit.command`. Media events start async media generation only after `--send-story` succeeds.

中文说明：2.1.9 把正文投递也收回到固定脚本入口，不再依赖 Codex runtime 的 message 工具解析自定义渠道。稳定 session 只负责写正文和调用 `--send-story --story-stdin`；脚本按 dispatch lock 里的 `delivery_contract` 显式发文本，成功后再提交状态。这样新用户和老用户都统一走外部 OpenClaw CLI 的真实渠道表，避免 `Unknown channel` 或 current chat 误路由。

### 2.1.8

Version 2.1.8 makes media delivery independent of model follow-up behavior. For media events, `companion_presence_tick.py` now starts a background recent-media watcher immediately after the stable companion session is launched; the watcher finds the next media task created by that stable session, waits for completion, extracts the generated media path, and sends it with the explicit `delivery_contract`. `--watch-media-task` remains the task-id-specific helper, and `--send-media` remains the direct send fallback.

中文说明：2.1.8 不再要求模型在媒体工具返回后“自觉”运行 watcher。wrapper 会自己启动后台 watcher，按稳定 session 和启动时间找到本次生成任务，然后用 `delivery_contract` 显式投递到真实渠道，避开 Codex runtime 的 `internal-ui/current chat` 误路由。

### 2.1.7

Version 2.1.7 adds deterministic media delivery entrypoints for async OpenClaw media tasks. After the main presence turn starts media generation, it runs `companion_presence_tick.py --watch-media-task` with the returned task id; the helper waits for the generated media path and sends through the explicit `delivery_contract` using `openclaw message send --channel/--target/--account/--media`. `--send-media` remains the direct completion fallback and retries once if a result indicates `internal-ui` or current-webchat routing.

中文说明：2.1.7 为异步媒体任务增加固定监控和投递入口。主 turn 启动媒体生成后立刻运行 `--watch-media-task` 等待任务完成并按 `delivery_contract` 显式发送到真实渠道；不再依赖 completion turn 自己理解 current chat。

### 2.1.6

Version 2.1.6 hardens OpenClaw CLI child processes launched by the presence wrapper so cron-inherited CA settings cannot reintroduce Keychain startup failures. It also keeps dispatch-lock startup acknowledgement and launch-error diagnostics in the release contract.

中文说明：2.1.6 加固了 presence wrapper 启动 OpenClaw CLI 子进程时的 CA 环境，避免 cron 继承的系统 CA 设置再次触发 Keychain 启动失败；同时保留稳定 session 启动确认和启动失败诊断能力。

### 2.1.5

Version 2.1.5 removes prompt wording that explicitly names concrete runtime tools while preserving the mandatory real web-search requirements for day-schedule generation and matched-event presence writing.

### 2.1.4

Version 2.1.4 removes the legacy visible `mode` field from the presence prepare contract and default wrapper command. There is now only one public presence flow: cron calls the deterministic wrapper, the wrapper prepares the current event, and matched events are handed to the stable companion session.

### 2.1.3

Version 2.1.3 moves the cron-side current-event decision into `scripts/companion_presence_tick.py`. The visible cron should run in an isolated session and only call that wrapper; the wrapper performs fresh prepare deterministically, then starts the stable companion session only for matched events. Presence writing must run a small public web search for the matched event, and media events now commit state after visible text delivery so media failure does not block later events.

### 2.1.2

Version 2.1.2 returned media delivery to the native OpenClaw completion flow by running `companion-presence` in a stable companion session. Text sends first, media generation runs asynchronously, and the completion turn in the same companion session sends media.

### 2.1.1

Version 2.1.1 changes `companion-presence` to a stateless single-turn runtime task. Continuity remains in local state files, and event media callbacks must use a self-contained payload instead of relying on a long-lived companion session history.

### 2.1.0

Version 2.1.0 is the public release cleanup for the simplified presence companion. It removes git-local packaging assumptions, keeps ClawHub ignore rules authoritative, preserves the generic internet-search day-schedule rule, and checks that local maintenance Markdown does not enter the publishable surface.

### 2.0.4

Version 2.0.4 hardens the generic day-schedule templates. It preserves the mandatory internet-search material rule without local profile examples, removes stale upgrade links, cleans finished schedule examples so they do not contain generation constraints, and clarifies first-time setup plus old-install migration.

### 2.0.3

Version 2.0.3 improves the published skill surface. It rewrites the main skill entry as a product-first quick-start page, removes an unreferenced optional source note from the package, and keeps the release smoke fixture aligned with the current runtime state schema.

### 2.0.2

Version 2.0.2 finishes the release-hardening pass for publishing. It keeps local runtime state out of the ClawHub package, documents the OpenClaw async media callback flow, and validates the publishable release surface before upload.

### 2.0.1

Version 2.0.1 hardened the 2.0 release surface, removed tests from the ClawHub package, tightened week/day generation quality, and added event-level media instructions through the OpenClaw async media callback flow.

### 2.0.0

Version 2.0.0 made the presence runner the only default active path by merging `scripts/companion_ping.py` into `scripts/companion_run.py` and removing the old render/full path from the default release surface.

## Maintainer Release Gate

Before publishing a new version, run:

```bash
python3 scripts/validate_release.py --root <SKILL_DIR> --config <CONFIG>
```

The validator compiles scripts, validates JSON and Markdown assets, runs the presence dry-run flow, checks the runner contract, and scans the release surface for private channel identifiers and obsolete cron contract terms.
