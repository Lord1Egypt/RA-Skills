# Claw World Skill

OpenClaw skill for Claw Civilization Universe.

## Version

`1.1.12`

## Highlights

- Status output now separates NFA assets from account gas via `wallet.address` and `wallet.gasBnb`
- Runtime/save semantics clarified: local CML save is separate from root sync
- Added lightweight `env` command for runtime/network/account checks
- `owned` is now explicitly documented as ownership-summary-only
- `boot` remains the full session initializer for CML/personality/emotion context
- Setup guidance now points users to the standard OpenClaw runtime flow instead of ad-hoc local install or inline scripts
- Update flow docs now warn about local `package-lock.json` conflicts before pulling updates

## Core Files

- `SKILL.md`: agent instructions and gameplay rules
- `claw`: main CLI entrypoint
- `claw-read.js`: read helpers
- `claw-task.js`: task execution helpers
- `claw-lore.js`: lore query helper

## Command Roles

- `claw env`: lightweight runtime/network/account check only
- `claw owned`: lightweight ownership summary only
- `claw boot`: full session initialization with NFA, CML, legacy fallback, and emotion trigger

## CML Save Semantics

- `claw cml-save <tokenId>`: saves the CML locally
- `claw cml-save <tokenId> <pin>`: saves locally and attempts root sync immediately
- Without a PIN, local save can still succeed while root sync remains pending
- Optional remote backup only runs when the local environment supports it

## Safety

- This skill never reads private keys or silently signs transactions.
- State-changing wallet actions require explicit user intent and wallet confirmation.
- Read tools are kept separate from transaction tools.
- The public Hermes adapter marks raw passthrough as developer-only local debugging.

## Update Notes

- The repository now tracks `package-lock.json`
- Before pulling updates manually, make sure you do not have an untracked local `package-lock.json`, or the merge may be blocked
- If you only change docs/help text, avoid regenerating the lockfile unnecessarily
