## Description: <br>
Run DNS, email security, SSL, WHOIS, and network tools via dnsrobot.net API — no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dnsrobot](https://clawhub.ai/user/dnsrobot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, sysadmins, and security practitioners use this skill to run DNS, domain, email-authentication, SSL/TLS, WHOIS, HTTP-header, IP reputation, and port diagnostics from an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup and scan targets, including domains, IPs, hostnames, ports, and URLs, are sent to dnsrobot.net. <br>
Mitigation: Avoid internal, confidential, customer-sensitive, incident-response, or token-bearing targets unless sharing them with dnsrobot.net is acceptable. <br>
Risk: SMTP tests, subdomain discovery, and port checks can interact with external systems. <br>
Mitigation: Use these features only on systems you own or are authorized to test. <br>


## Reference(s): <br>
- [DNS Robot Homepage](https://dnsrobot.net) <br>
- [DNS Robot All Tools](https://dnsrobot.net/all-tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline curl commands and JSON or NDJSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; endpoints accept JSON request bodies and some responses stream as NDJSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
