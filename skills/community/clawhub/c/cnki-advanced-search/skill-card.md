## Description:

知网（CNKI）高级检索论文自动化工具，当用户提供研究关键词时，指导代理在 CNKI 高级检索中筛选 CSSCI 来源期刊、按被引量排序、切换摘要视图，并通过导出功能保存含题录和摘要的 Word 文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yipng05-max](https://clawhub.ai/user/yipng05-max)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and analysts use this skill to run structured CNKI advanced searches for CSSCI journal papers, confirm keyword groups, and export bibliographic records and abstracts for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent operates CNKI in a browser and may encounter login, payment, captcha, or anti-automation controls.

Mitigation: Confirm the intended CNKI workflow before execution and require the user to handle any access-control or verification step that blocks form operation.

Risk: The skill creates local exported result files that may include bibliographic records and abstracts selected by the search criteria.

Mitigation: Confirm keyword groups, expected export count, and save location before export, then report the final file path and exported quantity.

## Reference(s):

- [CNKI Advanced Search](https://kns.cnki.net/kns8s/AdvSearch)
- [ClawHub skill page](https://clawhub.ai/yipng05-max/skills/cnki-advanced-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown progress updates and local exported document file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Word or Excel export files containing CNKI search results, bibliographic records, and abstracts.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
