## Description:

Create custom http.Agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose proxy-agent subclasses or implement custom Node.js http.Agent connection logic with agent-base for HTTP, HTTPS, SOCKS, PAC, and custom socket routing scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proxy or custom connection code can route application traffic to unintended destinations if PAC, SOCKS, or proxy settings are wrong.

Mitigation: Review generated proxy URLs, PAC rules, SOCKS settings, and connect() implementations before using them in production.

## Reference(s):

- [Proxy Details and Subclass Selection](references/proxy-details.md)
- [ClawHub Skill Page](https://clawhub.ai/openlark/skills/agent-base)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript/JavaScript code blocks and npm install commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
