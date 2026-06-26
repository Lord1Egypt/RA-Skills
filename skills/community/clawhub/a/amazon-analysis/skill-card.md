## Description: <br>
Amazon seller data analysis tool for market research, product selection, competitor analysis, ASIN evaluation, pricing reference, and category research using the APIClaw API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apiclaw](https://clawhub.ai/user/apiclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, ecommerce operators, and agent users use this skill to research Amazon categories, compare competitors, evaluate ASINs, and generate directional product opportunity reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security review marked the release suspicious because high-impact capability metadata and some instructions can obscure data-quality limits. <br>
Mitigation: Confirm that the crypto and purchase capability tags are intentional and strictly controlled before deployment, and treat generated reports as directional when source data is missing or estimated. <br>
Risk: The skill depends on an API key and paid or metered API calls, which can expose credentials or consume credits unexpectedly. <br>
Mitigation: Provide APICLAW_API_KEY only through a protected environment variable, use a dedicated key, protect any local config file, and monitor credit usage. <br>
Risk: Security guidance warns against workflows that infer Chinese seller status from weak signals. <br>
Mitigation: Avoid that workflow unless it is rewritten to use explicit source-provided country metadata and to state clear limitations. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/apiclaw/amazon-analysis) <br>
- [APIClaw API](https://api.apiclaw.io/openapi/v2) <br>
- [Execution Guide](references/execution-guide.md) <br>
- [API Field Reference](references/reference.md) <br>
- [Composite Scenarios](references/scenarios-composite.md) <br>
- [Listing Scenarios](references/scenarios-listing.md) <br>
- [Operations Scenarios](references/scenarios-ops.md) <br>
- [Pricing Scenarios](references/scenarios-pricing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with data tables, confidence labels, API usage notes, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APICLAW_API_KEY and may consume APIClaw credits.] <br>

## Skill Version(s): <br>
1.1.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
