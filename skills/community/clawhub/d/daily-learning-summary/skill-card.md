## Description: <br>
Generates structured daily learning summaries for agents from local InStreet activity, ClawHub discovery, heartbeat, skill usage, and lessons-learned records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yu441374-oss](https://clawhub.ai/user/yu441374-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent developers and operators use this skill to create a dated Markdown archive of daily learning activity, including community interactions, discovered skills, skill effectiveness notes, and follow-up tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily summaries may persist sensitive local activity history from workspace memory logs. <br>
Mitigation: Keep memory/learning private or excluded from synced and shared repositories, and review generated summaries before sharing them. <br>
Risk: Generated learning summaries depend on the completeness and accuracy of local activity files. <br>
Mitigation: Verify important conclusions or follow-up tasks against the source logs before relying on the summary for planning or publication. <br>


## Reference(s): <br>
- [Daily Learning Summary on ClawHub](https://clawhub.ai/yu441374-oss/daily-learning-summary) <br>
- [Publisher profile on ClawHub](https://clawhub.ai/user/yu441374-oss) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown file written to memory/learning/YYYY-MM-DD.md, with optional shell commands for manual or heartbeat-triggered execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a persistent local daily summary from workspace memory logs; no third-party package dependencies are declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
