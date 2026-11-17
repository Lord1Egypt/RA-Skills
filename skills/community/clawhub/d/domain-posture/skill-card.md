## Description:

Audit a domain's email and DNS security posture (SPF, DMARC, DKIM, MX, DNSSEC, CAA, MTA-STS, TLS-RPT, exposed records) and produce a scored, prioritized hardening report. Use when asked to check domain security, email spoofing risk, DMARC/SPF/DKIM setup, or DNS hygiene for any domain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[croxsec](https://clawhub.ai/user/croxsec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security teams can use this skill to review email authentication, mail transport, DNS integrity, and common exposure signals for domains they own or are authorized to assess. It produces prioritized findings and DNS record suggestions for hardening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default subdomain pass issues DNS queries for common sensitive-looking hostnames, despite the skill's passive-only description.

Mitigation: Run audits only for domains you own or are authorized to assess. Use --no-subdomains to skip that pass when it is not needed.

## Reference(s):

- [Domain Posture on ClawHub](https://clawhub.ai/croxsec/skills/domain-posture)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Configuration instructions]

**Output Format:** [Scored per-domain report in Markdown or JSON, with findings and prioritized DNS fix suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One report per domain; DNS changes are suggested for the user to publish.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
