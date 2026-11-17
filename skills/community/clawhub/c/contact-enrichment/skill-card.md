## Description:

Extract contact information from a website using a 3-tier approach: direct HTML scraping, WHOIS lookup, then Hunter.io API domain search for verified business emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to enrich a public business website or domain with likely contact emails, phone numbers, business names, WHOIS details, and confidence indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary user-provided URLs, which may expose internal or untrusted network locations if used without URL controls.

Mitigation: Run it only against approved public business websites and add URL validation, redirect controls, and private-IP blocking before broader use.

Risk: Optional Hunter.io enrichment sends domain and contact data to a third-party service.

Mitigation: Provide HUNTER_API_KEY only when third-party enrichment is intended and the data-sharing implications are acceptable.

Risk: Collected contact data may be used for outreach.

Mitigation: Use public contact data only, honor opt-out requests, and review CAN-SPAM, GDPR, and other applicable outreach requirements before emailing.

## Reference(s):

- [Contact Enrichment ClawHub listing](https://clawhub.ai/maverick-software/skills/contact-enrichment)
- [Hunter.io Domain Search API endpoint](https://api.hunter.io/v2/domain-search)
- [Hunter.io Email Verifier API endpoint](https://api.hunter.io/v2/email-verifier)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown with Python code blocks and a JSON-like contact enrichment result schema]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires outbound requests to public websites and WHOIS services; Hunter.io enrichment is optional and requires HUNTER_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
