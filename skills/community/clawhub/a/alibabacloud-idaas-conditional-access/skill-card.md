## Description:

Helps agents audit, preview, and manage conditional access policies for a specified Alibaba Cloud IDaaS instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and identity administrators use this skill to plan, review, and manage IDaaS conditional access policies, including application, network, and MFA requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags a potentially high impact policy activation flaw and says part of a script could not be fully inspected.

Mitigation: Review and address the activation issue and inspect the incomplete portion before use; verify the resulting policy state and settings after any confirmed change.

## Reference(s):

- [API reference](artifact/references/api.md)
- [Scenario templates](artifact/references/scenarios.md)
- [RAM permissions and policy operations](artifact/references/ram-policies.md)
- [ClawHub release page](https://clawhub.ai/sdk-team/skills/alibabacloud-idaas-conditional-access)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Configuration, Shell commands, JSON]

**Output Format:** [Markdown summaries, JSON plans and results, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Policy changes require user confirmation and are followed by read-back verification.]

## Skill Version(s):

0.0.1-beta.1 (source: release metadata, references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
