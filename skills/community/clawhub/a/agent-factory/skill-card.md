## Description: <br>
Creates and switches OpenClaw agents, including generated agent workspaces, memory files, cron templates, and configuration entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TevfikGulep](https://clawhub.ai/user/TevfikGulep) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create persistent OpenClaw sub-agents, switch between agents, and prepare the files and configuration needed for each agent workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent sub-agents can inherit broad OpenClaw capabilities including browser, Sheets, cron, memory, and configuration authority. <br>
Mitigation: Install only when persistent sub-agents are intended, restrict external credentials, and review each generated agent's permissions before use. <br>
Risk: The release can modify OpenClaw configuration and may require manual cleanup if agent creation is incorrect. <br>
Mitigation: Back up openclaw.json before running the creation script and remove incorrect agent entries manually if needed. <br>
Risk: Using an existing Chrome profile can expose active browser sessions to newly created agents. <br>
Mitigation: Prefer isolated browser profiles and avoid profile=chrome unless shared session access is explicitly required. <br>
Risk: Generated USER.md and cron files may contain sensitive or unintended data or automation behavior. <br>
Mitigation: Review generated USER.md content and cron files before enabling or copying cron jobs into the active workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TevfikGulep/agent-factory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and generated Markdown, Python, and JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent agent directories and updates OpenClaw configuration when the bundled shell script is run.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
