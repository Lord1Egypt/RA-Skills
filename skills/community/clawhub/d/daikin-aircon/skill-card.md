## Description:

Control Daikin air conditioners over WiFi. Use when the user wants to control their Daikin AC units - turn on/off, set temperature, mode, fan speed, swing, or query status. Supports multiple devices with custom names across multiple locations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leroylim](https://clawhub.ai/user/leroylim)

### License/Terms of Use:

GPL-3.0

## Use Case:

External users and smart-home operators use this skill through OpenClaw to discover, configure, monitor, and control their own Daikin air conditioners over local WiFi.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control HVAC devices on the local network.

Mitigation: Install and use it only on networks and Daikin devices you own or administer, and review requested control actions before execution.

Risk: Device IP addresses and credentials such as API keys or passwords may be stored in a local JSON file.

Mitigation: Avoid shared workspaces for real credentials, restrict local file permissions, and clear stored credentials when changing or removing devices.

Risk: The skill can send network traffic to user-supplied addresses.

Mitigation: Validate that configured addresses are expected local Daikin device addresses before adding or updating devices.

Risk: Dependency versions are not fully pinned in package metadata.

Mitigation: Review and pin dependencies before deployment in managed or sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leroylim/skills/daikin-aircon)
- [OpenClaw](https://openclaw.ai)
- [daikin-ts](https://github.com/leroylim/daikin-ts)
- [pydaikin](https://github.com/fredrike/pydaikin)

## Skill Output:

**Output Type(s):** [Text, Configuration]

**Output Format:** [Plain text status, confirmation, and error messages; JSON device configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist device IP addresses, API keys, and passwords in a local JSON file and send local network requests to configured Daikin devices.]

## Skill Version(s):

1.0.0 (source: package.json, skill.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
