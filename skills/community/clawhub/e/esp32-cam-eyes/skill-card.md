## Description: <br>
Set up ESP32-S3-CAM modules as visual sensors for OpenClaw agents, including hardware identification, firmware flashing, WiFi configuration, and HTTP camera server deployment with PlatformIO and Arduino. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[p697](https://clawhub.ai/user/p697) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use this skill to configure ESP32-S3-CAM hardware as physical vision sensors for OpenClaw agents, including flashing firmware, confirming the sensor type, and testing snapshot or stream endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The resulting camera server may expose private images on a local network or fallback hotspot if used without access controls. <br>
Mitigation: Use the camera only on a trusted isolated guest or IoT network, do not expose it to the internet, and add authentication or other access controls before using it in private spaces. <br>
Risk: Firmware examples require WiFi credentials, which could be accidentally committed or reused if real values are placed in source files. <br>
Mitigation: Keep credentials out of shared source, use placeholders in committed files, and replace the fallback access point password with a strong unique value. <br>


## Reference(s): <br>
- [ESP32-S3-CAM Setup Guide](references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and firmware code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes hardware-specific setup, flashing, camera endpoint, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
