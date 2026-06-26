## Description: <br>
Tracks detailed AI agent expenses, revenues, budgets, and ROI with per-agent attribution and alerts for micro-budget financial management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmonddantesj](https://clawhub.ai/user/edmonddantesj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators running AI agent squads use this skill to log API costs, gas fees, revenue, budgets, and per-agent spend for ROI and runway tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ledger records are stored as local plaintext files and may expose financial details, receipt links, wallet notes, or other sensitive records. <br>
Mitigation: Use trusted local workspaces, avoid storing secrets or private wallet details, and protect or remove ledger files according to the user's data-handling requirements. <br>
Risk: Budget limits provide alerts and reporting signals rather than controls that can stop API, infrastructure, or blockchain spending. <br>
Mitigation: Pair ledger alerts with provider-side budgets, account limits, or wallet controls when spend enforcement is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edmonddantesj/aoineco-ledger) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python usage examples and CSV/JSON ledger output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled Python engine writes local plaintext JSON, JSONL, and CSV-style ledger records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
