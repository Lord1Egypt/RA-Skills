## Description: <br>
Searches DuckDuckGo and fetches readable web page content without requiring API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mengbin92](https://clawhub.ai/user/mengbin92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to perform web searches and retrieve readable content from URLs when native web search is unavailable or an API-key-free workflow is preferred. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and requested URLs may be sent to third-party web services. <br>
Mitigation: Avoid secrets, sensitive investigation terms, and internal-only URLs when using this skill. <br>
Risk: The URL fetcher can request broad web destinations, including private or localhost-style targets if supplied by a user. <br>
Mitigation: Review requested URLs before execution and avoid localhost, private-network, and internal-only links. <br>
Risk: Fetched page text is untrusted web content and may contain misleading instructions. <br>
Mitigation: Treat fetched content as evidence only and review it before using it to drive agent actions. <br>


## Reference(s): <br>
- [DuckDuckGo](https://duckduckgo.com) <br>
- [DuckDuckGo Lite Search Endpoint](https://lite.duckduckgo.com/lite/) <br>
- [ClawHub Skill Page](https://clawhub.ai/mengbin92/ddg-search-fetch) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [JSON or plain text from command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include title, URL, and snippet; fetched pages include URL, title, extracted text, status code, and error information when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
