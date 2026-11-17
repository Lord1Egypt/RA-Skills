## Description:

Prospector helps an agent search for potential customer companies by keyword or region, extract public contact email addresses from company websites and WHOIS data, and return structured lead lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xieyz1980](https://clawhub.ai/user/xieyz1980)

### License/Terms of Use:

MIT-0

## Use Case:

External users and sales or business-development agents use this skill to find candidate customer companies, collect public contact emails, query locally cached leads, and export lead data for follow-up workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs broad web searches, crawls discovered sites, uses WHOIS lookups, and can route traffic through user-provided proxies.

Mitigation: Run it in an isolated environment with limited network reach, use only trusted proxy settings, and avoid targeting sensitive internal networks.

Risk: Collected company and email data is cached persistently and can be exported to JSON or CSV.

Mitigation: Define retention and deletion procedures, restrict access to cache and export files, and treat exported CSV files as untrusted input.

Risk: Lead-generation and contact collection can create legal, privacy, or policy obligations depending on jurisdiction and intended outreach.

Mitigation: Review local compliance requirements and perform human review of high-value contacts before using the data in outreach workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xieyz1980/skills/bestprospector)
- [Publisher profile](https://clawhub.ai/user/xieyz1980)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON or CSV lead exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces company names, domains, URLs, descriptions, email lists, cache statistics, and optional export files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
