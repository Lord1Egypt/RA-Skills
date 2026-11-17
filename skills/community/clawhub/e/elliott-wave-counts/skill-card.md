## Description:

Automated wave counting and market cycle prediction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request automated Elliott Wave-style wave counts and market-cycle signals for an asset ticker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts an external API with the ticker provided by the user.

Mitigation: Use only ticker values appropriate to share with the provider and expect a network request during execution.

Risk: Returned market signals can be incomplete, inaccurate, or unsuitable as financial advice.

Mitigation: Treat outputs as informational market-signal data and verify them with independent analysis before making financial decisions.

Risk: Premium responses can include a payment request.

Mitigation: Follow payment instructions only after independently trusting the provider and confirming the pricing terms.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ssidharhubble/skills/elliott-wave-counts)
- [Publisher profile](https://clawhub.ai/user/ssidharhubble)
- [Premium pricing page](https://ssyopros.zo.space/pricing)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON response from an external market-signal API, or a JSON payment-required error]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a ticker string; premium signals may require a payment proof.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
