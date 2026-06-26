## Description: <br>
Complete VPN server setup from scratch, including VPS hardening, 3x-ui Xray proxy panel installation, VLESS Reality or VLESS TLS configuration, and Hiddify client connection guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DavydenkovM](https://clawhub.ai/user/DavydenkovM) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and external users use this skill to set up a fresh Ubuntu or Debian VPS as a hardened 3x-ui VPN/proxy server. It guides SSH access, firewall and system hardening, VLESS Reality or TLS setup, client connection, and final access-lockdown steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can give the agent root or server-admin authority on a VPS. <br>
Mitigation: Install only on a fresh, dedicated VPS and review downloaded installer commands and root-level commands before execution. <br>
Risk: The workflow includes risky credential handling paths, including passwords in generated guides or chat summaries. <br>
Mitigation: Redact passwords from generated guides and summaries, avoid plaintext password commands, and share credentials only through the minimum necessary channel. <br>
Risk: The optional fake cloud login fallback page can mislead users or visitors. <br>
Mitigation: Do not use the fake cloud login fallback; replace it with a truthful static page or omit the fallback page. <br>


## Reference(s): <br>
- [VLESS TLS Setup](references/vless-tls.md) <br>
- [Fallback Site (Nginx Stub)](references/fallback-nginx.md) <br>
- [ClawHub release page](https://clawhub.ai/DavydenkovM/3x-ui-vpn-setup) <br>
- [RealiTLScanner releases](https://github.com/XTLS/RealiTLScanner/releases) <br>
- [Hiddify client releases](https://github.com/hiddify/hiddify-app/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a local user guide with server access, panel access, and client connection details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
