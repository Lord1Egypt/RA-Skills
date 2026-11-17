## Description:

Encrypted Clawbot-to-Clawbot messaging. Send messages to friends' Clawbots with end-to-end encryption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davemorin](https://clawhub.ai/user/davemorin)

### License/Terms of Use:

MIT

## Use Case:

Developers and external Clawbot users use Clawlink to set up encrypted agent-to-agent messaging, exchange friend links, send messages, poll for inbox updates, and manage delivery preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Clawlink data can include decrypted messages, identity material, friend data, and shared secrets under ~/.openclaw/clawlink.

Mitigation: Protect filesystem access to that directory, review or fix mailbox path validation before sensitive use, and regularly remove retained message data that is no longer needed.

Risk: Remote Clawlink messages are untrusted content and may be surfaced through the agent heartbeat.

Mitigation: Review incoming messages before using them as instructions or inputs to other tools, and deploy heartbeat polling only after the documented security issues are reviewed or fixed.

Risk: Messaging actions can send content to the wrong recipient or send unintended text.

Mitigation: Confirm the exact recipient and message text before sending, especially for urgent or sensitive messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davemorin/skills/clawlink)
- [README](README.md)
- [ClawLink Invite Flow Specification](INVITE_SPEC.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with CLI commands and JSON handler responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local setup and stores identity, friend, preference, invite, and message state under ~/.openclaw/clawlink.]

## Skill Version(s):

2.6.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
