## Description:

Answers technical questions about Light Protocol, Solana development, Claude Code, and agent skills using local repository context and DeepWiki MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tilo-14](https://clawhub.ai/user/tilo-14)

### License/Terms of Use:


## Use Case:

Developers and technical users use this skill to answer repository-grounded questions about Light Protocol, Solana development, Claude Code, and agent skill patterns. It gathers local file context, consults public research sources when allowed, and returns precise Markdown answers with code examples or source references when relevant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Questions and summarized context may be used with external research tools.

Mitigation: Avoid including secrets, private keys, access tokens, customer data, proprietary source code, or other sensitive material in prompts.

Risk: Repository-grounded answers may still contain incorrect or stale technical guidance.

Mitigation: Verify cited source references, code examples, and commands before applying them to production work.

Risk: The release has no server-resolved GitHub import provenance.

Mitigation: Verify the publisher profile and any install source before installing or relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tilo-14/skills/ask-deep-wiki)
- [ZK Compression documentation](https://zkcompression.com/)
- [Light Protocol GitHub organization](https://github.com/Lightprotocol)
- [Light Protocol audits](https://github.com/Lightprotocol/light-protocol/tree/main/audits)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with source references and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not directly write files or execute shell commands; answers may be informed by public MCP or web research tools.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
