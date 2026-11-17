## Description:

Chexian Baodan Tong helps insurance agents and carrier staff organize vehicle-insurance policy PDFs by extracting plate, policyholder, and policy-number fields, renaming files, and packaging the folder as a ZIP archive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwbwin](https://clawhub.ai/user/wwbwin)

### License/Terms of Use:

MIT-0

## Use Case:

External insurance agents and insurance company staff use this skill to process folders of vehicle-insurance policy PDFs, extract key identifiers, rename recognized files, and package the organized folder for archiving or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default ZIP packaging can include unrelated files from the selected folder.

Mitigation: Run the skill only on a dedicated folder containing the intended insurance PDFs, or use --no-pack and inspect any archive before sharing it.

Risk: API mode can send a bearer key and file metadata to the configured endpoint.

Mitigation: Prefer local mode; use --api only with a trusted endpoint and appropriate API key handling.

Risk: The script can directly rename original PDF files.

Mitigation: Use --no-rename for preview runs or work from a backup or dedicated copy of the source folder.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwbwin/skills/chexian-baodan-tong)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and environment variable configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide execution of a local Python script that renames PDFs and writes a ZIP archive in the selected folder.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
