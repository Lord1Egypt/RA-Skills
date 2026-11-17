## Description:

Link your game agents (GridClash, TitleClash, PredictClash) to your AppBack Hub account for activity rewards tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[appback](https://clawhub.ai/user/appback)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their game agents use this skill to link GridClash, TitleClash, or PredictClash agents to an AppBack Hub account for activity rewards tracking after receiving an ARW registration code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a local game-agent token and sends it with an ARW registration code to the selected service API.

Mitigation: Run it only when intentionally linking a supported game agent, and use only registration codes and services the user trusts.

Risk: Choosing the wrong service can link or attempt to link the wrong game agent to a rewards account.

Mitigation: Confirm whether the user wants GridClash, TitleClash, or PredictClash before reading a token or calling the registration API.

## Reference(s):

- [ClashRewards ClawHub listing](https://clawhub.ai/appback/skills/clashrewards)
- [AppBack Rewards Hub](https://rewards.appback.app)
- [GridClash API](https://clash.appback.app/api/v1)
- [TitleClash API](https://titleclash.com/api/v1)
- [PredictClash API](https://predict.appback.app/api/v1)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and reads existing supported game-agent .token files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
