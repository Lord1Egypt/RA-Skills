## Description:

Provides read-only DeFi intelligence for opportunity research, portfolio diagnostics, allocation analysis, route previews, Trail Heat, and Sybil review without executing transactions.

This skill is for research and development only.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

DeFi users and agents use this skill to compare protocols, review portfolio and wallet signals, and explore hypothetical allocations using time-bound research. It provides analysis and guidance for user decisions, not transaction execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research inputs and any supplied API key are sent to FarmDash; optional onboarding and installation tracking also involve data sharing.

Mitigation: Use public wallet addresses only, omit the optional API key when keyless Scout access is sufficient, and skip optional onboarding or installation tracking if you do not want that data shared.

Risk: DeFi scores, wallet signals, and points simulations can be heuristic, time-sensitive, or mistaken for guarantees about returns or eligibility.

Mitigation: Show timestamps, sources, and data-quality limits; treat simulations as hypothetical, and check current protocol rules and risks before making decisions.

Risk: FarmDash may receive referral, affiliate, or routing compensation from some routes.

Mitigation: Disclose the possible compensation and fee details when presenting a route, and only surface routes when the user asks how to proceed.

## Reference(s):

- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [FarmDash OpenAPI Contract](https://www.farmdash.one/agents/openapi.yaml)
- [FarmDash MCP Discovery Manifest](https://www.farmdash.one/.well-known/mcp.json)
- [FarmDash Security and Authority Boundaries](https://www.farmdash.one/security)
- [FarmDash Fees and Commercial Terms](https://www.farmdash.one/fees)
- [ClawHub release page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-trail-intelligence)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text, Markdown]

**Output Format:** [Text or Markdown research summaries and comparison tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include timestamps, source attribution, confidence and data-quality caveats, and hypothetical scenario results.]

## Skill Version(s):

1.0.22 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
