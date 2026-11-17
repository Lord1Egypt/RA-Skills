## Description:

Guides agents to rewrite code comments into concise Chinese comments focused on intent, risk, and non-obvious behavior while preserving executable code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhongm](https://clawhub.ai/user/yhongm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to standardize comments during code writing, modification, review, refactoring, and explanation tasks. It is intended to remove obvious or verbose comments, rewrite useful comments in concise Chinese, and avoid changes to executable logic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is broadly scoped and may affect unrelated coding tasks by enforcing Chinese-only comment output.

Mitigation: Enable it only for repositories or tasks where Chinese comment normalization is desired, and avoid broad activation for review, explanation, security analysis, or multilingual projects.

Risk: Comment rewriting can remove wording that carries project-specific context or compliance requirements.

Mitigation: Review proposed comment changes before applying them, especially in codebases with required comment language or preserved legal, safety, or audit wording.

## Reference(s):


## Skill Output:

**Output Type(s):** [code, markdown, guidance]

**Output Format:** [Markdown code blocks containing complete source files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs the agent to output only the rewritten complete file without explanatory text.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
