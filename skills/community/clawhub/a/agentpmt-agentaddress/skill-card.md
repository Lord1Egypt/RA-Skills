## Description:

This deprecated AgentPMT index skill routes agents to the current canonical AgentPMT ClawHub skills for setup, x402/no-account, overview, and current tool workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[firef1ie](https://clawhub.ai/user/firef1ie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as a routing index when choosing or installing current AgentPMT ClawHub skills. It helps route users to AgentPMT setup, no-account x402, overview, account MCP/REST, and image generation skill pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install commands resolve by current slug rather than immutable digest, so users could install a different package or version than intended if listings change.

Mitigation: Before installing referenced AgentPMT skills, confirm the ClawHub page starts with the listed AgentPMT publisher URL and that the resolved package and version match the intended skill.

Risk: The index is time-sensitive and may point to outdated current skills after its listed update date.

Mitigation: Check the AgentPMT ClawHub publisher page before relying on the index when the current date is more than seven days after 2026-06-09.

## Reference(s):

- [Deprecated AgentPMT AgentAddress + Paid Marketplace ClawHub page](https://clawhub.ai/firef1ie/skills/agentpmt-agentaddress)
- [AgentPMT ClawHub publisher page](https://clawhub.ai/user/agentpmt)
- [AgentPMT no-account AgentAddress/x402 setup](https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402)
- [What Is AgentPMT](https://clawhub.ai/agentpmt/what-is-agentpmt)
- [AgentPMT account MCP/REST API setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [Image Generation Agent](https://clawhub.ai/agentpmt/image-generation-agent)
- [AgentPMT website](https://www.agentpmt.com)
- [AgentPMT marketplace](https://www.agentpmt.com/marketplace)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with ClawHub links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No credentials required; output is an index of current AgentPMT skill choices and installation commands.]

## Skill Version(s):

1.1.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
