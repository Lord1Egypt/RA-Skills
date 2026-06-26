## Description: <br>
Manage the full lifecycle of Alibaba Cloud EMR Serverless StarRocks instances, including creation, scaling, configuration, maintenance, and diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SREs, operations engineers, and architects use this skill to manage Alibaba Cloud EMR Serverless StarRocks instances through guided aliyun CLI workflows. It supports instance creation, status checks, scaling, configuration changes, restarts, and diagnostics, but not SQL authoring, data import/export, query tuning, or non-StarRocks products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact cloud provisioning and management actions that may affect cost, availability, or configuration. <br>
Mitigation: Review proposed actions before execution, require confirmation for paid resource creation and restart, scale, or configuration changes, and use least-privilege Alibaba Cloud RAM roles. <br>
Risk: Prompts, commands, logs, or shared documentation could expose access keys, passwords, or other operational secrets. <br>
Mitigation: Do not paste real passwords or access keys into prompts or logs; source secrets securely and mask sensitive values in outputs. <br>


## Reference(s): <br>
- [API Parameter Reference](references/api-reference.md) <br>
- [Quick Start: Create Your First StarRocks Instance from Scratch](references/getting-started.md) <br>
- [Instance Full Lifecycle: Plan to Create to Manage](references/instance-lifecycle.md) <br>
- [Daily Operations: Configuration, Maintenance, SSL, Billing, Gateway](references/operations.md) <br>
- [RAM Permission Policy Reference](references/ram-policies.md) <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-emr-starrocks-manage) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are intended for Alibaba Cloud CLI environments with configured credentials and appropriate RAM permissions.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
