## Description:

Use when managing a self-hosted Dify instance, checking feature feasibility, or orchestrating apps, prompts, datasets, and knowledge-base operations via the dify-manager MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arn0ld87](https://clawhub.ai/user/arn0ld87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage self-hosted Dify apps, prompts, datasets, knowledge retrieval, and health checks through the dify-manager MCP server. It also helps evaluate version-sensitive Dify features against official documentation and release notes before operational changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through powerful self-hosted Dify management actions, including app creation, prompt updates, dataset changes, uploads, and deletion.

Mitigation: Use narrowly scoped Dify credentials, verify target endpoints and object IDs before write actions, and require explicit confirmation before destructive operations.

Risk: Secrets could be exposed if Dify credentials are placed in prompts, examples, logs, or generated content.

Mitigation: Keep Dify API keys and console credentials in local configuration or a secret store, and avoid writing them into prompts, logs, examples, or skill documentation.

Risk: Self-hosted Dify behavior can differ by version, especially for plugins, providers, triggers, OAuth, and workflow engine features.

Mitigation: Check official Dify documentation, releases, and the target instance version before making version-sensitive feature claims or operational changes.

## Reference(s):

- [Dify Docs](https://docs.dify.ai/)
- [Dify GitHub Repository](https://github.com/langgenius/dify)
- [Dify Releases](https://github.com/langgenius/dify/releases)
- [Dify Official Plugins](https://github.com/langgenius/dify-official-plugins)
- [Dify Key Concepts](https://docs.dify.ai/en/use-dify/getting-started/key-concepts)
- [Dify Application Orchestrate](https://docs.dify.ai/versions/3-0-x/en/user-guide/application-orchestrate/readme)
- [Dify Knowledge Retrieval Node](https://docs.dify.ai/en/use-dify/nodes/knowledge-retrieval)
- [Dify Plugin Workspace Docs](https://docs.dify.ai/en/use-dify/workspace/plugins)
- [Dify Plugin Trigger Docs](https://docs.dify.ai/en/use-dify/nodes/trigger/plugin-trigger)
- [App Types Reference](references/app_types.md)
- [App Type Decision Guide](references/app_type_decision_guide.md)
- [Knowledge Retrieval Reference](references/knowledge_retrieval.md)
- [Plugins And Providers Reference](references/plugins_and_providers.md)
- [Self-Hosted Operations Reference](references/self_hosted_operations.md)
- [Version Notes Reference](references/version_notes.md)
- [Plugin Integration Patterns Reference](references/plugin_integration_patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks, API call examples, and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Dify MCP tool calls and self-hosted configuration variables; secrets are expected to remain in local configuration.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
