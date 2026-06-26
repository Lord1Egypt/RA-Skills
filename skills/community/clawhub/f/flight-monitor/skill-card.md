## Description: <br>
Searches flight prices, formats one-way or round-trip results, records price history, manages recurring fare monitors, and can send low-price push notifications through configured services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JackZhao3925](https://clawhub.ai/user/JackZhao3925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to query flight fares, compare schedules, track route-specific price history, and create recurring alerts for fare thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved notification keys and travel history may be sensitive because the skill stores configuration and route history under ~/.workbuddy. <br>
Mitigation: Use revocable notification or API keys, keep local files access-controlled, and remove monitors or configuration files when they are no longer needed. <br>
Risk: Flight lookup and alert details may be sent to Ctrip and any optional push or API provider the user configures. <br>
Mitigation: Configure only trusted providers and avoid monitoring routes or dates that should not be disclosed to those services. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JackZhao3925/flight-monitor) <br>
- [City IATA Codes Reference](references/city_codes.md) <br>
- [Ctrip flight search](https://flights.ctrip.com/) <br>
- [zbape flight API documentation](https://api.zbape.com/doc/54) <br>
- [ServerChan notification service](https://sct.ftqq.com) <br>
- [PushDeer notification service](https://www.pushdeer.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and prose with shell command snippets, JSON command output, and notification setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write route history, monitor definitions, and notification configuration under the user's ~/.workbuddy directory.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
