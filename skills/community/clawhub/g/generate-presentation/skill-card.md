## Description: <br>
Generate professional HTML and PDF presentations from markdown content, URLs, or topics. Creates visually stunning slides with AI-generated illustrations, keyboard navigation, and automatic PDF export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nhype](https://clawhub.ai/user/nhype) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers, designers, and business users use this skill to turn markdown content, URLs, topics, or plain text into polished slide decks with editable source content, browser-based slides, AI-generated images, and PDF export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged local settings preapprove broad rsync use. <br>
Mitigation: Remove or ignore artifact/.claude/settings.local.json before installation unless broad rsync access is intentional. <br>
Risk: The bundled image MCP server accepts absolute image input and output paths. <br>
Mitigation: Run it in a dedicated presentation workspace and restrict image reads and writes to intended project directories. <br>
Risk: Slide content and reference images may be sent to OpenAI or Azure OpenAI for image generation and editing. <br>
Mitigation: Use a dedicated limited API key and avoid confidential content unless external processing is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nhype/generate-presentation) <br>
- [Skill README](README.md) <br>
- [OpenAI GPT Image MCP Server README](mcp-servers/openai-gpt-image/README.md) <br>
- [OpenAI API keys](https://platform.openai.com/api-keys) <br>
- [Pillow documentation](https://pillow.readthedocs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance plus generated HTML, PDF, PNG images, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the skill is designed to produce presentation/slides.html, presentation/presentation.pdf, slide screenshots, generated images, and presentation/content.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
