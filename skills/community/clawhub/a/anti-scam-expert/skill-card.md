## Description:

Anti Scam Expert helps agents analyze suspicious opportunities, investments, projects, collaborations, products, or services by comparing user-described scenarios against historical and modern scam patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gao322759](https://clawhub.ai/user/gao322759)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents can use this skill to assess whether a described opportunity, transaction, or relationship shows scam indicators. It produces a risk rating, red-flag analysis, comparable cases, reasoning, and suggested next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may trigger on broad credibility or trustworthiness questions and provide scam-analysis framing even when the situation is ambiguous.

Mitigation: Use the output as decision-support guidance and ask the agent or a human reviewer to separate evidence-backed red flags from uncertain assumptions.

Risk: The skill is Chinese-language and may respond in Chinese unless the hosting agent adapts the output language.

Mitigation: Configure the agent to translate or localize the response when serving users who need another language.

## Reference(s):

- [Historical Scam Reference Library](references/history.md)
- [Modern Scam Reference Library](references/modern.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with structured risk rating, red flags, comparable cases, rationale, and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primarily Chinese-language scam-pattern analysis; no executable code or tool calls are produced by the skill itself.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
