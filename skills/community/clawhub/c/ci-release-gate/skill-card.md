## Description:

CI release engineer skill for validation gating, release-readiness checks, and automation-safe delivery criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to assess CI gates, release readiness, validation evidence, and automation-safe delivery criteria before merge or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for an automatic release approval authority.

Mitigation: Treat its output as release-readiness guidance that still requires review by the responsible maintainers.

Risk: The skill depends on repository CI, test, release, and Weline collaboration documents that may be incomplete or outdated.

Mitigation: Confirm referenced project documents and validation evidence are current before relying on the release recommendation.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with a release-gate recommendation, satisfied and missing checks, blockers, risks, and follow-up actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output; it should not be treated as automatic release authority.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
