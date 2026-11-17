## Description:

Helps agents create and edit Firefly Air Compressor product images, videos, voiceovers, 3D displays, and bilingual product detail pages using local scripts or template-guided generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhc2026](https://clawhub.ai/user/yhc2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and marketing operators use this skill to produce branded Firefly Air Compressor media assets, product pages, OCR-derived product data, voiceovers, and video edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can alter the local Python environment when dependency installation is requested.

Mitigation: Run environment checks first, prefer an isolated virtual environment, and review install commands before execution.

Risk: The TTS workflow can send input text to an online service.

Mitigation: Avoid sensitive text unless remote processing is acceptable and disclose that network processing may occur.

Risk: Generated HTML may include active content derived from YAML, OCR results, or product data.

Mitigation: Use trusted inputs, sanitize user-provided content, and review generated pages before publishing.

Risk: Generated pages may load third-party code.

Mitigation: Review generated HTML dependencies and hosting requirements before deployment.

## Reference(s):

- [Firefly Air Compressor homepage](http://www.fireflies.net.cn)
- [Design Guidelines](references/design-guidelines.md)
- [Product Templates](references/product-templates.md)
- [Tools Reference](references/tools-reference.md)
- [Video Production Specs](references/video-specs.md)
- [Python](https://www.python.org/)
- [FFmpeg Downloads](https://ffmpeg.org/download.html)
- [AgentSkills Open Standard](https://agentskills.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands, generated HTML, JSON OCR output, media files, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local image, audio, video, YAML, JSON, and self-contained HTML artifacts depending on the requested workflow.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and README report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
