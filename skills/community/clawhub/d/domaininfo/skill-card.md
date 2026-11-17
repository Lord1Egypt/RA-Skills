## Description:

Look up domain WHOIS information, check email security (DMARC/SPF/DKIM), inspect TLS certificates, and capture website screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxlderek](https://clawhub.ai/user/sxlderek)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security analysts, and operations teams use this skill to produce a domain-only report covering WHOIS, DNS records, email security signals, TLS certificate details, and an optional website screenshot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional screenshot helper can be directed at local or private network targets in environments that can reach internal dashboards, localhost services, cloud metadata, or private networks.

Mitigation: Review or disable screenshot capture before installation; if enabled, restrict targets to public registrable hostnames and fixed in-skill output paths.

## Reference(s):

- [Skill setup notes](references/setup.md)
- [ClawHub skill page](https://clawhub.ai/sxlderek/skills/domaininfo)
- [ipinfo country endpoint](https://ipinfo.io/{IP}/country)

## Skill Output:

**Output Type(s):** [text, markdown, files]

**Output Format:** [Single Markdown-style domain report, optionally accompanied by a website screenshot image file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Buffered final response only; screenshot capture is optional and skipped when browser tooling is unavailable.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
