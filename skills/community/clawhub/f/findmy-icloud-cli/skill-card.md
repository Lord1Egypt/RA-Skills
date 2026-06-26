## Description: <br>
Find My iCloud CLI helps an agent query Apple Find My device and family-device locations through the pyicloud iCloud CLI while storing the Apple ID username in local state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rolandkakonyi](https://clawhub.ai/user/rolandkakonyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to check current locations, battery status, or device details for their own Apple devices or family-shared devices through a CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive Apple Find My location and device data. <br>
Mitigation: Install and use it only for your own or family-shared devices, keep local state private, and avoid sharing command output that contains coordinates or device identifiers. <br>
Risk: The local username state file is sourced as shell code. <br>
Mitigation: Avoid using the skill until the username file is parsed as data instead of sourced as shell code, and do not place untrusted content in the state file. <br>
Risk: The authentication flow asks the user to trust the local icloud/pyicloud CLI with Apple credentials. <br>
Mitigation: Verify the installed icloud/pyicloud CLI before login and do not store Apple passwords in the skill state files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return sensitive Apple device and location details from the local icloud CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
