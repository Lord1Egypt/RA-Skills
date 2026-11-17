## Description:

Extract text from PDF, DOCX, and TXT with encoding detection and page/paragraph structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, RAG builders, researchers, and data engineers use this skill to extract readable text from individual documents or batches of supported files for search, retrieval, and analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions may lead users to download and execute mutable remote Python code.

Mitigation: Run the reviewed bundled doc_extractor.py from the package, or require a pinned commit with checksum or signature verification.

Risk: Batch extraction can process more local files than intended if pointed at a broad directory.

Mitigation: Limit batch extraction to directories intentionally selected for the task.

Risk: PDF extraction depends on PyMuPDF when PDF support is needed.

Mitigation: Pin and review the PyMuPDF dependency in the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itspremkumar/skills/doc-extractor)
- [Publisher profile](https://clawhub.ai/user/itspremkumar)
- [GitHub repository](https://github.com/itsPremkumar/doc-extractor)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Guidance]

**Output Format:** [Plain text output and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print extracted text to the terminal or write extracted content to .txt files; PDF support requires PyMuPDF.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
