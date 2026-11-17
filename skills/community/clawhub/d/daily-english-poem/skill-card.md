## Description:

每日英语诗歌推送从多个英文诗歌网站抓取 Poem of the Day，生成包含诗歌全文、作者介绍和深度赏析的内容并推送至飞书。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cantoneyes](https://clawhub.ai/user/cantoneyes)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or external users use this skill to receive a daily English poem in Feishu with source attribution, poet background, and structured reading appreciation. The skill is intended for recurring poetry discovery and literary analysis rather than code generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic daily Feishu posting may be inappropriate for some chats, workspaces, or audiences.

Mitigation: Confirm the target Feishu channel and posting cadence before enabling the scheduled push.

Risk: Forwarding full poem text and analysis from third-party sites may raise copyright, attribution, or source-quality concerns.

Mitigation: Review source terms and attribution expectations for the configured poetry sources before deployment.

Risk: Poem metadata, author background, or analysis may be incomplete or inaccurate when gathered from web sources.

Mitigation: Prefer reliable author references and review generated analysis when accuracy matters.

## Reference(s):

- [PoemAnalysis Poem of the Day](https://poemanalysis.com/poem-of-the-day/)
- [Poets.org Poem-a-Day](https://poets.org/poem-a-day)
- [Poetry Daily](https://poems.com/)
- [Discover Poetry Poem of the Day](https://discoverpoetry.com/poems/poem-of-the-day/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Feishu-ready structured text with poem text, poet background, and reading appreciation sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source poem formatting where possible and may send a failure notification if all configured sources fail.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
