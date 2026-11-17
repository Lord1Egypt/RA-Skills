## Description:

Analyzes cryptocurrency screenshots and text queries by classifying the asset type, cross-checking public market information, and producing a quick risk scan followed by deeper analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyanzhuang5-cyber](https://clawhub.ai/user/haiyanzhuang5-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to interpret cryptocurrency screenshots or coin questions, classify assets, compare screenshot-derived values with public search information, and receive risk-focused observation notes. It is intended for informational analysis, not trading execution or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can present unverified or fabricated market and screenshot data as fresh analysis in a financial context.

Mitigation: Treat outputs as rough, unverified analysis; independently verify prices and news before relying on them.

Risk: Users may provide screenshots containing balances, account details, or other sensitive financial information.

Mitigation: Redact balances, account identifiers, and other sensitive details before submitting screenshots.

Risk: Financial analysis could be mistaken for trading advice or used to support automated trading decisions.

Mitigation: Keep the skill limited to informational observation, preserve disclaimers, and do not use it to execute trades or make automated trading decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/haiyanzhuang5-cyber/skills/crypto-search-advisor)
- [README](artifact/README.md)
- [Architecture](artifact/ARCHITECTURE.md)
- [Output Format](artifact/FORMAT.md)
- [Examples](artifact/EXAMPLES.md)
- [OpenClaw Integration](artifact/OPENCLAW_INTEGRATION.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and structured JSON-style analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Two-stage response pattern: quick risk scan first, then deeper analysis; outputs include disclaimers and input reliability scoring.]

## Skill Version(s):

2.5.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
