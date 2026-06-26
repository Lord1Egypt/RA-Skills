## Description: <br>
Helps medical billers, denials specialists, revenue-cycle analysts, and coders convert denied medical insurance claims into draft appeal packets with denial-code routing, appeal-level selection, deadline tracking, and enclosures for biller or clinician review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Medical billers, denials specialists, coders, revenue-cycle analysts, and clinicians use this skill to draft payer-specific medical claim appeal packets from denied claims, remittance data, denial codes, and chart evidence. It is intended for human review before submission, not automated filing or clinical decision-making. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Draft appeal packets may involve protected health information or payer/member identifiers. <br>
Mitigation: Use minimum-necessary identifiers, avoid full DOB, SSN, and full member IDs in working drafts, and follow the organization's HIPAA and data-handling requirements. <br>
Risk: Incorrect payer rules, plan type, appeal level, or filing deadline could harm the appeal. <br>
Mitigation: Verify deadlines, appeal rights, payer procedures, delivery address, and portal or fax requirements against source documents before submission; treat deadlines within seven days as critical. <br>
Risk: Generated arguments may overstate chart evidence or include unsupported medical, coding, policy, or authorization facts. <br>
Mitigation: Require every clinical and policy assertion to be anchored to supplied evidence and have the appropriate biller, coder, or clinician review the draft before use. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/archlab-space/denied-claim-appeal-drafter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown draft appeal packet with cover letter, denial mapping table, enclosures index, deadline tracker, delivery checklist, escalation calendar, and unresolved-information list.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-only output for biller, coder, or clinician review before any submission.] <br>

## Skill Version(s): <br>
0.1.1 (source: evidence release and changelog, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
