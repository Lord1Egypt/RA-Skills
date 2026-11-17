## Description:

Comprehensive code documentation skill that standardizes source headers, function comments, subsystem documentation, architecture docs, and API references for codebases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI coding agents use this skill to create, update, and audit code documentation after documentation requests, significant code changes, subsystem onboarding, or API changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated documentation can become incorrect or misleading if it is not checked against the current code.

Mitigation: Review generated headers and docs against live source files and complete the skill's documentation audit before committing.

Risk: The skill may remove existing comments while cleaning up prohibited or stale inline comment patterns.

Mitigation: Review comment deletions and retain concise comments that explain non-obvious behavior or design constraints.

Risk: Repo-wide documentation updates can touch many files and create a broad review surface.

Mitigation: Inspect diffs by subsystem and require normal code review before merging documentation changes.

## Reference(s):

- [Code Documentation skill page](https://clawhub.ai/encryptshawn/skills/code-documentation)
- [Architecture Document Template](artifact/references/architecture-doc.md)
- [Subsystem Documentation Template](artifact/references/subsystem-doc.md)
- [API Reference Template](artifact/references/api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown documentation and inline source-code comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update source-file headers, function comments, subsystem docs, architecture docs, API references, and documentation audit notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
