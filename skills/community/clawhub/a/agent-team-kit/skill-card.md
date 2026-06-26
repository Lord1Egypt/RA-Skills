## Description: <br>
Agent Team Kit provides a process framework for AI agent teams to manage work queues, roles, discovery, and proactive heartbeat-driven operation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryancampbell](https://clawhub.ai/user/ryancampbell) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators of multi-agent workspaces use this skill to set up self-service queues, role ownership, intake triage, status tracking, and heartbeat checks. It helps an agent team discover work, triage it, assign execution, and feed completed work back into future opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent instructions that can encourage agents to spawn and act autonomously without enough local safety boundaries. <br>
Mitigation: Define in-scope queues before enabling heartbeat checks, cap agent spawning, restrict writable paths, require human approval for destructive, deployment, public, financial, account, or credential-related actions, and review file changes before committing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ryancampbell/agent-team-kit) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Heartbeat template](templates/HEARTBEAT.md) <br>
- [Intake process template](templates/process/INTAKE.md) <br>
- [Roles template](templates/process/ROLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown templates with inline shell commands and process tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational process files and agent coordination guidance; no runtime API output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
