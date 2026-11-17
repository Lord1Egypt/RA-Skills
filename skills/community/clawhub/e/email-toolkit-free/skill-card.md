## Description: <br>
Email Toolkit Free helps agents configure and send text or HTML email with attachments through common SMTP providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and small teams use this skill to set up SMTP credentials, send plain-text or HTML email, include CC/BCC recipients, and attach files from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email and attachments through the user's SMTP account. <br>
Mitigation: Manually verify recipients, subject, body text, and attachments before allowing any send command. <br>
Risk: SMTP credentials may be exposed if stored in a local configuration file or committed to version control. <br>
Mitigation: Use an app password or dedicated email account, prefer environment variables where practical, and keep email_config.json out of version control. <br>


## Reference(s): <br>
- [Email Toolkit Free on ClawHub](https://clawhub.ai/thcjp/skills/email-toolkit-free) <br>
- [Google Account security settings](https://myaccount.google.com/security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, Python, and text examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce email-send status text and setup guidance for SMTP configuration, recipients, message bodies, and attachments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
