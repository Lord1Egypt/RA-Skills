## Description: <br>
Automates BUYMA order processing for daily and ad hoc order-range runs, including memo checks, CSV or fallback input, Tmazon workbook generation, history enrichment, Naver Mail delivery, and Telegram failure notification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[innoucon-blip](https://clawhub.ai/user/innoucon-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and automation maintainers use this skill to prepare BUYMA order workbooks for regular daily processing or requested order-number ranges, then send the result through Naver Mail with Telegram notification on completion or failure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to operate in logged-in BUYMA and Naver Mail browser sessions. <br>
Mitigation: Use a dedicated browser profile where possible, confirm the active account before each run, and keep browser-only steps as procedural placeholders until they are implemented and tested. <br>
Risk: Order workbooks may be sent by email or Telegram without enough recipient or channel controls. <br>
Mitigation: Require manual confirmation before any email or Telegram send, verify recipients and channels, and avoid attaching sensitive files unless necessary. <br>
Risk: Failure handling can attach generated order files to Telegram. <br>
Mitigation: Confirm file scope before sending fallback attachments and limit attachments to the minimum output needed to resolve the failed run. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Run Modes](references/run-modes.md) <br>
- [Failure Rules](references/failure-rules.md) <br>
- [File Rules](references/file-rules.md) <br>
- [Memo Rules](references/memo-rules.md) <br>
- [Column Mapping](references/column-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated workbook, JSON, and state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates order workbooks, normalized JSON records, state JSON, logs, and notification text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
