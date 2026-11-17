## Description:

Helps agents provide guidance and Python code for filling Word .docx templates with text placeholders, smart table markers, images, and batch document data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huagc](https://clawhub.ai/user/huagc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document automation users use this skill to generate code and implementation guidance for filling .docx templates, including ordinary placeholders, declared table regions, multiline text, images, and batch report or contract generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processing untrusted .docx templates may require additional hardening before use.

Mitigation: Use trusted .docx templates and harden validation before processing untrusted templates.

Risk: Large table row or column declarations can create oversized generated documents.

Mitigation: Keep table r/c values modest and validate requested row and column counts before generation.

Risk: Saving generated output over the original template can overwrite source documents.

Mitigation: Save generated documents to a new output path rather than the original template path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huagc/skills/fill-docx-template)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include python-docx helper code and instructions for writing generated documents to a separate output path.]

## Skill Version(s):

1.1.3 (source: server release metadata and user changelog, released 2026-06-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
