## Description: <br>
You are an embedded systems and IoT engineering specialist with deep expertise in hardware programming, real-time systems, and edge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for embedded systems and IoT guidance across hardware platforms, low-level firmware, communication protocols, sensors, actuators, and edge computing. It provides implementation patterns and example code for microcontroller, gateway, and real-time control workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example firmware includes sample credentials and public or unauthenticated network patterns that are unsafe if reused unchanged. <br>
Mitigation: Replace sample credentials and require TLS plus authentication for MQTT, web, and control endpoints before deployment. <br>
Risk: Example OTA update flows can expose devices to untrusted firmware if copied without verification. <br>
Mitigation: Use signed firmware, verified HTTPS update sources, and explicit update approval or policy controls. <br>
Risk: Reset, reboot, relay, or other control actions in embedded examples can affect physical systems. <br>
Mitigation: Gate destructive or physical-control actions behind authenticated administrator checks, explicit confirmation, and appropriate physical safety controls. <br>


## Reference(s): <br>
- [Embedded Engineer Examples](references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mtsatryan/ah-embedded-engineer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with embedded code examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include firmware, gateway, protocol, testing, and security recommendations for embedded and IoT projects.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
