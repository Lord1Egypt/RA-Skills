## Description: <br>
Get daily weather and top news for multiple cities with one command, no API keys needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piaomiao123](https://clawhub.ai/user/piaomiao123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to generate a concise daily briefing with current weather for a selected city, Baidu trending topics, and a short daily tip from a local shell command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The shell script contacts wttr.in and Baidu over the network and may expose the requested city to those services. <br>
Mitigation: Use broad city names instead of sensitive or precise personal locations, and run only in environments where those outbound requests are acceptable. <br>
Risk: Documented weather-only and news-only examples are not implemented by the bundled script. <br>
Mitigation: Treat the current command as producing the full daily brief unless the script is updated and retested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/piaomiao123/daily-brief) <br>
- [wttr.in weather service](https://wttr.in) <br>
- [Baidu realtime trends API](https://top.baidu.com/api/board?platform=wise&tab=realtime) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text brief with weather, news headlines, and a daily tip] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and network access to wttr.in and Baidu; no API keys are required.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
