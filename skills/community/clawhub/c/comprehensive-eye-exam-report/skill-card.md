## Description: <br>
Drafts a structured comprehensive eye exam report from encounter data for licensed Doctor of Optometry review, covering visual acuity, refraction, binocular vision, anterior and posterior segment findings, intraocular pressure, diagnoses, and treatment or referral planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Doctors of Optometry, optometric residents, and clinical documentation specialists use this skill to turn eye exam encounter data into a structured draft report for licensed OD review. It supports documentation for comprehensive exams, EMR entry, referral planning, and continuity of care, but does not finalize records or issue prescriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft eye exam documentation could be mistaken for finalized clinical guidance, a prescription, or a medical-record entry. <br>
Mitigation: Keep outputs clearly labeled as draft-only and require licensed Doctor of Optometry review and signature before clinical, billing, referral, payer, or record use. <br>
Risk: Patient identifiers or unnecessary sensitive data could be entered during documentation drafting. <br>
Mitigation: Collect only patient initials and year of birth, and avoid full names, full dates of birth, medical record numbers, insurance information, or other unnecessary identifiers. <br>
Risk: ICD-10 codes, referral flags, or clinical impressions may be incomplete or incorrect if source encounter data is missing or unconfirmed. <br>
Mitigation: Surface history gaps, reduced visual acuity, urgent findings, referral flags, and unconfirmed ICD-10 codes as open items for licensed OD review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/comprehensive-eye-exam-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured draft report in Markdown with tables, referral flags, open items, and a licensed OD review and signature block.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-only clinical documentation; requires licensed OD review before prescription issuance, referral, billing, payer transmission, or medical-record entry.] <br>

## Skill Version(s): <br>
0.1.0 (source: changelog, released 2026-06-01; server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
