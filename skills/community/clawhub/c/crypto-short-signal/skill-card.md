## Description:

Generates crypto short-signal outputs for token unlock scenarios, including timing, target, stop-loss, and risk information based on the skill's packaged token data and analysis flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennyhuang2024](https://clawhub.ai/user/dennyhuang2024)

### License/Terms of Use:

MIT

## Use Case:

External ClawHub users can request short-signal guidance for supported crypto tokens around unlock events. The skill is intended for informational analysis and does not provide investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a hardcoded financial API key.

Mitigation: Remove and rotate the embedded key, require injected secrets, and document required secret configuration before installation.

Risk: The security evidence reports caller-supplied billing identity and request validation concerns.

Mitigation: Bind billing to authenticated platform identity, validate requests before charging, and add idempotency or duplicate-charge protection.

Risk: The skill produces crypto trading signals that could be mistaken for financial advice.

Mitigation: Keep the investment-risk disclaimer visible and require users to treat outputs as informational rather than trading instructions.

Risk: The security evidence recommends clearer disclosure of user data shared with SkillPay.

Mitigation: Disclose payment and request data sent to SkillPay and pin reviewed dependencies for release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dennyhuang2024/skills/crypto-short-signal)
- [Publisher profile](https://clawhub.ai/user/dennyhuang2024)
- [SkillPay](https://skillpay.me/)
- [OpenClaw](https://openclaw.ai/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON responses and human-readable command-line text with payment, error, or crypto signal fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include payment-required states, analysis data for supported tokens, and risk or disclaimer text.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact files also declare 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
