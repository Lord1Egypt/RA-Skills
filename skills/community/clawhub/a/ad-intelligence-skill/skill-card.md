## Description: <br>
Competitive ad intelligence skill for fetching, analyzing, and reporting on competitor ads across Meta, Google Ads Transparency Center, and LinkedIn Ad Library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhishekj9621](https://clawhub.ai/user/abhishekj9621) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, ecommerce operators, and analysts use this skill to research competitor ads across Meta, Google, and LinkedIn, compare creative messaging, and decide whether to use quick public scraping or deeper API-backed workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to make web requests to ad platforms and named third-party API providers for competitor research. <br>
Mitigation: Use Phase 1 for public lookups when possible, and use API keys only with providers the user trusts. <br>
Risk: Sensitive competitor or investigation terms may be sent to selected platforms or API services. <br>
Mitigation: Avoid sensitive investigation terms unless the user is comfortable disclosing them to the chosen platform or provider. <br>
Risk: Public ad libraries do not expose private performance metrics such as exact spend, CTR, conversions, or ROAS. <br>
Mitigation: Present unavailable metrics as limitations and avoid implying that public ad-library data provides private campaign performance. <br>


## Reference(s): <br>
- [Meta (Facebook / Instagram) Ad Intelligence](references/meta.md) <br>
- [Google Ads Transparency Center - Ad Intelligence](references/google.md) <br>
- [LinkedIn Ad Library - Ad Intelligence](references/linkedin.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summary report plus normalized JSON, with optional code snippets, shell commands, and API setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes platform limitations, recommended next steps, and phase selection guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
