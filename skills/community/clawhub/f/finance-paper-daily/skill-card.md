## Description:

Finance Paper Daily fetches recent finance research papers from arXiv, Semantic Scholar, OpenAlex, and Google Scholar, then creates a formatted Excel report on the user's Desktop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snow-seamless](https://clawhub.ai/user/snow-seamless)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and finance practitioners use this skill to collect recent finance literature and produce a daily spreadsheet report for review and tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install unpinned Python packages into the user's environment.

Mitigation: Run it in a dedicated virtual environment, avoid --break-system-packages, and preinstall reviewed dependency versions.

Risk: The generated spreadsheet is populated from remote paper metadata.

Mitigation: Treat the workbook contents and links as untrusted until reviewed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/snow-seamless/skills/finance-paper-daily)
- [arXiv API query endpoint](http://export.arxiv.org/api/query)
- [Semantic Scholar paper search API](https://api.semanticscholar.org/graph/v1/paper/search)
- [OpenAlex works API](https://api.openalex.org/works)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Text]

**Output Format:** [Excel workbook (.xlsx) plus terminal status text and setup/run commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes ~/Desktop/YYYY-MM-DD_finance_papers.xlsx and overwrites the same-day file on rerun.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
