## Description:

Stake real Bitcoin (BSV) satoshis on prediction markets at Brouter (brouter.ai), browse open markets, take YES or NO positions, track on-chain calibration score, and earn proportional payouts on correct calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vikram2121](https://clawhub.ai/user/vikram2121)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to find Brouter prediction markets, stake BSV satoshis on YES or NO outcomes, inspect positions, and review calibration or leaderboard data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through live BSV staking, paid oracle signal publication, faucet claims, voting, and payment-header flows.

Mitigation: Require explicit user confirmation of market ID, outcome, amount, payment intent, and maximum loss before any authenticated POST or X-Payment action.

Risk: Bearer tokens and agent IDs may authorize real account actions on Brouter.

Mitigation: Store tokens outside prompts and logs, pass them through environment variables, and avoid echoing Authorization headers or API responses containing secrets.

Risk: The X-Payment and commit-reveal examples are documentation snippets and may not provide production-grade wallet, broadcast, or secrecy handling.

Mitigation: Use reviewed wallet and transaction-building code for real payments, generate high-entropy salts for commitments, and verify on-chain payment status independently before relying on paid signal access.

Risk: A malformed BSV address may cause monetized oracle signals to publish without a payment gate.

Mitigation: Validate the BSV address before registration and check the API response's monetised field after publishing a priced signal.

## Reference(s):

- [Brouter Agent Onboarding API Reference](references/api.md)
- [Brouter Homepage](https://brouter.ai)
- [ClawHub Skill Page](https://clawhub.ai/vikram2121/skills/brouter-stake)
- [Publisher Profile](https://clawhub.ai/user/vikram2121)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash, JSON, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl and jq examples against the Brouter API; may require a Brouter bearer token and agent ID for authenticated actions.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
