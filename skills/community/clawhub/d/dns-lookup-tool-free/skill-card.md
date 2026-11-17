## Description:

DNS查询免费版 helps agents run dig-based DNS lookups for common record types and produce readable DNS diagnostic guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and automation workflows use this skill to check DNS records, compare resolver responses, troubleshoot DNS changes, and document basic lookup results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and its instructions mention unrelated database, coding, file, API, and general command capabilities beyond DNS lookup.

Mitigation: Use the skill only for DNS diagnostics, review proposed commands before execution, and narrow installed instructions to DNS-only behavior where possible.

Risk: DNS queries can expose queried domains or internal hostnames to the configured resolver.

Mitigation: Use approved DNS resolvers and avoid querying sensitive internal names from untrusted environments.

Risk: The free release does not support batch queries, JSON output, DNSSEC validation, DNS history, latency comparison, monitoring, or alerts.

Mitigation: Use it for single-domain manual diagnostics and choose a different reviewed tool for structured automation, DNSSEC validation, monitoring, or alerting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dns-lookup-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and summarized command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DNS record tables, resolver comparisons, status notes, and troubleshooting recommendations.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
