## Description: <br>
This skill helps travel companions compare travel styles before a trip, identify likely conflicts, and produce a compatibility report with compromise recommendations based on FlyAI travel search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to run an interactive travel-style questionnaire, score compatibility across itinerary pace, lodging, photography, food, and spending preferences, then generate a practical trip agreement and compromise plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read or persist personal travel preferences in Qoder Memory or ~/.flyai/user-profile.md. <br>
Mitigation: Ask for user confirmation before saving preferences, and tell users they can review or delete ~/.flyai/user-profile.md when they do not want persistent travel-profile data. <br>
Risk: The workflow asks the agent to install or upgrade a global FlyAI CLI package. <br>
Mitigation: Have the user approve any global npm install manually and verify the package source before installation. <br>
Risk: The artifact documents an unsafe TLS workaround using NODE_TLS_REJECT_UNAUTHORIZED=0. <br>
Mitigation: Avoid disabling TLS verification during normal use; use that workaround only as an explicit, temporary troubleshooting step after user approval. <br>
Risk: Generated booking links could be mistaken for purchase approval. <br>
Mitigation: Present booking links as reviewable options and require the user to complete and approve any booking action themselves. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hello-ahang/flyai-companion-matcher) <br>
- [Workflow](reference/workflow.md) <br>
- [Compromise Strategies](reference/strategies.md) <br>
- [User Profile Storage](reference/user-profile-storage.md) <br>
- [Examples](reference/examples.md) <br>
- [AI Search Reference](reference/ai-search.md) <br>
- [Keyword Search Reference](reference/keyword-search.md) <br>
- [Hotel Search Reference](reference/search-hotel.md) <br>
- [POI Search Reference](reference/search-poi.md) <br>
- [Flight Search Reference](reference/search-flight.md) <br>
- [Train Search Reference](reference/search-train.md) <br>
- [Marriott Hotel Search Reference](reference/search-marriott-hotel.md) <br>
- [Marriott Package Search Reference](reference/search-marriott-package.md) <br>
- [Self-Growth Notes](reference/self-growth.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with compatibility scores, conflict warnings, compromise recommendations, optional FlyAI command snippets, images, and booking links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or save a travel preference profile when the user approves; booking links should be treated as options, not purchase approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
