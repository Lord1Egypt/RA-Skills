## Description: <br>
Helps agents guide Clash Verge and mihomo REST API configuration, proxy selection, connection monitoring, rule management, and sample client usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gyaoshi](https://clawhub.ai/user/gyaoshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and operate a Clash Verge or mihomo controller through documented REST endpoints and example code. It is most useful for node switching, proxy inspection, connection management, delay testing, and controller maintenance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Clash Verge or mihomo controller exposed beyond localhost can allow unauthorized control of proxy settings if the secret or network boundary is weak. <br>
Mitigation: Keep the controller bound to 127.0.0.1 when possible, set a strong secret, and use firewall restrictions before enabling remote access. <br>
Risk: Mutating API actions can change routing behavior, delete connections, update configuration, upgrade components, or restart the controller. <br>
Mitigation: Require explicit user confirmation before node switching, configuration updates, connection deletion, upgrades, or restarts. <br>


## Reference(s): <br>
- [Clash Verge / mihomo API Reference](references/api_reference.md) <br>
- [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev) <br>
- [mihomo API Documentation](https://wiki.metacubex.one/api/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with YAML, bash, Python, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include REST endpoint descriptions and JSON request examples for a user-provided controller address and secret.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
