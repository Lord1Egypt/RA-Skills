## Description: <br>
Cron hygiene and cost-control for OpenClaw that audits scheduled jobs for duplicate purpose, noisy notifications, heavy cadence, repeated failures, and missing prerequisites while remaining report-only by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmonddantesj](https://clawhub.ai/user/edmonddantesj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw operators and developers use this skill to review cron job exports for duplicate jobs, noisy notifications, frequent schedules, failures, and missing prerequisites before making manual, approved schedule changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cron exports and generated reports may include operationally sensitive job names or error details. <br>
Mitigation: Treat cron exports and generated reports as sensitive and review them before sharing. <br>
Risk: Suggested cron schedule or delivery changes may be inappropriate for a specific environment if applied without review. <br>
Mitigation: Apply only exact changes that a user has manually reviewed and explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edmonddantesj/aoi-cron-ops-lite) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/edmonddantesj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise Markdown-style audit report with recommended actions and non-executed apply plan lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report-only; does not automatically update, disable, or remove cron jobs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
