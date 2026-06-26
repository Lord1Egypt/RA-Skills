## Description: <br>
Car Log helps users record and review vehicle mileage, fuel, maintenance, and expense records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zengkang](https://clawhub.ai/user/zengkang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Drivers and personal vehicle owners use this skill to maintain a local log for multiple vehicles, including odometer readings, fuel purchases, maintenance events, and vehicle expenses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle, mileage, fuel, maintenance, and spending records are stored in a local SQLite database. <br>
Mitigation: Install only if local storage of these records is acceptable, avoid highly sensitive note content, and confirm the target vehicle and record before adding or deleting data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zengkang/car-log) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with concise list-style summaries and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local SQLite database at ~/.car-log/car_log.db by default.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
