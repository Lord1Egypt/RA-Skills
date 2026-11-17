## Description:

AgentAPI helps agents browse and search a curated directory of MCP-compatible APIs across search, AI, communication, databases, payments, and related integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gizmo-dev](https://clawhub.ai/user/gizmo-dev)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to find AgentAPI directory entries and identify APIs by capability, category, MCP compatibility, authentication model, pricing, and documentation links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AgentAPI directory lookups are external network requests and may expose sensitive search terms.

Mitigation: Avoid putting secrets, private customer data, or confidential project details in AgentAPI search terms.

Risk: Optional x402 payment flows can spend USDC if implemented without controls.

Mitigation: Require explicit user confirmation, verify the payment recipient, and configure per-request and daily spending limits before using any payment flow.

Risk: Directory entries and linked third-party API details may change outside this documentation-only skill.

Mitigation: Review the linked provider documentation before integrating an API or relying on current pricing, rate limits, or authentication requirements.

## Reference(s):

- [AgentAPI ClawHub listing](https://clawhub.ai/gizmo-dev/skills/agentapi)
- [AgentAPI website](https://agentapihub.com)
- [AgentAPI API documentation](https://api.agentapihub.com/api/docs)
- [AgentAPI directory endpoint](https://agentapihub.com/api/v1/apis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and API response JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable behavior is defined by the skill.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
