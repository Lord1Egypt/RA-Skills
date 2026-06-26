## Description: <br>
Generate medical documents from clinical notes. Input: patient info, symptoms, diagnosis. Output: SOAP notes, discharge summaries, referral letters, prescription drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinicians and healthcare staff use this skill to turn raw clinical notes into draft SOAP notes, discharge summaries, referral letters, and prescription drafts for review before EHR entry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patient-identifying or sensitive clinical information may be exposed through command-line arguments, shell history, process listings, or generated drafts. <br>
Mitigation: Use only in an approved clinical environment, avoid unnecessary real patient identifiers, and follow local privacy controls for generated drafts. <br>
Risk: Generated diagnoses, medication details, doses, interactions, or EHR-ready content may be clinically incomplete or incorrect. <br>
Mitigation: Have a licensed medical professional verify diagnoses, medications, doses, interactions, and all EHR content before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/loutai0307-prog/bytesagain-medical-scribe) <br>
- [BytesAgain feedback](https://bytesagain.com/feedback/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Structured plain text medical document drafts emitted by a Bash command-line script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-only output; licensed medical professional review is required before clinical use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
