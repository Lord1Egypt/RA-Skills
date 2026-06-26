## Description: <br>
Use when tasks need Exa MCP for web or people research, or when preparing Exa MCP server configuration with a fixed tool set. Trigger for requests to run Exa search, advanced Exa search, people search, or summarize Exa-based findings with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tokyo-s](https://clawhub.ai/user/tokyo-s) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to choose and configure Exa MCP tools for focused web research, advanced filtered search, and person-centric lookup tasks. It guides concise research outputs with source links and explicit unknowns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Exa MCP endpoint uses an API key for hosted external API access. <br>
Mitigation: Store EXA_API_KEY in a secure environment variable or secret store and verify the Exa MCP endpoint before adding credentials. <br>
Risk: Research topics, person lookups, or business queries may be sent to an external service. <br>
Mitigation: Avoid confidential research topics, private names, or sensitive business queries unless Exa's data handling is acceptable for the intended use. <br>
Risk: Free-tier or rate-limit constraints may interrupt broad searches. <br>
Mitigation: Narrow query scope on 429 responses or use an API key with higher limits. <br>


## Reference(s): <br>
- [Exa MCP Setup](artifact/references/exa-mcp-setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/tokyo-s/exa-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline tool names, links, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be concise findings with source links and explicit unknowns when research is performed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
