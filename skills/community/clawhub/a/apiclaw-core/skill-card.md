## Description: <br>
APIClaw provides agent-facing access to 11 Amazon commerce data endpoints for category browsing, market metrics, product search, competitor lookup, realtime ASIN detail, AI review analysis, price band analysis, brand intelligence, and product history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apiclaw](https://clawhub.ai/user/apiclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect APIClaw capabilities, configure API access, and call Amazon commerce data endpoints for product, market, competitor, review, pricing, brand, and history analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend API credits and sends Amazon product keywords, ASINs, categories, competitor context, and market research inputs to APIClaw. <br>
Mitigation: Use APICLAW_API_KEY explicitly, monitor returned credit usage, and avoid submitting sensitive proprietary research unless APIClaw is trusted for that processing. <br>
Risk: Composite analysis and monitoring commands can perform broader API activity than a simple endpoint reference lookup. <br>
Mitigation: Review the command scope before execution and use narrower endpoint-specific commands when only targeted data is needed. <br>
Risk: Storing API keys in shared local configuration can expose credentials. <br>
Mitigation: Prefer environment-variable configuration for APICLAW_API_KEY and avoid keeping keys in shared local config files. <br>


## Reference(s): <br>
- [APIClaw ClawHub release page](https://clawhub.ai/apiclaw/apiclaw-core) <br>
- [APIClaw publisher profile](https://clawhub.ai/user/apiclaw) <br>
- [APIClaw API Quick Reference](references/openapi-reference.md) <br>
- [Market Entry Analyzer API Field Reference](references/reference.md) <br>
- [APIClaw OpenAPI specification](https://apiclaw.io/api/v1/openapi-spec) <br>
- [APIClaw API documentation](https://api.apiclaw.io/api-docs) <br>
- [APIClaw homepage](https://apiclaw.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API responses and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APICLAW_API_KEY; API calls consume credits and may return live or delayed Amazon commerce data depending on endpoint.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
