## Description: <br>
Boss Agent coordinates multi-agent work by assigning tasks to Ass Agent and Ops Agent, tracking their status, and summarizing progress for the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pikaqiuyaya](https://clawhub.ai/user/pikaqiuyaya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and operators use this skill to coordinate work across Ass and Ops agents, delegate tasks, check agent status, and receive a consolidated progress report. It is intended for environments where cross-agent coordination and controlled visibility into agent sessions are expected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate and inspect other agents' conversations, memory, status, and task channels. <br>
Mitigation: Define exactly which agents and sessions it may access, and require explicit approval before sensitive reads or operational delegation. <br>
Risk: Delegated operational work may affect other agents' configuration, services, or data. <br>
Mitigation: Require user authorization before modifying configurations, restarting services, or deleting agent data. <br>
Risk: Summaries may expose unrelated private history from other agents. <br>
Mitigation: Limit summaries to task-relevant context and avoid including private history that was not needed for the requested work. <br>


## Reference(s): <br>
- [Boss Agent on ClawHub](https://clawhub.ai/pikaqiuyaya/boss-agent) <br>
- [pikaqiuyaya publisher profile](https://clawhub.ai/user/pikaqiuyaya) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with task breakdowns, delegated messages, status summaries, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cross-agent task assignments, progress summaries, and operational status checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
