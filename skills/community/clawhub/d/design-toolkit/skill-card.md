## Description:

自适应设计偏好引擎 helps an agent observe design choices, feedback, and revisions to maintain reusable visual-preference guidance for UI, graphic, video, and print work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External designers, developers, and teams use this skill during design workflows to capture repeated visual-preference signals and apply the resulting profile to later design guidance. The artifact excludes 3D modeling, animation production, design-tool control, automatic rendering, and brand-asset-management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad read, write, and exec tool access.

Mitigation: Review and constrain tool permissions before installation, especially exec and write access, to the minimum needed for the design-preference workflow.

Risk: The skill maintains a continuing profile of user design preferences without clear storage, retention, or deletion controls.

Mitigation: Define where preference data is stored, who can access it, how long it is retained, and how users can inspect or delete it before using the skill on sensitive work.

Risk: The artifact includes callback and API-key behavior that may affect privacy or credential exposure if left unconstrained.

Mitigation: Clarify allowed callback destinations and environment-variable handling, and avoid confidential client or brand work until those controls are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/design-toolkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with compact JSON-style preference records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preference records are maintained as concise design rules; storage, retention, deletion, callback behavior, and execution permissions should be reviewed before deployment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
