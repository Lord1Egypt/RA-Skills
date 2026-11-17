## Description:

电商多平台商品数据分析助手。输入任意主流电商平台商品链接（淘宝/天猫/京东/拼多多/抖音电商/1688），自动抓取商品详情、搜索跨平台同款商品、对比价格/评分/评价，生成交互式可视化HTML分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping researchers use this skill to compare product listings across major Chinese e-commerce platforms, summarize price and rating differences, and generate a visual buying-analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can execute unsafe content from product-derived data.

Mitigation: Escape all product-derived text before rendering reports and review generated HTML before opening or sharing it.

Risk: Product links in generated reports can expose users to unsafe navigation behavior.

Mitigation: Restrict report links to http/https URLs and add rel="noopener noreferrer" to external links.

Risk: The report depends on a remotely loaded Chart.js script.

Mitigation: Bundle Chart.js locally or use an integrity-checked dependency source.

Risk: Shared /tmp output paths can leave stale data or collide between runs.

Mitigation: Use unique per-run output paths or clean up temporary files after report generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/ecommerce-multi-analyzer)
- [Project homepage](https://github.com/bettermen/ecommerce-analyzer)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance, Files]

**Output Format:** [JSON data prepared for a generated interactive HTML report, with concise shopping analysis and buying guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python.exe; report generation uses product-derived data and should be reviewed before opening or sharing generated HTML.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
