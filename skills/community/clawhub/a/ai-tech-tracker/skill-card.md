## Description:

获取最新AI技术动向，区分国内和国外市场，追踪各大模型的重点更新优化、重要技术迭代，识别划时代级产品，进行热度评级和专业分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hwl1413520](https://clawhub.ai/user/hwl1413520)

### License/Terms of Use:

MIT-0

## Use Case:

AI practitioners, investors, and technology researchers use this skill to gather recent AI news across domestic and international markets, classify model and product updates, rate importance and heat, and produce structured weekly or monthly reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can change or remove files in a selected skills directory and includes a validation step flagged as injection-prone by the security evidence.

Mitigation: Review install.sh before use, install only into a user-controlled Claude skills directory, avoid elevated privileges, and prefer manual copying or a fixed validation block that passes paths as Python arguments.

Risk: AI news reports can become stale quickly or include unsupported claims if sources are weak.

Mitigation: Use official announcements and reputable technical sources first, include report time ranges and source links, and review important claims before business or investment use.

## Reference(s):

- [AI vendor and product database](references/AI_DATABASE.md)
- [AI technology evaluation criteria](references/EVALUATION_CRITERIA.md)
- [AI technology report template](assets/report_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports with structured sections, tables, ratings, trend analysis, and source links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper script can also export structured JSON report data when used directly.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
