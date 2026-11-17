## Description:

Guides agents through Alibaba CloudMonitor monitoring, onboarding, diagnostics, metrics, and alerting with the aliyun cms2 CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations teams use this skill to manage and troubleshoot Alibaba Cloud monitoring integrations, telemetry, dashboards, and alerts through the aliyun CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitoring changes can create, modify, or delete cloud and Kubernetes resources without sufficiently scoped confirmation.

Mitigation: Use least-privilege credentials and require explicit confirmation of the target and action before every create, update, delete, or patch.

Risk: Unverified installer downloads or piped shell commands can execute untrusted code.

Mitigation: Independently verify the download source and checksum before running an installer; avoid curl-to-shell commands.

Risk: APM tokens and kubeconfig files can expose credentials if copied into chat or shared storage.

Mitigation: Keep tokens and kubeconfig out of chat logs and persistent shared paths.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-cms-manage)
- [Alibaba Cloud CLI installation](https://help.aliyun.com/document_detail/121541.html)
- [Monitoring integration guidance](references/integration-common.md)
- [Application performance monitoring guidance](references/apm.md)
- [Alerting guidance](references/alerting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Analysis]

**Output Format:** [Markdown with CLI commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires aliyun CLI 3.3.15 or newer and an appropriate Alibaba Cloud profile.]

## Skill Version(s):

1.0.6 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
