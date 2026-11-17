## Description:

Helps developers plan and manage Alibaba Cloud infrastructure, including ROS and Terraform templates, resource changes, cost estimates, and stack operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to design, generate, review, and validate Alibaba Cloud infrastructure templates, estimate costs, and manage approved cloud resources and ROS stacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud operations may use Alibaba Cloud credentials and change infrastructure.

Mitigation: Review each permission and deployment prompt, and grant only the RAM actions required for the approved task.

Risk: The downloaded local runtime may inherit unrelated secrets from its shell environment.

Mitigation: Use a shell environment without unrelated secrets and run only the verified runtime.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-iac-code)
- [Alibaba Cloud RAM permissions guidance](references/ram-policies.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with generated ROS or Terraform templates when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cloud actions require explicit user approval; results can include plans, cost estimates, progress, and actionable errors.]

## Skill Version(s):

0.5.0 (source: release metadata, references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
