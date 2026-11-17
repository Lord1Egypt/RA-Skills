## Description:

Local document reading skill that extracts plain text and lightweight structure from PDF, DOCX, TXT, and Markdown files for downstream summarization, retrieval, and structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-work agents use this skill to preprocess authorized local documents into text or JSON before summarization, search indexing, translation, or structured extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processing sensitive or unauthorized documents can expose private content during extraction or downstream workflows.

Mitigation: Use the extractor only with documents you are authorized to process, and avoid forwarding extracted content unless it has been reviewed or redacted.

Risk: The learner logger can persist notes and preferences outside the core document-reading task.

Mitigation: Disable or remove learner.py unless persistent local learning records are required, and do not store document content or private details in learner notes.

Risk: Optional PDF and DOCX dependencies affect extraction behavior and supply-chain exposure.

Mitigation: Install pypdf, PyPDF2, and python-docx in an isolated environment with pinned versions where possible.

## Reference(s):

- [ClawHub skill page: doc-reader](https://clawhub.ai/qq435912743/skills/doc-reader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, structured JSON, Markdown guidance, and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write extracted content to local output files; PDF and DOCX support depend on optional local Python libraries.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
