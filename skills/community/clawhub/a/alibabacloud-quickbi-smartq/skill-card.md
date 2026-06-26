## Description: <br>
Quick BI-SmartQ routes data analysis requests across Quick BI file and dataset Q&A, document parsing, dashboard skill generation, data insights, and report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and data analysts use this skill to analyze Quick BI datasets, uploaded spreadsheet or document files, dashboards, and report requests through a routed agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Quick BI may receive uploaded files, questions, dashboard data, and report inputs. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and prefer scoped Quick BI credentials for the intended workspace. <br>
Risk: Trial mode may create a persistent device-linked user record and the skill may store credentials or identifiers in .qbi configuration files. <br>
Mitigation: Review ~/.qbi/config.yaml and the workspace .qbi/smartq-chat/config.yaml before use, and disable global saving where possible. <br>
Risk: Dashboard skill generation may alter skill-center directories. <br>
Mitigation: Review generated dashboard skills and scan them before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-quickbi-smartq) <br>
- [Publisher profile](https://clawhub.ai/user/sdk-team) <br>
- [File Q&A module](artifact/references/chat/module-chat-file.md) <br>
- [Dataset Q&A module](artifact/references/chat/module-chat-dataset.md) <br>
- [Document parser module](artifact/references/document/module-document-parser.md) <br>
- [Dashboard skill generation module](artifact/references/dashboard/module-dashboard.md) <br>
- [Data insight module](artifact/references/insight/module-data-insight.md) <br>
- [Data report module](artifact/references/report/module-data-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown responses with command examples, chart image links, and generated files where applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chart image Markdown links are treated as primary deliverables and should be preserved verbatim when produced.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata; artifact metadata reports 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
