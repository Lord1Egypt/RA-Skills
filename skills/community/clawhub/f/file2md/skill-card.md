## Description:

File2md helps agents convert local documents and media, including PDF, DOCX, XLSX, PPTX, HTML, CSV, images, audio, and video, into Markdown using the @covoyage/file2md CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luduoxin](https://clawhub.ai/user/luduoxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users can use this skill when they need an agent to convert local office documents, PDFs, spreadsheets, presentations, HTML, CSV, notebooks, archives, email, or media into readable Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an unpinned third-party npm CLI.

Mitigation: Use a pinned or internally vetted @covoyage/file2md package version before processing sensitive or production documents.

Risk: Optional Azure cloud conversion flags can send document content to external services.

Mitigation: Avoid cloud conversion flags unless the user explicitly intends to use those services and has approval to send the document content.

## Reference(s):

- [File2md ClawHub skill page](https://clawhub.ai/luduoxin/skills/file2md)
- [@covoyage/file2md npm package](https://www.npmjs.com/package/@covoyage/file2md)
- [@covoyage/file2md project repository](https://github.com/covoyage/file2md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write Markdown to a file when the CLI is invoked with an output path; requires Node.js 18+.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
