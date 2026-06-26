## Description: <br>
基于用户当前位置，自动推荐三个周边城市作为本月周末出游目的地，筛选周末天气，并为每个目的地给出简洁的往返高铁或航班交通安排和预订链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[osrange](https://clawhub.ai/user/osrange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers use this skill to discover three nearby weekend destinations for the remaining weekends in the current month, filtered by suitable weather and practical train or flight options. It is useful for spontaneous short trips where the user wants destination ideas, transport choices, attraction highlights, and booking links in one Markdown response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan notes that the skill can install an unpinned global FlyAI CLI and may suggest sudo for npm installation. <br>
Mitigation: Prefer a manually reviewed and pinned FlyAI CLI installation, avoid sudo or global npm installation unless the package source is trusted, and verify the installed CLI before use. <br>
Risk: FlyAI searches may receive city-level travel details and trip preferences. <br>
Mitigation: Share only the location and preferences needed for the search, and review FlyAI data handling before using it for sensitive travel plans. <br>
Risk: Weather forecasts, ticket prices, availability, and booking links are time-sensitive and may become inaccurate. <br>
Mitigation: Verify forecasts, transport schedules, fares, and booking pages before making travel decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/osrange/flyai-monthly-travel-blindbox) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown travel recommendation cards with route tables, attraction highlights, booking links, and concise fallback guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses FlyAI CLI searches for weather, train, flight, attraction, and keyword lookups; outputs should remind users that forecasts and prices can change.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
