## Description:

Opens a local browser-based Markdown editor and previewer for explicitly requested Markdown files, with theme switching, rich-text copy, image paste, and live preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webkixi](https://clawhub.ai/user/webkixi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and agents use this skill to open a local Markdown preview/editor for .md files, inspect rendered output, switch styles, copy themed rich text, and optionally paste images into the Markdown file's images folder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local editor can autosave over the original Markdown file.

Mitigation: Open only intended files and keep a backup or version-control checkpoint before editing.

Risk: Unauthenticated localhost APIs can save Markdown content and write pasted images to disk.

Mitigation: Run the preview server only in trusted local sessions, keep it bound to 127.0.0.1, and stop it when previewing is complete.

Risk: Rendered Markdown can include active HTML.

Mitigation: Avoid opening untrusted Markdown until authentication, origin checks, and HTML sanitization are reviewed.

## Reference(s):

- [Claw Markdown Preview on ClawHub](https://clawhub.ai/webkixi/skills/claw-markdown-preview)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-facing guidance with shell commands and a local browser preview UI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts a localhost preview server that reads the selected Markdown file and can save edits or pasted images back to local disk.]

## Skill Version(s):

1.4.15 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
