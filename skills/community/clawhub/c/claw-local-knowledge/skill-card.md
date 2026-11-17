## Description:

Local knowledge-base skill for adding documents to a workspace knowledge base and retrieving relevant stored knowledge for agent responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[overdue-lin](https://clawhub.ai/user/overdue-lin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and external users use this skill to ingest uploaded docx, pdf, xlsx, and pptx files into a local Markdown knowledge base, maintain a JSON index, and retrieve relevant stored documents to support task responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A workspace-local knowledge base can influence future agent answers, including content from documents that may not be trustworthy.

Mitigation: Ingest only trusted documents, review retrieved content before relying on it, and treat stored knowledge as contextual evidence rather than authoritative instructions.

Risk: The skill recommends modifying SOUL.md to enable persistent proactive retrieval behavior.

Mitigation: Apply the SOUL.md configuration only when that persistent behavior is intended, and review the resulting instructions before use.

Risk: The ingestion workflow deletes source uploads after successful conversion and index update.

Mitigation: Confirm the converted Markdown and index entry are correct, and retain separate backups when original uploads must be preserved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/overdue-lin/skills/claw-local-knowledge)
- [README](artifact/README.md)
- [Add knowledge workflow](artifact/references/add_knowledge.md)
- [Knowledge retrieval workflow](artifact/references/retrieval_knowledge.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Markdown knowledge files and a JSON knowledge-base index.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
