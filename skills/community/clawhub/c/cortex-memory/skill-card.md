## Description: <br>
Long-term memory for OpenClaw agents - auto-recall before turns, auto-capture after, tools for search/save/forget. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewubundi](https://clawhub.ai/user/matthewubundi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to give agents persistent Cortex-backed memory for recalling prior context, saving durable facts, and forgetting stored memories when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist detailed conversation-derived facts to an external Cortex service. <br>
Mitigation: Install only when that data flow is acceptable, store the Cortex API key securely, and use audit or forget controls for sensitive work. <br>
Risk: Broad tool access can expose more agent authority than the memory workflow requires. <br>
Mitigation: Prefer a selective Cortex tool allowlist over a full tools profile when configuring OpenClaw. <br>
Risk: Automatic capture and recall may preserve or reuse outdated, sensitive, or incorrect memories. <br>
Mitigation: Disable auto-capture or auto-recall when needed, review recalled context against live state, and remove stale memories with the forget workflow. <br>


## Reference(s): <br>
- [Cortex Memory on ClawHub](https://clawhub.ai/matthewubundi/cortex-memory) <br>
- [README.md](artifact/README.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown with inline commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Cortex memory tools and OpenClaw Cortex CLI commands when available.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
