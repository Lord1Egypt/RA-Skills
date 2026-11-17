## Description:

Collects AI and automotive industry news from specified sources and organizes the results into a structured spreadsheet report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rouclaw](https://clawhub.ai/user/rouclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to gather current AI and automotive industry updates from vetted sources and produce structured Excel or CSV news reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional enhancement commands use unpinned `npx clawhub@latest` installs.

Mitigation: Verify the referenced packages and pin trusted versions before running optional enhancement installs.

Risk: The workflow creates a local spreadsheet or CSV report in the working directory.

Mitigation: Run it in an appropriate workspace and review generated report files before sharing or committing them.

Risk: Collected news summaries may affect reporting or business decisions if sources, dates, or cross-checks are wrong.

Mitigation: Review the generated table against the skill's source-quality, date, and cross-verification checklist before relying on the report.

## Reference(s):

- [AI Content Collection Channels Reference](artifact/references/channels.md)
- [ClawHub Skill Page](https://clawhub.ai/rouclaw/skills/ai-content-collector)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown text table plus Excel (.xlsx) or CSV report file; may include Python and shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local dated report file in the working directory when executed.]

## Skill Version(s):

1.10.1 (source: release.version; changelog: v1.10.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
