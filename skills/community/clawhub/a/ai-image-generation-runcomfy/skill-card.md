## Description:

Routes image-generation and image-editing requests through the RunComfy CLI across supported text-to-image and image-to-image models, selecting model endpoints and prompt patterns for the user's intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to generate or edit images through RunComfy by choosing suitable model routes, prompt patterns, and CLI invocations for text-to-image and image-to-image workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release guidance includes unpinned npm/npx RunComfy CLI setup.

Mitigation: Use a pinned, reviewed CLI version or a project-local install before enabling the skill in production workflows.

Risk: RunComfy prompts, reference-image URLs, and generated-output requests are sent to RunComfy.

Mitigation: Install only when that data sharing is acceptable, and pass reference URLs or enable web search only when the user intends those external inputs to affect generation.

Risk: RunComfy credentials are required through RUNCOMFY_TOKEN or local CLI token storage.

Mitigation: Protect RUNCOMFY_TOKEN and ~/.config/runcomfy/token.json, and avoid logging, prompting with, or committing tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/ai-image-generation-runcomfy)
- [RunComfy image models](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-image-generation-runcomfy)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-image-generation-runcomfy)
- [RunComfy CLI install](https://docs.runcomfy.com/cli/install?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-image-generation-runcomfy)
- [RunComfy CLI authentication](https://docs.runcomfy.com/cli/auth?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-image-generation-runcomfy)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-image-generation-runcomfy)
- [Best image editing models collection](https://www.runcomfy.com/models/collections/best-image-editing-models?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-image-generation-runcomfy)
- [Nano Banana collection](https://www.runcomfy.com/models/collections/nano-banana?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-image-generation-runcomfy)
- [Seedream collection](https://www.runcomfy.com/models/collections/seedream?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-image-generation-runcomfy)
- [Qwen Image collection](https://www.runcomfy.com/models/collections/qwen-image?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-image-generation-runcomfy)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline RunComfy CLI commands and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces model-selection guidance and command examples; generated image files are downloaded by the RunComfy CLI into the requested output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
