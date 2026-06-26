## Description: <br>
Provides operational guidance for deploying and managing an OpenClaw gateway on an Alibaba Cloud server, including SSH tunneling, device pairing, Feishu integration, Browser Relay, and model configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoyoalphax](https://clawhub.ai/user/yoyoalphax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deploy, connect, pair, and maintain a private OpenClaw gateway on Alibaba Cloud. It is most useful when an agent needs step-by-step deployment, tunnel setup, Feishu connection, Browser Relay, model configuration, or troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports exposed real-looking passwords, API keys, app secrets, and gateway tokens. <br>
Mitigation: Rotate every referenced credential before use and replace hard-coded secrets with placeholders or secret-manager references. <br>
Risk: Gateway settings and browser-control setup may expose control surfaces beyond the intended user or network. <br>
Mitigation: Restrict gateway binding, allowed origins, and firewall rules to trusted hosts or networks before enabling remote access. <br>
Risk: The artifact includes commands that upload skills, restart services, and delete pairing state. <br>
Mitigation: Review each command before execution, use SSH keys and least-privilege accounts, and back up configuration and pairing data before destructive maintenance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yoyoalphax/aliyun-openclaw) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw device pairing documentation](https://docs.openclaw.ai/web/control-ui#device-pairing-first-connection) <br>
- [Alibaba Cloud Model Studio documentation](https://help.aliyun.com/zh/model-studio/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell command blocks and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include deployment commands and configuration values; users should replace or rotate any secrets before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
