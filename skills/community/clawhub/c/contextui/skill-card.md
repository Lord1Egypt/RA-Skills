## Description:

ContextUI helps agents build, run, test, and publish local visual workflows using React TSX, local Python backends, scoped UI automation, and the ContextUI Exchange.

This skill is ready for commercial/non-commercial use.

## Publisher:

[midz99](https://clawhub.ai/user/midz99)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create ContextUI workflows, manage local workflow backends, test UI behavior inside the ContextUI app window, and publish or browse workflows through the ContextUI Exchange.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags broad local workflow-development authority, including marketplace, local execution, and persisted MCP capabilities.

Mitigation: Install only when comfortable granting this authority, and consider using an isolated environment for untrusted workflows.

Risk: Marketplace operations can use CONTEXTUI_API_KEY for publishing, downloading, comments, likes, deletes, or billing-adjacent actions.

Mitigation: Provide CONTEXTUI_API_KEY only when Exchange features are needed and require explicit confirmation before account-affecting actions.

Risk: Downloaded marketplace workflows may be untrusted code.

Mitigation: Stage, review, and validate downloaded workflows before placing them in an executable workflow directory.

Risk: Local workflow backends and connected external MCP servers can run commands or services under the user's OS permissions.

Mitigation: Pin and review dependencies, monitor package installs, and connect only trusted persistent MCP server commands or URLs.

## Reference(s):

- [ContextUI Website](https://contextui.ai)
- [ClawHub Skill Listing](https://clawhub.ai/midz99/skills/contextui)
- [ContextUI YouTube Channel](https://www.youtube.com/@ContextUI)
- [Workflow Building Guide](references/workflow-guide.md)
- [ContextUI MCP Tools API Reference](references/mcp-tools.md)
- [ServerLauncher Python Backend Pattern](references/server-launcher.md)
- [ContextUI Exchange](references/exchange.md)
- [ContextUI Exchange API](references/exchange-api.md)
- [Exchange Categories](references/exchange-categories.md)
- [HuggingFace Cache Monitoring](references/cache-monitoring.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, JSON, TSX, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local filesystem paths, localhost server URLs, and ContextUI Exchange API calls when requested.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
