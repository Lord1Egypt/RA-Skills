## Description: <br>
An Improvement Planning Agent that creates actionable improvement plans for existing projects by reviewing analysis, prioritizing work, designing implementation phases, selecting agents, and defining validation criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill after project analysis to turn identified issues into a prioritized, phased improvement plan with agent assignments, task breakdowns, dependencies, validation criteria, and rollback considerations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Improvement plans may recommend follow-on code, infrastructure, or security changes that are inappropriate for the project context. <br>
Mitigation: Review the generated plan before authorizing implementation agents, with extra scrutiny for security settings, infrastructure changes, and newly proposed specialized agents. <br>


## Reference(s): <br>
- [Improvement Planner examples](references/examples.md) <br>
- [ClawHub release page](https://clawhub.ai/mtsatryan/ah-improvement-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown improvement plan with prioritized phases, agent assignments, validation criteria, rollback strategy, timeline, and success metrics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Planning-only output; review recommendations before authorizing follow-on agents to modify code, infrastructure, or security settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
