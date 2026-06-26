## Description: <br>
A2A Manager helps coordinators create and manage agents, Discord channels and roles, agent-to-agent coordination, specialist sub-agents, A2A maps, and Notion task workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nyrosveil](https://clawhub.ai/user/nyrosveil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and orchestrator operators use this skill to manage multi-agent workspaces, assign work, create specialist agents, and track tasks through Discord and Notion-backed workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write persistent OpenClaw workspace files and logs, changing local agent state. <br>
Mitigation: Back up ~/.openclaw before use and review the target workspace path before running commands. <br>
Risk: Task-board actions can modify external Notion task state when a Notion token is available. <br>
Mitigation: Use a Notion token scoped to the intended database and confirm task IDs before update, approval, or deletion actions. <br>
Risk: Agent and specialist disposal actions may remove local workspaces or coordination records. <br>
Mitigation: Require manual confirmation and explicit agent names before destructive actions. <br>


## Reference(s): <br>
- [A2A Map Template](references/A2A_MAP.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/nyrosveil/a2a-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and generated workspace or configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local OpenClaw workspace files, logs, A2A_MAP.md, Discord configuration, and Notion task records when scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
