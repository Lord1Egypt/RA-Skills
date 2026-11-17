## Description:

SSL/TLS certificate expiry checker and domain health monitor for checking certificate expiration, issuer details, SAN entries, chain validity, custom ports, and report output for one or multiple domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and security reviewers use this skill to check SSL/TLS certificate expiry and domain certificate health for one or multiple domains before deployment, renewal, or CI/CD gating.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may include unescaped data from scanned domains or endpoints.

Mitigation: Use JSON or terminal output for untrusted targets, and open generated HTML reports only when the domain list and scanned endpoints are trusted.

Risk: The checker initiates network connections to domains and ports supplied by the user.

Mitigation: Run it only against domains and ports the user is authorized to inspect.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericlooi504/skills/cert-expiry-checker)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown or terminal text with optional JSON output and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform network checks against user-specified domains and write JSON or HTML reports when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
