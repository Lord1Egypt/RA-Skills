## Description:

Batch Format Converter helps agents convert batches of CSV, Excel, JSON, PDF, Markdown, DOCX, HTML, image, and TXT files between supported output formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiji0802](https://clawhub.ai/user/qiji0802)

### License/Terms of Use:

MIT-0

## Use Case:

Data professionals, analysts, operations teams, finance users, document workers, and developers can use this skill to batch convert common data and document files while preserving a concise success, failure, and skipped-file summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because the converter includes under-disclosed credential and network behavior.

Mitigation: Review the code before installation, remove the OPENAI_API_KEY fallback if it is not needed, and provide only a converter-specific API key when token verification is required.

Risk: Feishu push behavior can send conversion notifications or results outside the local environment.

Mitigation: Keep Feishu disabled for sensitive documents unless the webhook destination and transmitted content are approved.

Risk: Cleanup commands included in the artifact can remove local files if copied into the wrong directory.

Mitigation: Review cleanup commands before use and run them only in the intended release or disposable working directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qiji0802/skills/batch-format-converter)
- [Publisher Profile](https://clawhub.ai/user/qiji0802)
- [YK-Global](https://yk-global.com)
- [Tesseract OCR Windows Installer Reference](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [files, text, shell commands, configuration, guidance]

**Output Format:** [Converted files plus JSON-style conversion summaries, CLI output, and Markdown guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports batch conversion, tier-aware quota checks, optional OCR dependencies, and optional Feishu notification output.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
