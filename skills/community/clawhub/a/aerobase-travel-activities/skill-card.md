## Description: <br>
Discover near-airport and destination activities with ratings, reviews, and booking context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurosh87](https://clawhub.ai/user/kurosh87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel agents use this skill to find realistic attractions, tours, and restorative layover activities by destination context, budget, time, and traveler stamina. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Aerobase API key and travel search details to be sent to Aerobase. <br>
Mitigation: Install only if that data sharing is acceptable, store the key in AEROBASE_API_KEY, and redact raw API keys from all agent output. <br>
Risk: Users could be asked for unrelated travel account credentials or sensitive authentication data. <br>
Mitigation: Use only the documented Aerobase endpoints and never collect passwords, cookies, OTPs, loyalty credentials, or third-party travel account logins. <br>
Risk: Quota or service errors can interrupt activity search results. <br>
Mitigation: Handle 401, 403, 429, timeout, and 5xx responses as documented, retry at most once on transient failures, and return partial guidance with a next step when needed. <br>


## Reference(s): <br>
- [Aerobase homepage](https://aerobase.app) <br>
- [Aerobase OpenClaw travel agent setup](https://aerobase.app/openclaw-travel-agent) <br>
- [ClawHub skill page](https://clawhub.ai/kurosh87/aerobase-travel-activities) <br>
- [Publisher profile](https://clawhub.ai/user/kurosh87) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Text, Markdown, Configuration] <br>
**Output Format:** [Markdown or plain text recommendations with Aerobase API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AEROBASE_API_KEY; responses should redact raw API keys and keep recommendations concise.] <br>

## Skill Version(s): <br>
3.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
