## Description: <br>
Monitor and manage Asus routers running AsusWRT/AsusWRT-Merlin firmware, including status checks, client/top-talker lists, presence detection, AiMesh topology, WAN/port/VPN/firmware diagnostics, raw AsusData dumps, and safe reboots for ZenWiFi, RT/GT/ExpertWiFi, Wi-Fi 6/6E/7, and other AsusWRT-based routers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rtaylorgraham](https://clawhub.ai/user/rtaylorgraham) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and home-network administrators use this skill to inspect AsusWRT router health, clients, WAN status, AiMesh topology, VPN status, firmware details, and perform controlled router administration tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses router administrator credentials and can access sensitive local network, client, VPN, and diagnostic data. <br>
Mitigation: Keep config.yaml out of source control, restrict file permissions, prefer HTTPS local router access when available, and avoid sharing raw or client JSON output. <br>
Risk: Presence detection can reveal whether named people or devices are connected to the local network. <br>
Mitigation: Configure presence detection only for devices and people the operator is authorized to track. <br>
Risk: Router reboot commands can interrupt internet access and disconnect devices. <br>
Mitigation: Require explicit user approval before rebooting; the provided command path requires a confirmation flag. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rtaylorgraham/asus-router) <br>
- [Home Assistant AsusRouter integration](https://github.com/Vaskivskyi/ha-asusrouter) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON, and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands return sensitive router, client, VPN, and local network data; JSON output is available for monitoring and automation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
