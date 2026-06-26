## Description: <br>
旅行盲盒 helps users set travel constraints, randomly selects an eligible surprise destination, and prepares a flight, hotel, and attraction plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers use this skill to reduce destination choice friction by setting budget, flight-time, schedule, and exclusion constraints, then receiving a surprise destination with a practical itinerary. Agents use it to collect travel preferences, search FlyAI travel data, and present a concise blind-box travel plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose setup commands that install or upgrade the FlyAI CLI globally. <br>
Mitigation: Review setup commands before execution and prefer a pinned, user-local FlyAI CLI installation. <br>
Risk: The artifact includes command examples that disable TLS verification. <br>
Mitigation: Do not run commands with TLS verification disabled unless the user has explicitly reviewed and accepted the risk. <br>
Risk: Travel profile details may persist in Memory or in ~/.flyai/user-profile.md. <br>
Mitigation: Save travel preferences only after user confirmation and only when the user is comfortable with persistent storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hello-ahang/flyai-travel-blindbox) <br>
- [Workflow](artifact/reference/workflow.md) <br>
- [Tools](artifact/reference/tools.md) <br>
- [User profile storage](artifact/reference/user-profile-storage.md) <br>
- [Random algorithm](artifact/reference/algorithm.md) <br>
- [Flight search](artifact/reference/search-flight.md) <br>
- [Hotel search](artifact/reference/search-hotel.md) <br>
- [POI search](artifact/reference/search-poi.md) <br>
- [Examples](artifact/reference/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured travel-plan details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include travel profile reads or updates when the user confirms persistence.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
