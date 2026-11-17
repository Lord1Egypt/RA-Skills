## Description:

Run DNS, domain, email security, SSL, WHOIS, and network diagnostics through the dnsrobot.net API without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dnsrobot](https://clawhub.ai/user/dnsrobot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, security teams, and support engineers use this skill to inspect DNS records, domain health, email authentication, SSL/TLS certificates, WHOIS data, HTTP headers, ports, and IP reputation for assets they own or are authorized to test.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried domains, IP addresses, hostnames, mail-server names, and full URLs are sent to dnsrobot.net.

Mitigation: Avoid submitting secrets, tokenized URLs, private paths, or sensitive internal targets unless this data sharing is approved.

Risk: SMTP, HTTP header, subdomain, blacklist, SSL, and port checks may actively probe hosts.

Mitigation: Use active checks only for systems you own or have authorization to test.

## Reference(s):

- [DNS Robot homepage](https://dnsrobot.net)
- [DNS Robot tools](https://dnsrobot.net/all-tools)
- [ClawHub DNS Robot skill](https://clawhub.ai/dnsrobot/skills/dnsrobot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl examples and JSON or NDJSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl. Some endpoints return newline-delimited JSON streams.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
