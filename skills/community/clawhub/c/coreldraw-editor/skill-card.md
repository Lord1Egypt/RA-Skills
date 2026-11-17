## Description:

Inspect, edit, and export CorelDRAW CDR files via COM automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, developers, and automation engineers use this skill to inspect CDR structure, generate previews and exports, and apply copy-first edits through an installed CorelDRAW application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CorelDRAW automation requires a trusted Windows environment with CorelDRAW and pywin32 installed.

Mitigation: Install only from a trusted Python package source on a Windows system where CorelDRAW is installed and intended for automation.

Risk: Document edits such as delete, ungroup, rasterize, color conversion, or overwriting files can be destructive.

Mitigation: Inspect files first, use copy-first edit plans by default, avoid --in-place unless intentionally modifying the original, and use --overwrite only when replacement is intended.

Risk: Shape indexes and visual rendering can change after edits or vary with missing fonts, linked assets, effects, and export settings.

Mitigation: Re-inspect edited copies and export previews or contact sheets before reporting completion.

## Reference(s):

- [CorelDRAW Editor ClawHub skill page](https://clawhub.ai/stanestane/skills/coreldraw-editor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON operation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of JSON metadata, CSV manifests, image previews, exported assets, and edited CDR copies when the bundled script is run.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
