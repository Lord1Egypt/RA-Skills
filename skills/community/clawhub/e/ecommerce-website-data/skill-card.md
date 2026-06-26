## Description: <br>
Provides agent-assisted access to EcCompass ecommerce intelligence for searching ecommerce stores, analyzing domains, reviewing historical GMV and traffic trends, identifying installed apps, and retrieving LinkedIn contacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roger52027](https://clawhub.ai/user/roger52027) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
External users, developers, analysts, and sales teams use this skill to research ecommerce stores, compare competitors, inspect store technology and revenue estimates, and find business contacts for lead-generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an APEX_TOKEN and documentation includes flows where users may paste credentials into chat or plaintext configuration. <br>
Mitigation: Use a dedicated revocable token, avoid pasting the token into chat, and prefer environment variables or a secure secret store over plaintext configuration. <br>
Risk: Ecommerce searches, target domains, and contact-lookup requests are sent to EcCompass. <br>
Mitigation: Install only when this data sharing is acceptable for the user's organization and use case. <br>
Risk: Returned emails and LinkedIn profiles may be personal data used in lead-generation workflows. <br>
Mitigation: Handle contact data under applicable privacy, platform, and anti-spam rules before storage, enrichment, or outreach. <br>
Risk: GMV and revenue fields are estimates based on traffic and benchmark data rather than exact financial records. <br>
Mitigation: Present revenue figures as estimates and avoid using them as audited financial facts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roger52027/ecommerce-website-data) <br>
- [EcCompass AI](https://eccompass.ai) <br>
- [API schema](references/schema.md) <br>
- [Usage examples](references/examples.md) <br>
- [EcCompass API base URL](https://api.eccompass.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, JSON examples, and summarized ecommerce data returned from API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and a revocable APEX_TOKEN; API calls send ecommerce search, domain, app, historical, and contact lookup requests to EcCompass.] <br>

## Skill Version(s): <br>
1.2.18 (source: frontmatter, changelog, claw.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
