## Description:

Use when an agent or developer wants to reduce Claude API costs, route requests through a Claude Max or Pro subscription instead of per-token billing, or set up claude-max-api-proxy for OpenClaw or any OpenAI-compatible client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[error403agent](https://clawhub.ai/user/error403agent)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to install and configure a local Claude subscription-backed proxy for OpenClaw or other OpenAI-compatible clients. It is intended for users who already have a Claude Max or Pro subscription and need setup guidance, client configuration, and operational checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The proxy creates an unauthenticated local endpoint backed by the user's Claude subscription.

Mitigation: Keep the proxy bound to localhost, avoid shared machines, never expose port 3456 publicly, and treat access to localhost:3456 as access to the subscription.

Risk: The skill installs and runs a third-party package that forwards requests through the authenticated Claude CLI session.

Mitigation: Review the package source before installation and pin a known package version where possible.

Risk: Enabling the optional persistent service can keep the proxy available across sessions.

Mitigation: Run the proxy manually when needed unless persistence is required, and review the user service configuration before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/error403agent/skills/claude-max-proxy-setup)
- [claude-max-api-proxy source](https://github.com/atalovesyou/claude-max-api-proxy)
- [Publisher profile](https://clawhub.ai/user/error403agent)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local setup checks, client configuration examples, service setup commands, verification commands, model ID references, and troubleshooting guidance.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
