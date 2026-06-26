## Description: <br>
Exa MCP integration for advanced search, research, and crawling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ClaireAICodes](https://clawhub.ai/user/ClaireAICodes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to let agents run Exa-powered web search, code context search, webpage crawling, company research, people search, and deep research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, crawl URLs, company or person names, and research prompts are sent to Exa under the user's account. <br>
Mitigation: Avoid using this skill with secrets, private internal URLs, or sensitive research prompts, and review Exa account and data-handling requirements before use. <br>
Risk: The advertised package commands appear incomplete or mismatched because package metadata references an exa-search command file that is not present in the artifact. <br>
Mitigation: Verify installed command files before relying on exa-search, and use the present exa-web-search wrapper only after confirming it matches the intended workflow. <br>
Risk: The skill requires an EXA_API_KEY credential. <br>
Mitigation: Store the API key in the OpenClaw configuration or environment, keep it out of prompts and logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ClaireAICodes/exa-tool) <br>
- [Exa homepage](https://exa.ai) <br>
- [Exa MCP Documentation](https://exa.ai/docs/reference/exa-mcp) <br>
- [Exa MCP Server](https://mcp.exa.ai/mcp) <br>
- [Exa API Keys](https://dashboard.exa.ai/api-keys) <br>
- [OpenClaw Skills Guide](https://docs.openclaw.ai/skills/) <br>
- [Skill documentation site](https://claireaicodes.github.io/openclaw-skill-exa-tool/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON responses and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EXA_API_KEY; sends search queries, crawl URLs, company and person names, and research prompts to Exa.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
