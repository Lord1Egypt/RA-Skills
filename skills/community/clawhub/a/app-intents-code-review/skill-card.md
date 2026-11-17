## Description:

Reviews App Intents code for intent structure, entities, shortcuts, and parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill to review Swift App Intents implementations for intent structure, AppEntity queries, Shortcuts discovery, parameters, and platform-specific pitfalls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a neighboring review-verification-protocol skill that is outside this artifact.

Mitigation: Before using the skill, confirm that the referenced protocol skill is present, trusted, versioned, and cannot silently override or suppress review findings.

Risk: Incorrect or stale review guidance could lead to false positives, missed App Intents defects, or misleading code-review feedback.

Mitigation: Apply the skill's hard gates for every finding, including current file and line evidence, full surrounding type review, and concrete platform or integration artifacts for version-dependent claims.

## Reference(s):

- [Intent Structure](references/intent-structure.md)
- [Entities and Queries](references/entities.md)
- [Shortcuts Integration](references/shortcuts.md)
- [Parameters](references/parameters.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown review findings with file and line references, or concise review questions when evidence is insufficient]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are expected to use the [FILE:LINE] ISSUE_TITLE format and pass the skill's pre-reporting gates.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
