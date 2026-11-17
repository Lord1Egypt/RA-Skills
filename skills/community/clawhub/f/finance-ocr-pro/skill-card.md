## Description:

Finance OCR Pro helps agents OCR, transcribe, extract, or convert scanned PDFs, images, and office documents into Markdown, HTML, DOCX, and Excel using a configured OpenAI-compatible vision-language model endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rizmoon](https://clawhub.ai/user/rizmoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn scanned or visually complex financial documents, office files, and images into reviewable Markdown, HTML, DOCX, and Excel outputs. It is intended for workflows where page layout, tables, charts, formulas, and long-running OCR jobs matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document page images and OCR prompts are sent to the configured VLM endpoint.

Mitigation: Use the skill only with a trusted BASE_URL, and point BASE_URL to a trusted local service when documents require local-only processing.

Risk: Generated HTML reports may carry unsafe active content from OCR Markdown or Mermaid output.

Mitigation: Avoid opening or sharing generated HTML reports from untrusted documents until report sanitization has been reviewed.

Risk: API credentials are required for the VLM endpoint.

Mitigation: Keep API_KEY local, do not commit populated .env files, and use .env.example only as a template.

Risk: Long-running OCR jobs may leave sensitive results on disk.

Mitigation: Monitor background jobs and remove ~/.semantic-ocr/jobs artifacts when results are no longer needed.

## Reference(s):

- [Finance OCR Pro README](artifact/README.md)
- [Security Notes](artifact/SECURITY.md)
- [Third-Party Notices](artifact/THIRD_PARTY_NOTICES.md)
- [ClawHub Skill Page](https://clawhub.ai/rizmoon/skills/finance-ocr-pro)
- [Publisher Profile](https://clawhub.ai/user/rizmoon)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and generated Markdown, HTML, DOCX, and Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires API_KEY, BASE_URL, and VLM_MODEL; default OCR jobs write results under ~/.semantic-ocr/jobs/<job_id>/results/.]

## Skill Version(s):

1.0.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
