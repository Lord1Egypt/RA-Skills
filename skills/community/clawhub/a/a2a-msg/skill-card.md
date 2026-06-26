## Description: <br>
通过 Redis 消息队列与其他 OpenClaw 实例通信（需自备 Redis 服务器） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaodaabao](https://clawhub.ai/user/gaodaabao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to send, receive, inspect, and optionally auto-handle messages between OpenClaw instances through a self-managed Redis queue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto mode can allow anyone with Redis queue write access to trigger local actions and automatic replies. <br>
Mitigation: Use only a Redis server you control, restrict queue writers to trusted parties, and require sender authentication, allowlists, logging, and per-action approval before enabling auto mode or scheduled processing. <br>
Risk: The skill includes a hardcoded local skills directory listing path. <br>
Mitigation: Review or remove the local skills directory listing before deployment so it does not expose host-specific paths or fail unexpectedly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaodaabao/a2a-msg) <br>
- [Publisher profile](https://clawhub.ai/user/gaodaabao) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-readable text with command-line examples and Redis message responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, Redis connectivity, and A2A_REDIS_HOST, A2A_REDIS_PORT, A2A_REDIS_PASSWORD, A2A_MY_ID, and A2A_PEER_ID environment variables.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
