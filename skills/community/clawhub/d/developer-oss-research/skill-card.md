## Description:

Researches public GitHub repositories, users, organizations, and Chrome Web Store extensions through the Crawlora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to assess public GitHub projects and profiles, track trending repositories, and review Chrome extensions, including permissions and privacy disclosures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and lookups pass through Crawlora's intermediary service.

Mitigation: Avoid sensitive or private search terms unless intended; review Crawlora's data-handling terms.

Risk: The Crawlora API key could be exposed if shared or stored insecurely.

Mitigation: Keep CRAWLORA_API_KEY private and out of committed files and query parameters.

Risk: Successful API requests may incur usage charges.

Mitigation: Review Crawlora's billing terms before use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/developer-oss-research)
- [Endpoint reference](reference/endpoints.md)
- [Crawlora service](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Text summaries or JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public data only; list results may be paginated.]

## Skill Version(s):

1.0.18 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
