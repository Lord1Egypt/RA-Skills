## Description:

Doc OCR helps agents extract searchable, editable text from scanned pages or image-embedded content in Word .docx files using MinerU OCR and VLM modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, office teams, legal teams, and archivists use this skill to OCR scanned or image-only content inside Word .docx files and convert it into readable, searchable Markdown or text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends or enables processing of potentially sensitive Word documents through the third-party MinerU tool.

Mitigation: Review MinerU data handling terms before use and avoid processing confidential legal, business, medical, or personal files unless approved.

Risk: The install guidance uses mutable global package installs for mineru-open-api.

Mitigation: Use a pinned, reviewed mineru-open-api version in an isolated environment before deploying the skill.

Risk: OCR results can vary when language settings are left implicit.

Mitigation: Set the language flag explicitly for the document language, such as en for English.

## Reference(s):

- [Doc OCR ClawHub Page](https://clawhub.ai/mzlzyca/skills/doc-ocr)
- [mzlzyca Publisher Profile](https://clawhub.ai/user/mzlzyca)
- [MinerU Homepage](https://mineru.net)
- [MinerU Token Management](https://mineru.net/apiManage/token)
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and OCR output as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mineru-open-api and MINERU_TOKEN; document content can be written to stdout or an output directory.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
