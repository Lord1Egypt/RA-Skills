## Description:

A document-to-HTML image naming skill that renames generic exported image files using document context and visual content, then updates HTML references and filename mappings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinglan803-coder](https://clawhub.ai/user/tinglan803-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content engineers use this skill when converting doc, docx, pdf, or similar documents to HTML and need generic exported image names replaced with useful semantic filenames. It guides agents to inspect nearby document context and image content, rename image assets, update HTML src references, and preserve a source-to-final mapping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Semantic filenames may be inaccurate when document context is vague or image interpretation is uncertain.

Mitigation: Review the generated source-to-final mapping and spot-check updated HTML references before relying on the renamed assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tinglan803-coder/skills/document-html-image-semantic-naming)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with file edits, updated HTML references, and a source-to-final filename mapping]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify user-provided HTML and image asset filenames; review generated mappings because semantic names depend on context and visual interpretation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
