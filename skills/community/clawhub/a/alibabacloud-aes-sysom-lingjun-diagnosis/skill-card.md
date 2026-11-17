## Description:

Performs SysOM deep OS-level diagnosis on Alibaba Cloud lingjun nodes to identify root causes of performance issues and optionally configure DingTalk alert notifications for diagnosis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operations engineers and SREs use this skill to diagnose Alibaba Cloud lingjun node performance problems such as CPU spikes, memory leaks, IO latency, and kernel-level issues. It can also guide SysOM-based DingTalk alert destination and alert strategy setup after diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use existing Alibaba Cloud credentials and proceed without a separate confirmation checkpoint once required inputs are available.

Mitigation: Install and run it only with a least-privilege RAM profile scoped to the documented SysOM and ECS actions.

Risk: The skill can modify local Aliyun CLI/plugin settings and initialize SysOM authorization.

Mitigation: Review the workflow before use and run it in an environment where changes to local CLI configuration and SysOM authorization are acceptable.

Risk: The alert workflow can create SysOM alert destinations and strategies connected to DingTalk.

Mitigation: Provide a DingTalk webhook only when alerting is intended, and remove created alert destinations or strategies from the SysOM console when no longer needed.

Risk: The security summary notes that diagnosis is partly described as read-only even though SysOM and alert setup can change cloud state.

Mitigation: Treat SysOM initialization and alert configuration as state-changing operations and audit them separately from diagnosis result retrieval.

## Reference(s):

- [Diagnosis Execution Detailed Workflow](references/diagnose-workflow.md)
- [Alert Configuration Detailed Workflow](references/alert-workflow.md)
- [RAM Policies](references/ram-policies.md)
- [Related Commands](references/related-commands.md)
- [Success Verification](references/verification-method.md)
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md)
- [Acceptance Criteria](references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnosis status, task IDs, inferred time windows, SysOM result summaries, and DingTalk alert setup results.]

## Skill Version(s):

0.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
