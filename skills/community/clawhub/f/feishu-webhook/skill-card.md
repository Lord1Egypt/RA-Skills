## Description:

Sends Markdown-formatted rich text messages to Feishu channels or DMs through a configured Feishu webhook with heredoc input support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[talentestors](https://clawhub.ai/user/talentestors)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send scheduled notifications, alerts, and reports from agent workflows to configured Feishu channels or DMs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message content supplied to the skill is posted to the configured Feishu destination.

Mitigation: Send only content intended for that Feishu channel or DM, and avoid secrets, credentials, private logs, and internal reports unless sharing is deliberate.

Risk: A misconfigured webhook URL can route messages to an unintended destination.

Mitigation: Verify FEISHU_WEBHOOK_URL and FEISHU_WEBHOOK_SECRET before use in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/talentestors/skills/feishu-webhook)
- [Project homepage](https://github.com/talentestors/feishu-webhook)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Text]

**Output Format:** [Markdown content sent as a Feishu interactive card, with a short terminal status message.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads message content from stdin and sends it to the configured Feishu webhook URL.]

## Skill Version(s):

1.2.4 (source: server release metadata; artifact frontmatter lists 1.2.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
