## Description:

Use when someone asks for ai image generation, image generator, text-to-image, image-to-image, prompt-to-image, image model selection, or CLI-based image workflows on ricebowl.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinchanzis](https://clawhub.ai/user/jinchanzis)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to select image models, configure ai-media credentials, and run ricebowl.ai text-to-image or image-to-image workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external ai-media CLI package that is not pinned in the release evidence.

Mitigation: Install a pinned, reviewed ai-media-generator version and review package updates before use.

Risk: API-key setup guidance may lead users to paste sensitive credentials into shell history or logs.

Mitigation: Use a hidden interactive prompt or protected secret storage where available, and rotate any key already exposed in shell history.

Risk: The API key may control paid credits or sensitive account access.

Mitigation: Use a scoped key when possible, monitor usage, and review the skill before installing in shared or production agent environments.

## Reference(s):

- [ai-media-generator homepage](https://github.com/214140846/ai-media-generator)
- [ClawHub skill page](https://clawhub.ai/jinchanzis/skills/ai-media-generator-ai-image-generation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ai-media CLI commands, model-selection guidance, API-key setup steps, and task retrieval instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
