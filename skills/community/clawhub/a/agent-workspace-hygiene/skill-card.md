## Description:

This skill helps agents inventory generated workspace artifacts and plan dry-run cleanup, review, or recoverable archiving inside a coding repo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollis9087](https://clawhub.ai/user/hollis9087)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill when a user explicitly asks to inventory, review, archive, or delete generated workspace artifacts without touching source changes or sensitive files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup reports can expose local project paths, filenames, and generated artifact names.

Mitigation: Treat reports as potentially sensitive and avoid sharing them outside the intended workspace context.

Risk: Archive or deletion actions could remove useful generated outputs if paths are approved without review.

Mitigation: Review the proposed paths before approving changes, prefer recoverable archive, and keep tracked changes, data, databases, credentials, and secret-looking files protected or review-required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hollis9087/skills/agent-workspace-hygiene)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or Markdown cleanup reports with optional shell commands and JSON inventory summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only inventory by default; archive or deletion actions require explicit user confirmation.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
