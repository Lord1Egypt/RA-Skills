## Description:

Consulting and industry report search and QA skill that prioritizes iResearch free reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiyenwong](https://clawhub.ai/user/hiyenwong)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research analysts use this skill to find consulting, industry, and market research reports, then generate conservative answers grounded in public report summaries, catalogs, and reader links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The networked report-detail fetch path can be steered to unexpected web addresses.

Mitigation: Restrict detail fetches to expected iResearch and QuestMobile hosts, require HTTPS, and validate redirects before use in environments with access to private internal services.

## Reference(s):

- [Report Source Notes](references/iresearch-api.md)
- [iResearch report list API](https://www.iresearch.com.cn/api/products/GetReportList)
- [iResearch report detail pages](https://report.iresearch.cn/report/YYYYMM/NNNN.shtml)
- [iResearch online reader](https://report.iresearch.cn/report_pdf.aspx?id=NNNN)
- [QuestMobile reports](https://www.questmobile.com.cn/research/reports/)
- [QuestMobile article list API](https://www.questmobile.com.cn/api/v2/report/article-list?version=0&pageSize=6&pageNo=1&industryId=-1&labelId=-1)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON report search results, detail summaries, and grounded answers with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritizes iResearch results before QuestMobile, preserves source grouping when requested, and states evidence boundaries for report-specific answers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
