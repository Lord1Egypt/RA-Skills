## Description:

Guides Windows users through batch conversion of Word documents to PDF using LibreOffice and PowerShell without Microsoft Word.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zd200572](https://clawhub.ai/user/zd200572)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Windows users use this skill to batch-convert .doc and .docx files to PDF with LibreOffice from PowerShell, without installing Microsoft Word.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converting in the wrong directory or overwriting existing PDFs may cause unintended changes.

Mitigation: Run commands only from the intended directory and back up existing PDFs that matter.

Risk: Force-stopping LibreOffice during troubleshooting may interrupt open work.

Mitigation: Use the process-stopping command only after confirming no important LibreOffice work is open.

Risk: Complex Word document layouts may shift during conversion.

Mitigation: Spot-check important PDFs, especially documents with tracked changes or embedded objects.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zd200572/skills/docx2pdf)
- [LibreOffice download](https://www.libreoffice.org/download/)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers output directories and conversion troubleshooting.]

## Skill Version(s):

1.0.0 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
