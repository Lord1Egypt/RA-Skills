## Description:

Set up and use 1Password CLI (op) for installation, desktop app integration, sign-in, and secret read, inject, and run workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangfeng1995](https://clawhub.ai/user/huangfeng1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and operate the 1Password CLI, authorize accounts, and safely consume secrets in shell workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples that print secrets or use --no-masking can expose secret values in terminal output or logs.

Mitigation: Prefer op run or op inject flows that consume secrets without displaying them, and avoid printing secret environment variables.

Risk: Captured terminal panes after secret access can retain sensitive output.

Mitigation: Review captured output before sharing it and avoid capture steps after commands that may reveal secret values.

Risk: Writing private keys or generated configs to normal project files can leave secrets on disk.

Mitigation: Use restrictive file permissions, short-lived files, cleanup steps, and direct secret consumption whenever possible.

## Reference(s):

- [1Password CLI get started](https://developer.1password.com/docs/cli/get-started/)
- [get-started.md](references/get-started.md)
- [cli-examples.md](references/cli-examples.md)
- [ClawHub skill page](https://clawhub.ai/huangfeng1995/skills/1password-old)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance should avoid exposing secret values and should prefer commands that consume secrets without displaying them.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
