## Description:

Perform Alibaba Cloud NIS (Network Intelligence Service) network path reachability analysis with forward and reverse path diagnosis, topology visualization, and resource monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud network engineers use this skill to diagnose Alibaba Cloud connectivity issues, confirm bidirectional reachability, inspect security group or route-table causes, visualize topology, and query monitoring data for resources on the analyzed path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary flags unsafe cloud-credential guidance in the setup material.

Mitigation: Use least-privilege RAM roles or temporary credentials, keep access keys out of agent sessions and command lines, and verify credential setup outside the conversation.

Risk: The server security summary says the read-only framing understates that NIS analysis tasks are created.

Mitigation: Confirm with the user before starting each analysis task, and check whether NIS tasks persist, appear in audit logs, or count against quotas.

Risk: The server security guidance flags privileged or unverified CLI installation paths.

Mitigation: Prefer a trusted package manager or a verified pinned CLI download before enabling automatic plugin installation.

## Reference(s):

- [RAM Policies](references/ram-policies.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md)
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/)
- [Aliyun CLI plugin repository](https://github.com/aliyun/aliyun-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with CLI commands, parameter prompts, diagnostic summaries, and Mermaid topology diagrams.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Alibaba Cloud NIS and CloudMonitor command sequences plus topologyData.positive-derived Mermaid output.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
