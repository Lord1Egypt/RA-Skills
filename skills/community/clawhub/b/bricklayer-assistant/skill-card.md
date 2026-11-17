## Description:

Chinese-language masonry workflow assistant for material calculations, mortar ratios, pricing references, tile layout, construction guidance, quality diagnosis, acceptance checks, and safety guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External Chinese-speaking construction and renovation users use this skill to estimate masonry and tile materials, compare mortar ratios and pricing references, plan tile layouts, diagnose workmanship issues, and generate practical checklists or reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pricing, safety rules, waterproofing practices, and construction requirements can vary by location and project conditions.

Mitigation: Confirm estimates and practices against current local prices, local codes, site conditions, and qualified professional guidance before acting.

Risk: Load-bearing walls, leaks, falling tiles, and high-risk repair work can create structural or personal safety hazards.

Mitigation: Escalate these cases to a qualified professional and avoid relying on the skill as the sole source of advice.

Risk: Material calculations can be wrong if dimensions, units, waste rates, or tile layouts are entered incorrectly.

Mitigation: Review all inputs and include appropriate waste factors before purchasing materials or starting work.

## Reference(s):

- [Project homepage](https://github.com/bettermen/bricklayer-assistant)
- [材料计算参考表](references/calculation-reference.md)
- [砂浆配比速查表](references/mortar-ratio.md)
- [瓦匠报价参考表](references/pricing-reference.md)
- [瓷砖排版指南](references/tile-layout.md)
- [施工工艺标准](references/workmanship-standards.md)
- [常见质量问题诊断与解决](references/troubleshooting.md)
- [验收自检清单](references/acceptance-checklist.md)
- [瓦匠施工安全规范](references/safety-guidelines.md)
- [bricklayer_calc.py](references/bricklayer_calc.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text, with optional interactive HTML reports and JSON calculator output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a Python helper calculator; estimates should be checked against local codes, site conditions, and current prices.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
