## Description: <br>
Run one controlled daily project loop for a single active project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunbinnju-star](https://clawhub.ai/user/sunbinnju-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, planners, and project operators use this skill to advance one active project by one meaningful daily step while preserving project state, decisions, and the next action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can update project records and daily logs. <br>
Mitigation: Use it only when project writeback is intended, and review project_card_updates and writeback_payload before relying on saved state. <br>
Risk: The selected downstream agent or tool could take the project in the wrong direction if the task input is too broad or stale. <br>
Mitigation: Review selected_agent and task_input for sensitive projects, and keep each run limited to one bottleneck and one main action. <br>
Risk: Incomplete project state can make the daily run unsafe to continue. <br>
Mitigation: Require the project card, recent daily logs, and open questions before execution; stop with safe_to_proceed=false when state is missing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunbinnju-star/daily-loop-runner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Structured text with JSON-like fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes today_objective, selected_agent, task_input, execution_summary, findings, decisions, next_action, project_card_updates, writeback_payload, and safe_to_proceed.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
