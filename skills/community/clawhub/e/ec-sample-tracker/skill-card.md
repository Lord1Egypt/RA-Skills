## Description:

Track and manage electrochemistry samples from synthesis to characterization with data linking, event logging, search, export, and dashboard visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xrayxiaoruiyang-pixel](https://clawhub.ai/user/xrayxiaoruiyang-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and lab staff use this skill to manage electrochemistry sample records, attach characterization data, log experimental events, search inventory, export reports, and generate dashboard summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk imports can permanently change the local SQLite sample database, including replacing records when sample_id values collide.

Mitigation: Back up samples.db before imports, inspect incoming sample_id values, and test imports on a copy before using them on lab records.

Risk: CSV exports may create spreadsheet files that are risky to open when records include untrusted values.

Mitigation: Prefer JSON or Markdown exports for untrusted data, or review CSV content before opening it in spreadsheet software.

Risk: Dashboard generation depends on optional plotting packages installed in the local Python environment.

Mitigation: Install optional dashboard dependencies only from trusted, pinned package sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xrayxiaoruiyang-pixel/skills/ec-sample-tracker)
- [Publisher Profile](https://clawhub.ai/user/xrayxiaoruiyang-pixel)
- [Artifact Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown or plain text with shell commands and file paths; exported records may be CSV, JSON, Markdown, SQLite, or PNG dashboard files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local outputs can include samples.db, exported sample reports, and sample-dashboard.png.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
