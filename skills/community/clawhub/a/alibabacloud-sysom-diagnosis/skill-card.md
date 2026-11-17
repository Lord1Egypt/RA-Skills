## Description:

Troubleshoots Linux server performance and stability issues on Alibaba Cloud ECS by routing symptoms through SysOM CLI diagnostics and summarizing evidence-based recommendations without applying fixes automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and operations engineers use this skill to diagnose CPU, memory, IO, network, and Java runtime symptoms on Alibaba Cloud Linux ECS instances. It helps select appropriate SysOM commands, interpret returned findings, and present safe remediation targets.

### Deployment Geography for Use:

China Mainland and Hong Kong

## Known Risks and Mitigations:

Risk: The installer path pipes a remote shell script into a shell, including a system-wide sudo option.

Mitigation: Prefer downloading the installer first, verifying a published checksum or signature, inspecting it, and using the user-local install path instead of the sudo pipeline.

Risk: Remote SysOM diagnosis requires Alibaba Cloud credentials through AK/SK or an ECS RAM role.

Mitigation: Use least-privilege RAM permissions and keep credential setup outside the conversation; do not paste AccessKey IDs or secrets into chat.

Risk: Some Java profiling and collection steps can run for minutes and may add CPU, memory, or pause overhead to the target process.

Mitigation: Explain duration and expected impact before running these commands and wait for explicit user confirmation unless a standing approval exists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-sysom-diagnosis)
- [Supported Environments](references/supported-environments.md)
- [Deep Actions Reference](references/deep-actions.md)
- [Parameter Guide](references/parameter-guide.md)
- [Report Interpretation](references/report-interpretation.md)
- [RAM Policies](references/ram-policies.md)
- [Java Application Diagnosis Reference](references/java/README.md)
- [Memory Triage](references/memory-triage.md)
- [Non-Memory Triage](references/non-memory-triage.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with SysOM command snippets and summarized diagnosis findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not apply fixes automatically; long-running or higher-impact profiling follow-ups require user confirmation.]

## Skill Version(s):

0.0.7 (source: server release metadata and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
