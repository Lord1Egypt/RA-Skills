## Description:

Assists with installing, configuring, and using the Apple Mail channel plugin for OpenClaw and Hermes on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jehadurre](https://clawhub.ai/user/jehadurre)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to set up Apple Mail as an OpenClaw or Hermes email channel on macOS, including installation, account configuration, monitoring, troubleshooting, and common multi-account patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example configurations can allow processing email from any sender.

Mitigation: Prefer explicit sender allowlists and use a dedicated or least-privileged mailbox where possible.

Risk: The setup grants an external Apple Mail plugin access to mailbox automation through macOS Automation permissions.

Mitigation: Pin or verify the external plugin before granting Mail.app automation access and review permissions before deployment.

Risk: Automated replies or archiving can affect live mailbox state.

Mitigation: Require manual approval before replies or archiving, and leave archiveOnReply disabled unless the workflow intentionally archives handled threads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jehadurre/skills/apple-mail-setup)
- [Apple Mail channel documentation](https://openclaw-apple-mail.jehadurre.me)
- [Apple Mail plugin package](https://www.npmjs.com/package/@jehadurre/openclaw-apple-mail)
- [Skill package](https://www.npmjs.com/package/@jehadurre/openclaw-apple-mail-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, Apple Mail, Node.js 18 or newer, and OpenClaw 2026.1.0 or Hermes.]

## Skill Version(s):

1.0.1 (source: skill.json, package.json, CHANGELOG, released 2026-06-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
