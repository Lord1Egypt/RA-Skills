## Description:

OCR documents (PDFs and images) using Gemini 2.5 Flash, PaddleOCR (local), or RapidOCR (local).

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottkiss](https://clawhub.ai/user/scottkiss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to extract text from scanned PDFs and images with local OCR engines or Gemini-based cloud OCR. It supports single-document and batch workflows with optional output files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags installation through mutable remote code and an unauthenticated native binary that was not included for review.

Mitigation: Build from reviewed source or use a release with published checksums or signatures; avoid curl-piped shell installation and do not run the installer with elevated privileges.

Risk: Gemini mode may send selected documents to a cloud OCR service, and the documented configuration stores the API key in plaintext.

Mitigation: Use local OCR engines for sensitive documents unless cloud processing is approved; protect, scope, and rotate the Gemini API key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scottkiss/skills/doc-ocr-skills)
- [Publisher profile](https://clawhub.ai/user/scottkiss)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Plain text OCR output and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can process individual files or batches; Gemini mode uses a configured API key and may send selected documents to a cloud OCR service.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
