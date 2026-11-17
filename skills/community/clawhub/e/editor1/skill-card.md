## Description:

This skill helps users view and manage Knot platform agent draft configurations, including listing editable agents and models, regenerating drafts, editing draft fields, and publishing drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inspect Knot agent draft settings, update names, descriptions, welcome messages, system prompts, and default models, then publish reviewed draft changes when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill disables TLS certificate verification while sending credentials to the Knot service.

Mitigation: Install only when the Knot service and network path are trusted, treat environment credentials as sensitive, and prefer use only after TLS verification is fixed or a trusted CA bundle is configured.

Risk: Draft regeneration, modification, and publishing can overwrite or expose production agent behavior.

Mitigation: Require explicit user confirmation before regeneration or publishing, inspect stale-draft warnings, and review all draft changes before making them live.

Risk: The modify workflow can read prompt content from @file arguments.

Mitigation: Inspect referenced files before execution and avoid passing files that contain unrelated secrets or unintended instructions.

## Reference(s):

- [Knot Agent Editor API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses environment credentials for Knot API access and may display complete draft configuration fields, including full system prompts.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
