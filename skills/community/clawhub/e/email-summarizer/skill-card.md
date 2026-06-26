## Description: <br>
Fetches emails from IMAP or local exports (.pst, .mbox, .msg), builds HTML and Excel contact profile reports, and can send the report by email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[momothemage](https://clawhub.ai/user/momothemage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to fetch or parse mailbox content, summarize important messages, profile email contacts, and create shareable contact reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive mailbox contents and local email archives. <br>
Mitigation: Use app-specific email passwords, limit date ranges and max counts, and keep generated JSON, HTML, and XLSX reports private. <br>
Risk: The optional SMTP delivery step can disclose reports to the wrong recipient. <br>
Mitigation: Review the generated report and verify the recipient address before running the send step. <br>
Risk: Local export parsing may invoke local Node.js or readpst executables for PST files. <br>
Mitigation: Install parsing dependencies from trusted sources and run the parser only on email exports the user intends to analyze. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/momothemage/email-summarizer) <br>
- [Skill documentation](SKILL.md) <br>
- [Python dependency manifest](requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands; generated artifacts include JSON email data, HTML reports, Excel workbooks, and optional email messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses EMAIL_USER and EMAIL_PASS only for IMAP fetch and SMTP send workflows; local file parsing does not require credentials.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
