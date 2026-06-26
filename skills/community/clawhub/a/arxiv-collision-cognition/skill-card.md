## Description: <br>
Helps agents compare ArXiv papers with project context through four-direction collision reasoning to extract actionable research insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingofzhao](https://clawhub.ai/user/kingofzhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to have an agent compare ArXiv papers against project context, separate known and unknown items, and turn intersections into actionable research or implementation insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated daily or heartbeat screening can fetch ArXiv data and write local research logs without close review. <br>
Mitigation: Enable scheduled screening deliberately, keep collision logs in a workspace you can inspect, and review queued insights before acting on them. <br>
Risk: Project context supplied to the skill may include confidential details that are stored in local logs or passed to downstream tools. <br>
Mitigation: Avoid supplying confidential project details unless the workspace and downstream tools are approved for that data. <br>
Risk: Paper-collision insights may be incomplete or misleading if treated as validated research conclusions. <br>
Mitigation: Use the human feedback and verification flow to mark insights as validated or disproven before relying on them. <br>


## Reference(s): <br>
- [ArXiv Collision Cognition on ClawHub](https://clawhub.ai/kingofzhao/arxiv-collision-cognition) <br>
- [Project homepage](https://github.com/KingOfZhao/AGI_PROJECT) <br>
- [Group-Evolving Agents](https://arxiv.org/abs/2602.04837) <br>
- [A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046) <br>
- [SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255) <br>
- [VLM for 3D CAD Code](https://arxiv.org/abs/2410.05340) <br>
- [2D to 3D Parametric via VLM](https://arxiv.org/abs/2412.11892) <br>
- [Efficient VLA Models](https://arxiv.org/abs/2510.17111) <br>
- [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564) <br>
- [Beyond RAG for Agent Memory](https://arxiv.org/abs/2602.02007) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and JSON-style collision logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces four-direction paper comparisons, confidence-labeled actionable insights, and local collision log entries.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, SKILL.md frontmatter, README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
