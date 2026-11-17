## Description:

Helps people import recurring commitments, find free time, plan outings around travel and weather, and manage events in their iCloud calendars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alan1527061](https://clawhub.ai/user/alan1527061)

### License/Terms of Use:

MIT-0

## Use Case:

People using Apple Calendar with an agent can import class schedules or work shifts, check availability, plan travel-aware outings, and add or cancel calendar events after confirming changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Canceling by UID can delete unrelated Apple Calendar events despite the skill's stated deletion safeguards.

Mitigation: Avoid cancel --uid until exact skill-created event ownership and calendar scoping are enforced; review events and confirm before deleting.

Risk: Stored calendar credentials and personal schedule or home-location details may be exposed.

Mitigation: Use a revocable Apple app-specific password, keep data/profile.json private, and use a dedicated plans calendar.

Risk: Trip planning can share destinations and coordinates with weather, geocoding, or routing services.

Mitigation: Review privacy implications before using trip planning and avoid supplying sensitive locations.

## Reference(s):

- [Apple Calendar Pal on ClawHub](https://clawhub.ai/alan1527061/skills/apple-calpal)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Conversational planning guidance and calendar event specifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [With user confirmation, can create or cancel iCloud calendar events.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
