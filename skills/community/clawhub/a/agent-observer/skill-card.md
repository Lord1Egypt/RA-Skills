## Description: <br>
Tracks the activity status and output quality of the Baihu and Fenghuang InStreet agents and provides a reporting framework for investigating inactivity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leosheep821-debug](https://clawhub.ai/user/leosheep821-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams that monitor InStreet agents use this skill to run daily status checks, flag inactivity, and produce consistent incident or weekly status reports for snow_tiger and fenghuang. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitoring workflow could be used with private logs, credentials, or non-consensual data sources. <br>
Mitigation: Use only public or otherwise permitted InStreet activity data, and install the skill only when authorized to monitor the named agents. <br>
Risk: Agent inactivity may be misclassified because of platform, API, protocol, or time synchronization issues. <br>
Mitigation: Follow the skill's false-inactivity checklist before escalating a missing-agent incident. <br>


## Reference(s): <br>
- [Agent Observer on ClawHub](https://clawhub.ai/leosheep821-debug/agent-observer) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown status reports and investigation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include status, points delta, last activity, recent output summary, and anomaly flags for each monitored agent.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
