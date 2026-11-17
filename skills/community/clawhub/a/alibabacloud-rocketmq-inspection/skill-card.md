## Description: <br>
Read-only batch health inspection for Alibaba Cloud RocketMQ instances (4.x classic and 5.x serverless), using CMS metrics and management APIs through the Aliyun CLI to produce a scored Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect Alibaba Cloud RocketMQ health, consumer lag, backlog, throttling, DLQ growth, and quota usage across one or more instances. It supports main inspection reports and focused single-consumer-group diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes the local Aliyun CLI plugin environment through automatic plugin installation and updates. <br>
Mitigation: Run it in a dedicated shell, container, or workstation profile; review Aliyun CLI installer and plugin updates before use. <br>
Risk: Cloud credentials with write or wildcard permissions would increase blast radius if commands are changed or misused. <br>
Mitigation: Use read-only RAM permissions for CMS, ONS, RocketMQ, and STS, and avoid granting write or wildcard cloud permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-rocketmq-inspection) <br>
- [RocketMQ metrics catalogue](artifact/references/metrics.md) <br>
- [RAM policies required](artifact/references/ram-policies.md) <br>
- [Thresholds and health score algorithm](artifact/references/thresholds.md) <br>
- [Aliyun CLI pitfalls](artifact/references/cli-pitfalls.md) <br>
- [Alibaba Cloud RocketMQ 4.x limits](https://help.aliyun.com/zh/apsaramq-for-rocketmq/cloud-message-queue-rocketmq-4-x-series/product-overview/limits) <br>
- [Alibaba Cloud RocketMQ 5.x usage limits](https://help.aliyun.com/zh/apsaramq-for-rocketmq/cloud-message-queue-rocketmq-5-x-series/product-overview/usage-limits) <br>
- [Aliyun CLI configuration documentation](https://help.aliyun.com/document_detail/121258.html) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with supporting shell commands and YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes report files in the current directory, temporary JSON under /tmp, and a user threshold file on first run.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
