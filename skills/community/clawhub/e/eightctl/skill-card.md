## Description: <br>
Control Eight Sleep pods (status, temperature, alarms, schedules). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate an Eight Sleep pod through the eightctl CLI, including status checks, temperature changes, alarms, schedules, audio, and base controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a physical Eight Sleep pod, including commands that change temperature, alarms, schedules, audio, base position, or power state. <br>
Mitigation: Require explicit user confirmation before every command that changes device state. <br>
Risk: The skill depends on sensitive Eight Sleep account credentials. <br>
Mitigation: Protect the configured credentials and avoid exposing EIGHTCTL_EMAIL, EIGHTCTL_PASSWORD, or ~/.config/eightctl/config.yaml in logs, prompts, or shared files. <br>
Risk: The upstream Eight Sleep API is unofficial and rate-limited. <br>
Mitigation: Avoid repeated logins and excessive polling, and review or pin the upstream eightctl CLI version before installation. <br>


## Reference(s): <br>
- [Eightctl homepage](https://eightctl.sh) <br>
- [ClawHub skill page](https://clawhub.ai/steipete/eightctl) <br>
- [Publisher profile](https://clawhub.ai/user/steipete) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires eightctl CLI authentication and explicit confirmation before commands that change device state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
