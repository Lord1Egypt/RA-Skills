## Description: <br>
Calculate subnet information from CIDR notation. Use when the user asks to calculate a subnet, find the network address, broadcast address, host range, subnet mask, or number of hosts for an IP in CIDR notation like 192.168.1.0/24. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ohernandez-dev-blossom](https://clawhub.ai/user/ohernandez-dev-blossom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, network engineers, and operators use this skill to calculate subnet properties from a single IPv4 CIDR string, including network and broadcast addresses, host ranges, masks, host counts, IP class, network type, and binary representation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Assistant-generated subnet arithmetic may be incorrect for production-sensitive edge cases such as /31 and /32. <br>
Mitigation: Double-check production network planning results with authoritative network tooling or peer review before applying changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ohernandez-dev-blossom/cidr-calc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown or labeled text with computed CIDR fields and validation messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts one IPv4 CIDR string and returns normalized subnet information; no files, network calls, credentials, persistence, or system changes are involved.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
