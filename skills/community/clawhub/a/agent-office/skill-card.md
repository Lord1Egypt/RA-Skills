## Description:

Agent Office creates and manages local AI office workers as independent HTTP workers, supporting openclaw, hermes, deerflow, cli, external, and stub engines for office automation and multi-agent team workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jast-hub](https://clawhub.ai/user/jast-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create, manage, health-check, task, and remove local AI worker teams. It is suited for local office automation workflows that need individual worker identities, ports, state, logs, presets, and optional integration with local agent CLIs or an existing HTTP worker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local HTTP workers can expose powerful local agent actions.

Mitigation: Run workers only in trusted local environments and stop or remove workers when they are no longer needed.

Risk: Local CLI, workspace, and DeerFlow task execution can access or modify sensitive files.

Mitigation: Use a dedicated low-sensitivity workspace and review worker roles, CLI commands, and DeerFlow runtime source before running tasks.

Risk: External upstream workers and optional shared memory can carry untrusted context into task execution.

Mitigation: Use external upstream URLs only when fully trusted and keep MEMORY_CLI disabled for sensitive work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jast-hub/skills/agent-office)
- [Publisher Profile](https://clawhub.ai/user/jast-hub)
- [ClawHub Homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and generated local worker files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start persistent local HTTP worker processes and write worker state, logs, prompts, and runtime configuration under the user's local office directories.]

## Skill Version(s):

1.5.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
