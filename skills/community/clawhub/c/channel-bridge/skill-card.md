## Description: <br>
In-memory message routing library for multi-channel agent communication. Provides routing rules, filters, and transforms. Wire your own platform adapters for Discord, Slack, Telegram, etc. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to route messages between communication platforms, apply simple filters, and transform or buffer messages before handing them to user-provided platform adapters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A documented filter can fail open and forward more messages than intended when unsupported filter syntax is used. <br>
Mitigation: Review routes before connecting real messaging adapters, test with harmless messages first, and avoid unsupported filters unless they are implemented. <br>
Risk: Routed or buffered messages may include sensitive content. <br>
Mitigation: Add explicit allowlists, redaction, and buffer limits before using the skill with sensitive or production messages. <br>


## Reference(s): <br>
- [Channel Bridge on ClawHub](https://clawhub.ai/TheShadowRose/channel-bridge) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [JavaScript objects and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes are produced in memory; external message delivery depends on user-provided platform adapters.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
