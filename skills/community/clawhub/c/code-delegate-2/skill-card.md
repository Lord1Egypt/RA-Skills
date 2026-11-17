## Description:

代码委派助手 helps agents delegate programming tasks to a local AI coding CLI, with environment checks, asynchronous execution, session continuation, and independent test validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to hand off code generation, debugging, refactoring, testing, and deployment tasks to a local coding CLI while keeping the main agent responsive. It is intended for technical workflows with clear project context and explicit task descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated local coding work may edit files with permission bypass while write protection is only optional.

Mitigation: Use an external sandbox or write guard before delegation, review the exact command and target directory, and avoid repositories containing secrets or sensitive data unless containment is enforced.

Risk: Generated code or remediation advice can be incorrect, incomplete, or misaligned with project constraints.

Mitigation: Review delegated changes, run independent tests in a fresh session, and require concise reports of commands run, outputs, failures, and changed files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-delegate-2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with shell command examples and structured status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include delegated session IDs, polling instructions, file-change summaries, test results, and risk warnings.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
