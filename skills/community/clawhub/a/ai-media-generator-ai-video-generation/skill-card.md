## Description:

Use when someone asks for AI video generation, video generator, text-to-video, image-to-video, prompt-to-video, video model selection, or CLI-based video workflows on ricebowl.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinchanzis](https://clawhub.ai/user/jinchanzis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI media operators use this skill to configure the ai-media CLI, select ricebowl.ai video models, and generate or retrieve text-to-video or image-to-video jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on a mutable third-party npm CLI.

Mitigation: Review or pin the ai-media-generator package before installation, and rescan before deployment.

Risk: The workflow uses a paid-service API key for ricebowl.ai media generation.

Mitigation: Use a scoped API key where possible, avoid exposing unrelated environment variables or files to the CLI process, and confirm where the key is stored so it can be rotated or removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinchanzis/skills/ai-media-generator-ai-video-generation)
- [Publisher profile](https://clawhub.ai/user/jinchanzis)
- [ai-media-generator homepage](https://github.com/214140846/ai-media-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands for API key setup, model inspection, video generation, polling, and task retrieval.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
