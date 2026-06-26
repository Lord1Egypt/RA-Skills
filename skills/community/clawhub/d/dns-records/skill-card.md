## Description: <br>
Looks up DNS records for domains, including A, AAAA, MX, NS, TXT, CNAME, and SOA records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check domain DNS records, find IP addresses or mail servers, inspect nameservers, and debug DNS configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DNS lookups for supplied domains may be visible to the configured resolver or network operator. <br>
Mitigation: Use the skill only for domains you are comfortable querying, and run it in an environment whose resolver and network visibility are acceptable for the task. <br>
Risk: Unexpected record type or domain arguments could change the DNS query behavior. <br>
Mitigation: Use the documented record types only: A, AAAA, MX, NS, TXT, CNAME, and SOA. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; command output is plain text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports multiple domains and record-type selection; uses system dig when available with Python socket fallback for A and AAAA records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
