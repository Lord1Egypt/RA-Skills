## Description:

Automates BUYMA order processing for regular daily runs and ad hoc order-range runs, including memo checks, CSV parsing, workbook creation, history enrichment, mail delivery, and Telegram failure notification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[innoucon-blip](https://clawhub.ai/user/innoucon-blip)

### License/Terms of Use:

MIT-0

## Use Case:

External operators use this skill to prepare BUYMA order workbooks for daily deadlines or requested order-number ranges. It helps an agent select a base workbook, process BUYMA CSV data, enrich rows from prior workbook history, validate outputs, and coordinate Naver Mail or Telegram notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad browser and session access for BUYMA and Naver Mail.

Mitigation: Use a dedicated Chrome profile only for BUYMA and Naver Mail, and review browser actions before execution.

Risk: The workflow can edit receipt memos and send order workbooks or attachments externally.

Mitigation: Require operator confirmation before memo edits or email/Telegram sends, and verify recipients and attachment paths.

Risk: Generated spreadsheets may contain untrusted cell values from BUYMA CSV data or manual fallback files.

Mitigation: Sanitize spreadsheet cells against formulas and validate generated workbooks before delivery.

Risk: Generated workbooks, logs, and state files may retain order information after processing.

Mitigation: Define retention and cleanup rules for generated workbooks, logs, CSV files, and state files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/innoucon-blip/skills/buyma-order-automation)
- [Workflow](references/workflow.md)
- [Run Modes](references/run-modes.md)
- [Failure Rules](references/failure-rules.md)
- [File Rules](references/file-rules.md)
- [Memo Rules](references/memo-rules.md)
- [Column Mapping](references/column-mapping.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python script commands and generated JSON/XLSX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates order workbooks, normalized JSON records, validation output, and last_state.json; browser-only BUYMA, Naver Mail, and Telegram actions are procedural.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
