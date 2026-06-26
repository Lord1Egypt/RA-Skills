## Description: <br>
AI 智能写作助手，支持公众号、小红书、知乎、LinkedIn 等多平台内容创作风格，并提供改写润色、SEO 关键词和热点搜索辅助。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and social media operators use this skill to generate and adapt Markdown drafts for multiple publishing platforms and tones. It can optionally use Tavily-powered hot-topic search when TAVILY_API_KEY is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided topics may be sent to Tavily search when hot-topic search is enabled. <br>
Mitigation: Avoid confidential or sensitive topics unless sharing that topic text with Tavily is acceptable. <br>
Risk: The security summary reports that user-supplied topics are placed into a shell command. <br>
Mitigation: Review before installing and avoid untrusted topic strings until command execution is changed to argument-safe invocation. <br>
Risk: The skill can write generated content to a caller-supplied output path. <br>
Mitigation: Use explicit, expected output paths and document overwrite behavior before relying on generated files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-wuxl/ai-writer-pro) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown article text with console status messages; optionally writes a UTF-8 Markdown file when an output path is supplied.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js. Hot-topic search uses TAVILY_API_KEY when available; topic, style, tone, keywords, length, and output path are command-line options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; README changelog also lists v1.0.0 released 2026-03-20) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
