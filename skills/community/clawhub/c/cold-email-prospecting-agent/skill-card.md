## Description: <br>
Find work emails, personal emails, mobile phone numbers, and verify email deliverability for cold email outreach using RevoScale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dotcomcj2](https://clawhub.ai/user/dotcomcj2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, growth, and business development users use this skill to look up and verify prospect contact information for legitimate business outreach. It supports work-email lookup by name and domain, email verification, and personal email or mobile phone lookup from LinkedIn profile URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive personal and business contact data for outreach. <br>
Mitigation: Use it only for lawful business prospecting and apply consent, anti-spam, platform-terms, and privacy-law controls before processing emails or mobile numbers. <br>
Risk: All API calls require a RevoScale API key. <br>
Mitigation: Protect REVOSCALE_API_KEY and avoid exposing it in prompts, logs, shared files, or responses. <br>
Risk: Outreach decisions may rely on contact data that is unavailable, uncertain, or not permitted for a given use. <br>
Mitigation: Return only API-provided contact data, include confidence or verification status when available, and suppress outreach when processing rights are unclear. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dotcomcj2/cold-email-prospecting-agent) <br>
- [RevoScale](https://revoscale.io) <br>
- [RevoScale API Key Settings](https://app.revoscale.io/settings) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration] <br>
**Output Format:** [Markdown with API endpoint, JSON request, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REVOSCALE_API_KEY and user-provided names, company domains, LinkedIn profile URLs, or email addresses.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
