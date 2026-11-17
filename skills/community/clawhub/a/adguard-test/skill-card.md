## Description:

Query AdGuard Home instances for DNS statistics, blocked domains, client activity, service status, filter rules, query logs, and configuration details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foxleoly](https://clawhub.ai/user/foxleoly)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and self-hosted infrastructure administrators use this skill to inspect AdGuard Home health, DNS activity, blocking trends, client usage, filters, query logs, and TLS status from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrator credentials and session cookies may be sent to AdGuard Home over unencrypted HTTP.

Mitigation: Configure only HTTPS AdGuard Home URLs and verify TLS is enabled before use.

Risk: Plaintext AdGuard credentials in adguard-instances.json can expose administrator access in local or shared workspaces.

Mitigation: Prefer environment variables or a secrets manager, avoid real admin passwords in configuration files, and restrict any local config file permissions.

Risk: Query log and client commands can reveal browsing history, internal hostnames, IP addresses, and network topology.

Mitigation: Limit use to trusted workspaces and redact DNS query, client, and configuration output before sharing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/foxleoly/skills/adguard-test)
- [Publisher profile](https://clawhub.ai/user/foxleoly)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-style text with command examples, configuration snippets, DNS statistics, status summaries, query logs, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive DNS query history, client identifiers, internal network details, and AdGuard Home configuration values returned by the configured instance.]

## Skill Version(s):

1.2.1 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
