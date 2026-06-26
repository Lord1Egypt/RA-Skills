## Description: <br>
Control Dyson air purifiers, fans, and heaters via local MQTT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmustier](https://clawhub.ai/user/tmustier) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and smart-home operators use this skill to have an agent control configured Dyson fans, purifiers, and heaters on the same WiFi network, including power, fan speed, oscillation, heat target, night mode, and status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup requires Dyson account credentials and stores device credentials locally. <br>
Mitigation: Run setup only when comfortable entering Dyson credentials, keep ~/.dyson/config.json private, and do not share or commit that file. <br>
Risk: Commands can change physical device power, airflow, oscillation, and heating settings. <br>
Mitigation: Review agent-proposed commands before execution, especially heat-related commands and target temperatures. <br>
Risk: Installing from an untrusted or moving source could run unexpected code. <br>
Mitigation: Install only from a trusted or pinned source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tmustier/dyson-cli) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text, JSON] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may affect physical device power, airflow, oscillation, heating, and locally stored device credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
