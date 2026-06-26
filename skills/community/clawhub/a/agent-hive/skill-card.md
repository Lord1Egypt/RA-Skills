## Description: <br>
Agent Hive helps developers create and manage OpenClaw multi-agent teams with shared workspaces, budget governance, and configurable spawn permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up or extend OpenClaw agent teams, configure spawn permissions, and add budget audit routines for team governance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent OpenClaw workspace, agent directory, symlink, budget file, and service configuration changes. <br>
Mitigation: Use it only when intentionally setting up a persistent multi-agent OpenClaw team, and review and back up ~/.openclaw/openclaw.json and existing workspaces before applying changes. <br>
Risk: The supplied security summary says the budget controls may overstate how strongly spawn limits are enforced. <br>
Mitigation: Treat the budget audit as governance support, and separately verify that allowAgents is actually revoked or restored when demoting or reinstating agents. <br>
Risk: Agent identifiers are used in workspace and configuration paths. <br>
Mitigation: Use simple trusted agent IDs and review generated paths before creating workspaces or updating OpenClaw configuration. <br>


## Reference(s): <br>
- [Agent Budget Governance Framework](references/governance.md) <br>
- [Heartbeat Budget Audit Snippet](references/heartbeat-snippet.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may propose persistent OpenClaw workspace, configuration, symlink, and budget file changes that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
