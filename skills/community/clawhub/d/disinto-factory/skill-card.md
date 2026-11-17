## Description:

Set up and operate a disinto autonomous code factory. Use when bootstrapping a new factory instance, checking on agents and CI, managing the backlog, or troubleshooting the stack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johba37](https://clawhub.ai/user/johba37)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to bootstrap, operate, monitor, and troubleshoot a disinto autonomous code factory for repositories, agents, CI, backlog management, pull requests, and mirrors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact factory administration can affect credentials, containers, CI workers, repositories, and destructive recovery state.

Mitigation: Run the factory on an isolated host or container, review commands before execution, and avoid privileged or host-network CI workers unless that risk is explicitly accepted.

Risk: Tokens, passwords, or Git credentials may be exposed through command lines, logs, or remotes.

Mitigation: Avoid pasting real passwords into command lines, limit log exposure, and rotate any tokens exposed in logs or Git remotes.

Risk: Running the skill against untrusted factory directories may lead to unsafe administrative operations.

Mitigation: Use trusted factory directories only and keep execution in an isolated environment.

## Reference(s):

- [Disinto homepage](https://disinto.ai)
- [Disinto repository](https://github.com/disinto/disinto)
- [Disinto Factory on ClawHub](https://clawhub.ai/johba37/skills/disinto-factory)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are intended to be reviewed before execution, especially when they affect credentials, containers, CI, repositories, or recovery state.]

## Skill Version(s):

0.2.1 (source: server release evidence, metadata, and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
