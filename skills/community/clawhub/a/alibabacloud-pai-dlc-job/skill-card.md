## Description: <br>
Alibaba Cloud PAI-DLC job management skill for distributed training job CRUD, logs and events monitoring, and GPU sanity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML engineers use this skill to operate Alibaba Cloud PAI-DLC training jobs through the Aliyun CLI, including resource discovery, job creation, status inspection, logs and events, updates, stops, and GPU sanity checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates Alibaba Cloud PAI-DLC jobs through configured Aliyun CLI credentials. <br>
Mitigation: Use a dedicated RAM user or role with the narrowest required permissions, and avoid root or broad administrator credentials. <br>
Risk: Job stop, web-terminal URL generation, sharing-token generation, plugin installation, and persistent CLI configuration changes can affect running workloads or expose access paths. <br>
Mitigation: Review and confirm these operations before execution, pre-check job status for stop/update actions, and share generated URLs or tokens only through trusted channels. <br>
Risk: Creating or continuing training jobs can incur Alibaba Cloud compute charges. <br>
Mitigation: Confirm resource choices before creation, use appropriate quotas or ECS specs, and set running-time limits for long experiments when available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-pai-dlc-job) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Job Lifecycle Management](references/job-management.md) <br>
- [PAI-DLC RAM Permission Policies](references/ram-policies.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [Verification Method](references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON policy snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should use confirmed Alibaba Cloud regions, workspace and job identifiers, scoped RAM permissions, and the required user-agent flag.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
