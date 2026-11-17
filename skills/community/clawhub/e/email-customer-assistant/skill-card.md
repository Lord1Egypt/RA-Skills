## Description:

Email Customer Assistant reads IMAP mailboxes, classifies customer emails, generates multilingual reply suggestions, and can push summaries or urgent alerts to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiji0802](https://clawhub.ai/user/qiji0802)

### License/Terms of Use:

MIT-0

## Use Case:

Customer support operators and small business teams use this skill to triage incoming mailbox messages, draft human-reviewed replies, and route urgent or summarized email information to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox content may be sent to third-party AI or Feishu services when those features are enabled.

Mitigation: Enable AI and Feishu processing only for approved mailboxes, document data-sharing expectations, and restrict Feishu recipients or webhooks to the minimum audience.

Risk: Credential boundaries may be unclear because license validation can use environment-provided API keys.

Mitigation: Use a dedicated 91Skillhub license token for licensing, do not rely on OPENAI_API_KEY for license validation, and rotate any credential that may have been sent to the validation endpoint.

Risk: Scheduled execution can repeatedly process mailbox data before dry-run behavior and data-sharing controls are reviewed.

Mitigation: Run manual dry-runs first, validate configuration and disclosure settings, and enable cron only after the deployment owner approves recurring processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiji0802/skills/email-customer-assistant)
- [Publisher profile](https://clawhub.ai/user/qiji0802)
- [YK-Global website](https://yk-global.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with configuration examples, shell commands, console reports, JSON output, Feishu card payloads, and draft reply text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces AI-assisted classifications, summaries, and reply suggestions from mailbox content; replies are intended for user review before sending.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
