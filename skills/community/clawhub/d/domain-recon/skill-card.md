## Description:

Passive domain/infra OSINT over five keyless public APIs - subdomains, RDAP/WHOIS, DNS-over-HTTPS, IP geo/ISP, and ASN/prefix ownership.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maggiedev-bot](https://clawhub.ai/user/maggiedev-bot)

### License/Terms of Use:

MIT

## Use Case:

Developers, security analysts, and operators use this skill to passively inspect a domain, IP address, or ASN through public OSINT sources without directly probing the target host.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries disclose the submitted domains, URLs, IP addresses, and ASNs to public third-party OSINT services.

Mitigation: Use only authorized targets, avoid sensitive incident-response targets when disclosure is unacceptable, and disable sources such as Wayback or IP enrichment when they are not needed.

Risk: Some upstream services have rate limits, coverage gaps, or transport constraints, including HTTP-only IP enrichment.

Mitigation: Scope profile and full-TLD runs narrowly, use command limits such as --no-wayback and enrichment caps, and review upstream service terms before commercial workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maggiedev-bot/skills/domain-recon)
- [Project homepage](https://github.com/maggiedev-bot/domain-recon)
- [API Notes](artifact/references/API_NOTES.md)
- [Changelog](artifact/references/CHANGELOG.md)
- [RDAP Coverage Map](artifact/docs/tld-rdap-coverage.md)
- [Sample Output](artifact/examples/SAMPLE_OUTPUT.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Python shell commands; helper output is JSON by default or compact text with --human.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Passive public-source lookups; no credentials required; results depend on third-party OSINT service availability, rate limits, and coverage.]

## Skill Version(s):

0.6.0 (source: frontmatter, release evidence, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
