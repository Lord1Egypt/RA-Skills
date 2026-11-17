## Description:

Finds available meeting times in Caly using the user's event types, working hours, and availability, and presents options in the appropriate time zone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Caly users can find open times for a meeting, check their event types and schedules, and share available options before booking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting Caly grants access to account details, event types, schedules, and availability.

Mitigation: Confirm you trust the Caly connector and are comfortable granting OAuth read access before connecting.

Risk: Assuming free time from working hours alone or omitting the time zone can mislead invitees.

Mitigation: Offer only returned availability slots and show the time zone with every proposed time.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/devino/skills/caly-finding-meeting-times)
- [Caly connector installation](https://github.com/DevinoSolutions/mcp-servers/tree/main/caly#install)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Meeting options grouped by day, with a time zone shown for each time.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
