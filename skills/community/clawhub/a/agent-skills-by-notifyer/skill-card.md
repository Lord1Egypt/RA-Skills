## Description: <br>
Notifyer by WhatsAble helps an agent operate a Notifyer workspace for WhatsApp account setup, connection checks, team and recipient management, outbound messaging, templates, bots, broadcasts, webhooks, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whatsable](https://clawhub.ai/user/whatsable) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate Notifyer WhatsApp workflows, including account access, workspace administration, messaging, campaign scheduling, bot configuration, webhook integration, and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise broad Notifyer workspace authority, including team administration, API-key retrieval, conversation access, webhook changes, outbound messaging, and destructive broadcast or member operations. <br>
Mitigation: Run it only with an account scoped to the intended workspace tasks, review commands before execution, and require confirmation before destructive operations. <br>
Risk: Credentials and sensitive data may appear in environment variables, command arguments, API responses, message logs, phone numbers, and recipient CSV files. <br>
Mitigation: Use environment variables or secret storage for tokens, avoid passing passwords directly on the command line, and treat generated outputs and CSV files as sensitive. <br>
Risk: Outbound WhatsApp messages, templates, bots, webhooks, and broadcasts can affect customers, external recipients, subscriptions, or compliance obligations. <br>
Mitigation: Validate recipients, templates, webhook URLs, bot settings, and schedules in a low-risk workspace before production use. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/whatsable/agent-skills-by-notifyer) <br>
- [Messaging reference](artifact/references/messaging-reference.md) <br>
- [Templates reference](artifact/references/templates-reference.md) <br>
- [Bots reference](artifact/references/bots-reference.md) <br>
- [Broadcasts reference](artifact/references/broadcasts-reference.md) <br>
- [Webhooks reference](artifact/references/webhooks-reference.md) <br>
- [Analytics reference](artifact/references/analytics-reference.md) <br>
- [Team reference](artifact/references/team-reference.md) <br>
- [API key reference](artifact/references/api-key-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON, CSV, or status text returned by Notifyer scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or newer and Notifyer API credentials; command outputs may contain sensitive workspace, recipient, message, or API-key data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
