## Description:

Real-time electricity prices and cheapest hours in 40 countries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zemloai-ctrl](https://clawhub.ai/user/zemloai-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Elecz to answer electricity spot-price, cheapest-hour, contract-comparison, and high-consumption scheduling questions for supported markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Electricity price lookups use Elecz's remote MCP service and may send zone plus optional consumption and heating inputs.

Mitigation: Install only if use of that remote service is acceptable, avoid sending unnecessary sensitive context, and review the linked privacy policy.

Risk: Price, cheapest-hour, and contract-comparison responses are advisory and may not include every retail fee, tax, grid fee, or regulated-market constraint.

Mitigation: Verify important contract, billing, or automation decisions against the user's utility, provider terms, and local retail-rate details.

Risk: Automating high-consumption devices from price signals can create cost, comfort, or safety impacts if data is stale or local conditions differ.

Mitigation: Keep a human approval step for material device scheduling decisions and apply local safeguards before controlling EV chargers, appliances, or heating loads.

## Reference(s):

- [Elecz Homepage](https://elecz.com)
- [Elecz Privacy Policy](https://elecz.com/privacy)
- [Elecz Docs](https://elecz.com/docs)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls]

**Output Format:** [Markdown or plain text responses with electricity prices, cheapest-hour windows, savings estimates, and local-market notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a remote read-only MCP service for electricity price lookups; no API key required by the skill evidence.]

## Skill Version(s):

1.9.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
