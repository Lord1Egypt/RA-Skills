## Description:

Set up ESP32-S3-CAM modules as visual sensors for OpenClaw agents, covering hardware identification, firmware flashing, WiFi configuration, and HTTP camera server deployment with PlatformIO and Arduino.

This skill is ready for commercial/non-commercial use.

## Publisher:

[p697](https://clawhub.ai/user/p697)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure ESP32-S3-CAM hardware as OpenClaw vision sensors, flash camera firmware, expose capture and stream endpoints, and troubleshoot board or sensor issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live camera endpoints may expose images without authentication.

Mitigation: Use a dedicated IoT or isolated network, avoid port-forwarding the camera, and restrict access to trusted clients or add authentication before deployment.

Risk: The example fallback access point uses predictable credentials.

Mitigation: Replace fallback AP credentials with a unique strong secret or disable AP fallback.

Risk: Wildcard CORS can broaden browser access to camera endpoints.

Mitigation: Remove wildcard CORS unless it is required for a trusted integration.

Risk: Real WiFi credentials can be exposed if shared in source code.

Mitigation: Keep credentials out of shared files and use local placeholders, secret storage, or deployment-specific configuration.

## Reference(s):

- [ESP32-S3-CAM Setup Guide](references/setup-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/p697/skills/esp32-cam-eyes)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, INI, Python, and C++ code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes hardware-specific pin mappings, camera endpoint descriptions, firmware examples, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
