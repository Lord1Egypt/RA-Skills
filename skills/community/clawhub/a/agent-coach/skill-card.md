## Description:

Register with Agent Coach (upskill.coach), set one north-star goal, get vetted skills and MCP servers matched to it, and check in daily to get a keep / temporary / remove verdict on each installed item. Use when your owner wants to know which skills and tools are worth keeping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[f-o-x11](https://clawhub.ai/user/f-o-x11)

### License/Terms of Use:

MIT-0

## Use Case:

AI agent users use Agent Coach to define a measurable goal, receive skill and MCP server recommendations, and review adopted items through daily check-ins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service receives the agent's display name, platform, goals, stage, reported numbers, and short notes during use.

Mitigation: Share only information approved by the owner; omit secrets, API keys, customer data, and email contents, as the skill directs.

Risk: The API key returned during registration authorizes subsequent account requests and is shown only once.

Mitigation: Store the key in private memory and include it only in authenticated requests to Agent Coach; never expose it in reports or other tools.

## Reference(s):

- [Agent Coach](https://upskill.coach)
- [Agent Coach setup guide](https://upskill.coach/start?ref=clawhub)
- [Agent Coach verdict rules](https://upskill.coach/api/v1/rules)
- [Agent Coach MCP server](https://upskill.coach/mcp?ref=clawhub)

## Skill Output:

**Output Type(s):** [Guidance, Text, API responses]

**Output Format:** [Natural-language recommendations and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Goal-based skill and MCP recommendations, daily check-in summaries, and keep / temporary / remove verdicts.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
