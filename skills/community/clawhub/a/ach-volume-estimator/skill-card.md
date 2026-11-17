## Description:

Estimates Dwolla's end-of-month ACH transaction volume from daily KPI emails by extracting transaction and business-day inputs, calculating a per-business-day rate, and projecting monthly totals with a US Federal Reserve holiday calendar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daveglaser0823](https://clawhub.ai/user/daveglaser0823)

### License/Terms of Use:

MIT-0

## Use Case:

Business operators and analysts use this skill to estimate month-end ACH transaction volume from daily KPI email data and PDF dashboard exports. It also supports ACH summary reporting and dashboard updates when the user has approved access to the relevant mailbox, attachments, and local report files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may access named Gmail KPI emails and PDF attachments containing sensitive business data.

Mitigation: Install only after confirming mailbox and attachment access is intended, and limit credentials or tool access to the approved KPI workflow.

Risk: Bundled scripts include revenue forecasting, revenue calibration file reads, external SOFR fetching, and dashboard writes beyond the basic ACH estimate.

Mitigation: Remove or disable revenue-related scripts and SOFR access when approving the skill only for ACH volume estimation.

Risk: Cron or automated dashboard use can repeatedly read business data and write local report artifacts.

Mitigation: Require explicit approval before scheduled execution and confirm local dashboard/report paths before allowing writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daveglaser0823/skills/ach-volume-estimator)
- [Publisher profile](https://clawhub.ai/user/daveglaser0823)
- [Federal Reserve holiday schedule](https://www.federalreserve.gov/aboutthefed/k8.htm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, one-line text estimates, optional JSON script output, and local dashboard/report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read approved Gmail KPI emails and attachments, calculate forecasts from ACH transaction inputs, and write local ACH report or dashboard files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
