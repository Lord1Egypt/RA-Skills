## Description:

Get AI-powered match predictions for Premier League and Champions League including scores, next goal, and corners.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billychl1](https://clawhub.ai/user/billychl1)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to fetch FootballBin soccer predictions for Premier League and Champions League matches, including current or selected matchweeks and optional home or away team filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts a third-party FootballBin service and sends requested league, matchweek, and team filters.

Mitigation: Use the skill only when sharing those soccer query parameters with the FootballBin endpoint is acceptable.

Risk: Sports prediction output can be incomplete, stale, or incorrect for real-world decisions.

Mitigation: Treat predictions as informational and verify important match details against current sources before acting on them.

Risk: Formatted output depends on local curl and jq availability and network access to the FootballBin endpoint.

Mitigation: Confirm required binaries and outbound access are available before relying on the skill in an agent workflow.

## Reference(s):

- [FootballBin ClawHub Skill](https://clawhub.ai/billychl1/skills/footballbin-predictions)
- [FootballBin iOS App](https://apps.apple.com/app/footballbin/id6757111871)
- [FootballBin Android App](https://play.google.com/store/apps/details?id=com.achan.footballbinandroid)
- [FootballBin API Endpoint](https://api.footballbin.achaninc.net/mcp)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API Calls]

**Output Format:** [Plain text or JSON from a JSON-RPC API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq for formatted output; sends league, matchweek, and optional team filters to FootballBin.]

## Skill Version(s):

1.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
