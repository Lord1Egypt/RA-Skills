## Description:

Guides agents through image-to-image generation workflows using ricebowl.ai and the ai-media CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinchanzis](https://clawhub.ai/user/jinchanzis)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent prepare and run CLI-based image-to-image generation with a reference image, prompt, selected model, and task retrieval on ricebowl.ai.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on a mutable npm CLI package.

Mitigation: Install only after trusting the ai-media-generator package and review the installed CLI version before use.

Risk: The workflow requires an API key for image generation.

Mitigation: Set AI_MEDIA_API_KEY through a secret manager or protected environment variable and avoid placing real keys in shell history.

Risk: The workflow may use ricebowl.ai credits for generation requests.

Mitigation: Confirm account, credit, and provider terms before running generation commands.

## Reference(s):

- [ai-media-generator homepage](https://github.com/214140846/ai-media-generator)
- [ClawHub skill page](https://clawhub.ai/jinchanzis/skills/ai-media-generator-image-to-image)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the ai-media CLI and the AI_MEDIA_API_KEY and AI_MEDIA_BASE_URL environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
