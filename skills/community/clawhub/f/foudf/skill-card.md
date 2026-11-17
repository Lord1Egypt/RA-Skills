## Description:

Provides a five-operator framework for analyzing complex decisions across systems, layers, probabilities, constraints, and strategic interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kings0527](https://clawhub.ai/user/kings0527)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to structure multi-variable, high-uncertainty decisions in domains such as technology, business, policy, education, relationships, and health. It guides the agent to examine topology, explanatory layers, probability distributions, hard constraints, and game interactions before giving conditional recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad trigger can make answers more formal or framework-driven than a simple question requires.

Mitigation: Use the framework for complex decisions with multiple variables, uncertainty, or tradeoffs; ask the agent for a concise answer or to skip the framework for simple requests.

Risk: The framework asks for probability weights and base rates, which can lead to overconfident estimates when reliable data is unavailable.

Mitigation: Require the agent to label low-confidence estimates, use qualitative ranges when data is weak, and separate evidence-backed probabilities from assumptions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kings0527/skills/foudf)
- [Source skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis with structured lists, tables, scenario branches, and conditional recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include system topology descriptions, layer maps, probability tables, constraint lists, game-structure analysis, monitoring indicators, and alternatives.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
