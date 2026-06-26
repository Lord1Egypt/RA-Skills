## Description: <br>
Context7 MCP provides intelligent documentation search and context for libraries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheSethRose](https://clawhub.ai/user/TheSethRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to search Context7 for library documentation and retrieve LLM-reranked context for implementation questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation search terms and questions are sent to Context7, which may expose sensitive project details if prompts include credentials, private URLs, customer data, or proprietary code. <br>
Mitigation: Use a dedicated Context7 API key, keep .env files out of source control and logs, and avoid sending secrets or proprietary data in queries. <br>
Risk: The skill depends on a Context7 API key for external documentation retrieval. <br>
Mitigation: Rotate the key if exposed and install only when external Context7 queries are acceptable for the deployment environment. <br>


## Reference(s): <br>
- [Context7 MCP on ClawHub](https://clawhub.ai/TheSethRose/context7) <br>
- [Context7 documentation](https://context7.com/docs) <br>
- [Context7 llms.txt](https://context7.com/docs/llms.txt) <br>
- [Context7 dashboard](https://context7.com/dashboard) <br>
- [Context7 library search API](https://context7.com/api/v2/libs/search) <br>
- [Context7 context API](https://context7.com/api/v2/context) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a Context7 API key.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
