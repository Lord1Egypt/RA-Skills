## Description: <br>
Fapiao Clipper helps an agent scan email and local folders for Chinese invoices, extract invoice data with local PDF text and vision-OCR workflows, verify risk signals, query stored records, and export reimbursement packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alan5168](https://clawhub.ai/user/alan5168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, finance staff, and agent operators use this skill to collect Chinese invoice attachments or files, organize recognized invoice records, review reimbursement risks, and produce export files for expense workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can log in to a configured mailbox and download invoice attachments and links from messages. <br>
Mitigation: Use a dedicated mailbox or narrowly scoped folder, review the email configuration before scanning, and disable email scanning when it is not needed. <br>
Risk: Automatic link following may fetch invoice-like URLs from email bodies. <br>
Mitigation: Set automatic email-link following to false unless the mailbox source is trusted, and review downloaded files before reimbursement use. <br>
Risk: Configuration may contain mailbox or API credentials and local invoice records may contain sensitive business data. <br>
Mitigation: Keep config.yaml and the invoice database in a restricted local directory, avoid committing them to source control, and limit access to exported files. <br>
Risk: The Web UI can expose invoice data if made reachable beyond localhost without access controls. <br>
Mitigation: Keep the Web UI bound to local or trusted private networks and add access controls before any broader exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alan5168/fapiao-clipper) <br>
- [Publisher profile](https://clawhub.ai/user/alan5168) <br>
- [Project homepage](https://github.com/Alan5168/fapiao-clipper) <br>
- [Issue tracker](https://github.com/Alan5168/fapiao-clipper/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI text summaries; generated Excel and PDF export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local SQLite invoice database, downloaded invoice files, and reimbursement exports under user-configured folders.] <br>

## Skill Version(s): <br>
1.5.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
