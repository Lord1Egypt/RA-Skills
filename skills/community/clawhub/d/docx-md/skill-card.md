## Description:

docx-md helps agents read DOCX files as compact Markdown or JSON, apply structured edit JSON back into DOCX tracked revisions and comments, and finalize DOCX files by accepting revisions and removing comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanweiliang323868-del](https://clawhub.ai/user/yanweiliang323868-del)

### License/Terms of Use:

GPL-3.0-or-later

## Use Case:

Developers and document-review agents use this skill to convert DOCX content into model-friendly Markdown or JSON, apply reviewed edit JSON back to Word documents with tracked changes and comments, and produce final DOCX files after review approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DOCX files may contain sensitive contract or business content that could be exposed if sent to an unapproved external LLM.

Mitigation: Use approved model providers for confidential data and keep document processing in an approved environment.

Risk: Applying generated edits can introduce incorrect changes into a Word document.

Mitigation: Run the scripts on document copies and review tracked revisions and comments before accepting changes.

Risk: Finalization removes tracked revisions and comments from the output file.

Mitigation: Run finalization only after explicit review approval and retain the reviewed source copy.

Risk: Unpinned Python dependencies can change behavior across installations.

Mitigation: Install in an isolated Python environment and pin dependency versions where possible.

## Reference(s):

- [LLM-Oriented DOCX Pipeline](references/llm-pipeline.md)
- [OOXML Reference for DOCX](references/ooxml.md)
- [ClawHub skill page](https://clawhub.ai/yanweiliang323868-del/skills/docx-md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON for document reads, JSON edit instructions for modifications, and DOCX output files for reviewed or finalized documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill works on local DOCX copies; finalization removes tracked revisions and comments from the output file.]

## Skill Version(s):

1.0.1 (source: server release evidence, LICENSE.txt)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
