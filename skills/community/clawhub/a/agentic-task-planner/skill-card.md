## Description:

Coordinates full clinical research analysis tasks by breaking them into staged evidence retrieval, cohort mapping, statistical analysis, export governance, and completion steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emergenceronearth](https://clawhub.ai/user/emergenceronearth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research operations teams use this skill to run a complete demo clinical research workflow with staged progress updates, mock data reads, evidence grounding, cohort analysis, statistical summaries, and export governance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the workflow with real patient data could create privacy, consent, de-identification, or export-governance exposure.

Mitigation: Install and run it only in the intended demo environment unless patient-data handling and monitoring-log controls are governed separately.

Risk: Progress updates posted to a local monitoring service may expose workflow status or research context in local logs.

Mitigation: Review the monitoring endpoint, access controls, and log-retention policy before deployment.

Risk: The skill coordinates downstream research steps, so stale mock data or incomplete downstream outputs could lead to misleading summaries.

Mitigation: Have qualified reviewers validate evidence, cohort mappings, statistical results, and export decisions before relying on outputs.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/emergenceronearth/skills/agentic-task-planner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown with staged summaries and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports progress to a local monitoring endpoint and reads fixed mock clinical research files.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
