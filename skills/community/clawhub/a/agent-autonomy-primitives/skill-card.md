## Description: <br>
Build long-running autonomous agent loops using ClawVault primitives for tasks, projects, memory types, templates, and heartbeats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G9Pedro](https://clawhub.ai/user/G9Pedro) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up task-driven autonomous agent workflows with persistent memory, project grouping, customizable templates, and heartbeat-based work queues. It also supports adapting those primitives to existing agent frameworks and shared multi-agent vaults. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring heartbeat or cron-driven task loops can continue operating without adequate oversight or shutdown controls. <br>
Mitigation: Use a private or tightly controlled vault, define which projects and tools the agent may use, require human approval for risky actions, log each run, and configure a clear pause or shutdown mechanism before enabling recurring execution. <br>
Risk: The workflow depends on installing and using the clawvault npm package. <br>
Mitigation: Verify the clawvault package before installation and consider pinning or isolating the install. <br>


## Reference(s): <br>
- [Adaptation Guide](references/adaptation-guide.md) <br>
- [Template Customization Guide](references/template-customization.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash, YAML, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for configuring ClawVault-backed agent autonomy; it does not directly execute commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
