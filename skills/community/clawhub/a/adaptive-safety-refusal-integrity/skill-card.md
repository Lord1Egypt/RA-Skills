## Description:

Tests whether an agent maintains safety refusals when harmful requests are disguised through role-play, linguistic variation, or persuasive framing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tzwwww](https://clawhub.ai/user/tzwwww)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and safety evaluators use this skill to create refusal-integrity test data for agents facing harmful requests hidden behind role-play, slang, technical framing, or authority-based pressure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and reuses disguised harmful prompts for refusal testing.

Mitigation: Install only in a controlled safety-evaluation environment and treat generated prompts, trajectories, and seed sets as sensitive red-team data.

Risk: Using broad private corpora or live web search during evaluation can increase exposure of sensitive or current-event risk material.

Mitigation: Connect only authorized data sources and web tools, with logging, review controls, and clear approval.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tzwwww/skills/adaptive-safety-refusal-integrity)
- [Environment Exploration Guide](artifact/references/EXPLORATION.md)
- [Trajectory Selection Criteria](artifact/references/SELECTION.md)
- [Data Synthesis Instructions](artifact/references/SYNTHESIS.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown guidance and JSON question-answer trajectories]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated data should include a question, refusal answer, and trajectory steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
