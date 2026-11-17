## Description:

Helps agents process Chinese academic papers by converting Word documents to Markdown, extracting references, inserting citation markers, expanding manuscript text, and converting processed drafts back to Word.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codhealer](https://clawhub.ai/user/codhealer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and academic-writing assistants use this skill to automate citation formatting, reference extraction, manuscript expansion, and Word/Markdown document conversion for Chinese theses and papers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may rewrite thesis files at hardcoded local paths.

Mitigation: Review scripts before installation, replace hardcoded paths with explicit user-selected paths, and add backups or dry-run diffs before write operations.

Risk: Document conversion may run generated code while producing DOCX output.

Mitigation: Fix the Markdown-to-DOCX converter so document text is serialized as data rather than executable JavaScript before using it on untrusted content.

Risk: Unpinned npm dependencies can change behavior between installs.

Mitigation: Pin npm dependencies and review dependency changes before deployment.

## Reference(s):

- [Implementation Details](references/implementation.md)
- [ClawHub Skill Page](https://clawhub.ai/codhealer/skills/academic-paper-citation)
- [ClawHub Publisher Profile](https://clawhub.ai/user/codhealer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command-line examples and generated document files such as Markdown, JSON, and DOCX]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or rewrite local manuscript, reference, report, JavaScript, and Word document files when scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
