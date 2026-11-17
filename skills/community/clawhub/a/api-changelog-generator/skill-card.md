## Description:

Generate and maintain API changelogs from OpenAPI/Swagger specs - track endpoints added, removed, deprecated, or modified between versions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API documentation teams use this skill to compare OpenAPI or Swagger specifications, identify breaking and non-breaking changes, and draft consumer-facing changelogs, release notes, and migration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The diff command can run unintended local code when given a crafted file path.

Mitigation: Review and fix the diff command to pass file paths through argv or another data-only channel before using it with untrusted filenames or specifications.

Risk: Breaking-change output may be incomplete for authentication changes, nested schemas, and $ref-heavy specifications.

Mitigation: Treat the output as a review aid and verify important API compatibility decisions against the source specifications and client impact analysis.

## Reference(s):

- [API Changelog Generator on ClawHub](https://clawhub.ai/charlie-morrison/skills/api-changelog-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, text, JSON, RSS or Atom snippets, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update API-CHANGELOG.md and may scan local source files for affected API calls when requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
