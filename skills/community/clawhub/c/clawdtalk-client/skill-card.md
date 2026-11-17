## Description:

ClawdTalk adds voice calls, SMS messaging, approval requests, and AI mission workflows to Clawdbot and OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dcasem](https://clawhub.ai/user/dcasem)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to connect a Clawdbot or OpenClaw agent to phone calls, SMS conversations, approval flows, and outbound mission tracking through ClawdTalk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote phone and SMS interactions can reach the user's main agent session and connected tools.

Mitigation: Install only when comfortable with that access, restrict sessions_send to the narrowest practical scope, and keep approval flows fail-closed for sensitive actions.

Risk: Voice transcripts, SMS content, mission state, and cloud events are handled by ClawdTalk services.

Mitigation: Use the skill only with data appropriate for ClawdTalk processing and avoid storing live gateway tokens or API keys in plaintext configuration.

Risk: Weak approval boundaries or voice-only approval fallbacks can make sensitive actions easier to trigger remotely.

Mitigation: Remove voice-only approval fallback for sensitive actions, require stronger out-of-band approval where available, and review approval behavior before deployment.

Risk: Updater and dependency handling can change executable skill behavior.

Mitigation: Review updates and dependency changes before applying them in production environments.

## Reference(s):

- [ClawdTalk ClawHub listing](https://clawhub.ai/dcasem/skills/clawdtalk-client)
- [ClawdTalk Client homepage](https://github.com/team-telnyx/clawdtalk-client)
- [ClawdTalk service](https://clawdtalk.com)
- [Clawdbot](https://clawdbot.com)
- [Telnyx](https://telnyx.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may guide agents to invoke local scripts that connect to ClawdTalk services for calls, SMS, approvals, and mission state.]

## Skill Version(s):

2.0.5 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
