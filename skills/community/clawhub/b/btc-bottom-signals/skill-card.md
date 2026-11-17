## Description:

Evaluate potential BTC bottom zones with AgentKey-powered crypto market, sentiment, on-chain, ETF flow, and technical confluence signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzallenn](https://clawhub.ai/user/zzallenn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and crypto analysts use this skill to evaluate whether BTC/USD is near a potential bottom by combining live market, sentiment, on-chain, ETF-flow, and technical signals into a scored research report with invalidation conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs may be mistaken for financial advice or direct trade recommendations.

Mitigation: The skill frames results as research, avoids buy/sell orders, states uncertainty, and includes invalidation conditions.

Risk: AgentKey calls can incur third-party costs or depend on live endpoint availability.

Mitigation: The skill requires a preflight tool check, endpoint descriptions before execution, and user confirmation when three or more calls or at least 10 credits are expected.

## Reference(s):

- [BTC Bottom Signals on ClawHub](https://clawhub.ai/zzallenn/skills/btc-bottom-signals)
- [AgentKey Tool Reference](artifact/references/agentkey-tools.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with verdict, evidence table, bottom checklist, invalidation conditions, and method summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live AgentKey crypto data when tools are connected; includes call count and approximate credits.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
