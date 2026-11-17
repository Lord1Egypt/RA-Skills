## Description:

Generates Xiaohongshu post plans, captions, hashtags, and AI images, and can publish notes through a local xiaohongshu MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baoshan685](https://clawhub.ai/user/baoshan685)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and social-media operators use this skill to turn a topic into Xiaohongshu-ready visual post content, including structured page prompts, captions, hashtags, generated image files, and optional publishing steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generated images may be sent to configured API and MCP services.

Mitigation: Use only content and assets that are acceptable to share with those services, and review provider configuration before running generation or publishing commands.

Risk: API keys are stored in a local configuration file.

Mitigation: Keep config/local-config.json out of Git, use a restricted and revocable API key, and rotate the key if it may have been exposed.

Risk: The optional auto-sync setup creates a recurring background job that commits repository changes.

Mitigation: Do not run setup-auto-sync.sh unless recurring commits are intentional; inspect Git status and exclude secrets or generated artifacts before enabling it.

Risk: Publishing can post generated content to a real Xiaohongshu account.

Mitigation: Review generated captions, tags, and images before publishing, and confirm that the local MCP service is connected to the intended account.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/baoshan685/skills/easy-xiaohongshu)
- [Z3i0 API](https://z.3i0.cn)
- [Prompt Template](artifact/references/prompt-template.md)
- [Caption Template](artifact/references/caption-template.md)
- [Style Presets](artifact/references/style-presets.json)
- [Hashtag Library](artifact/references/hashtag-library.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON content artifacts and PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include generated_content.json, generated_caption.json, generated_images/*.png, and MCP publish results.]

## Skill Version(s):

0.2.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
