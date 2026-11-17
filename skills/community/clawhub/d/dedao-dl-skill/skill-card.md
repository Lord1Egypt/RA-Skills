## Description:

Handles interactions with the dedao-dl CLI tool for downloading and managing content from the Dedao (得到) App, including purchased courses, ebooks, audiobooks, and selected export formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angjustinl](https://clawhub.ai/user/angjustinl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide authenticated dedao-dl CLI workflows for listing and downloading their Dedao courses, ebooks, audiobooks, and related notes in selected formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an unverified third-party native downloader with local user privileges.

Mitigation: Review the skill before installation and verify or pin the downloaded dedao-dl binary before use.

Risk: Dedao cookies may expose account access if pasted into login commands.

Mitigation: Prefer QR login, and provide cookies only when the user understands they are account secrets.

Risk: Full-course downloads can take a long time, consume substantial disk space, and may trigger anti-bot controls.

Mitigation: Require explicit user permission before full-course downloads and favor single-article downloads when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/angjustinl/skills/dedao-dl-skill)
- [dedao-dl release lookup endpoint](https://api.github.com/repos/yann0917/dedao-dl/releases/latest)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown guidance with inline shell commands and cleaned CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides CLI installation, login, listing, and download commands; resulting downloads may be Markdown, PDF, EPUB, MP3, HTML, or notes depending on the selected dedao-dl format.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
