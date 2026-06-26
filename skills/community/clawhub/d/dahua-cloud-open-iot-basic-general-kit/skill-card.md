## Description: <br>
Provides a Python CLI and SDK for Dahua Cloud Open IoT device lifecycle management, including device, GB28181, SD card, Wi-Fi, callback subscription, ringtone, and image-decryption operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dolynkdeveloper](https://clawhub.ai/user/dolynkdeveloper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and IoT operations engineers use this skill to manage Dahua Cloud Open IoT devices and automate surveillance-device workflows through CLI commands or Python SDK calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform real Dahua Cloud device-management operations, including deletion, SD card formatting, Wi-Fi changes, and callback or subscription changes. <br>
Mitigation: Use least-privilege or test credentials first and manually verify target devices before executing state-changing operations. <br>
Risk: The skill requires sensitive Dahua Cloud credentials and may receive real device passwords during use. <br>
Mitigation: Store credentials in environment variables, avoid persistent secrets where possible, do not pass real passwords on command lines, and rotate exposed keys. <br>
Risk: Verbose API logging may expose operational details or sensitive request context during real deployments. <br>
Mitigation: Disable verbose logging for SDK integration and review logs before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/dolynkdeveloper/dahua-cloud-open-iot-basic-general-kit) <br>
- [Dahua Cloud Developer Platform](https://open.cloud-dahua.com/) <br>
- [API reference](references/api_reference.md) <br>
- [Quickstart](QUICKSTART.md) <br>
- [API coverage](API_COVERAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API call examples, environment-variable setup, and JSON response handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
