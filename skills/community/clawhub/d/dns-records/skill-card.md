## Description:

Looks up A, AAAA, MX, NS, TXT, CNAME, and SOA DNS records for one or more domains, using dig when available with a socket fallback for A and AAAA records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support engineers use this skill to inspect DNS records, find domain IP addresses, review mail servers and nameservers, and debug DNS configuration from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes DNS queries from the user's machine, which can reveal lookup intent to configured DNS resolvers and queried infrastructure.

Mitigation: Install and run it only when that network behavior is acceptable for the domains being checked.

Risk: Record type and domain inputs are passed to the system dig command, and the security evidence notes limited input validation around that external command.

Mitigation: Use normal domain names and documented record types only; publishers should add record-type allowlists and domain validation before broader deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, json, shell commands]

**Output Format:** [Plain text DNS summaries or JSON records, with shell command examples in skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports multiple domains per command and returns up to five displayed values per record type in plain text mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
