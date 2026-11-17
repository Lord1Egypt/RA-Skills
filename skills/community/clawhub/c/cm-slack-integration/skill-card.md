## Description:

Slack messaging - send messages, manage channels, upload files, add reactions, and automate team notifications via CLI and API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate Slack workspace notifications, channel workflows, file sharing, reactions, and user lookups through Slack Web API commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Slack token allows the agent to read or post workspace data according to the token scopes.

Mitigation: Use the minimum Slack scopes needed, prefer bot tokens over user tokens, and restrict the bot to approved channels.

Risk: Slack messages, files, links, logs, and channel changes may expose sensitive workspace information or alter team communications.

Mitigation: Review messages, files, links, logs, and channel changes before sending them to Slack.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/cm-slack-integration)
- [Publisher profile](https://clawhub.ai/user/charlie-morrison)
- [Slack app configuration](https://api.slack.com/apps)
- [Slack chat.postMessage API](https://slack.com/api/chat.postMessage)
- [Slack chat.scheduleMessage API](https://slack.com/api/chat.scheduleMessage)
- [Slack conversations API examples](https://slack.com/api/conversations.list)
- [Slack file upload API example](https://slack.com/api/files.getUploadURLExternal)
- [Block Kit Builder](https://app.slack.com/block-kit-builder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with Slack Web API curl examples and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Slack token provided through SLACK_TOKEN.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
