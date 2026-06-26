## Description: <br>
Scans Amazon category landscapes to discover trending subcategories, emerging niches, and market shifts for product selection and market entry timing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apiclaw](https://clawhub.ai/user/apiclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, product researchers, and ecommerce operators use this skill to scan Amazon parent categories, compare subcategory trend signals, and generate market-entry guidance or scheduled monitoring setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Amazon categories, keywords, ASINs, and the APIClaw API key to APIClaw. <br>
Mitigation: Install only if that data sharing is acceptable, and provide credentials through the declared APICLAW_API_KEY environment variable. <br>
Risk: Broad scans can consume API credits. <br>
Mitigation: Review expected credit usage before running full scans or enabling recurring monitoring. <br>
Risk: Scheduled monitoring can create cron or task configuration that runs repeatedly. <br>
Mitigation: Review generated schedules and alert thresholds before enabling automated checks. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/apiclaw/amazon-market-trend-scanner) <br>
- [Market Entry Analyzer API Field Reference](references/reference.md) <br>
- [APIClaw API documentation](https://api.apiclaw.io/api-docs) <br>
- [APIClaw API base endpoint](https://api.apiclaw.io/openapi/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with tables, inline API field names, optional shell commands, and monitoring configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include a data provenance table, API usage and credit summary, confidence labels for conclusions, and optional scheduled monitoring configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
