## Description:

A Word document layout and styling system based on the docx npm library for generating structured .docx documents with professional colors, tables, and heading hierarchy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperkwok](https://clawhub.ai/user/casperkwok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use this skill to generate runnable Node.js scripts that create structured Word documents such as PRDs, technical plans, project reports, and meeting notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scripts create local JavaScript and .docx files and may overwrite existing files if paths or filenames collide.

Mitigation: Review generated filenames and output paths before running the script, especially in shared or important directories.

Risk: The skill expects installation of the docx npm package before generated scripts can run.

Mitigation: Review package installation in the target environment and run generated scripts only after dependencies are approved.

## Reference(s):

- [Docx Template Reference](references/docx-template.js)
- [Example PRD Generator](examples/example-prd.js)
- [Docx Builder on ClawHub](https://clawhub.ai/casperkwok/skills/docx-builder)
- [OpenClaw ClawHub](https://github.com/openclaw/clawhub)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown containing JavaScript code and command guidance; generated scripts create .docx files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npm, and the docx npm package; writes local .js and .docx outputs.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
