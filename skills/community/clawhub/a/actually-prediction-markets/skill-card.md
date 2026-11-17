## Description:

Looks up current Polymarket prediction market pricing for future-event claims such as elections, rate decisions, sports, court dates, and releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sofiia7](https://clawhub.ai/user/sofiia7)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn future-event claims in conversation, news, or documents into current market-implied probabilities. It supports reporting the matched market question, confidence, and alternatives so the probability is presented with context.

### Deployment Geography for Use:

Global for read-only probability lookup; trading features are subject to Polymarket geographic restrictions when deliberately enabled.

## Known Risks and Mitigations:

Risk: Setting POLYMARKET_PRIVATE_KEY can enable real-money trading through the MCP server.

Mitigation: Keep the skill read-only by default; if trading is intentionally enabled, isolate the MCP process, pin and review the npm package version, use a limited wallet, set strict order and daily caps, and require manual confirmation for every trade.

Risk: Semantic matching can return a related but different market for a thin or ambiguous claim.

Mitigation: Show the matched market question, confidence score, and alternatives before reporting a probability.

Risk: Prediction-market prices are market signals, not authoritative forecasts, and thin markets can be noisy.

Mitigation: Describe probabilities as current market pricing and avoid presenting them as guarantees or expert consensus.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sofiia7/skills/actually-prediction-markets)
- [Publisher profile](https://clawhub.ai/user/sofiia7)
- [Source and threat model referenced by the skill](https://github.com/Sofiia7/actually)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON MCP configuration examples and structured market lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use MCP calls that return matched market questions, probabilities, confidence scores, alternatives, live prices, and orderbook snapshots.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
