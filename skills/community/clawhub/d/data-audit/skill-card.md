## Description:

Data Audit helps agents generate SHA256 directory snapshots, compare file changes, record local audit logs, validate data-directory health, and export JSON or CSV reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cqdev-ai](https://clawhub.ai/user/cqdev-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and compliance reviewers use this skill to prepare audit evidence by tracking file integrity, comparing data-directory changes, recording local operation history, and checking directory health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated snapshots, reports, and log history can expose local paths, filenames, hashes, and metadata.

Mitigation: Store generated audit artifacts and ~/.data-audit-logs with appropriate local access controls and share them only with intended reviewers.

Risk: CSV exports are not hardened against spreadsheet-formula injection.

Mitigation: Avoid opening CSV exports from untrusted directories or untrusted snapshot files in spreadsheet software until formula sanitization is added.

Risk: The manifest understates write behavior.

Mitigation: Review installation permissions with the expectation that the skill can write local audit history and user-selected report or export files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cqdev-ai/skills/data-audit)
- [README.md](artifact/README.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands, plus JSON or CSV report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include retained local audit logs, directory paths, filenames, hashes, metadata, and generated report files.]

## Skill Version(s):

1.1.0 (source: release evidence, package.json, CHANGELOG, and script constant)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
