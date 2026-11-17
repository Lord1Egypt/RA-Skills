## Description:

Reads an attached Markdown document, summarizes it, and generates one minimalist handwritten whiteboard-style image in a requested aspect ratio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Markdown documents into concise summaries and simple whiteboard-style visuals for social banners, hero images, or tutorial-style communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-provided Markdown and sends summarized content into image generation.

Mitigation: Use non-sensitive documents unless that processing is acceptable for the user's data handling requirements.

Risk: The generated image is saved locally in a Hermes cache path.

Mitigation: Review local retention expectations and remove cached output when it should not persist.

Risk: The skill only supports Markdown inputs and can halt on missing or unreadable documents.

Mitigation: Confirm the attached source file is valid Markdown before invoking the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/260611-md2mini-img)
- [Publisher profile](https://clawhub.ai/user/j3ffyang)
- [Author profile](https://github.com/j3ffyang)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, files]

**Output Format:** [Markdown summary plus generated image file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces exactly one image and reports the resolved aspect ratio and color scheme.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
