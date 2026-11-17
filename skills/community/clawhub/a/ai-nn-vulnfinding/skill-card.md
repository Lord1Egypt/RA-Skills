## Description:

Analyzes textual descriptions of neural network architectures for structural weaknesses that may increase adversarial attack risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3mper0rr](https://clawhub.ai/user/3mper0rr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, ML engineers, and security reviewers use this skill to assess architecture descriptions for adversarial-robustness concerns and practical hardening actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the conceptual robustness review for a full security audit or empirical adversarial evaluation.

Mitigation: Use the skill as triage guidance and validate important conclusions with model testing, threat modeling, and human security review.

Risk: Incomplete architecture descriptions can lead to missing or overstated findings.

Mitigation: Provide preprocessing, activation, regularization, training, and defense details when requesting analysis, and review the output before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/3mper0rr/skills/ai-nn-vulnfinding)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown response following a fixed assessment schema]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conceptual architecture analysis only; no code output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
