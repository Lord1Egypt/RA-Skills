## Description: <br>
A Model Context Protocol skill that lets agents query fund knowledge and search Eastmoney stock information through XiaoBenYang-backed tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to route fund-knowledge and stock-search questions to the configured XiaoBenYang MCP API, then present the returned raw JSON as concise user-facing results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a XiaoBenYang API key and can store it in a local plaintext .env file. <br>
Mitigation: Use a dedicated API key, restrict access to the workspace, and rotate the key if the local .env file may have been exposed. <br>
Risk: Fund, stock, and research queries are sent to an upstream API provider. <br>
Mitigation: Avoid entering highly sensitive investment or research queries unless the upstream provider and its data handling are acceptable. <br>
Risk: The skill should not fabricate fund or stock information when an API key or required parameter is missing. <br>
Mitigation: Ask the user for the missing API key or parameter before calling tools, and report upstream failures instead of inventing results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/fund-knowledge-query) <br>
- [XiaoBenYang API key service](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Markdown/text summary of raw JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY value and network access to the upstream XiaoBenYang API.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
