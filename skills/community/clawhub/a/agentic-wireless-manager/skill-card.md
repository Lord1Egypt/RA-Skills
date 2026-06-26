## Description: <br>
AI-powered wireless network manager that helps agents diagnose Wi-Fi and hotspot connectivity, compare network quality, explain RF interference, and propose or run consent-based optimization actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to let an agent inspect local wireless conditions, explain slow or unstable connectivity, compare Wi-Fi and hotspot options, and guide network optimization with explicit user approval for privileged or disruptive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose or execute network-changing actions such as DNS changes, DHCP renewal, Wi-Fi switching, and adapter restarts. <br>
Mitigation: Use read-only scan mode first and require explicit confirmation before any privileged or disruptive network operation. <br>
Risk: Monitor and sentinel modes can run background wireless checks and presence sensing. <br>
Mitigation: Enable these modes only when intentionally requested, disclose what is being monitored, and stop them when continuous sensing is no longer needed. <br>
Risk: Local RF history, action logs, model weights, and spatial calibration data may be stored under ~/.net-intel. <br>
Mitigation: Review or delete ~/.net-intel when local wireless history should not be retained. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/danielfoojunwei/agentic-wireless-manager) <br>
- [Permissions and Controls](docs/PERMISSIONS_AND_CONTROLS.md) <br>
- [RF Environment Intelligence](docs/RF_ENVIRONMENT_INTELLIGENCE.md) <br>
- [SAC-LTC Architecture](docs/SAC_LTC_ARCHITECTURE.md) <br>
- [Cross-Platform Command Reference](docs/CROSS_PLATFORM_COMMANDS.md) <br>
- [Training Pipeline](docs/TRAINING_PIPELINE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command snippets, JSON examples, and concise plain-language recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed OS network commands, local scan summaries, SAC-LTC explanations, and consent-gated monitoring or optimization steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact package.json and CHANGELOG list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
