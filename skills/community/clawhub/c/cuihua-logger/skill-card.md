## Description:

AI-powered logging assistant that generates production-ready structured logs with appropriate levels, context, and formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supermario11](https://clawhub.ai/user/supermario11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess JavaScript and TypeScript logging coverage and generate structured logging snippets for application functions, API endpoints, errors, and performance timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated logging can write private data such as raw arguments, request bodies, headers, tokens, cookies, passwords, full email addresses, or stack traces into application logs.

Mitigation: Review generated logging before use, especially in authentication, payment, user-profile, request-handling, and API code; prefer allowlisted metadata, redaction, retention limits, and access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supermario11/skills/cuihua-logger)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown text with JavaScript code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include logging coverage reports and generated structured logging snippets.]

## Skill Version(s):

1.0.0 (source: server release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
