## Description:

Helps developers plan, review, validate, and refine Alibaba Cloud infrastructure with ROS Agent, including guided choices and approved deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use ROS Agent to plan and compare Alibaba Cloud architectures, review and validate infrastructure, and guide approved deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials authorize ROS Agent requests and potentially consequential infrastructure workflows.

Mitigation: Use a minimal RAM policy for ROS StartChat and StopChat, and approve deployments only after checking the plan, costs, region, and architecture.

Risk: CLI plugin installation changes local tooling; remote CLI execution may expose more environment data to workers than expected.

Mitigation: Prefer the default code transport or a trusted local CLI; use remote CLI only with a trusted executor and environment handling, and review plugin installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-ros-agent)
- [ROS RAM permissions](references/ram-policies.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration, Shell commands]

**Output Format:** [Markdown with diagrams and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include candidate architectures, estimated costs, deployment summaries, and infrastructure artifacts.]

## Skill Version(s):

0.4.0 (source: ClawHub release metadata and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
