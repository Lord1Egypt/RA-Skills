## Description:

PPTX helps agents create, edit, analyze, validate, and convert PowerPoint presentations using HTML-to-PowerPoint and Office Open XML workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, presentation authors, and external users use this skill to create new PowerPoint decks, modify template-based presentations, inspect existing PPTX content, edit OOXML directly, validate presentation structure, replace slide text, and generate thumbnails for visual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local document-conversion and presentation-editing tools against Office files.

Mitigation: Use it only with trusted PPTX files or inside a sandboxed workspace where local file access and document conversion are acceptable.

Risk: Some workflows may require system or global dependency installation.

Mitigation: Review install commands before running them, avoid elevated privileges unless necessary, and prefer isolated environments for dependencies.

Risk: Template text replacement can clear slide text when replacement entries are missing.

Mitigation: Keep backups of source presentations, review inventory and replacement JSON before applying changes, and validate thumbnails after modification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/exceltable-in-ppt-pptx)
- [Artifact skill definition](artifact/SKILL.md)
- [HTML to PowerPoint Guide](artifact/html2pptx.md)
- [Office Open XML Technical Reference for PowerPoint](artifact/ooxml.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, JSON inventories, HTML or JavaScript slide definitions, and generated or modified PowerPoint-related files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify PPTX files, unpacked OOXML directories, thumbnail images, replacement JSON, inventory JSON, and conversion scripts; workflows may call local Python, Node.js, LibreOffice, and presentation-processing dependencies.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
