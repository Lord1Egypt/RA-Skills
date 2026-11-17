## Description:

Remove visible Gemini AI watermarks from images via reverse alpha blending.

This skill is for research and development only.

## Publisher:

[fzlra](https://clawhub.ai/user/fzlra)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to run local Python commands that remove the visible bottom-right Gemini watermark from images they are allowed to edit. The artifact states that it is for personal learning and research only and prohibits commercial use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to remove visible AI watermarking, which can create content-authenticity, licensing, service-terms, or disclosure concerns.

Mitigation: Use only on images the user is allowed to edit, preserve AI-origin disclosure through other means, and review applicable service terms before publication.

Risk: The skill installs and runs Python image-processing dependencies locally.

Mitigation: Install dependencies in a pinned or isolated environment before processing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fzlra/skills/gemini-watermark-remover)
- [Artifact README](artifact/README.md)
- [Artifact Chinese README](artifact/README_zh.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local command guidance and an edited image file when the generated commands are run.]

## Skill Version(s):

1.1.2 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
