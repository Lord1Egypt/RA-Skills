## Description: <br>
Install and configure the security-related plugins required by OpenClaw, including the `ai-assistant-security-openclaw` plugins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinjianfenghzau-wq](https://clawhub.ai/user/qinjianfenghzau-wq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, authorize, and configure the ClawSentry security plugin for an OpenClaw environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and configures an external OpenClaw security plugin and links the host to a remote ClawSentry backend. <br>
Mitigation: Install only when the publisher, the @omni-shield plugin package, and the ClawSentry backend are trusted; review OpenClaw plugin configuration after use. <br>
Risk: The bundled script derives a device fingerprint from host and network-interface data for account binding. <br>
Mitigation: Avoid running it on shared or sensitive hosts, and prefer a release that removes hostname and MAC-derived fingerprinting. <br>
Risk: Login state, polling logs, and OpenClaw configuration may contain login tokens, device fingerprints, ApiKey, or AppId values. <br>
Mitigation: Review and protect generated .state files and plugin configuration, redact logs before sharing, and rotate credentials if they may have been exposed. <br>
Risk: The script can restart the OpenClaw gateway after authorization. <br>
Mitigation: Run it during an acceptable maintenance window and prefer a release that asks before restarting the gateway. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qinjianfenghzau-wq/anhfabh1-test) <br>
- [Volcengine](https://www.volcengine.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and login-link guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local state files, update OpenClaw plugin configuration, and restart the OpenClaw gateway.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
