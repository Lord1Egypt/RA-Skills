## Description:

AOI Cron Ops (Lite) provides report-only OpenClaw cron hygiene and cost-control audits that detect duplicates, noisy notifications, heavy cadence, repeated failures, and missing prerequisites while requiring explicit approval before any schedule changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmonddantesj](https://clawhub.ai/user/edmonddantesj)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to audit OpenClaw cron job exports for duplicate purposes, noisy notifications, high-frequency schedules, repeated failures, and missing prerequisites. It produces report-only recommendations and requires explicit user approval before any schedule change is applied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron job names and error messages in the generated report may expose operational details.

Mitigation: Review the generated report before sharing it or applying any proposed cron changes.

Risk: Schedule recommendations could be inappropriate for a specific operational environment if applied without review.

Mitigation: Keep the Lite workflow report-only and require explicit approval for each concrete schedule change.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Concise Markdown-style audit report with recommended actions and an explicit apply plan.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report-only by default; proposed cron changes require explicit user approval before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
