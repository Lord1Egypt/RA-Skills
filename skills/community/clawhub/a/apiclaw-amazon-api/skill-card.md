## Description: <br>
APIClaw Amazon API helps agents look up Amazon commerce data across categories, market metrics, product search, competitor lookup, realtime ASIN detail, and AI review analysis using the APIClaw API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christine-srp](https://clawhub.ai/user/christine-srp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to answer APIClaw capability questions, configure API access, and choose the correct APIClaw endpoint and fields for Amazon commerce data workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIClaw receives the product, market, ASIN, and review queries submitted through API workflows that use this skill. <br>
Mitigation: Install and use the skill only when APIClaw is trusted for those commerce-data queries. <br>
Risk: The APICLAW_API_KEY can be exposed if copied into chats, files, logs, or shared snippets. <br>
Mitigation: Store the key in the APICLAW_API_KEY environment variable and avoid pasting it into prompts or logs. <br>
Risk: API calls can consume paid APIClaw credits. <br>
Mitigation: Monitor API usage and remaining credits before running repeated or high-volume queries. <br>
Risk: APIClaw endpoints return different field shapes, so assuming a shared response structure can produce incorrect guidance or analysis. <br>
Mitigation: Check the endpoint-specific reference before using response fields such as price, BSR, sales, reviews, or sentiment. <br>


## Reference(s): <br>
- [APIClaw Amazon API release page](https://clawhub.ai/christine-srp/apiclaw-amazon-api) <br>
- [APIClaw API Quick Reference](references/openapi-reference.md) <br>
- [APIClaw API documentation](https://api.apiclaw.io/api-docs) <br>
- [APIClaw OpenAPI specification](https://apiclaw.io/api/v1/openapi-spec) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and endpoint field guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API setup steps, endpoint recommendations, request examples, response field notes, and credit usage guidance; the skill itself is reference guidance and does not execute API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
