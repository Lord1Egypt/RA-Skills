## Description:

Exports WorkBuddy conversation history into JSON, Markdown, and TXT files with timelines, metadata, statistics, milestones, and skill usage records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xf4vul](https://clawhub.ai/user/0xf4vul)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and WorkBuddy users use this skill to export local conversation history for archiving, review, analysis, and sharing. It supports date ranges, event filters, output detail controls, and optional file attachment listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exports may include persistent WorkBuddy memory, project metadata, automation-task information, and skill usage records.

Mitigation: Specify the exact date range, sources, output format, and destination before exporting, then review generated files for secrets or private information before sharing.

Risk: The security summary notes broad local reads and history file writes without clear source-by-source consent or concrete redaction rules.

Mitigation: Use only in workspaces where the user has approved the source scope, and manually verify that sensitive content has been removed from the export.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xf4vul/skills/conversation-exporter)
- [Publisher profile](https://clawhub.ai/user/0xf4vul)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [JSON, Markdown, and UTF-8 text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WorkBuddy memory, project metadata, automation-task information, and skill usage records; users can choose date range, filters, detail level, and destination.]

## Skill Version(s):

1.0.0 (source: server release metadata, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
