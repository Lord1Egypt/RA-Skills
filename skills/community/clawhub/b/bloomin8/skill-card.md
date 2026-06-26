## Description: <br>
Push images or markdown to a Bloomin8 e-ink photo frame via cloud API (async) or local BLE+LAN (instant). Scan nearby devices, check status, track delivery, change wake schedule, upload directly over WiFi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xander887](https://clawhub.ai/user/xander887) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to control Bloomin8 e-ink photo frames, choosing cloud API delivery for scheduled remote pushes or local BLE and LAN commands for immediate image upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use BLOOMIN8_TOKEN_* credentials for device-bound cloud API access. <br>
Mitigation: Confirm the intended device token before use, never reveal token values, and rotate or revoke a token if it may have been exposed. <br>
Risk: Local mode can scan nearby Bluetooth devices and probe device IPs on the user's LAN. <br>
Mitigation: Ask for explicit approval before BLE scans or local network probes, and state the target device name or IP before contacting it. <br>
Risk: The advanced upstream command can change cloud pull settings and transmit a token to the device over local HTTP. <br>
Mitigation: Use upstream changes only for intentional device configuration or debugging, and confirm the token, URL, and schedule before applying changes. <br>
Risk: The skill caches device names, IDs, IP addresses, and screen sizes outside the skill directory. <br>
Mitigation: Treat the cache as local device metadata, avoid sharing it, and refresh device info when IP addresses or ownership may have changed. <br>


## Reference(s): <br>
- [Bloomin8 ClawHub Skill](https://clawhub.ai/xander887/bloomin8) <br>
- [Bloomin8 OpenClaw Skill Repository](https://github.com/xander887/bloomin8-openclaw-skill) <br>
- [Bloomin8 Open API Help](https://einkshot-349134901638.us-central1.run.app/open-api/help) <br>
- [Bloomin8 Help Center](https://support.bloomin8.com/) <br>
- [Bloomin8 Website](https://www.bloomin8.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, curl examples, and optional JSON command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prepare or transmit image and markdown content to Bloomin8 cloud APIs or local devices; local CLI commands can emit structured JSON with --json.] <br>

## Skill Version(s): <br>
2.2.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
