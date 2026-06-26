## Description: <br>
Query ecobee thermostat data via Beestat API including temperature, humidity, air quality (CO2, VOC), sensors, and HVAC runtime. Use when user asks about home temperature, thermostat status, air quality, or heating/cooling usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjrussell](https://clawhub.ai/user/mjrussell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and home automation operators use this skill to query ecobee thermostat, sensor, air quality, and HVAC runtime information through the Beestat CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill outputs may reveal private home occupancy, temperature, air quality, thermostat, and HVAC usage details. <br>
Mitigation: Use the skill only in trusted sessions and avoid sharing command output in public transcripts, logs, or support tickets. <br>
Risk: The skill depends on an external npm CLI and a Beestat API key. <br>
Mitigation: Install only if you trust the beestat-cli package, store BEESTAT_API_KEY as an environment variable, and do not paste the key into prompts or command output. <br>


## Reference(s): <br>
- [Beestat](https://beestat.io) <br>
- [ClawHub Beestat release](https://clawhub.ai/mjrussell/beestat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the beestat CLI and BEESTAT_API_KEY environment variable.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
