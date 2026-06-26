## Description: <br>
Crawleo Web Search lets OpenClaw agents use Crawleo's REST API for web search, Google SERP and Maps data, URL crawling, content extraction, and headful browser crawling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crawleo](https://clawhub.ai/user/crawleo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add Crawleo-backed live web search, Google Search, Google Maps place data, URL crawling, content extraction, and headful browser crawling to an agent. Live Crawleo calls require a Crawleo API key before requests are sent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crawleo API keys are sensitive credentials, and requests may consume account credits or expose user-chosen queries and URLs to Crawleo. <br>
Mitigation: Install only if the publisher is trusted, keep CRAWLEO_API_KEY out of logs and committed files, monitor usage, and avoid confidential search terms, private URLs, or access-controlled pages unless sharing them with Crawleo is acceptable. <br>
Risk: Live web search and crawling send data to Crawleo and can reach protected or highly dynamic sites. <br>
Mitigation: Use the offline-safe tests and examples by default; run live verification only when both CRAWLEO_API_KEY and CRAWLEO_ENABLE_LIVE_TESTS=1 are intentionally set. <br>


## Reference(s): <br>
- [Crawleo ClawHub listing](https://clawhub.ai/crawleo/crawleo) <br>
- [Crawleo API introduction](https://docs.crawleo.dev/api-reference/introduction.md) <br>
- [Crawleo authentication](https://docs.crawleo.dev/authentication.md) <br>
- [Crawleo MCP overview](https://docs.crawleo.dev/mcp/overview.md) <br>
- [Crawleo OpenAPI](https://docs.crawleo.dev/openapi.json) <br>
- [Endpoint contract inventory](contracts/crawleo-endpoints.md) <br>
- [Machine-readable endpoint contract](contracts/crawleo-endpoints.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and JSON endpoint contracts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live Crawleo calls require CRAWLEO_API_KEY; default tests and examples are designed to stay offline-safe.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
