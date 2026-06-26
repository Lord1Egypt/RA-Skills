## Description: <br>
Guides agents through configuring mihomo proxy routing so mainland China servers can reach Binance API endpoints and troubleshoot common connection, DNS, and HTTP 451 failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eastnomoring](https://clawhub.ai/user/eastnomoring) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators managing mainland China servers use this skill to configure a local mihomo proxy, route Binance API traffic through a non-US VPS, and test signed or unsigned Binance API calls. <br>

### Deployment Geography for Use: <br>
China mainland origin servers with non-US proxy exit regions such as Japan, Hong Kong, Singapore, South Korea, or Europe. <br>

## Known Risks and Mitigations: <br>
Risk: The skill configures a persistent system proxy and routes sensitive financial API traffic through proxy infrastructure. <br>
Mitigation: Review before installation, use only trusted or self-managed proxy infrastructure, run services with least privilege, and avoid sending signed or private Binance requests through shared or untrusted nodes. <br>
Risk: The skill downloads and installs mihomo as part of the setup flow. <br>
Mitigation: Download mihomo only from an official source and verify checksums or signatures before installing it. <br>
Risk: Signed Binance API examples can expose account privileges if broad API keys are used. <br>
Mitigation: Use restricted Binance API keys, such as read-only keys unless trading is explicitly needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eastnomoring/binance-proxy-cn) <br>
- [MetaCubeX mihomo release download referenced by the skill](https://ghfast.top/https://github.com/MetaCubeX/mihomo/releases/download/v1.19.0/mihomo-linux-amd64-v1.19.0.gz) <br>
- [Binance API time endpoint used for connectivity testing](https://api.binance.com/api/v3/time) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, YAML, and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes proxy configuration examples, systemd service setup, API signing commands, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
