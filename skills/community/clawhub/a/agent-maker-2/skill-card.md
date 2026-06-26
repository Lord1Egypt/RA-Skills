## Description: <br>
Create autonomous AI agents for OpenClaw with guided discovery that clarifies purpose, personality, skills, channels, automation, and security before generating a configured agent workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anhnt224](https://clawhub.ai/user/anhnt224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to design and create autonomous OpenClaw agents through a guided requirements flow, then generate workspace files, gateway configuration, optional heartbeat automation, and optional cron jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent autonomous OpenClaw agents with broad access. <br>
Mitigation: Start with tier1 autonomy, explicit tool allow and deny lists, and sandboxing for any agent that may process untrusted input. <br>
Risk: Gateway configuration changes may grant agents broader model, tool, sandbox, heartbeat, or workspace access than intended. <br>
Mitigation: Review the printed gateway config patch before applying it and confirm the workspace, tool policy, sandbox mode, and heartbeat settings. <br>
Risk: Heartbeat, cron, external channel bindings, and bot credentials can increase persistence and exposure. <br>
Mitigation: Enable automation and external channel bindings only when necessary, and store any required credentials securely. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/anhnt224/agent-maker-2) <br>
- [Publisher profile](https://clawhub.ai/user/anhnt224) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash commands, JSON configuration patches, and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OpenClaw agent workspace files and configuration updates when the creation script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
