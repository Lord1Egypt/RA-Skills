## Description:

Use when creating, editing, debugging, or validating Dify workflow DSL for self-hosted Dify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arn0ld87](https://clawhub.ai/user/arn0ld87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, edit, debug, and validate Dify workflow DSL for self-hosted Dify instances, especially when making minimal import/export-based workflow changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example workflows may send data to configured external APIs or LLM providers if imported and run.

Mitigation: Verify model providers, external URLs, API key handling, and data-sharing behavior before importing or running templates.

Risk: Templates can be mistaken for production-ready workflows without matching the target Dify instance.

Mitigation: Start from an export of the target instance, make minimal edits, run local validation, and verify re-import on the same instance.

Risk: Fetched or user-supplied content may be exposed to downstream LLM providers.

Mitigation: Prefer redaction, trusted endpoints, and scoped test credentials when evaluating workflows.

## Reference(s):

- [Workflow Structure](references/workflow_structure.md)
- [Node Types](references/node_types.md)
- [Edge Types](references/edge_types.md)
- [Variable Syntax](references/variable-syntax.md)
- [Common Gotchas](references/common-gotchas.md)
- [Current Patterns](references/current_patterns.md)
- [Advanced Patterns](references/advanced_patterns.md)
- [Retrieval Patterns](references/retrieval_patterns.md)
- [Dify Docs](https://docs.dify.ai/)
- [Dify GitHub Repository](https://github.com/langgenius/dify)
- [Dify Releases](https://github.com/langgenius/dify/releases)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with YAML, code, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Dify workflow DSL drafts or edits that require validation against a target instance export before import.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
