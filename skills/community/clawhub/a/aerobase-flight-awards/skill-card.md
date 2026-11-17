## Description:

Search 24+ airline loyalty programs for award space with miles cost, seat availability, and canonical jetlag scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurosh87](https://clawhub.ai/user/kurosh87)

### License/Terms of Use:

MIT

## Use Case:

External travelers and travel-planning agents use this skill to find and compare flight award redemptions by route, date, cabin, miles cost, seat availability, and recovery context. It can also help create, list, update, and delete Aerobase award alerts when the user asks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an Aerobase API key for award searches and alert management.

Mitigation: Store the key in AEROBASE_API_KEY, avoid printing raw keys, and redact secrets in user-facing output.

Risk: Alert actions can create, deactivate, or delete Aerobase alerts.

Mitigation: Use clear user instructions for alert changes and summarize the intended action before making changes.

Risk: Users may share travel-account credentials or one-time authentication details unnecessarily.

Mitigation: Do not request passwords, OTPs, cookies, loyalty logins, or other travel-account secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kurosh87/skills/aerobase-flight-awards)
- [Aerobase homepage](https://aerobase.app)
- [Aerobase OpenClaw travel agent setup](https://aerobase.app/openclaw-travel-agent)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration instructions]

**Output Format:** [Markdown with concise ranked travel options and follow-up actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AEROBASE_API_KEY for Aerobase API access; can manage award alerts when requested.]

## Skill Version(s):

3.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
