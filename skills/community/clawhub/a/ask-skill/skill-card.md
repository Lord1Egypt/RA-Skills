## Description:

Ask is a Chinese-language structured questioning and deep analysis workflow that narrows ambiguous judgments into confidence-scored conclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gloryjack](https://clawhub.ai/user/gloryjack)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Ask to analyze ambiguous judgments, forecasts, or comparisons by triaging question depth, asking targeted follow-ups, checking evidence, and producing a direct conclusion with uncertainty and risk notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store recurring critique memory in /workspace/ask-memory.db, which may retain sensitive context across sessions.

Mitigation: Avoid sensitive personal or business judgments unless local memory is acceptable, cleared, or disabled before use.

Risk: The skill may use web search and a critic subagent for analysis, which can expose prompts or intermediate reasoning to external or separate agent workflows.

Mitigation: Review inputs before use and avoid including confidential information in searches or subagent tasks.

Risk: Prediction workflows may use Monte Carlo simulation and evidence scoring that can produce overconfident or misleading decisions if inputs are weak.

Mitigation: Treat forecasts as decision support, verify input data quality, and review stated uncertainty and risk notes before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gloryjack/skills/ask-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style structured analysis with scoring, uncertainty labels, conclusions, and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Monte Carlo simulation summaries for prediction tasks and critic findings for research-style analysis.]

## Skill Version(s):

6.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
