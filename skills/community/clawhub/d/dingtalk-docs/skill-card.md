## Description: <br>
Manages DingTalk cloud documents, folders, and document content, including search, creation, reading when available, and writing through DingTalk document tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aliramw](https://clawhub.ai/user/aliramw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external users, and developers use this skill when an agent needs to operate DingTalk cloud documents with the user's configured DingTalk document credential. It is suited for finding documents, creating documents or folders, writing Markdown content, and reading document content when the DingTalk service exposes the read method. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write to DingTalk documents using the configured credential, including overwrite mode. <br>
Mitigation: Confirm whether the user wants overwrite or append behavior before write operations, and review document targets before allowing imports or updates. <br>
Risk: Requests involving tables or multidimensional tables may be ambiguous because the documented scope is inconsistent. <br>
Mitigation: Ask the user to confirm the exact target type before creating or modifying tables, multidimensional tables, or other non-document nodes. <br>
Risk: The read method may not be available in every DingTalk MCP instance. <br>
Mitigation: Check whether get_document_content_by_url is exposed before promising read access, and explain unavailable reads as service rollout status rather than a local configuration failure. <br>
Risk: The DingTalk service URL contains an access token. <br>
Mitigation: Store the URL with mcporter configuration or an environment variable and avoid echoing or committing credential-bearing URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aliramw/dingtalk-docs) <br>
- [Publisher profile](https://clawhub.ai/user/aliramw) <br>
- [Project homepage from ClawHub metadata](https://github.com/aliramw/dingtalk-docs) <br>
- [DingTalk MCP documentation](https://mcp.dingtalk.com) <br>
- [API reference](references/api-reference.md) <br>
- [Error codes](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with DingTalk document command examples and local file workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, overwrite, append, import, or export document content through mcporter and the configured DingTalk document service.] <br>

## Skill Version(s): <br>
0.3.4 (source: frontmatter, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
