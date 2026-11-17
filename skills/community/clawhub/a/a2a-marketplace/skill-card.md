## Description:

AI tool marketplace via AgentForge - discover, compare, and execute tools with automatic billing and trust scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paparusi](https://clawhub.ai/user/paparusi)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to discover marketplace tools, compare options by price and trust score, inspect schemas, check balance, and execute single or batch tool calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketplace tool execution can incur charges automatically.

Mitigation: Check balance and pricing before execution, use max-price filters where available, and require explicit spending controls for reviewed deployments.

Risk: Submitted inputs may be handled by third-party marketplace tools.

Mitigation: Avoid sensitive data unless provider handling is clear and the publisher and selected tool are trusted.

Risk: The release lacks enough install pinning and safeguards for high-impact paid execution behavior.

Mitigation: Prefer a pinned, reviewed plugin version before installation and review the skill carefully before use.

## Reference(s):

- [A2A Marketplace on ClawHub](https://clawhub.ai/paparusi/skills/a2a-marketplace)
- [Publisher profile: paparusi](https://clawhub.ai/user/paparusi)

## Skill Output:

**Output Type(s):** [Guidance, API calls, JSON]

**Output Format:** [Markdown guidance with inline marketplace tool-call and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute paid third-party marketplace tools; batch execution supports up to 10 calls.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
