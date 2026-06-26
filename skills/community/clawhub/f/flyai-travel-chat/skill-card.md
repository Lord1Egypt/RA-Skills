## Description: <br>
智能旅行规划助手，一个能够自主学习、持续成长的智能旅行规划助手，支持周末出游、家庭旅行、蜜月规划、拼假攻略等场景。能记住你的偏好，提供个性化推荐。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to turn open-ended trip ideas into personalized destination recommendations, itinerary drafts, and booking-oriented guidance. It supports profile-aware planning across weekend trips, family travel, honeymoons, vacation planning, flight, hotel, train, POI, and Marriott search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documentation normalizes disabling HTTPS certificate checks for FlyAI commands. <br>
Mitigation: Review generated commands before execution and do not allow HTTPS verification to be disabled unless the operator explicitly accepts that network risk. <br>
Risk: The workflow can install or globally upgrade the FlyAI CLI through npm. <br>
Mitigation: Avoid sudo installs and unpinned global upgrades in managed environments; install reviewed versions through approved package-management channels. <br>
Risk: The skill can persist travel preferences in Qoder Memory or a local profile file. <br>
Mitigation: Ask before saving preferences and avoid storing sensitive family, budget, accessibility, or trip-history details unless they are necessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hello-ahang/flyai-travel-chat) <br>
- [Core workflow](reference/core-workflow.md) <br>
- [Exploration framework](reference/exploration-framework.md) <br>
- [Scenarios](reference/scenarios.md) <br>
- [Personas](reference/personas.md) <br>
- [Memory system](reference/memory-system.md) <br>
- [User profile storage](reference/user-profile-storage.md) <br>
- [Tools](reference/tools.md) <br>
- [FlyAI commands](reference/flyai-commands.md) <br>
- [AI search](reference/ai-search.md) <br>
- [Keyword search](reference/keyword-search.md) <br>
- [Flight search](reference/search-flight.md) <br>
- [Hotel search](reference/search-hotel.md) <br>
- [POI search](reference/search-poi.md) <br>
- [Train search](reference/search-train.md) <br>
- [Marriott hotel search](reference/search-marriott-hotel.md) <br>
- [Marriott package search](reference/search-marriott-package.md) <br>
- [Examples](reference/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown conversation responses with inline shell commands and structured travel-planning sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live-search results, travel preference prompts, itinerary tables, cost estimates, booking links, and profile-save suggestions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
