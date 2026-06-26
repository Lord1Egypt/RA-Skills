## Description: <br>
Free email for AI agents. No sign-up needed. One call to get a mailbox and send. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huberthe-pro](https://clawhub.ai/user/huberthe-pro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to create an Agents Mail mailbox, send email, check inboxes, and configure permanent mailboxes or webhook-based workflows through the REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables an agent to use an external email mailbox and send messages. <br>
Mitigation: Keep the API key private, review recipients and message content before sending when possible, and install only when external email access is intended. <br>
Risk: Automated inbox checks, auto-responders, heartbeat checks, and webhooks can send or forward content without direct human review. <br>
Mitigation: Enable automation only for trusted senders and trusted destinations, and use rate limits or approval rules for message handling. <br>
Risk: Mailbox deletion, retention, and webhook behavior can affect sensitive email content. <br>
Mitigation: Confirm deletion and retention policies before handling sensitive data, and verify webhook HMAC signatures before processing inbound events. <br>


## Reference(s): <br>
- [Agents Mail Homepage](https://agentsmail.org) <br>
- [Agents Mail API Reference](references/API.md) <br>
- [Agents Mail Common Patterns](references/EXAMPLES.md) <br>
- [Agents Mail API Help](https://agentsmail.org/api/help) <br>
- [Agents Mail Docs](https://agentsmail.org/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with REST API examples, curl commands, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [External API calls require an Agents Mail API key after mailbox creation.] <br>

## Skill Version(s): <br>
0.4.6 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
