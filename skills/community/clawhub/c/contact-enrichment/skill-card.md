## Description: <br>
Extract contact information from a website using a 3-tier approach: direct HTML scraping, WHOIS lookup, then Hunter.io API domain search for verified business emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to enrich a business website or domain with public contact details, including emails, phone numbers, business names, WHOIS information, and optional Hunter.io results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may visit public business websites and query WHOIS data while enriching contacts. <br>
Mitigation: Use the skill only for public business sites and respect robots.txt, login boundaries, and applicable privacy requirements. <br>
Risk: Hunter.io lookup can send domains or email addresses to a third-party service and consume paid quota. <br>
Mitigation: Set HUNTER_API_KEY only when that sharing and cost profile is acceptable, and monitor API usage. <br>
Risk: Enriched contact data could be used for outreach subject to privacy and anti-spam rules. <br>
Mitigation: Confirm outreach workflows include opt-out handling and comply with applicable CAN-SPAM, GDPR, and similar requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick-software/contact-enrichment) <br>
- [Hunter.io domain search API](https://api.hunter.io/v2/domain-search) <br>
- [Hunter.io email verifier API](https://api.hunter.io/v2/email-verifier) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [Markdown with Python code blocks and JSON-shaped contact-enrichment examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a public website URL or domain; HUNTER_API_KEY is optional for Hunter.io lookups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
