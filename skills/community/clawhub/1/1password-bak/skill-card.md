## Description:

Set up and use 1Password CLI (op), including installation, desktop app integration, sign-in, and secret read, inject, and run workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaozewen0519](https://clawhub.ai/user/zhaozewen0519)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and operate the 1Password CLI safely during agent-assisted workflows that need authenticated secret access. It helps agents propose setup checks, sign-in steps, tmux-based command execution, and safer alternatives to writing secrets to disk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable examples can expose resolved secrets in terminal output, especially commands that disable masking or print environment variables.

Mitigation: Do not run no-masking or secret-printing examples with real secrets; prefer masked flows and avoid sharing terminal captures from secret sessions.

Risk: Some examples write secret material such as keys or rendered configuration files to disk.

Mitigation: Prefer op run or op inject without persistent files; when files are necessary, use restrictive permissions and exclude them from source control.

Risk: tmux pane captures or terminal logs from authenticated sessions can retain sensitive command output.

Mitigation: Keep 1Password operations in a dedicated session and avoid copying, storing, or sharing captured output that may contain secrets.

## Reference(s):

- [1Password CLI get-started documentation](https://developer.1password.com/docs/cli/get-started/)
- [ClawHub skill page](https://clawhub.ai/zhaozewen0519/skills/1password-bak)
- [get-started.md](references/get-started.md)
- [cli-examples.md](references/cli-examples.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and concise procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the 1Password CLI (op), a 1Password account, and tmux for the documented command workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
