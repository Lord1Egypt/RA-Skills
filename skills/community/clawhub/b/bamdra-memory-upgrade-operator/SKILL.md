---
name: bamdra-memory-upgrade-operator
description: Safely install, uninstall, reinstall, or upgrade the Bamdra OpenClaw memory suite when stale config, existing plugin directories, or partial installs break normal `openclaw plugins install` flows.
---

# Bamdra Memory Upgrade Operator

Use this skill when the user wants to install, uninstall, repair, or upgrade the Bamdra memory suite and a normal `openclaw plugins install @bamdra/bamdra-openclaw-memory` flow is blocked by:

- `plugin already exists`
- `plugin not found` errors from stale `openclaw.json`
- old bundled skills preventing new skill files from being copied
- partial installs where `bamdra-openclaw-memory`, `bamdra-user-bind`, and `bamdra-memory-vector` are out of sync

## Operating Goal

Perform a safe Bamdra suite lifecycle operation without leaving `~/.openclaw/openclaw.json` broken.

The bundled script supports these modes:

- `upgrade`: backup config, clear stale Bamdra references, move old plugin and skill directories aside, then run `openclaw plugins install`
- `install`: run install without first moving old plugin directories
- `uninstall`: backup config, remove Bamdra plugin references from config, and move Bamdra plugin and skill directories into a backup folder

## Default Commands

Upgrade to the latest published suite:

```bash
node ./scripts/upgrade-bamdra-memory.cjs upgrade
```

Install a specific published version:

```bash
node ./scripts/upgrade-bamdra-memory.cjs upgrade --package @bamdra/bamdra-openclaw-memory@0.3.18
```

Uninstall the suite safely:

```bash
node ./scripts/upgrade-bamdra-memory.cjs uninstall
```

## Optional Flags

- `--package <npm-spec>` to install a specific version
- `--openclaw-home <path>` to target a non-default OpenClaw home
- `--restart-gateway` to restart the gateway after a successful install

## Behavior Rules

- prefer the script over manual deletion or ad-hoc `openclaw.json` edits
- mention the backup directory after success
- after install or upgrade, remind the user to restart OpenClaw if `--restart-gateway` was not used
- do not manually edit unrelated plugin config while doing this work
- do not delete backup directories unless the user explicitly asks

## User-Facing Examples

- “升级一下 Bamdra memory 套件”
- “修复 openclaw plugins install 时的 plugin already exists”
- “安全卸载 bamdra-openclaw-memory 套件”
- “重新安装 bamdra 套件，但不要把 openclaw.json 弄坏”
