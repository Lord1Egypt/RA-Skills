## Description: <br>
Monitors communication between the muzhe agent and named peer agents, checks message delivery, and reports normal or abnormal cross-agent communication status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nancliu](https://clawhub.ai/user/nancliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators managing a multi-agent workspace use this skill to test one-way and two-way agent messaging, inspect timeouts, and receive concise communication status reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact other agents and persist operational notes without clear user approval. <br>
Mitigation: Require confirmation before sending cross-agent messages, narrow activation conditions, and review or disable writes to MEMORY.md and HEARTBEAT.md unless persistent state is intended. <br>


## Reference(s): <br>
- [Agent Comm Monitor Skill Page](https://clawhub.ai/nancliu/agent-comm-monitor) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Concise Markdown status report with a table and operational notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include communication status, response timing, timeout notes, and follow-up guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
