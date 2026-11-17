## Description:

n8n workflow bridge pack for exporting OpenClaw pipelines to n8n format and importing n8n workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation engineers use this skill to move workflow definitions between OpenClaw and n8n, including exporting OpenClaw pipelines to n8n JSON and importing n8n workflow files with validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow export and import can move automation logic across systems, so unreviewed workflow JSON may encode actions that behave differently after conversion.

Mitigation: Review exported or imported workflow JSON before using it in automation, and confirm trust in the required mcp-openclaw-extensions provider before installation.

Risk: The source includes a French AI-generated-content warning, which may be missed by English-only reviewers.

Mitigation: Translate or duplicate the warning in English during release review so the need for human validation is clear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/skills/firm-n8n-bridge-pack)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML usage examples, shell-style tool invocations, and JSON workflow file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or consumes OpenClaw and n8n workflow JSON through the required mcp-openclaw-extensions provider.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
