## Description:

Generate a Cartesian verification artifact before trusting a plan, claim, implementation, or release. Turn confidence into explicit checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[malleus35](https://clawhub.ai/user/malleus35)

### License/Terms of Use:

MIT-0

## Use Case:

Teams, reviewers, and developers use this skill to turn plans, claims, implementations, or releases into classified claims, doubt categories, verification actions, and a release posture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce doubts that are too abstract to guide action.

Mitigation: Require each serious doubt to map to a concrete verification action before completion.

Risk: The skill may slow or block decisions if used as general disagreement instead of evidence-based review.

Mitigation: Use the claim classification and release posture sections to separate facts, inferences, preferences, and guesses, then name the conditions needed to proceed.

Risk: High-consequence claims may be accepted without enough supporting evidence.

Mitigation: Escalate when key claims cannot be verified with currently available evidence or when release pressure overrides clarity.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/malleus35/skills/agora-doubt-list)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Analysis]

**Output Format:** [Markdown checklist with claim classifications, doubts, verification actions, clarity gate, and release posture.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No tool execution; output is a review artifact for human verification.]

## Skill Version(s):

2.2.0 (source: server release metadata; artifact frontmatter: 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
