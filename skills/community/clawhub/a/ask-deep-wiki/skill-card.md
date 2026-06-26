## Description: <br>
For questions about Light Protocol's SDK, smart contracts and Solana development, Claude Code features, or agent skills. AI-powered answers grounded in repository context via DeepWiki MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tilo-14](https://clawhub.ai/user/tilo-14) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to answer technical questions about Light Protocol, Solana development, Claude Code, and agent skills by combining local repository reads with public DeepWiki and documentation searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local project files and may send question context to MCP or search providers. <br>
Mitigation: Use it only in workspaces where agent-readable files are appropriate, and avoid asking questions that include secrets, private keys, wallet credentials, unreleased confidential code, or other sensitive local data. <br>
Risk: Repository-grounded answers can still be incomplete or outdated if public wiki, documentation, or search context is missing. <br>
Mitigation: Review cited sources, file references, and code examples before applying the guidance in production. <br>


## Reference(s): <br>
- [ZK Compression documentation](https://zkcompression.com/) <br>
- [Light Protocol audits](https://github.com/Lightprotocol/light-protocol/tree/main/audits) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with code examples and source references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP-backed repository citations, file paths, and line references when available.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
