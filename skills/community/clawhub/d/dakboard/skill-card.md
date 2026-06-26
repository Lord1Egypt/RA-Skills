## Description: <br>
Manage DAKboard screens, devices, and push custom display data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krisclarkdev](https://clawhub.ai/user/krisclarkdev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query DAKboard devices and screens, change a device's screen layout, and push metrics or JSON data to DAKboard display blocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The DAKBOARD_API_KEY can update screens and push display data. <br>
Mitigation: Use a dedicated or limited key where possible and rotate it if logs or shared environments may have exposed it. <br>
Risk: Metrics or fetch payloads may contain sensitive data that is sent to DAKboard or shown on a display. <br>
Mitigation: Avoid passing secrets or sensitive personal data as metric values or fetch content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krisclarkdev/dakboard) <br>
- [Publisher profile](https://clawhub.ai/user/krisclarkdev) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DAKBOARD_API_KEY; sends command arguments and the API key to dakboard.com.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
