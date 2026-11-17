## Description:

Guides agents through hardening an Ubuntu or Debian VPS and installing 3x-ui with VLESS Reality or VLESS TLS so a user can connect through Hiddify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davydenkovm](https://clawhub.ai/user/davydenkovm)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and technical end users use this skill to configure a fresh VPS as a hardened 3x-ui VPN server and produce client connection guidance. It supports both no-domain VLESS Reality setup and domain-based VLESS TLS setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-privilege installer execution can change a server substantially and may execute unverified remote code.

Mitigation: Review the skill before use, run it only against a VPS you own or are authorized to configure, and prefer pinned and verified installer sources.

Risk: Subnet scanning may violate provider policy or local network rules.

Mitigation: Confirm scanning is permitted before running Reality scanner commands, and skip or adapt the scan when provider terms do not allow it.

Risk: Generated guide files may contain sudo passwords, panel credentials, and VPN connection details.

Mitigation: Avoid storing sudo or panel passwords in generated markdown, keep any guide file private, delete temporary copies, and rotate credentials after setup.

## Reference(s):

- [VLESS TLS Setup](references/vless-tls.md)
- [Fallback Site (Nginx Stub)](references/fallback-nginx.md)
- [3x-ui install script](https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)
- [RealiTLScanner release download](https://github.com/XTLS/RealiTLScanner/releases/latest/download/RealiTLScanner-linux-${SA})
- [Hiddify client releases](https://github.com/hiddify/hiddify-app/releases)
- [ClawHub skill page](https://clawhub.ai/davydenkovm/skills/3x-ui-vpn-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, JSON, configuration, and connection-link snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate a local markdown guide with server access details, panel access details, and VPN client setup instructions.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
