## Description:

A Chinese-language diagram skill for creating and managing Mermaid and Graphviz-style diagrams with brand themes, batch rendering, exports, version comparison, and team workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and business teams use this skill to generate flowcharts, architecture diagrams, reports, and batch-rendered diagram exports from natural-language requests and structured options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt an agent to read or write files, run local commands, call external APIs, and handle credentials beyond a narrow diagram-generation task.

Mitigation: Use least-privilege workspace access, explicit output paths, and review generated commands, batch operations, webhook URLs, and credential handling before execution.

Risk: External callbacks, API integrations, and logs can expose diagram inputs, file paths, credentials, or business data if configured carelessly.

Mitigation: Use trusted HTTPS endpoints, keep secrets in environment variables or a secret manager, redact sensitive values from logs, and validate callback destinations before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/diagram-tools-tool-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagram source, rendered export instructions, execution logs, status JSON, and audit-oriented metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
