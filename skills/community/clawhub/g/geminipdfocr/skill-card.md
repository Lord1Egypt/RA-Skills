## Description:

Extract text from PDFs using Google Gemini OCR. Use when extracting text from PDFs, performing OCR on scanned documents, or processing image-based PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashtonizmev](https://clawhub.ai/user/ashtonizmev)

### License/Terms of Use:


## Use Case:

Developers and document-processing users can use this skill to extract plain text or structured JSON from scanned or image-based PDF documents with Google Gemini OCR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF page content is sent to Google Gemini for OCR.

Mitigation: Confirm this processing is acceptable before use and avoid highly sensitive documents unless external processing is approved.

Risk: Unpinned dependencies can change between installations.

Mitigation: Use an isolated virtual environment and pin or lock dependency versions before production deployment.

Risk: The --output option writes OCR results to the path supplied by the user.

Mitigation: Review output paths before execution and use workspace locations appropriate for the document sensitivity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ashtonizmev/skills/geminipdfocr)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [Plain text or JSON OCR results from a CLI workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports one or more PDF paths, optional page limits, quiet mode, and writing output to a user-provided file path.]

## Skill Version(s):

0.1.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
