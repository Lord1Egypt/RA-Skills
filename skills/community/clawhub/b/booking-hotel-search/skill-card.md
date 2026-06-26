## Description: <br>
Search Booking.com for real-time hotel availability, prices, and room details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtnrabi](https://clawhub.ai/user/mtnrabi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to search hotel availability, compare prices and amenities, check room details, and return Booking.com links for selected destinations and dates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search details are sent to RapidAPI and the Booking Live API. <br>
Mitigation: Use the skill only for searches you are comfortable sharing with that API provider. <br>
Risk: RapidAPI key misuse could cause unauthorized usage or billing exposure. <br>
Mitigation: Use a dedicated RapidAPI key with quota or billing limits and monitor usage. <br>
Risk: Broad travel prompts may trigger external hotel-search API calls automatically. <br>
Mitigation: Disable the skill or narrow invocation when automatic travel-related API calls are not desired. <br>


## Reference(s): <br>
- [Booking Live API on RapidAPI](https://rapidapi.com/mtnrabi/api/booking-live-api) <br>
- [ClawHub skill page](https://clawhub.ai/mtnrabi/booking-hotel-search) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with inline curl commands and JSON-derived hotel fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RAPIDAPI_KEY and sends hotel search details to the Booking Live API through RapidAPI; bulk comparison is limited to five hotels.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, SKILL.md frontmatter, clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
