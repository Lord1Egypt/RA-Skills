## Description:

Look up domain WHOIS/RDAP info and check marketplace listings. Free API, no auth required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[julianengel](https://clawhub.ai/user/julianengel)

### License/Terms of Use:


## Use Case:

Developers, domain investors, and operations teams use this skill to query domain registration details and marketplace availability from documented public APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional npx command may fetch and execute external npm package code with the user's permissions.

Mitigation: Prefer the documented curl API examples; if using the CLI, pin a trusted package version and avoid sensitive environments until the package has been verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/julianengel/skills/domaindetails)
- [Domain Lookup API Example](https://mcp.domaindetails.com/lookup/example.com)
- [Marketplace Search API Example](https://api.domaindetails.com/api/marketplace/search?domain=example.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and summarized JSON response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for documented API examples; optional CLI uses npx.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
