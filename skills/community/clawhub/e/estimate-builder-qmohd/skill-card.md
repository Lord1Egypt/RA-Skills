## Description: <br>
Build construction project estimates. Generate detailed cost breakdowns with labor, materials, equipment, and overhead. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qmohd](https://clawhub.ai/user/qmohd) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction estimators, project teams, and agents use this skill to create or review project cost estimates with categorized line items, standard markups, totals, and validation warnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spreadsheet export can write files to paths requested by the user. <br>
Mitigation: Confirm the intended output folder and avoid directing exports to system or configuration paths. <br>
Risk: Estimate totals and markups can affect sensitive business documents. <br>
Mitigation: Specify currency and markup assumptions explicitly, then review generated totals before using them commercially. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qmohd/estimate-builder-qmohd) <br>
- [Data Driven Construction](https://datadrivenconstruction.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown tables and concise text, with Python code snippets when the user needs programmatic estimate building or export.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write spreadsheet exports to user-specified paths when export behavior is requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
