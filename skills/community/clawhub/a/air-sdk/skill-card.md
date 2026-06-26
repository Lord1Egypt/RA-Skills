## Description: <br>
Collective web intelligence for browser agents. Discover site capabilities, get CSS selectors, extract structured data, and report outcomes. When one agent learns how to use a website, every agent benefits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FransDevelopment](https://clawhub.ai/user/FransDevelopment) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to discover website capabilities, retrieve tested CSS selectors, extract structured data from URLs, and report browser automation outcomes back to a shared knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill configures and depends on a third-party MCP service that requires AIR_API_KEY. <br>
Mitigation: Review the npx install command and MCP configuration before installation, and provide the API key only in an environment where this third-party service is approved. <br>
Risk: Browser automation guidance could be used on logged-in sites, checkout flows, private dashboards, or forms containing personal data. <br>
Mitigation: Require explicit user approval before purchases, account-changing actions, or interactions with sensitive personal data. <br>
Risk: The capability index may have gaps and some websites may block automated browsing. <br>
Mitigation: Treat returned selectors and capability plans as assistance rather than guarantees, verify actions in the browser, and report failures when automation is blocked. <br>


## Reference(s): <br>
- [AIR SDK GitHub repository](https://github.com/ArcedeDev/air-sdk) <br>
- [AIR SDK API key dashboard](https://agentinternetruntime.com/extract/dashboard/sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CSS selectors, capability plans, extracted URL metadata, MCP setup instructions, and outcome-reporting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
