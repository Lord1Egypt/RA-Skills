## Description:

Ex-Coder guides agents in using the Ex-Coder Autonomy CLI for model selection, delegated coding workflows, sessions, snapshots, LSP, HTTP API, and MCP integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lordmahakaal](https://clawhub.ai/user/lordmahakaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to operate Ex-Coder Autonomy for implementation, review, analysis, and session workflows while delegating external-model runs through sub-agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Use with real repositories or credentials can grant broad filesystem, shell, remote-control, and persistent configuration authority.

Mitigation: Review before installation, keep filesystem access scoped to the project, prefer approval prompts, and avoid letting agents write user-provided values into shell startup files.

Risk: Under-scoped MCP examples can expose more filesystem access than intended or resolve unreviewed packages.

Mitigation: Avoid root filesystem MCP mounts, use project-scoped paths, and pin MCP packages instead of relying on unreviewed npx resolution.

Risk: HTTP API access can enable remote control of the coding environment.

Mitigation: Expose the API only to trusted local access and require appropriate authentication when the server is enabled.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/lordmahakaal/skills/excoder-autonomy)
- [OpenRouter](https://openrouter.ai)
- [OpenRouter Models](https://openrouter.ai/models)
- [OpenRouter API Docs](https://openrouter.ai/docs)
- [Ex-Coder GitHub](https://github.com/ex-coder/ex-coder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command examples, environment variable names, workflow steps, and concise delegation instructions.]

## Skill Version(s):

1.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
