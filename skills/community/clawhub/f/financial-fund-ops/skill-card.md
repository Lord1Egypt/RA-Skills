## Description: <br>
Fund administration and finance operations skill for GL reconciliation, break tracing, accrual schedules, roll-forwards, variance commentary, and NAV tie-out workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Fund accounting, finance operations, and controller teams use this skill to draft and review reconciliation reports, accrual schedules, roll-forwards, variance commentary, and NAV statement tie-outs before controlled approval steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require access to sensitive fund accounting, ledger, subledger, NAV, invoice, or statement data. <br>
Mitigation: Install only in environments where the agent is authorized to read the relevant fund accounting data. <br>
Risk: Draft journal entries, statement flags, and reconciliation actions could be mistaken for approved financial changes. <br>
Mitigation: Keep ledger posting, statement editing, resolver actions, and other financial changes behind human approval or separate controlled tools. <br>
Risk: Break classifications and variance drivers are diagnostic hypotheses that may be incorrect or incomplete. <br>
Mitigation: Require controller, resolver, or finance operations review before acting on diagnoses, adjustments, suppressions, or external reporting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/financial-fund-ops) <br>
- [Publisher profile](https://clawhub.ai/user/paudyyin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown tables and narrative text, with JSON objects for traced reconciliation breaks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces draft schedules, diagnostics, commentary, and review flags; it does not post ledger entries, edit statements, or execute financial changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter, package.json, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
