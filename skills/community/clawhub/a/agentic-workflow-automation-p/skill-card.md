## Description:

Design and generate reusable multi-step workflow blueprints with explicit triggers, ordered steps, fallback behavior, and portable JSON, Markdown, or CSV outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to turn workflow requirements into structured blueprints for implementation in orchestration tools such as n8n or internal platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script can create or overwrite output files, including when dry-run output may imply no file changes.

Mitigation: Run it only with an explicit safe output path, inspect that location before execution, and do not rely on --dry-run to prevent file writes.

Risk: CSV exports from untrusted workflow inputs may be unsafe to open in spreadsheet tools.

Mitigation: Review CSV output before opening it in spreadsheet software and prefer JSON or Markdown for untrusted inputs.

## Reference(s):

- [Workflow Blueprint Guide](references/workflow-blueprint-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [JSON, Markdown, or CSV workflow blueprint artifacts with implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include ordered step lists, trigger metadata, dependency structure, fallback behavior, and portable blueprint files.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
