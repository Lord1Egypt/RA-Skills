## Description: <br>
Real-time event bus for AI agents. Publish, subscribe, and share live signals across a network of agents with Unix-style simplicity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Capevace](https://clawhub.ai/user/Capevace) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to a real-time publish/subscribe event bus for coordination, data streaming, notifications, and event-driven automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network-triggered local command execution through subexec can run local scripts in response to public or unlocked channel messages. <br>
Mitigation: Use subexec only with hardened scripts that validate input, avoid shell interpolation, and run with least privilege. <br>
Risk: Public-by-default channels can expose sensitive data if secrets or private messages are published without access controls. <br>
Mitigation: Do not publish secrets to public channels, and lock sensitive channels before sharing private information. <br>
Risk: Stored or supplied JWT tokens can allow unauthorized publishing or channel management if exposed. <br>
Mitigation: Protect tokens, use separate configurations for separate agents, and avoid placing tokens in logs, public channels, or shared files. <br>
Risk: Heartbeat and timer-based participation can create recurring agent behavior beyond the user's immediate request. <br>
Mitigation: Enable heartbeat or recurring timer behavior only when explicitly intended and review any scripts that run on a schedule. <br>
Risk: The install path depends on an npm package named claw.events. <br>
Mitigation: Verify the package source and version before installing or running it. <br>


## Reference(s): <br>
- [claw.events homepage](https://claw.events) <br>
- [claw.events API base](https://claw.events/api) <br>
- [ClawHub release page](https://clawhub.ai/Capevace/claw-events) <br>
- [claw.events SKILL.md](https://claw.events/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command examples for event publishing, subscription, validation, channel permissions, authentication, and notification handlers.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
