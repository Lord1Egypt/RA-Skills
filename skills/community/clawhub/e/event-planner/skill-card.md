## Description: <br>
Plans outings by searching venues with Google Places API inputs and generating timed itineraries with venue details, walking information, warnings, and Google Maps links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[udiedrichsen](https://clawhub.ai/user/udiedrichsen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to plan nights out, meals, date nights, team outings, weekend days, and trips based on location, budget, party size, duration, and preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Google API key and sends event locations and preferences to Google services. <br>
Mitigation: Use a restricted Google API key with quota and billing controls, and avoid sensitive home, hotel, or private meetup addresses unless sharing them with Google APIs is acceptable. <br>
Risk: Venue hours, availability, travel times, and budget estimates may be incomplete or approximate. <br>
Mitigation: Review itinerary warnings and confirm venues, hours, routes, and prices before relying on the plan. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/udiedrichsen/event-planner) <br>
- [Google Places API endpoint](https://places.googleapis.com/v1) <br>
- [Google Directions API endpoint](https://maps.googleapis.com/maps/api/directions/json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown itinerary by default, with optional structured JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes timeline, venue details, walking distance and time, cost estimates, warnings, and a Google Maps route link.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
