---
name: aoineco-starter-pack
description: Install a curated starter pack of @edmonddantesj ClawHub skills (security, stability, memory, ops) in one command via the ClawHub CLI. Use when a user asks to install all/most AOI/Aoineco skills at once, wants a beginner-friendly recommended bundle, or needs minimal/core/full install options.
---

# AOI / Aoineco Starter Pack

Install a curated bundle of skills from the ClawHub profile `edmonddantesj`.

## What this does

- Installs multiple skills via `clawhub install ...` in one run
- Offers 3 pack modes:
  - `minimal`: 2 essentials
  - `core`: recommended for beginners
  - `full`: all published utilities

Skill list reference: `references/skill_list.md`

## Prereqs

1) Have `clawhub` CLI available
2) Be logged in:

```bash
clawhub login
clawhub whoami
```

## Install (fast path)

1) Install this pack:

```bash
clawhub install aoineco-starter-pack
```

2) Run the recommended bundle (`core`):

```bash
bash skills/aoineco-starter-pack/scripts/run.sh core
```

Other modes:

```bash
bash skills/aoineco-starter-pack/scripts/run.sh minimal
bash skills/aoineco-starter-pack/scripts/run.sh full
```

## Windows (PowerShell)

```powershell
clawhub install aoineco-starter-pack
powershell -ExecutionPolicy Bypass -File .\skills\aoineco-starter-pack\scripts\install_pack.ps1 core
```

## Notes

- This is an installer pack. It does not enable/auto-configure risky automations.
- If you need to update later:

```bash
clawhub update
```
