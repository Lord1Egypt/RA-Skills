## Description:

生成多尺度中文资讯简报，按全球、国家、省市、区县、街道或行业范围检索公开新闻和社交来源并结构化输出简报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shine8592](https://clawhub.ai/user/shine8592)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to assemble Chinese-language briefings for local, national, global, or industry topics from public web and news sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefings may include incorrect, outdated, or misleading claims from public news or social-platform sources.

Mitigation: Review the cited sources before relying on conclusions or taking action.

Risk: Briefing prompts could expose private or sensitive information if users include it in the topic or location request.

Mitigation: Avoid entering private, confidential, or sensitive information in prompts.

## Reference(s):

- [搜索模板](references/search-templates.md)
- [新闻来源库](references/source-library.md)
- [ClawHub skill page](https://clawhub.ai/shine8592/skills/china-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown briefing with structured sections, source citations, optional tables, and helper-script JSON when invoked directly.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite sources for each item and keep the briefing concise.]

## Skill Version(s):

1.0.0 (source: server release metadata and README version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
