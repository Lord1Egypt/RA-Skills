## Description:

查询企业的中标履历和公开业绩，生成附公告来源的企业背调或双公司对比报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

企业采购、投标和尽调人员可核查一家公司的中标业绩、客户与竞争格局、公开风险，或对比两家公司，并追溯报告中的公告来源。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials stored in local configuration may be exposed if the file or conversation is shared.

Mitigation: Restrict access to the local configuration file and do not include the API key in messages or reports.

Risk: Shareable reports may contain contact details or signed links that grant access without login.

Mitigation: Review reports and recipients before sharing; treat contact details and signed links as sensitive.

Risk: Automatic account registration and paid API queries can affect privacy or consume account credits.

Mitigation: Obtain consent before registration, disclose estimated credit use, and confirm the data handling is acceptable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhiliaobiaoxun/skills/bid-winner-company-profile)
- [知了标讯 Skill 文档](https://ai.zhiliaobiaoxun.com/docs/skill)
- [Report template](references/report-template.md)
- [Query workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML]

**Output Format:** [Markdown report in chat with an optional shareable HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-company or two-company reports with source announcement links and stated data coverage.]

## Skill Version(s):

1.0.6 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
