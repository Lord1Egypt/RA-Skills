## Description: <br>
Control vehicles via DroneMobile (Firstech/Compustar remote start systems) for remote start, stop, lock, unlock, trunk, battery, and vehicle status requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BryanTegomoh](https://clawhub.ai/user/BryanTegomoh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to control and inspect DroneMobile-connected vehicles from an agent workflow after configuring DroneMobile credentials. It supports commands for remote start and stop, door lock and unlock, trunk opening, battery checks, and status retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real remote commands to a vehicle. <br>
Mitigation: Install only when the operator accepts DroneMobile credential use and confirms the intended vehicle before issuing commands. <br>
Risk: If DRONEMOBILE_DEVICE_KEY is missing or does not match, the script can fall back to the first vehicle on the account. <br>
Mitigation: Configure a specific DRONEMOBILE_DEVICE_KEY for multi-vehicle accounts and consider changing the script to fail closed on missing or mismatched keys. <br>


## Reference(s): <br>
- [DroneMobile ClawHub listing](https://clawhub.ai/BryanTegomoh/dronemobile) <br>
- [drone-mobile command success bug workaround](https://github.com/bjhiltbrand/drone_mobile_python/pull/18) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Configuration] <br>
**Output Format:** [Plain text status lines and error messages from a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DRONEMOBILE_EMAIL and DRONEMOBILE_PASSWORD, with optional DRONEMOBILE_DEVICE_KEY for multi-vehicle accounts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
