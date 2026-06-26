## Description: <br>
Automated product opportunity scanner for Amazon sellers that scans categories, validates candidates with APIClaw data, and ranks product opportunities by a composite score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apiclaw](https://clawhub.ai/user/apiclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and agent users use this skill to discover, filter, score, and compare product opportunities based on budget, experience level, risk tolerance, category data, and APIClaw market signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Amazon research keywords, ASINs, categories, filters, budget, and seller-profile context are sent to APIClaw. <br>
Mitigation: Use the skill only when sharing that product research context with APIClaw is acceptable. <br>
Risk: API-backed scans may consume APIClaw credits. <br>
Mitigation: Monitor credit usage and use quick-scan mode when a lower-cost directional scan is sufficient. <br>
Risk: API keys can be exposed if stored in shared configuration. <br>
Mitigation: Use a dedicated APIClaw key in APICLAW_API_KEY and avoid storing credentials in shared config files. <br>


## Reference(s): <br>
- [APIClaw API key setup](https://apiclaw.io/en/api-keys) <br>
- [APIClaw](https://apiclaw.io) <br>
- [APIClaw OpenAPI base](https://api.apiclaw.io/openapi/v2) <br>
- [APIClaw API docs](https://api.apiclaw.io/api-docs) <br>
- [Market Entry Analyzer API Field Reference](references/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with tables, ranked analysis, risk alerts, data provenance, and API usage summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responds in the user's language and requires APICLAW_API_KEY for API-backed scans.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
