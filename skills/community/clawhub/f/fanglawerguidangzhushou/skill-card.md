## Description: <br>
Helps legal professionals organize civil case folders by extracting case details from images or PDFs, generating archive dossiers and case summaries, and converting outputs to PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fong12368](https://clawhub.ai/user/fong12368) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal professionals and their agents use this skill to turn a case folder of images or PDFs into civil archive documents, case summaries, PDF copies, and OCR text for local recordkeeping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The automatic Word-to-PDF step runs a PowerShell command built from file paths. <br>
Mitigation: Use only trusted case folders with simple, controlled path names, and fix or disable the conversion step before routine use. <br>
Risk: Generated OCR text and archive documents may contain confidential case information. <br>
Mitigation: Protect, retain, or delete generated OCR text and archive outputs according to applicable confidentiality obligations. <br>
Risk: Configuration placeholders include email and WeChat credential fields that could expose secrets if populated carelessly. <br>
Mitigation: Avoid adding real credentials to configuration files unless the related code path has been reviewed and secrets are stored appropriately. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [DOCX/PDF documents, OCR text files, and Markdown guidance with shell and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local files in the case folder; Word-to-PDF conversion depends on Windows, Microsoft Word COM, and configured local paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
