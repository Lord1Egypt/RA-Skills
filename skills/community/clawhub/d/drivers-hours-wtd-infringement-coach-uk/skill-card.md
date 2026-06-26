## Description: <br>
Creates a 1-page driver-facing tacho/WTD infringement note plus corrective actions and review date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KOwl64](https://clawhub.ai/user/KOwl64) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Transport managers, compliance staff, and fleet operators use this skill to turn supplied tacho or WTD infringement evidence into a driver-facing coaching note, corrective action plan, and review date. It is intended for evidence-based coaching and follow-up scheduling, not standalone legal or disciplinary advice. <br>

### Deployment Geography for Use: <br>
United Kingdom <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive driver and employment-context information. <br>
Mitigation: Provide only necessary driver data and have a manager or compliance owner review outputs before using them in any formal HR or disciplinary process. <br>
Risk: RAG escalation depends on the user's internal policy and prior infringement history. <br>
Mitigation: Confirm the RAG escalation rule, lookback window, authorisation path, and prior amber or red counts before relying on the proposed status or review schedule. <br>
Risk: Generated notes could overstate responsibility or legal thresholds if source records are incomplete. <br>
Mitigation: Use supplied records and internal policy only, resolve conflicting sources before drafting, and keep outputs factual and coaching-focused. <br>


## Reference(s): <br>
- [Company RAG Escalation Rule](references/rag-escalation-rule.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/KOwl64/drivers-hours-wtd-infringement-coach-uk) <br>
- [Publisher Profile](https://clawhub.ai/user/KOwl64) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown documents for a driver infringement note and corrective action plan] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces driver-infringement-note.md and corrective-action-plan.md; the driver note is intended to stay around one page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
