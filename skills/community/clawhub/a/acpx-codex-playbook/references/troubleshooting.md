# acpx troubleshooting notes

## Symptom: `exec` works poorly for multi-step tasks
Use a persistent session instead of one-shot `exec`.

## Symptom: shell `touch` works but ACP file edit fails
Likely an ACP handler, permission-control, or cwd sandbox boundary issue. Switch to shell/Python file generation.

## Symptom: prompt fails before Codex even starts
Usually shell quoting. Move the prompt into `prompt.txt` and pass `-f prompt.txt`.

## Symptom: `full-access` did not grant true system privilege
Expected. `full-access` is session-level freedom, not guaranteed root or sudo.

## Symptom: package install fails
Try local `.venv` or project-local package installs. Do not assume global install rights or unrestricted network access.

## Symptom: generated binary opens inconsistently
Add explicit validation steps before copying the artifact to its final location.
