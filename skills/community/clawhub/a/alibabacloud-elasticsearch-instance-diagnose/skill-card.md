## Description: <br>
Alibaba Cloud Elasticsearch instance diagnosis skill for cluster health checks, troubleshooting, and performance analysis on Elasticsearch instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and cloud operations teams use this skill to diagnose Alibaba Cloud Elasticsearch incidents by combining Alibaba Cloud OpenAPI, CloudMonitor metrics, Elasticsearch REST API evidence, and scenario SOPs into a root-cause report with remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses high-impact Alibaba Cloud and Elasticsearch credentials during diagnosis. <br>
Mitigation: Use scoped or short-lived credentials where possible, configure them locally, and avoid pasting secrets into chat, command lines, logs, or shell history. <br>
Risk: The security evidence flags destructive operational commands and remediation examples that may include DELETE, PUT, or POST actions. <br>
Mitigation: Treat remediation as manual change-control guidance requiring backups, exact target review, and explicit approval before execution. <br>
Risk: The skill is best treated as an expert-assisted runbook rather than an automatic repair tool. <br>
Mitigation: Have an operator review diagnosis evidence and proposed actions before making production changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-elasticsearch-instance-diagnose) <br>
- [Reference index](references/README.md) <br>
- [Verification method](references/verification-method.md) <br>
- [Report template](references/report-template.md) <br>
- [Elasticsearch API diagnosis strategy](references/es-api-diagnosis-strategy.md) <br>
- [Elasticsearch API call failures](references/es-api-call-failures.md) <br>
- [Elasticsearch API catalog](references/es-api-catalog.md) <br>
- [Health events catalog](references/health-events-catalog.md) <br>
- [RAM policies](references/ram-policies.md) <br>
- [Aliyun CLI installation guide](references/cli-installation-guide.md) <br>
- [Alibaba Cloud Elasticsearch CLI center](https://api.aliyun.com/api-tools/cli/elasticsearch/2017-06-13) <br>
- [Alibaba CloudMonitor CLI center](https://api.aliyun.com/api-tools/cli/Cms/2019-01-01) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with shell command snippets and structured diagnostic findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include an evidence chain, prioritized remediation guidance, and a recency-ordered incident timeline.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
