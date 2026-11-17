## Description:

This OpenClaw skill extracts text from local txt, docx, pdf, xlsx, and xls files and generates summaries or analysis in Chinese or English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonthepro2012](https://clawhub.ai/user/leonthepro2012)

### License/Terms of Use:


## Use Case:

External OpenClaw users use this skill to summarize or analyze local documents after explicitly providing a file path. It is intended for document review workflows involving supported text, Word, PDF, and Excel formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local document contents and sends extracted content to OpenClaw LLM for summarization or analysis.

Mitigation: Use only with files approved for that processing path; avoid sensitive or confidential documents unless the environment and data handling are approved.

Risk: The skill may automatically install unpinned Python packages at runtime when document parsing dependencies are missing.

Mitigation: Run in a sandbox or preinstall reviewed, pinned dependencies so the auto-install path does not run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leonthepro2012/skills/file-summary-zongjie)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text or Markdown prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a user-provided local file path and returns extracted document text, a concise summary, or analysis.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
