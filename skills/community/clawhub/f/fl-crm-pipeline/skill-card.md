## Description:

Manage sales pipelines through natural language: add leads, update stages, log interactions, set reminders, and generate pipeline reports without full CRM software.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipstark](https://clawhub.ai/user/philipstark)

### License/Terms of Use:

MIT-0

## Use Case:

Solo founders, small sales teams, and freelancers use this skill to maintain a local CRM pipeline from chat. It helps track leads, reminders, interactions, deal stages, pipeline reports, and revenue forecasts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CRM records may contain prospect, contact, and revenue information stored in local plaintext JSON files.

Mitigation: Keep the data directory out of public repositories, shared backups, and other locations where unauthorized users can read it.

Risk: Natural-language CRM updates can modify deal stages, values, reminders, and notes incorrectly if the request is ambiguous.

Mitigation: Review the assistant's confirmations carefully before relying on pipeline records or reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/philipstark/skills/fl-crm-pipeline)
- [Publisher profile](https://clawhub.ai/user/philipstark)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, files, guidance]

**Output Format:** [Markdown responses plus local JSON CRM records and optional CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains pipeline data in local plaintext JSON files and may create backups or exports.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
