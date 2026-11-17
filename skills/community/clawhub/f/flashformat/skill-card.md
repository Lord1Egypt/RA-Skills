## Description:

Provides five repository-local format conversion scripts for YAML, JSON, Markdown, JSON minification, and conservative YAML auto-fixing in offline CLI and pipeline workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phantom5125](https://clawhub.ai/user/phantom5125)

### License/Terms of Use:

BSD 2-Clause

## Use Case:

Developers and engineers use this skill to convert YAML, JSON, and Markdown locally, batch format data, and normalize text in CI or offline workflows without calling the FlashFormat API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The converter scripts can read local input files and optionally write output files.

Mitigation: Use the scripts only with files intended for conversion and choose output paths deliberately to avoid accidental overwrites.

Risk: The skill requires a Python runtime dependency and is installed from a copied repository version.

Mitigation: Install PyYAML in an isolated Python environment when possible and review the repository version copied into Codex before deployment.

## Reference(s):

- [IO Contracts](references/io-contracts.md)
- [FlashFormat](https://www.flashformat.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and converted text, JSON, or YAML output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports stdout or output-file delivery and optional structured JSON success or failure envelopes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
