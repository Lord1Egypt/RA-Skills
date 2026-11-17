## Description:

DiePre Vision Cognition combines packaging and die-cut machine-vision inspection with SOUL-style reasoning to separate known features from uncertain regions, log inspections, and route low-confidence defects for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingofzhao](https://clawhub.ai/user/kingofzhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and manufacturing quality teams use this skill to analyze die-cut packaging images, track inspection confidence, and escalate uncertain defect decisions for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent QA logs and feedback data may contain sensitive production image paths, feature vectors, defect decisions, or human annotation notes.

Mitigation: Use the skill only in workspaces where persistent inspection logs are acceptable, and define retention, access-control, and deletion practices before deployment.

Risk: Low-confidence visual decisions can affect quality-control outcomes if they are treated as final decisions.

Mitigation: Route low-confidence findings to human review and use feedback loops to update labels or rules before relying on repeated automated decisions.

## Reference(s):

- [Project homepage](https://github.com/KingOfZhao/AGI_PROJECT)
- [Generating CAD Code with Vision-Language Models](https://arxiv.org/abs/2410.05340)
- [From 2D CAD to 3D Parametric via VLM](https://arxiv.org/abs/2412.11892)
- [Efficient Vision-Language-Action Models](https://arxiv.org/abs/2510.17111)
- [Vlaser: Synergistic Embodied Reasoning](https://arxiv.org/abs/2510.11027)
- [ClawHub skill page](https://clawhub.ai/kingofzhao/skills/diepre-vision-cognition)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe confidence scores, defect lists, collision logs, QA logs, and human-review flags.]

## Skill Version(s):

1.1.0 (source: frontmatter, release evidence, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
