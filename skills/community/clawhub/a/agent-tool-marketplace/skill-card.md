## Description:

Agent Tool Marketplace catalog for AgentPMT - list available paid tools, fetch tool schemas, invoke any tool with a signed request, and consume responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover AgentPMT marketplace tools, inspect action schemas and pricing, and invoke selected third-party capabilities through wallet-signed requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad paid third-party tool invocation with wallet-signed requests.

Mitigation: Require explicit approval for the specific product and action, review pricing and provider identity, set a spending limit, and avoid sending secrets, credentials, private files, or unnecessary personal data in tool parameters.

## Reference(s):

- [AgentPMT External Agent API](https://www.agentpmt.com/external-agent-api)
- [AgentPMT Marketplace](https://www.agentpmt.com)
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/agent-tool-marketplace)

## Skill Output:

**Output Type(s):** [guidance, code, API calls, configuration]

**Output Format:** [Markdown with Python and text code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint, signing, request construction, catalog workflow, and error-handling guidance.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
