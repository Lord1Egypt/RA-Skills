## Description: <br>
日历管理工具包基础版 helps an agent create calendar events, schedule meetings, review daily or weekly agendas, configure recurring events, and work with Google, Apple, or Outlook calendar sync for individual and lightweight use cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage personal calendar workflows such as creating events, checking availability, reviewing schedules, and returning structured status results. It is intended for individual and lightweight scheduling tasks rather than team calendar administration or advanced analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar data, provider credentials, local cache, cloud sync data, callback URLs, or external APIs may be exposed or used too broadly if the agent is allowed to run vague calendar tasks. <br>
Mitigation: Use the skill only for explicit calendar tasks, review provider credential and cache access before execution, and avoid callback URLs unless the destination is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/calendar-toolkit-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON or text response examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return structured status, result data, execution logs, and error fields.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
