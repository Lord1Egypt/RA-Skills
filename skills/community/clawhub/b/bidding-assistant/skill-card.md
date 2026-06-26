## Description: <br>
Collects bidding and procurement notices for Yannan High-tech Zone and Yancheng Economic Development Zone, filters target-region projects, generates daily or monthly PDF reports, and can push reports to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xzc13815555922](https://clawhub.ai/user/xzc13815555922) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations staff and agents use this skill to monitor Yancheng-area bidding sources, collect and deduplicate matching projects, prepare PDF daily or monthly summaries, and deliver reports through Feishu when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended scheduled collection and delivery can send collected reports outside the local environment. <br>
Mitigation: Disable cron or scheduled Feishu delivery until the workflow is tested and approved for the target workspace. <br>
Risk: Feishu credentials and recipient identifiers can expose reports or enable unwanted messaging if mishandled. <br>
Mitigation: Use a dedicated least-privilege Feishu bot, store secrets in a protected secret store, and verify exact chat or user IDs before sending. <br>
Risk: Crawler behavior may interact with external sites in ways that require authorization or policy review. <br>
Mitigation: Confirm permission for the target sources and avoid proxy or anti-bot bypass behavior without authorization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xzc13815555922/bidding-assistant) <br>
- [PDF report generation and Feishu delivery guide](references/PDF报告生成与飞书推送使用指南.md) <br>
- [PDF report layout guide](references/PDF报告排版说明.md) <br>
- [PDF display optimization guide](references/PDF显示优化说明.md) <br>
- [Website configuration reference](references/website-config.md) <br>
- [Sufu workflow reference](references/sufu-workflow.md) <br>
- [OpenClaw browser relay guide](references/openclaw-browser-relay-guide.md) <br>
- [Feishu enterprise app configuration guide](references/飞书企业自建应用配置指南.md) <br>
- [Feishu delivery configuration guide](references/飞书推送配置说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash and Python snippets; PDF reports and Feishu messages when the bundled scripts are executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local SQLite and PDF files and may send collected reports externally when Feishu delivery is configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
