## Description: <br>
反向穷游根据用户预算、出发城市和可出行天数，搜索交通、住宿和景点价格并生成三档旅行方案及预算拆解。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers use this skill to ask what destinations fit a stated budget, departure city, travel duration, and preferences. The agent searches FlyAI travel data, compares candidate destinations, and returns budget-aware itinerary options with cost breakdowns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses external FlyAI travel search services, so generated plans may depend on remote service availability and returned price data. <br>
Mitigation: Review current prices and booking details before relying on a generated itinerary or making purchases. <br>
Risk: The skill can retain travel preferences in memory or a local profile file. <br>
Mitigation: Store only profile details the user is comfortable keeping persistently, and honor requests to ignore or avoid saved preferences. <br>
Risk: The release security guidance warns against automatic global npm, sudo, or TLS-disabling commands. <br>
Mitigation: Use a pinned user-level CLI setup, keep certificate validation enabled, and require user review before running installation or network commands. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/hello-ahang/flyai-reverse-budget) <br>
- [Workflow](reference/workflow.md) <br>
- [Tool usage](reference/tools.md) <br>
- [Flight search reference](reference/search-flight.md) <br>
- [Hotel search reference](reference/search-hotel.md) <br>
- [POI search reference](reference/search-poi.md) <br>
- [User profile storage](reference/user-profile-storage.md) <br>
- [Example dialogue](reference/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown travel recommendations with budget tables, command snippets, and booking or detail links when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include price estimates, three-tier destination comparisons, itinerary details, and user preference updates.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
