## Description: <br>
Flightroutes24 AI helps agents parse international flight requests, search demo or procurement fares, verify offers, and create orders after required user confirmations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mafly](https://clawhub.ai/user/mafly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travel users and their agents use this skill to search one-way or round-trip international airfare, refine carrier and departure-time preferences, compare direct and connecting options, and proceed through verified booking when procurement credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real flight orders. <br>
Mitigation: Require explicit confirmation of passenger information, itinerary, price, refund rules, and final order intent before running the order command. <br>
Risk: Passenger information and procurement credentials may be stored locally. <br>
Mitigation: Prefer environment variables or a secure secret store, avoid sharing secrets in chat, and clear local cache files after bookings. <br>
Risk: Maintainer-only skip-auth and skip-IP-whitelist switches can bypass normal controls. <br>
Mitigation: Use those switches only in isolated testing and confirm they are disabled before production or shared use. <br>
Risk: The packaged local settings include Git remote add and push permissions unrelated to flight booking. <br>
Mitigation: Remove the packaged Git publishing permission file unless it is explicitly required for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mafly/fr24-ai) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mafly) <br>
- [Flightroutes24](https://www.flightroutes24.com/) <br>
- [README.en.md](README.en.md) <br>
- [Booking flow](references/booking.md) <br>
- [Output rules](references/output-rules.md) <br>
- [User procurement key setup](references/user-appkey-config.md) <br>
- [Search parameters](references/search_params.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON stdout for agent execution results, with concise Markdown or text summaries for user-facing guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Only userView and message are intended for user-visible output; agentOnly data, raw API payloads, local cache paths, and secrets remain internal.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
