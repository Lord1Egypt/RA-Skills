## Description: <br>
Control and check a BYD vehicle using portable Python helper scripts built on pyBYD. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hiimivantang](https://clawhub.ai/user/hiimivantang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and vehicle owners use this skill to run repeatable BYD account actions from local scripts, including checking battery state, locking the vehicle, flashing lights or horn, and starting or stopping climate control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote lock, horn/lights, and climate commands can trigger real vehicle actions using stored BYD credentials. <br>
Mitigation: Run only with authorization, protect the .env file like a password, and require explicit confirmation or approval before command scripts execute. <br>
Risk: If no BYD_VIN or BYD_VEHICLE_ALIAS is configured, scripts use the first vehicle returned by the account. <br>
Mitigation: Set BYD_VIN or BYD_VEHICLE_ALIAS before running control scripts so actions target the intended vehicle. <br>
Risk: Battery monitoring output can be connected to unattended automation. <br>
Mitigation: Review threshold and delivery automation, and add confirmation before any vehicle action is triggered from a low-battery alert. <br>


## Reference(s): <br>
- [Setup](references/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or status output from Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts read BYD credentials and vehicle selection from environment variables and can print JSON battery snapshots or command status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
