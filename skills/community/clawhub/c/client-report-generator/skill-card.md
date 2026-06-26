## Description: <br>
Generate professional client-facing reports from raw data, metrics, and KPIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agencies, consultants, and client-facing teams use this skill to turn CSV, JSON, analytics exports, or plain text metrics into polished performance, campaign, project status, and analytics reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Client reports may process sensitive client metrics or proprietary business data. <br>
Mitigation: Only provide files, URLs, and metrics that are approved for processing and sharing in the target report. <br>
Risk: Generated HTML may retain active untrusted text or links from source data. <br>
Mitigation: Review generated HTML before sharing it with clients or publishing it externally. <br>
Risk: Broad prompts such as "weekly report" may invoke the skill when the user intended a different task. <br>
Mitigation: Confirm the reporting intent and desired data sources before generating or exporting a client-facing report. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/client-report-generator) <br>
- [Report Templates](references/report-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports by default, with optional HTML, plain text, or JSON summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include normalized metrics, trend analysis, recommendations, styled HTML with inline CSS, and commands for local parsing or HTML export.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
