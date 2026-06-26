# acpx troubleshooting notes

## Symptom: `exec` works poorly for multi-step tasks
Use a persistent session instead of one-shot `exec`.

## Symptom: shell `touch` works but ACP file edit fails
Likely an ACP handler, permission-control, or cwd sandbox boundary issue. Switch to shell/Python file generation.

## Symptom: prompt fails before the agent meaningfully starts
Usually shell quoting or CLI shape mismatch. Move the prompt into `prompt.txt` and pass `-f prompt.txt`. Also verify whether the chosen agent subcommand actually supports the flags you are using.

## Symptom: one agent accepts a flag that another rejects
Do not assume all `acpx <agent>` subcommands share the same option surface.

Workspace example:
- top-level `acpx` supports `--cwd`
- `acpx claude` may reject `--cwd` on the agent subcommand

If the command fails before real tool use begins, check CLI shape before blaming the model or provider.

## Symptom: `full-access` did not grant true system privilege
Expected. `full-access` is session-level freedom, not guaranteed root or sudo.

## Symptom: package install fails
Try local `.venv` or project-local package installs. Do not assume global install rights or unrestricted network access.

## Symptom: generated binary opens inconsistently
Add explicit validation steps before copying the artifact to its final location.

## Symptom: the agent answers text but does not create files
Treat this as a workflow/reliability issue, not proof that the prompt is bad. First rule out provider compatibility, quota problems, acpx permission policy, and command-shape mistakes.

Fast check order:
- confirm plugin-local `acpx` binary exists
- inspect `~/.acpx/config.json`
- if config is `defaultPermissions: "approve-reads"` + `nonInteractivePermissions: "fail"`, expect non-interactive writes to abort
- retry with a minimal fixed-text test, then a minimal file-write test

If the task is a real deliverable and the chosen agent still fails after those checks, switch to the currently verified delivery agent instead of repeatedly retrying the broken path.

## Symptom: Claude relay returns `403`, `401 quota exhausted`, or `500 invalid claude code request`
Treat the provider as not production-ready for Claude Code / `claude-agent-acp` in the current environment until it passes the minimal sequence in `provider-compat.md` again.

## Symptom: acpx config `nonInteractivePermissions` value seems ignored
Check the actual allowed values for the installed acpx version. In this environment, values like `allow` are invalid; use a supported value and rely on explicit smoke tests for deliverable work.
