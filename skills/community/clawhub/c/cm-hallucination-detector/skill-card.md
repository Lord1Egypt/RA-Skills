## Description:

Detect and flag hallucinations in LLM outputs by cross-referencing claims against source documents, code, and verifiable data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI application teams, and content reviewers use this skill to check LLM-generated documentation, summaries, release notes, API references, code comments, and RAG outputs against available source material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read project documents, source files, and git metadata while checking factual claims.

Mitigation: Use it only in repositories and document sets the agent is authorized to review, and avoid providing sensitive material that is not needed for the accuracy check.

Risk: Incomplete source material can leave claims uncertain or unverifiable.

Mitigation: Require human review for uncertain or unverifiable findings before publishing or relying on generated content.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown analysis report with claim classifications, confidence scores, evidence notes, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested verification commands and human-review notes for uncertain or unverifiable claims.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
