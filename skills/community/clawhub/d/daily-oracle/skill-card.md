## Description:

A background agent that generates a daily life prediction by analyzing local data and social signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[invelene](https://clawhub.ai/user/invelene)

### License/Terms of Use:


## Use Case:

External users install this skill to run a scheduled personal prediction agent that analyzes local calendar, message, file, and social signals and sends a concise desktop notification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently combine private messages, calendar details, Downloads metadata, and logged-in social account data.

Mitigation: Review before installation and grant Full Disk Access, calendar access, and browser-cookie access only if this level of local data access is acceptable.

Risk: Scheduled background execution provides limited user control at run time.

Mitigation: Prefer disabling the cron job, running in an isolated session, or requiring per-run approval before allowing the skill to execute.

Risk: The privacy posture depends on the model and execution environment being truly local.

Mitigation: Confirm local-only model execution and prevent third-party logging or external data transmission before use.

Risk: Using existing browser cookies can expose authenticated social pages.

Mitigation: Use an isolated browser profile or avoid granting browser-cookie access unless authenticated social-page access is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/invelene/skills/daily-oracle)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Plain-text desktop notification with setup commands and scheduling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs as a one-shot scheduled task and sends the prediction through the operating system notification mechanism.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
