# Publish To ClawHub

This directory is prepared as a web-upload-friendly public release of `cli-agent-bridge`.

## Why this directory is publishable

This package keeps only text files that explain the skill and its local companion model.

It intentionally excludes executable runtime files such as PowerShell and batch launchers so the published package does not promise behavior that the upload directory cannot provide by itself.

## Files kept in this directory

- `SKILL.md`
- `README.md`
- `PUBLISH-TO-CLAWHUB.md`
- `references/auth-model.md`
- `references/fs-operations.md`
- `references/provider-commands.md`

## Files that should not be uploaded

Keep these in the local full package, not in the public web upload directory:

- `*.ps1`
- `*.bat`
- local install scripts
- local verification scripts
- local test notes
- historical reports
- temporary test directories

## Suggested publish form values

- slug: `cli-agent-bridge`
- display name: `CLI Agent Bridge (Windows Companion)`
- version: `0.3.0`
- tags: `windows`, `openclaw`, `local-cli`, `powershell`, `companion`
- changelog: `First public text release for ClawHub. Documents the local Windows companion deployment and its capability boundaries without bundling executors.`

## Why `0.3.0` instead of `1.0.0`

`0.3.0` is the recommended public version because:

- the public release shape is now clear
- the uploaded package is documentation-first, not a self-contained runtime
- real `claude` availability still depends on each user's local Claude CLI authentication and quota

## Provider wording guidance

Public docs should state:

- this published directory does not execute providers by itself
- the local full package is intended to support `gemini`, `codex`, and `claude`
- `gemini` and `codex` were validated in the local full package
- `claude` depends on the user's local authentication and quota state

## Publish checklist

- only text files remain in the upload directory
- no `.ps1` files remain
- no `.bat` files remain
- `SKILL.md`, `README.md`, and this file use the same capability boundary
- no local absolute paths remain
- no account IDs, tokens, or secrets remain
- the package does not claim that executors are bundled
- the package does not claim open-ended filesystem access

## Recommended upload directory

Upload this directory:

```text
<repo-root>/clawhub/cli-agent-bridge
```
