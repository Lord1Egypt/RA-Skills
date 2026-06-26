## Description: <br>
Manage and track contract renewals by monitoring expiration dates, renewal windows, lifecycle status, and local JSON contract records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cunningham050503-ops](https://clawhub.ai/user/cunningham050503-ops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operations, procurement, or legal teams use this skill to track contract metadata, renewal deadlines, notice windows, and renewal status. It can also help analyze contract text and draft renewal proposals using the included renewal guidance and templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local contract records may include contract names, counterparties, dates, values, and notes. <br>
Mitigation: Install only if local JSON storage is acceptable, and back up ~/.openclaw/workspace/contract-renewal-agent/contracts.json regularly. <br>
Risk: Update and delete actions can change or remove important contract records. <br>
Mitigation: Require clear user confirmation before updating or deleting important records. <br>


## Reference(s): <br>
- [Contract Renewal Strategies](references/renewal_strategies.md) <br>
- [Contract Renewal Proposal Templates](references/contract_templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, update, or delete local contract records when the user runs the corresponding CLI actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
