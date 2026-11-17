## Description:

Check the health and status of popular AI APIs and services, including OpenAI, Anthropic, Pollinations, OpenRouter, Gemini, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudcompile](https://clawhub.ai/user/cloudcompile)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to check whether common AI API endpoints appear reachable while troubleshooting service availability or connectivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Status checks may be unreliable on networks where HTTPS traffic can be intercepted because the bundled script disables certificate verification.

Mitigation: Treat results as advisory, avoid relying on them over untrusted or intercepted networks, and restore normal TLS certificate verification before using the results for operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cloudcompile/skills/api-health-check)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or terminal text with status labels, HTTP status codes, and response times]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are advisory point-in-time checks of selected API endpoints.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
