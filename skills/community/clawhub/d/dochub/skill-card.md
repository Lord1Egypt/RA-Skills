## Description:

Dochub helps an agent turn .docx and .xlsx source documents into a structured Markdown knowledge base using a raw -> wiki -> schema workflow for initialization, updates, search/Q&A, and health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longjf25](https://clawhub.ai/user/longjf25)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and document owners use this skill to organize local Office documents into a source-traceable Markdown wiki, then answer questions, add updates, and run health checks against that knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move many local documents into a managed raw folder during initialization or update.

Mitigation: Run it only on a dedicated document folder, review the file move list before proceeding, and avoid broad home, project, Documents, or synced folders.

Risk: The skill may install and run Python dependencies for document conversion.

Mitigation: Provision trusted, pinned dependencies such as python-docx and openpyxl yourself, and review any generated conversion script before execution.

Risk: The artifact discusses sandbox bypass for Windows file moves.

Mitigation: Avoid disabling the sandbox; if elevated access is unavoidable, limit the scope to the dedicated knowledge-base folder and inspect planned file operations first.

Risk: The knowledge base may contain sensitive or confidential document content.

Mitigation: Use the documented safety confirmation step and only proceed after the source documents have been reviewed for sensitive personal or confidential data.

## Reference(s):

- [Dochub skill release](https://clawhub.ai/longjf25/skills/dochub)
- [Dochub entity types](references/entity-types.md)
- [Karpathy LLM Wiki methodology reference](references/karpathy-methodology.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown knowledge-base files, cited Markdown answers, lint reports, and occasional shell or Python setup commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operates on a user-selected document knowledge-base directory and may generate or update raw, wiki, update, and schema files.]

## Skill Version(s):

1.5.0 (source: server release metadata, created 2026-06-05T07:30:49Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
