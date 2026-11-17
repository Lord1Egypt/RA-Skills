## Description:

Render Excalidraw (.excalidraw) files to PNG images and take screenshots of web pages using headless Chrome via the brow CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zypher-agent](https://clawhub.ai/user/zypher-agent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to render Excalidraw diagrams into PNG files and capture web page screenshots through the brow CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer runs an unverified remote shell script with the user's privileges.

Mitigation: Review the skill before installing and install brow only through a trusted, pinned, and verifiable source.

Risk: The screenshot capability can access URLs supplied during use.

Mitigation: Use screenshot capture only for trusted external URLs and avoid internal services or sensitive local addresses.

## Reference(s):

- [brow CLI](https://github.com/corespeed-io/brow)
- [Corespeed](https://corespeed.io)
- [Corespeed skills support](https://github.com/corespeed-io/skills/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and saved file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PNG image files through the brow CLI; the skill instructs agents to report saved paths rather than read generated images back.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
