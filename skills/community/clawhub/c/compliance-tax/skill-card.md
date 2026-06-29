## Description: <br>
输入销售国家后，该技能为跨境电商卖家汇总多国税率、注册门槛、申报周期、截止日、EU OSS 场景和平台代扣注意事项。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheyuy](https://clawhub.ai/user/sheyuy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and operators use this skill to quickly compare tax obligations across supported cross-border ecommerce markets, including VAT, GST, Sales Tax, JCT, registration checks, filing calendars, EU OSS guidance, and next-action planning. The output is informational and should be verified before filing or changing tax strategy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tax rates, registration thresholds, and filing duties may be outdated or jurisdiction-specific. <br>
Mitigation: Verify current obligations with official tax authorities or a qualified tax professional before registering, filing, or changing tax strategy. <br>
Risk: Users may mistake informational tax checklists for professional tax advice. <br>
Mitigation: Treat the output as a starting point for review, especially for EU OSS, marketplace-facilitator, double-taxation, and filing-duty questions. <br>
Risk: Marketplace-facilitator and platform collection rules can reduce collection work without removing every reporting obligation. <br>
Mitigation: Confirm whether each marketplace, country, and sales channel still requires registration, periodic filing, or zero returns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sheyuy/compliance-tax) <br>
- [Server-resolved GitHub provenance](https://github.com/Sheyuy/compliance-skills/tree/main/compliance-tax) <br>
- [Tax data matrix](references/tax-data.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown summaries with JSON-compatible tax health, country detail, recommendation, and next-action fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses countries plus optional revenue, channel, and existing-compliance inputs; produces informational tax checklists rather than filing-ready advice.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
