## Description:

Automates publishing local images or videos with a title to the Douyin creator platform through OpenClaw browser control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dream007007s](https://clawhub.ai/user/dream007007s)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers who manage Douyin creator accounts can use this skill to attach to a logged-in Chrome session, upload local media, fill a title, publish the post, and verify it in the creator console.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish publicly from a logged-in Douyin creator account without a hard final confirmation.

Mitigation: Confirm the account, media file, title, and description before allowing the final publish action.

Risk: The skill gives an agent control of an authenticated browser session.

Mitigation: Use an isolated browser profile for Douyin publishing instead of an everyday Chrome profile.

Risk: The skill documents navigation through JavaScript evaluation when normal navigation is blocked.

Mitigation: Restrict use to the intended Douyin creator destination and inspect the active page before upload or publish actions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dream007007s/skills/browser-douyin-post)
- [Douyin Creator Platform](https://creator.douyin.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with browser tool-call examples and PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Chrome session with remote debugging enabled and an authenticated Douyin creator account.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
