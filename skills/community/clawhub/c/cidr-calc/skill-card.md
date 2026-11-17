## Description:

Calculate subnet information from CIDR notation. Use when the user asks to calculate a subnet, find the network address, broadcast address, host range, subnet mask, or number of hosts for an IP in CIDR notation like 192.168.1.0/24.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohernandez-dev-blossom](https://clawhub.ai/user/ohernandez-dev-blossom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, network engineers, and operators use this skill to calculate and present subnet details for a single IPv4 CIDR input, including network address, broadcast address, host range, subnet mask, host counts, IP class, network type, and binary representation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subnet results may be incorrect if the agent misapplies CIDR math or accepts invalid input.

Mitigation: Validate CIDR notation, octet ranges, and prefix length before use, and review key network, broadcast, mask, and host-range results before applying them to operational network changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ohernandez-dev-blossom/skills/cidr-calc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text with labeled subnet fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts one IPv4 CIDR notation string at a time.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
