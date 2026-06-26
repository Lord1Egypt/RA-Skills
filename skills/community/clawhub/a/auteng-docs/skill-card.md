## Description: <br>
Publish technical docs with Mermaid diagrams, KaTeX math, and code highlighting. Persistent workspace, shareable links, versioning. Free. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[operator-auteng-ai](https://clawhub.ai/user/operator-auteng-ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical agents use this skill to publish rendered Markdown documentation, including diagrams, math, code examples, API specs, architecture notes, and research reports, to AutEng share links or persistent workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Published or shared documents can be public and may expose sensitive content. <br>
Mitigation: Review markdown for secrets, credentials, private keys, internal URLs, and confidential data before publishing or sharing. <br>
Risk: Workspace operations use wallet signatures for authentication. <br>
Mitigation: Use a dedicated low-risk wallet or signer for agent workloads and never provide private keys in agent chat. <br>
Risk: The skill depends on the external @auteng/docs package and outbound HTTPS requests to AutEng services. <br>
Mitigation: Verify the package and network destination before use in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/operator-auteng-ai/auteng-docs) <br>
- [Project homepage](https://github.com/operator-auteng-ai/docs) <br>
- [AutEng Docs MCP server](https://auteng.ai/mcp/docs) <br>
- [AutEng Docs API](https://auteng.ai/api/docs) <br>
- [AutEng llms.txt](https://auteng.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, TypeScript examples, API endpoint tables, and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces documentation-publishing instructions and examples; published AutEng documents may become public share links.] <br>

## Skill Version(s): <br>
1.1.1 (source: VERSION.txt and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
