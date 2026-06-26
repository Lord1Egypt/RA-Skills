## Description: <br>
Manage OpenClaw isolated agents from chat with short commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alincatalin](https://clawhub.ai/user/alincatalin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to translate short chat requests into agent management commands for listing, creating, switching, binding, unbinding, deleting, and updating agent identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent OpenClaw agent configuration changes, including binding channels and deleting agents. <br>
Mitigation: Double-check agent names and channel bindings before running commands, and require explicit confirmation before delete operations. <br>
Risk: Short chat commands may be ambiguous and could target the wrong agent or channel. <br>
Mitigation: Ask one focused clarification question when an agent name, channel, workspace, or binding is unclear. <br>


## Reference(s): <br>
- [Agent Control on ClawHub](https://clawhub.ai/alincatalin/agent-control) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides a brief success or failure result and the next useful command after each operation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
