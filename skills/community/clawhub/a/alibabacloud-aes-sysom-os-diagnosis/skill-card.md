## Description: <br>
Perform SysOM deep OS-level diagnosis on Alibaba Cloud ECS instances to identify root causes of performance issues, with optional instance enrollment and DingTalk alert notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operations engineers and developers use this skill to confirm Alibaba Cloud ECS instance details, run SysOM diagnosis, review root causes and suggestions, and optionally enroll instances or clusters for continuous monitoring and DingTalk alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make lasting Alibaba Cloud and instance changes, including SysOM initialization, agent enrollment, alert destinations, alert strategies, and local CLI or SDK setup. <br>
Mitigation: Use explicit user confirmation for target instances, clusters, alert selections, and webhook setup; plan cleanup for installed agents, alert destinations, alert strategies, and local SDK changes. <br>
Risk: The skill requires sensitive Alibaba Cloud credentials and may handle DingTalk webhook URLs. <br>
Mitigation: Use a least-privilege RAM role or profile, never expose AccessKey values in conversation or command output, and treat DingTalk webhook URLs as secrets. <br>
Risk: Incorrect target selection can enroll or monitor the wrong ECS instance or ACK cluster. <br>
Mitigation: Verify every region, instance ID, cluster ID, and resolved cluster name with the user before running diagnosis, enrollment, or alert configuration commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sdk-team/alibabacloud-aes-sysom-os-diagnosis) <br>
- [Diagnosis Execution Detailed Workflow](references/diagnose-workflow.md) <br>
- [Enrollment and Alert Detailed Workflow](references/manage-and-alert-workflow.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related Commands](references/related-commands.md) <br>
- [Success Verification](references/verification-method.md) <br>
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include parsed SysOM diagnosis summaries, root causes, suggestions, enrollment steps, and alert configuration guidance.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
