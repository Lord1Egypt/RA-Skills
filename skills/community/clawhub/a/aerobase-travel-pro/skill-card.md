## Description: <br>
Full jetlag intelligence suite with award search, comparison, recovery plans, and itinerary analysis <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurosh87](https://clawhub.ai/user/kurosh87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and travel-planning agents use this skill to compare flights, search award availability, analyze itineraries, and generate jetlag-aware recovery guidance through the Aerobase Travel API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make recurring Aerobase API requests using the user's API key. <br>
Mitigation: Use a dedicated API key where possible, monitor quota and calls_remaining, and disable or avoid recurring checks unless the user explicitly requests them. <br>
Risk: Deal monitoring may proactively surface travel deals without clear opt-in or controls. <br>
Mitigation: Only enable deal monitoring after an explicit user decision, and confirm the user's home airport and notification preference before repeated checks. <br>
Risk: Itinerary details, arrival commitments, and meeting context may be sensitive. <br>
Mitigation: Avoid sending sensitive itinerary or commitment details unless the user trusts Aerobase and has approved sharing that information. <br>


## Reference(s): <br>
- [Aerobase API base](https://aerobase.app/api) <br>
- [ClawHub skill page](https://clawhub.ai/kurosh87/aerobase-travel-pro) <br>
- [Publisher profile](https://clawhub.ai/user/kurosh87) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline bash/curl commands and summarized API response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AEROBASE_API_KEY and observes the pro-tier request limit described by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
