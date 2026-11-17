## Description:

智能旅行规划助手，支持周末出游、家庭旅行、蜜月规划、拼假攻略等旅行场景，并可记住用户偏好以提供个性化推荐。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to explore destinations, compare travel options, plan itineraries, and receive personalized travel recommendations based on stated or saved preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill evidence identifies unsafe network and installation practices, including TLS-bypass commands, global @latest installs, and possible elevated installation.

Mitigation: Review commands before use, avoid TLS bypass and sudo, and prefer a pinned trusted FlyAI CLI installed without elevated privileges.

Risk: The skill may persist detailed travel profiles with inconsistent consent controls.

Mitigation: Save profile data only after explicit user confirmation, limit stored details to necessary preferences, and keep or delete the local profile deliberately.

Risk: Travel recommendations can be incorrect, outdated, or incomplete when search results are empty or supplemented with general AI knowledge.

Mitigation: Verify time-sensitive travel details such as prices, schedules, visa rules, and opening hours against authoritative sources before booking.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hello-ahang/skills/flyai-travel-chat)
- [Memory System](reference/memory-system.md)
- [User Profile Storage](reference/user-profile-storage.md)
- [Core Workflow](reference/core-workflow.md)
- [Travel Scenarios](reference/scenarios.md)
- [Exploration Framework](reference/exploration-framework.md)
- [FlyAI Commands](reference/flyai-commands.md)
- [Tools](reference/tools.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Conversational Markdown with optional shell command blocks and structured itinerary sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include travel options, itinerary tables, estimated costs, booking links, follow-up questions, and profile-save prompts.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
