## Description:

Automates publishing content to Xiaohongshu, including image/text posts, login-status checks, and QR-code login support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragon015](https://clawhub.ai/user/dragon015)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to prepare and run Xiaohongshu publishing workflows for image/text posts, batch posting, scheduled publishing, and login checks through a local MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external MCP server executable and npm tooling whose provenance is not verified by the evidence.

Mitigation: Install only from trusted sources, verify executable and package provenance before use, and run under a non-admin account.

Risk: Publishing flows can post content publicly without strong safeguards, including bundled examples with hardcoded post content.

Mitigation: Confirm the target Xiaohongshu account, title, content, images, and tags before publishing; do not run bundled publish_*.js examples unless that public post is intended.

Risk: Private text or images can be exposed through the publishing workflow.

Mitigation: Avoid sensitive or private images and text, and use login-status checks before posting.

## Reference(s):

- [Configuration Guide](references/config.md)
- [Xiaohongshu MCP Project](https://github.com/xpzouying/xiaohongshu-mcp)
- [mcporter Documentation](http://mcporter.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, PowerShell, JSON, and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may initiate live Xiaohongshu publishing when executed against a logged-in local MCP server.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
