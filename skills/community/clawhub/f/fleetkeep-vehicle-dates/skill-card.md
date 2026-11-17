## Description:

Read authorised Fleetkeep vehicle records and summarise recorded MOT, tax, insurance and service dates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlucwright](https://clawhub.ai/user/jlucwright)

### License/Terms of Use:

MIT-0

## Use Case:

Fleetkeep account holders use this skill to check upcoming or overdue dates for vehicles they are authorised to view, based on saved records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or signing in to an untrusted CLI could expose vehicle data or credentials.

Mitigation: Confirm you trust the Fleetkeep CLI package, use the normal browser consent flow and minimum needed vehicle access, and keep credentials out of chat and command arguments.

Risk: Saved or missing dates could be mistaken for current official verification or proof of insurance coverage.

Mitigation: Identify dates as saved Fleetkeep records; label absent dates as not recorded and do not claim a fresh DVLA/DVSA check or infer coverage.

## Reference(s):

- [Fleetkeep vehicle dates on ClawHub](https://clawhub.ai/jlucwright/skills/fleetkeep-vehicle-dates)
- [Fleetkeep](https://fleetkeep.co.uk)
- [Fleetkeep account sign-in](https://fleetkeep.co.uk/login)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown summary of vehicle dates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows an explicit as-of date and labels missing dates as not recorded.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
