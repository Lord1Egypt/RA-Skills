## Description: <br>
Email Customer Assistant reads IMAP mailboxes, classifies customer emails, generates multilingual AI reply suggestions, and pushes email summaries or urgent alerts to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiji0802](https://clawhub.ai/user/qiji0802) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer support teams and operators use this skill to monitor IMAP inboxes, prioritize customer messages, draft response suggestions, and route summaries or urgent alerts to Feishu for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles mailbox credentials and customer email contents. <br>
Mitigation: Use a dedicated mailbox or app password, limit mailbox folders and message volume, and avoid deploying it on regulated or production inboxes until review is complete. <br>
Risk: Email subjects, snippets, bodies, summaries, and reply drafts may be sent to configured AI providers and Feishu recipients. <br>
Mitigation: Configure approved AI endpoints and Feishu recipients only, disclose external data flows to operators, and restrict notifications to channels authorized for customer data. <br>
Risk: The security guidance notes that dry-run behavior may not provide a true preview-only mode. <br>
Mitigation: Avoid relying on --dry-run for safety-critical previews until the behavior is fixed or independently verified. <br>
Risk: Dependency and token-validation behavior require clarification before broader deployment. <br>
Mitigation: Pin and review dependencies, and clarify or remove token-validation behavior before use in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/qiji0802/email-customer-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/qiji0802) <br>
- [YK-Global](https://yk-global.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain-text reports, JSON email result lists, Markdown-style notification content, Python command examples, and YAML-style configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include email subjects, snippets, classifications, summaries, reply suggestions, and Feishu delivery status messages] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
