## Description:

Adaptive Reasoning Plus helps agents score task complexity and choose an appropriate response depth, from quick execution through structured extended reasoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsangho](https://clawhub.ai/user/tsangho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to make task handling more adaptive by scoring complexity, ambiguity, impact, and irreversible actions before selecting a reasoning posture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The file-deletion example can encourage fast handling of a destructive action.

Mitigation: Correct the example so file deletion and other irreversible actions require path validation, impact review, and explicit user confirmation before execution.

## Reference(s):

- [Domain Scoring Reference](references/domain-scoring.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown or text guidance with optional structured complexity labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a visible complexity score and selected reasoning strategy for higher-complexity tasks.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
