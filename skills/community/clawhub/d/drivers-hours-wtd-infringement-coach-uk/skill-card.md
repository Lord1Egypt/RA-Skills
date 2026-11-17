## Description:

Creates a 1-page driver-facing tacho/WTD infringement note plus corrective actions and review date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kowl64](https://clawhub.ai/user/kowl64)

### License/Terms of Use:


## Use Case:

Fleet managers, transport compliance teams, and driver supervisors use this skill to turn supplied tacho/WTD infringement evidence into driver-facing coaching notes and corrective action plans with review dates.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: The skill may draft coaching material that could be used in employment or disciplinary decisions.

Mitigation: Use outputs as factual coaching drafts only; have a responsible manager or compliance lead review them before any employment action.

Risk: RAG escalation depends on the organization's own policy and prior infringement history.

Mitigation: Confirm the escalation rule, lookback window, prior amber/red counts, authorization path, and evidence bundle before applying an escalation.

Risk: Missing or conflicting driver-hours records can lead to incorrect coaching notes.

Mitigation: Provide driver ID, date range, infringement types, source records, and resolve source conflicts before using the output.

## Reference(s):

- [Company RAG escalation rule](references/rag-escalation-rule.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a driver infringement note and a corrective action plan using supplied facts, internal policy, and a review date.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
