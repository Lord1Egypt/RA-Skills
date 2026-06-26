## Description: <br>
Diagnose AWS cost anomalies and explain root cause in plain English when spend spikes unexpectedly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, cloud engineers, and FinOps responders use this skill to turn AWS cost anomaly alerts, billing diffs, and optional CloudTrail context into a concise incident explanation with likely root cause, evidence, impact, containment, and prevention guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AWS billing, anomaly, or CloudTrail inputs may contain sensitive account, spend, or operational details. <br>
Mitigation: Provide only the details needed for cost-incident analysis and avoid unnecessary secrets or unrelated logs. <br>
Risk: The artifact declares bash access even though the security guidance says the skill does not appear to need shell commands. <br>
Mitigation: Restrict or monitor shell access when installing or running the skill in environments that support tool controls. <br>
Risk: Root-cause and impact estimates can be incomplete or wrong when the supplied billing or CloudTrail context is partial. <br>
Mitigation: Review recommendations against authoritative AWS billing, Cost Explorer, and CloudTrail records before taking containment action. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown incident analysis with a Slack-ready summary and Jira ticket body] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes confidence level, root cause, evidence, estimated impact, containment action, prevention recommendation, and incident ticket text.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
