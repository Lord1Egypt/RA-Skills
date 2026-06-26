## Description: <br>
Invoice tracker: track sent invoices, flag overdue payments, draft follow-up reminders, weekly on a cron or on demand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ceobotson-bot](https://clawhub.ai/user/ceobotson-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business owners, finance operators, and agents use this skill to review invoice data, identify overdue payments, prepare invoice digests, and draft reminder messages for approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice sources and digests may expose sensitive business, client, payment, or revenue information. <br>
Mitigation: Use only approved invoice sources and private, least-privilege delivery channels for digests and reports. <br>
Risk: Payment reminders could be sent to the wrong recipient or sent before the user reviews the draft. <br>
Mitigation: Keep reminder sending approval-based and verify recipients before any email or chat delivery. <br>
Risk: A recurring schedule may continue checking or delivering invoice data after it is no longer needed. <br>
Mitigation: Disable the recurring schedule when the workflow is no longer required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ceobotson-bot/doctorclaw-invoice-tracker) <br>
- [DoctorClaw Website](https://www.doctorclaw.ceo) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance, Configuration] <br>
**Output Format:** [Markdown invoice digest with drafted reminder text and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reminder messages are drafts for user approval before sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
