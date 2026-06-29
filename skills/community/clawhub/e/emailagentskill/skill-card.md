## Description: <br>
Helps agents plan, review, audit, and improve email workflows with explicit tool handoffs, approval gates, QA loops, and safe execution boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polnikale](https://clawhub.ai/user/polnikale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and AI agents use this skill to structure email-related work into safe routing plans, approval matrices, tool handoff specifications, review loops, execution checklists, and audit-friendly status reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger text could pull the skill into work outside email-related planning, QA, and handoffs. <br>
Mitigation: Keep usage focused on email workflows and require the final handoff to name unresolved risks, assumptions, and owners. <br>
Risk: Email workflow guidance can lead to live sends, contact imports, DNS or authentication changes, suppression edits, or production automation changes. <br>
Mitigation: Require explicit human approval before any live send, import, DNS/authentication change, suppression edit, or production automation change. <br>


## Reference(s): <br>
- [Email Agent Skill Operating Checklist](references/operating-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured plans, matrices, checklists, and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Separates recommendations from live-system actions and identifies approval gates before high-risk email operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
