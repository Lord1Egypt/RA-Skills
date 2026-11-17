## Description:

This skill provides coding style standards, security guidance, and accessibility checks for code generation, programming assistance, debugging, testing, and development workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to generate code, review code quality, check style, security, and accessibility expectations, debug tests, and prepare development or deployment workflows. It is not intended for vague requests without a clear technical stack or for decisions that require complex human judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad authority to read and write files and run local commands.

Mitigation: Use it only in repositories where agent file access and local command execution are acceptable, and review proposed changes before applying them.

Risk: The security summary flags broad command, file-writing, and external-service authority without enough scoping for routine use.

Mitigation: Avoid use with secrets, proprietary code, production credentials, or outbound API access unless explicit approval and data-handling controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-quality-2)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown or JSON with code, issue lists, fix suggestions, command guidance, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository file edits, test results, and remediation recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
