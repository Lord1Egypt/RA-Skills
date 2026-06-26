## Description: <br>
Organize and track daily AI agent tasks, progress, blockers, and shipments with repeatable, persistent planning across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gpunter](https://clawhub.ai/user/Gpunter) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and their operators use this skill to create daily plans, carry forward unfinished work, log shipped items and blockers, and summarize progress across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Planner notes may contain secrets, sensitive personal details, or operational context that should not be persisted casually. <br>
Mitigation: Avoid placing secrets or sensitive personal details in planner notes, and review local memory files before sharing or committing them. <br>
Risk: Commands that update today's plan or overwrite priority tasks can replace useful planning context. <br>
Mitigation: Review the current daily plan before using update or priority-overwrite commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Gpunter/agent-daily-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown planning notes and concise command-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local daily and weekly planning records under memory/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact Version section) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
