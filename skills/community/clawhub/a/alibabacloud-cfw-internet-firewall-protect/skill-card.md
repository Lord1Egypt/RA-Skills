## Description:

Helps administer Alibaba Cloud Firewall public IP protection, including asset status queries, scoped or account-wide protection changes, and auto-protection settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and operations engineers use this skill to inspect public IP protection, change firewall switches for selected assets or accounts, and configure protection for newly discovered resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scoped disable operations can remove protection from many public IPs without a script-enforced confirmation gate.

Mitigation: Review the affected assets and exact scope before execution; prefer explicit IP lists or tightly combined filters over a region, resource type, or IP version alone.

Risk: Firewall administration grants the agent authority to change cloud protection settings.

Mitigation: Use least-privilege or temporary cloud credentials, and install or upgrade Aliyun CLI through a trusted package path.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-cfw-internet-firewall-protect)
- [Resource types](references/resource-types.md)
- [RAM permissions](references/ram-policies.md)
- [Aliyun CLI installation guide](references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with shell commands and JSON status results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can export asset protection status as CSV.]

## Skill Version(s):

0.0.2 (source: ClawHub release and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
