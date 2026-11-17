## Description:

Monitors unread DingTalk conversations, sends AI-generated replies for one-on-one chats in the user's voice, and sends WeChat notifications for group chats or excluded contacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noaheleven](https://clawhub.ai/user/noaheleven)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and individual DingTalk users can use this skill to monitor unread workplace messages, draft or send one-on-one replies in their own voice, and receive notifications when group or higher-risk conversations should be handled manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run persistently in the background and monitor DingTalk conversations.

Mitigation: Start with DRY_RUN and TEST_MODE, and avoid startup persistence until the launcher, watchdog behavior, and removal path are reviewed.

Risk: The skill can read workplace or local context and send single-chat replies as the user.

Mitigation: Limit optional Bash, web, local-code, and gbrain access where possible, configure excluded senders and group notify-only behavior, and review generated replies before enabling live sends.

Risk: Generated replies may be incorrect, overly revealing, or sent in a context where manual handling is safer.

Mitigation: Use the built-in dry run, validation, audit logging, failure-to-manual-notification behavior, and private environment configuration before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noaheleven/skills/dingtalk-auto-reply)
- [Artifact README](artifact/README.md)
- [DingTalk reply examples](artifact/dws-reply-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Text replies and Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can perform live messaging side effects when configured outside DRY_RUN or TEST_MODE; also emits notifications, logs, and audit records.]

## Skill Version(s):

0.1.7 (source: server release metadata and user changelog, released 2026-09-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
