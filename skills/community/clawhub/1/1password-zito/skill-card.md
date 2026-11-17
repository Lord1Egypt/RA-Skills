## Description:

Set up and use 1Password CLI (op) for installation, desktop app integration, sign-in, and reading, injecting, or running secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miguelguerra200022-sudo](https://clawhub.ai/user/miguelguerra200022-sudo)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure and use the 1Password CLI safely inside agent workflows, including app integration, account sign-in, vault checks, secret reads, command execution with injected secrets, and configuration templating.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples and workflows can expose secrets in terminal output, captured panes, or local files.

Mitigation: Prefer masked or non-printing flows, avoid copying examples that print secrets or disable masking, and apply strict permissions and cleanup when files are intentionally written.

Risk: Running 1Password CLI commands outside the intended authenticated terminal session can cause repeated prompts or failed secret access.

Mitigation: Use a dedicated tmux session for op commands, verify access with op whoami before reading secrets, and re-run op signin in that session when an account is not signed in.

## Reference(s):

- [1Password CLI get-started](https://developer.1password.com/docs/cli/get-started/)
- [Local get-started summary](references/get-started.md)
- [Local CLI examples](references/cli-examples.md)
- [ClawHub skill page](https://clawhub.ai/miguelguerra200022-sudo/skills/1password-zito)
- [Publisher profile](https://clawhub.ai/user/miguelguerra200022-sudo)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance should avoid exposing secret values in logs, chat, terminal captures, or files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
