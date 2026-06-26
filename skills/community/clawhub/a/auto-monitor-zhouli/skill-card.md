## Description: <br>
Monitors server health on a recurring basis and proactively reports status, alerts, and suggested responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent check disk, memory, CPU load, network status, and process status, then report normal health or alert on abnormal conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to run ongoing system checks without clear scope, check frequency, alert destination, or stop controls. <br>
Mitigation: Configure explicit monitoring targets, check intervals, alert destinations, stop conditions, and read-only defaults before use. <br>
Risk: The artifact says auto-fixable issues can be handled immediately, which could trigger restarts, deletions, configuration changes, or other repair actions without approval. <br>
Mitigation: Require confirmation before any restart, deletion, configuration change, or other repair action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/auto-monitor-zhouli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown status reports, alerts, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concise normal-status reports and detailed anomaly alerts with suggested actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
