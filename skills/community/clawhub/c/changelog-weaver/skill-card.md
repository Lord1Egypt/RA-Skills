## Description:

Generate polished changelogs and release notes from git history, PRs, and issues, with automatic categorization for features, fixes, and breaking changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to turn repository change history into changelogs, release notes, team announcements, and CI-friendly changelog JSON. It is most useful when a project follows or can be mapped to Conventional Commits and needs human-reviewed release communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commit messages, PR titles, issue text, or AI rewrites may contain misleading wording, injected links, headings, or instructions that end up in generated release notes.

Mitigation: Review generated changelogs and release notes before publishing, and treat repository text supplied to an AI assistant as untrusted input.

Risk: The local helper script reads repository commit history and writes output files chosen by the user.

Mitigation: Run it only in repositories whose metadata may be processed for release documentation, and confirm output paths before writing changelog artifacts.

Risk: Private repository metadata can be exposed if changelog JSON is pasted into a tool-enabled chat without a clear data boundary.

Mitigation: Redact sensitive commits, issue links, and private identifiers before sharing with an AI assistant, or keep the processing local when confidentiality is required.

## Reference(s):

- [Changelog Weaver on ClawHub](https://clawhub.ai/harrylabsj/skills/changelog-weaver)
- [Conventional Commits Reference](references/conventional-commits.md)
- [Output Format Specifications](references/output-formats.md)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, JSON, and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated changelog content should be reviewed before publication, especially when commit messages or AI rewrites influence the final wording.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
