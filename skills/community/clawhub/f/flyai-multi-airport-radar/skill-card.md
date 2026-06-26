## Description: <br>
同城不同价 helps travelers compare nearby departure airports and flexible dates, estimate cross-city transport costs, and choose the lowest total-cost flight option. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search flights from a primary city and nearby airports across flexible dates, then compare airfare, ground transport, and schedule tradeoffs before booking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can lead an agent to install or upgrade an unpinned global FlyAI CLI and may suggest sudo for permission issues. <br>
Mitigation: Review setup before use; use a verified, pinned CLI version and avoid sudo or global escalation unless the user explicitly approves it. <br>
Risk: The workflow includes a TLS bypass setting for flight searches. <br>
Mitigation: Remove the TLS-bypass setting and use normal certificate validation before running network calls. <br>
Risk: The skill can store travel preferences in Memory or ~/.flyai/user-profile.md. <br>
Mitigation: Ask for user consent before saving preferences, avoid sensitive details, and delete local profile data when it is no longer needed. <br>
Risk: Flight prices and availability can change after the skill generates a recommendation. <br>
Mitigation: Treat recommendations as time-sensitive and confirm the live price, itinerary, and booking details before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hello-ahang/flyai-multi-airport-radar) <br>
- [Workflow](reference/workflow.md) <br>
- [Flight Search Reference](reference/search-flight.md) <br>
- [Hotel Search Reference](reference/search-hotel.md) <br>
- [User Profile Storage](reference/user-profile-storage.md) <br>
- [Error Handling](reference/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown recommendations with price matrices, ranked options, booking links, and occasional FlyAI CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feizhu booking URLs, transport cost estimates, time-sensitivity notes, and optional user-preference memory updates.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
