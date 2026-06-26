## Description: <br>
Orchestrates multi-agent teams with defined roles, task lifecycles, handoff protocols, and review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nuradil](https://clawhub.ai/user/nuradil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and team leads use this skill to set up sustained multi-agent workflows with role assignments, task routing, handoffs, reviews, and shared artifact conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Secrets or sensitive work products could be exposed through shared folders used by multiple agents. <br>
Mitigation: Keep secrets out of shared folders and restrict access to shared artifacts to agents that need them. <br>
Risk: Agents with broad write access could alter persistent instructions or coordination files in ways that affect future work. <br>
Mitigation: Restrict which agents can edit persistent instructions and require review for changes to team protocols. <br>
Risk: Unbounded parallel agents or schedules can increase coordination overhead and operational risk. <br>
Mitigation: Cap parallel agents and scheduled workflows, and require human approval for high-impact work. <br>


## Reference(s): <br>
- [Team Setup](references/team-setup.md) <br>
- [Task Lifecycle](references/task-lifecycle.md) <br>
- [Communication](references/communication.md) <br>
- [Patterns](references/patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/nuradil/agent-team-orchestration-1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown guidance with task templates, role definitions, workflow patterns, and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no executable code was found in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
