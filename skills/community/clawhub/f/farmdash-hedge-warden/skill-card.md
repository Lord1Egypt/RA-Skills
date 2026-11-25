## Description:

Use when sizing a hedge for existing DeFi exposure: delta-neutral recommendations with explicit bounds and risk notes. Advisory only; never trades itself.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

DeFi traders and agents use the skill to estimate hedge sizes for existing spot positions and prepare a risk-aware handoff for a separate futures research and execution skill. It is advisory and does not sign or submit trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio exposure data, including holdings, notionals, and betas, can be sensitive when sent to FarmDash tooling.

Mitigation: Obtain explicit user consent before measurement or submission, and share only the fields needed to size the hedge.

Risk: Hedge recommendations can be affected by incorrect exposure mappings, correlation or basis changes, funding costs, liquidity, and non-atomic execution; a hedge plan alone does not authorize a trade.

Mitigation: Independently verify exposure and instrument suitability, assess funding and execution drag, use only eligible legs, and reconcile both legs and residual delta after settlement. Require the separate Futures Strategist’s applicable authorization and venue checks before any action.

Risk: The security scan reports a low-probability concern about autonomous decisions and incomplete reference coverage.

Mitigation: Review the authorization conditions before enabling autonomous actions, including the owner-signed grant, session and scope checks, live runtime gates, and local venue-signing requirements described by the skill.

## Reference(s):

- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [FarmDash Hedge Warden manual](https://www.farmdash.one/agents/skills/farmdash-hedge-warden)
- [FarmDash Security and Authority Boundaries](https://www.farmdash.one/security)
- [FarmDash OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [ClawHub release page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-hedge-warden)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON]

**Output Format:** [Structured hedge sizing recommendations with text handoff and risk guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes per-asset hedge targets, data-quality and execution-eligibility indicators, residual exposure, and invalidation guidance.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
