## Description:

Monitor Claude Code releases and send Telegram alerts when new versions ship using Bash, curl, jq, npm, and OpenClaw scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[assistant-design](https://clawhub.ai/user/assistant-design)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to monitor the @anthropic-ai/claude-code npm package and receive Telegram alerts when a new release appears. It can run manually or as an OpenClaw or macOS cron job.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes a built-in Telegram bot token and fixed chat destination that can be used automatically when user-provided Telegram settings are absent.

Mitigation: Require explicit user-provided Telegram credentials, confirm the destination before test or first run, and protect the credential file permissions.

Risk: The monitor can download and extract npm tarballs for future diffs.

Mitigation: Validate tarballs before extraction or disable package extraction when it is not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/assistant-design/skills/cc-changelog-monitor)
- [Claude Code npm package](https://www.npmjs.com/package/@anthropic-ai/claude-code)
- [Claude Code npm latest metadata](https://registry.npmjs.org/@anthropic-ai/claude-code/latest)
- [OpenClaw](https://openclaw.ai)
- [Telegram BotFather](https://t.me/BotFather)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and Telegram notification content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime scripts write local version and credential files and may create extracted package directories for diffs.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
