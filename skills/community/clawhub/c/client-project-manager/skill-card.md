## Description: <br>
Manage freelance clients, projects, invoices, and communications. Use when tracking client work, creating invoices, sending updates, managing deadlines, or organizing freelance business operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanwyngaard](https://clawhub.ai/user/seanwyngaard) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Freelancers and small service teams use this skill to manage client records, project status, time entries, invoices, payment reminders, and weekly client updates from local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent local files containing client, billing, invoice, and payment details. <br>
Mitigation: Install it only in a private workspace and keep freelance-data out of shared folders and source control. <br>
Risk: Generated invoices, payment reminders, and weekly updates may be sent to clients. <br>
Mitigation: Review all generated business communications before sending them. <br>
Risk: Payment configuration can include sensitive financial details. <br>
Mitigation: Avoid storing raw bank details in config.json unless the local file is appropriately protected. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-backed local files, with generated invoice and client-update text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local freelance-data JSON records plus Markdown and HTML invoice files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
