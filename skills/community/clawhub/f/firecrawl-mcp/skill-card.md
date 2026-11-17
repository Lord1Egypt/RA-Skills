## Description:

Provides Firecrawl web search, scraping, crawling, extraction, autonomous research, and browser-session tools through OneKey Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search the web, scrape or crawl pages, extract structured data, and automate browser-backed web research with Firecrawl MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive URLs, page content, credentials, or logged-in browser sessions may be sent through an external gateway.

Mitigation: Use a dedicated scoped gateway key and avoid submitting sensitive internal URLs, private page content, credentials, or logged-in sessions unless the data flow has been reviewed.

Risk: Remote browser and code execution can affect real websites or accounts.

Mitigation: Run the skill in an isolated environment, review browser actions before execution, and use test accounts or constrained sessions for automation.

Risk: The artifact falls back to a shared demo key when no gateway key is configured.

Mitigation: Set DEEPNLP_ONEKEY_ROUTER_ACCESS to an owned scoped key before use and do not rely on the fallback key for release or production workflows.

Risk: Unpinned npm and Python dependencies can change between installs.

Mitigation: Install from a pinned, reviewed dependency set before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/firecrawl-mcp)
- [OneKey MCP Router documentation](https://www.deepnlp.org/doc/onekey_mcp_router)
- [OneKey Gateway documentation](https://deepnlp.org/doc/onekey_agent_router)
- [OneKey Gateway keys](https://www.deepnlp.org/workspace/keys)
- [DeepNLP AI Agent Marketplace](https://www.deepnlp.org/store/ai-agent)
- [DeepNLP Skills Marketplace](https://www.deepnlp.org/store/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON or Markdown from Firecrawl tools, with shell command examples and Python script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a OneKey Gateway key; browser execution requires an active browser session.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
