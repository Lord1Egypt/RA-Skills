## Description: <br>
Mandatory safety gatekeeper for AI agents performing destructive operations; it intercepts destructive file, database, system, mass-operation, and external-transmission actions, verifies backup coverage, and escalates high-risk or unverified actions for human approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tooled-app](https://clawhub.ai/user/tooled-app) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Guardian as a safety gate for AI agents before operations that could irreversibly modify, delete, transmit, or reconfigure data and systems. The skill returns proceed-or-halt guidance, backup-verification expectations, and escalation prompts for human approval when required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Policy inconsistencies could allow destructive actions to proceed without the human approval users expect. <br>
Mitigation: Require explicit human approval for all high-risk or critical destructive actions, regardless of backup status or JIT downgrade language. <br>
Risk: Backup verification signals may not prove that a real, restorable backup exists for the affected target. <br>
Mitigation: Treat helper-script results as advisory and verify restore coverage before permitting destructive execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tooled-app/data-guardian) <br>
- [Operation Taxonomy](artifact/OPERATION-TAXONOMY.md) <br>
- [Decision Matrix](artifact/DECISION-MATRIX.md) <br>
- [Backup Verification Script for Linux and macOS](artifact/scripts/verify-backup.sh) <br>
- [Backup Verification Script for Windows](artifact/scripts/verify-backup.ps1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with structured escalation prompts and optional JSON backup-verification results from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit human approval for high-risk destructive actions and treats unverified backup status as a halt condition.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata; bundled SKILL.md frontmatter reports 1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
