## Description:

Use this skill when a medical biller, denials specialist, revenue-cycle analyst, or coder needs to convert a denied insurance claim into a draft appeal packet with denial-code routing, appeal-level guidance, deadline tracking, and enclosures for biller, coder, or clinician review before submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

External medical billing, denials, coding, revenue-cycle, and clinician-review teams use this skill to turn EOB or 835 ERA denial details and chart excerpts into a draft, single-issue appeal packet. It helps route the denial by CARC/RARC pattern, identify the appeal level, assemble evidence anchors, and track filing deadlines for human review before submission.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Sensitive healthcare billing workflows may involve PHI, claim identifiers, or chart excerpts.

Mitigation: Use minimum necessary data, redact full identifiers, avoid pasting PHI into external services, and keep every output as a draft for qualified review.

Risk: Incorrect payer deadlines, appeal levels, or policy citations could harm the appeal record.

Mitigation: Verify payer procedures, filing windows, policy citations, and deadline calculations against the denial letter or payer documentation before submission.

Risk: Unsupported clinical or coding assertions could overstate the record.

Mitigation: Anchor each assertion to user-provided chart, coding, or policy evidence; mark missing facts as unknown and require biller, coder, or clinician review.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown draft appeal packet with structured tables and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft only; includes an appeal letter, denial-reason mapping table, enclosures index, filing-deadline tracker, certified-delivery checklist, escalation calendar, and unresolved-information list.]

## Skill Version(s):

0.1.1 (source: server release metadata and CHANGELOG, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
