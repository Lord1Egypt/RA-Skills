## Description:

Query AdGuard Home instances for DNS statistics, blocked domains, client activity, service status, configuration, filter rules, TLS status, and recent query logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foxleoly](https://clawhub.ai/user/foxleoly)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and self-hosted DNS administrators use this skill to inspect AdGuard Home monitoring data and configuration from an agent without manually opening each instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured http:// AdGuard Home URLs can send administrator credentials over unencrypted HTTP.

Mitigation: Use HTTPS-only AdGuard Home URLs and avoid the documented http:// examples when configuring instances.

Risk: Administrator credentials may be stored in plaintext in adguard-instances.json.

Mitigation: Prefer environment variables or a secrets manager; if a local config file is used, keep it strictly local, set restrictive file permissions, and never commit it.

Risk: The skill can access sensitive DNS query history, client identifiers, filtering rules, and AdGuard control-plane data.

Mitigation: Install only in trusted workspaces and grant access only to AdGuard instances and accounts appropriate for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/foxleoly/skills/adguard-home)
- [Artifact-declared repository](https://github.com/foxleoly/adguard-home-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown-style command output with DNS statistics, lists, status messages, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include DNS query history, client identifiers, domains, filter rules, and service configuration from configured AdGuard Home instances.]

## Skill Version(s):

1.2.7 (source: evidence.release.version and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
