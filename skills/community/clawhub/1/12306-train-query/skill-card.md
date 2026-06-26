## Description: <br>
Queries 12306 train-ticket availability for a departure station, arrival station, and travel date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuermos](https://clawhub.ai/user/fuermos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to check train availability between Chinese railway stations for a specified date. It helps surface train numbers, departure and arrival times, trip duration, and seat availability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script weakens HTTPS certificate validation for live 12306 requests. <br>
Mitigation: Use only for low-sensitivity ticket-availability lookup until valid HTTPS certificate verification is required. <br>
Risk: The script sends departure station, arrival station, and date to 12306. <br>
Mitigation: Do not use the skill for account login, ticket purchasing, payment, or other sensitive account activity. <br>
Risk: Redirect handling is not restricted to expected 12306 domains. <br>
Mitigation: Review redirect behavior before relying on results, and restrict redirects to expected 12306 domains in a future update. <br>


## Reference(s): <br>
- [12306 station name resource](https://kyfw.12306.cn/otn/resources/js/framework/station_name.js) <br>
- [12306 left-ticket query endpoint](https://kyfw.12306.cn/otn/leftTicket/queryG) <br>
- [ClawHub skill page](https://clawhub.ai/fuermos/12306-train-query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text console output with train numbers, stations, departure and arrival times, duration, and seat availability.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires departure station, arrival station, and date inputs; defaults are provided by the script when arguments are omitted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
