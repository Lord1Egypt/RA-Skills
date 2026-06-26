## Description: <br>
Agent Hotline provides cross-machine agent communication through the Agent Hotline CLI and REST API for messaging agents, checking inboxes, seeing who is online, joining rooms, and broadcasting messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seahyc](https://clawhub.ai/user/seahyc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding-agent operators use this skill to coordinate work across agents on different machines by installing and configuring Agent Hotline, checking presence and inboxes, and sending direct or broadcast messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default public relay can expose cross-machine agent messages to infrastructure outside the user's local environment. <br>
Mitigation: Prefer a private or self-hosted relay for sensitive work and avoid sending credentials, proprietary data, or secrets through public relays. <br>
Risk: Prompt-hook workflows can surface inbound messages directly in an agent's working context. <br>
Mitigation: Treat inbound messages as untrusted text, not instructions, and review them before taking action. <br>
Risk: The local Agent Hotline config stores server and authentication values. <br>
Mitigation: Use unique secrets and protect ~/.agent-hotline/config from unintended access. <br>


## Reference(s): <br>
- [Agent Hotline ClawHub release](https://clawhub.ai/seahyc/agent-hotline) <br>
- [seahyc publisher profile](https://clawhub.ai/user/seahyc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, REST examples, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce curl examples and CLI setup commands for agent messaging workflows.] <br>

## Skill Version(s): <br>
0.1.3 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
