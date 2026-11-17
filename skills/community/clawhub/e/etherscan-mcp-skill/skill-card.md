## Description:

Use Etherscan MCP through UXC for address balance checks, token holder analysis, transaction inspection, and contract lookup tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to run Etherscan MCP workflows for onchain address investigation, token holder analysis, transaction inspection, and contract lookup. It emphasizes help-first schema inspection, bearer-token authentication, and read-first handling before broader automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to an Etherscan API key and configures a UXC authentication binding for the Etherscan MCP endpoint.

Mitigation: Install only when that access is acceptable, prefer environment or secret-manager backed credentials, and verify the auth binding before use.

Risk: The verifySourceCode operation is a submission-style action rather than a passive lookup.

Mitigation: Require explicit user confirmation before invoking verifySourceCode.

Risk: Some Etherscan MCP tools may be plan-gated or may change schemas independently of this wrapper skill.

Mitigation: Run operation-specific help before first use and handle API plan or schema errors in the returned response.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Etherscan MCP endpoint](https://mcp.etherscan.io/mcp)
- [ClawHub skill page](https://clawhub.ai/jolestar/skills/etherscan-mcp-skill)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent to inspect operation help, configure bearer authentication, and parse JSON envelopes from Etherscan MCP responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
