---
name: bookmark-organize
description: Organize Chrome bookmarks through OpenClaw with preview, explicit confirmation, apply, undo, and a local Chrome executor bridge. Use for conservative Chrome bookmark cleanup and folder organization.
version: 0.1.0
license: MIT
homepage: https://github.com/xiaoshidefeng/bookmark-organize-skill
category: productivity
emoji: 🔖
usage: /skill bookmark-organize [natural-language bookmark organization request]
user-invocable: true
requires:
  - macOS
  - Node.js 18 or newer
  - Google Chrome
  - Manual one-time loading of the bundled unpacked Chrome executor extension
metadata:
  openclaw:
    emoji: 🔖
    os:
      - darwin
---

## ClawHub Package Notes

This ClawHub build is self-contained. The installed skill folder includes:

- `bridges/` for the local bridge server and preflight scripts
- `apps/chrome-executor-extension/` for the bundled unpacked Chrome executor extension
- `package.json` with the local bridge dependency

When this skill says `<skill-folder>`, use the installed ClawHub skill folder containing this `SKILL.md` file.

Do not symlink or modify OpenClaw configuration during setup. ClawHub/OpenClaw owns skill installation. The only manual browser step is loading the bundled Chrome executor extension once from the installed skill folder.

# Bookmark Organize

这是一个“计划优先、显式确认、桥接执行”的技能，不是普通聊天提示。

## Host Workflow

The host should treat this skill as an operational workflow, not just extra prose.

Invocation:

- Preferred generic command: `/skill bookmark-organize [自然语言整理需求]`
- If OpenClaw exposes a direct skill command, use `/bookmark_organize ...`; skill command names are sanitized, so `/bookmark-organize ...` may not exist.

User-facing modes:

- `setup` or `doctor`: run the setup/doctor flow, open Chrome extension settings if needed, and report the next single user action
- `organize` or any natural-language cleanup request: run doctor/preflight first, then preview a plan
- `apply`: run `bridge:ensure-live`, validate the latest plan, then apply only after explicit confirmation
- `undo`: run `bridge:ensure-live`, call `POST /undo`, and report the bridge result

Shortest safe path:

1. run the local preflight wrapper from this skill folder
2. fetch live bookmark context from `POST /context`
3. generate a conservative preview
4. wait for explicit confirmation
5. run `bridge:ensure-live` again before any apply or undo
6. call `POST /validate`
7. call `POST /apply` or `POST /undo`
8. report only bridge-verified results

Portable preflight command:

```bash
node <skill-folder>/scripts/run-repo-script.mjs bridge:preflight
```

Portable first-run setup command:

```bash
node <skill-folder>/scripts/run-repo-script.mjs setup
```

When installed from ClawHub, `<skill-folder>` is the installed skill folder containing this `SKILL.md` file.

For local end-to-end verification, prefer:

```bash
node <skill-folder>/scripts/run-repo-script.mjs test:e2e
```

## Purpose

Help the user organize Chrome bookmarks through natural language.

The host AI should:

1. talk to the user in natural language
2. ask the Chrome executor extension for bookmark context
3. produce a structured action plan
4. preview the plan before any mutation
5. ask for explicit confirmation
6. apply the plan through the Chrome bridge
7. offer undo after a successful apply

## Important Rules

- Never mutate bookmarks on the first planning response
- Always present a preview before apply
- Keep actions limited to the supported schema
- Surface low-confidence or ambiguous cases in warnings
- If Chrome is not connected, distinguish first-run install from an already-installed but sleeping/disconnected extension
- Never claim that bookmarks were changed unless you have verified success through the local bridge
- Never invent folder counts, bookmark counts, or apply results
- Never tell the user to restart Chrome unless a verified tool result requires it
- If bridge verification fails, explicitly say the task is not yet executed
- Do not use direct filesystem reads or writes of Chrome bookmark files as a substitute for execution
- The only supported execution path is the local bridge plus Chrome executor extension
- Do not rely on stale bridge health alone; require a live context check before planning or apply

## Mandatory Preflight

Before planning, validation, apply, or undo, the host AI should run a local preflight.

Preferred command:

```bash
node <skill-folder>/scripts/run-repo-script.mjs bridge:preflight
```

The preflight is responsible for:

1. starting the local bridge server if it is not running
2. refreshing the unpacked Chrome extension when needed
3. verifying that live bookmark context can be fetched

If preflight fails, stop and explain that execution has not happened yet.

Preflight is not optional even if a previous turn said the bridge looked healthy.

Before `POST /validate`, `POST /apply`, or `POST /undo`, prefer the stronger live gate:

```bash
node <skill-folder>/scripts/run-repo-script.mjs bridge:ensure-live
```

If this command succeeds, continue the current operation. If it fails, stop and tell the user no mutation happened.

If this is the user's first run, or if preflight says `needsManualInstall: true`, run:

```bash
node <skill-folder>/scripts/run-repo-script.mjs setup
```

Then tell the user to load the unpacked Chrome extension folder printed by the setup command and reply `好了`.

Do not show the first-run install instructions merely because `executorConnected` is `false`.

Use `/health` and preflight output to choose the recovery message:

