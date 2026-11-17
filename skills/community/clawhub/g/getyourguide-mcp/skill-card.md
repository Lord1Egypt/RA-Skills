## Description:

This skill should be used when the user asks about GetYourGuide tours, activities, or attraction tickets. Triggers on phrases like "find tours on GetYourGuide", "things to do in Paris", "skip-the-line tickets", "GetYourGuide reviews", "book an activity", or any request involving searching tours, activities, day trips, or attraction tickets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and trip planners use the skill to find GetYourGuide tours, activities, attraction tickets, available options, and customer reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Partner API key could be exposed through project configuration or logs.

Mitigation: Use project-specific configuration when practical and protect the partner API key.

Risk: The external npm package or a future version may introduce unexpected behavior.

Mitigation: Review and pin the package before running it.

## Reference(s):

- [GetYourGuide MCP npm package](https://www.npmjs.com/package/getyourguide-mcp)
- [GetYourGuide Partner Program](https://partner.getyourguide.com)
- [Project repository (listed in the skill instructions)](https://github.com/chrischall/getyourguide-mcp)

## Skill Output:

**Output Type(s):** [API data, JSON, Text]

**Output Format:** [Structured tour search results, details, options, and reviews, typically as JSON for the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only catalog information; booking takes place on GetYourGuide.]

## Skill Version(s):

2.2.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
