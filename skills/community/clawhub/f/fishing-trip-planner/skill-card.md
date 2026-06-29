## Description: <br>
Fishing Trip Planner helps an agent plan fishing trips by using map, weather, and tide APIs to generate route guidance, condition scoring, safety suggestions, and an HTML trip report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Anglers and trip-planning agents use this skill to gather route, weather, tide, and fishing-condition information for a planned fishing outing and produce a local HTML report with recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Amap and QWeather API keys and trip history locally. <br>
Mitigation: Use dedicated low-privilege API keys, avoid running the planner with elevated privileges, and remove ~/.fishing-planner/ when stored keys or history are no longer needed. <br>
Risk: Trip locations and dates are shared with map and weather providers during planning. <br>
Mitigation: Use the skill only for trips where sharing those details with Amap and QWeather is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/fishing-trip-planner) <br>
- [Server-resolved GitHub provenance](https://github.com/bettermen/fishing-trip-planner) <br>
- [Amap developer site](https://lbs.amap.com/) <br>
- [QWeather developer site](https://dev.qweather.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, HTML] <br>
**Output Format:** [Markdown-style agent guidance with shell commands and generated local HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Amap and QWeather API keys; stores configuration and trip history under ~/.fishing-planner/.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
