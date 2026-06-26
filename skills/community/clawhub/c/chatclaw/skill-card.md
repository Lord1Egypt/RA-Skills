## Description: <br>
Connect your OpenClaw bot to the ChatClaw cloud dashboard for remote chat, token tracking, task management, agent workspace file browsing, and skills management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sumeralabs](https://clawhub.ai/user/sumeralabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to connect a local OpenClaw agent to the ChatClaw cloud dashboard for browser-based chat, token tracking, workspace file browsing, skill management, and scheduled task management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the cloud dashboard can chat with the agent, read workspace files through the gateway, manage installed skills, and manage scheduled tasks with broad operator authority. <br>
Mitigation: Install only in workspaces where that remote control model is acceptable, protect and rotate the ChatClaw API key, and disable the skill when remote access is not needed. <br>
Risk: The security evidence flags broad operator authority that is not fully scoped or disclosed. <br>
Mitigation: Review local OpenClaw and ChatClaw access before enabling, avoid sensitive workspaces, and monitor skill logs for file, skill, and cron actions. <br>
Risk: The skill depends on a persistent outbound cloud relay operated by SumeraLabs. <br>
Mitigation: Treat SumeraLabs and the ChatClaw cloud account as part of the trust boundary, and verify that organizational policy permits relaying agent messages and workspace metadata through that service. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/sumeralabs/chatclaw) <br>
- [ChatClaw homepage](https://chatclaw.sumeralabs.com) <br>
- [ChatClaw setup](https://app.chatclaw.sumeralabs.com/setup) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [Streaming text and JSON status/control messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ChatClaw API key, OpenClaw gateway configuration, and outbound connections to the ChatClaw cloud relay.] <br>

## Skill Version(s): <br>
0.5.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
