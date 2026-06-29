## Description: <br>
Provides an MCP-style lookup service for Chinese Magic: The Gathering card information, including card search, set lookup, set card listing, and card-image text composition through the XiaoBenYang service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve Chinese Magic: The Gathering card and set data through structured tool calls. It can search cards by query syntax, fetch individual cards by set and collector number, list sets and set contents, and generate image-composed text from card images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The XiaoBenYang API key is stored in a local plaintext .env file. <br>
Mitigation: Use a dedicated API key, keep the workspace private, restrict file access, and rotate the key if the workspace or .env file is exposed. <br>
Risk: The skill depends on the external XiaoBenYang service for card lookup and image-composition behavior. <br>
Mitigation: Confirm the service is approved for the intended environment and avoid sending sensitive information through lookup or image-composition requests. <br>
Risk: The hzls tool can generate card-image-composed text, which is broader than basic card lookup. <br>
Mitigation: Review generated image output before sharing it and disable or avoid this tool where only lookup functionality is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alinklab/gathering-card-lookup-service) <br>
- [XiaoBenYang service](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown summaries and structured JSON-derived results from tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a XiaoBenYang API key before tool calls can succeed; tool responses include success status, raw upstream data, and a status message.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
