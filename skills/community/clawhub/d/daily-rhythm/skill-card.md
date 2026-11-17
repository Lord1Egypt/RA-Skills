## Description:

Automated daily planning and reflection system with morning briefs, wind-down prompts, sleep nudges, and weekly reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anthonyfrancis](https://clawhub.ai/user/anthonyfrancis)

### License/Terms of Use:


## Use Case:

External users, founders, and professionals use Daily Rhythm to configure automated morning briefs, evening wind-down prompts, sleep reminders, and weekly reviews that combine tasks, calendar context, optional ARR tracking, and personal planning notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Google Tasks, optional Stripe billing data, calendar data, and local planning memory that may include sensitive personal or business information.

Mitigation: Review before installing, keep credentials and generated memory files out of shared folders and repositories, and lock down file permissions.

Risk: Optional ARR tracking can use live Stripe billing credentials and persist derived customer and revenue data locally.

Mitigation: Use a restricted Stripe key where possible and avoid production credentials unless necessary.

Risk: Cron jobs can repeatedly run data sync and brief-generation scripts without interactive review.

Mitigation: Enable only scheduled jobs you understand, use paths and commands you have reviewed, and keep a clear disable procedure.

## Reference(s):

- [Daily Rhythm Configuration Guide](references/CONFIGURATION.md)
- [HEARTBEAT Template](assets/HEARTBEAT_TEMPLATE.md)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Stripe API Keys Dashboard](https://dashboard.stripe.com/apikeys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown brief and prompt text with shell command and configuration snippets; supporting scripts write local JSON state files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read Google Tasks, optional Stripe billing data, calendar ICS data, weather configuration, and local memory files when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
