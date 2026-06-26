## Description: <br>
Athena Protocol is a modular identity and communication framework for personal AI assistants on OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skbylife](https://clawhub.ai/user/skbylife) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to adapt an existing personal AI assistant with persistent memory conventions, operating principles, communication analysis patterns, and proactive check-in templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory guidance may lead an assistant to record sensitive or unnecessary personal information. <br>
Mitigation: Define what may be remembered before installation, exclude secrets and sensitive records, and periodically review memory files. <br>
Risk: Proactive heartbeat behavior may inspect email, calendar, project, or memory sources beyond the user's intended scope. <br>
Mitigation: Limit access to accounts and workspaces the user controls, set quiet hours, and scope each optional check before enabling it. <br>
Risk: Copying framework sections into agent configuration can materially change assistant behavior. <br>
Mitigation: Review selected sections before copying them into AGENTS.md, SOUL.md, or HEARTBEAT.md, and require explicit approval before external actions. <br>


## Reference(s): <br>
- [Athena Protocol Skill Page](https://clawhub.ai/skbylife/athena-protocol) <br>
- [SKILL.md](SKILL.md) <br>
- [protocol.md](protocol.md) <br>
- [memory-architecture.md](memory-architecture.md) <br>
- [human-comms-framework.md](human-comms-framework.md) <br>
- [heartbeat-template.md](heartbeat-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with configuration snippets and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; users copy selected sections into existing OpenClaw configuration files.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
