## Description: <br>
记忆模组 provides an always-on agent memory infrastructure for perception memory, short-term semantic buckets, long-term memory, context reconstruction, insight generation, reasoning reflection support, privacy configuration, and encryption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kiwifruit13](https://clawhub.ai/user/kiwifruit13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add local memory, state capture, context reconstruction, insight generation, LangGraph state integration, and reasoning reflection workflows to an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Always-on local memory can persist sensitive user, state, profile, and reflection data across sessions. <br>
Mitigation: Require explicit opt-in for cross-session memory, restrict storage paths, and define retention, export, and deletion rules before deployment. <br>
Risk: Credential storage can increase exposure if encryption and access controls are not reviewed. <br>
Mitigation: Disable credential storage unless needed, separately review the credential manager, and verify real encryption at rest before storing secrets. <br>
Risk: Sensitive profiling may be reused in later agent behavior without clear user expectations. <br>
Mitigation: Use the privacy configuration flow, minimize stored profile data, and require user consent before storing or reusing sensitive memory. <br>
Risk: The security verdict is suspicious and VirusTotal telemetry was pending in the provided evidence. <br>
Mitigation: Review and scan the artifact before deployment, and only install it when an always-on local memory layer is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kiwifruit13/agent-memory-plus) <br>
- [Global architecture overview](references/architecture_overview.md) <br>
- [Memory types](references/memory_types.md) <br>
- [Activation mechanism](references/activation_mechanism.md) <br>
- [Agent loops guide](references/agent_loops_guide.md) <br>
- [Chain reasoning guide](references/chain_reasoning_guide.md) <br>
- [Privacy guide](references/privacy_guide.md) <br>
- [Encryption guide](references/encryption_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation and reuse of persisted local memory, state, profile, reflection, and credential data.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
