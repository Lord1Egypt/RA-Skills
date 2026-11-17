## Description:

Data Skill helps an agent process local office datasets by importing, cleaning, querying, merging, exporting, reporting on, and visualizing CSV and Excel-style files with SQL, Python, and SQLite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgwanai](https://clawhub.ai/user/lgwanai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and office teams use this skill to guide an agent through local spreadsheet and CSV workflows, including import, cleaning, SQL querying, fuzzy joins, chart generation, exports, and summary reports. It is intended for local data handling where large files and privacy-sensitive records should not be loaded into the model context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The chart server can expose local project data more broadly than users are told.

Mitigation: Review before installing, use only in a trusted local workspace, bind chart serving to 127.0.0.1, serve only approved output files, remove wildcard CORS, and add a clear stop or timeout mechanism before using sensitive datasets.

Risk: Map and geocoding workflows may send address data to Baidu services.

Mitigation: Treat Baidu map and geocoding features as an external-data path and use them only with approved non-sensitive location data or explicit user approval.

Risk: Python dependencies are listed without pinned versions.

Mitigation: Pin and review dependencies before production use.

## Reference(s):

- [Data Skill ClawHub release page](https://clawhub.ai/lgwanai/skills/data-skill)
- [Metrics definitions](references/metrics.md)
- [Chart prompt templates index](references/prompts/index.md)
- [Baidu Map API key setup](https://lbsyun.baidu.com/apiconsole/key)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline SQL, Python, shell commands, JSON chart configuration, and generated local output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include SQLite databases, exported CSV or Excel files, Markdown reports, and interactive ECharts HTML files served from a local chart server.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
