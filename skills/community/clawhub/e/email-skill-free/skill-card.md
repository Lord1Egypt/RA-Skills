## Description: <br>
邮件技能免费版 helps agents send basic SMTP email with plain-text bodies, one attachment, Gmail or Outlook presets, and test-message validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and personal automation users can use this skill to configure an agent for simple notification emails, test SMTP credentials, and send a single report attachment through Gmail or Outlook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SMTP passwords may be stored in a local configuration file. <br>
Mitigation: Protect the configuration file with appropriate permissions, keep it out of version control, and prefer dedicated app passwords rather than account passwords. <br>
Risk: The skill can send email and attachments to external recipients. <br>
Mitigation: Review recipient, subject, body, and attachment paths before sending, and use the test-message flow to validate setup before production messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/email-skill-free) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON configuration examples and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides SMTP configuration, test sending, plain-text email sending, and single-attachment workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
