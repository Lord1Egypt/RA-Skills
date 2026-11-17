## Description:

AI 行业资讯专家 + 小红书内容创作。检索 24 小时内最新 AI 资讯，生成小红书文案 + 3:4 比例 HTML 封面。使用场景：(1) 每日 AI 资讯汇总，(2) 小红书图文笔记创作，(3) 大模型发布/融资/技术突破等资讯整理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[javastarboy](https://clawhub.ai/user/javastarboy)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and AI-news operators use this skill to turn recent AI industry news into Xiaohongshu-ready posts, mobile HTML cover pages, source lists, and summary tables. It supports demo data for testing and accepts externally searched news data for normal publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the release as suspicious because the real-data workflow handles web-search results unsafely.

Mitigation: Review and modify the workflow before installation; escape search-result fields before generating HTML or Markdown and inspect generated copy and sources before publishing.

Risk: Shell-string execution and automatic browser or directory opening can create avoidable execution and environment risks.

Mitigation: Replace shell-string examples with argument-array execution, disable automatic opening unless explicitly requested, and avoid unpinned npx search commands.

Risk: Author-controlled promotional contact text can appear in generated outputs.

Mitigation: Review and replace default call-to-action and contact text in the user configuration before using the skill in a public workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/javastarboy/skills/ai-news-xiaohongshu)
- [OpenClaw integration guide](references/openclaw-integration.md)
- [Search query reference](references/search-queries.md)
- [User configuration](references/user-config.md)
- [HTML pagination notes](references/HTML分页修复说明.md)
- [UI optimization notes](references/UI 优化说明.md)
- [Issue fix notes](references/问题修复说明.md)
- [OpenAI blog](https://openai.com/blog)
- [Anthropic news](https://www.anthropic.com/news)
- [Google DeepMind](https://deepmind.google/)
- [Hugging Face blog](https://huggingface.co/blog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, HTML, source-link lists, summary tables, JSON-compatible news inputs, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are written under an output date directory and may include Xiaohongshu copy, a 3:4 mobile HTML cover, a news summary, and source links.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
