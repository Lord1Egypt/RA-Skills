## Description:

Manage a climate-generalizable raised-bed garden with planted crops, Open-Meteo weekly forecasts, sowing recommendations, watering-week plans, reminders, harvest windows, and garden memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobiaswestholm](https://clawhub.ai/user/tobiaswestholm)

### License/Terms of Use:

MIT-0

## Use Case:

External gardeners and allotment users use this skill to manage raised-bed crop records, watering plans, sowing recommendations, reminders, harvest tracking, and weekly garden conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains persistent local garden memory files.

Mitigation: Review the configured data directory and confirm state-changing actions before installation and routine use.

Risk: The skill calls Open-Meteo using configured coordinates.

Mitigation: Use only location data appropriate for the deployment context and disclose external weather lookups to users.

Risk: The skill may send weekly garden reports to configured Telegram recipients.

Mitigation: Review recipient configuration, disable unneeded delivery, and verify message destinations before enabling scheduled reports.

Risk: The unknown-crop flow can add generated crop facts to the persistent knowledge base without prior user review.

Mitigation: Require human review of newly generated crop knowledge before relying on it for planting, watering, or harvest decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobiaswestholm/skills/garden-assistance)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise natural-language guidance backed by JSON-producing CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local garden memory files and may send configured weekly reports through Telegram.]

## Skill Version(s):

1.0.2 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
