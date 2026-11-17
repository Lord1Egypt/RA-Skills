## Description:

Design Ads generates vertical AI knowledge posters and cover images as 1200x1800 PNGs from user-provided topics, content, and template choices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bozoyan](https://clawhub.ai/user/bozoyan)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, educators, and knowledge workers use this skill to turn topic outlines or educational content into mobile-friendly poster and cover images for social, newsletter, and learning materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the renderer runs active HTML in an unsandboxed browser.

Mitigation: Review generated or user-supplied HTML before rendering and run the skill in a low-privilege, isolated environment with Chromium sandboxing enabled where possible.

Risk: The security guidance notes dependency and file-copying risks.

Mitigation: Pin and review dependencies, block unexpected network requests, and avoid sensitive data in poster HTML because source HTML and PNG outputs may be copied to a downloads folder.

## Reference(s):

- [Design Ads design system](references/design-system.md)
- [ClawHub skill page](https://clawhub.ai/bozoyan/skills/design-ads)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with HTML/CSS source and rendered PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates 1200x1800 PNG posters; longer content may be split into multiple numbered images.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
