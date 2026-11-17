## Description:

帮助电商经营者在淘宝、天猫、京东、拼多多、抖音电商、小红书、视频号及 Temu 上评估选品、测算定价和投放回报、诊断转化、检查文案并规划备货。

This skill is ready for commercial/non-commercial use.

## Publisher:

[g305595965](https://clawhub.ai/user/g305595965)

### License/Terms of Use:

MIT

## Use Case:

电商经营者和运营人员使用该技能评估产品、测算利润与广告回报、定位店铺转化瓶颈，并辅助商品文案审核及库存计划。

### Deployment Geography for Use:

China, with Temu cross-border selling guidance

## Known Risks and Mitigations:

Risk: Live-data commands can include untrusted values that become executable shell text.

Mitigation: Validate and shell-quote every value in live_data.json, and review generated commands before execution.

Risk: Live searches may expose sensitive product, supplier, pricing and platform details to external sites.

Mitigation: Avoid sending confidential business terms to external search or fetch services without approval.

Risk: Reference fees and compliance checks can be outdated or incomplete.

Mitigation: Confirm rates and rules against current seller-platform notices and obtain human review before publishing claims or making consequential decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/g305595965/skills/cn-ecommerce-ops)
- [Platform operations playbook](artifact/references/platform-playbook.md)
- [Product selection guide](artifact/references/product-selection.md)
- [Listing and content guide](artifact/references/listing-and-content.md)
- [Operations playbook](artifact/references/operations-playbook.md)
- [Temu cross-border guide](artifact/references/crossborder-temu.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance and calculator results, with optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live-data workflows may suggest commands to run with user-supplied values.]

## Skill Version(s):

1.2.1 (source: ClawHub release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
