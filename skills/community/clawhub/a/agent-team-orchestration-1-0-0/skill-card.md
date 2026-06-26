## Description: <br>
Orchestrate multi-agent teams with defined roles, task lifecycles, handoff protocols, and review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Matttgx](https://clawhub.ai/user/Matttgx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical leads use this skill to coordinate sustained multi-agent workflows with clear roles, shared artifacts, handoffs, reviews, and task lifecycle tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Multi-agent workspaces can expose files or credentials to agents that do not need them. <br>
Mitigation: Define which agents may read or write each workspace, keep credentials out of shared folders unless explicitly needed, and review shared artifacts before use. <br>
Risk: Unbounded spawning, scheduling, or handoffs can create coordination failures or unattended work. <br>
Mitigation: Set concurrency and approval limits for spawned agents, use explicit stop conditions for scheduled operations, and require review points before marking work done. <br>


## Reference(s): <br>
- [Agent Team Orchestration Skill Page](https://clawhub.ai/Matttgx/agent-team-orchestration-1-0-0) <br>
- [Team Setup](references/team-setup.md) <br>
- [Task Lifecycle](references/task-lifecycle.md) <br>
- [Communication](references/communication.md) <br>
- [Patterns](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown guidance with structured role definitions, task flows, handoff templates, and verification steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only playbook; no executable install hooks are included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
