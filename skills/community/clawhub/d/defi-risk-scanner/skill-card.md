## Description:

DeFi Risk Scanner helps agents assess DeFi protocols and tokens using public TVL, liquidity, market, and FDV data to produce structured risk scores and verification guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emeraldring3134-netizen](https://clawhub.ai/user/emeraldring3134-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to screen DeFi protocols or token contracts for risk indicators before deeper due diligence. It produces a 0-100 risk score, explains major risk factors, and suggests independent verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary reports unsafe handling of API response values in AWK that could allow malicious API data to execute local commands.

Mitigation: Run the skill only in a low-privilege environment until numeric validation or awk -v style argument passing is implemented.

Risk: Queries to third-party APIs can disclose the protocols, token addresses, or investigation targets being analyzed.

Mitigation: Avoid submitting confidential targets unless third-party API disclosure is acceptable for the investigation.

Risk: Risk scores can be incomplete or misleading if public market and liquidity data are stale, unavailable, or manipulated.

Mitigation: Treat outputs as educational screening guidance and verify findings with independent on-chain, audit, and authorization-review tools before acting.

## Reference(s):

- [DeFi Risk Scanner ClawHub listing](https://clawhub.ai/emeraldring3134-netizen/skills/defi-risk-scanner)
- [Reference data sources and checklist](references/sources.md)
- [DefiLlama](https://defillama.com)
- [DexScreener](https://dexscreener.com/)
- [Token Sniffer](https://tokensniffer.com/)
- [Revoke.cash](https://revoke.cash/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or terminal text risk report with a numeric score, factor breakdown, and recommended verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call public DeFi data APIs and may include financial-risk disclaimers; not financial advice.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
