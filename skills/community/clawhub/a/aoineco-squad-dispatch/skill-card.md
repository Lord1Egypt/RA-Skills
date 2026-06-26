## Description: <br>
Routes tasks to suitable agents based on skills, availability, cost, dependencies, load, and priority. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmonddantesj](https://clawhub.ai/user/edmonddantesj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and multi-agent operators use this skill to plan which agent should handle each task, identify parallel versus sequential work, and estimate rough cost before dispatch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A dispatch plan may route work to a poorly matched agent or rely on rough cost and time estimates. <br>
Mitigation: Review generated plans before handing tasks to real agents or using the estimates for operational decisions. <br>
Risk: Task titles and descriptions may contain sensitive information if the planner is later connected to external model providers or session-spawning tools. <br>
Mitigation: Avoid secrets and sensitive data in task descriptions, and apply the same data-handling rules used for the connected agent runtime. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/edmonddantesj/aoineco-squad-dispatch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown dispatch plans and Python data objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes agent assignments, parallel execution groups, warnings, estimated cost, and estimated time.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
