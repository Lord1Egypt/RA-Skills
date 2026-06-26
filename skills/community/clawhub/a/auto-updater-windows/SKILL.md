---
name: auto-updater
description: "Set up and maintain automatic OpenClaw + skill updates on Windows/macOS/Linux. Use when a user asks for scheduled updates, manual update runs, update health checks, or update summaries. On Windows, enforce native Windows/Git Bash flow and avoid WSL bash paths."
---

# Auto-Updater Skill (Windows-first, cross-platform)

Configure safe recurring updates for OpenClaw and installed skills.

## Core Rules

1. Prefer OpenClaw-native actions and `npx clawhub`.
2. On **Windows**, run updates in **native Windows shell**.
3. On Windows, ensure `bash` resolves to **Git Bash / MSYS**, not `C:\Windows\System32\bash.exe` (WSL launcher).
4. Never include user-specific local paths/usernames in public docs or published skill content.
5. Always output a concise summary: updated, unchanged, failed.

## Windows-Only Guardrails (Important)

- Do **NOT** use WSL for update execution.
- If build steps require `bash`, prepend Git Bash path in PATH for the current shell session.
- Verify active bash:

```powershell
where.exe bash
bash --version
```

Expected on Windows: GNU bash from MSYS/Git, **not** WSL launcher path first.

## Path Placeholders (Use These)

- `<openclaw-repo>`: source repo root (example: `%USERPROFILE%\\dev\\openclaw`)
- `<openclaw-home>`: runtime home (example: `%USERPROFILE%\\.openclaw`)

## Manual Update Flow

### 1) Update OpenClaw (source install)

```powershell
git -C <openclaw-repo> pull --ff-only
pnpm -C <openclaw-repo> install
pnpm -C <openclaw-repo> build
```

### 2) Restart gateway

Use OpenClaw gateway restart tool/action after successful build.

### 3) Update skills

```powershell
npx clawhub update --all --workdir <openclaw-home> --no-input
```

If local edits exist and user confirms overwrite:

```powershell
npx clawhub update <slug> --force --workdir <openclaw-home> --no-input
```

## Successful Windows Command Template (Sanitized)

```powershell
git -C <openclaw-repo> pull --ff-only
pnpm -C <openclaw-repo> install
pnpm -C <openclaw-repo> build
openclaw gateway restart
openclaw --version
```

## Scheduling (Optional)

When user asks for automation, create cron jobs with isolated `agentTurn` runs and summary delivery. Keep schedule conservative (e.g., daily 04:00 local) unless user asks otherwise.

## References

- `references/agent-guide.md`
- `references/summary-examples.md`
