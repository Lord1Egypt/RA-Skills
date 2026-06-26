## Description: <br>
Travel Planner helps agents research destinations, compare flight options, fetch weather, and produce a concise itinerary and budget report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nodermachine](https://clawhub.ai/user/nodermachine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to gather Xiaohongshu destination guidance, Fliggy flight options, weather forecasts, and budget details for trip planning. The resulting report is advisory and should be checked against live booking and weather sources before travel purchases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use browser automation against travel and social platforms, including reuse of logged-in sessions and sharing trip details with those services. <br>
Mitigation: Review before installing and use only with accounts, sessions, and trip data that the user intentionally authorizes for these services. <br>
Risk: Prices, itineraries, and weather can be advisory or estimated when live source data is unavailable. <br>
Mitigation: Verify live source data, timestamps, and booking terms before relying on the report for purchases or travel decisions. <br>
Risk: Persistent price monitoring is referenced without clear consent, stop conditions, or notification controls. <br>
Mitigation: Do not enable price monitoring unless the workflow has explicit user consent, a stop condition, and notification controls. <br>


## Reference(s): <br>
- [Skill README](artifact/README.md) <br>
- [Browser Flow Reference](artifact/references/browser-flow.md) <br>
- [Prompt Templates](artifact/references/prompts.md) <br>
- [Usage Examples](artifact/references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/nodermachine/fliggy-travel-planner) <br>
- [Xiaohongshu](https://www.xiaohongshu.com/) <br>
- [Fliggy](https://www.fliggy.com/) <br>
- [Ctrip](https://www.ctrip.com/) <br>
- [Weather.com.cn](http://www.weather.com.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown travel report with optional JSON intermediate data and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include itinerary tables, budget estimates, source links, weather summaries, and flight-price guidance.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
