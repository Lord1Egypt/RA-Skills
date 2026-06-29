## Description: <br>
Checks Ahrefs Domain Rating and backlink profile strength for a domain or URL using Ahrefs' free public API endpoint without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharkqwy](https://clawhub.ai/user/sharkqwy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and SEO analysts use this skill to check Ahrefs Domain Rating for one or more domains or URLs and compare backlink profile strength without paid Ahrefs API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domains or URLs checked with the skill are sent to Ahrefs' public API. <br>
Mitigation: Avoid submitting confidential internal hostnames, private URLs, or sensitive customer targets unless sharing them with Ahrefs is acceptable. <br>
Risk: The endpoint returns only Domain Rating and not paid Site Explorer metrics such as backlinks, referring domains, organic keywords, or historical data. <br>
Mitigation: Use the skill only for DR lookups and choose authenticated Ahrefs products when broader SEO metrics are required. <br>
Risk: Invalid domains or URLs can produce API errors instead of scores. <br>
Mitigation: Validate or clarify the target with the user before retrying when Ahrefs returns an invalid-target error. <br>


## Reference(s): <br>
- [Ahrefs Domain Rating Free API Documentation](https://docs.ahrefs.com/en/api/reference/public/get-domain-rating-free) <br>
- [ClawHub Skill Listing](https://clawhub.ai/sharkqwy/ahrefs-domain-rating-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional text or JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Ahrefs Domain Rating values or user-facing errors for invalid targets.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
