---
name: AirDrop
slug: airdrop
version: 1.0.0
homepage: https://clawic.com/skills/airdrop
description: Send local files to nearby Apple devices through AirDrop with macOS guardrails, staging checks, and automation-friendly workflows.
changelog: Initial release with direct AirDrop launch, shortcut fallback, and safer file-sharing guardrails for nearby Apple devices.
metadata: {"clawdbot":{"emoji":"A","requires":{"bins":[]},"os":["darwin"],"configPaths":["~/airdrop/"]}}
---

## When to Use

User wants the agent to send a local file, export, screenshot, log bundle, or review artifact to a nearby Apple device with AirDrop.
Agent handles file staging, confirmation, local handoff, and mode selection between direct AppKit launch and Shortcut fallback.

## Requirements

- macOS with AirDrop enabled in Finder.
- Nearby Apple recipient available and visible to the current Mac.
- Direct mode uses `xcrun swift` or `swift` to run `airdrop-send.swift`.
- Shortcut mode uses the built-in `shortcuts` CLI and a user-owned shortcut that accepts file input.

## Architecture

Memory lives in `~/airdrop/`. If `~/airdrop/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/airdrop/
|- memory.md          # Activation and confirmation preferences
`- staging/           # Optional user-approved temp exports before sharing
```

## Quick Reference

| Topic | File |
|-------|------|
| First-run behavior and activation | `setup.md` |
| Memory structure | `memory-template.md` |
| Direct CLI wrapper | `airdrop-send.sh` |
| AppKit AirDrop launcher | `airdrop-send.swift` |
| Common execution patterns | `workflow-recipes.md` |
| Recovery and diagnostics | `troubleshooting.md` |

## Core Rules

### 1. Resolve Exact Files Before Sharing
- Work only with explicit local file paths.
- For generated text or mixed output, stage to a user-approved file first, then share that file.
- Refuse vague requests like "send the project" until the exact payload is listed.

### 2. Use the Smallest Safe Payload
- Prefer the exact artifact the recipient needs: one PDF, one ZIP, one screenshot set, one installer.
- When the source is a directory, curate or archive the approved subset before launch.
- Treat hidden files, secrets, and unrelated workspace state as excluded by default.

### 3. Keep Recipient Choice Interactive
- AirDrop recipient selection stays in the macOS share UI.
- Do not claim silent recipient targeting, background delivery, or machine-verifiable recipient identity.
- If the user wants zero-click routing, use Shortcut mode only when they already built that behavior locally.

### 4. Pick the Right Execution Mode
- Default to `airdrop-send.sh` for direct local handoff because it launches the native AirDrop sharing service without inventing unsupported CLI verbs.
- Use Shortcut mode when the user already has a Shortcut that renames, compresses, or routes files before AirDrop.
- If `swift` is unavailable, fall back to the user's Shortcut flow or stop with a concrete requirement message.

### 5. Confirm Sensitive Shares
- Before launching AirDrop for logs, source bundles, contracts, exports, or anything private, list the exact files and ask for confirmation.
- If the user says "only the final artifact", strip extras before sharing.
- Never include credential files, env files, database dumps, or hidden config unless the user explicitly requests them.

### 6. Report Handoff Honestly
- Success means the AirDrop chooser launched with the requested files.
- Do not say the transfer completed unless the user confirms it on-device.
- If launch succeeds but the device does not appear, route to `troubleshooting.md` instead of retrying blindly.

## Common Traps

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Treating AirDrop like `scp` | No stable official recipient CLI targeting | Launch native chooser and keep recipient selection interactive |
| Sending raw text directly | AirDrop works on shareable items, not vague chat content | Write the text to a file, then share that file |
| Sharing whole folders by reflex | Leaks unrelated files and slows discovery | Zip or curate the exact approved subset first |
| Claiming delivery success too early | Launching the chooser is not transfer confirmation | Report "handoff started" until the user confirms receipt |
| Retrying with the same bad payload | Hidden files or unsupported items keep failing | Reduce to one known-good file and retry once |

## Data Storage

This skill can operate with no persistent local state.
If the user wants repeatable behavior, store only activation, confirmation, and staging preferences in `~/airdrop/memory.md`.
Create `~/airdrop/staging/` only with user approval when temporary share files are useful.

## Security & Privacy

**Data that stays local:**
- Skill memory and optional staging files in `~/airdrop/`
- The source files until the user chooses a nearby AirDrop recipient

**Data that may leave your machine:**
- Only the specific files the user approved for AirDrop
- Discovery and transfer metadata handled by macOS AirDrop services with nearby Apple devices

**This skill does NOT:**
- Upload files to undeclared cloud services
- Select recipients silently in the background
- Confirm transfer completion without user-visible evidence
- Read or share files outside the approved payload list

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `macos` - General macOS command workflows, permissions checks, and native app automation patterns.
- `applescript` - Finder and app automation when AirDrop workflows need UI scripting around local files.
- `files` - File selection, packaging, renaming, and cleanup before sharing the final payload.
- `photos` - Exporting and converting image assets before sending them to another Apple device.

## Feedback

- If useful: `clawhub star airdrop`
- Stay updated: `clawhub sync`
