## Description:

Guides agents through batch creation of OpenClaw agents and workspace templates, including scope confirmation, agent-by-agent drafting, approved file writes, and summary reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zcxggmu](https://clawhub.ai/user/zcxggmu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create one or more agent workspaces, collect configuration preferences, draft core agent files, and optionally run OpenClaw CLI setup commands after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated AGENTS, SOUL, IDENTITY, BOOTSTRAP, USER, and STYLE files may encode incorrect agent behavior if accepted without review.

Mitigation: Review every generated workspace file before confirming writes.

Risk: Workspace paths or OpenClaw CLI commands can behave unexpectedly when paths contain spaces or shell-special characters.

Mitigation: Use trusted workspace paths and structured arguments or proper shell quoting for OpenClaw CLI commands.

Risk: The helper script can overwrite existing workspace files when run with --force.

Mitigation: Use --force only when replacing existing files is intentional.

## Reference(s):

- [Question Bank](artifact/references/question-bank.md)
- [Create Agents Wizard on ClawHub](https://clawhub.ai/zcxggmu/skills/create-agents-wizard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown drafts with inline shell commands, file paths, and summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-confirmed workspace files and may suggest optional OpenClaw CLI commands.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
