## Description: <br>
Bridge Discord messages to Agent Zero's HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wespeakallday](https://clawhub.ai/user/wespeakallday) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to relay messages from selected Discord channels to Agent Zero and send Agent Zero responses back into Discord. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord chat may be relayed to Agent Zero too broadly if channels and bot permissions are not scoped. <br>
Mitigation: Set DISCORD_CHANNEL_IDS to a narrow allowlist and restrict the Discord bot to only the channels and permissions required. <br>
Risk: Discord messages may be sent to Agent Zero and answered publicly in a channel. <br>
Mitigation: Notify channel participants before use and run the bridge only in channels intended for Agent Zero interaction. <br>
Risk: Agent Zero API access may be exposed if credentials or the HTTP endpoint are configured broadly. <br>
Mitigation: Use HTTPS or loopback-only API access and dedicated low-privilege credentials for the bridge. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wespeakallday/discord-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration instructions] <br>
**Output Format:** [Discord text messages, JSON HTTP requests, and Markdown setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Discord responses are split to fit the 2,000-character message limit.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
