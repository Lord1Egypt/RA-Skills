## Description:

AI智能内容总结和项目复盘工具，支持多个大模型API。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users use this skill to summarize daily work, meetings, articles, and project material with configured LLM providers, compare provider outputs, and fall back to basic summarization when API keys are unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted content may be sent to configured external AI providers.

Mitigation: Use the skill only with content that is approved for the selected provider and configure API keys according to the provider's data handling requirements.

Risk: Full input text may be retained in a plaintext SQLite database at ~/.ai_summary.db.

Mitigation: Run the skill in an isolated environment, avoid confidential inputs unless local retention is acceptable, and remove or protect the database after use.

Risk: The artifact imports a parent-directory llm_client module that was not included in the reviewed files.

Mitigation: Verify the llm_client source before installation or before entering API keys and sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nidhov01/skills/06-ai)
- [Zhipu AI API keys](https://open.bigmodel.cn/usercenter/apikeys)
- [OpenAI API keys](https://platform.openai.com/api-keys)
- [Anthropic Console](https://console.anthropic.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Plain text summaries, JSON-like result dictionaries, and exported Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can use configured external LLM providers or a basic local fallback; normal use may save summary history locally.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
