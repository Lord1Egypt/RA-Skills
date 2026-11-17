## Description:

Automatically generates and posts persona-matched tweets to X using GPT-5.1, with repetition checks, content filters, character limit protection, and optional Telegram alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edisonchenai](https://clawhub.ai/user/edisonchenai)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to set up an automated X posting workflow that generates short persona-matched posts, checks recent output for repetition, and can notify a Telegram chat after posts or failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automation can repeatedly publish generated content to a live X account.

Mitigation: Use a dedicated X account, keep API keys narrowly scoped, run dry-run previews first, and do not enable cron until generated posts are acceptable.

Risk: When SCAN_DIR is set, local Markdown scan content may be sent to OpenAI as generation context.

Mitigation: Leave SCAN_DIR unset unless needed, and point it only at approved Markdown that contains no private or untrusted content.

Risk: Telegram notifications may expose tweet text and some failure details to the configured Telegram chat.

Mitigation: Enable Telegram only for an appropriate bot and chat, and assume notification contents are visible to that channel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edisonchenai/skills/edison-autopilot-post-x)
- [X Developer Platform](https://developer.x.com)
- [OpenAI Platform](https://platform.openai.com)
- [Tweepy](https://github.com/tweepy/tweepy)
- [Telegram BotFather](https://t.me/BotFather)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration steps, and Python code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance for an automation script that can generate tweet text, post through the X API, log posted tweets, and send optional Telegram notifications.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
