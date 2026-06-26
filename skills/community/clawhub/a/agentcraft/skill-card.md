## Description: <br>
Visualize coding sessions as a real-time strategy game with automatic deploy and event reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[idosal](https://clawhub.ai/user/idosal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use AgentCraft to visualize coding sessions in a real-time dashboard and report activity such as prompts, file access, shell commands, and idle state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session telemetry can include sensitive prompts, file paths, commands, and workspace context. <br>
Mitigation: Use only in workspaces where that activity can be shared, and disable or redact reporting before handling secrets or sensitive repositories. <br>
Risk: The local AgentCraft service may be exposed beyond localhost when remote sharing is enabled. <br>
Mitigation: Keep the service local by default; do not expose it publicly without authentication and a clear shutdown process. <br>
Risk: Automatic startup through npx can run the currently resolved package version. <br>
Mitigation: Review the package before installation and pin an approved version when using the skill in controlled environments. <br>


## Reference(s): <br>
- [AgentCraft homepage](https://getagentcraft.com) <br>
- [AgentCraft on ClawHub](https://clawhub.ai/idosal/agentcraft) <br>
- [idosal publisher profile](https://clawhub.ai/user/idosal) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON event examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Starts or checks a local service and emits fire-and-forget session activity events when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
