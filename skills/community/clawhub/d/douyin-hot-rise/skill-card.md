## Description:

调用抖音上升热点榜接口，获取实时热点上升趋势数据，并通过随附的 Python 脚本返回排名、标题、热度和状态信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyriswu](https://clawhub.ai/user/kyriswu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch and summarize Douyin rising hot topic lists, with optional paging, sorting, category, and keyword filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AZT_API_KEY can be exposed if passed as a command-line argument or recorded in shell history or logs.

Mitigation: Prefer a managed secret or the AZT_API_KEY environment variable, and rotate any key previously exposed in shell history or logs.

Risk: The skill sends the API key and query filters to coze-js-api.devtool.uk/devtool.uk.

Mitigation: Install and run the skill only when those service operators are trusted for the submitted data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyriswu/skills/douyin-hot-rise)
- [Douyin hot rise API endpoint](https://coze-js-api.devtool.uk/douyin/billboard/fetch_hot_rise_list)
- [Devtool plugin documentation](https://devtool.uk/plugin)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summary with optional raw JSON output from the bundled Python script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AZT_API_KEY; supports page, page_size, order, sentence_tag, and keyword filters.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
