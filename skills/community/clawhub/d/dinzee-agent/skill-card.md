## Description:

DinzeeAgent is a cross-border e-commerce data agent that lets an agent discover Dinzee gateway data sources at runtime, sync bundled business skills locally, invoke matched tools or workflows, and summarize e-commerce research and billing results for the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yefeng311](https://clawhub.ai/user/yefeng311)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use DinzeeAgent to run cross-border e-commerce research, product analysis, advertising diagnostics, and bundled business workflows through the Dinzee gateway. The skill helps agents discover available data providers at runtime, call selected tools, sync Dinzee business skills, and return concise reports with billing context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or update remote skill packages into the live agent runtime.

Mitigation: Use sync-skills, skill-install, or bulk updates only when the user intends to trust Dinzee-delivered packages and has reviewed the package source.

Risk: Gateway call data may be saved locally with broad data-file permissions.

Mitigation: Use --no-save for sensitive requests or configure DINZEE_DATA_DIR to a private location in single-user or isolated deployments.

Risk: The skill depends on Dinzee gateway availability, policy, authentication, billing, and upstream provider behavior.

Mitigation: Run status, providers, and list-tools before paid workflows, and handle gateway errors as user-facing availability or account issues.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yefeng311/skills/dinzee-agent)
- [Dinzee Gateway](https://gateway.dinzee.ai/)
- [Keepa API Reference](references/keepa.md)
- [Seller Sprite MCP Reference](references/seller-sprite.md)
- [Server Skill Workflows](references/server-skill-workflows.md)
- [SIF MCP Reference](references/sif.md)
- [Sorftime MCP Reference](references/sorftime.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON data outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save gateway call records locally unless --no-save or a private DINZEE_DATA_DIR is used.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
