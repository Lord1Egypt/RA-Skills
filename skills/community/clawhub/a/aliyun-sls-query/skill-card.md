## Description: <br>
Queries Alibaba Cloud Log Service (SLS) logs through the aliyunlog CLI for a specified project, logstore, time range, and optional query or SQL analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yunr-tg](https://clawhub.ai/user/yunr-tg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent assemble Aliyun SLS log query commands for bounded projects, logstores, time ranges, and SQL-style log analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aliyun cloud credentials may be exposed if long-lived AccessKey secrets are pasted into generated commands. <br>
Mitigation: Use least-privilege RAM users or temporary STS credentials, and prefer configured profiles or environment-based credentials over command-line secrets. <br>
Risk: Overbroad log queries may return excessive or sensitive operational data. <br>
Mitigation: Restrict Project, Logstore, time range, query, and result size values before executing generated commands. <br>
Risk: Returned log text can contain untrusted or sensitive data. <br>
Mitigation: Treat log output as untrusted data and review it before reuse in prompts, reports, or follow-up commands. <br>


## Reference(s): <br>
- [ClawHub listing: 阿里云SLS日志查询](https://clawhub.ai/yunr-tg/aliyun-sls-query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON result expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include aliyunlog command templates, credential setup guidance, query parameters, and returned log interpretation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
