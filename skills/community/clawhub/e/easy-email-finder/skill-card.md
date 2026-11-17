## Description:

Search for local or digital businesses and enrich them with verified email addresses, tech stack detection, and social media links using the Easy Email Finder API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[faalbane](https://clawhub.ai/user/faalbane)

### License/Terms of Use:


## Use Case:

Developers and business users use this skill to find local or digital business leads, enrich websites with email addresses, and check related metadata such as technology stack, social links, credit balance, and usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends business search queries, website URLs, and an API key to the Easy Email Finder service.

Mitigation: Use it only when that data sharing is intended, store EEF_API_KEY securely, and avoid including sensitive data in queries or website lists.

Risk: Returned email addresses may be personal data and may be subject to privacy, consent, website terms, or anti-spam rules.

Mitigation: Review applicable rules before contacting addresses, especially personal or non-role-based addresses.

Risk: Enrichment endpoints consume credits and documented rate limits apply.

Mitigation: Check balance and usage endpoints, batch requests within the documented limits, and honor Retry-After responses when rate limited.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/faalbane/skills/easy-email-finder)
- [Easy Email Finder homepage](https://easyemailfinder.com)
- [Easy Email Finder developer access](https://easyemailfinder.com/developer)
- [Easy Email Finder API base URL](https://easyemailfinder.com/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with curl examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an EEF_API_KEY bearer token and sends business search queries or website URLs to the Easy Email Finder API.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
