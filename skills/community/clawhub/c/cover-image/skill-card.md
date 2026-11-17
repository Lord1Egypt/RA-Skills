## Description:

Generate article cover images with structured dimensions and bundled generation tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[632657122](https://clawhub.ai/user/632657122)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn article, blog, newsletter, or banner concepts into structured cover-image prompts, generation batches, image files, and compressed delivery assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a WeryAI API key and may persist it in local configuration if setup is run with key persistence.

Mitigation: Prefer environment variables, avoid shared or source-controlled configuration directories, and only persist the key when the user explicitly approves.

Risk: Reference-image handling has review-worthy local-file behavior according to the security evidence.

Mitigation: Use only intentional reference images and treat local reference paths as uploadable to WeryAI until the documentation and runtime are reconciled.

Risk: The skill runs local Node/Bun tooling and sends generation requests to the WeryAI gateway.

Mitigation: Review the skill before installation, run it in a trusted workspace, and install only when WeryAI network access is acceptable.

Risk: Bearer-token forwarding to result URLs could expose credentials if result URLs are not trusted.

Mitigation: Review result download behavior before use and avoid forwarding bearer tokens to untrusted URLs.

## Reference(s):

- [Cover Image Dimensions](references/dimensions.md)
- [Prompt Template](references/prompt-template.md)
- [WeryAI Gateway Alignment Notes](scripts/vendor/shared-image-generation/references/weryai-platform.md)
- [First-Time Setup](scripts/vendor/shared-image-generation/references/config/first-time-setup.md)
- [Style Presets](scripts/vendor/shared-image-generation/references/style-presets.md)
- [WeryAI API Introduction](https://docs.weryai.com/en)
- [WeryAI Text-to-Image API](https://docs.weryai.com/api-reference/image-generation/submit-text-to-image-task)
- [WeryAI Image-to-Image API](https://docs.weryai.com/api-reference/image-generation/submit-image-to-image-task)
- [WeryAI Task Status API](https://docs.weryai.com/api-reference/tasks/query-task-details)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, JSON batch files, prompt files, generated image files, and compressed image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses IMAGE_GEN_API_KEY for WeryAI gateway requests and writes project or user configuration plus cover-image output files.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
