## Description: <br>
Look up domain WHOIS/RDAP info and check marketplace listings. Free API, no auth required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[julianengel](https://clawhub.ai/user/julianengel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, domain operators, and external users can use this skill to generate curl-based lookup commands for domain registration, RDAP/WHOIS details, and marketplace listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domain names queried through the skill are sent to DomainDetails services. <br>
Mitigation: Avoid submitting sensitive internal or private domain names unless that use is approved. <br>
Risk: The artifact mentions an optional npx package that is outside the documented curl-only security posture. <br>
Mitigation: Prefer the documented curl commands unless the optional package has been separately verified. <br>


## Reference(s): <br>
- [Domain Details ClawHub release](https://clawhub.ai/julianengel/domaindetails) <br>
- [DomainDetails lookup API example](https://mcp.domaindetails.com/lookup/example.com) <br>
- [DomainDetails marketplace search API example](https://api.domaindetails.com/api/marketplace/search?domain=example.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces curl examples for public domain lookup and marketplace search; no authentication is documented.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
