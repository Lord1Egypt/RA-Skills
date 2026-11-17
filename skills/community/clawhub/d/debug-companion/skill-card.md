## Description:

Debug Companion analyzes pasted error messages and tracebacks, identifies likely causes, and returns repair suggestions for common programming errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ysy88092144](https://clawhub.ai/user/ysy88092144)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to interpret runtime errors, compiler errors, and tracebacks across common programming languages. It helps extract error details, explain likely root causes, and propose actionable fixes or reference material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill claims automatic redaction, but the security evidence says the inspected implementation retains and displays raw traceback and context data that may contain secrets.

Mitigation: Manually redact production tracebacks, secrets, tokens, passwords, connection strings, private URLs, and proprietary code before using the skill.

Risk: Generated debugging guidance or code changes may be incomplete or incorrect for project-specific logic.

Mitigation: Review proposed fixes and test them in a controlled environment before applying them to production code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ysy88092144/skills/debug-companion)
- [ClawHub publisher profile](https://clawhub.ai/user/ysy88092144)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with structured sections and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external reference links and code snippets; users should redact sensitive traceback or code context before sharing.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata, script header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
