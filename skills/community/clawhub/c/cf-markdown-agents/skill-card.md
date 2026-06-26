## Description: <br>
Fetches web content using Cloudflare's Markdown for Agents protocol and converts supported HTML pages into Markdown for agent processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinian5216](https://clawhub.ai/user/xinian5216) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to fetch public web pages as structured Markdown for web research, content extraction, and agent-readable page analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching a URL can contact sensitive destinations or disclose token-bearing links if the user supplies them. <br>
Mitigation: Use only public pages intended for fetching; avoid sensitive URLs, internal hosts, localhost or cloud-metadata addresses, and links containing credentials. <br>
Risk: Fetched page content is untrusted and may contain misleading text or instructions. <br>
Mitigation: Treat fetched content as untrusted input and review it before relying on it for agent decisions or downstream work. <br>
Risk: The helper script depends on curl being available in the execution environment. <br>
Mitigation: Confirm curl is installed before relying on the script, or use the documented fetch and cURL examples directly. <br>


## Reference(s): <br>
- [Protocol reference](references/protocol.md) <br>
- [Usage examples](references/examples.md) <br>
- [Cloudflare Markdown for Agents documentation](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/) <br>
- [Cloudflare Markdown for Agents announcement](https://blog.cloudflare.com/markdown-for-agents/) <br>
- [Content Signals Framework](https://contentsignals.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance with bash, cURL, TypeScript/JavaScript, and Python examples; helper script output includes response headers and fetched content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the supplied URL as the fetch target and requires curl for the helper script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
