## Description:

Redrafts unclear or risky contract clauses into clearer, more balanced alternatives for drafting review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to improve contract clause wording by identifying ambiguity or imbalance, generating balanced, protective, and plain-language alternatives, and explaining the changes. The skill provides drafting assistance only and does not replace review by qualified counsel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs may be mistaken for legal advice or final contract language.

Mitigation: Treat redrafts as drafting suggestions and have important clauses reviewed by qualified counsel before use.

Risk: Highly sensitive contract text may be exposed to the runtime handling the prompt.

Mitigation: Avoid submitting confidential clauses unless the runtime and data handling are trusted.

Risk: A broad trigger may activate this skill for non-contract editing prompts.

Mitigation: Confirm the request involves contract language before applying legal drafting patterns.

## Reference(s):

- [Clause Redraft Templates](references/redraft-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/clause-redraft)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style drafting analysis with identified issues, alternative clauses, recommendations, and legal disclaimer text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces suggested alternatives only; outputs require legal review before use in binding agreements.]

## Skill Version(s):

1.0.0 (source: server release evidence, clawhub.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
