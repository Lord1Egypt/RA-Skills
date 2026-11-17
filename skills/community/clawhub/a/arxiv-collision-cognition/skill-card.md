## Description:

Guides an agent to compare ArXiv papers against a project context from four reasoning angles and extract actionable research insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingofzhao](https://clawhub.ai/user/kingofzhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical teams use this skill to screen ArXiv papers, compare them with known and unknown project context, and turn promising overlaps into actionable insight queues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project context and collision logs may contain persistent or sensitive project knowledge.

Mitigation: Avoid entering secrets or sensitive business details in project_context, and periodically review stored collision_log entries and queued insights.

Risk: Research insights may be incorrect, low confidence, or unsuitable for direct knowledge base updates.

Mitigation: Use the documented confidence thresholds and human validation workflow before promoting insights into project knowledge.

Risk: Paper handling may raise copyright or data-sharing concerns if full text is sent to third-party services.

Mitigation: Follow the artifact's disclosed guardrail to block full-paper external requests and record the event for review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kingofzhao/skills/arxiv-collision-cognition)
- [Project Homepage](https://github.com/KingOfZhao/AGI_PROJECT)
- [Group-Evolving Agents](https://arxiv.org/abs/2602.04837)
- [A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046)
- [SAGE: Multi-Agent Self-Evolution for LLM Reasoning](https://arxiv.org/abs/2603.15255)
- [Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411)
- [Generating CAD Code with Vision-Language Models for 3D Designs](https://arxiv.org/abs/2410.05340)
- [From 2D CAD Drawings to 3D Parametric Models](https://arxiv.org/abs/2412.11892)
- [Efficient Vision-Language-Action Models for Embodied Manipulation](https://arxiv.org/abs/2510.17111)
- [Vlaser: Vision-Language-Action Model with Synergistic Embodied Reasoning](https://arxiv.org/abs/2510.11027)
- [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564)
- [Beyond RAG for Agent Memory](https://arxiv.org/abs/2602.02007)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and text guidance with Python and shell examples, plus JSON-style collision log records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce confidence-scored insight lists, local collision logs, and human review queues when executed by the host agent.]

## Skill Version(s):

1.1.0 (source: server release metadata, SKILL.md frontmatter, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
