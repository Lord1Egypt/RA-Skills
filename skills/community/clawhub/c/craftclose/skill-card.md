## Description: <br>
AI-powered Minecraft server monitoring with crash detection, auto-restart, and smart alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ginhooser-cyber](https://clawhub.ai/user/ginhooser-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Minecraft server operators use CraftClose to monitor Java/Paper server health, diagnose crashes and performance issues, configure alerts, analyze logs with Gemini, and manage Pterodactyl panel servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CraftClose can control Minecraft servers through SSH, RCON, or Pterodactyl panel operations. <br>
Mitigation: Use dedicated low-privilege server and API credentials, keep restart limits or confirmations enabled, and verify actions before enabling production automation. <br>
Risk: Configuration may contain secrets such as RCON passwords, Pterodactyl API keys, alert webhook URLs, Telegram tokens, and Gemini API keys. <br>
Mitigation: Protect craftclose.yml, prefer environment variables for API keys, and avoid sharing logs or configuration files that expose credentials. <br>
Risk: Logs or alerts may be sent to Discord, Telegram, or Gemini during monitoring and AI analysis. <br>
Mitigation: Review what server logs and alert content may be transmitted before connecting third-party services. <br>


## Reference(s): <br>
- [CraftClose ClawHub listing](https://clawhub.ai/ginhooser-cyber/craftclose) <br>
- [CraftClose npm package](https://www.npmjs.com/package/craftclose) <br>
- [CraftClose Discord community](https://discord.gg/bJDGXc4DvW) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the craftclose CLI and a craftclose.yml configuration with appropriate server, alerting, and optional Gemini credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
