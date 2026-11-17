## Description:

1688-ai-message-push helps an agent send WeChat or APP system notifications to the current user's own account through a Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to send short notification text to the user's own WeChat or APP notification channels, after configuring a 1688 AK when required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential configuration can use or overwrite another skill's 1688-shopkeeper API key rather than this skill's own namespace.

Mitigation: Install only when the publisher is trusted, review credential handling before use, and prefer a later release that stores secrets under this skill's own namespace.

Risk: A provided AK can be transmitted to the configured OpenClaw gateway URL during setup.

Mitigation: Use only a trusted local or managed gateway and avoid entering production credentials in untrusted environments.

Risk: Notification commands are write actions that send user-provided text when the message content is clear.

Mitigation: Confirm the notification text is supplied by the user, ask for missing text, and avoid rewriting the user's intended message without approval.

Risk: CLI invocations report usage telemetry to the 1688 gateway when authenticated.

Mitigation: Review the documented telemetry behavior before deployment and account for this network call in privacy and operational reviews.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-ai-message-push)
- [APP system notification guide](artifact/references/capabilities/app_push.md)
- [AK configuration guide](artifact/references/capabilities/configure.md)
- [WeChat notification guide](artifact/references/capabilities/wx_push.md)
- [Skill usage telemetry notes](artifact/references/skill埋点说明.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [JSON responses with a user-facing markdown field and optional data object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Notification commands perform write actions; configure stores an AK for authenticated use.]

## Skill Version(s):

0.8.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
