## Description:

Estimate the fair opening or intraday value of Hong Kong-listed CSOP SK Hynix Daily (2x) Leveraged Product (07709.HK) from its latest NAV, KRX 000660 price, Nasdaq SKHY return, ADR conversion ratio, FX, and prior market discount.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinjobs](https://clawhub.ai/user/qinjobs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial analysis agents use this skill to estimate a timestamped NAV fair value, carried-discount trading scenario, and ADR cross-check for HKEX 07709. It is intended for market-data-assisted valuation analysis, not trade execution or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The estimate can be misleading if NAV, KRX, Nasdaq ADS, FX, or prior market-price inputs are stale or unverified.

Mitigation: Require the calling agent to fetch and timestamp each input, verify symbols, and state the market date and local timestamp used for the estimate.

Risk: A leveraged daily product can trade away from theoretical NAV because of market-maker inventory, swap or option capacity, liquidity, spreads, and creation or redemption constraints.

Mitigation: Report NAV fair value separately from a carried-discount tradable scenario, and include warnings when secondary-market premium or discount risk is material.

Risk: SKHY ADS absolute parity can be distorted by issuance, settlement, liquidity, market-hour differences, or cross-border arbitrage limits.

Mitigation: Use live KRX 000660 as the primary anchor when available and treat SKHY as an overnight direction check when the ADS parity gap is large.

Risk: Users may overread the output as a guaranteed executable quote or investment recommendation.

Mitigation: Present the result as a timestamped estimate with a scenario range and state that the skill does not fetch data, place trades, persist data, or handle credentials.

## Reference(s):

- [Methodology and Sources](references/methodology.md)
- [CSOP SK Hynix Daily (2x) Leveraged Product](https://www.csopasset.com/en/products/hk-skhy-2l)
- [HKEX Product Key Facts Statement](https://www.hkexnews.hk/listedco/listconews/sehk/2026/0622/2026062200892.pdf)
- [SKHY SEC ADS Ratio Filing](https://www.sec.gov/Archives/edgar/data/2120882/000119312526299963/d32785d424b4.htm)
- [Citi Depositary Receipts Directory](https://depositaryreceipts.citi.com/)
- [ClawHub Skill Page](https://clawhub.ai/qinjobs/skills/estimate-hynix-2x-open)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with valuation figures, scenario range, warnings, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires fresh, timestamped NAV, KRX, Nasdaq ADS, FX, and prior market price inputs supplied by the calling agent.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
