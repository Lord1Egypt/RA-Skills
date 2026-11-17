## Description:

摆摊创业全流程助手为街摊创业者提供选品推荐、利润测算、选址评分、天气应对、合规检查、痛点预检和综合决策报告支持。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan a street-vending business by collecting user constraints, running bundled calculators, comparing products and locations, and preparing an operating checklist and report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can execute injected script if report data is untrusted.

Mitigation: Only generate or open reports from trusted data, or HTML-escape and sanitize user-controlled fields before previewing or sharing reports.

Risk: Planning recommendations rely on market references, scoring assumptions, and user-supplied local details that may not match actual permits, costs, traffic, or demand.

Mitigation: Validate local policy, pricing, supplier availability, and location traffic before investing or operating.

## Reference(s):

- [摆摊品类目录与利润参考](references/product_catalog.md)
- [摆摊选址评估因子体系](references/location_factors.md)
- [摆摊10大痛点与应对策略](references/pain_points_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON calculator outputs, tables, checklists, and an optional HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on user-provided budget, city tier, season, experience, product preference, location scores, and optional report data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
