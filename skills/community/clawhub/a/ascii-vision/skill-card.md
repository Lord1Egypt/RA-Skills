## Description:

Fallback image viewer when vision models are unavailable. Converts images to ASCII art via ffmpeg and Python for brightness distribution, texture analysis, edge detection, and color sampling without a vision API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chdlc](https://clawhub.ai/user/chdlc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect image structure when direct vision analysis is unavailable, especially for checking whether generated images contain content, comparing variants, and sampling coarse brightness, edge, and color signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local ffmpeg and Python commands against user-selected image files.

Mitigation: Install only where local command execution on chosen images is acceptable, and review generated commands before running them.

Risk: ASCII, edge, brightness, and coarse color outputs can be mistaken for reliable object, text, face, or semantic recognition.

Mitigation: Use the output as rough structural diagnostics and prefer a real vision model when accurate visual understanding is required.

## Reference(s):

- [ASCII Vision skill page](https://clawhub.ai/chdlc/skills/ascii-vision)
- [Publisher profile](https://clawhub.ai/user/chdlc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown with inline bash commands and ASCII text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local ffmpeg and python3; output is a coarse structural diagnostic, not semantic image recognition.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact frontmatter and _meta.json report 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
