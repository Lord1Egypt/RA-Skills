## Description: <br>
Deploy privacy-first analytics with correct API patterns, rate limits, and GDPR compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and product teams use this skill to configure privacy-first analytics integrations for Umami, Plausible, and PostHog while avoiding common API, rate limit, credential, and GDPR mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analytics setup may collect personal information or identifiers without valid consent. <br>
Mitigation: Verify configuration against applicable privacy laws, use explicit consent where needed, and avoid tracking names, emails, IP addresses, or other personal information in custom events. <br>
Risk: Hardcoded analytics API keys can expose credentials. <br>
Mitigation: Keep API keys in environment variables and review configuration before deployment. <br>
Risk: Incorrect provider-specific IDs, timestamp units, or rate-limit handling can cause failed requests or unreliable analytics data. <br>
Mitigation: Confirm provider IDs and timestamp units before sending events, and implement exponential backoff for HTTP 429 responses. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Markdown-only guidance; it does not install hooks or run code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
