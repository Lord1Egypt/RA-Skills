## Description:

Runs paid security checks for software, deployments, websites, and text that may contain prompt injection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[montassirbbk-dot](https://clawhub.ai/user/montassirbbk-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security teams use the skill to check dependencies, CI and container configuration, domain security, website quality, and untrusted text before acting on it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's examples use the unpinned `agentcash@latest` package and checks may send submitted content to external services.

Mitigation: Review and pin or verify the CLI version before use; redact or withhold sensitive content unless it is approved for external processing.

## Reference(s):

- [Genexxis Skills](https://skills.genexxis.com)
- [Genexxis MCP service](https://mcp.genexxis.com/mcp)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [Structured check results with findings and suggested fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only checks; each service call has a listed USDC price, and results depend on the selected check.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
