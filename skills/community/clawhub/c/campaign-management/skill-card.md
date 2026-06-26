## Description: <br>
Read campaign packages, manage campaign state, generate intelligence reports. Entry point for all campaign operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nadavnaveh](https://clawhub.ai/user/nadavnaveh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Campaign operators and developers use this skill to structure marketing campaign packages, track campaign progress, and generate intelligence reports before deciding whether to proceed with outreach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous outreach workflows can send email, LinkedIn, X, Reddit, or other campaign actions without enough explicit approval controls. <br>
Mitigation: Use intelligence or draft-only workflows unless explicit human approval gates are added before any outbound or autonomous campaign action. <br>
Risk: Campaign lead collection can expose contact data and campaign intelligence if folders are shared too broadly or retained indefinitely. <br>
Mitigation: Keep campaign folders private and define retention and deletion rules for lead data, intelligence files, outbox drafts, reports, and logs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, CSV, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and message drafts, JSON campaign state, YAML configuration, and CSV lead files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are organized under campaign folders such as state.json, report.md, enriched-leads.csv, intel files, outbox drafts, and logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
