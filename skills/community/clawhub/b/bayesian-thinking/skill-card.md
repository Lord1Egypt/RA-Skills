## Description:

Applies Bayesian thinking to help an agent update beliefs from priors to posteriors based on new evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanikua](https://clawhub.ai/user/wanikua)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to structure uncertain decisions by defining hypotheses, setting priors, weighing evidence, estimating posteriors, and deciding whether to act or gather more information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce probability estimates that sound more certain than the available evidence supports, especially in high-stakes domains.

Mitigation: Treat estimates as structured judgment and require qualified expert review before relying on them for medical, legal, financial, safety-critical, or similarly consequential decisions.

Risk: Poor priors, incomplete alternatives, or dependent evidence can lead to misleading posterior estimates.

Mitigation: Ask the agent to state assumptions, include alternative hypotheses, identify evidence quality, and describe what new evidence would materially change the conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanikua/skills/bayesian-thinking)
- [Publisher profile](https://clawhub.ai/user/wanikua)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with structured reasoning steps and optional probability estimates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reasoning scaffolds only; it does not execute tools, request credentials, or modify files.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
