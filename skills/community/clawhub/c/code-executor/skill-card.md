## Description:

Runs Python, JavaScript, Bash, TypeScript, and SQL code dynamically so an agent can generate, execute, and return results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miguelguerra200022-sudo](https://clawhub.ai/user/miguelguerra200022-sudo)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate and run short scripts, shell commands, calculations, data transformations, dependency installs, and one-off automation from prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run arbitrary code and shell commands, including local scripts and package installs.

Mitigation: Use it only in a disposable sandbox with minimal filesystem access, network access disabled by default, strict timeouts, controlled dependency sources, and confirmation before execution.

Risk: The artifact documents safety controls but does not implement those controls in the skill file itself.

Mitigation: Verify the host agent enforces sandboxing, timeouts, network blocks, dependency controls, and read-only filesystem policy before enabling the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/miguelguerra200022-sudo/skills/code-executor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated code, command output summaries, dependency installation steps, and execution guidance.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
