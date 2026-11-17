## Description:

Helps users create OpenClaw agents by collecting requirements in a conversation and generating standardized agent configuration files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squallfire](https://clawhub.ai/user/squallfire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create, validate, and list reusable OpenClaw agent configurations with standard identity, workflow, memory, and workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe agent names or workspace paths can write files outside the intended OpenClaw workspace area or overwrite existing agent instructions.

Mitigation: Use only trusted, simple kebab-case agent names, avoid custom workspace paths outside the intended area, and review the target paths before execution.

Risk: Generated agent files persist and can influence future agent behavior.

Mitigation: Inspect generated configuration files before using the new agent and validate the configuration after creation.

Risk: Running the scripts with elevated privileges increases the impact of unintended file writes.

Mitigation: Run the skill as a normal user rather than with administrator privileges.

## Reference(s):

- [Agent Maker ClawHub release page](https://clawhub.ai/squallfire/skills/agent-maker)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated Markdown configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent OpenClaw agent and workspace files under user-selected local paths.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
