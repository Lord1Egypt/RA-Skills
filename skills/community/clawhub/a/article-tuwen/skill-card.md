## Description:

Article Tuwen converts provided URLs, files, or text into a long-form article, 5-9 social card images, and a text summary, with web-search enrichment, local file creation, and opt-in Feishu sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and operators use this skill to turn supplied source material into a ready-to-share social-card package. It is intended for conversion workflows where the user explicitly asks to transform material into Chinese graphic-text content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic web fetches and web searches may process sensitive source material or reveal topics externally.

Mitigation: Use the skill only with material appropriate for web-assisted processing, and avoid confidential content unless the user has reviewed the workflow.

Risk: The skill creates local Desktop output files from user-provided material.

Mitigation: Confirm the intended output folder and remove generated files that should not remain on the local machine.

Risk: Optional Feishu cloud sync can upload generated PNG and text outputs.

Mitigation: Approve Feishu sync only after checking the exact filenames and using a safe simple slug; do not upload confidential source-derived content unless the upload manifest is explicit.

Risk: The skill orchestrates sub-skills for article writing and card rendering.

Mitigation: Review the installed transcript-crafter and xhs-crafter skill declarations before use in sensitive workflows.

## Reference(s):

- [Article Tuwen pipeline](artifact/references/pipeline.md)
- [Article Tuwen ClawHub page](https://clawhub.ai/edwardwason/skills/article-tuwen)
- [lark-cli](https://github.com/larksuite/lark-cli)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [Markdown article, PNG image files, plain-text summary, and optional Feishu upload guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a Desktop output folder with 5-9 1080x1440 PNG cards, an article markdown file, a text summary, and an image-source log.]

## Skill Version(s):

1.1.2 (source: frontmatter, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
