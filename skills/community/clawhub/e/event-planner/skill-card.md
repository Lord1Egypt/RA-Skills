## Description:

Plan events (night out, weekend, date night, team outing, meals, trips) by searching venues via Google Places API. Auto-selects best restaurants, bars, activities based on location, budget, party size, and preferences. Generates detailed itinerary with timing and Google Maps link. Use when asked to plan an outing, create an itinerary, find places for events, or organize activities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[udiedrichsen](https://clawhub.ai/user/udiedrichsen)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to plan outings and itineraries by finding venues near a location, selecting restaurants, bars, or activities, and producing route-aware schedules with Google Maps links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Event locations, venue searches, route details, and the configured Google API key are sent to Google services and may incur API billing.

Mitigation: Use a scoped Google API key, monitor Google Cloud billing and quotas, and install only when this data sharing is acceptable.

Risk: Generated venue hours, availability, budgets, and routes may be inaccurate or incomplete.

Mitigation: Treat generated itineraries as planning suggestions and verify venue availability, costs, and route details before relying on them.

Risk: Some advertised trip, preference, date, or duration handling is not implemented accurately.

Mitigation: Avoid relying on those options until the skill is fixed or documented more accurately.

## Reference(s):

- [Event Planner ClawHub page](https://clawhub.ai/udiedrichsen/skills/event-planner)
- [udiedrichsen publisher profile](https://clawhub.ai/user/udiedrichsen)
- [Declared homepage](https://github.com/clawdbot/clawdbot)
- [Google Places API endpoint](https://places.googleapis.com/v1)
- [Google Directions API endpoint](https://maps.googleapis.com/maps/api/directions/json)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown itinerary by default, or structured JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes venue details, timing, walking distance or travel estimates, warnings, and a Google Maps route link.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
