## Description:

DiePre Embodied Bridge maps 2D packaging dieline detections into 3D geometry, fold sequences, grasp points, and quality estimates for robotics planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingofzhao](https://clawhub.ai/user/kingofzhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to bridge 2D carton dieline or CAD detections into structured 3D coordinates, folding plans, grasp parameters, and quality checks for packaging automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic persistent tuning of robot action parameters could change grasp force, fold sequence, or approach angle without clear safety bounds or operator approval.

Mitigation: Require strict schema validation, trusted log writers, immutable safety limits, simulation or operator approval before activation, and rollback before use in a robotics workflow.

Risk: Evolution logs and updated parameter files may retain operational data or alter future behavior in ways that are hard to audit.

Mitigation: Define data retention rules, access controls, audit trails, and review gates for evolution_log entries and evolved parameter files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingofzhao/skills/diepre-embodied-bridge)
- [Project homepage](https://github.com/KingOfZhao/AGI_PROJECT)
- [From 2D CAD to 3D Parametric via VLM](https://arxiv.org/abs/2412.11892)
- [Tool-Augmented VLLMs as Generic CAD Task Solvers](https://arxiv.org/)
- [Vlaser: Synergistic Embodied Reasoning](https://arxiv.org/abs/2510.11027)
- [Efficient VLA Models](https://arxiv.org/abs/2510.17111)
- [SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255)
- [Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks and structured examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe tool schemas, generated action-planning outputs, and persistent parameter update files.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
