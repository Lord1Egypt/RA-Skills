## Description:

基金新闻日报。从证券时报、中国证券报、证券日报、上海证券报、中国基金报抓取公募基金新闻，支持今日/过去七天/指定日期/指定日期范围查询，过去七天和日期范围查询支持生成Word文档。严格过滤私募/ETF龙虎榜/资金净流入等内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yujing2013](https://clawhub.ai/user/yujing2013)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to gather public fund-industry news from five Chinese financial news sources for today, the past seven days, a specified date, or a specified date range. It returns a structured news summary and can generate Word documents for weekly or date-range reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may modify the execution environment by automatically installing unpinned third-party dependencies, including a global npm package and a Python package.

Mitigation: Use an isolated environment, manually install reviewed and pinned dependency versions, and require explicit approval before any global npm or ambient pip install.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yujing2013/skills/fund-news-daily)
- [Query rules](references/query_rules.md)
- [Filter rules](references/filter_rules.md)
- [Technical specifications](references/technical_specs.md)
- [Word format](references/word_format.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration]

**Output Format:** [Structured text or Markdown response, with optional DOCX file generation for weekly and date-range reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public news URLs as inputs and can produce a Word document when python-docx is available.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
