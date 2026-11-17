## Description:

基金新闻日报。从五大财经平台抓取基金新闻，支持特定日期或一段时间查询，自动生成 Word 文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[imkiiki](https://clawhub.ai/user/imkiiki)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance reporting teams use this skill to collect Chinese public-fund industry news for a specific day or date range, filter out single-product or non-public-fund items, and produce a concise daily summary or Word report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on outbound searches through financial news providers, so results may be incomplete, unavailable, or vary by provider coverage.

Mitigation: Review the returned source links and treat the generated summary as a reporting aid, not an authoritative financial record.

Risk: The documented setup uses unpinned global npm and pip installation commands.

Mitigation: Install dependencies in an isolated environment and pin reviewed versions before operational use.

Risk: Date-range queries can create local Word report files.

Mitigation: Run the skill in a controlled workspace and review the generated document path and contents before sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/imkiiki/skills/fundnews-search)
- [Content Filtering Rules](references/filter_rules.md)
- [Technical Implementation Details](references/technical_specs.md)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Markdown-style text summaries and .docx Word documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Date-scoped Chinese public-fund news summaries with source links; multi-day queries can create a local Word document.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
