## Description: <br>
Publishes Markdown or HTML to a shareable dochost.io page and returns the hosted URL to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zyli5313](https://clawhub.ai/user/zyli5313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to publish generated documents, reports, README content, or HTML pages to a dochost.io link for sharing. It is useful when an assistant needs to turn finished content into a hosted page and return the resulting URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing sends selected Markdown or HTML to dochost.io and creates a public or unlisted web page. <br>
Mitigation: Review and redact sensitive content before publishing, and do not include secrets, tokens, private keys, or confidential material in the page body. <br>
Risk: The skill requires a dochost API key for authenticated publishing. <br>
Mitigation: Provide the key through the DOCHOST_API_KEY environment variable and avoid placing it in published content, command logs, or shared documents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zyli5313/dochost-publish) <br>
- [dochost](https://dochost.io) <br>
- [dochost MCP API Endpoint](https://dochost.io/api/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with JSON-RPC and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a dochost.io URL; may include expiration timing and an edit token from the publish response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
