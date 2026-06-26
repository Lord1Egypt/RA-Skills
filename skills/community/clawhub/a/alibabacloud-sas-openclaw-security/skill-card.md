## Description: <br>
Performs OpenClaw security operations by using the aliyun CLI to query Alibaba Cloud Security Center and ECS APIs for assets, vulnerabilities, baselines, alerts, guardrail status, remote command execution, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security operators, cloud administrators, and developers use this skill to inspect OpenClaw deployments, review vulnerabilities, baseline findings, and alerts, trigger checks, install or verify guardrails, run approved ECS Cloud Assistant commands, and generate security reports. <br>

### Deployment Geography for Use: <br>
Global, with Security Center and AI Security Center operations limited by the skill documentation to cn-shanghai and ap-southeast-1. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute powerful remote commands on ECS instances through Cloud Assistant. <br>
Mitigation: Use a tightly scoped RAM role, restrict ECS RunCommand permissions to intended instances, review the full command, and obtain explicit operator confirmation before execution. <br>
Risk: Generated output may contain sensitive host inventory, vulnerability data, alerts, and command results. <br>
Mitigation: Run the skill only in a controlled operator environment and treat the output directory as sensitive. <br>
Risk: The skill requires Alibaba Cloud credentials and cloud-service permissions. <br>
Mitigation: Use aliyun CLI credential configuration, avoid hard-coded access keys, and grant only the documented minimum RAM actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-sas-openclaw-security) <br>
- [Security Operations Workflow](artifact/references/security_workflow.md) <br>
- [RAM Permission Policies](artifact/references/ram-policies.md) <br>
- [Remediation and Product Recommendations](artifact/references/remediation_guide.md) <br>
- [Security Center RAM Authentication](https://help.aliyun.com/zh/security-center/developer-reference/api-authentication-rules) <br>
- [ECS RAM Authentication](https://help.aliyun.com/zh/ecs/developer-reference/authentication-rules-for-ecs-api) <br>
- [RAM Custom Policies](https://help.aliyun.com/zh/ram/user-guide/create-a-custom-policy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [CLI output, JSON files, Markdown reports, and human-facing operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Query results and reports are saved under output/; command output may include sensitive host inventory, vulnerabilities, alerts, and remote execution results.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
