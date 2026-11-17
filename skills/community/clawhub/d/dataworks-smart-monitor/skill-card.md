## Description:

Monitors DataWorks task status, analyzes failures, classifies alerts by severity, and generates daily reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexmayanjun-collab](https://clawhub.ai/user/alexmayanjun-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Data engineers and operations teams use this skill to check DataWorks task runs, summarize success and failure counts, analyze error logs, classify P0/P1/P2 alerts, and prepare daily monitoring reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read DataWorks task metadata and failure logs that contain sensitive operational details.

Mitigation: Use a least-privilege read-only DataWorks identity and limit the monitored projects to the intended scope.

Risk: Failure logs may be sent to an LLM or Feishu destination without strong safeguards.

Mitigation: Redact and truncate logs before analysis or notification, and approve the Feishu channel and membership before enabling delivery.

Risk: Cloud credentials could be exposed if stored in TOOLS.md or source files.

Mitigation: Store secrets in environment variables or a secret manager and rotate any credentials that were committed or shared.

Risk: Scheduled monitoring could repeatedly process or distribute sensitive task data before the data flow is reviewed.

Mitigation: Review the data flow and notification destinations before enabling cron or other unattended execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text reports with JSON report references, shell command examples, configuration snippets, and operational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include alert severity labels, task status summaries, failure-analysis details, retry suggestions, and Feishu notification text.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
