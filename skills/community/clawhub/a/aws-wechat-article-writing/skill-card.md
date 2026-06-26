## Description: <br>
公众号写稿｜长文写作｜文章润色｜改写续写 — 公众号长文 AI 写作，从话题或提纲生成完整初稿，支持改写、续写、润色、开头结尾优化，可调 DeepSeek / GPT / Claude 或由 Agent 代写。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiworkskills](https://clawhub.ai/user/aiworkskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, WeChat account operators, and brand copywriters use this skill to draft, rewrite, continue, and polish long-form WeChat articles from a topic, outline, existing article, or selected reference documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Drafts, topic cards, writing configuration, and selected reference documents may be sent to the configured LLM endpoint. <br>
Mitigation: Use only trusted providers or an approved internal proxy, and avoid passing confidential business documents through --reference unless that endpoint is approved for that data. <br>
Risk: The skill requires a writing-model API key and sends it to the configured endpoint as a bearer token. <br>
Mitigation: Use a dedicated key, store it in aws.env, and configure only endpoints trusted to receive that credential. <br>
Risk: Generated article drafts may contain inaccurate, unsupported, or overly promotional content. <br>
Mitigation: Review draft.md before downstream review, layout, image, or publishing steps, and verify claims against provided source documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiworkskills/aws-wechat-article-writing) <br>
- [Writing script usage](references/usage.md) <br>
- [WeChat long-form structure template](references/structure-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown articles, prompt JSON, and configuration-oriented instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write draft.md in the selected article directory and can emit prompt JSON without calling an external model.] <br>

## Skill Version(s): <br>
1.0.25 (source: server release evidence, created 2026-06-16T09:48:28Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
