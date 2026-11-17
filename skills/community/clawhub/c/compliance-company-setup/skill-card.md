## Description:

输入产品与目标市场，一分钟生成跨境公司注册地推荐方案，含8个热门管辖区的成本、税率、流程和平台兼容性对比。适用于跨境电商卖家、独立站创业者、工贸一体小工厂在海外注册公司时不知道选哪个国家的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheyuy](https://clawhub.ai/user/sheyuy)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, independent web store owners, and small manufacturers use this skill to compare cross-border ecommerce company registration jurisdictions and plan registration next steps. It provides preliminary compliance planning guidance, not legal or tax advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company registration, tax, banking, BOI, VAT, and trademark requirements can change or vary by user circumstances.

Mitigation: Treat outputs as preliminary planning guidance and confirm current official requirements with qualified legal, tax, or registration professionals before acting.

Risk: Downstream agents or users may treat suggested next actions as authorization to file documents, pay providers, open accounts, or submit registrations.

Mitigation: Require explicit user approval before any filing, payment, account opening, BOI, VAT, tax identifier, or trademark action is executed.

Risk: The skill covers a limited set of popular jurisdictions and may not address all markets, entity types, or product-specific compliance obligations.

Mitigation: Use the recommendation as a comparison starting point and request expert review when the target market, product category, or planned sales channel is outside the documented coverage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sheyuy/skills/compliance-company-setup)
- [Server-resolved GitHub provenance](https://github.com/Sheyuy/compliance-skills/tree/main/compliance-company-setup)
- [Company setup data matrix](artifact/references/company-setup-data.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown with comparison tables, warnings, feasibility scoring, and structured nextActions examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include jurisdiction recommendations, reasons, warnings, timelines, and action items with priority, action type, description, and status fields.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
