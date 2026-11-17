## Description:

电商商品兴趣度分析助手，可读取用户浏览行为数据（CSV、JSON 或手动录入），通过多维度加权算法分析商品兴趣度，结合 NLP 文案质量评估诊断价格和文案问题，并生成交互式 HTML 可视化诊断报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, analysts, and developers use this skill to turn product behavior metrics into interest scores, conversion diagnostics, HTML reports, and prioritized optimization guidance for platforms such as Douyin Ecommerce, Taobao, Pinduoduo, and JD.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can execute injected JavaScript when built from malicious CSV or JSON input.

Mitigation: Use trusted datasets only, and avoid opening or sharing reports from untrusted inputs until report fields are HTML-escaped and JavaScript values are safely serialized.

Risk: Reports load Chart.js from a public CDN, which may be unsuitable for sensitive business data or offline environments.

Mitigation: Bundle Chart.js locally before using the skill with sensitive data or in restricted-network deployments.

Risk: Interest scores and recommendations are heuristic diagnostics and may not capture all business context.

Mitigation: Treat the report as decision support and review recommendations with business, pricing, and merchandising context before acting.

## Reference(s):

- [Project homepage](https://github.com/bettermen/ecommerce-interest-analyzer)
- [ClawHub skill page](https://clawhub.ai/bettermen/skills/ecommerce-interest-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands plus generated JSON analysis results and an interactive HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on CSV or JSON ecommerce behavior data; generated reports load Chart.js from a CDN unless the dependency is bundled locally.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
