## Description: <br>
Manage AI agent finances under budget constraints by tracking expenses, runway, revenue experiments, and forecasting survival metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gpunter](https://clawhub.ai/user/Gpunter) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to maintain local finance logs, monitor runway, track revenue experiments, and generate budget-aware survival forecasts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores budget, revenue, expense, and experiment notes in local workspace files. <br>
Mitigation: Install it only in workspaces where those local finance notes are appropriate, and review generated memory files for persisted content. <br>
Risk: Users could enter payment credentials, account numbers, or confidential business details into finance logs. <br>
Mitigation: Keep finance logs limited to non-sensitive operational notes and avoid recording credentials or confidential account details. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Gpunter/agent-survival-kit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown responses with local JSON finance records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update MEMORY.md, memory/projects.json, and memory/finances.json in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact Version section) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
