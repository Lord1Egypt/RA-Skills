## Description: <br>
Provides guidance, shell commands, and configuration examples for running and using a local Dockerized Crawl4AI web crawling and scraping service through its REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orange-afk](https://clawhub.ai/user/orange-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy, check, and call a local Crawl4AI Docker service for webpage crawling, markdown extraction, screenshots, PDF generation, monitoring, and optional LLM-based content extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running a local crawler service can expose a web API on port 11235. <br>
Mitigation: Restrict access to the local service port and avoid exposing it to untrusted networks. <br>
Risk: Using the Docker image tag latest can introduce unreviewed upstream changes. <br>
Mitigation: Pin the Crawl4AI Docker image to a reviewed version before production use. <br>
Risk: LLM extraction can send crawled content to a configured model provider. <br>
Mitigation: Avoid LLM extraction on sensitive pages unless the provider's data handling is acceptable. <br>
Risk: Crawler use against internal, authenticated, or restricted pages can collect unintended data. <br>
Mitigation: Crawl only pages that are intended for this workflow and comply with site access rules. <br>
Risk: API keys stored in .llm.env can be exposed through local files or container configuration. <br>
Mitigation: Protect .llm.env, limit credential scope, and rotate keys if exposure is suspected. <br>


## Reference(s): <br>
- [Crawl4AI documentation](https://docs.crawl4ai.com/) <br>
- [Example Docker and API configuration](references/example-config.json) <br>
- [ClawHub release page](https://clawhub.ai/orange-afk/crawl4ai-docker-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include curl requests, Docker Compose guidance, local service checks, and LLM provider environment variable examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
