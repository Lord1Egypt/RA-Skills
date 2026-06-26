## Description: <br>
Guide users through building a custom multi-agent team on OpenClaw, from role design to workspace files, routing bindings, channel configuration, and collaboration rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superjavason](https://clawhub.ai/user/superjavason) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and advanced OpenClaw users use this skill to design custom multi-agent setups and generate proposed OpenClaw configuration, workspace files, routing bindings, collaboration rules, and shared-memory guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated examples may grant broad command, filesystem, session, and shared-memory authority to OpenClaw agents. <br>
Mitigation: Review generated configuration before use, narrow each agent's tool allowlist, prefer workspace-only filesystem access, and avoid storing secrets in shared files. <br>
Risk: Multi-agent routing or agent-to-agent settings can create unintended replies, delegation, or loops. <br>
Mitigation: Use explicit allowlists, specific mention patterns, low max ping-pong limits, loop detection, and explicit approval for exec or restart steps. <br>


## Reference(s): <br>
- [Agent Team Builder on ClawHub](https://clawhub.ai/superjavason/agent-team-builder) <br>
- [Agent-to-Agent Communication](references/agent-communication.md) <br>
- [Architecture Corrections](references/architecture-corrections.md) <br>
- [OpenClaw Team Example](references/openclaw-team-example.json5) <br>
- [Team Shared Memory](references/team-shared-memory.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with JSON5 configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated examples can include placeholder tokens and broad permissions; review and narrow them before use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
