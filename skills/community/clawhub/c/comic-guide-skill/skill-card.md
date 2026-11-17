## Description:

Generate AI-illustrated comic-style educational guides from documentation, source code, or technical topics, including storyboards, character definitions, image prompts, and comic PNG outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongzhe4](https://clawhub.ai/user/hongzhe4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and technical writers use this skill to turn documentation, source code, or technical concepts into comic-style visual explainers. It supports multi-chapter workflows that produce analysis notes, storyboards, character definitions, image prompts, and generated comic images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended installer can run mutable remote code and persist files into multiple agent skill directories.

Mitigation: Install through ClawHub or use a reviewed, pinned manual copy path; avoid curl-piped shell installation and unattended agent installation.

Risk: Generated prompts may expose proprietary code, private documents, secrets, or licensed character/style requests to external image-generation services.

Mitigation: Review source material and generated prompts before submission to image-generation services, and remove sensitive or rights-restricted content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hongzhe4/skills/comic-guide-skill)
- [Style Prompt Templates](artifact/references/styles.md)
- [Image Prompt Writing Guide](artifact/references/prompt-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, PNG images, Guidance]

**Output Format:** [Markdown files, image-generation prompts, and PNG comic images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports storyboard-only and prompts-only modes; style, language, chapter count, aspect ratio, and output directory are configurable.]

## Skill Version(s):

1.0.0 (source: evidence release version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
