## Description:

Pragmatic coding standards for concise, direct, maintainable agent-generated code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gabrielsubtil](https://clawhub.ai/user/gabrielsubtil)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to apply pragmatic clean-code standards, keep changes focused, and validate work before completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may pressure agents to run local validation scripts outside the reviewed package.

Mitigation: Treat the listed .agent/skills Python commands as untrusted unless the scripts are separately verified and appropriate for the current task.

Risk: The skill imposes mandatory cross-agent validation workflows that may not match a project's own process.

Mitigation: Review the skill before deployment and prefer user-specified or project-specific validation requirements when they conflict.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, code, shell commands, markdown]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May influence validation workflow and coding-style decisions during agent tasks.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter declares 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
