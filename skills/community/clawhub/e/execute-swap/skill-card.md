## Description:

Executes Uniswap token swaps with quotes, safety checks, simulation, and routing across supported Uniswap protocols and chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to prepare and execute Uniswap token swaps from natural-language requests while checking token safety, limits, slippage, routing, and transaction results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare and submit real token swaps through external Uniswap MCP and trade-executor components.

Mitigation: Use it only in an environment approved for live transaction authority, verify the MCP server and executor separately, and require manual final confirmation before transactions involving real funds.

Risk: Installation guidance uses mutable package or repository references.

Mitigation: Prefer pinned package versions, immutable commit references, and reviewed dependency sources before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/execute-swap)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, guidance]

**Output Format:** [Markdown status reports with transaction details, errors, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Uniswap MCP tooling and a trade-executor component for live swap execution.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
