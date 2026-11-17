## Description:

DNS查询工具 helps agents resolve hostnames and inspect DNS records with the bind-utils `dig` command for domain troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IT operators, and automation workflows use this skill to ask an agent for DNS lookups, inspect DNS record responses, and troubleshoot domain-resolution issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad command and file authority without clearly limiting how those powers are used.

Mitigation: Install it only in an agent environment where command execution is controlled, and restrict use to DNS lookup requests.

Risk: Free-form instructions could cause behavior outside the intended DNS lookup workflow.

Mitigation: Narrow the manifest and prompts to DNS-specific parameters such as hostname, record type, timeout, and trace options.

Risk: Generated DNS commands may be incorrect or inappropriate for the user's environment.

Mitigation: Review proposed commands before execution and prefer simple, explicit `dig` queries.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/dns-lookup-free)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown or JSON-style text with DNS lookup results and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed `dig` commands and resolved DNS record data when command execution is available.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
