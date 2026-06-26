## Description: <br>
Retrieves bank partnership activity and subsidy policy details for a requested city, province, or region from a maintained Feishu policy spreadsheet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users and support agents use this skill to answer regional questions about bank subsidy policies, eligibility terms, activity timing, and policy changes. It formats matching policy rows into concise markdown summaries with special warnings when restrictions or pauses are present. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill directly references a Feishu policy spreadsheet that may contain internal business fields. <br>
Mitigation: Confirm the sheet and columns are appropriate for the intended users before deployment; use a scoped data source or redact internal-only fields if broader access is not intended. <br>
Risk: Responses depend on a manually maintained policy table and may reflect stale or incomplete rows. <br>
Mitigation: Verify high-impact policy answers against the source spreadsheet before using them for customer-facing or financial decisions. <br>


## Reference(s): <br>
- [Bank Policy Query on ClawHub](https://clawhub.ai/runkecheng/bank-policy-query) <br>
- [Publisher profile](https://clawhub.ai/user/runkecheng) <br>
- [Feishu policy spreadsheet](https://sqb.feishu.cn/sheets/ZIfoscVEJhvsHttAwYocTCd2n1b?sheet=0siobJ) <br>
- [Retrieval guide](references/retrieval-guide.md) <br>
- [Policy analysis rules](references/policy-analysis-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Analysis] <br>
**Output Format:** [Markdown policy summaries with warnings and comparison notes when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve source policy values, include required bank activity fields, and avoid inventing missing terms.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
