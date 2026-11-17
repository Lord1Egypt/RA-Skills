## Description:

企业年金/职业年金智能查询技能，可帮助代理识别单位性质、选择查询渠道、交叉验证企业年金或职业年金信息，并生成带来源链接和错误检查的调查报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanwenzhe](https://clawhub.ai/user/yanwenzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, job candidates, benefits researchers, and agents use this skill to investigate whether Chinese companies or public institutions disclose enterprise annuity or occupational pension benefits. It guides search-channel selection, source reliability checks, pension-bank lookup, confidence scoring, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names and investigation queries may be sent to external search services.

Mitigation: Use only non-sensitive investigation targets, review search-provider settings before use, and prefer a controlled SearXNG endpoint when confidentiality matters.

Risk: Batch and report scripts derive output paths from company names and use shell templating.

Mitigation: Run scripts only in an isolated workspace, use trusted company-list files, and review or sanitize filenames before batch execution.

Risk: Search scripts can call external skill scripts while inheriting configured credentials.

Mitigation: Review, verify, or vendor search dependencies before installing, and avoid exporting sensitive API keys until that path has been checked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanwenzhe/skills/company-pension-search)
- [Search methods reference](references/search-methods.md)
- [Advanced search channels reference](references/advanced-search-channels.md)
- [CNINFO annual reports](http://www.cninfo.com.cn/)
- [Shanghai Stock Exchange disclosures](http://www.sse.com.cn/)
- [Shenzhen Stock Exchange disclosures](http://www.szse.cn/)
- [Eastmoney fund information](http://fund.eastmoney.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, text search summaries, shell command examples, and JSON configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence scores, source links, pension-bank roles, raw investigation notes, and saved report files.]

## Skill Version(s):

3.2.1 (source: server release evidence; artifact frontmatter and _meta.json list 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
