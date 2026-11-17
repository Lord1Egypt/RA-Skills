## Description:

Build repeatable data-to-Docs pipelines from Sheets and Drive sources. Use for automated status reports, template-based document assembly, and scheduled publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x-professor](https://clawhub.ai/user/0x-professor)

### License/Terms of Use:


## Use Case:

Developers and documentation operators use this skill to define repeatable pipelines that transform Workspace data sources into generated Google Docs reports and publishing artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can create parent directories and overwrite the output file path provided by the user.

Mitigation: Point --output at a dedicated generated-artifact path and check for important existing files before execution.

Risk: The dry-run flag is present in output details but does not prevent the helper from writing the requested output artifact.

Mitigation: Do not rely on --dry-run as a no-write mode unless the script is fixed; use a disposable output path when testing.

## Reference(s):

- [Docs Pipeline Guide](references/docs-pipeline-guide.md)
- [ClawHub skill page](https://clawhub.ai/0x-professor/skills/docs-pipeline-automation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON, Markdown, or CSV pipeline artifact with concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper reads optional local JSON input up to 1048576 bytes and writes the requested output artifact.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
