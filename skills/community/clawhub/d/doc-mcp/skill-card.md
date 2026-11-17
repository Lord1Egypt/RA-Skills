## Description:

Search, browse, and read Doctor of Credit bank bonus and credit card posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guavatech-llc](https://clawhub.ai/user/guavatech-llc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search, browse, and read Doctor of Credit posts about bank bonuses, credit card offers, brokerage deals, and related personal finance content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured MCP server is installed through an unpinned npm package, so future executions may run code that differs from the reviewed release.

Mitigation: Pin @guava-tech/doc-mcp to a reviewed exact version before deployment and re-run review when updating it.

Risk: The skill requires internet access to Doctor of Credit content through the MCP server.

Mitigation: Run it with least-privilege filesystem, environment, and network access appropriate for the intended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guavatech-llc/skills/doc-mcp)
- [Doctor of Credit](https://www.doctorofcredit.com/)
- [npm package: @guava-tech/doc-mcp](https://www.npmjs.com/package/@guava-tech/doc-mcp)
- [Project homepage](https://github.com/Guava-Tech-LLC/DoC-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text summaries with MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on live access to doctorofcredit.com through the configured MCP server.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
