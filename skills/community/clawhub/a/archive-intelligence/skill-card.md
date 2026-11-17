## Description:

定时获取档案行业最新情报、政策法规、技术动态和行业资讯。当用户需要获取档案行业新闻、政策更新、技术趋势或设置定时情报收集任务时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijie012](https://clawhub.ai/user/lijie012)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect, summarize, and periodically report archive-sector policy updates, industry news, technology trends, and academic research. It supports ad-hoc intelligence requests and configuration-driven recurring report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The examples encourage creating recurring Windows scheduled tasks or cron jobs, which can cause ongoing automatic execution.

Mitigation: Only create scheduled tasks after explicitly confirming the desired schedule, script path, config path, and removal procedure.

Risk: The bundled script is identified by server security guidance as syntactically broken and not actually collecting intelligence.

Mitigation: Review and test the script before use, and treat generated reports as templates unless collection behavior has been verified.

Risk: Archive-sector intelligence summaries may include stale, inaccurate, copyrighted, or sensitive information from external sources.

Mitigation: Prefer official sources, preserve links and publication dates, verify important claims, and avoid collecting or redistributing confidential material.

## Reference(s):

- [Skill page](https://clawhub.ai/lijie012/skills/archive-intelligence)
- [Publisher profile](https://clawhub.ai/user/lijie012)
- [State Archives Administration of China](https://www.saac.gov.cn)
- [Government policy database](https://www.gov.cn/zhengce/zhengceku/)
- [CNKI](https://www.cnki.net)
- [Wanfang Data](https://www.wanfangdata.com.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown reports, JSON configuration examples, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated Markdown reports to configured local output directories when the bundled script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
