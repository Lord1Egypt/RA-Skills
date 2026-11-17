## Description:

Use ctxd to inspect tracked source paths and read current context for an agent task. Apply when a user wants answers grounded in changing project sources, needs to refresh indexed context, or wants to verify an edit or removal through ctxd.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctxddev](https://clawhub.ai/user/ctxddev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect current content from selected, tracked project folders and ground answers or edit and removal checks in the source files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected project folders may contain secrets or unrelated private files.

Mitigation: Register only project folders intended for the task and exclude secrets and unrelated private files.

Risk: Retrieved source content can reach the configured AI provider.

Mitigation: Review provider and data-handling settings before indexing or querying sensitive content.

Risk: The external ctxd package was not audited as part of this release review.

Mitigation: Review the package and consider pinning the documented version for reproducible installation.

## Reference(s):

- [ctxd documentation](https://ctxd.dev)
- [ctxd-agent-plugin source and installation instructions](https://github.com/ctxddev/ctxd-agent-plugin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Natural-language answers with source paths and relevant line references; setup guidance may include shell commands and JSON configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers are grounded in the selected tracked source content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
