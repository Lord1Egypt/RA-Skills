## Description:

公众号贴图 / 九宫格多图推送 helps agents plan, generate, review, and optionally publish WeChat public-account sticker or multi-image posts with unified style, prompt planning, image generation, compression, and grid-oriented packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiworkskills](https://clawhub.ai/user/aiworkskills)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and developers use this skill to turn a topic, brief, or source material into a planned WeChat multi-image post with prompts, image files, review checks, and optional publishing steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may send image prompts to an external image API and prepared images to the WeChat API when publishing is used.

Mitigation: Use it only for intended WeChat publishing workflows, review prompts and generated images before upload, and run publishing only after explicit confirmation.

Risk: The workflow requires local article files plus IMAGE_MODEL_API_KEY and optional WeChat app credentials.

Mitigation: Provide credentials only in the expected local environment file, limit credential scope where possible, and confirm configuration checks pass before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aiworkskills/skills/aws-wechat-sticker)
- [AIWorkSkills Homepage](https://aiworkskills.cn)
- [Sticker Review Checklist](references/checklist.md)
- [Sticker Sequence Workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, prompt plans, and file-oriented workflow outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or updates imgs/ outlines, prompts, generated image files, and article status fields; optional publishing sends prepared images through the WeChat workflow.]

## Skill Version(s):

1.0.24 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
