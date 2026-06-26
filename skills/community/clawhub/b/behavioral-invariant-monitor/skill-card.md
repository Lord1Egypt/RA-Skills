## Description: <br>
Helps verify that AI agent skills maintain consistent behavioral invariants across repeated executions, including shifts based on execution count, environmental conditions, delayed activation triggers, performance drift, audit trails, and risk-proportional monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and agent operators use this skill to test selected skills or execution histories for behavioral drift, delayed activation patterns, side-effect changes, resource anomalies, and invariant violations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitoring selected targets can involve repeated execution of workflows that may touch private data or irreversible actions. <br>
Mitigation: Use the skill only on explicitly selected targets, preferably in a sandbox or dry-run environment. <br>
Risk: Behavioral audit logs may retain sensitive observations from monitored workflows. <br>
Mitigation: Decide in advance how audit logs will be stored, redacted, retained, and deleted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/andyxinweiminicloud/behavioral-invariant-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown behavioral invariant report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes violation logs, resource trend analysis, side-effect assessment, trigger-sensitivity results, and a consistency verdict.] <br>

## Skill Version(s): <br>
1.3.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
