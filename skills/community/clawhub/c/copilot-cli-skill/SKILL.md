---
name: copilot-cli-operator
description: Run GitHub Copilot CLI from OpenClaw for coding tasks in a target project directory. Use when the user asks OpenClaw to use Copilot for implementation, debugging, refactoring, review, or scripted coding workflows.
---

# GitHub Copilot CLI Operator

Use this skill to reliably call Copilot CLI from OpenClaw.

## Core rules

1. Verify Copilot CLI exists (`copilot --version`) before first task.
2. Always run Copilot through OpenClaw `exec` with `pty:true`.
3. Always set explicit `workdir` to the target repository.
4. For long tasks, use `background:true` and track via `process`.
5. Report clear milestones: started, waiting-input, finished/failed.

## Execution patterns

### One-shot coding task

Use:
- `exec.command`: `copilot -p "<task>" --allow-all-tools`
- `exec.pty`: `true`
- `exec.workdir`: `<repo path>`

### Scoped tool approval

Use `--allow-tool` and `--deny-tool` to control what Copilot can do:
- `exec.command`: `copilot -p "<task>" --allow-tool 'shell(git)' --allow-tool 'write'`
- `exec.pty`: `true`
- `exec.workdir`: `<repo path>`

To block dangerous operations:
- `copilot -p "<task>" --allow-all-tools --deny-tool 'shell(rm)' --deny-tool 'shell(git push)'`

### Interactive session

Use:
- `exec.command`: `copilot`
- `exec.pty`: `true`
- `exec.workdir`: `<repo path>`

### Long-running background task

1. Start with `exec(background:true, pty:true, workdir, command:"copilot -p '...' --allow-all-tools")`
2. Record returned `sessionId`.
3. Poll with `process action:poll`.
4. Read output with `process action:log`.
5. If Copilot asks for input, use `process action:submit`.

### Resume a previous session

Use:
- `exec.command`: `copilot --resume` (select from list)
- `exec.command`: `copilot --continue` (resume most recent)

## Recommended prompts

- "Implement <feature> with tests, run tests, and summarize changed files."
- "Find root cause for failing CI in this repo and propose minimal fix."
- "Review current branch diff and list high-risk issues first."
- "Work on issue https://github.com/owner/repo/issues/123 in a new branch."
- "Create a PR that updates the README with the latest API usage."

## Guardrails

- Do not claim files were changed unless logs show completion.
- If `copilot` is missing or auth fails, return exact remediation steps.
- Keep OpenClaw tool config (`pty/workdir/background`) separate from CLI args.
- Prefer `--allow-tool` with specific scopes over `--allow-all-tools` for safety.
- Use `--deny-tool 'shell(rm)'` when working in directories with important data.

## References

- `references/copilot-doc-summary.md`
- `references/copilot-usage-recipes.md`
- `scripts/run-copilot-example.sh`
