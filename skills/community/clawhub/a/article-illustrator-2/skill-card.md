## Description:

Generates coordinated illustrations for articles with structured type and style decisions, prompt and batch generation, and optional Markdown insertion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[632657122](https://clawhub.ai/user/632657122)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan, generate, and insert multiple coordinated illustrations into long-form Markdown articles. It is suited to tutorials, methods, reviews, explainers, and other articles where visuals should clarify section flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article prompts, generated-task metadata, and provided reference images may be sent to WeryAI.

Mitigation: Use the skill only with content and reference images that are appropriate to share with WeryAI; avoid private local reference images unless upload is intended.

Risk: The image generation API key can be persisted under `.image-skills/article-illustrator/.env` when setup is run with persistent storage.

Mitigation: Prefer environment variables for `IMAGE_GEN_API_KEY`, and review file permissions before choosing persisted setup.

Risk: The workflow may use `npx -y bun`, which can fetch a runtime during execution.

Mitigation: Use a pinned local Bun runtime when reproducibility or supply-chain control is required.

Risk: `http://` reference image URLs may be insecure or blocked.

Mitigation: Prefer public `https://` reference image URLs and avoid local paths or data URLs.

Risk: The insertion step can modify article Markdown in place.

Mitigation: Use an explicit output file or review the automatic backup and insertion summary before publishing.

## Reference(s):

- [Types and Styles](references/types-and-styles.md)
- [Outline Template](references/outline-template.md)
- [Prompt Template](references/prompt-template.md)
- [WeryAI Text-to-Image API](https://docs.weryai.com/api-reference/image-generation/submit-text-to-image-task)
- [WeryAI Image-to-Image API](https://docs.weryai.com/api-reference/image-generation/submit-image-to-image-task)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON configuration, generated image files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create outline.md, prompt files, batch.json, image outputs, and an updated article Markdown file.]

## Skill Version(s):

9.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
