## Description:

Free Bitcoin AI: live BTC price, halving 2028, Fear & Greed, predictions. Lightning: welove@blink.sv

This skill is ready for commercial/non-commercial use.

## Publisher:

[welove111](https://clawhub.ai/user/welove111)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve Bitcoin market information, including live BTC price, halving details, on-chain signals, market-cycle context, and long-range BTC predictions. It can also surface voluntary Bitcoin Lightning donation information with explicit user consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes an unrelated search, OSINT, and security-dorking package capable of finding exposed secrets, admin pages, personal identifiers, and other sensitive information.

Mitigation: Install only if that bundled package is intended; otherwise remove or disable it before deployment and allow sensitive discovery workflows only for authorized targets.

Risk: Bitcoin price and prediction outputs may be treated as investment advice or relied on without validation.

Mitigation: Present market outputs as informational, include non-financial-advice framing, and encourage users to verify live data against trusted market sources.

Risk: Donation and Lightning invoice behavior could prompt a user toward payment.

Mitigation: Require explicit user confirmation before displaying or acting on wallet registration, invoice generation, or payment-related steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/welove111/skills/btcvision-oracle)
- [BTCvision website](https://btc-vision.org)
- [BTCvision MCP endpoint](https://btc-vision.org/.netlify/functions/mcp)
- [Publisher profile](https://clawhub.ai/user/welove111)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text with optional structured API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live market data, prediction ranges, market-signal summaries, donation addresses, or Lightning invoice details depending on the invoked tool.]

## Skill Version(s):

2.2.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
