## Description: <br>
基金新闻日报。从五大财经平台抓取基金新闻，支持特定日期或一段时间查询，自动生成 Word 文档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imkiiki](https://clawhub.ai/user/imkiiki) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to collect Chinese public fund industry news from major finance outlets for a specific day or date range. It filters for industry-wide and regulatory items and can produce a dated Word report for range queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs outbound searches against third-party financial and news search services. <br>
Mitigation: Review network access expectations before installation and run it only in environments where those outbound searches are permitted. <br>
Risk: Range queries can create local Word documents. <br>
Mitigation: Choose an explicit report output path and review generated documents before sharing or relying on them. <br>
Risk: The skill depends on npm and pip packages for search access and Word document generation. <br>
Mitigation: Pin or review the mcporter and python-docx dependencies in stricter environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/imkiiki/fundnews-search) <br>
- [Content Filtering Rules](references/filter_rules.md) <br>
- [Technical Implementation Details](references/technical_specs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown/text news summaries and .docx Word documents for date-range reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are grouped by date and source, include article summaries and official links, and may create an auto-named Word file for range queries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
