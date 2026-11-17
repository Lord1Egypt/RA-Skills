## Description:

Audits existing Chinese-market investment articles, advisor ads, commentary, screenshots, and relayed company statements against official disclosures and market-data sources, producing a claim-by-claim fact-check report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ovalpatty](https://clawhub.ai/user/ovalpatty)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to check whether claims in existing Chinese listed-company investment content match official filings, exchange market data, and company disclosure channels. It is for fact-checking existing assertions, not for generating stock research, valuations, forecasts, or investment advice.

### Deployment Geography for Use:

Global; market coverage is limited to A-share content as the primary supported scope, with NEEQ and Hong Kong claims handled only within the documented limitations.

## Known Risks and Mitigations:

Risk: The skill may browse or fetch public filings and market-data sources during use.

Mitigation: Use normal network and source-review controls for public-data retrieval, and verify cited filings or market data before relying on the report.

Risk: Optional AKShare or Qichacha MCP access can affect coverage for valuation series or equity-chain checks.

Mitigation: Treat missing optional tooling as a coverage limitation and preserve the skill's documented downgrade behavior instead of filling gaps with guesses.

Risk: Fact-check reports about investment content can be mistaken for investment advice.

Mitigation: Keep outputs framed as factual consistency checks against public information and avoid buy, sell, price-target, valuation, or portfolio recommendations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ovalpatty/skills/a-share-fact-check)
- [Official Channels Inventory](artifact/official-channels.md)
- [Evidence Priority and Source Rules](artifact/evidence-rules.md)
- [Claim Normalization Rules](artifact/normalization.md)
- [Narrative Error Taxonomy](artifact/narrative-errors.md)
- [AKShare](https://github.com/akfamily/akshare)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown fact-check report with quick-read summary, claim tables, source notes, verdicts, and risk-signal sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are public-information fact checks and should not be treated as investment advice.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
