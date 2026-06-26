## Description: <br>
Search 24+ airline loyalty programs for award space with miles cost, seat availability, and canonical jetlag scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurosh87](https://clawhub.ai/user/kurosh87) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search award-flight availability, compare mileage cost and seat scarcity, and assess recovery quality for a route and date window. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Aerobase API key and sends route, date, cabin, and optional fare details to aerobase.app. <br>
Mitigation: Install only when that data sharing is acceptable, store the key in AEROBASE_API_KEY, and redact API keys from agent output. <br>
Risk: The skill can create, modify, and delete saved award alerts. <br>
Mitigation: Ask the user to confirm before creating, changing, or deleting saved alerts. <br>
Risk: Google Flights Pro wording may imply browser-powered behavior beyond the disclosed API flow. <br>
Mitigation: Treat that wording as marketing unless Aerobase provides a clearly documented and consented mechanism. <br>


## Reference(s): <br>
- [Aerobase homepage](https://aerobase.app) <br>
- [Aerobase OpenClaw travel agent setup](https://aerobase.app/openclaw-travel-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API calls] <br>
**Output Format:** [Markdown summaries with ranked award options and concise follow-up actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AEROBASE_API_KEY and sends route, date, cabin, and optional fare details to Aerobase API endpoints.] <br>

## Skill Version(s): <br>
3.3.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
