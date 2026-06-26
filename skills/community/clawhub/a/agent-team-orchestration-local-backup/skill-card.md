## Description: <br>
Orchestrates multi-agent teams with defined roles, task lifecycles, handoff protocols, shared artifacts, and review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up sustained multi-agent workflows with role definitions, task routing, handoff protocols, shared artifact paths, and review gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared workspaces and artifact folders can expose credentials or unrelated private data to other agents. <br>
Mitigation: Use a dedicated project workspace and keep credentials and unrelated private data out of shared folders. <br>
Risk: Scheduled or dispatching agents can continue work without clear human approval or stop conditions. <br>
Mitigation: Define approval, review, and stop rules before enabling scheduled or dispatching agents. <br>
Risk: Poor handoffs can cause lost artifacts, unclear verification, or quality drift across multi-agent work. <br>
Mitigation: Require exact output paths, handoff summaries, verification steps, and cross-role review before marking work done. <br>


## Reference(s): <br>
- [Team Setup](references/team-setup.md) <br>
- [Task Lifecycle](references/task-lifecycle.md) <br>
- [Communication](references/communication.md) <br>
- [Patterns](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with templates, checklists, and inline examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only playbook; produces role, workflow, handoff, and review guidance for an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
