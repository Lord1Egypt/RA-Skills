## Description: <br>
Controls Daikin air conditioners over WiFi, including discovery, setup, status checks, and commands for power, mode, temperature, fan, swing, and advanced modes across multiple locations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leroylim](https://clawhub.ai/user/leroylim) <br>

### License/Terms of Use: <br>
GPL-3.0 <br>


## Use Case: <br>
External users and smart-home operators use this skill to discover, configure, monitor, and control Daikin air-conditioning units from an agent interface. It supports multi-device and multi-location setups where users need clear device selection and status feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved device configuration may contain internal IP addresses, API keys, or passwords. <br>
Mitigation: Keep data/devices.json private, remove it before sharing the workspace, and rotate device credentials after uninstalling or exposure. <br>
Risk: Network discovery can reveal local Daikin devices and related network details. <br>
Mitigation: Run discovery only on trusted networks and prefer manual device entry when network scanning is not appropriate. <br>
Risk: Control commands can change HVAC state for the wrong device when names are duplicated or ambiguous. <br>
Mitigation: Confirm location or device identity before executing commands when multiple devices share similar names. <br>


## Reference(s): <br>
- [Daikin Aircon OpenClaw Skill README](README.md) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [daikin-ts](https://github.com/leroylim/daikin-ts) <br>
- [pydaikin](https://github.com/fredrike/pydaikin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Plain text or Markdown responses with structured tool parameters and device status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local device configuration and send local-network requests to configured Daikin devices.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, skill.yaml, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
