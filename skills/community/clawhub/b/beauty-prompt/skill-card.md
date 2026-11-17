## Description:

Guides Chinese-speaking users from interior-design or commercial-display needs to confirmed bilingual image prompts, generated image files, and optional handoff for video creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[865116251](https://clawhub.ai/user/865116251)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn home decor, interior design, space planning, or commercial display requests into structured questions, bilingual image-generation prompts, generated images, and an optional video-generation handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags under-disclosed external sharing through Feishu delivery and optional forwarding to another agent.

Mitigation: Use only where external sharing is acceptable, avoid sensitive floor plans, addresses, proprietary layouts, and private business details, and revise the workflow to ask before any external transmission.

Risk: The security assessment flags unsafe shell-based image generation when prompts are passed through a command line.

Mitigation: Pass prompts to the image generator without shell interpolation and review generated commands before execution.

Risk: The artifact workflow performs web searches for design trends, materials, and terminology.

Mitigation: Review retrieved sources and avoid entering private or proprietary details into web queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/865116251/skills/beauty-prompt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Conversational Markdown with structured options, bilingual prompt text, image file paths, and shell command invocations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create image files under the workspace output directory and optionally send the image path to another agent after user confirmation.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
