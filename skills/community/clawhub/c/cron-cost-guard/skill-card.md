## Description:

Audit AI agent cron jobs for token cost risks, model-switch loops, and session isolation failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pouria3](https://clawhub.ai/user/pouria3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit scheduled AI agent jobs for token cost spikes, session binding conflicts, model-switch retry loops, and oversized injected prompts before or after incidents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Removing the wrong cron job could interrupt healthy automation.

Mitigation: Confirm the exact job ID and preserve relevant job configuration and log context before removing only the confirmed offending job.

Risk: Runaway retry loops can continue spending tokens if model-switch or session-binding errors are left active.

Mitigation: Audit consecutive errors, model-switch log patterns, and stale sessionKey bindings, then recreate affected jobs with isolated sessions and explicit agent/model settings.

## Reference(s):

- [Token Spike Diagnosis & Post-Incident Checklist](references/diagnosis.md)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Configuration guidance]

**Output Format:** [Markdown runbook with command examples and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cron health thresholds, session isolation checks, and post-incident steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
