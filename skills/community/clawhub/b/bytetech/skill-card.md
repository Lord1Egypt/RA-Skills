## Description: <br>
Fetches ByteTech technical article metadata, directory structure, and document content by using Chrome DevTools MCP to connect to the user's local Chrome session, reuse login state, inspect APIs, and extract article data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiushibang](https://clawhub.ai/user/qiushibang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to retrieve ByteTech article summaries, metadata, recommendations, team context, and selected full document bodies from an authenticated browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reuses a logged-in Chrome and Feishu session and can access sensitive authenticated ByteTech article, author, network, and document data. <br>
Mitigation: Use a dedicated browser profile, avoid unrelated logged-in sessions, and fetch full document bodies only for specific articles the user chooses. <br>
Risk: Network inspection and response export behavior can reveal or save sensitive headers, request bodies, responses, or document content. <br>
Mitigation: Avoid full header and body dumps unless necessary, keep exported responses scoped to the requested article, and remove saved sensitive files when no longer needed. <br>


## Reference(s): <br>
- [ByteTech API Reference](references/api-reference.md) <br>
- [ClawHub ByteTech Release](https://clawhub.ai/qiushibang/bytetech) <br>
- [Publisher Profile](https://clawhub.ai/user/qiushibang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authenticated ByteTech metadata, article links, summaries, metrics, author fields, and selected document content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
