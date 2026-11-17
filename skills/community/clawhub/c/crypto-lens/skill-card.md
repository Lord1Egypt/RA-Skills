## Description:

CryptoLens provides paid, AI-driven cryptocurrency comparison and technical analysis with indicator summaries and dark-theme PNG charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godofbush](https://clawhub.ai/user/godofbush)

### License/Terms of Use:


## Use Case:

External users and agents use CryptoLens to compare 2-5 crypto assets, generate single-coin technical-analysis charts, and request scoring-based market signal summaries after SkillPay billing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a paid release that sends a wallet-based billing identifier to SkillPay before execution.

Mitigation: Install only when users understand the billing flow, provide wallet identifiers deliberately, and can verify any payment_url before topping up.

Risk: The security review reports an embedded reusable billing API key and insufficiently controlled charge handling.

Mitigation: Rotate and remove the embedded billing key, make exact charges verifiable before use, and restrict execution until billing behavior is reviewed.

Risk: The skill sends token queries to external market-data services and writes chart/cache files under /tmp.

Mitigation: Use it only where external market-data requests are acceptable, and secure or clean temporary outputs that may reveal queried assets.

Risk: Dependencies are version-ranged rather than pinned.

Mitigation: Pin and review Python dependencies before production deployment.

Risk: Documentation states each command costs 1 token, while the compare command has a script comment indicating 5 tokens.

Mitigation: Confirm the active SkillPay dashboard pricing and user-facing billing disclosure before enabling paid use.

## Reference(s):

- [CryptoLens ClawHub listing](https://clawhub.ai/godofbush/skills/crypto-lens)
- [Publisher profile: godofbush](https://clawhub.ai/user/godofbush)
- [SkillPay billing service](https://skillpay.me)
- [CoinGecko API](https://api.coingecko.com/api/v3)
- [Hyperliquid API endpoint](https://api.hyperliquid.xyz/info)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON with text_plain summaries and chart_path values for PNG charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a payment_url when balance is insufficient; chart outputs are written under /tmp.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
