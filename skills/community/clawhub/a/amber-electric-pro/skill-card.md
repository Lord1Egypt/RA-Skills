## Description:

Access real-time electricity prices, forecasts, and site details from Amber Electric, including current price data, 24-hour forecasts, and account site lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingmaxmmxweisun](https://clawhub.ai/user/kingmaxmmxweisun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve Amber Electric site information, current wholesale electricity prices, and 24-hour price forecasts for an Amber Electric account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses AMBER_API_KEY to read Amber Electric site, price, and forecast data.

Mitigation: Install only for Amber Electric customers, store the token securely, and remove or rotate it when access is no longer needed.

## Reference(s):

- [Amber Electric API base URL](https://api.amber.com.au/v1)
- [ClawHub skill page](https://clawhub.ai/kingmaxmmxweisun/skills/amber-electric-pro)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON responses with brief error messages for missing or invalid parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AMBER_API_KEY credential and a site_id for price and forecast actions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
