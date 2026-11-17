## Description:

Helps cross-border ecommerce sellers analyze keywords, estimate marketplace profit, compare simulated competitors, and generate product listing copy for Amazon and eBay workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and developers use this skill to screen product opportunities, calculate Amazon or eBay selling economics, and draft marketplace listing content. It is most useful for early product research where simulated keyword and competitor data are acceptable or can be replaced with reviewed data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network exposure from the Flask app can make local development endpoints reachable beyond a private environment.

Mitigation: Disable Flask debug by default, bind development runs to localhost, and restrict CORS before any wider deployment.

Risk: Unauthenticated AI listing generation can create billable API usage when an OpenAI API key is configured.

Mitigation: Add authentication plus request, rate, and cost limits before enabling real API-backed listing generation.

Risk: Frontend rendering may expose users to unsafe browser content if untrusted values are displayed without sanitization.

Mitigation: Sanitize rendered values and review browser output paths before exposing the web app to users.

Risk: Dependency installation paths differ between requirements.txt and setup.sh, which can make reviews and updates inconsistent.

Mitigation: Use one reviewed dependency installation path and lock or update dependencies through that path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/skills/cross-border-ecommerce-kay)
- [Publisher profile](https://clawhub.ai/user/shenghoo123-png)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [CLI text, optional JSON API responses, and product listing copy with bullet-style descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use simulated keyword, competitor, and listing data when real data sources or an OpenAI API key are unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
