## Description:

萤火虫空压机报价单生成助手，可根据产品型号和配置生成客户报价单，并输出品牌 HTML 或 Markdown 报价单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhc2026](https://clawhub.ai/user/yhc2026)

### License/Terms of Use:

MIT-0

## Use Case:

Sales users and agents use this skill to produce Firefly compressor quotations from requested models, air-demand requirements, accessories, discounts, freight, installation, and tax rules. It is intended for customer-facing quote preparation, with final business terms reviewed before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated quotations may contain incorrect VAT, tax, freight, discount, or total-price calculations.

Mitigation: Verify seller contact details and independently check VAT, tax totals, and final business terms before sending quotes to customers.

Risk: HTML quote output may be unsafe or misleading if populated with untrusted customer-supplied text.

Mitigation: Escape or sanitize customer-supplied text before using it in HTML output.

## Reference(s):

- [Pricing Rules Reference](references/pricing-rules.md)
- [Firefly Compressor Website](http://www.fireflies.net.cn)
- [ClawHub Skill Page](https://clawhub.ai/yhc2026/skills/firefly-quotation-v5)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Shell commands, Configuration]

**Output Format:** [Markdown quotation text, optional self-contained HTML, and optional Python calculation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses YAML product and pricing data; HTML quotes should be reviewed before distribution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
