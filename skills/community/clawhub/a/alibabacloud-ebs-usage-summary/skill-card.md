## Description:

Analyzes Alibaba Cloud EBS disk performance and fleet composition, helping agents summarize usage, identify IOPS or bandwidth bottlenecks, review disk events, and point users to relevant dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud infrastructure engineers and operations teams use this skill to inspect Alibaba Cloud EBS metrics, summarize disk inventory and events, and prepare read-only CLI commands and dashboard guidance for storage troubleshooting and capacity review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance can persistently change Aliyun CLI plugin behavior or local CLI state.

Mitigation: Require user confirmation before installation, plugin updates, or auto-plugin changes; prefer package-manager installation and review downloaded installers before execution.

Risk: The skill relies on an existing Alibaba Cloud profile, so an overly broad credential can expose more account data than the EBS reporting task needs.

Mitigation: Use a least-privilege RAM user or role limited to the read-only EBS and disk-resolution permissions listed in the skill references.

Risk: Access keys or secrets could be exposed if credential setup is handled inside an agent conversation or shell transcript.

Mitigation: Do not enter or echo AK/SK values in the agent session; verify credential status with safe CLI inspection and configure credentials outside the session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-ebs-usage-summary)
- [Alibaba Cloud EBS Data Insights documentation](https://help.aliyun.com/zh/ecs/user-guide/what-is-a-piece-of-data-is-stored-insight/)
- [RAM Policies for EBS Monitoring Skill](references/ram-policies.md)
- [EBS Monitoring CLI Commands Reference](references/related-commands.md)
- [Parameter Confirmation](references/parameter-confirmation.md)
- [Verification Methods for EBS Monitoring Skill](references/verification-method.md)
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md)
- [Error Handling Reference](references/error-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON-oriented summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include parameter checklists, verification steps, and dashboard URLs; does not itself execute cloud changes.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
