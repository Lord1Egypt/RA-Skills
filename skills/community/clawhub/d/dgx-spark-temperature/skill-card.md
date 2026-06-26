## Description: <br>
Reads and reports DGX Spark hardware temperature sensor values via SNMP for hardware health monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seitzbg](https://clawhub.ai/user/seitzbg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to run a DGX Spark temperature check and interpret hardware thermal sensor readings for health monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run for unrelated temperature questions and contact a specific network device. <br>
Mitigation: Narrow the trigger wording before use so only explicit DGX Spark hardware temperature requests invoke the skill. <br>
Risk: The skill uses a visible SNMP community string to query a specific host. <br>
Mitigation: Install only where querying the host is authorized, restrict file access, and prefer protected configuration or SNMPv3 before broader sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seitzbg/dgx-spark-temperature) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with plain-text shell output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports temperature sensor values in Celsius after converting milliCelsius SNMP readings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
