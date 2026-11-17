## Description:

Conducts rigorous, adversarial code reviews that identify security issues, edge cases, bad practices, and quality problems across Python, R, JavaScript/TypeScript, SQL, and front-end code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[corbin-breton](https://clawhub.ai/user/corbin-breton)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to request direct PR or code review feedback, prioritize findings by severity, and receive actionable recommendations before merging changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional cross-model review can increase model usage, latency, and cost.

Mitigation: Use --dual only when deeper scrutiny is worth the additional time and spend, and audit each second-reviewer finding before accepting it.

Risk: The deliberately direct review posture can overstate low-confidence findings if context is incomplete.

Mitigation: Keep findings tied to concrete file locations and failure modes, and mark uncertain concerns as verification items rather than blocking defects.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/corbin-breton/skills/adversarial-code-reviewer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown review with severity tiers and actionable recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional --dual mode can perform cross-model iterative review with added cost and latency.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
