## Description: <br>
Autonomous CRM for freelancers that tracks clients, detects follow-up opportunities, generates proposals, tracks invoices, and sends a weekly digest via WhatsApp Bridge or the official WhatsApp Business API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omermalix](https://clawhub.ai/user/omermalix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External freelancers use this agent skill to manage client records, follow-ups, invoices, proposals, and weekly CRM summaries through local files and WhatsApp messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local client records and WhatsApp configuration may include sensitive contact, invoice, and credential data. <br>
Mitigation: Protect config.json and clients.json, keep generated local data out of version control, and restrict filesystem access to the skill folder. <br>
Risk: Configured WhatsApp integrations can send messages to clients after approval. <br>
Mitigation: Review recipient numbers and message text before approving any send, especially for follow-up and invoice reminders. <br>
Risk: Setup installs Python dependencies and configures messaging behavior on the local machine. <br>
Mitigation: Run setup in a controlled environment and review generated configuration before using scheduled or messaging features. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omermalix/freelancer-crm) <br>
- [Publisher profile](https://clawhub.ai/user/omermalix) <br>
- [Meta WhatsApp Business API messages endpoint](https://graph.facebook.com/v18.0/{phone_id}/messages) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and Markdown responses with CLI commands, generated proposal text, CRM summaries, and WhatsApp message drafts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local client records and may send WhatsApp messages after user approval when configured.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
