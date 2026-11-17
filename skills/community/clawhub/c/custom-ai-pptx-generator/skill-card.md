## Description:

AI PPT Designer creates custom, content-driven, fully editable PowerPoint presentations from notes, documents, emails, spreadsheets, images, or other source material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenzje228](https://clawhub.ai/user/kenzje228)

### License/Terms of Use:

MIT

## Use Case:

Employees, external users, and presentation-heavy teams use this skill to turn source material into reviewed, content-driven PPTX decks with native editable PowerPoint objects. It is suited for training decks, project briefings, policy explainers, business updates, and other presentations where users need approval checkpoints before final production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation source material may be routed to optional external image-generation services without an explicit privacy or consent checkpoint.

Mitigation: Confirm the image provider before use, avoid confidential or regulated content unless the provider is approved, and prefer a local or organization-approved workflow.

Risk: Prompts or project files may accidentally include secrets or sensitive internal business details.

Mitigation: Remove secrets and sensitive details from prompts, source files, and generated assets before invoking image-generation or automation steps.

Risk: The cutout helper can be used to alter image assets, including watermark removal.

Mitigation: Use the helper only on assets the user owns or is authorized to modify.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kenzje228/skills/custom-ai-pptx-generator)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Project Experience Summary](artifact/references/千题千境_项目经验总结.md)
- [Six-Page Prompt Package](artifact/references/prompts/千题千境_6页提示词.md)
- [Single-Block Prompt Template](artifact/references/prompts/千题千境_单block提示词.txt)
- [SSC Automation Prompt Template](artifact/references/prompts/SSC自动化_单block提示词.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and generated PowerPoint files or supporting render assets when executed in a suitable environment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow may produce editable PPTX files, rendered slide images, prompt text for external image generation, and concise delivery notes.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
