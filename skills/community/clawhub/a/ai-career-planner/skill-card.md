## Description:

AI时代职业规划助手基于用户职业画像评估AI自动化风险、分析能力差距、推荐转型路径，并生成包含12个月行动计划的交互式HTML报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to assess AI automation exposure, identify AI-era competency gaps, compare career transition options, and receive a 12-month action plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may execute unsafe user-derived content.

Mitigation: Review report content before opening or sharing; prefer a version that escapes user input and avoids generated JavaScript.

Risk: The report template loads Chart.js from a remote source without integrity protection.

Mitigation: Use a bundled or integrity-pinned Chart.js dependency before relying on generated reports in sensitive environments.

Risk: Career details, salary, and location can be sensitive personal information.

Mitigation: Collect only needed details and avoid entering salary or location unless required for the planning task.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bettermen/skills/ai-career-planner)
- [Project Homepage](https://github.com/bettermen/ai-career-planner)
- [AI-Era Job Catalog](references/ai_jobs_catalog.md)
- [Automation Risk Framework](references/risk_factors.md)
- [AI-Era Competency Framework](references/competency_framework.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Files]

**Output Format:** [Chinese conversational guidance, Markdown summaries, and an interactive HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports may contain sensitive career details and should be reviewed before sharing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