- If `/health` has `executor.extensionVersion` or `executor.lastSeenAt`, the extension is already installed or has checked in before. Treat this as a sleeping/disconnected MV3 worker. Run `bridge:ensure-live` or `bridge:preflight`; if recovery still fails, ask the user to reload the existing `Bookmark Organize Executor` card on `chrome://extensions`, not to click `加载已解压的扩展程序` again.
- If `/health` does not have `executor.extensionVersion` and does not have `executor.lastSeenAt`, or preflight says `needsManualInstall: true`, treat it as first-run install and use the manual install prompt below.

Use this user-facing wording only when the extension is not installed:

```text
我需要你完成唯一一步浏览器授权操作：
1. 在已打开的 chrome://extensions 页面开启「开发者模式」
2. 点击「加载已解压的扩展程序」
3. 选择 setup 输出的 Chrome executor extension 文件夹

加载完成后回复「好了」，我会自动继续检查连接并读取书签。
```

Use this user-facing wording when the extension was seen before but is currently disconnected:

```text
Chrome executor 扩展已经安装过，但当前后台连接休眠/断开了。我会先自动唤醒并重连。
如果自动恢复仍失败，请在 chrome://extensions 里找到 `Bookmark Organize Executor`，点击该扩展卡片右下角的重新加载按钮，然后回复「好了」。
我还没有实际修改你的书签。
```

## Mandatory Execution Guardrails

Before claiming any of the following:

- "已整理完成"
- "已创建文件夹"
- "已移动书签"
- "已重命名"
- "已撤销"

you must first verify with the local bridge.

Required bridge checks:

1. Run `node <skill-folder>/scripts/run-repo-script.mjs bridge:ensure-live`
2. Check `http://127.0.0.1:8787/health`
3. Ensure `executorConnected` is `true`
4. Fetch live context from `POST /context`
5. Use bridge endpoints to validate actions, apply actions, or undo actions
6. Report only the results returned by the bridge

If the bridge is unavailable, say that execution has not happened yet.

## Local Bridge

Preferred local bridge:

- HTTP base URL: `http://127.0.0.1:8787`
- Health endpoint: `GET /health`
- Context endpoint: `POST /context`
- Validate endpoint: `POST /validate`
- Apply endpoint: `POST /apply`
- Undo endpoint: `POST /undo`

The Chrome executor extension folder is:

- `<repo-root>/apps/chrome-executor-extension`

The local bridge server can be started from:

- `<repo-root>`

with:

```bash
npm run bridge:server
```

Preferred recovery command:

```bash
npm run bridge:preflight
```

## Supported Actions

- `create_folder`
- `move_bookmark`
- `rename_bookmark`
- `rename_folder`

## Planning Guidance

When generating a plan:

- prefer conservative actions
- avoid renaming when confidence is low
- create folders before moving bookmarks into them
- never emit deletion actions
- never emit move-folder actions
- if doing an E2E test, put `create_folder`, `move_bookmark`, and `rename_bookmark` in one single action list and one single `POST /apply`; do not split the test into multiple apply calls because only the latest apply has an undo token
- for moves into a folder created earlier in the same plan, use `targetPath` with the newly-created folder path instead of waiting for a folder id

When the user asks to organize bookmarks:

1. run preflight
2. if preflight fails, guide setup and stop
3. fetch live bookmark context
4. generate a conservative structured plan
5. preview the plan
6. wait for explicit confirmation
7. run `bridge:ensure-live` again before apply
8. apply only after confirmation
9. summarize actual bridge results

## Confirmation Flow

After previewing a plan, allow the user to respond with short commands such as:

- apply
- apply moves only
- exclude renames
- regenerate more conservatively
- undo last apply

## Setup Guidance

If the Chrome executor extension is unavailable, first check whether it was seen before:

- If `/health` includes `executor.extensionVersion` or `executor.lastSeenAt`, do not run first-run setup unless the user explicitly asks. Run `bridge:ensure-live`; if it still fails, ask the user to reload the existing extension card.
- If `/health` has neither `executor.extensionVersion` nor `executor.lastSeenAt`, guide the user with first-run setup:

1. run `node <skill-folder>/scripts/run-repo-script.mjs setup`
2. tell the user to open the extension page if it did not open automatically
3. tell the user to enable Developer Mode
4. tell the user to choose Load unpacked
5. tell the user to select the extension folder printed by setup
6. ask the user to reply `好了`
7. after the user replies, run `node <skill-folder>/scripts/run-repo-script.mjs bridge:preflight`

Then ask the user to reply with `已安装` or `installed`.

## Verification Commands

Use these commands when you need to verify the environment instead of guessing:

```bash
node <skill-folder>/scripts/run-repo-script.mjs bridge:preflight
node <skill-folder>/scripts/run-repo-script.mjs bridge:ensure-live
node <skill-folder>/scripts/run-repo-script.mjs bridge:smoke
node <skill-folder>/scripts/run-repo-script.mjs test:local
node <skill-folder>/scripts/run-repo-script.mjs test:e2e
```

## Output Contract

The host AI should generate a structured plan with:

- `summary`
- `warnings`
- `actions`

Each action must include an `actionId`.

## Response Style

- Be explicit about whether you are previewing or executing
- Use phrases like `我准备这样整理` before apply
- Use phrases like `我已经通过本地桥接执行完成` only after verified bridge success
- If execution has not happened, say `我还没有实际修改你的书签`
