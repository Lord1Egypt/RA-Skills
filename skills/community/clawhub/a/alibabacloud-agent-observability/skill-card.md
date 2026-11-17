## Description:

Analyzes a user-specified Alibaba Cloud agent trace for task outcomes, failures, latency, token usage, collaboration, and tool quality, then produces an observation summary and self-contained HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and product teams use this skill to investigate a selected agent trace across Alibaba Cloud observability sources and explain behavior, failures, latency, token usage, and data gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Locally cached trace data and generated reports may expose sensitive messages, tool arguments, infrastructure details, or secrets recorded in telemetry; some cache entries persist indefinitely.

Mitigation: Use a private 0700 cache directory or disable caching with AGENT_OBS_NO_CACHE=1, and periodically delete cached facts and generated reports.

Risk: Installing or updating Alibaba Cloud CLI plugins can change the local execution environment.

Mitigation: Install only where Alibaba Cloud CLI updates and plugins are approved.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-agent-observability)
- [Scenario playbooks](references/scenario-playbooks.md)
- [Behavioral insight playbook](references/behavior-insight-playbook.md)
- [Report rendering specification](references/report-render-spec.md)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Markdown analysis summary and self-contained HTML observation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyzes a user-selected trace within a four-hour query window; identifies missing source coverage.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
