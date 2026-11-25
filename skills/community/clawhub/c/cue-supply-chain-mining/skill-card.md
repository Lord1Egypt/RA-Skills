## Description:

Maps public A-share industry chains, explains business-cycle transmission, and screens listed companies for research using public information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Industry researchers and investors can use the skill to map listed-company supply chains, trace demand and pricing trends across upstream and downstream segments, and identify companies for further diligence. Its documentation limits the work to public-information research and excludes trade timing or buy/sell advice.

### Deployment Geography for Use:

China (A-share markets: Shanghai, Shenzhen, and Beijing)

## Known Risks and Mitigations:

Risk: The security assessment flags credential-exposure concerns, actions outside the stated research purpose, and external-package and mutable-repository dependencies; it also reports incomplete analysis.

Mitigation: Review and correct credential-handling instructions and unrelated actions before installation; do not share API keys in chat. Review and pin external package and repository sources before use.

Risk: Company screening and elasticity analysis could be mistaken for reliable investment recommendations.

Mitigation: Treat the report as preliminary research, verify claims against linked public filings and sources, and do not use it as buy/sell or timing advice.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/panting09266-ai/skills/cue-supply-chain-mining)
- [Cue platform](https://cuecue.cn)
- [Example research report](https://cuecue.cn/share/F8PzjKYbVBgYX2oN9clWB)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Structured Markdown report with an industry-chain map, transmission analysis, company screening, elasticity assessment, risk notes, and source links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One industry-chain query; findings are linked to public sources where available.]

## Skill Version(s):

1.1.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
