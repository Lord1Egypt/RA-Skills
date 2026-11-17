## Description:

Fía Signals lets agents call a crypto market intelligence API for gas prices, Solana activity, DeFi yields, due diligence, MEV data, wallet risk, and related market signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odds7](https://clawhub.ai/user/odds7)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agents use this skill to query third-party crypto market data, signals, and risk-style summaries from Fía Signals endpoints. Users should treat the responses as market intelligence inputs rather than financial, audit, or security advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading, audit, and wallet-risk outputs may be misleading if treated as advice.

Mitigation: Treat outputs as third-party market data and require qualified human review before trading, audit, or security decisions.

Risk: Premium x402 endpoints can require paid USDC network use.

Mitigation: Require explicit user confirmation before invoking paid endpoints and review the x402 discovery or endpoint price first.

Risk: Artifact descriptions make broad and partly inconsistent endpoint-count claims.

Mitigation: Confirm needed endpoint availability with the discovery or health endpoint before relying on a specific command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/odds7/skills/fia-signals-skill)
- [Fía Signals API](https://api.fiasignals.com)
- [Fía Signals x402 discovery](https://x402.fiasignals.com/.well-known/x402.json)
- [Fía Signals x402 gateway](https://x402.fiasignals.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and JSON returned by shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some endpoints are free, while premium endpoints require x402 USDC payment.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
