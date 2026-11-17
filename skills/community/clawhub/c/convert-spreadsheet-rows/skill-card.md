## Description:

Converts spreadsheet rows into structured task objects for Jira, Markdown, or JSON formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users use this skill to convert spreadsheet or CSV task rows into structured Jira, Markdown, or JSON task outputs while preserving field mapping and validation warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the documentation asks for an unspecified API key.

Mitigation: Do not provide API keys unless the publisher documents the exact service and data flow; prefer local CSV parsing without secrets when possible.

Risk: Markdown or Jira output generated from untrusted spreadsheets may be manipulated before import.

Mitigation: Prefer JSON output for reviewable structure, or inspect generated Markdown and Jira text before importing it into another system.

Risk: The security verdict is suspicious because the documentation overstates capabilities compared with the simple local conversion behavior.

Mitigation: Review the skill before installing and validate generated task data against the destination workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/convert-spreadsheet-rows)
- [Metadata source: MiniMax-AI skills](https://github.com/MiniMax-AI/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown tables, JSON task objects, Jira-style task text, or written output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Consumes local CSV rows with Python standard library parsing; generated Markdown or Jira text should be inspected before import.]

## Skill Version(s):

1.0.1 (source: release metadata and CHANGELOG, released 2026-05-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
