## Description: <br>
Fund administration and finance operations skillset for GL reconciliation, break tracing, accrual schedules, roll-forwards, variance commentary, and NAV tie-out. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance operations, fund accounting, and controller teams use this skill during daily reconciliation and month-end close to prepare schedules, trace breaks, draft journal-entry support, write variance commentary, and flag NAV tie-out issues for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated journal entries, suppress or adjust recommendations, variance commentary, and NAV flags could affect financial records or statements if treated as final. <br>
Mitigation: Treat all generated outputs as drafts for controller or finance operations review before any ledger posting, statement change, or business action. <br>
Risk: The skill is intended to work with finance systems and documents that may contain sensitive accounting data. <br>
Mitigation: Install and run it only in environments where the agent is authorized to read the relevant finance systems and documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/financial-admin-tool) <br>
- [Publisher profile](https://clawhub.ai/user/paudyyin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown tables, narrative summaries, JSON objects, and draft journal-entry blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are draft review artifacts and do not post ledger entries, edit statements, or make final business decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
