## Description:

洞明 is a Chinese-language strategic analysis agent that uses a Rumelt-style diagnosis, guiding policy, and coherent action structure with hypothesis-driven validation and red-team critique.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to analyze strategy, markets, competition, business models, growth choices, market entry, portfolio questions, and strategy-aligned organization diagnosis. It helps produce judgment-first strategy reports with hypotheses, validation plans, coherent actions, and red-team review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Strategic recommendations may be incorrect, overconfident, or misleading when market, customer, financial, or organizational evidence is incomplete.

Mitigation: Specify the target market, time horizon, data sources, confidentiality expectations, and decision constraints; review the hypotheses, validation plan, and red-team record before relying on the recommendation.

Risk: The skill tends to prioritize China-market examples and may not fit other geographies without explicit direction.

Mitigation: State the intended geography and require region-specific evidence, comparable cases, and assumptions in the final report.

Risk: Optional expert routing can broaden analysis scope or expose sensitive business context to additional agent workflows.

Mitigation: Clarify whether expert delegation is allowed and limit shared context to the information needed for the selected analysis dimension.

## Reference(s):

- [Core Principles](references/core-principles.md)
- [Hypothesis-Driven Insight Generation](references/insight-generation.md)
- [Output Specification](references/output-spec.md)
- [Red-Team Protocol](references/red-team-protocol.md)
- [Expert Scheduling Protocol](references/scheduling-protocol.md)
- [ClawHub skill page](https://clawhub.ai/tuobadaidai/skills/dongming)
- [Publisher profile](https://clawhub.ai/user/tuobadaidai)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown strategy report with tables, Mermaid diagrams, validation plans, and red-team records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route complex questions to optional expert subskills; outputs should state assumptions, evidence needs, and residual strategic risks.]

## Skill Version(s):

2.1.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
