## Description:

Send and receive email as an agent via the agenticboxes HTTP API, using one API key without IMAP or SMTP setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenticbrian](https://clawhub.ai/user/agenticbrian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to provision and operate an email address for sending messages, receiving replies, handling sign-up confirmations, managing boxes, and interacting with AgenticBoxes support or feature request endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may gain broad email, DNS, billing, webhook, and account-administration authority through the third-party service.

Mitigation: Require explicit user approval before sending or reading sensitive mail, registering accounts, changing DNS, topping up credit, deleting boxes, configuring webhooks, or sharing support context.

Risk: Newly fetched platform documentation can change the agent's operating instructions.

Mitigation: Review updated API documentation before relying on new or changed endpoints for sensitive workflows.

Risk: API keys and webhook signing secrets are sensitive credentials.

Mitigation: Store credentials in environment variables or a secret manager, avoid exposing them in logs or messages, and rotate webhook secrets when access may have been disclosed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agenticbrian/skills/agenticboxes-email)
- [AgenticBoxes agent manifest](https://api.agenticboxes.email/.well-known/agentic.json)
- [AgenticBoxes OpenAPI specification](https://www.agenticboxes.email/openapi.yaml)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce authenticated HTTP requests and operational instructions for email, DNS, billing, webhook, support, and feature-request workflows.]

## Skill Version(s):

1.4.5 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
