## Description: <br>
Hotel search and pricing via the RollingGo CLI for destinations, dates, guest counts, star ratings, budgets, tags, distance filters, hotel details, room pricing, and hotel tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longcreat](https://clawhub.ai/user/longcreat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search hotels, compare current room pricing and policies, inspect hotel details, discover valid hotel tags, and produce booking or detail links for the user to complete a reservation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AIGOHOTEL API key, and passing it directly on the command line can expose the secret through shell history or process inspection. <br>
Mitigation: Prefer setting AIGOHOTEL_API_KEY through the environment or a secret manager, and avoid including the API key in prompts, logs, or command-line examples. <br>
Risk: Hotel searches and travel details are sent to the external AIGOHOTEL/RollingGo service. <br>
Mitigation: Use the skill only when the user is comfortable sharing the relevant travel details with that provider, and avoid sending unnecessary sensitive information. <br>


## Reference(s): <br>
- [find-hotel on ClawHub](https://clawhub.ai/longcreat/find-hotel) <br>
- [RollingGo Hotel service](https://mcp.agentichotel.cn) <br>
- [RollingGo API key application](https://mcp.agentichotel.cn/apply) <br>
- [RollingGo NPX Reference](references/rollinggo-npx.md) <br>
- [RollingGo UV Reference](references/rollinggo-uv.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured JSON result guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May surface booking URLs, hotel detail page links, room pricing, policies, availability, and CLI troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
