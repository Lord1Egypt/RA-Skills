## Description: <br>
Manages a fn-knock gateway through its admin API for reverse proxy, DDNS, SSL/ACME, tunnels, scanner, whitelist, and related administration tasks; requires fn-knock on localhost:7998. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kci-lnk](https://clawhub.ai/user/kci-lnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this MCP server to let an AI assistant inspect and administer a self-hosted fn-knock gateway, including routing, certificates, DDNS, tunnels, scanner settings, sessions, logs, and maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an AI broad control over gateway, firewall, tunnel, DDNS, scanner, session, reset, delete, import, and gateway-setting operations. <br>
Mitigation: Install only when that level of administration is intended, and require explicit user approval before destructive or network-affecting changes. <br>
Risk: The fn-knock HMAC secret protects administrative access and can expose gateway control if mishandled. <br>
Mitigation: Keep the secret in an environment variable or chmod 600 credentials file, do not place it in MCP configuration, and review or pin the external package source before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kci-lnk/fn-knock-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown with JSON and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide or propose MCP tool calls against the configured fn-knock admin API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
