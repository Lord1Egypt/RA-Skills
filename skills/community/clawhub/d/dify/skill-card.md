## Description:

Dify helps agents guide developers through building LLM applications, workflows, agents, knowledge bases, API integrations, and self-hosted Dify deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krx1511](https://clawhub.ai/user/krx1511)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill for concise Dify guidance when creating AI applications, designing workflows, configuring RAG knowledge bases, setting up model providers, calling Dify APIs, or preparing a self-hosted deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a copy-paste shell installer pattern for Ollama that downloads and executes a remote script.

Mitigation: Review commands before running them and prefer a verified package, pinned release, or manual download-and-inspect installation flow.

Risk: Dify API examples involve API keys, file uploads, and conversation deletion operations.

Mitigation: Use scoped Dify API keys, avoid uploading sensitive files unless intended, and confirm destructive API calls before execution.

## Reference(s):

- [Dify API Complete Reference](references/api.md)
- [Dify Workflow Nodes](references/workflow-nodes.md)
- [Dify Knowledge Base Configuration](references/knowledge-base.md)
- [Dify Model Provider Configuration](references/model-providers.md)
- [Dify Official Documentation](https://docs.dify.ai)
- [Dify GitHub Repository](https://github.com/langgenius/dify)
- [Dify GitHub Discussions](https://github.com/langgenius/dify/discussions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with API examples, JSON snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance; review commands and API operations before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
