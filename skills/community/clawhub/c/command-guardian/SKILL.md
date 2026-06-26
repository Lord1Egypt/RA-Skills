---
name: command-guardian
description: Preflight safety guard for shell and infrastructure commands. Use before running commands that delete, overwrite, move, deploy, rewrite git history, change permissions, use shell wrappers like bash -c or powershell -Command, chain multiple commands with &&/||/; or may expose inline secrets. Especially for shell, git, docker, kubectl, terraform, npm, curl, wget, rsync, chmod, chown, and PowerShell file operations.
metadata: {"openclaw":{"requires":{"anyBins":["python","python3","py"]}}}
---

# Command Guardian

Use this skill before executing commands with non-trivial side effects.

It classifies risk, checks targets against workspace boundaries, looks for obvious secret leakage, inspects compound and nested shell commands, adds lightweight git context when available, and produces rollback guidance before the command is run.

## Workflow

1. Normalize the command, working directory, and allowed roots.
2. Run the preflight script with one of these input modes:

```bash
python {baseDir}/scripts/preflight.py --command "<raw command>" --cwd "<working dir>" --allowed-root "<workspace root>" --format json
```

```bash
python {baseDir}/scripts/preflight.py --command-file command.txt --cwd "<working dir>" --allowed-root "<workspace root>" --format json
```

```bash
echo '<raw command>' | python {baseDir}/scripts/preflight.py --cwd "<working dir>" --allowed-root "<workspace root>" --format json
```

3. Read the report and respond by risk level:

- `low`: proceed if the command still matches user intent
- `medium`: explain the risk briefly and tighten the command if a safer rewrite is obvious
- `high`: do not execute blindly; show why, provide a safer version, and require explicit confirmation
- `critical`: stop automatic execution; narrow scope, strip secrets, or stage the operation before retrying

4. Always surface:

- `Risk:`
- `Why:`
- `Safer rewrite:`
- `Rollback:`
- `Need approval: yes/no`

If `safer_commands` are available, show them before execution.
If the user only asks for analysis, stop at the review.
If the user asks to proceed, use the report to tighten the command before execution.

## Default Policy

- Treat inline secrets as at least `high` risk. If the command embeds active credentials, treat it as `critical`.
- Treat destructive operations on broad targets such as `.`, `..`, `/`, drive roots, wildcard-only paths, or repo roots as `critical`.
- Treat `git push --force`, `git reset --hard`, `docker system prune`, `kubectl delete`, and `terraform apply/destroy` as requiring rollback guidance before execution.
- Treat `curl | sh` and similar download-and-execute patterns as `critical` unless the script is pinned, inspected, and verified.
- Treat compound commands by the highest-risk segment, not by the first visible token.
- If the current git branch is `main` or `master`, raise the review bar for destructive git commands.

## Scripts

Use these scripts directly:

- `scripts/preflight.py`
  Main entrypoint. Supports `--command`, `--command-file`, or stdin. Runs command classification, path checks, secret detection, context checks, rollback hint generation, and safer-action suggestions.

- `scripts/classify_command.py`
  Labels command risk and categories such as `write`, `destructive`, `privileged`, and `production-impacting`.

- `scripts/path_guard.py`
  Resolves candidate paths relative to `--cwd`, checks whether they escape allowed roots, and flags broad deletion targets.

- `scripts/secret_guard.py`
  Detects obvious inline secrets such as bearer tokens, JWTs, AWS keys, GitHub PATs, and suspicious key/value pairs.

- `scripts/rollback_hints.py`
  Produces rollback and pre-change backup guidance for git, kubectl, terraform, docker, npm, and destructive file operations.

## References

Read these only when needed:

- `references/risk-rules.md`
  Risk rubric, approval thresholds, and examples of broad targets and secret exposure.

- `references/tool-patterns.md`
  Tool-specific review notes for git, docker, kubectl, terraform, curl/wget, npm/pip/cargo, and file operations.

## Response Template

Use this shape in your answer:

```text
Risk: high
Why:
- rewrites shared git history
- no rollback checkpoint was created

Safer commands:
- git branch backup/pre-force-push-main HEAD
- git push --force-with-lease origin main

Safer rewrite:
- create a backup branch first
- use force-with-lease instead of plain force

Rollback:
- git reflog
- restore backup branch if remote history breaks collaborators

Need approval: yes
```
