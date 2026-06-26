## Description: <br>
Clawlist guides agents through planning, executing, tracking, and verifying multi-step, long-running, or recurring workflows with checkpoint validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arisylafeta](https://clawhub.ai/user/arisylafeta) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to structure agent work into brainstorming, planning, execution, optional parallel dispatch, and verification. It also supports tracking long-running or recurring workflows through an ongoing tasks file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the agent broad workflow control across planning, execution, verification, and recurring task management. <br>
Mitigation: Set explicit scope, allowed actions, approval requirements, and review checkpoints before using it for important work. <br>
Risk: Long-running or infinite tasks can continue without clear stop or re-approval limits. <br>
Mitigation: Define cadence, stop conditions, and periodic human review for entries in memory/tasks/ongoing-tasks.md. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklists, plans, status reports, and occasional shell commands or file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update task plans, completion reports, and ongoing task tracking files when used by an agent.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
