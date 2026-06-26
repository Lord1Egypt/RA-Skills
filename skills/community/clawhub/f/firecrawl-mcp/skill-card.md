## Description: <br>
Firecrawl Mcp gives agents access to Firecrawl web scraping, crawling, search, extraction, autonomous research, and browser automation tools through OneKey Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-Hub-Admin](https://clawhub.ai/user/AI-Hub-Admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the web, scrape or crawl websites, extract structured page data, and run browser automation through Firecrawl-compatible tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs, prompts, schemas, and extracted content may be sent to OneKey/Firecrawl. <br>
Mitigation: Use the skill only for data that is acceptable to share with those services and avoid sensitive logged-in sites unless that transfer is intended. <br>
Risk: A bundled demo fallback key may be used when no OneKey access key is configured. <br>
Mitigation: Configure a scoped DEEPNLP_ONEKEY_ROUTER_ACCESS key before use instead of relying on the demo fallback. <br>
Risk: Browser click, type, and execute actions can alter remote web state inside the provider-side browser session. <br>
Mitigation: Review browser automation payloads before execution and restrict use to sessions where those changes are intended. <br>


## Reference(s): <br>
- [ClawHub Firecrawl Mcp Skill Page](https://clawhub.ai/AI-Hub-Admin/firecrawl-mcp) <br>
- [OneKey Gateway Keys](https://www.deepnlp.org/workspace/keys) <br>
- [OneKey MCP Router Documentation](https://www.deepnlp.org/doc/onekey_mcp_router) <br>
- [OneKey Gateway Documentation](https://deepnlp.org/doc/onekey_agent_router) <br>
- [AI Agent Marketplace](https://www.deepnlp.org/store/ai-agent) <br>
- [Skills Marketplace](https://www.deepnlp.org/store/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [JSON responses and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool calls may return scraped content, extracted structured data, crawl status, search results, browser session data, or job identifiers depending on the selected Firecrawl tool.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
