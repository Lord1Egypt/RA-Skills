## Description:

Canopy lets AI agents make policy-gated USD payments on Base, pay paywalled APIs through x402 or MPP, discover paid services, check budgets, and route higher-risk payments through human approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atifazam](https://clawhub.ai/user/atifazam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Canopy to connect AI agents to a policy-gated treasury wallet for organizational payments, paywalled API access, paid service discovery, budget checks, and approval workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent connected to Canopy can move organizational funds.

Mitigation: Install only when payment capability is intended, use the least-privileged Canopy agent, and configure strict spend caps and allowlists.

Risk: A payment could be sent to the wrong recipient or for the wrong amount.

Mitigation: Verify the recipient and amount before each payment, and use preview behavior when the amount is dynamic or untrusted.

Risk: Pending approvals could be mishandled if an agent approves without explicit user intent.

Mitigation: Do not auto-approve; call approval or denial tools only after a clear user instruction.

## Reference(s):

- [Canopy ClawHub Skill Page](https://clawhub.ai/atifazam/skills/canopy)
- [Canopy Homepage](https://www.trycanopy.ai)
- [Canopy Dashboard](https://www.trycanopy.ai/dashboard/agents)
- [MCP Tools Reference](https://www.trycanopy.ai/documentation/reference/mcp-tools)
- [Payment Outcomes](https://www.trycanopy.ai/documentation/concepts/payment-outcomes)
- [Policies](https://www.trycanopy.ai/documentation/concepts/policies)
- [x402 Protocol](https://www.trycanopy.ai/documentation/concepts/x402)
- [Connect MCP Hosts](https://www.trycanopy.ai/documentation/connect/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Canopy account plus CANOPY_API_KEY and CANOPY_AGENT_ID; payment actions are policy-gated and may require human approval.]

## Skill Version(s):

1.0.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
