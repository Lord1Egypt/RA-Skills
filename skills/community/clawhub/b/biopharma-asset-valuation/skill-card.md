## Description:

Combines rNPV, peak-sales assumptions, probability of success, development cost, timing, comparable transactions, and deal-structure analysis to estimate biopharma asset value for licensing and negotiation preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Biopharma BD managers and deal teams use this skill to value pipeline assets for in-licensing, out-licensing, and negotiation preparation. It guides a sourced workflow that combines market sizing, pricing assumptions, clinical probability of success, comparable transactions, scenario valuation, deal-structure design, and negotiation strategy into a professional report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may contain unsafe or misleading content, especially HTML created from valuation inputs.

Mitigation: Treat generated HTML as untrusted, avoid opening or sharing reports from untrusted inputs, and review generated reports before use.

Risk: Real transaction data and valuation formula assumptions may be incomplete or unsuitable for a specific asset.

Mitigation: Review the transaction dataset, assumptions, source labels, and confidence levels before relying on any valuation result.

Risk: The scanner recommends review before installation.

Mitigation: Install only when the publisher is trusted and run the skill in an isolated workspace with outputs confined to a dedicated directory.

## Reference(s):

- [Real Deals Database](references/real_deals_1394.json)
- [Sample Real Deals](references/real_deals.json)
- [ClawHub Skill Page](https://clawhub.ai/yuanzhian-patsnap/skills/biopharma-asset-valuation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, generated HTML reports, JSON input configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow emphasizes source labels, confidence levels, three-scenario valuation, and review of generated reports before relying on results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
