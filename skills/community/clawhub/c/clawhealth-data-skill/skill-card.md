## Description:

ClawHealth lets an agent query hosted ClawHealth services for synced wearable data, nutrition records, goals, readiness signals, anomaly context, temporary panels, and feedback workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hengruizzzz](https://clawhub.ai/user/hengruizzzz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill after ClawHealth iOS setup to request health reports, readiness checks, nutrition summaries, mood tracking, anomaly context, and temporary visual panel links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses synced health, nutrition, profile, and mood data with a hosted service and a long-lived Agent API token.

Mitigation: Install only when the user intends to use ClawHealth with that data, protect the Agent API token like a password, and revoke it in the iOS app if exposed.

Risk: Temporary panel links may expose a user's health panel while the link is active.

Mitigation: Do not share temporary panel links, and treat them as private until they expire.

## Reference(s):

- [ClawHealth site](https://clawhealth.site)
- [ClawHub skill page](https://clawhub.ai/hengruizzzz/skills/clawhealth-data-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown prose with HTTP examples, temporary links, and structured nutrition summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include health reports, readiness guidance, nutrition estimates, setup steps, and temporary panel URLs.]

## Skill Version(s):

0.5.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
