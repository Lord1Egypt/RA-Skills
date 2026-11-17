## Description:

Answers questions based on the content of uploaded documents (PDF, DOCX, TXT), supporting individual files or entire folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anand2426](https://clawhub.ai/user/anand2426)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers can use this skill to extract local document content and ask factual questions about one file or a folder of supported files. It is best suited for document-grounded summarization, retrieval, and content review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the specific local document or top-level folder path provided by the user.

Mitigation: Provide only files or folders intended for analysis, especially when working with sensitive documents.

Risk: Untrusted document text may contain prompt-injection attempts or misleading content that affects generated answers.

Mitigation: Treat answers as document-grounded assistance and verify important claims against the source documents.

Risk: PDF, DOCX, and XLSX handling depends on separate reader skills or Python libraries.

Mitigation: Use reviewed, pinned dependencies and a trusted PDF-reader skill before relying on the workflow for sensitive files.

## Reference(s):

- [Usage Guide for Document Q&A Skill](references/usage_guide.md)
- [ClawHub skill page](https://clawhub.ai/anand2426/skills/document-qa)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text document context and question prompts; answers are typically returned as text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-provided document paths or folders and emits extracted content for the agent to answer against.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
