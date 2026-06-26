## Description: <br>
aky-public-opinion 2.0 helps agents collect and cross-check international media signals and produce structured Chinese public-opinion analysis reports with risk assessments and recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangfromchu-ai](https://clawhub.ai/user/wangfromchu-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and government or enterprise teams use this skill to gather public web and media signals, select an appropriate report type, and draft Chinese sentiment or risk reports for incidents, monthly summaries, and international public-opinion tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public-opinion analysis can carry framing bias or mismatch the intended audience and language. <br>
Mitigation: Review final reports for framing bias, confirm the intended audience, and ensure the output language matches the user's needs before use. <br>
Risk: Browser or logged-in source collection can access sites or accounts outside the user's authorization. <br>
Mitigation: Use browser-based or authenticated collection only on sites and accounts the user is authorized to access. <br>
Risk: Media and social-source data can be incomplete, stale, duplicated, or misleading. <br>
Mitigation: Cross-check material across multiple sources, deduplicate repeated reporting, and preserve source names and timestamps in the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangfromchu-ai/aky-publicopinion) <br>
- [Report templates reference](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Chinese Markdown reports with source attribution, structured risk assessment, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include collection checklists, report-type selection, media-source notes, and concrete mitigation recommendations.] <br>

## Skill Version(s): <br>
2.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
