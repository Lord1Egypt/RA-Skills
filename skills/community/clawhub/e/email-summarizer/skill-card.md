## Description:

Fetches emails from an IMAP mailbox or local exports, builds contact profile reports as HTML and Excel files, and can send the report by email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[momothemage](https://clawhub.ai/user/momothemage)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to summarize mailbox contents, analyze contact relationships, and generate shareable contact profile reports from IMAP mailboxes or exported email archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes private mailbox contents and writes generated JSON, HTML, and XLSX reports that may contain sensitive email data.

Mitigation: Run it in a restricted workspace, fetch only the needed mailbox scope, and treat all generated report files as sensitive.

Risk: IMAP and SMTP workflows require mailbox credentials.

Mitigation: Use least-privilege app passwords and avoid hardcoding or sharing credentials.

Risk: Reports can be sent by email, which may expose sensitive results to unintended recipients.

Mitigation: Verify recipient addresses and report contents before sending.

Risk: Generated spreadsheets from untrusted mailbox content may expose spreadsheet formula injection risk.

Mitigation: Do not open generated spreadsheets from untrusted mailboxes unless formulas are neutralized or the output is reviewed first.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands; generated JSON, HTML, and XLSX report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local email exports or mailbox credentials as inputs and can send reports by SMTP when configured.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
