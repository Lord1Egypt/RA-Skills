## Description:

Multi-channel customer service auto-responder with FAQ matching, escalation, and daily summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Customer service teams and operators use this skill to monitor configured customer channels, answer common FAQ-matched inquiries, escalate sensitive or unresolved messages, and summarize daily support activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw customer conversations and identifiers may be stored in local JSONL logs by default.

Mitigation: Review privacy and retention requirements, obtain consent where required, disable or minimize raw transcript logging, and keep logs in a restricted directory.

Risk: Log cleanup uses the configured log directory, so an unsafe logDir could remove unintended dated directories.

Mitigation: Verify logDir points to a dedicated skill log directory before enabling retention cleanup or running the monitor in the background.

Risk: Channel integrations are mock implementations until replaced with production APIs.

Mitigation: Validate real channel adapters, credentials handling, and escalation routing in a controlled environment before customer-facing use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/cs-autoresponder)
- [Skill homepage](https://github.com/openclaw/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and Node.js shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces FAQ responses, escalation notices, JSONL log entries, and daily summary text when its scripts are run.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; package.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
