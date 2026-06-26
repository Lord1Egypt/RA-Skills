## Description: <br>
DiePre Embodied Bridge connects 2D vision and DXF detection to 3D spatial understanding and robot action planning through a vision-action-evolution loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingofzhao](https://clawhub.ai/user/kingofzhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to reason about converting 2D dieline or DXF inputs for known packaging geometries into 3D coordinates, fold sequences, grasp points, and quality checks. It also describes a feedback loop for logging failures and updating future robot-action parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Self-updating parameters may affect future robot actions without clear user controls. <br>
Mitigation: Require manual approval before evolved parameters influence robot actions, and provide a clear way to inspect, reset, or disable the evolution state. <br>
Risk: Automatic logging may store task details and failure records in uncontrolled locations. <br>
Mitigation: Keep logs in a controlled location and review the implementation before using the skill with real equipment. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/kingofzhao/diepre-embodied-bridge) <br>
- [Project Homepage](https://github.com/KingOfZhao/AGI_PROJECT) <br>
- [From 2D CAD to 3D Parametric via VLM](https://arxiv.org/abs/2412.11892) <br>
- [Vlaser: Synergistic Embodied Reasoning](https://arxiv.org/abs/2510.11027) <br>
- [Efficient VLA Models](https://arxiv.org/abs/2510.17111) <br>
- [SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255) <br>
- [Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell examples plus structured tool and parameter schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes robot-planning outputs such as 3D coordinates, fold sequences, grasp points, quality scores, failure logs, and evolved parameter files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
