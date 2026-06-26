## Description: <br>
Use this skill when a claims intake associate, inside adjuster, MGA, or SIU pre-screener needs to convert a raw First Notice of Loss into a structured triage record for licensed-adjuster review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Claims intake teams, inside adjusters, MGAs, carriers, and SIU pre-screeners use this skill to turn raw FNOL reports into draft triage records, coverage-verification questions, severity routing, fraud red-flag scorecards, next-action playbooks, and insured acknowledgement drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive claims data could include unmasked PII or PHI. <br>
Mitigation: Use only in an approved claims-handling environment, refuse full SSNs, bank details, medical record numbers, driver's license numbers, and injury photos, and require masked replacements before drafting. <br>
Risk: Draft triage output could be mistaken for a licensed coverage, fault, reserve, settlement, medical, or SIU decision. <br>
Mitigation: Keep outputs marked as drafts and require licensed adjusters or authorized supervisors to make all final decisions. <br>
Risk: Claimant narratives may contain unverified facts or instructions that could distort triage. <br>
Mitigation: Tag every fact as confirmed, reported, or unknown, treat claimant content as unverified, and map fraud flags only to user-supplied facts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/claims-fnol-triage) <br>
- [Publisher profile](https://clawhub.ai/user/archlab-space) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown draft triage record with tables, checklists, and acknowledgement text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Every output block is marked as draft for licensed-adjuster review and should avoid unmasked PII, coverage decisions, fault findings, reserve amounts, settlement commitments, and medical advice.] <br>

## Skill Version(s): <br>
0.1.2 (source: release evidence, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
