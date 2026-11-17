## Description:

自动采集盐南高新区、经开区招投标信息，并支持区域筛选、去重存储、PDF日报/月报生成和飞书推送。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xzc13815555922](https://clawhub.ai/user/xzc13815555922)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to monitor Jiangsu Yancheng bidding sources for Yannan High-tech Zone and Economic Development Zone projects, run collection jobs, store deduplicated results locally, generate daily or monthly PDF reports, and send reports to Feishu.

### Deployment Geography for Use:

China, focused on Yancheng, Jiangsu bidding sources

## Known Risks and Mitigations:

Risk: Automated Feishu delivery can share bidding reports with unintended groups or users.

Mitigation: Review all Feishu destination IDs and permissions before running or scheduling report pushes.

Risk: Feishu credentials and webhook URLs can be exposed through shell startup files, committed .env files, or shared configuration.

Mitigation: Store secrets only in approved local or managed secret stores and keep them out of source control and shell profiles.

Risk: Scheduled jobs can repeatedly scrape sites, generate files, and push reports without operator review.

Mitigation: Disable scheduled execution by default and enable it only after confirming collection scope, recipients, and retention needs.

Risk: Browser Relay deployment can expose browser-control capability if left unauthenticated or reachable from untrusted networks.

Mitigation: Deploy Browser Relay only when required, pin the image or package, require authentication, and bind it to a trusted interface.

Risk: The skill stores scraped bidding data locally, which can create data retention and access-control concerns.

Mitigation: Confirm that the listed bidding sources may be collected for the intended use and apply local access controls and retention rules to the SQLite database and generated PDFs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xzc13815555922/skills/bidding-assistant)
- [Publisher profile](https://clawhub.ai/user/xzc13815555922)
- [Website configuration](references/website-config.md)
- [PDF report generation and Feishu push guide](references/PDF报告生成与飞书推送使用指南.md)
- [Feishu enterprise app configuration guide](references/飞书企业自建应用配置指南.md)
- [Feishu push configuration](references/飞书推送配置说明.md)
- [OpenClaw Browser Relay configuration guide](references/openclaw-browser-relay-guide.md)
- [Sufu interactive collection workflow](references/sufu-workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python snippets; bundled scripts can create PDF report files, local SQLite records, and Feishu messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on configured bidding sites, local database paths, Feishu credentials, and optional scheduling.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
