## Description: <br>
Drafts structured pre-test and post-test genetic counseling session notes covering pedigree narrative, risk assessment, informed consent, result disclosure, psychosocial assessment, patient understanding, and plan for licensed CGC review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Genetic counseling professionals use this skill to convert session intake details into a structured draft note for pre-test, post-test, follow-up, supervisory review, EMR preparation, or billing workflows. The output is intended for licensed CGC review before clinical use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft counseling notes could be mistaken for final clinical documentation. <br>
Mitigation: Keep the draft-only label, CGC review block, and requirement for licensed CGC approval before EMR entry, billing use, patient release, or patient communication. <br>
Risk: Patient identifiers or family member names could be entered into an AI tool or included in generated notes. <br>
Mitigation: Use initials plus case number only, omit full names, dates of birth, MRNs, and family member names, and verify institutional HIPAA and BAA requirements before external-system use. <br>
Risk: Preliminary risk estimates, VUS handling, or result interpretation could be used without appropriate clinical judgment. <br>
Mitigation: Label all risk estimates as preliminary, never classify or reclassify VUS results, document lab-reported classifications only, and require licensed CGC or supervising clinical geneticist verification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/genetic-counseling-session-note) <br>
- [Feedback and contributions](https://github.com/archlab-space/Open-Skill-Hub/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Structured draft session note in Markdown-style sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes flagged review callouts and a CGC review block; draft-only clinical content requires licensed CGC approval.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and changelog, released 2026-05-31) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
