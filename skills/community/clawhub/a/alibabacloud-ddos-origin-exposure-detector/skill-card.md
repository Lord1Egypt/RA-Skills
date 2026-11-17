## Description:

Detects whether websites protected by Alibaba Cloud Anti-DDoS Proxy still expose origin server IPs through public DNS resolution or direct public reachability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud security engineers, and support teams use this skill to check Alibaba Cloud Anti-DDoS Proxy configurations for origin exposure and produce a binary exposure verdict with recommended remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an existing Aliyun profile and may inspect cloud configuration or run probes against origin IPs.

Mitigation: Use least-privilege RAM or temporary credentials, confirm all parameters before execution, and avoid pasting access keys into commands or chat.

Risk: CloudMonitor one-off site monitor probes may incur pay-as-you-go costs.

Mitigation: Disclose the cloud probe method and cost before running, let the user choose local probing when appropriate, and review probe scope before creating tasks.

Risk: The skill asks the agent to modify local Aliyun CLI/plugin setup.

Mitigation: Review CLI installation, upgrade, and plugin update steps manually before allowing changes to the local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-ddos-origin-exposure-detector)
- [RAM policies](references/ram-policies.md)
- [Related CLI commands](references/related-commands.md)
- [Verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [Aliyun CLI installation guide](references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with inline shell commands and structured evidence tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also produce supporting JSON evidence and action logs in the session output directory.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
