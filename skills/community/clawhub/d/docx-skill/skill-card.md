## Description:

Create, read, edit, and manipulate Word documents (.docx), including text, tables, images, headers, footers, styles, and tracked changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weaglewang](https://clawhub.ai/user/weaglewang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document automation users use this skill to generate, inspect, convert, and modify Microsoft Word .docx files. It is useful for building reports, invoices, resumes, templates, and other structured documents with paragraphs, tables, images, headers, footers, styles, and tracked changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation steps can change the user's local development environment.

Mitigation: Prefer project-local npm dependencies, a Python virtual environment, and pinned versions where practical.

Risk: Optional converters and image tools add local execution and processing surface.

Mitigation: Install optional converters or image tools only when the related document conversion or image feature is needed.

Risk: Generated examples may read, create, overwrite, or transform local document files.

Mitigation: Review paths and run examples on copies or test files before applying them to important documents.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript, Python, XML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide users to create or modify local .docx files when they run generated code or commands.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
