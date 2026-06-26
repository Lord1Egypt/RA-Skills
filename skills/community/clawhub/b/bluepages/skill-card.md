## Description: <br>
Look up wallet address to Twitter/X and Farcaster identity mappings via Bluepages.fyi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jesse-pallok](https://clawhub.ai/user/jesse-pallok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Bluepages to attribute Ethereum wallet addresses to Twitter/X or Farcaster identities and to find wallet addresses for social handles. It supports single and batch lookups through the Bluepages MCP server or direct HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an Ethereum private key and paid x402 wallet operations for lookups or credit purchases. <br>
Mitigation: Prefer BLUEPAGES_API_KEY. If PRIVATE_KEY is necessary, use only a dedicated low-balance wallet and require explicit approval for every paid lookup or credit purchase. <br>
Risk: The skill depends on an external MCP package for wallet-identity lookups. <br>
Mitigation: Review or pin the external MCP package before running it. <br>


## Reference(s): <br>
- [Bluepages API documentation](https://bluepages.fyi/docs.html) <br>
- [Bluepages API keys](https://bluepages.fyi/api-keys.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command snippets and lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BLUEPAGES_API_KEY or a dedicated low-balance PRIVATE_KEY; paid lookups should be explicitly approved.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
