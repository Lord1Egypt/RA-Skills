## Description: <br>
Easy Xiaohongshu helps an agent generate Xiaohongshu text-and-image post content from a topic and optionally prepare publishing through a local Xiaohongshu MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baoshan685](https://clawhub.ai/user/baoshan685) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and social media operators use this skill to turn a post topic into an eight-page Xiaohongshu note with captions, tags, generated image prompts, and generated images. Publishing is optional and should be used only after review with a trusted local MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish live content to Xiaohongshu through a local MCP service. <br>
Mitigation: Review generated captions and images before publishing, confirm the MCP URL is trusted, and use publishing only when the local service is intentionally running. <br>
Risk: Local configuration may contain API keys or other secrets in plaintext. <br>
Mitigation: Keep config/local-config.json private, do not commit it, and prefer environment overrides when practical. <br>
Risk: The auto-sync setup can create recurring background git commits of the skill directory. <br>
Mitigation: Run setup-auto-sync.sh only when background commits are explicitly desired, and inspect the LaunchAgent and auto-sync script before enabling it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/baoshan685/easy-xiaohongshu) <br>
- [Prompt template](references/prompt-template.md) <br>
- [Caption template](references/caption-template.md) <br>
- [Style presets](references/style-presets.json) <br>
- [Hashtag library](references/hashtag-library.json) <br>
- [Z3i0 API](https://z.3i0.cn) <br>
- [Gemini](https://ai.google.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, images, guidance] <br>
**Output Format:** [Markdown guidance with JSON content files, PNG image files, configuration snippets, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected artifacts include generated_content.json, generated_caption.json, and generated_images/*.png; publishing requires user review, a valid API key, and a trusted local MCP service.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
