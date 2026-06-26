# Agent Implementation Guide (Windows-first, sanitized)

Use this flow when user asks to set up, verify, or run updates.

## 1) Detect environment

- `openclaw --version`
- `npx clawhub --cli-version`
- `npx clawhub list --workdir <openclaw-home> --no-input`

## 2) On Windows, enforce native path

- Ensure updates run in PowerShell/cmd.
- Prepend Git Bash path in PATH before build steps that call `bash`.
- Avoid WSL launcher (`C:\Windows\System32\bash.exe`) as primary bash.

## 3) Update core OpenClaw (manual/source)

```powershell
git -C <openclaw-repo> pull --ff-only
pnpm -C <openclaw-repo> install
pnpm -C <openclaw-repo> build
```

Then restart gateway.

## 4) Update skills

```powershell
npx clawhub update --all --workdir <openclaw-home> --no-input
```

If local modifications block update and user explicitly approves overwrite:

```powershell
npx clawhub update <slug> --force --workdir <openclaw-home> --no-input
```

## 5) Verify and report

- `openclaw --version`
- summarize updated/unchanged/failed
- mention whether Windows-native (non-WSL) path was used

## Privacy/Publishing Rule

Before publishing skill docs, replace host-specific paths and usernames with placeholders (`<openclaw-repo>`, `<openclaw-home>`, `%USERPROFILE%`).
