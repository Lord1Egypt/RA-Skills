## Description:

A restaurant menu pricing and profit optimization agent that analyzes menu costs, sales volume, BCG/Menu Engineering quadrants, price elasticity, Pareto contribution, full-cost profitability, competitive pricing, and target-margin scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monsterdt](https://clawhub.ai/user/monsterdt)

### License/Terms of Use:

MIT-0

## Use Case:

Restaurant owners, franchise investors, menu developers, and operations teams use this skill to diagnose menu profitability, identify dishes to promote, reprice, rework, or retire, and generate sales-plus-profit reports from structured menu and sales data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser sales-entry page can mishandle crafted imported data, and exported CSV reports can be unsafe when opened in spreadsheet software.

Mitigation: Import only trusted restaurant sales files and treat exported CSV reports as untrusted when opening them in spreadsheet tools.

Risk: Pricing recommendations, especially Puzzle repricing and target-margin scenarios, may mislead decisions if accepted without review.

Mitigation: Have an operator or finance reviewer validate scenario assumptions, menu-level impact figures, and recommended price changes before changing menus.

Risk: Restaurant pricing, cost, and sales inputs may contain proprietary business information.

Mitigation: Run the analysis locally where possible, limit access to input and output files, and avoid sharing proprietary restaurant data unnecessarily.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/monsterdt/skills/dish-pricing-advisor)
- [Methodology reference](references/methodology.md)
- [SkillHub listing](references/skillhub_listing.md)
- [Restaurant owner guide](references/餐饮老板使用指南.md)
- [Joint analysis sample report](references/sample_joint_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with JSON analysis files, CSV exports, and inline shell commands for local analysis scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deterministic menu engineering, sales analytics, and joint insight reports from user-provided restaurant data; numeric recommendations require human review before business action.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter states 3.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
