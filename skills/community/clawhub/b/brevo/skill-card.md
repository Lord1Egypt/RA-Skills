## Description: <br>
Brevo (formerly Sendinblue) email marketing API for managing contacts, lists, sending transactional emails, and campaigns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yujesyoga](https://clawhub.ai/user/yujesyoga) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to work with Brevo API workflows for contact management, list updates, transactional email sending, campaign setup, and email automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill can send emails from the user's Brevo account. <br>
Mitigation: Use a least-privilege Brevo API key when available, keep the key out of chat and logs, and manually review recipients and message content before any send action. <br>
Risk: Using the skill can modify contact records, lists, imports, deletions, and unsubscribe handling. <br>
Mitigation: Review list IDs, contact payloads, import settings, deletion actions, and unsubscribe or blacklist handling before allowing write operations. <br>


## Reference(s): <br>
- [Brevo API base URL](https://api.brevo.com/v3) <br>
- [ClawHub skill page](https://clawhub.ai/yujesyoga/brevo) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Brevo API endpoints, request payloads, curl commands, Python examples, and operational guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
