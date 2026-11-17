## Description:

A collection of DomainHelp DNS and domain utility skills for agent-ready public IP, DNS resolver, homoglyph, redirect, SPF, and domain permutation checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markjr](https://clawhub.ai/user/markjr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security analysts, and domain or mail operators use this skill catalog to have agents select and call DomainHelp DNS APIs for resolver diagnostics, redirect inspection, homoglyph analysis, SPF flattening, public IP lookup, and domain permutation generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried domains, URLs, public IP information, resolver metadata, and related network details are sent to DomainHelp API endpoints.

Mitigation: Do not submit secrets, internal-only hostnames, private links, or URLs containing tokens unless sharing that data with DomainHelp is acceptable for the deployment environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/markjr/skills/dns-agent-skills)
- [DomainHelp DNS Skills Catalog](https://dnsskills.md/skills)
- [DomainHelp DNS Skills Markdown Catalog](https://dnsskills.md/skills.md)
- [DomainHelp OpenAPI Specification](https://dnsskills.md/openapi.yaml)
- [DomainHelp llms.txt](https://dnsskills.md/llms.txt)

## Skill Output:

**Output Type(s):** [guidance, API calls, JSON]

**Output Format:** [Markdown documentation with JSON API response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include DNS, URL, resolver, redirect, SPF, and domain permutation data returned by DomainHelp APIs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
