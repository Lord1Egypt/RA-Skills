## Description: <br>
Generates Markdown email templates for welcome, newsletter, transactional, cold outreach, follow-up, and collection email scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, sales, support, and operations users use this skill to generate editable email templates, subject-line variants, and compliance reminders for common customer communications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security verdict is suspicious because an unrelated command script persists user arguments locally without clear disclosure. <br>
Mitigation: Review scripts before installation, use scripts/emailtpl.sh for email-template generation, and avoid passing secrets, private business text, or personal data to scripts/script.sh unless the publisher clarifies or removes that behavior. <br>
Risk: Generated marketing and outreach emails may require legal or policy review before sending. <br>
Mitigation: Check each template for required unsubscribe links, sender address, monitored reply-to address, and applicable CAN-SPAM or GDPR obligations before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/email-template) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown email templates with subject-line variants, placeholders, compliance checklist items, and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Templates may include placeholder variables such as {{first_name}}, {{company_name}}, and {{product_name}}.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
