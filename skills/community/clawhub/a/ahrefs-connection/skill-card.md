## Description: <br>
Connect to the Ahrefs API to retrieve SEO data including backlinks, keyword metrics, domain analysis, rank tracking, and site audit information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonathan-sokol](https://clawhub.ai/user/jonathan-sokol) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External SEO practitioners, marketers, and developers use this skill to query Ahrefs API data for keyword research, backlink analysis, competitor analysis, rank tracking, SERP review, and technical site audit workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Ahrefs API key to make SEO-data requests. <br>
Mitigation: Store the API key securely, prefer environment variables or a secrets manager, and avoid exposing it in prompts, logs, or shared files. <br>
Risk: Queries can include confidential domains, URLs, keywords, or competitive SEO targets. <br>
Mitigation: Review requests before sending them to Ahrefs and obtain approval before submitting sensitive customer, internal, or competitor data. <br>
Risk: Large or batch requests may consume paid Ahrefs API quota. <br>
Mitigation: Set API unit limits when possible, limit rows and selected columns, batch intentionally, and review high-volume requests before execution. <br>


## Reference(s): <br>
- [Ahrefs API Documentation](https://docs.ahrefs.com/docs/api/reference/introduction) <br>
- [Ahrefs API Key Management](https://app.ahrefs.com/account/api-keys) <br>
- [Ahrefs Pricing and Plan Limits](https://ahrefs.com/pricing) <br>
- [Ahrefs Limits and Usage Tracking](https://app.ahrefs.com/account/limits-and-usage/web) <br>
- [Ahrefs API Setup Guide](references/setup.md) <br>
- [Ahrefs API Capabilities Reference](references/capabilities.md) <br>
- [Ahrefs API Workflow Patterns](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Guidance, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an Ahrefs API key and may consume paid Ahrefs API units.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
