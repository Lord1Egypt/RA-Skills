## Description:

Turns raw changes, commits, or PRs into Keep a Changelog-style release notes grouped by change type, with breaking changes and upgrade notes surfaced first.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and release maintainers use this skill to turn raw commits, PRs, or change lists into concise changelog entries and release notes for a defined version, date, and audience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated changelog entries may misstate user impact, breaking changes, or migration steps.

Mitigation: Review generated release notes for accuracy before publishing, with extra attention to breaking changes, upgrade notes, and semver rationale.

Risk: Raw commit logs or PR lists may include internal-only details that should not appear in public release notes.

Mitigation: Check that the final changelog translates raw changes into user-facing outcomes and omits internal-only refactors, CI details, or technical noise.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/changelog-writer)
- [Changelog Writer homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/changelog-writer.html)
- [Keep a Changelog](https://keepachangelog.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown changelog or release notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grouped change sections with empty sections omitted, breaking changes and upgrade notes surfaced first, and semver rationale when inferred.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
