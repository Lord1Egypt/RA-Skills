## Description: <br>
Manages Volcano Engine SMS workflows, including sending messages and querying sub-accounts, signatures, templates, send logs, and delivery statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users use this skill to send verification, notification, or marketing SMS messages through Volcano Engine and to inspect approved sending resources, delivery logs, and aggregate send statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send SMS messages to real recipients, which can create cost, privacy, and abuse risk. <br>
Mitigation: Require explicit user confirmation for every recipient, template, message purpose, and send action before execution. <br>
Risk: Phone numbers, template parameters, and message metadata are sent to an external SMS provider. <br>
Mitigation: Limit message content and recipient data to what is necessary, and avoid using the skill for sensitive or unapproved personal data. <br>
Risk: The skill depends on environment-provided API credentials and API base URL. <br>
Mitigation: Restrict access to ARK_SKILL_API_KEY and ARK_SKILL_API_BASE, do not print or share .env files, and verify the API destination before use. <br>


## Reference(s): <br>
- [Volcano Engine SMS documentation](https://www.volcengine.com/docs/6361/66704?lang=zh) <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-sms-sender) <br>
- [setup-guide.md](references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ARK_SKILL_API_KEY and ARK_SKILL_API_BASE to call Volcano Engine SMS endpoints; SMS send actions can affect real recipients and costs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter states 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
