## Description: <br>
Build construction project estimates. Generate detailed cost breakdowns with labor, materials, equipment, and overhead. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction estimators, project managers, and cost engineers use this skill to assemble project line items, apply overhead, profit, and contingency markups, and produce category-level cost summaries for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Filesystem exports can overwrite or place estimate workbooks in unintended locations. <br>
Mitigation: Choose output paths deliberately and review destination filenames before allowing the agent to create files. <br>
Risk: Construction estimates can be misleading if quantities, unit costs, markups, or categories are incomplete or incorrect. <br>
Mitigation: Review line items, category totals, and validation warnings before using outputs for bids, budgets, or approvals. <br>


## Reference(s): <br>
- [Data Driven Construction Website](https://datadrivenconstruction.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/datadrivenconstruction/estimate-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown tables and Python-oriented estimate data; optional Excel workbook output when exported.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses USD by default unless the user specifies another currency; monetary values are rounded to two decimal places.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
