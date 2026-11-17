## Description:

Correction Logger records and manages user corrections, agent errors, and improvement suggestions with priority, effectiveness feedback, and full-text search while preserving the existing Markdown correction format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whoisme007](https://clawhub.ai/user/whoisme007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to persist correction history, retrieve relevant prior corrections before actions, and inspect correction health or effectiveness during agent operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Correction records may include sensitive prompts, credentials, private customer data, or other context that becomes persistent memory.

Mitigation: Avoid logging sensitive data; add redaction, access controls, retention limits, deletion tooling, and approval rules before allowing records to influence future agent behavior.

Risk: Correction history is stored on disk and may outlive a single agent session.

Mitigation: Keep correction files, databases, archives, and logs in access-controlled locations and review retention requirements before commercial use.

## Reference(s):

- [Correction Logger ClawHub release page](https://clawhub.ai/whoisme007/skills/correction-logger)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown correction records, command-line text, Python dictionaries, and YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists correction history locally and can return recent corrections, pre-action matches, statistics, and health-check results.]

## Skill Version(s):

2.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
