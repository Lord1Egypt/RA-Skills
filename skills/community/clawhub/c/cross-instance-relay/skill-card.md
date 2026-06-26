## Description: <br>
Connect agents across OpenClaw instances via relay. Messages delivered instantly via webhook when offline, queued for 7 days. No persistent connection needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaravgarg](https://clawhub.ai/user/aaravgarg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure cross-instance OpenClaw agent messaging through a relay, including webhook delivery, queued fallback delivery, inbox polling, and optional WebSocket streaming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An external relay can continue delivering messages to an agent after setup. <br>
Mitigation: Use only a trusted relay operator or self-host the relay, and confirm there is a clear process to disable the webhook. <br>
Risk: Shared team tokens can expose relay access if reused or overprivileged. <br>
Mitigation: Use dedicated, rotateable, low-privilege tokens for relay access. <br>
Risk: Inbound relay messages could be mistaken for trusted commands. <br>
Mitigation: Treat inbound messages as requests that require agent-side validation before action. <br>
Risk: Queued offline messages may remain available for later delivery. <br>
Mitigation: Confirm queued messages can be cleared when access is revoked or a relay is no longer trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aaravgarg/cross-instance-relay) <br>
- [Agent Relay Open Source Project](https://github.com/aaravgarg/agent-relay) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with curl and WebSocket command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires relay URL, team token, team ID, and instance ID environment variables.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
