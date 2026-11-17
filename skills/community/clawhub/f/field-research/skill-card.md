## Description:

输入中文关键词后，生成中英双语关键词与文献检索结果表：中文来源知网、英文来源Google Scholar，近10年、相关性排序、按年份降序输出标准Markdown表格；优先可见浏览器人工验证。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huixiaheyu](https://clawhub.ai/user/huixiaheyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and researchers use this skill to turn a Chinese research keyword into bilingual academic search terms and a verified Markdown literature-results table from CNKI and Google Scholar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research keywords are sent to CNKI and Google Scholar during searches.

Mitigation: Avoid private or sensitive research terms unless querying those third-party services is acceptable.

Risk: Browser-based searching may encounter CAPTCHA or security verification pages.

Mitigation: Pause automation and require the user to complete verification before continuing.

Risk: Literature metadata can be incomplete or unverifiable from search result pages.

Mitigation: Do not fabricate missing fields; leave them blank or mark them with a placeholder.

## Reference(s):

- [CNKI Search](https://kns.cnki.net/kns8s/search)
- [Google Scholar](https://scholar.google.com/scholar)
- [ClawHub Skill Page](https://clawhub.ai/huixiaheyu/skills/field-research)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown table with bilingual keyword labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sorts entries by publication year in descending order and leaves unverifiable fields blank or marked with a placeholder.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
